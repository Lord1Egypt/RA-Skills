<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-triage banner" width="100%" />
</p>

<h1 align="center">yotta-triage · 元鉴 (Yuanjian)</h1>

<p align="center">YottaMeta's zero-dependency <b>static malware triage engine</b>: hashes (<b>MD5 / SHA1 / SHA256</b>), magic-type detection, <b>Shannon entropy</b>, printable-string extraction with <b>URL / domain / IP / email / command / path / base64</b> classification, and <b>PE / ELF header parsing</b> — then outputs a triage report plus an <b>IOC list</b> for downstream intel consumption.</p>
<p align="center">Activates when the user provides a suspicious file / sample (or a folder of samples) and needs hashing, file-type identification, entropy, string extraction, PE/ELF inspection, or a static-first look — <b>fully local and offline: no deobfuscation, no unpacking, no execution, no network lookups</b>.</p>
<p align="center">No external tools required (Python 3.8+ standard library); Windows + Linux + macOS; every result is a hint, never a verdict.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-triage"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-triage" /></a>
  <a href="https://github.com/YottaMeta/yotta-triage"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-triage" /></a>
  <a href="https://github.com/YottaMeta/yotta-triage/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-triage" /></a>
  <a href="https://github.com/YottaMeta/yotta-triage"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## What it is

Malware analysis almost always starts with "what is this file, and what does it look like without running it?". Yuanjian packages that into a zero-dependency engine: it computes hashes, identifies the file type from magic bytes, measures Shannon entropy, extracts and classifies printable strings, and parses PE / ELF headers — using only the Python standard library. No YARA, no sandbox, no commercial malware platform required.

It is not tied to any single platform: it is an agent-agnostic toolkit that works in any agent supporting Agent Skills. **Fully local and offline** — no deobfuscation, no unpacking, no execution, no network lookups, no resident service.

## Core value

- **Zero-dependency engine** — hashing + type detection + entropy + strings + PE/ELF parsing, built entirely with Python 3.8+ standard library.
- **Streaming hashes** — MD5 / SHA1 / SHA256 computed in chunks; large files do not exhaust memory.
- **Type detection** — magic-byte recognition for PE / ELF / Mach-O / PDF / ZIP / gzip / 7z / RAR / OLE / images / pyc / Java class, plus UTF-8 text and shebang scripts.
- **Entropy** — overall Shannon entropy plus per-section PE entropy (packing / encryption / compression hints).
- **String intelligence** — ASCII + UTF-16LE printable strings classified into URLs, domains, IPs, emails, suspicious commands, paths and long base64 blobs.
- **PE / ELF parsing** — architecture, timestamp, optional header, section table (names / characteristics / entropy), packed-section and RWX-section detection; ELF segments / sections with RWE checks.
- **Risk hints, not verdicts** — weighted static indicators produce an info/low/medium/high/critical hint with score and reasons; nothing is ever executed.
- **IOC output** — hashes / URLs / domains / IPs / emails aggregated as JSON, ready for yotta-intel (元情) and other downstream tooling.
- **Three output modes** — text / JSON / Markdown, plus --ioc-only.

## Why use it

| Advantage | Description |
|---|---|
| **Zero dependency** | Python 3.8+ standard library; no daemon / database / YARA / sandbox; Windows + Linux + macOS |
| **Fully local offline** | Read-only analysis of existing files; no deobfuscation, no unpacking, no execution, no network |
| **Explainable** | Every risk hint carries a score and plain-language reasons in Chinese; never a bare verdict |
| **Low noise** | Non-TLD suffix filtering (payload.exe is not a domain), IP octet validation, dedup |
| **Downstream ready** | --ioc-only emits a clean IOC JSON array for yotta-intel and other intel pipelines |
| **Ecosystem distribution** | GitHub + npm + ClawHub synced; four install methods (npx / git clone / Download ZIP / install.sh) |

## Commands

| Command | Description |
|---|---|
| triage --path <file\|dir> | Static triage of one file or a directory |
| triage --recursive | Recurse into subdirectories when scanning a directory |
| triage --format | Output format: text (default) / json / markdown |
| triage --output <file> | Write the report to a file (default: stdout) |
| triage --ioc-only | Emit only the IOC JSON array (for yotta-intel) |
| triage --no-strings | Skip string extraction; report marks it as skipped instead of showing zero strings |
| triage --strings-min <n> | Minimum printable-string length (default 4) |
| triage --strings-limit <n> | Max strings extracted per file (default 500) |
| triage --max-file-mb <n> | Skip files larger than n MB (default 256) |

Exit codes: **0** = max risk ≤ low; **1** = medium; **2** = high; **3** = critical; **4** = usage / read error.

## Quick start

Windows uses python, Linux/macOS uses python3.

```bash
# Triage a single sample (text report)
python3 scripts/yotta_triage.py triage --path sample.exe

# Scan a directory recursively
python3 scripts/yotta_triage.py triage --path samples/ --recursive

# JSON report
python3 scripts/yotta_triage.py triage --path sample.exe --format json --output report.json

# Markdown report
python3 scripts/yotta_triage.py triage --path samples/ --format markdown --output report.md

# IOC only (hashes / URLs / domains / IPs / emails) for yotta-intel
python3 scripts/yotta_triage.py triage --path samples/ --ioc-only --output iocs.json

# Version
python3 scripts/yotta_triage.py --version
```

Sample text output:

```
=== 元鉴 yotta-triage 静态初筛报告 ===
工具: yotta-triage v0.1.1 | 生成: 2026-08-28T00:00:00+00:00
文件: 2（成功 2）| 最高风险: medium | IOC: 5 条

:: sample_upx.exe  (DOS/PE executable (MZ), 4776 bytes)
  MD5   : 8440cd803c0ae8c092da448b2fa810d8
  SHA256: b90093fbae4e34ce410bd63fc203dbd88d94b38f54a7c1f9acca635b12efa203
  熵     : 0.184（全文）
  PE    : PE32+ | x86-64 | 时间戳 2021-05-03 00:00:00 UTC | 区段 2
    - .text     R-X 熵 0.36
    - .UPX0     RW- 熵 0.11
  字符串: 3 条 | 1 URL | 1 域 | 0 IP | 0 邮箱 | 0 命令 | 0 base64
    URL  : http://download.example.net/a.exe
  风险 : 中等风险线索（评分 4）
    - 疑似加壳区段: .UPX0
    - 可执行文件内嵌 URL（1 条）
```

## Installation

Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-triage --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-triage --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-triage.git <your-skills-dir>/yotta-triage
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-triage`, click **Code → Download ZIP**, unzip it and put the `yotta-triage` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.
## Output formats

- **text** — one block per file (hashes / type / entropy / PE-ELF / string stats / risk reasons) plus a file-level IOC summary;
- **json** — {tool, version, generated, summary, files[], iocs[]}; each file carries hashes / type / entropy / strings / pe|elf / risk, and iocs[] is {type, value, file} (ready for yotta-intel);
- **markdown** — fenced text report;
- **--ioc-only** — only the iocs[] JSON array.

## Development & validation

The package ships its own test script (included in the published package):

```bash
# Run the full suite (65 cases) from the skill directory
python scripts/test_yotta_triage.py
```

Spec details live in references/: triage-spec.md (analysis items / magic table / PE-ELF fields / string classification) and risk-model.md (weighting / thresholds / yotta-intel handoff).

## License

MIT © YottaMeta — see LICENSE.
