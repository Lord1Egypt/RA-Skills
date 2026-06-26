# CTF Techniques

## Table of Contents

- Core mindset
- Pseudo-encryption repair
- Default brute-force sequence
- Short-plaintext CRC32 recovery
- Mask attack details
- Known-plaintext attack details
- Template KPA details
- AES and ZipCrypto boundaries
- Performance and troubleshooting

## Core mindset

The original project is not just a ZIP password cracker. It is a layered CTF workflow:

1. Remove fake encryption first.
2. Use the strongest clue before brute force.
3. Fall back progressively instead of blindly combining every technique.
4. Extract automatically on success.
5. Keep the operator informed about why a path is strong or weak.

Preserve that ordering in OpenClaw.

## Pseudo-encryption repair

The bundled engine treats the encryption bit as a hypothesis, not a fact:

- If the ZIP advertises encryption, try clearing the bit and validating extraction.
- If the repaired copy extracts cleanly, stop there and report pseudo-encryption success.
- If the repair fails, continue with true-encryption workflows.

This matters because many CTF ZIP tasks are "fake encrypted" and do not need any password work at all.

## Default brute-force sequence

When no better clue exists, the engine reproduces the original sequence:

1. Try the bundled `password_list.txt`.
2. Try generated numeric passwords from 1 to 6 digits.
3. If the archive shape strongly suggests a built-in template KPA case, offer template KPA.

Do not override this sequence with random extra dictionaries unless the user provides them.

## Short-plaintext CRC32 recovery

CRC32 recovery in this tool is a content-recovery trick, not a password crack:

- It only applies to regular entries of size 1 to 6 bytes.
- It enumerates printable plaintext candidates until the ZIP entry CRC32 matches.
- If all files in the archive are recovered this way, dictionary brute force is skipped.

Use it when the archive obviously contains tiny marker files, challenge flags, or short tokens.

## Mask attack details

Mask placeholders mirror the original CLI:

- `?d` -> digits
- `?l` -> lowercase letters
- `?u` -> uppercase letters
- `?s` -> punctuation/symbols
- `??` -> literal `?`

Use a mask only when the clue is genuinely structural, such as:

- "four digits"
- "starts with `flag` and ends in two numbers"
- "one uppercase, three lowercase, three digits"

If the search space is enormous, keep the original caution: confirm the user wants that cost before auto-running it.

## Known-plaintext attack details

The skill bundles the same KPA logic as the original tool.

### Full plaintext

Use `-kpa` when the user has:

- the exact plaintext file corresponding to an encrypted member, or
- a passwordless ZIP containing the corresponding plaintext member.

Matching priority:

1. Exact inner path match.
2. Basename match.
3. Single usable file in the plaintext ZIP.
4. Single encrypted regular file in the target ZIP.

When matching is ambiguous, use `-c`.

### Partial plaintext

When the user only knows a fragment:

- supply `--kpa-offset` for the plaintext start offset inside the target file,
- add `-x offset hex` fragments for other fixed bytes,
- prefer cases with at least 12 known bytes total and at least 8 contiguous bytes.

### Original password recovery after KPA

After `bkcrack` recovers internal keys and extraction succeeds, the engine may still try to recover the original password:

- first by testing the built-in dictionary, common weak passwords, and 1-6 digit numbers,
- then by using `bkcrack` password recovery.

If the user only cares about extraction speed, use `--skip-orig-password-recovery`.

## Template KPA details

The bundled template families are:

- `png`
- `zip`
- `exe`
- `pcapng`

Important heuristics from the original project:

- Extension matching is the first clue.
- `ZIP_STORED` entries are higher-confidence template KPA candidates.
- Size must be compatible with the header or stub bytes of the candidate template.
- `exe` candidates can also benefit from `MZ`, DOS-stub text, and `PE` anchors.

Use template KPA when the file type is obvious but the user has no complete plaintext.

## AES and ZipCrypto boundaries

Preserve these boundaries exactly:

- Dictionary and mask workflows can work on AES ZIPs when `pyzipper` is available.
- AES verification and extraction are slower than legacy ZipCrypto.
- Fast in-memory known-plaintext validation is only for legacy ZipCrypto.
- WinZip AES is not a valid target for the same fast KPA path.
- Partial/template KPA without `bkcrack` should be described as unavailable, not silently skipped.

## Performance and troubleshooting

### Large dictionaries

For very large wordlists:

- Use `--skip-dict-count`.
- Expect progress to switch from password-count mode to streamed file-read mode.

### bkcrack on unstable systems

Useful environment hints retained from the original project:

- `BKCRACK_JOBS=1` to reduce parallelism during troubleshooting.
- `ZIPCRACKER_SKIP_ORIG_PW_RECOVERY=1` to stop after extraction.

### Common interpretation rules

- "Recovered internal keys" means the archive can usually be decrypted even if the original password is still unknown.
- "Pseudo-encryption fixed successfully" means no brute force was required.
- "Plaintext length does not match ciphertext payload length" means the current full-plaintext assumption is wrong; switch to partial KPA, extra bytes, or templates.
