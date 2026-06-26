#!/usr/bin/env python3
"""Semantic Versioning manager — parse, validate, compare, bump, and match versions."""

import re
import sys
import json
import argparse

SEMVER_RE = re.compile(
    r'^v?(?P<major>0|[1-9]\d*)'
    r'\.(?P<minor>0|[1-9]\d*)'
    r'\.(?P<patch>0|[1-9]\d*)'
    r'(?:-(?P<pre>[0-9A-Za-z\-]+(?:\.[0-9A-Za-z\-]+)*))?'
    r'(?:\+(?P<build>[0-9A-Za-z\-]+(?:\.[0-9A-Za-z\-]+)*))?$'
)

CONSTRAINT_RE = re.compile(
    r'^\s*(?P<op>=|!=|>=?|<=?|\^|~)\s*'
    r'(?P<major>0|[1-9]\d*)'
    r'(?:\.(?P<minor>0|[1-9]\d*))?'
    r'(?:\.(?P<patch>0|[1-9]\d*))?'
    r'(?:-(?P<pre>[0-9A-Za-z\-]+(?:\.[0-9A-Za-z\-]+)*))?\s*$'
)


class SemVer:
    __slots__ = ('major', 'minor', 'patch', 'pre', 'build')

    def __init__(self, major, minor, patch, pre=None, build=None):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.pre = tuple(pre) if pre else ()
        self.build = build or ''

    @classmethod
    def parse(cls, s):
        m = SEMVER_RE.match(s.strip())
        if not m:
            raise ValueError(f'Invalid semver: {s}')
        pre_str = m.group('pre')
        pre = []
        if pre_str:
            for p in pre_str.split('.'):
                pre.append(int(p) if p.isdigit() else p)
        return cls(
            int(m.group('major')), int(m.group('minor')), int(m.group('patch')),
            pre or None, m.group('build') or ''
        )

    def _pre_key(self):
        if not self.pre:
            return (1,)  # no pre-release > any pre-release
        parts = []
        for p in self.pre:
            if isinstance(p, int):
                parts.append((0, p, ''))
            else:
                parts.append((1, 0, p))
        return (0, *parts)

    def _sort_key(self):
        return (self.major, self.minor, self.patch, self._pre_key())

    def __eq__(self, o):
        return self._sort_key() == o._sort_key()

    def __lt__(self, o):
        return self._sort_key() < o._sort_key()

    def __le__(self, o):
        return self._sort_key() <= o._sort_key()

    def __gt__(self, o):
        return self._sort_key() > o._sort_key()

    def __ge__(self, o):
        return self._sort_key() >= o._sort_key()

    def __ne__(self, o):
        return self._sort_key() != o._sort_key()

    def __str__(self):
        s = f'{self.major}.{self.minor}.{self.patch}'
        if self.pre:
            s += '-' + '.'.join(str(p) for p in self.pre)
        if self.build:
            s += '+' + self.build
        return s

    def __repr__(self):
        return f'SemVer({self})'

    def to_dict(self):
        d = {'major': self.major, 'minor': self.minor, 'patch': self.patch, 'string': str(self)}
        if self.pre:
            d['prerelease'] = '.'.join(str(p) for p in self.pre)
        if self.build:
            d['build'] = self.build
        return d

    def bump(self, part, pre_tag=None):
        if part == 'major':
            return SemVer(self.major + 1, 0, 0,
                          [pre_tag, 0] if pre_tag else None)
        elif part == 'minor':
            return SemVer(self.major, self.minor + 1, 0,
                          [pre_tag, 0] if pre_tag else None)
        elif part == 'patch':
            if self.pre and not pre_tag:
                return SemVer(self.major, self.minor, self.patch)
            return SemVer(self.major, self.minor, self.patch + 1,
                          [pre_tag, 0] if pre_tag else None)
        elif part == 'prerelease':
            if self.pre:
                new_pre = list(self.pre)
                for i in range(len(new_pre) - 1, -1, -1):
                    if isinstance(new_pre[i], int):
                        new_pre[i] += 1
                        return SemVer(self.major, self.minor, self.patch, new_pre)
                new_pre.append(0)
                return SemVer(self.major, self.minor, self.patch, new_pre)
            tag = pre_tag or 'rc'
            return SemVer(self.major, self.minor, self.patch + 1, [tag, 0])
        raise ValueError(f'Unknown bump part: {part}')


def matches_constraint(ver, constraint_str):
    """Check if version matches a constraint like ^1.2.3, ~1.2, >=1.0.0"""
    m = CONSTRAINT_RE.match(constraint_str)
    if not m:
        raise ValueError(f'Invalid constraint: {constraint_str}')
    op = m.group('op')
    c_major = int(m.group('major'))
    c_minor = int(m.group('minor')) if m.group('minor') is not None else 0
    c_patch = int(m.group('patch')) if m.group('patch') is not None else 0
    pre_str = m.group('pre')
    pre = []
    if pre_str:
        for p in pre_str.split('.'):
            pre.append(int(p) if p.isdigit() else p)
    c = SemVer(c_major, c_minor, c_patch, pre or None)

    if op == '=':
        return ver == c
    elif op == '!=':
        return ver != c
    elif op == '>':
        return ver > c
    elif op == '>=':
        return ver >= c
    elif op == '<':
        return ver < c
    elif op == '<=':
        return ver <= c
    elif op == '^':
        # Compatible with: same leftmost non-zero
        if ver < c:
            return False
        if c_major != 0:
            return ver.major == c_major
        if c_minor != 0:
            return ver.major == 0 and ver.minor == c_minor
        return ver.major == 0 and ver.minor == 0 and ver.patch == c_patch
    elif op == '~':
        # Tilde: same major.minor
        if ver < c:
            return False
        return ver.major == c_major and ver.minor == c_minor
    return False


