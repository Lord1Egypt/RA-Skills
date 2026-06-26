---
name: zipcracker
description: CTF-oriented ZIP cracking and recovery with the bundled ZipCracker engine. Use when Codex or OpenClaw needs to analyze or recover an encrypted ZIP in authorized contexts, including pseudo-encryption repair, default dictionary attacks, custom wordlists, mask attacks, short-plaintext CRC32 recovery, known-plaintext attacks, bkcrack workflows, template KPA, WinZip AES triage, or large-dictionary handling. Trigger on requests mentioning zip password, encrypted zip, ZIP challenge, 压缩包破解, ZIP 爆破, 伪加密, 掩码, 四位数字密码, 字典跑一下, 已知明文, 明文攻击, bkcrack, CRC32, AES ZIP, 看起来像 png/exe/pcapng/zip 模板, 这个压缩包打不开, or ClawHub/OpenClaw ZIP solving.
---

# ZipCracker

Use this skill as a self-contained ZIP cracking package. Always prefer the bundled wrapper in `scripts/openclaw_zipcracker.py` over assuming the original repository still exists somewhere else.

Only use it for CTF, self-owned archives, or authorized security work. If the request sounds like unauthorized access to third-party data, refuse.

## Quick Start

1. Collect the minimum inputs before running anything:
- Target ZIP path.
- Whether the user already has a dictionary, a password pattern, a known plaintext file, a passwordless reference ZIP, or only a file signature guess.
- Whether the user wants the original ZIP password itself, or only wants extraction/recovery.
- Whether the archive is clearly ZIP-specific; do not force this skill onto `rar` or `7z`.

2. In ambiguous cases, inspect first:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile <zip>
```

Use the profile mode to surface pseudo-encryption, AES vs ZipCrypto mix, short-plaintext candidates, template KPA candidates, and recommended next commands.

3. Run the bundled wrapper:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> ...
```

4. Prefer the wrapper flags over ad-hoc environment variables:
- `--auto-crc` for short-plaintext CRC32 prompts.
- `--auto-template-kpa` to let the bundled engine follow up on template-KPA suggestions automatically.
- `--auto-large-mask` only when the user explicitly accepts a very large mask search.
- `--skip-dict-count` for huge wordlists.
- `--skip-orig-password-recovery` when the user only cares about extraction speed after a `bkcrack`-based recovery.
- `--allow-install-prompts` only when the user explicitly wants interactive dependency installation attempts.

5. Keep the current working directory as the project directory that contains the target ZIP. The bundled engine resolves its own built-in dictionary relative to the skill, so custom relative paths for the target, plaintext, or dictionary still behave naturally.

## Decision Tree

### 1. Start with the least-assumption path

When the user only says "crack this ZIP" or "analyze this archive", inspect first, then begin with the default flow:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile <zip>
```

Then:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --auto-template-kpa <zip>
```

This preserves the original ZipCracker mindset:
- Try pseudo-encryption repair before brute force.
- Warn about AES and missing `pyzipper`.
- Use the built-in dictionary first.
- Fall back to the generated 1-6 digit numeric dictionary.
- Offer template-based KPA when the archive structure strongly suggests it.

Add `--auto-crc` only when short-plaintext recovery is likely relevant or when the user explicitly asks to try CRC32-style recovery.

### 2. Choose the main attack based on the best clue

- If the user has a custom dictionary file or dictionary directory:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> <dict-or-dir>
```

- If the user knows the password shape, use a mask:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -m '?u?l?l?l?d?d'
```

- If the user has a full known plaintext file or a passwordless reference ZIP, use `-kpa`:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -kpa <plain-file-or-zip>
```

- If the known plaintext is partial, add offset and extra known bytes:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -kpa <part.bin> --kpa-offset 78 -x 0 4d5a
```

- If the user only knows the file type or magic header, use a built-in template:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> --kpa-template png -c image.png
```

- If the user wants pure `bkcrack` recovery and does not want fallback methods:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -kpa <plain-file> --bkcrack
```

### 3. Prefer the strongest clue instead of stacking random tactics

- Full known plaintext beats mask guessing.
- Partial known plaintext plus `bkcrack` usually beats blind dictionary work when at least some bytes are reliable.
- A realistic custom wordlist beats the built-in defaults.
- A tight mask beats a giant generic wordlist.
- Template KPA is worth trying when the encrypted member looks like `png`, `zip`, `exe`, or `pcapng`.

## Solving Heuristics

### Pseudo-encryption first

Do not jump directly into brute force when the request is vague. The bundled engine already attempts pseudo-encryption repair by clearing the encryption bit and validating extraction. Keep that behavior because many CTF ZIP tasks are fake-encrypted rather than truly protected.

