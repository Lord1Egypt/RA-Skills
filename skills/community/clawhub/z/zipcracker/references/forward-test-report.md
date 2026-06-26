# Forward Test Report

## Table of Contents

- Scope
- Scenario matrix
- Trigger phrase tuning
- Flow tuning outcomes

## Scope

This report records a local forward-test pass for the OpenClaw-oriented `zipcracker` skill on April 11, 2026.

Goals:

- pressure-test the profile-first workflow,
- verify the bundled wrapper on real sample archives,
- tighten trigger phrases based on realistic CTF wording,
- and identify any gaps between natural language clues and the best command path.

## Scenario matrix

| Scenario | Natural-language framing | Command exercised | Result | Tuning outcome |
| --- | --- | --- | --- | --- |
| Fake encryption triage | “先看看是不是伪加密，别急着爆破。” | `python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile test01.zip` and direct run on `test01.zip` | Profile correctly identified pseudo-encryption; main flow repaired and extracted `flag.txt`. | Keep pseudo-encryption high in profile recommendations and trigger copy. |
| Default dictionary path | “就按常规 ZIP 题先跑一遍。” | `python3 <skill-dir>/scripts/openclaw_zipcracker.py test02.zip` | Built-in dictionary recovered password `123456` and extracted `flag.txt`. | Default-flow language is strong and should remain a primary prompt. |
| Short plaintext CRC32 | “这个包里可能有短文件，先试 CRC32。” | `python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile test03.zip` and `--auto-crc test03.zip` | Profile flagged `key.txt(4B)` as a short-plaintext candidate; recovery succeeded with content `G00d`. | Add stronger CRC32 phrasing to examples and keep `--auto-crc` visible. |
| Mask attack | “密码像一位大写加 ali 再加特殊符号和三位数字。” | `python3 <skill-dir>/scripts/openclaw_zipcracker.py test04.zip -m '?uali?s?d?d?d'` | Mask attack succeeded; password recovered as `Kali@123`. | Natural-language mask examples should be prominent because profile alone cannot infer this clue from the archive. |
| Known plaintext KPA | “我有已知明文，直接走 bkcrack/KPA。” | `python3 <skill-dir>/scripts/openclaw_zipcracker.py --skip-orig-password-recovery test05.zip -kpa test05_plain.txt` | KPA succeeded; internal keys recovered and files extracted. | Keep KPA and extraction-first prompts explicit in listing copy. |
| Profile JSON for agent planning | “先给我一个机器可读的 ZIP 分析。” | `python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile-json test05.zip` | JSON output correctly exposed encryption mix, best verification member, and recommendations. | Retain profile JSON as a premium OpenClaw workflow feature. |

## Trigger phrase tuning

Phrases added or strengthened in the skill trigger description after testing:

- `ZIP 爆破`
- `四位数字密码`
- `字典跑一下`
- `明文攻击`
- `看起来像 png/exe/pcapng/zip 模板`
- `这个压缩包打不开`

These phrases improved coverage for:

- casual Chinese CTF wording,
- mask-oriented asks,
- template-KPA asks,
- and pseudo-encryption suspicion phrased as “打不开”.

## Flow tuning outcomes

### What performed especially well

- `--profile` makes the skill feel much more deliberate and premium.
- The wrapper-level auto flags remove friction for CRC32, template-KPA follow-up, and extraction-first workflows.
- Bundling the password list with the skill eliminated current-working-directory fragility.

### Main remaining limitation

- Archive profiling cannot infer password shape clues such as “four digits” or “one uppercase + three lowercase + three digits” from the ZIP itself.

### Mitigation

- Put mask-oriented natural-language examples directly into:
  - the listing copy,
  - the prompt pack,
  - and the natural-language example library.

This ensures OpenClaw reaches the mask path from user wording rather than from archive structure.
