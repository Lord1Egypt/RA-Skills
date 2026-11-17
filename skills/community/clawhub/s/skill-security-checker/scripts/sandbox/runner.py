"""
runner.py - Dynamic sandbox orchestration.

Flow:
  1. Detect available isolation backend (Docker -> Windows Sandbox -> degraded).
  2. Prepare a resource-limited, network-isolated environment.
  3. Execute the skill's scripts under a behavior monitor.
  4. Collect captured behaviors, apply anomaly rules, normalize into findings.
  5. Clean up all temporary resources.

If no real isolation backend is present, this module degrades to a static-only
hint and NEVER raises, so the caller (audit.py) keeps working everywhere.
"""

import os
import multiprocessing
from dataclasses import dataclass, field

from .backends import select_backend
from . import monitor as monitor_mod
from . import rules as rules_mod
from . import report as report_mod


@dataclass
class DynamicScanOptions:
    """Runtime knobs for the dynamic scan. Safe defaults for any machine."""
    timeout_sec: int = 30
    memory_mb: int = 512
    cpu_limit: float = 1.0
    network: bool = False              # network disabled by default
    whitelist_domains: list = field(default_factory=list)
    entrypoints: list = field(default_factory=list)  # scripts to execute
    force_backend: str = None          # 'docker' | 'winsandbox' | None (auto)

    @classmethod
    def auto(cls, **overrides):
        """Build options with hardware-aware CPU cap (never hog the host)."""
        try:
            cpu_count = multiprocessing.cpu_count()
        except Exception:
            cpu_count = 2
        # Use at most half of the cores, minimum 1.
        cpu_limit = max(1.0, cpu_count / 2.0)
        opts = cls(cpu_limit=cpu_limit)
        for k, v in overrides.items():
            if v is not None and hasattr(opts, k):
                setattr(opts, k, v)
        return opts


def _discover_entrypoints(skill_path):
    """Find candidate scripts to execute inside the sandbox.

    We only pick interpreted script files that a skill would actually run.
    Executables/binaries are intentionally excluded (they are already flagged
    by the static forbidden-extension check).
    """
    candidates = []
    exec_exts = {'.py', '.js', '.mjs', '.cjs'}
    for root, dirs, files in os.walk(skill_path):
        # Skip noise directories
        dirs[:] = [d for d in dirs if d not in {
            '__pycache__', '.git', '.venv', 'node_modules', '.pytest_cache',
        }]
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()
            if ext in exec_exts:
                candidates.append(os.path.join(root, fn))
    return candidates


def run_dynamic_scan(skill_path, options=None):
    """Run a dynamic sandbox scan and return a normalized result dict.

    Returns dict shape:
      {
        'available': bool,          # was a real isolation backend used?
        'backend': str,             # 'docker' | 'winsandbox' | 'none'
        'hint': str,                # degradation hint when unavailable
        'behaviors': [...],         # raw captured behaviors
        'findings': [...],          # normalized ScanResult-like dicts
        'error': str or None,
      }
    """
    if options is None:
        options = DynamicScanOptions.auto()

    skill_path = os.path.abspath(skill_path)

    # 1. Pick a backend (never raises; returns degraded backend if none).
    backend = select_backend(force=options.force_backend)

    if not backend.available:
        return {
            'available': False,
            'backend': 'none',
            'hint': '未检测到 Docker 或 Windows Sandbox，已跳过动态扫描。'
                    '建议在沙箱环境中进行动态扫描以获得更高检出率。',
            'behaviors': [],
            'findings': [],
            'error': None,
        }

    # 2. Discover entrypoints if not explicitly provided.
    entrypoints = options.entrypoints or _discover_entrypoints(skill_path)
    if not entrypoints:
        return {
            'available': True,
            'backend': backend.name,
            'hint': '未在 Skill 中发现可执行脚本，动态扫描无内容可执行。',
            'behaviors': [],
            'findings': [],
            'error': None,
        }

    # 3. Execute under the behavior monitor, collect behaviors.
    behaviors = []
    error = None
    try:
        raw = backend.execute(
            skill_path=skill_path,
            entrypoints=entrypoints,
            options=options,
            monitor=monitor_mod,
        )
        behaviors = monitor_mod.normalize(raw)
    except Exception as e:  # never let the sandbox crash the whole audit
        error = f'{type(e).__name__}: {e}'
    finally:
        try:
            backend.cleanup()
        except Exception:
            pass

    # 4. Apply anomaly rules -> normalized findings.
    findings = rules_mod.evaluate(behaviors, options=options)

    # 5. Return a report-ready structure.
    return report_mod.build(
        available=True,
        backend=backend.name,
        behaviors=behaviors,
        findings=findings,
        error=error,
    )
