"""Provider configuration data model.

Defines :class:`ProviderConfig`, the configuration container passed to each
translation / TTS provider at ``initialize`` time. It carries the HTTP
``endpoint``, the secret ``credential``, and an open-ended ``extra`` dict
that individual providers interpret on their own terms (e.g. ``model_name``,
``language_pair``, ``default_voice``).

Corresponds to requirement R6.2 and the "Data Models > ProviderConfig"
section of the design document.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProviderConfig:
    """Configuration for a translation or TTS provider.

    Attributes:
        endpoint: HTTP endpoint URL used to reach the upstream service.
        credential: Secret (API key / token) injected via the manifest's
            ``secret`` channel. Log formatters and error serializers MUST
            redact this value.
        extra: Provider-specific key/value bag. Common keys include
            ``model_name``, ``language_pair``, and ``default_voice``.
            Defaults to an empty dict so callers may omit it.
    """

    endpoint: str
    credential: str
    extra: dict[str, Any] = field(default_factory=dict)


__all__ = ["ProviderConfig"]
