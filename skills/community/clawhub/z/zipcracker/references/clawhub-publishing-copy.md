# ClawHub Publishing Copy

## Table of Contents

- Hero copy
- Short listing copy
- Full listing description
- Prompt pack
- Suggested tags

## Hero copy

### Primary title

ZipCracker

### Primary tagline

World-class ZIP CTF cracking, recovery, and known-plaintext workflows for OpenClaw.

### Alternate taglines

- Turn ZIP challenge clues into the right cracking path, not just more brute force.
- Profile first, strike with the strongest tactic, and recover files fast.
- Pseudo-encryption, masks, CRC32, KPA, `bkcrack`, and AES triage in one OpenClaw-ready skill.

## Short listing copy

### Recommended

OpenClaw-native ZIP CTF skill with pseudo-encryption repair, dictionaries, masks, CRC32 recovery, template KPA, and `bkcrack` workflows.

### Alternate short copies

- Built for ZIP CTFs: profile the archive, pick the strongest clue, and recover fast.
- A serious ZIP challenge skill for OpenClaw, from fake encryption to full KPA recovery.

## Full listing description

### Recommended long description

ZipCracker is a world-class ZIP recovery skill for OpenClaw, built for serious CTF workflows rather than one-size-fits-all brute force. It profiles the archive first, identifies whether the case looks like pseudo-encryption, ZipCrypto, AES, short-plaintext CRC32, or a template-based known-plaintext attack, then drives the bundled ZipCracker engine down the strongest path.

It covers the full ZIP challenge ladder: pseudo-encryption repair, built-in and custom dictionaries, mask attacks, large-wordlist handling, short-plaintext CRC32 recovery, full and partial known-plaintext attacks, template KPA for `png` / `zip` / `exe` / `pcapng`, and `bkcrack`-accelerated recovery. When the archive can be recovered, it extracts automatically; when it cannot, it explains the next best move instead of blindly guessing.

This skill is ideal for CTF players, challenge authors, and authorized recovery or testing workflows that need fast ZIP triage with strong reasoning. It is not a thin wrapper around a script: it captures the actual solving philosophy of the underlying tool so OpenClaw can choose better tactics from natural language clues like “this password is probably four digits”, “I have a known plaintext file”, “the file inside looks like a PNG”, or “help me check if this ZIP is fake-encrypted”.

### Capability bullets

- Inspect first with human-readable or JSON archive profiling.
- Repair pseudo-encryption before wasting time on brute force.
- Run bundled dictionary and numeric fallbacks automatically.
- Use custom wordlists and directories of wordlists.
- Support mask attacks with realistic password-structure clues.
- Recover tiny stored plaintexts with CRC32 enumeration.
- Drive full and partial KPA workflows with `bkcrack`.
- Recognize template-KPA cases for `png`, `zip`, `exe`, and `pcapng`.
- Handle AES ZIP triage and explain `pyzipper` constraints clearly.
- Skip original password recovery when the user only wants extracted files.

## Prompt pack

### Recommended default prompt

Use $zipcracker to profile this ZIP, choose the strongest recovery path, run the bundled workflow, and explain the exact command, rationale, and result.

### Alternate default prompts

- Use $zipcracker to inspect this archive first, then recover it with the best ZIP CTF technique available.
- Use $zipcracker to decide whether this ZIP is fake-encrypted, dictionary-worthy, mask-worthy, or a KPA case, then run the right command.
- Use $zipcracker to solve this ZIP challenge the way an experienced CTF player would: profile, choose the best clue, run, and report.
- Use $zipcracker to recover files from this encrypted ZIP and tell me whether the winning path was pseudo-encryption, dictionary, mask, CRC32, or KPA.
- Use $zipcracker to evaluate this ZIP for `bkcrack`, template KPA, and short-plaintext recovery before falling back to brute force.

### User-facing sample prompts

- 帮我看看这个压缩包是不是伪加密，别急着暴力跑。
- 这个 ZIP 密码大概率是四位数字，帮我直接试。
- 我有一份已知明文，帮我走 `bkcrack` / KPA。
- 这个压缩包里面看起来像张 PNG，试试模板明文攻击。
- 先分析这个 ZIP，再告诉我最值得跑的命令。
- Crack this ZIP like a CTF task and tell me why you chose that path.
- I only want the extracted files, not the original password.

## Suggested tags

- zip
- ctf
- password-cracking
- bkcrack
- known-plaintext
- pseudo-encryption
- crc32
- aes
- forensics
- archive-recovery