### Short plaintext CRC32 recovery

Use CRC32 recovery only for entries whose plaintext size is 1 to 6 bytes. This is not a generic password attack; it is a content recovery trick for tiny stored plaintexts. In OpenClaw, opt in with `--auto-crc` when the challenge obviously contains tiny files or the user asks to try CRC-based recovery.

### KPA matching rules

When using `-kpa`, the engine reproduces the original matching strategy:
- Prefer an encrypted member with the same full inner path.
- Otherwise prefer the same basename.
- If the plaintext ZIP contains exactly one usable file, use it automatically.
- If the encrypted ZIP contains exactly one encrypted regular file, use it automatically.
- If matching is ambiguous, supply `-c <inner-name>` explicitly.

### Partial KPA strength

Treat partial KPA as high-value only when the hints are meaningful. The original tool prints a warning when the known bytes are weak. In practice:
- Aim for at least 12 known bytes total.
- Aim for at least 8 contiguous bytes.
- Add `-x` byte fragments when you know fixed values like `MZ`, `PE`, or chunk markers.

### Template KPA strategy

The bundled engine carries the original built-in templates:
- `png`
- `zip`
- `exe`
- `pcapng`

These are strongest when:
- The encrypted member extension matches the template family.
- The file is `ZIP_STORED`, or at least size-compatible with a known header pattern.
- The user has no full plaintext but the file type is obvious.

If the user says "run the full default workflow", include `--auto-template-kpa` so OpenClaw does not stall at the follow-up prompt.

### Dictionary and mask strategy

- Start with the bundled defaults only when the user has no better clue.
- Use the user's dictionary immediately when they provide one.
- Use `--skip-dict-count` for very large wordlists to avoid expensive upfront line counting.
- Use `--auto-large-mask` only after the user explicitly accepts the cost of a huge mask search.
- Remember that the built-in default sequence is: bundled `password_list.txt` then 1-6 digit numeric passwords.

### AES and bkcrack caveats

- WinZip AES is supported for dictionary and mask workflows when `pyzipper` is available, but it is slower.
- Fast in-memory known-plaintext validation only applies to legacy ZipCrypto, not WinZip AES.
- `bkcrack` is the preferred path for full or partial KPA on ZipCrypto.
- Without `bkcrack`, partial/template KPA should be explained as unavailable rather than pretending it was tried.

## Execution Rules for OpenClaw

- Default to `--profile` before cracking when the user has not already provided a strong clue.
- Use `scripts/openclaw_zipcracker.py` as the command entrypoint.
- Quote and show the exact command you ran in your response.
- Explain why the selected attack path matches the available clues.
- If a run fails, choose the next tactic based on evidence, not by blindly enumerating every flag.
- If dependencies are missing in a restricted environment, explain the blocker and the next best path. Do not imply AES KPA succeeded when it was skipped.
- If the user only wants the decrypted contents, prefer `--skip-orig-password-recovery` after successful `bkcrack` extraction.

## Command Patterns

- Profile first:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile <zip>
```

- Default triage:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --auto-template-kpa <zip>
```

- Huge custom dictionary:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --skip-dict-count <zip> <huge-dict.txt>
```

- Tight mask:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -m '?l?l?l?l?d?d'
```

- Known plaintext ZIP:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -kpa <plain.zip>
```

- Partial known plaintext plus extra bytes:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -kpa <part.bin> --kpa-offset 78 -x 0 4d5a -x 128 50450000
```

- Template KPA:

```bash
python3 <skill-dir>/scripts/openclaw_zipcracker.py --auto-template-kpa <zip> --kpa-template exe -c app.exe
```

## References

- Read `references/clawhub-final-submission.md` when you need the final recommended Chinese and English storefront copy, tags, and default prompt for direct submission.
- Read `references/clawhub-publishing-copy.md` when you need polished listing copy, tags, and a prompt pack for ClawHub.
- Read `references/clawhub-bilingual-copy.md` when you need Chinese and English storefront copy with stronger marketing positioning.
- Read `references/competitive-ctf-prompts.md` when you want a sharper, more player-like default prompt or demo prompt.
- Read `references/natural-language-command-examples.md` when the user request is vague but contains clues that should map to a specific command.
- Read `references/forward-test-report.md` for the latest local pressure-test findings and wording adjustments.
- Read `references/release-checklist.md` before publishing or updating the skill on ClawHub.
- Read `references/openclaw-workflow.md` for the preflight-to-execution flow optimized for OpenClaw.
- Read `references/attack-playbook.md` for concrete user-intent-to-command mappings.
- Read `references/ctf-techniques.md` for the full reproduction of the tool's solving logic, clue prioritization, and troubleshooting heuristics.
