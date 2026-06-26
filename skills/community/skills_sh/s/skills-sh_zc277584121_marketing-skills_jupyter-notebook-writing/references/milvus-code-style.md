# Milvus Code Style Guidelines


## Installation

Install `pymilvus` and `milvus-lite` as **separate packages** — do NOT use the extras syntax:

```bash
# GOOD
pip install pymilvus milvus-lite

# BAD — do not use the extras bracket syntax
pip install "pymilvus[milvus_lite]"
```

The `pymilvus[milvus_lite]` extra is outdated and may pull in the wrong version. Always install them separately.

## API: Always Use MilvusClient (Not ORM)

pymilvus has two sets of APIs:

- **`MilvusClient`** (recommended) — the current, simplified interface. All new tutorials and examples should use this.
- **ORM layer** (`connections.connect()`, `Collection()`, `FieldSchema()`, `CollectionSchema()`, etc.) — the legacy interface. **Do not use ORM in new code.** It is verbose, harder to read, and no longer recommended.

If you see existing code using ORM patterns like `connections.connect()`, `Collection(name, schema)`, or `utility.has_collection()`, rewrite it to use `MilvusClient`.

### Quick comparison

```python
# BAD — ORM style (do not use)
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
connections.connect("default", host="localhost", port="19530")
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=768),
]
schema = CollectionSchema(fields)
collection = Collection("demo", schema)
collection.create_index("vector", {"index_type": "AUTOINDEX", "metric_type": "COSINE"})
collection.load()

# GOOD — MilvusClient style (always use this)
from pymilvus import MilvusClient
client = MilvusClient(uri="./milvus.db")
# ... see collection creation below
```


## Create Collection

Always define the schema explicitly so readers can see the data model clearly.

```python
from pymilvus import MilvusClient, DataType

client = MilvusClient(uri="./milvus.db")

schema = client.create_schema(auto_id=False, enable_dynamic_field=True)
schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=768)
schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=65535)

index_params = client.prepare_index_params()
index_params.add_index(
    field_name="id",
    index_type="AUTOINDEX"
)
index_params.add_index(
    field_name="vector",
    index_type="AUTOINDEX",
    metric_type="COSINE"
)

client.create_collection(collection_name="demo_collection", schema=schema, index_params=index_params)
```

**Always use `AUTOINDEX` as the index type.** It is compatible across Milvus Lite, Milvus server (Docker/K8s), and Zilliz Cloud, so notebooks work in all deployment modes without changing the index config.

In practice, you can specify different configurations for the schema and the index parameters depending on the scenario.

## Other format advice
- You'd better include a `has_collection` check before creating a collection to avoid creating a collection that already exists.
- You'd better add a comment line setting `consistency_level="Strong"` in the `create_collection()` method.
> ```python
> client.create_collection(
>     collection_name=collection_name,
>     dimension=5,
>     # Strong consistency waits for all loads to complete, adding latency with large datasets
>     # consistency_level="Strong", # Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`).
> )
> ```
  But if you find this description too verbose, you can just simply omit these lines.

- No need to explicitly load the collection using `load_collection()` after creating it, because the collection is loaded automatically when it is created.

- When the first time you connect to a Milvus server using uri or token, you need to provide the blockquote block for the explanation of the connection options, like this:
> As for the argument of `MilvusClient`:
> - Setting the `uri` as a local file, e.g.`./milvus.db`, is the most convenient method, as it automatically utilizes [Milvus Lite](https://milvus.io/docs/milvus_lite.md) to store all data in this file.
> - If you have large scale of data, you can set up a more performant Milvus server on [docker or kubernetes](https://milvus.io/docs/quickstart.md). In this setup, please use the server uri, e.g.`http://localhost:19530`, as your `uri`.
> - If you want to use [Zilliz Cloud](https://zilliz.com/cloud), the fully managed cloud service for Milvus, adjust the `uri` and `token`, which correspond to the [Public Endpoint and Api key](https://docs.zilliz.com/docs/on-zilliz-cloud-console#free-cluster-details) in Zilliz Cloud.
