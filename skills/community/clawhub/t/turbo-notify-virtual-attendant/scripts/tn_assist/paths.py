"""Workspace confinement. Every filesystem path the helper touches comes from here.

A workspace is ``<base>/<org_id>/<num_id>/``. Nothing outside it is reachable through
:meth:`Workspace.path`, whatever the arguments are (traversal, absolute paths, symlinks).
"""

from __future__ import annotations

import os
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

ORG_ID_RE = re.compile(r"^org_[0-9a-f]{32}$")
NUM_ID_RE = re.compile(r"^num_[0-9a-f]{32}$")
_CONTACT_RE = re.compile(r"^[0-9]{8,15}$")
_PHONE_PUNCTUATION = " \t+()-."
_DIR_MODE = 0o700


class PathEscapeError(ValueError):
    """A path argument tried to leave the workspace."""


class InvalidContactKey(ValueError):
    """The text is not a usable phone number."""


class InvalidWorkspaceId(ValueError):
    """An organization or number id does not have the public format."""


class ContactKey(str):
    """A contact's identity inside a workspace: canonical digits, 8 to 15 of them."""

    @classmethod
    def parse(cls, raw: str) -> ContactKey:
        text = "".join(_ascii_digit(ch) for ch in raw.strip() if ch not in _PHONE_PUNCTUATION)
        if not _CONTACT_RE.match(text):
            raise InvalidContactKey("not a phone number")
        return cls(_canonical_brazilian_mobile(text))


def _ascii_digit(ch: str) -> str:
    """Any Unicode decimal digit (Arabic-Indic, Devanagari, full width) becomes its ASCII digit."""
    folded = unicodedata.normalize("NFKC", ch)
    if len(folded) == 1 and unicodedata.category(folded) == "Nd":
        return str(unicodedata.digit(folded))
    return folded


def _canonical_brazilian_mobile(digits: str) -> str:
    """Brazilian mobiles are 13 digits; the old 12-digit form lacks the ninth digit.

    Landlines (local numbers starting 2 to 5) keep their 12 digits.
    """
    if len(digits) == 12 and digits.startswith("55") and digits[4] in "6789":
        return digits[:4] + "9" + digits[4:]
    return digits


@dataclass(frozen=True)
class Workspace:
    root: Path
    org_id: str
    num_id: str

    @classmethod
    def open(cls, base: Path, org_id: str, num_id: str, *, create: bool = False) -> Workspace:
        if not ORG_ID_RE.match(org_id):
            raise InvalidWorkspaceId("organization id")
        if not NUM_ID_RE.match(num_id):
            raise InvalidWorkspaceId("number id")
        base = Path(os.path.realpath(base))
        org_dir = base / org_id
        root = org_dir / num_id
        if create:
            for directory in (org_dir, root):
                directory.mkdir(mode=_DIR_MODE, parents=True, exist_ok=True)
                os.chmod(directory, _DIR_MODE)
        elif not root.is_dir():
            raise FileNotFoundError("workspace does not exist")
        return cls(root=Path(os.path.realpath(root)), org_id=org_id, num_id=num_id)

    def path(self, *parts: str) -> Path:
        for part in parts:
            if "\x00" in part or os.path.isabs(part):
                raise PathEscapeError("path outside the workspace")
        candidate = Path(os.path.realpath(self.root.joinpath(*parts)))
        try:
            inside = os.path.commonpath([str(self.root), str(candidate)]) == str(self.root)
        except ValueError:
            inside = False
        if not inside:
            raise PathEscapeError("path outside the workspace")
        return candidate

    def contact_dir(self, key: ContactKey) -> Path:
        return self.path("contacts", str(key))
