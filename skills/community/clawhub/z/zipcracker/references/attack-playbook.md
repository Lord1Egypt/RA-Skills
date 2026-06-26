# Attack Playbook

## Table of Contents

- Inputs to gather
- Intent-to-command mapping
- When to rerun with a different tactic
- Output contract
- Wrapper flags

## Inputs to gather

Before choosing a command, identify:

- The target ZIP path.
- Whether the user has a custom dictionary file or a directory of wordlists.
- Whether the user knows a mask pattern.
- Whether the user has a full plaintext file, a passwordless reference ZIP, or only a partial plaintext fragment.
- Whether the user knows the inner member name in the encrypted ZIP.
- Whether the user only wants extraction, or also wants the original ZIP password.
- Whether the archive is likely `png`, `zip`, `exe`, or `pcapng` inside.

If the clue set is weak, run profile mode first:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile <zip>
```

## Intent-to-command mapping

### "Just analyze / crack this ZIP"

Start with:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile <zip>
python3 <skill-dir>/scripts/openclaw_zipcracker.py --auto-template-kpa <zip>
```

If you only want the attack command and already understand the archive shape:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --auto-template-kpa <zip>
```

Add `--auto-crc` only when the archive likely contains tiny plaintext files or the profile output flags short-plaintext candidates.

### "Use this dictionary"

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> <dict-or-dir>
```

If the wordlist is large:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --skip-dict-count <zip> <huge-dict.txt>
```

### "The password looks like ..."

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -m '<mask>'
```

Only add `--auto-large-mask` when the user accepts a very large search space.

### "I have a plaintext file / reference ZIP"

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -kpa <plain-file-or-zip>
```

If matching the encrypted member is ambiguous, add:

```bash
-c <inner-name>
```

### "I only know part of the plaintext"

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -kpa <part.bin> --kpa-offset <offset> -x <offset> <hex>
```

Repeat `-x` for additional byte anchors.

### "I only know the file type"

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> --kpa-template png -c image.png
```

Template values:

- `png`
- `zip`
- `exe`
- `pcapng`

### "Use bkcrack only"

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -kpa <plain-file> --bkcrack
```

### "Only get the files out quickly"

If you expect `bkcrack` to recover internal keys and the user does not care about the original password:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --skip-orig-password-recovery <zip> -kpa <plain-file>
```

## When to rerun with a different tactic

- If the default flow fails and the archive clearly contains `png`, `zip`, `exe`, or `pcapng`, rerun with template KPA if it was not already enabled.
- If a custom dictionary fails but the user knows password structure, switch to a mask rather than trying more generic dictionaries.
- If `-kpa` fails because the plaintext length does not match, move to partial KPA with `--kpa-offset`, `-x`, or a template.
- If the archive uses WinZip AES, stop suggesting fast ZipCrypto KPA and switch to dictionary or mask logic.
- If multiple encrypted inner members exist and matching is unclear, inspect member names and rerun with `-c`.

## Output contract

When reporting back:

- Show the exact command you ran.
- State why that tactic was chosen.
- Summarize the key result:
  - pseudo-encryption repaired,
  - password recovered,
  - files extracted,
  - internal keys recovered via `bkcrack`,
  - or the next best tactic.
- If the run was blocked by missing `pyzipper` or `bkcrack`, say so explicitly.

## Wrapper flags

The wrapper maps OpenClaw-friendly flags to the bundled engine:

- `--auto-crc` -> auto-confirm short-plaintext CRC32 enumeration.
- `--auto-large-mask` -> auto-confirm huge mask warnings.
- `--auto-template-kpa` -> auto-confirm suggested built-in KPA templates.
- `--skip-dict-count` -> skip upfront dictionary line counting.
- `--skip-orig-password-recovery` -> stop after extraction instead of chasing the original password.
- `--allow-install-prompts` -> allow interactive install prompts for `pyzipper` and `bkcrack`.
- `--lang zh|en` -> choose the Chinese or English CLI layer.
