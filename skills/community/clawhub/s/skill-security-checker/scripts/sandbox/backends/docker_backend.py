"""
docker_backend.py - Run skill scripts inside a Docker container.

Isolation guarantees:
  - Network disabled by default (--network=none). Whitelist domains are only
    reachable when a proxy is explicitly attached (future extension); by
    default the container cannot reach the internet.
  - Skill directory mounted read-only (:ro) so the script cannot tamper with
    the host copy.
  - Resource limits: --memory, --cpus, and a hard wall-clock timeout.
  - --pids-limit and --cap-drop ALL to reduce blast radius.

No external Python package is required: we shell out to the `docker` CLI, which
keeps the tool dependency-free (死规则9: self-contained, graceful fallback).
"""

import os
import json
import shutil
import subprocess
import tempfile


DEFAULT_IMAGE = 'python:3.11-slim'


class DockerBackend:
    name = 'docker'

    def __init__(self):
        self._tmpdir = None
        self.available = self._detect()

    def _detect(self):
        """Docker is available only if the CLI exists AND the daemon responds."""
        if shutil.which('docker') is None:
            return False
        try:
            r = subprocess.run(
                ['docker', 'info'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=8,
            )
            return r.returncode == 0
        except Exception:
            return False

    def _build_monitor_payload(self, monitor):
        """Return the monitor bootstrap source that runs inside the container.

        The monitor installs audit hooks (network/file/proc/env) BEFORE the
        target script runs, then executes each entrypoint and prints a single
        JSON line with all captured behaviors.
        """
        return monitor.get_bootstrap_source()

    def execute(self, skill_path, entrypoints, options, monitor):
        """Execute entrypoints inside a locked-down container."""
        self._tmpdir = tempfile.mkdtemp(prefix='ssc_sandbox_')
        bootstrap_path = os.path.join(self._tmpdir, '_ssc_monitor.py')
        with open(bootstrap_path, 'w', encoding='utf-8') as f:
            f.write(self._build_monitor_payload(monitor))

        # Relative entrypoints as seen inside the container (/skill mount).
        rel_entrypoints = [
            os.path.relpath(ep, skill_path).replace('\\', '/')
            for ep in entrypoints
        ]

        network = 'none' if not options.network else 'bridge'

        cmd = [
            'docker', 'run', '--rm',
            '--network', network,
            '--memory', f'{options.memory_mb}m',
            '--cpus', str(options.cpu_limit),
            '--pids-limit', '128',
            '--cap-drop', 'ALL',
            '--security-opt', 'no-new-privileges',
            '-v', f'{skill_path}:/skill:ro',
            '-v', f'{bootstrap_path}:/_ssc_monitor.py:ro',
            '-w', '/skill',
            '-e', 'SSC_ENTRYPOINTS=' + json.dumps(rel_entrypoints),
            '-e', 'SSC_TIMEOUT=' + str(options.timeout_sec),
            DEFAULT_IMAGE,
            'python', '/_ssc_monitor.py',
        ]

        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=options.timeout_sec + 20,  # outer guard > inner timeout
                text=True,
            )
        except subprocess.TimeoutExpired:
            return {'behaviors': [], 'note': 'container wall-clock timeout'}

        return self._parse_output(proc.stdout, proc.stderr)

    def _parse_output(self, stdout, stderr):
        """Extract the JSON behavior line emitted by the in-container monitor."""
        for line in (stdout or '').splitlines():
            line = line.strip()
            if line.startswith('{') and 'behaviors' in line:
                try:
                    return json.loads(line)
                except Exception:
                    continue
        return {'behaviors': [], 'note': (stderr or '')[:500]}

    def cleanup(self):
        if self._tmpdir and os.path.isdir(self._tmpdir):
            shutil.rmtree(self._tmpdir, ignore_errors=True)
            self._tmpdir = None
