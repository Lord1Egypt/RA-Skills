"""
report.py - Normalize dynamic scan output for merging into the main report.

build() returns a dict consumed by audit.py:
  {
    'available': bool,
    'backend': str,
    'hint': str,
    'behaviors': [...],
    'findings': [...],   # ScanResult-like dicts, ready to merge + score
    'error': str or None,
  }
"""


def build(available, backend, behaviors, findings, error=None):
    hint = ''
    if not findings and not error:
        hint = '动态扫描完成，未发现异常运行时行为。'
    return {
        'available': available,
        'backend': backend,
        'hint': hint,
        'behaviors': behaviors,
        'findings': findings,
        'error': error,
    }
