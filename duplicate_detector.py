import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import numpy as np

class DuplicateDetector:
    def __init__(self, gemini_api_key=None):
        # Load spaCy model for NER
        self.nlp = spacy.load('en_core_web_sm')
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # Set up Gemini API if key is provided
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            # Configure the model
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None

    def extract_entities(self, text):
        """Extract named entities from text"""
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_
            })
            
        return entities
    
    def compare_entity_similarity(self, text1, text2):
        """Compare two texts based on their named entities"""
        entities1 = self.extract_entities(text1)
        entities2 = self.extract_entities(text2)
        
        if not entities1 or not entities2:
            return 0.0
            
        # Extract entity texts
        entity_texts1 = set(e['text'].lower() for e in entities1)
        entity_texts2 = set(e['text'].lower() for e in entities2)
        
        # Calculate Jaccard similarity
        intersection = len(entity_texts1.intersection(entity_texts2))
        union = len(entity_texts1.union(entity_texts2))
        
        return intersection / union if union > 0 else 0.0
    
    def compare_keyword_similarity(self, text1, text2):
        """Compare two texts based on TF-IDF and cosine similarity"""
        try:
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            print(f"Error in keyword similarity: {str(e)}")
            return 0.0
    
    def compare_semantic_similarity(self, text1, text2):
        """Compare semantic similarity using Gemini API"""
        if not self.model:
            # Fall back to keyword similarity if Gemini API is not available
            return self.compare_keyword_similarity(text1, text2)
        
        try:
            prompt = f"""
            I have two article texts. Please determine their semantic similarity on a scale of 0.0 to 1.0, 
            where 1.0 means they are duplicates or cover exactly the same content, and 0.0 means they are completely different.
            Only respond with a single number between 0 and 1.
            
            Article 1:
            {text1[:1000]}
            
            Article 2:
            {text2[:1000]}
            """
            
            response = self.model.generate_content(prompt)
            # Extract the numeric value from the response
            try:
                similarity = float(response.text.strip())
                # Ensure the value is between 0 and 1
                similarity = max(0.0, min(1.0, similarity))
                return similarity
            except ValueError:
                # If we can't parse the response as a float, default to keyword similarity
                return self.compare_keyword_similarity(text1, text2)
                
        except Exception as e:
            print(f"Error in semantic similarity: {str(e)}")
            # Fall back to keyword similarity
            return self.compare_keyword_similarity(text1, text2)
