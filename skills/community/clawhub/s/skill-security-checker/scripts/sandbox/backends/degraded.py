"""
degraded.py - No-op backend used when no isolation environment is available.

This backend keeps the whole audit working on machines without Docker or
Windows Sandbox. It never executes anything and never raises; it simply signals
that dynamic scanning was skipped so the caller can print the recommended hint:
    "建议在沙箱环境中进行动态扫描"
"""


class DegradedBackend:
    name = 'none'
    available = False

    def execute(self, skill_path, entrypoints, options, monitor):
        return {'behaviors': [], 'note': 'no isolation backend available'}

    def cleanup(self):
        return None
