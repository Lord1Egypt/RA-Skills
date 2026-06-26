#!/usr/bin/env python3
from __future__ import annotations


class AppError(Exception):
    """Base application error."""


class LicenseError(AppError):
    pass


class DependencyError(AppError):
    pass


class LoginStateError(AppError):
    pass


class RpaStepError(AppError):
    pass


class DownloadError(AppError):
    pass


class ParseError(AppError):
    pass
