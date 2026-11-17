"""Native provider adapters. Each adapter returns plaintext only to the in-process writer."""

from secret_drop.providers.registry import retrieve_secret

__all__ = ["retrieve_secret"]
