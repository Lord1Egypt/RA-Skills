#!/usr/bin/env python3
"""
Manage saved articles library: list, search, tag, organize.
"""

import sys
import json
import os
import re
from pathlib import Path
from datetime import datetime

LIBRARY_DIR = os.path.expanduser('~/.read-later-library')

class ArticleLibrary:
    def __init__(self, library_dir=LIBRARY_DIR):
        self.library_dir = library_dir
        os.makedirs(library_dir, exist_ok=True)
        self.index_file = os.path.join(library_dir, 'index.json')
        self.index = self._load_index()
    
    def _load_index(self):
        """Load the article index."""
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'articles': [], 'tags': {}}
    
    def _save_index(self):
        """Save the article index."""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    def _slugify(self, text):
        """Create a URL-friendly slug from text."""
        text = re.sub(r'[^\w\s-]', '', text.lower())
        text = re.sub(r'[-\s]+', '-', text)
        return text[:50]  # Limit length
    
    def add_article(self, metadata, content, tags=None):
        """Add a new article to the library."""
        slug = self._slugify(metadata.get('title', 'untitled'))
        article_dir = os.path.join(self.library_dir, slug)
        
        # Handle duplicates
        counter = 1
        original_slug = slug
        while os.path.exists(article_dir):
            slug = f"{original_slug}-{counter}"
            article_dir = os.path.join(self.library_dir, slug)
            counter += 1
        
        os.makedirs(article_dir, exist_ok=True)
        
        # Save metadata
        article_data = {
            'id': slug,
            'title': metadata.get('title', 'Untitled'),
            'url': metadata.get('url', ''),
            'author': metadata.get('author', ''),
            'date_saved': datetime.now().isoformat(),
            'date_published': metadata.get('date', ''),
            'word_count': metadata.get('word_count', 0),
            'tags': tags or [],
            'path': article_dir
        }
        
        with open(os.path.join(article_dir, 'metadata.json'), 'w', encoding='utf-8') as f:
            json.dump(article_data, f, ensure_ascii=False, indent=2)
        
        # Save content as markdown
        md_content = f"# {article_data['title']}\n\n"
        md_content += f"**Source:** [{article_data['url']}]({article_data['url']})  \n"
        if article_data['author']:
            md_content += f"**Author:** {article_data['author']}  \n"
        md_content += f"**Saved:** {article_data['date_saved']}  \n\n"
        md_content += "---\n\n"
        md_content += content
        
        with open(os.path.join(article_dir, 'article.md'), 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # Update index
        self.index['articles'].append(article_data)
        self._save_index()
        
        return article_data
    
    def list_articles(self, tag=None, limit=None):
        """List all articles, optionally filtered by tag."""
        articles = self.index['articles']
        
        if tag:
            articles = [a for a in articles if tag in a.get('tags', [])]
        
        # Sort by date saved (newest first)
        articles = sorted(articles, key=lambda x: x.get('date_saved', ''), reverse=True)
        
        if limit:
            articles = articles[:limit]
        
        return articles
    
    def search(self, query):
        """Search articles by title, content, or URL."""
        results = []
        query_lower = query.lower()
        
        for article in self.index['articles']:
            # Search in metadata
            if query_lower in article.get('title', '').lower():
                results.append(article)
                continue
            if query_lower in article.get('url', '').lower():
                results.append(article)
                continue
            
            # Search in content
            article_path = os.path.join(article['path'], 'article.md')
            if os.path.exists(article_path):
                try:
                    with open(article_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if query_lower in content.lower():
                            results.append(article)
                except:
                    pass
        
        return results
    
    def get_article(self, article_id):
        """Get a specific article by ID."""
        for article in self.index['articles']:
            if article['id'] == article_id:
                return article
        return None
    
    def delete_article(self, article_id):
        """Delete an article from the library."""
        article = self.get_article(article_id)
        if not article:
            return False
        
        # Remove from index
        self.index['articles'] = [a for a in self.index['articles'] if a['id'] != article_id]
        self._save_index()
        
        # Remove directory
        import shutil
        if os.path.exists(article['path']):
            shutil.rmtree(article['path'])
        
        return True
    
    def add_tags(self, article_id, tags):
        """Add tags to an article."""
        article = self.get_article(article_id)
        if not article:
            return False
        
        current_tags = set(article.get('tags', []))
        current_tags.update(tags)
        article['tags'] = list(current_tags)
        
        # Update metadata file
        metadata_file = os.path.join(article['path'], 'metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(article, f, ensure_ascii=False, indent=2)
        
        self._save_index()
        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: manage_library.py <command> [options]", file=sys.stderr)
        print("Commands: list, search, add, delete, tag", file=sys.stderr)
        sys.exit(1)
    
    command = sys.argv[1]
    library = ArticleLibrary()
    
    if command == 'list':
        tag = None
        limit = None
        
        for i, arg in enumerate(sys.argv[2:], 2):
            if arg == '--tag' and i + 1 < len(sys.argv):
                tag = sys.argv[i + 1]
            elif arg == '--limit' and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
        
        articles = library.list_articles(tag=tag, limit=limit)
        
        if not articles:
            print("No articles found.")
        else:
            print(f"\n{'ID':<30} {'Title':<50} {'Date':<20} {'Tags'}")
            print("-" * 120)
            for article in articles:
                title = article.get('title', 'Untitled')[:47] + '...' if len(article.get('title', '')) > 50 else article.get('title', 'Untitled')
                date = article.get('date_saved', '')[:19]
                tags = ', '.join(article.get('tags', []))
                print(f"{article['id']:<30} {title:<50} {date:<20} {tags}")
        
        print(f"\nTotal: {len(articles)} articles")
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("Usage: manage_library.py search <query>", file=sys.stderr)
            sys.exit(1)
        
        query = sys.argv[2]
        results = library.search(query)
        
        if not results:
            print(f"No articles found matching '{query}'.")
        else:
            print(f"\nFound {len(results)} articles matching '{query}':\n")
            for article in results:
                print(f"  {article['id']}: {article.get('title', 'Untitled')}")
    
    elif command == 'add':
        if len(sys.argv) < 4:
            print("Usage: manage_library.py add <metadata.json> <content.md>", file=sys.stderr)
            sys.exit(1)
        
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        with open(sys.argv[3], 'r', encoding='utf-8') as f:
            content = f.read()
        
        tags = []
        if '--tags' in sys.argv:
            idx = sys.argv.index('--tags')
            if idx + 1 < len(sys.argv):
                tags = sys.argv[idx + 1].split(',')
        
        article = library.add_article(metadata, content, tags)
        print(f"Added article: {article['id']}")
    
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Usage: manage_library.py delete <article-id>", file=sys.stderr)
            sys.exit(1)
        
        article_id = sys.argv[2]
        if library.delete_article(article_id):
            print(f"Deleted article: {article_id}")
        else:
            print(f"Article not found: {article_id}", file=sys.stderr)
            sys.exit(1)
    
    elif command == 'tag':
        if len(sys.argv) < 4:
            print("Usage: manage_library.py tag <article-id> <tag1,tag2,...>", file=sys.stderr)
            sys.exit(1)
        
        article_id = sys.argv[2]
        tags = sys.argv[3].split(',')
        
        if library.add_tags(article_id, tags):
            print(f"Added tags to {article_id}: {', '.join(tags)}")
        else:
            print(f"Article not found: {article_id}", file=sys.stderr)
            sys.exit(1)
    
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
