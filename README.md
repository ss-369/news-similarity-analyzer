# Duplicate Article Detector

This application allows you to detect duplicate articles from RSS feeds using Named Entity Recognition (NER) and semantic similarity matching.

## Features

- Fetch articles from multiple RSS feeds
- Compare articles using three similarity methods:
  - Keyword-based similarity (TF-IDF with cosine similarity)
  - Named Entity Recognition (NER) comparison
  - Semantic similarity (using Google's Gemini API)
- Visual comparison of article similarity
- User-friendly web interface

## Setup

1. Clone the repository
2. Install the requirements:

```bash
pip install -r requirements.txt
```

3. Download the spaCy model:

```bash
python -m spacy download en_core_web_sm
```

4. Create a `.env` file with your Gemini API key:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

5. Run the application:

```bash
python app.py
```

6. Open a browser and navigate to `http://localhost:5000`

## How It Works

The application uses three methods to compare articles:

1. **Keyword Similarity**: Uses TF-IDF vectorization and cosine similarity to compare article content based on important keywords.

2. **Entity Similarity**: Extracts named entities (people, organizations, locations, etc.) from the articles using spaCy's NER capabilities and compares them using Jaccard similarity.

3. **Semantic Similarity**: Uses Google's Gemini API to compare the semantic meaning of the articles, providing a deeper understanding beyond simple keyword matching.

The final similarity score is a weighted combination of all three methods, with semantic similarity given slightly more weight.

## Usage

1. Enter RSS feed URLs or select from the default feeds
2. Click "Fetch Articles" to load articles from the feeds
3. Select two articles to compare
4. Click "Compare Selected Articles" to see the similarity analysis
5. Review the comparison results including the overall similarity score and individual method scores


