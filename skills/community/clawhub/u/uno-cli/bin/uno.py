#!/usr/bin/env python3
"""Uno CLI launcher for the ``uno-cli`` skill.

This file is a thin dispatcher. The real CLI lives in the ``uno-cli`` PyPI
package — install once with::

    python3 -m pip install --user --upgrade 'uno-cli>=1.0.2'

After that, ``python bin/uno.py <args>`` behaves identically to ``uno <args>``.
This skill intentionally does not bundle the CLI source so that bug fixes and
new features land everywhere via ``pip install --upgrade uno-cli`` instead of
requiring a new skill release.

Security posture
----------------
- The CLI never echoes the stored API token to stdout. Every response is
  funnelled through ``uno_cli.cli._strip_secrets`` so any field whose key
  name looks like a secret (``api_key``, ``access_token``, ``refresh_token``,
  ``secret``, ``password``, ``token``, ...) is masked before printing.
- ``login --poll`` persists the freshly-issued token to
  ``~/.uno/credentials.json`` (mode ``0600``) and reports only the storage
  location back to the caller. No code path in the CLI prints the raw token
  to stdout; CI jobs that genuinely need the value read the file directly.
- ``call --dry-run <tool>`` is the primary user-confirmation surface: it
  formats the planned invocation as JSON without reading any credential,
  opening any network connection, or spending any credit. The expected
  agent flow is search → dry-run → show the preview to the user → real
  call, never call-before-preview.
- No background daemons, listeners, or retries: the CLI exits after each
  command. Each ``call`` is a single, explicit, user-visible invocation.
- Third-party OAuth (for per-server tokens) is always user-initiated: the
  CLI surfaces an ``auth_url``, the user completes the browser flow, and
  the resulting token is stored server-side — the CLI itself never sees
  third-party passwords.
"""

from __future__ import annotations

import json
import os
import sys


def _report_missing():
    sys.stdout.write(
        json.dumps(
            {
                "error": "uno-cli not installed",
                "hint": (
                    "Install the Uno CLI first: "
                    "python3 -m pip install --user --upgrade 'uno-cli>=1.0.0'"
                ),
                "install_url": "https://pypi.org/project/uno-cli/",
            },
            ensure_ascii=False,
        )
        + "\n"
    )
    sys.exit(2)


try:
    from uno_cli.cli import main
except ModuleNotFoundError:
    _report_missing()

# Attribution tag only — no scope restriction for the full-gateway skill.
os.environ.setdefault("UNO_CALLER_SKILL", "uno-cli")


if __name__ == "__main__":
    main()
