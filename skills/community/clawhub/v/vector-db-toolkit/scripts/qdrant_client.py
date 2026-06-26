"""
Qdrant-specific vector client wrapper.
"""
from typing import List, Dict, Any, Optional

try:
    from qdrant_client import QdrantClient
except ImportError:
    QdrantClient = None

class QdrantVectorClient:
    def __init__(self, url: str = "http://localhost:6333", api_key: Optional[str] = None):
        if QdrantClient is None:
            raise ImportError("qdrant-client not installed. Run: pip install qdrant-client")
        self.client = QdrantClient(url=url, api_key=api_key)

    def create_collection(self, name: str, dimension: int, distance: str = "COSINE", **kwargs):
        from qdrant_client.models import Distance, VectorParams
        dist = Distance.COSINE if distance == "COSINE" else Distance.EUCLID
        self.client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=dimension, distance=dist),
        )
        return True

    def upsert(self, collection: str, ids: List[str], vectors: List[List[float]], payloads: Optional[List[Dict]] = None):
        from qdrant_client.models import PointStruct
        points = [
            PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i] if payloads else {})
            for i in range(len(ids))
        ]
        self.client.upsert(collection_name=collection, points=points)
        return True

    def search(self, collection: str, vector: List[float], top_k: int = 5, filter_dict: Optional[Dict] = None):
        kwargs = {"collection_name": collection, "vector": vector, "limit": top_k}
        if filter_dict:
            from qdrant_client.models import FieldCondition, MatchValue, Filter
            conditions = [FieldCondition(key=k, match=MatchValue(v=v)) for k, v in filter_dict.items()]
            kwargs["query_filter"] = Filter(must=conditions)
        results = self.client.search(**kwargs)
        return [{"id": r.id, "score": r.score, "payload": r.payload} for r in results]

    def delete(self, collection: str, ids: Optional[List[str]] = None):
        if ids:
            from qdrant_client.models import PointIdsList
            self.client.delete(collection_name=collection, points_selector=PointIdsList(points=ids))
        else:
            self.client.delete_collection(collection_name=collection)
        return True

    def list_collections(self):
        return [c.name for c in self.client.get_collections().collections]
