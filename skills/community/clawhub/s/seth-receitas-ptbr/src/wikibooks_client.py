#!/usr/bin/env python3
"""
Wikibooks Client - MediaWiki API client for pt.wikibooks.org
"""

import json
import urllib.request
import urllib.parse
from typing import List, Dict, Optional


class WikibooksClient:
    BASE_URL = "https://pt.wikibooks.org/w/api.php"
    
    # Categorias de receitas
    CATEGORIES = [
        "Categoria:Receitas",
        "Categoria:Livro/Livro de receitas",
        "Categoria:Receitas por ingredientes",
        "Categoria:Bolos",
        "Categoria:Bebidas",
        "Categoria:Salgados",
        "Categoria:Doces",
    ]
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
    
    def _request(self, params: Dict) -> Dict:
        """Make request to MediaWiki API"""
        params["format"] = "json"
        query_string = urllib.parse.urlencode(params)
        url = f"{self.BASE_URL}?{query_string}"
        
        try:
            with urllib.request.urlopen(url, timeout=self.timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            return {"error": str(e)}
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for recipes using OpenSearch"""
        params = {
            "action": "opensearch",
            "search": query,
            "limit": limit,
            "namespace": 0,
            "language": "pt"
        }
        
        result = self._request(params)
        
        if "error" in result:
            return []
        
        # OpenSearch returns [query, titles, descriptions, urls]
        if len(result) >= 2:
            titles = result[1]
            descriptions = result[2] if len(result) > 2 else []
            urls = result[3] if len(result) > 3 else []
            
            recipes = []
            for i, title in enumerate(titles):
                recipes.append({
                    "title": title,
                    "description": descriptions[i] if i < len(descriptions) else "",
                    "url": urls[i] if i < len(urls) else f"https://pt.wikibooks.org/wiki/{urllib.parse.quote(title)}",
                    "source": "wikibooks"
                })
            return recipes
        
        return []
    
    def get_category_recipes(self, category: str, limit: int = 50) -> List[Dict]:
        """Get all recipes in a category"""
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": category,
            "cmlimit": limit,
            "cmtype": "page"
        }
        
        result = self._request(params)
        
        if "error" in result or "query" not in result:
            return []
        
        members = result.get("query", {}).get("categorymembers", [])
        
        recipes = []
        for member in members:
            title = member.get("title", "")
            pageid = member.get("pageid", 0)
            url = f"https://pt.wikibooks.org/wiki/{urllib.parse.quote(title)}"
            
            recipes.append({
                "title": title,
                "pageid": pageid,
                "url": url,
                "source": "wikibooks",
                "category": category
            })
        
        return recipes
    
    def get_all_categories(self, limit: int = 100) -> List[str]:
        """Get all recipe categories"""
        all_recipes = []
        
        for cat in self.CATEGORIES:
            recipes = self.get_category_recipes(cat, limit)
            all_recipes.extend(recipes)
        
        return all_recipes
    
    def get_page_content(self, title: str) -> Optional[str]:
        """Get raw HTML content of a page"""
        params = {
            "action": "parse",
            "page": title,
            "prop": "text",
            "disableeditsection": "true"
        }
        
        result = self._request(params)
        
        if "error" in result or "parse" not in result:
            return None
        
        return result.get("parse", {}).get("text", {}).get("*", "")


# Test if run directly
if __name__ == "__main__":
    client = WikibooksClient()
    
    print("🔍 Testando busca...")
    results = client.search("bolo", 5)
    for r in results:
        print(f"  - {r['title']}")
    
    print("\n📂 Testando categorias...")
    cats = client.get_category_recipes("Categoria:Bolos", 5)
    for c in cats:
        print(f"  - {c['title']}")
