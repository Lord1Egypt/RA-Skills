#!/usr/bin/env python3
"""rxtool — Regex testing and extraction tool. Zero dependencies."""
import re, sys, argparse, json

def cmd_test(args):
    pattern = re.compile(args.pattern, flags=get_flags(args))
    text = args.text if args.text else sys.stdin.read()
    matches = list(pattern.finditer(text))
    if not matches:
        print("❌ No matches")
        sys.exit(1)
    print(f"✅ {len(matches)} match(es)")
    for i, m in enumerate(matches):
        print(f"\n  Match {i+1}: \"{m.group()}\" (pos {m.start()}-{m.end()})")
        if m.groups():
            for j, g in enumerate(m.groups(), 1):
                print(f"    Group {j}: \"{g}\"")
        if m.groupdict():
            for k, v in m.groupdict().items():
                print(f"    {k}: \"{v}\"")

def cmd_extract(args):
    pattern = re.compile(args.pattern, flags=get_flags(args))
    text = args.text if args.text else sys.stdin.read()
    matches = pattern.findall(text)
    if args.json:
        print(json.dumps(matches, indent=2))
    else:
        for m in matches:
            if isinstance(m, tuple):
                print("\t".join(m))
            else:
                print(m)

def cmd_replace(args):
    pattern = re.compile(args.pattern, flags=get_flags(args))
    text = args.text if args.text else sys.stdin.read()
    result = pattern.sub(args.replacement, text)
    print(result, end="")

def cmd_split(args):
    pattern = re.compile(args.pattern, flags=get_flags(args))
    text = args.text if args.text else sys.stdin.read()
    parts = pattern.split(text)
    for p in parts:
        if p:
            print(p.strip() if args.strip else p)

def cmd_explain(args):
    """Show regex components."""
    pattern = args.pattern
    components = {
        r'\d': 'digit [0-9]', r'\w': 'word char [a-zA-Z0-9_]', r'\s': 'whitespace',
        r'\b': 'word boundary', r'\D': 'non-digit', r'\W': 'non-word', r'\S': 'non-whitespace',
        '.': 'any char', '^': 'start of string', '$': 'end of string',
        '*': '0 or more', '+': '1 or more', '?': '0 or 1 (optional)',
        '|': 'OR', '\\': 'escape next char',
    }
    print(f"Pattern: {pattern}")
    print(f"Components:")
    for token, desc in components.items():
        if token in pattern:
            print(f"  {token:>4} → {desc}")
    # Try to compile and show groups
    try:
        compiled = re.compile(pattern)
        if compiled.groups:
            print(f"  Groups: {compiled.groups}")
        if compiled.groupindex:
            print(f"  Named groups: {dict(compiled.groupindex)}")
    except re.error as e:
        print(f"  ⚠️ Invalid regex: {e}")

def get_flags(args):
    flags = 0
    if getattr(args, 'ignorecase', False):
        flags |= re.IGNORECASE
    if getattr(args, 'multiline', False):
        flags |= re.MULTILINE
    if getattr(args, 'dotall', False):
        flags |= re.DOTALL
    return flags

def main():
    p = argparse.ArgumentParser(prog="rxtool", description="Regex testing and extraction")
    sub = p.add_subparsers(dest="cmd")

    for name, func, extra_args in [
        ("test", cmd_test, []),
        ("extract", cmd_extract, [("--json", {"action": "store_true"})]),
        ("replace", cmd_replace, [("replacement", {})]),
        ("split", cmd_split, [("--strip", {"action": "store_true"})]),
        ("explain", cmd_explain, []),
    ]:
        s = sub.add_parser(name)
        s.add_argument("pattern")
        if name != "explain":
            s.add_argument("text", nargs="?")
            s.add_argument("-i", "--ignorecase", action="store_true")
            s.add_argument("-m", "--multiline", action="store_true")
            s.add_argument("-s", "--dotall", action="store_true")
        for arg_name, arg_kwargs in extra_args:
            s.add_argument(arg_name, **arg_kwargs)

    args = p.parse_args()
    cmds = {"test": cmd_test, "extract": cmd_extract, "replace": cmd_replace, "split": cmd_split, "explain": cmd_explain}
    if args.cmd in cmds:
        cmds[args.cmd](args)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
