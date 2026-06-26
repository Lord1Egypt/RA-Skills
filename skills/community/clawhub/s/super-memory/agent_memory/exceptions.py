"""exceptions.py — Agent Memory 异常类

所有异常统一继承自 AgentMemoryError（来自 ._errors），
不再使用 MemoryError 以避免与 Python 内置 MemoryError 冲突。

为保持向后兼容，重新导出 ._errors 中的所有异常类。
"""

from ._errors import (
    AgentMemoryError,
    AuthenticationError,
    ConfigurationError,
    DatabaseError,
    DependencyError,
    MemoryNotFoundError,
    PermissionDeniedError,
    RateLimitError,
)

__all__ = [
    "AgentMemoryError",
    "AuthenticationError",
    "ConfigurationError",
    "DatabaseError",
    "DependencyError",
    "MemoryNotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "StorageError",
    "DuplicateMemoryError",
    "FilterRejectedError",
    "DeduplicationError",
    "CooldownError",
    "MemoryPermissionError",
    "ValidationError",
    "LLMError",
    "EmbeddingError",
    "SyncError",
    "FederationError",
]


class StorageError(AgentMemoryError):
    """Database/storage operation failed."""
    def __init__(self, message: str = "Storage operation failed"):
        super().__init__(message)

class DuplicateMemoryError(AgentMemoryError):
    """Memory with same content/hash already exists."""
    def __init__(self, message: str = "Duplicate memory detected"):
        super().__init__(message)

class FilterRejectedError(AgentMemoryError):
    """Content rejected by memory filter."""
    def __init__(self, message: str = "Content rejected by filter"):
        super().__init__(message)

class DeduplicationError(AgentMemoryError):
    """Deduplication check failed."""
    def __init__(self, message: str = "Deduplication check failed"):
        super().__init__(message)

class CooldownError(AgentMemoryError):
    """Topic write cooldown active."""
    def __init__(self, message: str = "Topic write cooldown active"):
        super().__init__(message)

class MemoryPermissionError(AgentMemoryError):
    """Insufficient permissions."""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message)

class ValidationError(AgentMemoryError):
    """Input validation failed."""
    def __init__(self, message: str = "Input validation failed"):
        super().__init__(message)

class LLMError(AgentMemoryError):
    """LLM call failed or timed out."""
    def __init__(self, message: str = "LLM call failed or timed out"):
        super().__init__(message)

class EmbeddingError(AgentMemoryError):
    """Embedding computation failed."""
    def __init__(self, message: str = "Embedding computation failed"):
        super().__init__(message)

class SyncError(AgentMemoryError):
    """Synchronization operation failed."""
    def __init__(self, message: str = "Synchronization operation failed"):
        super().__init__(message)

class FederationError(AgentMemoryError):
    """Federation operation failed."""
    def __init__(self, message: str = "Federation operation failed"):
        super().__init__(message)
