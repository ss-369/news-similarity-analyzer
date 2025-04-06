import feedparser
import html
import re

class RSSFetcher:
    def __init__(self):
        # Common RSS feed URLs can be added as defaults
        self.default_feeds = [
            'http://feeds.bbci.co.uk/news/world/rss.xml',
            'http://rss.cnn.com/rss/edition.rss',
            'https://www.theguardian.com/world/rss'
        ]
    
    def fetch_feed(self, url):
        """Fetch and parse an RSS feed from the given URL"""
        try:
            feed = feedparser.parse(url)
            articles = []
            
            for entry in feed.entries:
                # Extract article data
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': self._clean_html(entry.get('summary', ''))
                }
                
                # If summary is too short, try to get content
                if len(article['summary']) < 50 and 'content' in entry:
                    article['summary'] = self._clean_html(entry.content[0].value)
                
                articles.append(article)
                
            return articles
        
        except Exception as e:
            print(f"Error fetching feed {url}: {str(e)}")
            return []
    
    def get_default_feeds(self):
        """Return a list of default feeds"""
        return self.default_feeds
    
    def _clean_html(self, text):
        """Remove HTML tags and decode entities"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Decode HTML entities
        text = html.unescape(text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
