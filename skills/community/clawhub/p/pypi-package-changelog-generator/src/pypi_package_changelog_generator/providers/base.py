from __future__ import annotations

from abc import ABC, abstractmethod


class ProviderError(RuntimeError):
    def __init__(self, code: str, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable


class RepositoryProvider(ABC):
    @abstractmethod
    def compare_versions(
        self, repo_url: str, from_version: str, to_version: str
    ) -> dict:
        raise NotImplementedError
