"""
Unit tests for vector-db-toolkit.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../scripts"))

import unittest
from vector_client import VectorClient
from embedding_utils import EmbeddingProvider

class TestVectorClient(unittest.TestCase):
    def test_memory_create_collection(self):
        c = VectorClient(backend="memory")
        self.assertTrue(c.create_collection("test", dimension=10))
        self.assertIn("test", c.list_collections())

    def test_memory_upsert_and_search(self):
        c = VectorClient(backend="memory")
        c.create_collection("test", dimension=3)
        c.upsert("test", ids=["1", "2"], vectors=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        results = c.search("test", vector=[1.0, 0.0, 0.0], top_k=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "1")

    def test_memory_delete(self):
        c = VectorClient(backend="memory")
        c.create_collection("test", dimension=2)
        c.upsert("test", ids=["x"], vectors=[[1.0, 1.0]])
        c.delete("test", ids=["x"])
        results = c.search("test", vector=[1.0, 1.0], top_k=1)
        self.assertEqual(len(results), 0)

    def test_memory_payload_filter(self):
        c = VectorClient(backend="memory")
        c.create_collection("test", dimension=2)
        c.upsert("test", ids=["a", "b"], vectors=[[1.0, 0.0], [1.0, 0.0]], payloads=[{"tag": "x"}, {"tag": "y"}])
        results = c.search("test", vector=[1.0, 0.0], top_k=5, filter_dict={"tag": "x"})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "a")

class TestEmbeddingProvider(unittest.TestCase):
    def test_fallback_encode(self):
        p = EmbeddingProvider(provider="fallback")
        embs = p.encode(["hello", "world"])
        self.assertEqual(len(embs), 2)
        self.assertEqual(len(embs[0]), 384)

if __name__ == "__main__":
    unittest.main()
