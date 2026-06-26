# OpenClaw Workflow

## Table of Contents

- Goal
- Default operating loop
- Profile mode
- When to skip profile mode
- Reporting style

## Goal

Make OpenClaw feel decisive and smooth:

- inspect first when the clue set is weak,
- choose one strong tactic,
- run it with the bundled wrapper,
- explain the result crisply,
- and only escalate when the evidence supports it.

## Default operating loop

### 1. Profile the archive

Run:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile <zip>
```

This exposes:

- whether the archive is valid ZIP,
- whether it is encrypted at all,
- whether pseudo-encryption is likely confirmed,
- AES vs ZipCrypto composition,
- short-plaintext candidates,
- template-KPA candidates,
- best verification member,
- and recommended next actions.

### 2. Pick one primary tactic

Use the best available clue:

- pseudo-encryption -> just run the wrapper normally and let it repair/extract,
- short plaintext -> add `--auto-crc`,
- template-like member -> add `--auto-template-kpa`,
- custom wordlist -> pass the wordlist directly,
- known plaintext -> switch to `-kpa`,
- structural password clue -> use `-m`.

### 3. Run the main attack

Examples:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --auto-template-kpa <zip>
python3 <skill-dir>/scripts/openclaw_zipcracker.py --auto-crc <zip>
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> <dict.txt>
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -kpa <plain.txt>
```

### 4. Escalate only with evidence

If the first tactic fails:

- use the profile output to justify the next attempt,
- do not enumerate every possible flag,
- do not pretend AES KPA was attempted when `pyzipper` or `bkcrack` was unavailable,
- do not ignore ambiguity in `-c` member matching.

## Profile mode

Human-readable mode:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile <zip>
```

Structured mode:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile-json <zip>
```

Use JSON mode when you want the model to reason from structured fields instead of scanning prose.

## When to skip profile mode

You may skip profile mode when the user already provides a dominant clue:

- a known plaintext file or reference ZIP,
- a specific mask,
- a specific dictionary,
- an explicit template KPA request,
- or a concrete rerun request based on a previous failed command.

## Reporting style

After each run, keep the response compact:

- show the exact command,
- say why this tactic was chosen,
- summarize the result,
- state the next best move only if needed.

This keeps OpenClaw feeling confident instead of verbose.
