# Google search module - adapted from public source
import os
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    relevance_score: float = 0.0

class SearchClient:
    def __init__(self, api_key: str = None, search_engine_id: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.search_engine_id = search_engine_id or os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        
        if not self.api_key or not self.search_engine_id:
            raise ValueError("GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID environment variables must be set")
    
    def search_image_content(self, image_description: str, num_results: int = 5) -> List[SearchResult]:
        """Search for information about image content"""
        query = f"{image_description} information reference"
        return self._search(query, num_results)
    
    def _search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        url = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.search_engine_id}&q={query}&num={min(num_results, 10)}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            items = data.get("items", [])
            results = []
            
            for i, item in enumerate(items):
                # Simple relevance scoring based on position
                relevance = 1.0 - (i * 0.1)
                
                results.append(SearchResult(
                    title=item.get("title", ""),
                    url=item.get("link", ""),
                    snippet=item.get("snippet", ""),
                    relevance_score=relevance
                ))
            
            return results
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Search failed: {str(e)}") from e