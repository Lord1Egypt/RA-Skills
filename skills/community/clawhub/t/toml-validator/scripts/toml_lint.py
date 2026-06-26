#!/usr/bin/env python3
"""TOML validator and linter — validate syntax, check types, compare files, pretty-print."""

import sys
import json
import argparse
import os

# Python 3.11+ has tomllib in stdlib
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None


def _parse_toml(path):
    """Parse a TOML file and return (data, error)."""
    if tomllib is None:
        return None, 'Python 3.11+ or tomli package required for TOML parsing'
    try:
        with open(path, 'rb') as f:
            data = tomllib.load(f)
        return data, None
    except Exception as e:
        return None, str(e)


def _lint_checks(data, path):
    """Run lint checks on parsed TOML data."""
    findings = []

    def _check(obj, prefix=''):
        if isinstance(obj, dict):
            for k, v in obj.items():
                full_key = f'{prefix}.{k}' if prefix else k
                # Empty string values
                if isinstance(v, str) and v.strip() == '':
                    findings.append({
                        'key': full_key, 'level': 'warning',
                        'message': 'Empty string value'
                    })
                # Empty tables
                if isinstance(v, dict) and len(v) == 0:
                    findings.append({
                        'key': full_key, 'level': 'warning',
                        'message': 'Empty table'
                    })
                # Empty arrays
                if isinstance(v, list) and len(v) == 0:
                    findings.append({
                        'key': full_key, 'level': 'info',
                        'message': 'Empty array'
                    })
                # Keys with spaces (unusual)
                if ' ' in k:
                    findings.append({
                        'key': full_key, 'level': 'info',
                        'message': 'Key contains spaces (valid but unusual)'
                    })
                # Very long string values
                if isinstance(v, str) and len(v) > 1000:
                    findings.append({
                        'key': full_key, 'level': 'info',
                        'message': f'Very long string value ({len(v)} chars)'
                    })
                # Mixed-type arrays
                if isinstance(v, list) and len(v) > 1:
                    types = set(type(i).__name__ for i in v)
                    if len(types) > 1:
                        findings.append({
                            'key': full_key, 'level': 'warning',
                            'message': f'Mixed-type array: {", ".join(sorted(types))}'
                        })
                _check(v, full_key)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                _check(item, f'{prefix}[{i}]')

    _check(data)
    return findings


def _type_tree(data, prefix=''):
    """Build type tree for TOML data."""
    result = {}
    if isinstance(data, dict):
        for k, v in data.items():
            full_key = f'{prefix}.{k}' if prefix else k
            if isinstance(v, dict):
                result[full_key] = 'table'
                result.update(_type_tree(v, full_key))
            elif isinstance(v, list):
                if v and isinstance(v[0], dict):
                    result[full_key] = 'array of tables'
                else:
                    elem_types = set(type(i).__name__ for i in v) if v else {'empty'}
                    result[full_key] = f'array[{",".join(sorted(elem_types))}]'
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        result.update(_type_tree(item, f'{full_key}[{i}]'))
            else:
                result[full_key] = type(v).__name__
    return result


def _diff_toml(data_a, data_b, prefix=''):
    """Compare two TOML structures."""
    diffs = []
    all_keys = set()
    if isinstance(data_a, dict):
        all_keys.update(data_a.keys())
    if isinstance(data_b, dict):
        all_keys.update(data_b.keys())

    for k in sorted(all_keys):
        full_key = f'{prefix}.{k}' if prefix else k
        in_a = isinstance(data_a, dict) and k in data_a
        in_b = isinstance(data_b, dict) and k in data_b

        if in_a and not in_b:
            diffs.append({'key': full_key, 'change': 'removed', 'old_value': _summarize(data_a[k])})
        elif not in_a and in_b:
            diffs.append({'key': full_key, 'change': 'added', 'new_value': _summarize(data_b[k])})
        elif in_a and in_b:
            va, vb = data_a[k], data_b[k]
            if type(va) != type(vb):
                diffs.append({
                    'key': full_key, 'change': 'type_changed',
                    'old_type': type(va).__name__, 'new_type': type(vb).__name__
                })
            elif isinstance(va, dict) and isinstance(vb, dict):
                diffs.extend(_diff_toml(va, vb, full_key))
            elif va != vb:
                diffs.append({
                    'key': full_key, 'change': 'modified',
                    'old_value': _summarize(va), 'new_value': _summarize(vb)
                })
    return diffs


