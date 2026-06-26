# SurrealML -- Machine Learning Models in SurrealDB

> **v1.6.6 status note:** v1.4.1 retracted the v1.4.0 documentation of
> `DEFINE MODEL ml::name<version>(...)`, `INFO FOR MODEL`, `REMOVE
> MODEL`, `ml::name<version>(...)` invocation, `surreal start
> --user-mem-limit`, `surreal ml import`, `db.upload_ml(...)`, and the
> `SurMlFile.from_pytorch / from_onnx / from_sklearn / from_keras /
> from_hf` factories -- none of those exist upstream. This rule documents
> the **actual** `SurMlFile` constructor + builder API
> verified against the published `surrealml 0.0.4` wheel
> (`surrealml/__init__.py`, `surrealml/surml_file.py`,
> `surrealml/engine/__init__.py`). The SurrealDB-side surface
> (server-side load, SurrealQL invocation form, CLI subcommand) remains
> unstable and is not documented here -- track upstream directly.

SurrealML is the SurrealDB project for storing and serving machine
learning models. The package compiles to a `.surml` artifact format
that bundles an ONNX graph plus metadata, intended to be loadable
into a SurrealDB server and invokable from queries.

- Upstream: `https://github.com/surrealdb/surrealml`
- GitHub release: `v0.1.2` (2025-04-29; Rust/C core + dynamic-library assets)
- PyPI: `https://pypi.org/project/surrealml/` (v0.0.4 remains the latest
  published Python package as of 2026-05-14)
- Status: early-stage / preview -- API and SurrealQL surface are not
  stable; treat anything below as a pointer, not a contract

---

## Current Reality (verified 2026-05-14)

- The PyPI package `surrealml 0.0.4` exists. Its extras are
  `[sklearn]`, `[torch]`, `[tensorflow]` -- there is no `[hf]` extra.
  Pinned deps include `numpy==1.26.3`.
- The GitHub repo has moved beyond the PyPI package. Current upstream
  `clients/python/setup.py` reports a Python package line driven by
  `config.json` and downloads precompiled dynamic C libraries from GitHub
  Releases into `~/surrealml_deps` during package setup unless
  `LOCAL_BUILD=TRUE`. That is a real supply-chain and reproducibility boundary:
  pin the GitHub release, review the setup script, and avoid source installs in
  locked-down production builders until upstream publishes a stable package with
  a documented artifact-verification story.
- The newer Rust workspace splits `modules/core`, `modules/c-wrapper`,
  `modules/tokenizers`, `modules/llms`, `modules/wasm-linker`, and
  `modules/transformers`, with ONNX Runtime pinned at `2.0.0-rc.9` and
  Candle/tokenizer dependencies for future local model work. Treat this as
  upstream implementation detail unless you are contributing to SurrealML.
- The package's Python API uses an `Engine` enum and builder methods
  on a `SurMlFile` (verified against the upstream `clients/python`
  source); it does **not** expose the `from_pytorch / from_onnx /
  from_sklearn / from_keras / from_hf` factory methods that v1.4.0
  documented.
- The SurrealDB `DEFINE` statement list does **not** include `MODEL`.
  Any rule, plan, or example that uses `DEFINE MODEL`, `INFO FOR
  MODEL`, `REMOVE MODEL`, or an `ml::name<version>(...)` call site is
  not portable to current upstream. Verify against
  `https://surrealdb.com/docs/surrealql/statements/define` before
  copying any such snippet.
- The `surreal ml` CLI root page exists at
  `https://surrealdb.com/docs/surrealdb/cli/ml`, but `/import` and
  `/export` subpages still 404 at the v1.6.6 cut. Treat the CLI surface as
  a moving target.

### Registry vs GitHub release boundary

Do not conflate these:

