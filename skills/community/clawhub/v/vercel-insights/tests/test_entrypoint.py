"""The entry points, and the standard library shadowing hazard they defuse.

This package contains a module named ``http``. So does the standard library,
and ``requests`` depends on that one: ``urllib3`` imports ``http.client``. If
this package's own directory is on ``sys.path``, the import resolves here
instead and dies on a relative import with no parent package, which is not a
failure anyone would connect to their ``PYTHONPATH``.

Running the file as a script puts its own directory on ``sys.path``
automatically. Running it as a module does not, but nothing stops the directory
already being there, so the repair in ``__main__.py`` is unconditional and both
forms are checked here. These are the only tests in the suite that start a
child process; nothing here touches the network either, since ``--version``
answers before any request is planned.
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest
from helpers import PACKAGE_DIR, REPO_ROOT

from vercel_insights import VERSION

EXPECTED = f"vercel-insights {VERSION}"

#: A PYTHONPATH pointing straight at the package directory, which is what makes
#: this package's http.py shadow the standard library one.
POISONED = str(PACKAGE_DIR)

MODULE_FORM = ["-m", "vercel_insights"]
SCRIPT_FORM = [str(PACKAGE_DIR / "__main__.py")]


def run_child(argv: list[str], cwd: str, python_path: str | None) -> str:
    """Run the tool in a child process and return its stdout."""
    env = dict(os.environ)
    env.pop("VERCEL_TOKEN", None)
    entries = [entry for entry in (python_path, str(REPO_ROOT)) if entry]
    env["PYTHONPATH"] = os.pathsep.join(entries)
    completed = subprocess.run(
        [sys.executable, *argv],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert completed.returncode == 0, completed.stderr
    assert "Traceback" not in completed.stderr
    return completed.stdout


@pytest.mark.parametrize("form", [MODULE_FORM, SCRIPT_FORM], ids=["module", "script"])
@pytest.mark.parametrize("cwd", [str(REPO_ROOT), os.sep], ids=["repo-root", "root-dir"])
@pytest.mark.parametrize(
    "python_path", [None, POISONED], ids=["clean-path", "poisoned-path"]
)
def test_both_entry_points_run_from_anywhere_and_with_a_poisoned_path(
    form: list[str], cwd: str, python_path: str | None
) -> None:
    assert run_child([*form, "--version"], cwd, python_path).strip() == EXPECTED


@pytest.mark.parametrize(
    "python_path", [None, POISONED], ids=["clean-path", "poisoned-path"]
)
def test_importing_the_entry_point_leaves_the_standard_library_reachable(
    python_path: str | None,
) -> None:
    # The direct statement of the hazard: after the entry point has run its
    # path repair, "import http.client" must still find the standard library.
    program = (
        "import vercel_insights.__main__\n"
        "import http.client\n"
        "print(http.client.__file__)\n"
    )
    resolved = run_child(["-c", program], os.sep, python_path).strip()
    assert resolved.endswith(os.path.join("http", "client.py"))
    assert str(PACKAGE_DIR) not in resolved
