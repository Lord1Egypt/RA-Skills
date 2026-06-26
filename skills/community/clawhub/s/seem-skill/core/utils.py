"""SEEM Skill Utilities
Includes: LLM client, Embedding encoder, BM25 retriever, Cache, etc.

Uses unified configuration from SEEM.config
"""

import json
import hashlib
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from functools import lru_cache
from collections import OrderedDict
import time
from datetime import datetime

# Import unified configuration
import sys
from pathlib import Path
skill_root = Path(__file__).parent.parent
sys.path.insert(0, str(skill_root))
from config import LLM_CONFIG, EMBEDDING_CONFIG

# Third-party libraries
try:
    from openai import OpenAI
    import requests
    from rank_bm25 import BM25Okapi
except ImportError as e:
    print(f"Warning: Missing dependencies. Install with: pip install openai requests rank-bm25")
    raise e


class LLMClient:
    """LLM API Client (OpenAI compatible)
    
    Uses unified configuration from config.LLM_CONFIG
    """
    
    def __init__(self, api_key: str, 
                 model: str = LLM_CONFIG["model"], 
                 base_url: Optional[str] = LLM_CONFIG["base_url"]):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
    
    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.1) -> str:
        """Generate text (JSON format output)"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")


class MMEmbedEncoder:
    """Multimodal Embedding Encoder (OpenAI compatible API)
    
    Uses unified configuration from config.EMBEDDING_CONFIG
    """
    
    def __init__(self, api_key: str, 
                 model: str = EMBEDDING_CONFIG["model"], 
                 base_url: Optional[str] = EMBEDDING_CONFIG["base_url"]):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url or EMBEDDING_CONFIG["base_url"]
        self.client = OpenAI(api_key=api_key, base_url=self.base_url)
        
    def encode_text(self, text: str) -> np.ndarray:
        """Encode text as vector"""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            embedding = response.data[0].embedding
            return np.array(embedding, dtype=np.float32)
        except Exception as e:
            raise Exception(f"Text embedding failed: {str(e)}")
    
    def encode_multimodal(self, text: str, image_path: Optional[str] = None) -> np.ndarray:
        """Encode multimodal input (text + image)"""
        # Currently using text-only encoding, multimodal support depends on API capability
        if not image_path:
            return self.encode_text(text)
        
        try:
            # Try to use multimodal-capable API
            # If API supports multimodal embedding, can extend this method
            # Currently fallback to text-only encoding
            import base64
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode("utf-8")
            
            # For APIs that support multimodal, can add image processing logic here
            # Currently using text-only encoding
            return self.encode_text(text)
        except Exception as e:
            # Fallback: text-only encoding
            print(f"Warning: Multimodal embedding failed, fallback to text-only: {str(e)}")
            return self.encode_text(text)


class BM25Retriever:
    """BM25 Sparse Retriever"""
    
    def __init__(self, documents: List[str]):
        """Initialize BM25, requires pre-built corpus"""
        from nltk.tokenize import word_tokenize
        try:
            # Try to download nltk resources
            import nltk
            nltk.download('punkt_tab', quiet=True)
            nltk.download('stopwords', quiet=True)
        except:
            pass
        
        # Tokenize
        tokenized_docs = [word_tokenize(doc.lower()) for doc in documents]
        self.bm25 = BM25Okapi(tokenized_docs)
        self.documents = documents
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[int, float]]:
        """Retrieve top-k documents"""
        from nltk.tokenize import word_tokenize
        
        query_tokens = word_tokenize(query.lower())
        scores = self.bm25.get_scores(query_tokens)
        
        # Get top-k indices and scores
        top_indices = np.argsort(scores)[-top_k:][::-1]
        results = [(idx, scores[idx]) for idx in top_indices if scores[idx] > 0]
        return results
    
    def add_document(self, document: str):
        """Add document (requires rebuilding index)"""
        self.documents.append(document)
        # Rebuild BM25
        from nltk.tokenize import word_tokenize
        tokenized_docs = [word_tokenize(doc.lower()) for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_docs)


class LRUCache:
    """LRU Cache (with TTL)"""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 300):
        self.cache = OrderedDict()
        self.timestamps = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached item"""
        if key not in self.cache:
            return None
        
        # Check TTL
        if time.time() - self.timestamps[key] > self.ttl_seconds:
            self.delete(key)
            return None
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: str, value: Any):
        """Store in cache"""
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        self.timestamps[key] = time.time()
        
        # Check size limit
        if len(self.cache) > self.max_size:
            oldest_key = next(iter(self.cache))
            self.delete(oldest_key)
    
    def delete(self, key: str):
        """Delete cached item"""
        if key in self.cache:
            del self.cache[key]
            del self.timestamps[key]
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.timestamps.clear()


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calculate cosine similarity"""
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (norm1 * norm2))


def batch_cosine_similarity(query_vec: np.ndarray, corpus_vec: np.ndarray) -> np.ndarray:
    """Batch calculate cosine similarity"""
    # corpus_vec: [N, D], query_vec: [D]
    norms = np.linalg.norm(corpus_vec, axis=1)
    norms[norms == 0] = 1e-10  # Avoid division by zero
    return np.dot(corpus_vec, query_vec) / norms


def generate_memory_id() -> str:
    """Generate unique memory ID"""
    timestamp = datetime.now().isoformat()
    return hashlib.md5(timestamp.encode()).hexdigest()[:16]


def format_structured_text(summary: str, events: List[Dict[str, Any]]) -> str:
    """Format structured text (for embedding)"""
    lines = [f"Summary: {summary}"]
    
    for i, event in enumerate(events, 1):
        lines.append(f"Event {i}:")
        if event.get('participants'):
            lines.append(f"  Participants: {', '.join(event['participants'])}")
        if event.get('action'):
            lines.append(f"  Action: {'; '.join(event['action'])}")
        if event.get('time'):
            lines.append(f"  Time: {event['time']}")
        if event.get('location'):
            lines.append(f"  Location: {event['location']}")
        if event.get('reason'):
            lines.append(f"  Reason: {event['reason']}")
        if event.get('method'):
            lines.append(f"  Method: {event['method']}")
    
    return "\n".join(lines)
