# WeryAI Podcast Runtime

Shared runtime for WeryAI podcast generation skills.

Responsibilities:

- list podcast speakers
- submit podcast text generation
- trigger podcast audio generation
- query podcast task state
- wait across the text -> audio lifecycle

This runtime reuses `core/weryai-core` for auth, HTTP, retries, and shared error mapping.
