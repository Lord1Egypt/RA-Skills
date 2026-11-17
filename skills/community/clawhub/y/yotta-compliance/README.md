<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-compliance banner" width="100%" />
</p>

<h1 align="center">yotta-compliance · 元规 (YuanGui)</h1>

<p align="center">YottaMeta's <b>deterministic compliance clause reviewer</b>: review UTF-8 text or Markdown
against versioned JSON rule packs, then output a report where every finding returns to
<b>source text evidence, the matched rule, the framework coverage level, and the cited provision</b>.</p>
<p align="center">Current <b>baseline_review</b> packs: PIPL (11 rules) and data export (4 rules).
GDPR / HIPAA / SOC2 / PCI-DSS / ISO27001 / China MLPS are <b>mapping_only</b> topic labels,
not independent compliance conclusions.</p>
<p align="center">Pure Python 3.8+ standard library, zero external dependencies; Windows + Linux + macOS;
local-only, no model calls and no network access in the review path.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-compliance"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-compliance" /></a>
  <a href="https://github.com/YottaMeta/yotta-compliance"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-compliance" /></a>
  <a href="https://github.com/YottaMeta/yotta-compliance/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-compliance" /></a>
</p>

## What it is

yotta-compliance reviews text or Markdown clauses with deterministic rules. It parses the document
structure, matches rule candidates, evaluates assertions, extracts source-text evidence, applies
framework coverage labels, and renders both a human-readable Markdown report and a stable JSON
contract.

It is a review aid, not a legal opinion. Every risk statement must point to source text, a rule id,
and a cited provision. If a rule cannot locate evidence, it does not invent a risk conclusion.

## Core value

- **Evidence first** — every `matched_span` quote is sliced from the original text, with original
  `start` / `end` offsets plus line and column.
- **Deterministic** — the same input, rule packs, and options produce the same report; only
  `generated_at` changes between runs.
- **Versioned rule packs** — each pack carries `pack_id`, `pack_version`, coverage level, and a
  SHA-256 in the report.
- **Explicit coverage levels** — `baseline_review` can produce findings; `mapping_only` is only a
  topic label and cannot be read as a completed framework review.
- **Stable JSON contract** — a fixed top-level schema for automation, audit records, and CI gates.
- **Local and zero-dependency** — Python 3.8+ standard library; no network, no model, no database.

## Coverage

| Pack | Framework | Level | Rules |
|---|---|---|---|
| `pipl` | PIPL | `baseline_review` | 11 |
| `data-export` | Data export | `baseline_review` | 4 |

GDPR / HIPAA / SOC2 / PCI-DSS / ISO27001 / China MLPS are `mapping_only`. They receive topic
labels only; the report does not output independent conclusions for them.

See [references/coverage.md](references/coverage.md) for the full rule list, cited provisions, topic
mappings, and the explicit out-of-scope list.

## Commands

| Command | Description |
|---|---|
| `review --input <file>` | Review a UTF-8 `.txt` / `.md` / `.markdown` file |
| `review --stdin` | Read text from standard input |
| `review --frameworks <list>` | Select packs by comma-separated id; default loads all packs |
| `review --format md\|json` | Markdown (default) or JSON |
| `review --out <file>` | Write the report to a file; default writes stdout |
| `review --gate <level>` | CI gate: `off` / `low` / `medium` / `high` / `critical` |
| `review --min-severity <level>` | Filter emitted findings by minimum severity |
| `review --include-safe` | List checked-but-unmatched rules |
| `rules list` | List packs and rules |
| `rules show <rule_id>` | Show one rule's rationale, remediation, source, and test ids |
| `rules validate --pack <file>` | Validate a rule pack and fail on any schema error |

Exit codes: **0** completed without hitting the gate; **1** gate hit; **2** input / encoding / path
error; **3** rule-pack error; **4** CLI usage error.

## Quick start

Windows uses `python`; Linux and macOS use `python3`.

```bash
# Review with the default packs
python3 scripts/yotta_compliance.py review --input contract.md

# Review only the PIPL pack
python3 scripts/yotta_compliance.py review --input contract.md --frameworks pipl

# JSON report + CI gate at high
python3 scripts/yotta_compliance.py review --input contract.md --format json --gate high --out report.json

# Read from stdin
python3 scripts/yotta_compliance.py review --stdin --frameworks pipl,data-export

# Inspect and validate the shipped rule packs
python3 scripts/yotta_compliance.py rules list --framework pipl
python3 scripts/yotta_compliance.py rules show PIPL-NOTICE-001
python3 scripts/yotta_compliance.py rules validate --pack rules/pipl.json
```

The report is written to stdout unless `--out` is provided. Output must not overwrite the input file
or be written inside the rule-pack directory.