def _summarize(v):
    if isinstance(v, dict):
        return f'table({len(v)} keys)'
    if isinstance(v, list):
        return f'array({len(v)} items)'
    if isinstance(v, str) and len(v) > 50:
        return v[:50] + '...'
    return v


def _toml_to_text(data, indent=0):
    """Pretty-print TOML data as readable text."""
    lines = []
    prefix = '  ' * indent
    for k, v in data.items():
        if isinstance(v, dict):
            lines.append(f'{prefix}[{k}]')
            lines.extend(_toml_to_text(v, indent + 1).split('\n'))
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            for item in v:
                lines.append(f'{prefix}[[{k}]]')
                lines.extend(_toml_to_text(item, indent + 1).split('\n'))
        else:
            lines.append(f'{prefix}{k} = {_format_value(v)}')
    return '\n'.join(lines)


def _format_value(v):
    if isinstance(v, str):
        return f'"{v}"'
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, list):
        return '[' + ', '.join(_format_value(i) for i in v) + ']'
    return str(v)


def cmd_validate(args):
    results = []
    exit_code = 0
    for path in args.files:
        if not os.path.isfile(path):
            results.append({'file': path, 'valid': False, 'error': 'File not found'})
            exit_code = 1
            continue
        data, error = _parse_toml(path)
        if error:
            results.append({'file': path, 'valid': False, 'error': error})
            exit_code = 1
        else:
            entry = {'file': path, 'valid': True, 'keys': len(data)}
            if args.lint:
                findings = _lint_checks(data, path)
                entry['findings'] = findings
                warnings = sum(1 for f in findings if f['level'] == 'warning')
                if warnings > 0:
                    entry['warnings'] = warnings
            results.append(entry)
    _output(results, args.format)
    return exit_code


def cmd_types(args):
    data, error = _parse_toml(args.file)
    if error:
        _output({'file': args.file, 'error': error}, args.format)
        return 1
    tree = _type_tree(data)
    _output({'file': args.file, 'types': tree}, args.format)
    return 0


def cmd_diff(args):
    data_a, err_a = _parse_toml(args.file_a)
    data_b, err_b = _parse_toml(args.file_b)
    if err_a or err_b:
        errors = {}
        if err_a:
            errors['file_a'] = err_a
        if err_b:
            errors['file_b'] = err_b
        _output({'error': errors}, args.format)
        return 1
    diffs = _diff_toml(data_a, data_b)
    result = {
        'file_a': args.file_a, 'file_b': args.file_b,
        'changes': len(diffs), 'diffs': diffs
    }
    _output(result, args.format)
    return 0 if not diffs else 1


def cmd_show(args):
    data, error = _parse_toml(args.file)
    if error:
        _output({'file': args.file, 'error': error}, args.format)
        return 1
    if args.key:
        parts = args.key.split('.')
        current = data
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                _output({'file': args.file, 'key': args.key, 'error': 'Key not found'}, args.format)
                return 1
        _output({'file': args.file, 'key': args.key, 'value': current, 'type': type(current).__name__}, args.format)
    else:
        if args.format == 'json':
            print(json.dumps(data, indent=2, default=str))
        else:
            print(_toml_to_text(data))
    return 0


def _output(data, fmt):
    if fmt == 'json':
        print(json.dumps(data, indent=2, default=str))
    elif fmt == 'markdown':
        _output_md(data)
    else:
        _output_text(data)


