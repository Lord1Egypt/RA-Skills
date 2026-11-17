# Security

## Scope

`xhs-knowledge-retriever` is a read-oriented local retrieval helper. It loads a local RAG index and writes JSON only when the caller explicitly passes `--output`.

## Data Access

- Reads local files under the configured XHS knowledge root:
  - `05-competitors/rag/index.json`
  - `05-competitors/rag/embeddings.npy`
  - `05-competitors/rag/metadata.jsonl`
- Does not read credential files, shell profiles, browser storage, SSH keys, or arbitrary home-directory paths by default.
- Optional `--index-dir` and `--output` paths are caller-controlled CLI arguments and should be used with trusted local paths.

## Network

The script contains no direct network, browser, or API client calls.

`sentence-transformers` may consult its local model cache. If the requested embedding model is absent, that third-party library can attempt a model download depending on the user environment. For fully offline operation, pre-cache the model used by `index.json` before running retrieval.

## Execution

- No `eval`.
- No shell execution.
- No child-process calls.
- No dynamic code loading.

## Dependencies

Runtime Python dependencies are listed in `requirements.txt`:

- `numpy`
- `sentence-transformers`

No npm package is required for this Skill.

## Reporting

If you find a security issue, hide the affected ClawHub release if already published, fix the issue, bump the version, and publish a patched release.
