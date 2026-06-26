from __future__ import annotations


class ResourceHunterError(RuntimeError):
    pass


class ConfigError(ResourceHunterError):
    pass


class UpstreamError(ResourceHunterError):
    def __init__(self, message: str, *, source: str = "", url: str = "", failure_kind: str = "upstream") -> None:
        super().__init__(message)
        self.source = source
        self.url = url
        self.failure_kind = failure_kind


class NetworkError(UpstreamError):
    def __init__(self, message: str, *, source: str = "", url: str = "") -> None:
        super().__init__(message, source=source, url=url, failure_kind="network")


class SchemaError(UpstreamError):
    def __init__(self, message: str, *, source: str = "", url: str = "") -> None:
        super().__init__(message, source=source, url=url, failure_kind="schema")


class BinaryMissingError(ResourceHunterError):
    pass
