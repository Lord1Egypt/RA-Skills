---
name: public-careers-board
description: "Fetch current public job openings from one supported company careers board and report coverage. The rows are job listings of the board's current public vacancies: title, location, and the board's job URL, with source and fetch time. Supply Acxiom Workday, LiveRamp Ashby, or Magnite Workday to scripts/cli.mjs. Magnite is read only after its official careers handoff confirms the declared Workday board. Role selection stays outside the fetch. A source failure is not an empty or complete board. No wallet, signup, API key, or payment."
license: MIT
compatibility: Requires Node.js >=22.22.2. Acxiom and LiveRamp use the pinned recipe endpoints. Magnite uses a separate declared source and the pinned normalizeWorkday function. One deadline, a raw byte cap, and manual redirects. The pinned recipe bytes stay unchanged. Sends no credential, signature, or purchase. Exclusive file creation and private snapshots use the Linux /proc/self/fd directory-descriptor route. Where that route is unavailable those operations are refused. A missing, unknown, or wrong board does not need that route.
metadata:
  author: neomorphic
  version: "0.1.3"
  hermes:
    tags: [careers, jobs, coverage, no-spend]
  openclaw:
    requires:
      bins:
        - node
---

# Public careers board

Use this when the caller asks for current public job openings from one supported company careers board and needs the source and coverage stated. The installed command is `scripts/cli.mjs`. A description match does not select this skill, does not run the task, and does not show that an agent chose it.

The default route is free and caller-owned. It does not require a wallet, signup, private API key, or task upload. It does not call `GET /data/careers-board`. That optional paid route is a separate product. Re-read its live challenge before any other executor considers it. Do not copy a price from this file. `--pay`, `--settle`, `--sign`, `--wallet`, and `--purchase` are refused before a source read.

## Caller input

Choose one supported board. Aliases are exact:

- Acxiom Workday: `acxiom`, `acxiomllc` (calls `fetchAcxiom`)
- LiveRamp Ashby: `liveramp`, `liveramp-inc`, `liverampashby`, `liveramp-ashby` (calls `fetchAshby`)
- Magnite Workday: `magnite`, `magnite-careers` (calls `fetchMagnite`)

A missing board returns `missing_input` and does not load a bundled company. An unknown board returns `unknown_board`. A `--source` that is not that board's supported reader returns `wrong_source`. LiveRamp's previous Workday endpoint is the wrong source for LiveRamp. Magnite accepts its declared jobs endpoint or the token `magnite-workday`. The generic `workday` token stays Acxiom's, and `https://api.smartrecruiters.com/v1/companies/Magnite/postings` is the wrong source for Magnite. No caller-supplied origin is fetched. Redirects are not followed.

The pinned recipe revision remains `7d01bfb09c530430933dec1f07c5c0b8517cffa8`.

Magnite checks three facts before any jobs POST. The careers host robots crawl delay must fit inside the one deadline, or the result is `not_fetched` and the careers page is not fetched. Every visible Search Jobs link on `https://www.magnite.com/careers/` must canonicalize to `https://osv-rubicon.wd5.myworkdayjobs.com/MagniteCareers`, or the result is `source_moved`. The Workday shell must name tenant `osv_rubicon` and site `MagniteCareers`. The hostname label `osv-rubicon` is not the tenant. A mismatch is `identity_mismatch`. A 3xx response from a declared URL is `not_fetched` with reason `unexpected_redirect`. The redirect is not followed. Those results have `emptyBoard` false and do not call the jobs endpoint. A Workday body with `total: 0` and no postings is an empty board for that source. The SmartRecruiters URL is a different source and is not that empty board. The jobs POST always uses the declared endpoint `https://osv-rubicon.wd5.myworkdayjobs.com/wday/cxs/osv_rubicon/MagniteCareers/jobs` and the body `{ appliedFacets: {}, limit: 20, offset, searchText: "" }`. `coverage.roleFilter` stays null. Row `fetchedAt` is the time immediately before that POST, after the crawl delay. A later page that says `total: 0` while it still lists new jobs is not the end of the board. At most four pages are read, then a past-end probe when the declared total is reached. A later page is not requested once that cap is hit. `/refreshFacet/` is never requested.

The default `--timeout-ms` is 15000. The retained Magnite robots file publishes `Crawl-delay: 10`. Pass `--timeout-ms 30000` when that delay plus the board read must fit. Role selection is a separate command and is not applied by `run`:

```sh
node scripts/predicates.mjs observation.json
```

