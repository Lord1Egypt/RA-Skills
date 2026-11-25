"""Runtime configuration for a recon run.

Kept deliberately tiny: a bundle of timeouts + skip lists + verbosity.
Each check receives this so behaviour is predictable and testable.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set


@dataclass
class Config:
    # network behaviour
    timeout: float = 10.0        # per-request seconds
    max_redirects: int = 5       # follow at most this many redirects
    # which checks to skip (empty set = run all)
    skip: Set[str] = field(default_factory=set)
    # noise controls
    max_subdomains: int = 25     # light sweep cap (keep it gentle)
    max_paths: int = 15          # sensitive-path probe cap
    max_js_bundles: int = 10     # JS chunks to download + scan
    # output
    verbose: bool = False
    # where to save downloaded bundles for inspection
    scratch_dir: str = "/tmp/recon-cli"
