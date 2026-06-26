"""Exception hierarchy for supervised-agentic-loop."""


class SalError(Exception):
    """Base exception for all SAL errors."""


class IterationCrash(SalError):
    """Agent code crashed (OOM, SyntaxError, timeout, subprocess failure)."""


class IterationHallucination(SalError):
    """Agent claimed success but verification gates failed."""


class MetricParseError(SalError):
    """metric_parser could not extract a float from command output."""


class BaselineCrashError(SalError):
    """Baseline measurement failed — the codebase is broken before we start.

    This is a HARD ABORT — the loop cannot begin if the unmodified
    codebase doesn't produce a valid metric.
    """
