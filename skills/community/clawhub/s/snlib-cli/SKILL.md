---
name: snlib-cli
description: Run Seongnam Library (snlib.go.kr) tasks from the command line. Use when you need login, book search, my-info (내 정보 조회)/loan status (대출 현황) checks, interlibrary loan (상호대차) request/status, hope-book (희망도서) request/list/detail, or basket (관심 도서함) queries.
metadata: { "openclaw": { "requires": { "bins": ["bash", "java", "clojure"], "env": ["SNLIB_USER", "SNLIB_PASSWORD"] } } }
---

# snlib-cli.sh

Use {baseDir}/scripts/snlib-cli.sh to initiate Seongnam Library Request from the CLI.

For more information, visits https://github.com/ruseel/snlib-cli

## Quick Start

```bash
# first-time login
SNLIB_USER="your-id" SNLIB_PASSWORD="your-password" {baseDir}/scripts/snlib-cli.sh login

# read-only checks
{baseDir}/scripts/snlib-cli.sh my-info
{baseDir}/scripts/snlib-cli.sh loan-status
{baseDir}/scripts/snlib-cli.sh search-books --keyword "제2차 세계대전 발췌본"
```

## Common Workflows

- Account/session (계정/세션): `login`, `my-info` (내 정보 조회)
- Discovery (도서 탐색): `search-books`, `basket` (관심 도서함)
- Status checks (현황 조회): `loan-status` (대출 현황), `interloan-status` (상호대차 현황), `hope-book-list`/`hope-book-detail` (희망도서 신청 내역/상세)
- Write: `interloan-request` (상호대차 신청), `hope-book-request` (희망도서 신청, `--request-edn` 단일 EDN 맵 사용)

Read `{baseDir}/references/commands.md` for command patterns and end-to-end flows.


## Safety Rules

- Start with read-only commands before any write action.
- In skills, pass credentials via `SNLIB_USER` and `SNLIB_PASSWORD` environment variables.
- Session data is stored under `~/.config/snlib-cli/`.

## Troubleshooting
If 3 hours passed, authentication can fail. then you can re-login.

## Technical Details 
On first execution, `clojure` downloads deps from Maven Central, including `io.github.ruseel/snlib-cli`.
