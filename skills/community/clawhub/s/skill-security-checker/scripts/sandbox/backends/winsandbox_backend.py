"""
winsandbox_backend.py - Run skill scripts inside Windows Sandbox.

Isolation guarantees:
  - Networking disabled by default via the .wsb config (<Networking>Disable</Networking>).
  - Skill folder mapped read-only (<ReadOnly>true</ReadOnly>).
  - vGPU disabled to reduce attack surface.

IMPORTANT (死规则13 compliance):
  The .wsb file is a plain XML config, NOT a script. We NEVER ship a .wsb file
  inside the skill repository. It is generated at runtime into a system temp
  directory and deleted on cleanup, so the repo stays free of forbidden file
  types.

Availability:
  Windows Sandbox is only present on Windows Pro/Enterprise with the optional
  feature enabled. We detect WindowsSandbox.exe; if absent, .available = False
  and the selector falls back gracefully.
"""

import os
import shutil
import subprocess
import tempfile


class WindowsSandboxBackend:
    name = 'winsandbox'

    def __init__(self):
        self._tmpdir = None
        self._wsb_path = None
        self.available = self._detect()

    def _detect(self):
        if os.name != 'nt':
            return False
        # WindowsSandbox.exe lives in System32 when the feature is enabled.
        exe = shutil.which('WindowsSandbox') or shutil.which('WindowsSandbox.exe')
        if exe:
            return True
        candidate = os.path.join(
            os.environ.get('WINDIR', r'C:\Windows'), 'System32', 'WindowsSandbox.exe'
        )
        return os.path.isfile(candidate)

    def _generate_wsb(self, skill_path, mapped_dir):
        """Generate a locked-down .wsb XML config into a temp dir at runtime."""
        wsb_xml = (
            '<Configuration>\n'
            '  <Networking>Disable</Networking>\n'
            '  <vGPU>Disable</vGPU>\n'
            '  <MappedFolders>\n'
            '    <MappedFolder>\n'
            f'      <HostFolder>{skill_path}</HostFolder>\n'
            f'      <SandboxFolder>{mapped_dir}</SandboxFolder>\n'
            '      <ReadOnly>true</ReadOnly>\n'
            '    </MappedFolder>\n'
            '  </MappedFolders>\n'
            '</Configuration>\n'
        )
        self._wsb_path = os.path.join(self._tmpdir, 'ssc_dynamic.wsb')
        with open(self._wsb_path, 'w', encoding='utf-8') as f:
            f.write(wsb_xml)
        return self._wsb_path

    def execute(self, skill_path, entrypoints, options, monitor):
        """Launch Windows Sandbox with the generated config.

        NOTE: Windows Sandbox is GUI-oriented and does not natively stream
        stdout back to the host. Behavior collection here is best-effort via a
        shared read-only mapping; full IPC is a future enhancement. When result
        capture is not possible, we return an empty-but-available payload so the
        audit still records that a dynamic run was attempted.
        """
        self._tmpdir = tempfile.mkdtemp(prefix='ssc_wsb_')
        mapped_dir = r'C:\skill'
        self._generate_wsb(skill_path, mapped_dir)

        # Best-effort launch; do not block the audit on GUI lifecycle.
        try:
            subprocess.Popen(
                ['WindowsSandbox', self._wsb_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception as e:
            return {'behaviors': [], 'note': f'launch failed: {e}'}

        return {
            'behaviors': [],
            'note': 'Windows Sandbox launched (GUI). Automated behavior capture '
                    'is limited in this backend; Docker is recommended for full '
                    'behavior monitoring.',
        }

    def cleanup(self):
        if self._tmpdir and os.path.isdir(self._tmpdir):
            shutil.rmtree(self._tmpdir, ignore_errors=True)
            self._tmpdir = None
            self._wsb_path = None
