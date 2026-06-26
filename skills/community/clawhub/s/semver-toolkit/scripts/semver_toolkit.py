#!/usr/bin/env python3
"""Semantic Versioning (SemVer) toolkit for parsing, comparing, bumping, and validating versions.

Follows the Semantic Versioning 2.0.0 specification (https://semver.org).
"""

import argparse
import json
import re
import sys
import textwrap

SEMVER_PATTERN = re.compile(
    r"^v?(?P<major>0|[1-9]\d*)"
    r"\.(?P<minor>0|[1-9]\d*)"
    r"\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+(?P<build>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


class SemVer:
    def __init__(self, major: int, minor: int, patch: int,
                 prerelease: str = "", build: str = ""):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.prerelease = prerelease
        self.build = build

    @classmethod
    def parse(cls, version_str: str) -> "SemVer":
        m = SEMVER_PATTERN.match(version_str.strip())
        if not m:
            raise ValueError(f"Invalid semver: '{version_str}'")
        return cls(
            major=int(m.group("major")),
            minor=int(m.group("minor")),
            patch=int(m.group("patch")),
            prerelease=m.group("prerelease") or "",
            build=m.group("build") or "",
        )

    def __str__(self):
        s = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            s += f"-{self.prerelease}"
        if self.build:
            s += f"+{self.build}"
        return s

    def to_dict(self):
        return {
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch,
            "prerelease": self.prerelease,
            "build": self.build,
            "full": str(self),
        }

    def _pre_tuple(self):
        """Convert prerelease to comparable tuple."""
        if not self.prerelease:
            return None
        parts = []
        for p in self.prerelease.split("."):
            if p.isdigit():
                parts.append((0, int(p)))
            else:
                parts.append((1, p))
        return tuple(parts)

    def _cmp_key(self):
        pre = self._pre_tuple()
        # No prerelease has higher precedence than any prerelease
        if pre is None:
            return (self.major, self.minor, self.patch, 1, ())
        return (self.major, self.minor, self.patch, 0, pre)

    def __eq__(self, other):
        return self._cmp_key() == other._cmp_key()

    def __lt__(self, other):
        return self._cmp_key() < other._cmp_key()

    def __le__(self, other):
        return self._cmp_key() <= other._cmp_key()

    def __gt__(self, other):
        return self._cmp_key() > other._cmp_key()

    def __ge__(self, other):
        return self._cmp_key() >= other._cmp_key()

    def bump(self, part: str, pre: str = "") -> "SemVer":
        if part == "major":
            v = SemVer(self.major + 1, 0, 0)
        elif part == "minor":
            v = SemVer(self.major, self.minor + 1, 0)
        elif part == "patch":
            v = SemVer(self.major, self.minor, self.patch + 1)
        elif part == "prerelease":
            if self.prerelease:
                # Increment last numeric identifier
                parts = self.prerelease.split(".")
                for i in range(len(parts) - 1, -1, -1):
                    if parts[i].isdigit():
                        parts[i] = str(int(parts[i]) + 1)
                        break
                else:
                    parts.append("1")
                v = SemVer(self.major, self.minor, self.patch, ".".join(parts))
            else:
                tag = pre or "alpha"
                v = SemVer(self.major, self.minor, self.patch + 1, f"{tag}.0")
        else:
            raise ValueError(f"Unknown bump part: {part}")

        if pre and part != "prerelease":
            v.prerelease = f"{pre}.0"
        return v


def cmd_parse(args):
    v = SemVer.parse(args.version)
    if args.fmt == "json":
        print(json.dumps(v.to_dict(), indent=2))
    else:
        d = v.to_dict()
        for key, val in d.items():
            print(f"  {key:<12} {val}")


def cmd_validate(args):
    results = []
    for ver in args.versions:
        try:
            SemVer.parse(ver)
            results.append({"version": ver, "valid": True})
        except ValueError:
            results.append({"version": ver, "valid": False})

    if args.fmt == "json":
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            status = "VALID ✓" if r["valid"] else "INVALID ✗"
            print(f"  {r['version']:<30} {status}")


def cmd_bump(args):
    v = SemVer.parse(args.version)
    bumped = v.bump(args.part, pre=args.pre or "")
    if args.fmt == "json":
        print(json.dumps({"from": str(v), "to": str(bumped), "part": args.part}, indent=2))
    else:
        print(f"  {v} → {bumped}")


def cmd_compare(args):
    a = SemVer.parse(args.version_a)
    b = SemVer.parse(args.version_b)

    if a > b:
        result, sign = "greater", ">"
    elif a < b:
        result, sign = "less", "<"
    else:
        result, sign = "equal", "="

    if args.fmt == "json":
        print(json.dumps({"a": str(a), "b": str(b), "result": result}, indent=2))
    else:
        print(f"  {a} {sign} {b}")


def cmd_sort(args):
    versions = []
    for v_str in args.versions:
        try:
            versions.append(SemVer.parse(v_str))
        except ValueError:
            print(f"Warning: skipping invalid version '{v_str}'", file=sys.stderr)

    versions.sort(reverse=args.reverse)

    if args.fmt == "json":
        print(json.dumps([str(v) for v in versions], indent=2))
    else:
        for v in versions:
            print(f"  {v}")


def main():
    parser = argparse.ArgumentParser(
        description="Semantic Versioning (SemVer 2.0.0) toolkit.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              %(prog)s parse 1.2.3-beta.1+build.42
              %(prog)s validate 1.0.0 v2.1 not-a-version
              %(prog)s bump 1.2.3 minor
              %(prog)s bump 1.2.3 major --pre rc
              %(prog)s compare 1.2.3 2.0.0
              %(prog)s sort 3.0.0 1.0.0-alpha 1.0.0 2.1.0
        """),
    )
    parser.add_argument(
        "-f", "--format", choices=["plain", "json"], default="plain",
        dest="fmt", help="Output format (default: plain)",
    )

    # Add -f/--format to a parent parser so it works before AND after subcommand
    fmt_parent = argparse.ArgumentParser(add_help=False)
    fmt_parent.add_argument(
        "-f", "--format", choices=["plain", "json"], default="plain",
        dest="fmt", help="Output format (default: plain)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # parse
    p_parse = sub.add_parser("parse", parents=[fmt_parent], help="Parse a version string into components")
    p_parse.add_argument("version", help="Version string to parse")
    p_parse.set_defaults(func=cmd_parse)

    # validate
    p_val = sub.add_parser("validate", parents=[fmt_parent], help="Validate one or more version strings")
    p_val.add_argument("versions", nargs="+", help="Version strings to validate")
    p_val.set_defaults(func=cmd_validate)

    # bump
    p_bump = sub.add_parser("bump", parents=[fmt_parent], help="Bump a version")
    p_bump.add_argument("version", help="Current version")
    p_bump.add_argument("part", choices=["major", "minor", "patch", "prerelease"],
                        help="Part to bump")
    p_bump.add_argument("--pre", help="Prerelease tag (e.g. alpha, beta, rc)")
    p_bump.set_defaults(func=cmd_bump)

    # compare
    p_cmp = sub.add_parser("compare", parents=[fmt_parent], help="Compare two versions")
    p_cmp.add_argument("version_a", help="First version")
    p_cmp.add_argument("version_b", help="Second version")
    p_cmp.set_defaults(func=cmd_compare)

    # sort
    p_sort = sub.add_parser("sort", parents=[fmt_parent], help="Sort version strings")
    p_sort.add_argument("versions", nargs="+", help="Versions to sort")
    p_sort.add_argument("-r", "--reverse", action="store_true",
                        help="Sort in descending order")
    p_sort.set_defaults(func=cmd_sort)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
