"""
axiom-rebrand — Generic rebrand pipeline for any project.

Strip internal jargon, fix hardcoded paths, regenerate manifests.
Akasha-style: deterministic, idempotent, byte-to-byte proof.

Pure Python stdlib, zero dependencies.
Apache 2.0 license.
"""
from .rebrand import (
    rebrand_project,
    rebrand_file,
    strip_jargon,
    fix_sys_path,
    sha256_file,
    regenerate_manifest,
    run_tests,
    validate,
    load_jargon_from_config,
    DEFAULT_JARGON_PATTERNS,
    DEFAULT_EXCLUDE_PATTERNS,
    main,
)

__version__ = "0.1.0"
__license__ = "Apache 2.0"

__all__ = [
    "rebrand_project",
    "rebrand_file",
    "strip_jargon",
    "fix_sys_path",
    "sha256_file",
    "regenerate_manifest",
    "run_tests",
    "validate",
    "load_jargon_from_config",
    "DEFAULT_JARGON_PATTERNS",
    "DEFAULT_EXCLUDE_PATTERNS",
    "main",
    "__version__",
    "__license__",
]