def _output_text(data):
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                valid = item.get('valid')
                if valid is not None:
                    status = '✅' if valid else '❌'
                    print(f'{status} {item.get("file", "?")}', end='')
                    if not valid:
                        print(f'  Error: {item.get("error", "?")}')
                    else:
                        print(f'  ({item.get("keys", 0)} top-level keys)')
                    for f in item.get('findings', []):
                        icon = '⚠️' if f['level'] == 'warning' else 'ℹ️'
                        print(f'  {icon} {f["key"]}: {f["message"]}')
                else:
                    for k, v in item.items():
                        print(f'  {k}: {v}')
    elif isinstance(data, dict):
        if 'diffs' in data:
            if data['changes'] == 0:
                print('✅ Files are identical')
            else:
                print(f'Found {data["changes"]} difference(s):')
                for d in data['diffs']:
                    change = d['change']
                    if change == 'added':
                        print(f'  + {d["key"]}: {d["new_value"]}')
                    elif change == 'removed':
                        print(f'  - {d["key"]}: {d["old_value"]}')
                    elif change == 'modified':
                        print(f'  ~ {d["key"]}: {d["old_value"]} → {d["new_value"]}')
                    elif change == 'type_changed':
                        print(f'  ! {d["key"]}: {d["old_type"]} → {d["new_type"]}')
        elif 'types' in data:
            for k, t in data['types'].items():
                print(f'  {k}: {t}')
        elif 'error' in data:
            print(f'❌ {data.get("file", "?")}  Error: {data["error"]}')
        else:
            for k, v in data.items():
                print(f'{k}: {v}')


def _output_md(data):
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                valid = item.get('valid')
                status = '✅' if valid else '❌'
                print(f'### {status} {item.get("file", "?")}')
                if not valid:
                    print(f'**Error:** {item.get("error", "?")}')
                else:
                    print(f'**Keys:** {item.get("keys", 0)}')
                for f in item.get('findings', []):
                    level = '⚠️' if f['level'] == 'warning' else 'ℹ️'
                    print(f'- {level} `{f["key"]}`: {f["message"]}')
    elif isinstance(data, dict):
        if 'diffs' in data:
            print(f'## Diff: {data.get("file_a")} vs {data.get("file_b")}')
            print(f'**Changes:** {data["changes"]}')
            if data['diffs']:
                print('| Key | Change | Details |')
                print('|-----|--------|---------|')
                for d in data['diffs']:
                    details = ''
                    if d['change'] == 'added':
                        details = f'New: {d["new_value"]}'
                    elif d['change'] == 'removed':
                        details = f'Was: {d["old_value"]}'
                    elif d['change'] == 'modified':
                        details = f'{d["old_value"]} → {d["new_value"]}'
                    elif d['change'] == 'type_changed':
                        details = f'{d["old_type"]} → {d["new_type"]}'
                    print(f'| `{d["key"]}` | {d["change"]} | {details} |')
        else:
            for k, v in data.items():
                if isinstance(v, dict):
                    print(f'**{k}:**')
                    for sk, sv in v.items():
                        print(f'- `{sk}`: {sv}')
                else:
                    print(f'**{k}:** {v}')


def main():
    p = argparse.ArgumentParser(description='TOML validator and linter')
    p.add_argument('--format', '-f', choices=['text', 'json', 'markdown'], default='text')
    sub = p.add_subparsers(dest='command', required=True)

    # validate
    sv = sub.add_parser('validate', help='Validate TOML files')
    sv.add_argument('files', nargs='+')
    sv.add_argument('--lint', '-l', action='store_true', help='Run lint checks')

    # types
    st = sub.add_parser('types', help='Show type tree')
    st.add_argument('file')

    # diff
    sd = sub.add_parser('diff', help='Compare two TOML files')
    sd.add_argument('file_a')
    sd.add_argument('file_b')

    # show
    ss = sub.add_parser('show', help='Pretty-print TOML or extract key')
    ss.add_argument('file')
    ss.add_argument('--key', '-k', help='Extract specific key (dot-separated)')

    args = p.parse_args()
    commands = {
        'validate': cmd_validate,
        'types': cmd_types,
        'diff': cmd_diff,
        'show': cmd_show,
    }
    sys.exit(commands[args.command](args))


if __name__ == '__main__':
    main()
