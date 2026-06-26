# ClawHub Final Submission

## Final Metadata

### Skill name

ZipCracker

### Display name

ZipCracker

### Short description

World-class ZIP CTF cracking, KPA, and recovery workflows

### Final default prompt

Use $zipcracker like a top-tier ZIP CTF solver: profile this archive, choose the strongest clue-driven path, run the bundled workflow, and explain the exact command, rationale, and result.

## Final Chinese Listing Copy

### 标题

ZipCracker

### 一句话卖点

面向 OpenClaw 的世界级 ZIP CTF 技能：先判断题型，再走最强破解路径。

### 短介绍

伪加密修复、字典、掩码、CRC32、模板 KPA、`bkcrack`、AES 研判，一套打穿 ZIP CTF。

### 长介绍

ZipCracker 是一套为 OpenClaw 打磨的高阶 ZIP CTF 技能，不是只会“跑字典”的脚本外壳，而是会先分析压缩包，再按线索选择最强路径的完整解题工作流。

它会先判断档案是否更像伪加密、ZipCrypto、WinZip AES、短明文 CRC32、模板明文攻击，还是已知明文 / `bkcrack` 题型，再驱动内置的 ZipCracker 引擎执行最合适的方案。技能本身覆盖伪加密修复、默认字典与自定义字典、掩码攻击、大字典流式处理、短明文 CRC32 恢复、完整与部分已知明文攻击、`png/zip/exe/pcapng` 模板 KPA、以及 `bkcrack` 加速恢复。

这套技能特别适合 CTF 选手、出题人，以及授权场景下需要快速分析 ZIP 加密与恢复策略的用户。面对“这个包打不开”、“密码大概是四位数字”、“我手里有明文”、“里面看起来像张 PNG”这类真实表达，OpenClaw 可以更自然地命中正确路径，而不是盲目穷举。

### 中文亮点

- 先 profile 后出手，减少无效爆破
- 自动识别伪加密与高价值 KPA 线索
- 支持内置/自定义字典、掩码、大字典流式跑法
- 支持短明文 CRC32、完整 KPA、部分 KPA、模板 KPA
- 支持 `bkcrack` 与 AES 题型边界说明
- 成功后自动解压，并解释为什么选这条路

## Final English Listing Copy

### Title

ZipCracker

### One-line value proposition

A world-class OpenClaw skill for ZIP CTFs that profiles first, then attacks with the strongest clue-driven path.

### Short intro

Pseudo-encryption repair, dictionaries, masks, CRC32 recovery, template KPA, `bkcrack`, and AES triage in one serious ZIP workflow.

### Long description

ZipCracker is a high-end ZIP CTF skill for OpenClaw. It is not a thin wrapper around a brute-force script. Instead, it profiles the archive first and then chooses the strongest recovery path based on real clues.

It identifies whether the case looks like pseudo-encryption, legacy ZipCrypto, WinZip AES, short-plaintext CRC32 recovery, template-based known-plaintext attack, or a full / partial `bkcrack` workflow, then drives the bundled ZipCracker engine accordingly. The skill covers pseudo-encryption repair, built-in and custom dictionaries, mask attacks, large-wordlist streaming, short-plaintext CRC32 recovery, full and partial known-plaintext attacks, template KPA for `png` / `zip` / `exe` / `pcapng`, and `bkcrack`-accelerated recovery.

This makes it a strong fit for CTF players, challenge authors, and authorized recovery workflows that need fast ZIP triage with better reasoning. It handles natural requests like “check if this ZIP is fake-encrypted”, “the password is probably four digits”, “I have a plaintext sample”, or “the encrypted member looks like a PNG” and turns them into the right attack path instead of random guesswork.

### English highlights

- Profile-first ZIP triage for OpenClaw
- Pseudo-encryption repair before unnecessary brute force
- Built-in and custom dictionaries, masks, and huge wordlists
- CRC32 recovery for tiny stored plaintexts
- Full KPA, partial KPA, and template KPA
- `bkcrack`-aware workflows and AES boundary handling
- Automatic extraction and clear reasoning on every run

## Recommended Tags

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

## Recommended Demo Prompts

### Chinese

- 帮我先分析这个 ZIP 是不是伪加密，再决定要不要爆破。
- 这个压缩包密码大概率是四位数字，直接帮我试。
- 我手里有已知明文，帮我用最适合的 KPA / bkcrack 路线恢复。
- 这个加密文件看起来像 PNG，试试模板明文攻击。
- 先 profile 这个 ZIP，再告诉我最值得跑的命令。

### English

- Profile this ZIP first and tell me the strongest recovery path.
- The password is probably four digits. Try the right ZIP attack path.
- I have a plaintext sample. Use the best KPA / bkcrack workflow for this archive.
- The encrypted member looks like a PNG. Try the best template KPA path.
- Recover the files from this ZIP like a serious CTF solver and explain why you chose that route.

## Notes

- This final submission is aligned with `agents/openai.yaml`.
- The default prompt here is the current selected prompt for the published skill.
- If ClawHub asks for fewer fields, prefer: title, short description, long description, default prompt, and tags.
