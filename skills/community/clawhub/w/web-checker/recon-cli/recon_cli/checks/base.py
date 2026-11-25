"""Base class for all checks."""
from __future__ import annotations

from abc import ABC, abstractmethod

from ..config import Config
from ..finding import CheckResult


class Check(ABC):
    """A named, run-able recon check.

    Subclasses implement `run()` and return a `CheckResult`.
    `name` is used both in reports and the --only/--skip flags.
    """

    name: str = "check"
    description: str = ""

    @abstractmethod
    def run(self, target: str, cfg: Config) -> CheckResult:  # pragma: no cover
        """Run against `target` (a bare domain or full URL)."""
        raise NotImplementedError

    def __repr__(self) -> str:  # pragma: no cover
        return f"<{type(self).__name__} name={self.name!r}>"