| Surface | Current verified state |
|---------|------------------------|
| PyPI `surrealml` | `0.0.4`, direct Python package, NumPy `1.26.3`, extras `[sklearn]`, `[torch]`, `[tensorflow]` |
| GitHub `surrealdb/surrealml` | `v0.1.2`, Rust/C core, dynamic-library download/install flow, Python client under `clients/python` |
| SurrealDB server / SurrealQL | No stable `DEFINE MODEL`, `INFO FOR MODEL`, `REMOVE MODEL`, or `ml::name<version>(...)` invocation documented here |

For application guidance, default to PyPI `0.0.4` unless you explicitly need
the newer GitHub core and have reviewed the setup-time binary download path.

---

## When to Reach for SurrealML

If your data lives in SurrealDB and you want a model to score it
without leaving the database -- yes. If you serve a single model
behind a high-QPS HTTP API with no DB coupling, keep the model in a
dedicated serving runtime (Triton, Ray Serve, BentoML).

The promise is *colocation*: model + features + downstream record
in the same engine.

---

## Python API (verified at `surrealml 0.0.4`)

### Engine enum

`from surrealml import Engine` exposes:

| Variant | String value | Notes |
|---------|--------------|-------|
| `Engine.PYTORCH` | `"pytorch"` | PyTorch model exported through ONNX |
| `Engine.SKLEARN` | `"sklearn"` | scikit-learn model exported through ONNX (skl2onnx) |
| `Engine.TENSORFLOW` | `"tensorflow"` | TensorFlow / Keras model exported through ONNX (tf2onnx) |
| `Engine.ONNX` | `"onnx"` | An already-ONNX graph; bypasses conversion |
| `Engine.NATIVE` | `"native"` | Rust + linfa native engine (declared on the enum but **unsupported in the v0.0.4 Python serializer** -- `_cache_model` raises `ValueError("Engine native not supported")`) |

`SKLEARN` requires the `[sklearn]` extra, `PYTORCH` requires `[torch]`,
and `TENSORFLOW` requires `[tensorflow]`. `numpy==1.26.3` is pinned
hard at the package level.

### `SurMlFile` constructor + builder

```python
from surrealml import SurMlFile, Engine

file = SurMlFile(
    model=trained_model,   # any sklearn / torch / tf / onnx instance
    name="house_price",    # string, becomes the artefact name
    inputs=X_sample,       # shape-defining sample (used to trace the model)
    engine=Engine.SKLEARN,
)
```

All four constructor args are optional in the signature; the only
supported "construct empty + load later" form passes **none of them**
and then calls `SurMlFile.load(path, engine)`. Any other partial
combination triggers the `_cache_model` engine match and either
serialises immediately or raises `ValueError`.

Builder methods on the instance (each returns `None`; mutate in place):

| Method | Purpose |
|--------|---------|
| `add_column(name)` | Append a feature-column name. Order matters; call once per column in input order. |
| `add_normaliser(column_name, normaliser_type, one, two)` | Attach a normaliser to a previously-added column. `one` / `two` are the two parameters consumed by the named normaliser. |
| `add_output(output_name, normaliser_type, one, two)` | Same shape as `add_normaliser` but for an output of the model. |
| `add_description(description: str)` | Sets `self.description` and embeds it in the `.surml` header. |
| `add_version(version: str)` | Sets `self.version`. |
| `add_name(name: str)` | Re-sets the artefact name after construction. |
| `add_author(author)` | Sets the author metadata. |
| `save(path)` | Writes the configured artefact to `path` (e.g. `model.surml`). |
| `to_bytes()` | Returns the serialised artefact bytes (alternative to `save`). |

Metadata-loading + remote-upload entry points:

| Method | Signature | Purpose |
|--------|-----------|---------|
| `SurMlFile.load(path, engine)` (static) | `(path: str, engine: Engine) -> SurMlFile` | Reconstructs `(file_id, name, description, version)` from disk and rebinds the engine. |
| `SurMlFile.upload(path, url, chunk_size, namespace, database, username=None, password=None)` (static) | -- | Streams a `.surml` file to a remote endpoint in chunks of `chunk_size` bytes; `username` / `password` are the SurrealDB-side credentials used to authenticate the upload. |