## Example

Input fragment:

```text
我们收集你的个人信息，用于提供服务。
保存期限：3年。
数据出境至境外服务器。
```

The default run on a deliberately incomplete document reports the following summary:

```text
- 本次输出 11 条发现（全部 11 条）
- high：3 条
- medium：4 条
- low：4 条
- 已检查规则：15 条 ｜ 命中规则：13 条
```

The exact result depends on the input and selected packs. A gate at `high` returns exit code 1 when
the `high` findings are present.

## Report contract

The Markdown report always contains seven sections: input summary, framework coverage summary, risk
summary, findings, out-of-scope ranges, manual review list, and disclaimer.

The JSON report always provides:

```json
{
  "schema_version": "1.0",
  "tool": "yotta-compliance",
  "tool_version": "0.1.0",
  "generated_at": "2026-09-24T12:00:00Z",
  "input": {},
  "rule_packs": [],
  "framework_coverage": [],
  "summary": {},
  "findings": [],
  "review_items": [],
  "disclaimer": "本工具提供基于确定性规则的条款审查建议与证据链，不构成法律意见。"
}
```

Field-level semantics, evidence shapes, and filtering behavior are documented in
[references/report-format.md](references/report-format.md).

## Known limitations

- **Word-form matching, not semantic understanding** — absence rules check whether the listed
  search terms appear; synonyms with different wording may be missed.
- **Document-level absence scope** — a term found anywhere in the document counts as present,
  regardless of whether it applies to the processing activity.
- **Negation is not modeled** — phrases such as “we will not share data” can still match a
  candidate rule.
- **Arabic numerals only** — `保存期限：N年` is parsed; Chinese numerals such as “三年” are not
  converted or compared.
- **No cross-border headcount thresholds in v1** — thresholds requiring unit-aware numbers are
  deferred to rule-pack v2 instead of producing a potentially wrong comparison.
- **Absence findings are deliberately lower confidence** — medium / low confidence findings are
  placed in the manual review list.
- **No direct PDF / docx parsing** — convert documents to UTF-8 text or Markdown first.
- **`mapping_only` is not a review** — it is a topic label only.

## Data and security boundaries

- Runs locally; it does not upload source text, evidence, or reports and does not fetch laws online.
- Rule packs are read-only data; rule content is never executed.
- Input limit: 2 MiB, UTF-8 text only.
- Writes to stdout unless `--out` is explicitly provided.
- Output path guards prevent overwriting the input or writing into the rule-pack directory.
- Source text is not cached or written to logs.

## Usage with an AI agent

1. Install the skill into the agent's skills directory (see **Install** below).
2. When the user asks for a PIPL or data-export clause review, run `review` against the supplied
   text or Markdown file.
3. Report the coverage summary first: state which frameworks are `baseline_review` and which are
   `mapping_only`.
4. Walk through findings by severity, quoting the source evidence and citing the rule's provision.
5. Treat all low-confidence findings as manual-review items; never present them as final legal
   conclusions.
6. Keep the original document unchanged unless the user explicitly asks for a separate report file.

## Install

Pick any of the four methods below; the order is the recommended priority. Skill files come from
**npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-compliance --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-compliance --dir <your-skills-dir>   # point to the skills dir itself
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each
  agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir`
  at their skills directory.
- If the mirror has not synced the new package (404): add
  `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror
  cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-compliance.git <your-skills-dir>/yotta-compliance
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-compliance`, click **Code → Download ZIP**, unzip it, and
put the `yotta-compliance` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use
> GitHub and may fail without a proxy in China.

## Development and validation

```bash
# Contract tests (run inside the skill directory)
python3 scripts/test_yotta_compliance.py

# Rule-pack validation
python3 scripts/yotta_compliance.py rules validate --pack rules/pipl.json
python3 scripts/yotta_compliance.py rules validate --pack rules/data-export.json

# Syntax check
python3 -m py_compile scripts/yotta_compliance.py
```

Rule authoring guidance: [references/rule-authoring.md](references/rule-authoring.md).

## Boundaries and disclaimer

yotta-compliance provides deterministic rule-based review suggestions and an evidence chain. It does
not constitute legal advice, does not replace a lawyer or compliance adviser, and does not determine
contract validity, regulatory approval, or litigation outcomes. A rule hit describes observable
text, not the user's actual business conduct. A rule miss does not prove the absence of risk.
`mapping_only` frameworks must not be described as reviewed or certified. Use the tool only on
content you are authorized to process, and have qualified professionals make the final judgment.

## License

[MIT](./LICENSE) © YottaMeta. The YottaMeta family names and the `yotta-*` prefix are YottaMeta brand
identifiers; derived works must not reuse them, see [NOTICE](./NOTICE).
