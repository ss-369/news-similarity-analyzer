from flask import Flask, render_template, request, jsonify
from duplicate_detector import DuplicateDetector
from rss_fetcher import RSSFetcher
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
rss_fetcher = RSSFetcher()
detector = DuplicateDetector(gemini_api_key=os.getenv('GEMINI_API_KEY'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch-feeds', methods=['POST'])
def fetch_feeds():
    data = request.json
    feed_urls = data.get('feed_urls', [])
    
    all_articles = []
    for url in feed_urls:
        articles = rss_fetcher.fetch_feed(url)
        all_articles.extend(articles)
    
    return jsonify({'articles': all_articles})

@app.route('/compare-articles', methods=['POST'])
def compare_articles():
    data = request.json
    article1 = data.get('article1', {})
    article2 = data.get('article2', {})
    
    # Compare using both methods
    keyword_similarity = detector.compare_keyword_similarity(
        article1.get('title', '') + ' ' + article1.get('summary', ''),
        article2.get('title', '') + ' ' + article2.get('summary', '')
    )
    
    entity_similarity = detector.compare_entity_similarity(
        article1.get('title', '') + ' ' + article1.get('summary', ''),
        article2.get('title', '') + ' ' + article2.get('summary', '')
    )
    
    semantic_similarity = detector.compare_semantic_similarity(
        article1.get('title', '') + ' ' + article1.get('summary', ''),
        article2.get('title', '') + ' ' + article2.get('summary', '')
    )
    
    # Combine scores with weighted average
    combined_score = 0.2 * keyword_similarity + 0.2 * entity_similarity + 0.6 * semantic_similarity
    is_duplicate = combined_score > 0.9  # Threshold for considering as duplicate
    
    return jsonify({
        'is_duplicate': is_duplicate,
        'similarity_score': combined_score,
        'keyword_similarity': keyword_similarity,
        'entity_similarity': entity_similarity,
        'semantic_similarity': semantic_similarity
    })

if __name__ == '__main__':
    # Download spaCy model if not already installed
    import spacy
    try:
        spacy.load('en_core_web_sm')
    except:
        import subprocess
        subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])
    
    app.run(debug=True)