Inference entry points:

| Method | Signature | Purpose |
|--------|-----------|---------|
| `raw_compute(input_vector, dims=None)` | `(list[float], Optional[list[int]]) -> ...` | One-shot inference from a flat 1-D input vector; `dims` describes how to slice it before feeding the model. |
| `buffered_compute(value_map)` | `(dict[str, float]) -> ...` | One-shot inference from a column-name → value mapping. Requires `add_column` to have been called for every key. |

### What the API does NOT expose

These were claimed in the v1.4.0 rule and **are not present** in
`surrealml 0.0.4`:

- `SurMlFile.from_pytorch()`, `.from_onnx()`, `.from_sklearn()`,
  `.from_keras()`, `.from_hf()` -- there are no `from_*` factory
  methods. Use the constructor with `engine=Engine.<...>`.
- A `ModelMeta` class -- metadata is set field-by-field via the
  `add_*` builder methods.
- Any HuggingFace integration / `[hf]` extra -- only `[sklearn]`,
  `[torch]`, `[tensorflow]` exist.

### What the SurrealDB side does NOT (yet) expose

These were also in the v1.4.0 rule and remain unverified upstream at
the v1.6.6 cut:

- `DEFINE MODEL ml::name<version>(...)` SurrealQL statement.
- `INFO FOR MODEL` / `REMOVE MODEL` statements.
- `ml::name<version>(...)` invocation form inside SurrealQL.
- `surreal ml import` / `surreal ml export` CLI subcommands -- the
  `surreal ml` root page exists at
  `https://surrealdb.com/docs/surrealdb/cli/ml`, but `/import` and
  `/export` 404 as of 2026-05-14.
- `db.upload_ml(...)` SDK method on the JS / Rust / Go clients.

If you need server-side model invocation today, push the model out via
`SurMlFile.upload(...)` and then drive inference from your application
code over the regular SDK -- not from inside SurrealQL.

---

## Composing With Other SurrealDB Surfaces

The patterns below are stable and don't depend on `DEFINE MODEL`:

### Vector indexes for embeddings

```surql
DEFINE TABLE document SCHEMAFULL;
DEFINE FIELD content   ON TABLE document TYPE string;
DEFINE FIELD embedding ON TABLE document TYPE array<float>;
DEFINE INDEX idx_doc_embedding ON TABLE document FIELDS embedding
  HNSW DIMENSION 384 DIST COSINE;
```

For the supported vector-index types and dimensions, see
`rules/vector-search.md`. MTREE was removed in v3.

### Computing embeddings server-side via DEFINE EVENT

If your eventual goal is to invoke a model server-side from an
event, today the practical path is:

1. Compute the embedding client-side (or via a SurrealDB function
   you've defined).
2. `UPDATE` the record with the embedding in the same transaction
   that created it.

The standard event-variable convention in SurrealDB is `$before`,
`$after`, and `$event`. Use `$after` (or `$after.id`) when writing
back to the record, not `$value`.

```surql
DEFINE EVENT compute_embedding ON TABLE document WHEN $event = "CREATE" THEN {
  UPDATE $after.id SET embedding = fn::compute_embedding($after.content);
};
```

`fn::compute_embedding` here is a placeholder for whatever surface
ends up exposing your model -- a Surrealism extension, a stable
SurrealML invocation form once the upstream API lands, or a
client-side write before insert.

---

## Cross-References

- `rules/vector-search.md` -- HNSW, dimensions, distance metrics
- `rules/data-modeling.md` -- computed fields, events, schemafull tables
- `rules/surrealism.md` -- Rust-based extensions (composes with SurrealML once it stabilizes)
- `rules/surrealkit.md` -- rollout-managed schema upgrades
- `rules/security.md` -- record-level permissions
- `rules/langchain.md` -- LangChain pipelines that produce embeddings
- Upstream: `https://github.com/surrealdb/surrealml`
- Upstream docs portal: `https://surrealdb.com/docs/`
