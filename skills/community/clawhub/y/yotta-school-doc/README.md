<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-school-doc banner" width="100%" />
</p>

<h1 align="center">yotta-school-doc · 元公 (YuanGong)</h1>

<p align="center">YottaMeta's <b>deterministic drafting-skeleton and validation skill for school documents</b>:
turn a versioned document-type rule pack and a structured facts file into a reproducible skeleton, then
check an existing draft for missing fields, date issues, attachment mismatches, placeholders, student
personal data, overclaims, sensitive wording and incomplete meeting action items.</p>
<p align="center">Pure Python 3.8+ standard library, zero dependencies; local-only — no network, no model
calls, no upload, no fabricated facts.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-school-doc"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-school-doc" /></a>
</p>

## Why

School documents are repetitive, but they are also high-stakes: wrong dates, missing attachments,
unfilled placeholders or student personal data can become real problems. Generic writing assistants
optimize for fluent prose. 元公 optimizes for a smaller, verifiable job:

- make missing facts visible as `〔待补〕`;
- make structural gaps reproducible and reviewable;
- keep school drafts and context on the local machine.

## Features

- Eight built-in document types: notice, parents letter, request, report, work summary,
  meeting minutes, work plan and briefing.
- `draft`: turn structured facts into a Markdown or JSON skeleton.
- `check`: validate an existing draft with evidence lines.
- `types`: list, show and validate built-in or custom rule packs.
- `--gate findings=n`: fail CI when the number of findings reaches a threshold.
- Zero-dependency Python 3.8+ standard library. No network access, no model calls.

## Quick Start

```bash
python3 scripts/yotta_school_doc.py template --output-dir ./school-doc-template
python3 scripts/yotta_school_doc.py draft --type notice --facts facts.json
python3 scripts/yotta_school_doc.py check --doc notice.md --type notice --facts facts.json --gate findings=1
python3 scripts/yotta_school_doc.py types list
```

Exit codes: `0` normal, `1` gate triggered, `2` input error, `3` rule-pack or document-type error,
`4` runtime error.

## Inputs

The facts file is a JSON object:

```json
{
  "schema_version": "1.0",
  "doc_type": "notice",
  "visibility": "public",
  "title": "关于开展秋季运动会的通知",
  "issuer": "示例中学",
  "published_date": "2026-09-24",
  "audience": "各年级组、各班级",
  "action_deadline": "2026-09-30",
  "contact": "教务处（010-00000000）",
  "body_points": ["运动会时间与地点", "报名办法", "安全工作要求"],
  "attachments": ["报名表.xlsx"]
}
```

Dates may be written as `YYYY-MM-DD` or `YYYY年M月D日`. The engine normalizes them internally.
Missing facts become `〔待补〕` and are reported as findings.

## Checks

`check` reports deterministic findings such as `field_missing`, `section_missing`,
`date_format_invalid`, `date_order_invalid`, `fact_date_mismatch`, `attachment_missing`,
`attachment_unknown`, `placeholder_present`, `privacy_risk`, `action_item_incomplete`,
`sensitive_term_review` and `overclaim_review`.

Every finding includes a severity, a suggestion and an evidence object with a line number and quote when applicable.

## Privacy and Boundaries

- No network access and no model calls.
- School drafts and context remain local.
- Personal-information checks are rule-based review prompts, not identity decisions.
- No standard text, real school template or case document is bundled.
- The output is drafting assistance and risk prompting. It is not a legal, compliance, inspection or
  ideological-review conclusion. Final issuance remains the school's responsibility.

## Installation

### Option 1: npx one-liner (recommended)

```bash
npx -y @yottameta/yotta-school-doc --agent <agent-name>
npx -y @yottameta/yotta-school-doc --dir <your-skills-dir>
```

### Option 2: git clone

```bash
git clone https://github.com/YottaMeta/yotta-school-doc.git <your-skills-dir>/yotta-school-doc
```

### Option 3: Download ZIP

Download ZIP from GitHub and extract it into your agent's skills directory.

### Option 4: install.sh

```bash
bash install.sh --list
bash install.sh --agent <agent-name>
bash install.sh --dir <your-skills-dir>
```

## Development

```bash
python3 scripts/test_yotta_school_doc.py
```

The engine is a single standard-library Python file: `scripts/yotta_school_doc.py`.

## License

MIT
