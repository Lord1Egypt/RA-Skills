# Chroma API Patterns

## Collection Management

```python
client.create_collection("my-collection", dimension=768)
client.list_collections()
client.delete("my-collection")  # deletes entire collection
```

## Document Operations

```python
client.upsert("my-collection", ids=["doc1"], vectors=[[0.1]*768], payloads=[{"source": "web"}])
client.delete("my-collection", ids=["doc1"])
```

## Query Patterns

```python
# Simple query
results = client.search("my-collection", vector=[0.1]*768, top_k=10)

# Metadata filter
results = client.search("my-collection", vector=[0.1]*768, top_k=10, filter_dict={"source": "web"})
```

## Notes

- Chroma distances are L2 by default (not cosine). Use `collection.query` with `n_results`.
- PersistentClient stores data on disk; EphemeralClient is in-memory.
- HttpClient connects to Chroma server.
