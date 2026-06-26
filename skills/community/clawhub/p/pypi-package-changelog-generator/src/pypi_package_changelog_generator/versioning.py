from __future__ import annotations

import re
from dataclasses import dataclass
from functools import total_ordering
from typing import Mapping

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version

from pypi_package_changelog_generator.models import VersionSelection


class VersionResolutionError(ValueError):
    """Raised when a version expression cannot be resolved."""


@total_ordering
@dataclass(frozen=True, slots=True)
class VersionCandidate:
    raw: str
    parsed: Version | None
    legacy_key: tuple
    is_prerelease: bool

    @property
    def normalized(self) -> str:
        return normalize_version(self.raw)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, VersionCandidate):
            return NotImplemented
        if self.parsed is not None and other.parsed is not None:
            return self.parsed < other.parsed
        if self.parsed is not None:
            return True
        if other.parsed is not None:
            return False
        return self.legacy_key < other.legacy_key


def normalize_version(value: str) -> str:
    return value.strip().removeprefix("v").removeprefix("V").lower()


def build_candidates(releases: Mapping[str, object]) -> list[VersionCandidate]:
    candidates: list[VersionCandidate] = []
    for version in releases:
        parsed: Version | None
        try:
            parsed = Version(version)
            prerelease = parsed.is_prerelease or parsed.is_devrelease
        except InvalidVersion:
            parsed = None
            prerelease = _looks_like_prerelease(version)
        candidates.append(
            VersionCandidate(
                raw=version,
                parsed=parsed,
                legacy_key=_legacy_sort_key(version),
                is_prerelease=prerelease,
            )
        )
    return sorted(candidates)


def resolve_version_pair(
    releases: Mapping[str, object],
    *,
    from_version: str | None,
    to_version: str | None,
    version_range: str | None,
) -> VersionSelection:
    candidates = build_candidates(releases)
    if not candidates:
        raise VersionResolutionError("No releases were returned by PyPI.")

    if version_range:
        return _resolve_range(candidates, version_range)

    assert from_version is not None and to_version is not None
    return VersionSelection(
        from_version=_resolve_explicit(candidates, from_version).raw,
        to_version=_resolve_explicit(candidates, to_version).raw,
        range_expression=None,
    )


def build_tag_candidates(version: str) -> list[str]:
    normalized = version.removeprefix("v")
    return [
        f"v{normalized}",
        normalized,
        f"release-{normalized}",
        f"release/{normalized}",
        f"python-v{normalized}",
    ]


def _resolve_explicit(
    candidates: list[VersionCandidate], requested: str
) -> VersionCandidate:
    normalized = normalize_version(requested)
    for candidate in candidates:
        if candidate.raw == requested or candidate.normalized == normalized:
            return candidate
    raise VersionResolutionError(f"Version '{requested}' was not found on PyPI.")


def _resolve_range(
    candidates: list[VersionCandidate], version_range: str
) -> VersionSelection:
    latest_match = re.fullmatch(r"latest-(\d+)", version_range.strip(), re.IGNORECASE)
    if latest_match:
        offset = int(latest_match.group(1))
        stable = _stable_preferred(candidates)
        if offset <= 0 or len(stable) <= offset:
            raise VersionResolutionError(
                f"Range '{version_range}' does not have enough matching versions."
            )
        return VersionSelection(
            from_version=stable[-(offset + 1)].raw,
            to_version=stable[-1].raw,
            range_expression=version_range,
        )

    try:
        specifier = SpecifierSet(version_range)
    except InvalidSpecifier as exc:
        raise VersionResolutionError(
            f"Unsupported version range '{version_range}'."
        ) from exc

    matched = [
        candidate
        for candidate in candidates
        if candidate.parsed and candidate.parsed in specifier
    ]
    matched = _stable_preferred(matched)
    if len(matched) < 2:
        raise VersionResolutionError(
            f"Range '{version_range}' must match at least two releases on PyPI."
        )
    return VersionSelection(
        from_version=matched[0].raw,
        to_version=matched[-1].raw,
        range_expression=version_range,
    )


def _stable_preferred(candidates: list[VersionCandidate]) -> list[VersionCandidate]:
    stable = [candidate for candidate in candidates if not candidate.is_prerelease]
    return stable or candidates


def _looks_like_prerelease(version: str) -> bool:
    return bool(re.search(r"(?:a|alpha|b|beta|rc|dev|pre|preview)", version.lower()))


def _legacy_sort_key(version: str) -> tuple:
    normalized = normalize_version(version)
    parts = re.split(r"[.\-+_]", normalized)
    key = []
    for part in parts:
        if not part:
            continue
        if part.isdigit():
            key.append((0, int(part)))
            continue
        match = re.fullmatch(r"([a-z]+)(\d*)", part)
        if match:
            key.append((1, match.group(1), int(match.group(2) or 0)))
            continue
        key.append((2, part))
    return tuple(key)