def cmd_validate(args):
    results = []
    exit_code = 0
    for v in args.versions:
        try:
            sv = SemVer.parse(v)
            results.append({'input': v, 'valid': True, 'parsed': sv.to_dict()})
        except ValueError as e:
            results.append({'input': v, 'valid': False, 'error': str(e)})
            exit_code = 1
    _output(results, args.format)
    return exit_code


def cmd_compare(args):
    a = SemVer.parse(args.version_a)
    b = SemVer.parse(args.version_b)
    if a < b:
        result = {'a': str(a), 'b': str(b), 'result': '<', 'description': f'{a} is older than {b}'}
    elif a > b:
        result = {'a': str(a), 'b': str(b), 'result': '>', 'description': f'{a} is newer than {b}'}
    else:
        result = {'a': str(a), 'b': str(b), 'result': '=', 'description': f'{a} and {b} are equal'}
    _output(result, args.format)
    return 0


def cmd_sort(args):
    versions = [SemVer.parse(v) for v in args.versions]
    versions.sort(reverse=args.reverse)
    result = [str(v) for v in versions]
    _output(result, args.format)
    return 0


def cmd_bump(args):
    sv = SemVer.parse(args.version)
    bumped = sv.bump(args.part, args.pre)
    result = {'original': str(sv), 'part': args.part, 'bumped': str(bumped)}
    if args.pre:
        result['pre_tag'] = args.pre
    _output(result, args.format)
    return 0


def cmd_filter(args):
    versions = [SemVer.parse(v) for v in args.versions]
    constraint = args.constraint
    matched = [str(v) for v in versions if matches_constraint(v, constraint)]
    not_matched = [str(v) for v in versions if not matches_constraint(v, constraint)]
    result = {'constraint': constraint, 'matched': matched, 'rejected': not_matched}
    _output(result, args.format)
    return 0


def cmd_latest(args):
    versions = [SemVer.parse(v) for v in args.versions]
    if args.constraint:
        versions = [v for v in versions if matches_constraint(v, args.constraint)]
    if not versions:
        _output({'latest': None, 'error': 'No versions match'}, args.format)
        return 1
    latest = max(versions)
    result = {'latest': str(latest)}
    if args.constraint:
        result['constraint'] = args.constraint
    _output(result, args.format)
    return 0


def _output(data, fmt):
    if fmt == 'json':
        print(json.dumps(data, indent=2))
    elif fmt == 'markdown':
        _output_md(data)
    else:
        _output_text(data)


def _output_text(data):
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                parts = []
                for k, v in item.items():
                    if isinstance(v, dict):
                        parts.append(f'{k}: {json.dumps(v)}')
                    else:
                        parts.append(f'{k}: {v}')
                print('  '.join(parts))
            else:
                print(item)
    elif isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (list, dict)):
                print(f'{k}: {json.dumps(v)}')
            else:
                print(f'{k}: {v}')


def _output_md(data):
    if isinstance(data, list):
        if data and isinstance(data[0], dict):
            keys = list(data[0].keys())
            print('| ' + ' | '.join(keys) + ' |')
            print('| ' + ' | '.join('---' for _ in keys) + ' |')
            for item in data:
                vals = []
                for k in keys:
                    v = item.get(k, '')
                    vals.append(str(v) if not isinstance(v, dict) else json.dumps(v))
                print('| ' + ' | '.join(vals) + ' |')
        else:
            for item in data:
                print(f'- {item}')
    elif isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, list):
                print(f'**{k}:** {", ".join(str(i) for i in v)}')
            elif isinstance(v, dict):
                print(f'**{k}:** {json.dumps(v)}')
            else:
                print(f'**{k}:** {v}')


def main():
    p = argparse.ArgumentParser(description='Semantic Versioning manager')
    p.add_argument('--format', '-f', choices=['text', 'json', 'markdown'], default='text')
    sub = p.add_subparsers(dest='command', required=True)

    # validate
    sv = sub.add_parser('validate', help='Validate semver strings')
    sv.add_argument('versions', nargs='+')

    # compare
    sc = sub.add_parser('compare', help='Compare two versions')
    sc.add_argument('version_a')
    sc.add_argument('version_b')

    # sort
    ss = sub.add_parser('sort', help='Sort versions')
    ss.add_argument('versions', nargs='+')
    ss.add_argument('--reverse', '-r', action='store_true', help='Newest first')

    # bump
    sb = sub.add_parser('bump', help='Bump version')
    sb.add_argument('version')
    sb.add_argument('part', choices=['major', 'minor', 'patch', 'prerelease'])
    sb.add_argument('--pre', help='Pre-release tag (e.g., alpha, beta, rc)')

    # filter
    sf = sub.add_parser('filter', help='Filter versions by constraint')
    sf.add_argument('constraint', help='Constraint (e.g., ^1.2.0, ~2.0, >=1.0.0)')
    sf.add_argument('versions', nargs='+')

    # latest
    sl = sub.add_parser('latest', help='Find latest version')
    sl.add_argument('versions', nargs='+')
    sl.add_argument('--constraint', '-c', help='Optional constraint filter')

    args = p.parse_args()
    commands = {
        'validate': cmd_validate,
        'compare': cmd_compare,
        'sort': cmd_sort,
        'bump': cmd_bump,
        'filter': cmd_filter,
        'latest': cmd_latest,
    }
    sys.exit(commands[args.command](args))


if __name__ == '__main__':
    main()
