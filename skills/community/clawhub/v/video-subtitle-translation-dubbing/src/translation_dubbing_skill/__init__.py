"""translation_dubbing_skill — OpenClaw skill for English→Chinese subtitle translation and dubbing.

The OpenClaw runtime locates the skill through the ``entrypoint`` declared
in ``manifest.yaml``. Re-exporting :func:`run` and :class:`ManifestParams`
at the package root keeps that wiring trivial: the runtime only has to
import ``translation_dubbing_skill`` and call ``.run(params)``.

Importing this module also pulls in :mod:`translation_dubbing_skill.providers`,
whose own import side effects register the four built-in providers
(LLM/Web × Translation/TTS) with the default provider registry, so the
runtime receives a fully-wired skill in one import.
"""

# Pull provider registrations into the import graph so the default
# registry is populated before ``run`` is called. ``noqa: F401`` — the
# name ``providers`` is imported purely for its side effects.
from translation_dubbing_skill import providers  # noqa: F401
from translation_dubbing_skill.entry import ManifestParams, parse_manifest, run

__version__ = "0.1.4"

__all__ = [
    "__version__",
    "ManifestParams",
    "parse_manifest",
    "run",
]
