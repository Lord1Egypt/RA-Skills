#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from search import get_searcher

searcher = get_searcher()

# Test query
query = "瀑布"
print(f"Testing query: {query}")

# Get embedding
embedding = searcher.embeddings.embed_query(query)
print(f"Embedding dimension: {len(embedding)}")
print(f"Embedding preview: {embedding[:5]}")

# Try different search methods
print("\n--- Method 1: similarity_search ---")
try:
    results = searcher.vectorstore.similarity_search(query, k=5)
    print(f"Found {len(results)} results")
    for i, doc in enumerate(results):
        print(f"{i+1}. {doc.metadata.get('filename', 'Unknown')} - {doc.page_content[:100]}")
except Exception as e:
    print(f"Error: {e}")

print("\n--- Method 2: similarity_search_with_score ---")
try:
    results = searcher.vectorstore.similarity_search_with_score(query, k=5)
    print(f"Found {len(results)} results")
    for i, (doc, score) in enumerate(results):
        print(f"{i+1}. {doc.metadata.get('filename', 'Unknown')} - score: {score}")
except Exception as e:
    print(f"Error: {e}")

print("\n--- Method 3: similarity_search_by_vector ---")
try:
    results = searcher.vectorstore.similarity_search_by_vector(embedding, k=5)
    print(f"Found {len(results)} results")
    for i, doc in enumerate(results):
        print(f"{i+1}. {doc.metadata.get('filename', 'Unknown')} - {doc.page_content[:100]}")
except Exception as e:
    print(f"Error: {e}")

print("\n--- Method 4: collection.query ---")
try:
    collection = searcher.vectorstore._collection
    query_result = collection.query(query_embeddings=[embedding], n_results=5)
    print(f"Found {len(query_result['ids'][0])} results")
    for i, doc_id in enumerate(query_result['ids'][0]):
        print(f"{i+1}. ID: {doc_id}")
        if query_result['documents'] and query_result['documents'][0]:
            print(f"    {query_result['documents'][0][i][:100]}")
        if query_result['distances'] and query_result['distances'][0]:
            print(f"    Distance: {query_result['distances'][0][i]}")
except Exception as e:
    print(f"Error: {e}")