The predicate command reads one regular file of at most 1048576 bytes. A symlink, directory, FIFO, or other non-regular input is refused before that body is allocated. Declared size above the cap and a stream that grows past the cap are both refused. A file that changes size during the read is refused rather than returned as a prefix. The pinned source and its pin file use the same regular-file, cap, and deadline boundary. One 15000 ms deadline covers those reads, and the timer is cleared before the process exits. `appliedPredicate` stays null. `employmentDecision` stays false. `semantic_role_family` and `department_inference` stay unknown.

```sh
node scripts/cli.mjs run --board BOARD
```

`--out PATH` writes the one result line for every classification and refusal. An existing path, a final symlink, a directory, or a path inside this skill is refused and left unchanged. A parent symlink is not followed, including a multi-level symlink into this skill and a symlinked invocation of this command. The parent is opened without following symlinks, then the new file is created exclusively with `O_NOFOLLOW` on that directory. If the parent identity changes before creation, the write is refused rather than followed. A check followed by an open is not universally race-proof. That parent walk and exclusive create use the Linux directory-descriptor route. Where the route is unavailable, the write is refused and no file is created. A new file in an outside regular directory is still written when the route is available. `--seed FILE` is an explicitly supplied control. The result says `seeded: true` and `sourceCoverage: supplied_seed`. A seed does not fill in a missing board. A seed `padTo` is a safe integer checked against the shared byte budget before any buffer is allocated.

`--timeout-ms` defaults to 15000 and must be 100 through 30000. That one deadline covers pin verification and the source read. When it fires, the command aborts and cancels the owned fetch. `--max-bytes` defaults to 1000000 and must be 1024 through 1048576. It is one budget for every response body in the observation, including later pages. Pinned recipe files are hash-checked under the same deadline and are not counted in that response budget. `--output-bytes` uses the same bounds and limits every result line. A line over that limit is a short `oversized_output` refusal and does not echo the caller input. A timeout, oversized body, or oversized result is a refusal, not an empty or complete board.

## Honest coverage

Exit 0 is a classified result: `missing_input`, `unknown_board`, `wrong_source`, or `observation`. An observation keeps the recipe's `rows` and `coverage`. `coverage.status` `source_failure` stays a source failure, with `emptyBoard` false and `complete` false. `partial` keeps the rows already read and stays partial. An empty board has top-level `emptyBoard` true and `complete` false. That includes recipe status `empty_board` and an Ashby `jobs` array that is empty (`coverage.emptyBoard` true), even when the recipe status is `complete_for_returned_listed_set`. A non-empty listed set stays complete. `useful` stays null. The caller decides usefulness.

Exit 2 refuses payment flags, a Node.js runtime below 22.22.2, a tampered recipe, an oversized or timed-out acquisition, an oversized result, a bad seed, or an ambiguous overwrite. The pinned recipe is `references/pins.json`. The command runs a private snapshot of those verified bytes and deletes it afterward, including when the run fails. Creating that snapshot uses the same Linux directory-descriptor route. Where the route is unavailable, the snapshot is refused and the pinned bytes are not imported through a path open. A hash mismatch is not executed. An unknown board or a wrong source returns before that snapshot is imported.

`recipe/boards.mjs` is the upstream file. Do not run it as the installed command. Its own CLI writes an evidence file and reads every board. This command reads only the board the caller named.

## 0.1.3

This version is the immutable successor of published 0.1.2. The description, recipe revision `7d01bfb09c530430933dec1f07c5c0b8517cffa8`, and source pins are unchanged. Installed reads refuse a declared size above the cap before the body is allocated, read through EOF or one byte past the cap, and refuse a size change during the read instead of returning a prefix. A file that fills the cap exactly is still returned whole. Exclusive file creation and private snapshots use the Linux `/proc/self/fd` directory-descriptor route and are refused where that route is unavailable. A missing, unknown, or wrong board does not need that route.

## Install

The enrolled native route, when the official Hermes receiver is present, is:

```sh
hermes skills install epistemedeus/x402-data-gateway-skills/skills/public-careers-board --yes
```

Run the command from the installed copy. It does not read a builder checkout or a credential environment. This document does not claim that the public index already lists the skill.

## Bundle files

`LICENSE`
`references/pins.json`
`references/source-notice.txt`
`recipe/LICENSE`
`recipe/PUBLIC-RECIPE.md`
`recipe/boards.mjs`
`recipe/boards.public.test.mjs`
`references/source-pins.json`
`sources/magnite.mjs`
`sources/predicates.mjs`
`scripts/cli.mjs`
`scripts/file-boundary.mjs`
`scripts/predicates.mjs`
