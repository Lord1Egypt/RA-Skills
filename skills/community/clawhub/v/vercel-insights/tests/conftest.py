"""Fixtures shared by every test module."""

from __future__ import annotations

import io
import sys
from pathlib import Path
from typing import Any

import pytest
import requests

# The package is not installed, so the repository root goes on sys.path before
# anything imports it. conftest.py is loaded before any test module, which is
# what makes this the right place for it.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from vercel_insights import cli as vi_cli  # noqa: E402  (needs the path fix above)


class Cli:
    """Runs ``main`` with a captured environment, streams and fake session."""

    def __init__(self, monkeypatch: pytest.MonkeyPatch) -> None:
        self.monkeypatch = monkeypatch
        self.created: list[Any] = []

    def run(
        self,
        argv: list[str],
        env: dict[str, str] | None = None,
        session: Any = None,
    ) -> tuple[int, str, str]:
        created = self.created

        def factory() -> Any:
            if session is None:
                raise AssertionError("a real requests.Session was constructed")
            created.append(session)
            return session

        # vercel_insights.cli does `import requests`, so this is the very object
        # the module reaches for when it builds its session.
        self.monkeypatch.setattr(requests, "Session", factory)
        out, err = io.StringIO(), io.StringIO()
        code = vi_cli.main(argv, env if env is not None else {}, out=out, err=err)
        return code, out.getvalue(), err.getvalue()


@pytest.fixture
def cli(monkeypatch: pytest.MonkeyPatch) -> Cli:
    return Cli(monkeypatch)
