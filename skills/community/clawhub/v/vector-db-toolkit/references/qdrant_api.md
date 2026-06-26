# Qdrant API Patterns

## Collection Management

```python
client.create_collection("my-collection", dimension=768, distance="COSINE")
client.list_collections()
client.delete("my-collection")  # deletes entire collection
```

## Point Operations

```python
client.upsert("my-collection", ids=["id1"], vectors=[[0.1]*768], payloads=[{"key": "val"}])
client.delete("my-collection", ids=["id1"])
```

## Search Patterns

```python
# Simple search
results = client.search("my-collection", vector=[0.1]*768, top_k=10)

# Filtered search
results = client.search("my-collection", vector=[0.1]*768, top_k=10, filter_dict={"status": "active"})
```

## Payload Filtering Syntax

Qdrant uses FieldCondition + MatchValue for equality filters.
See Qdrant docs for range, geo, and keyword filters.
