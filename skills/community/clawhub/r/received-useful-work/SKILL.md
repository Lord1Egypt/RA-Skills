---
name: received-useful-work
description: Discover received public libraries and run caller-supplied inputs for x402 integration repair, tool input compatibility, and task distribution. scripts/task-distribution/cli.mjs classifies a supplied seller integration as free_sufficient or missing_field_not_paid_demand and sends no payment. scripts/dispatch.mjs qualifies compatibility-query for a tool input compatibility decision on the candidate envelope. A description match does not complete the task.
license: MIT
compatibility: Requires Node.js >=22.22.2, tar, and npm. Public reads are GET only, use the caller's timeout and body budget, and send no credential, signature, purchase, or note. No payment header is sent.
metadata:
  author: neomorphic
  version: "0.1.1"
  hermes:
    tags: [discovery, library, no-spend]
  openclaw:
    requires:
      bins:
        - node
        - tar
        - npm
    homepage: https://neomorphic.io/.well-known/skills/received-useful-work/SKILL.md
---

# Received useful work

Use this to discover received libraries and verify their shipped contracts. The executable is `scripts/dispatch.mjs`. Its default execution mode is `contract_replay`: it runs fixed examples and negative controls. A caller label does not replace those example inputs. Caller mode is the same executable. It passes the caller's supplied inputs to the received library command. The input contract is `references/caller-input-contract.json`.

## Execution contract

This is the authority a visitor needs before install. The registry metadata above declares the binaries. ClawHub has no allowed-tools field and this skill does not invent one. It also does not create a sandbox. The limits below are what the commands actually enforce.

Runtime is Node.js `>=22.22.2`. Required binaries are `node`, `tar`, and `npm`. Owned children are only `node` running a hash-pinned library CLI, `tar -xzf` extracting a hash-pinned public archive, and, for compatibility-query, `npm ci --ignore-scripts --no-audit --no-fund`. Contract replay always runs that npm command. Caller mode runs it only when the extracted tree has no `node_modules`. npm is pinned to `https://registry.npmjs.org`. Child `LANG` and `LC_ALL` are `C`.

Public acquisition is GET only, with no body, credential, signature, purchase, or note. The origins are:

- `https://neomorphic.io` under `/downloads/`, for library delivery and the seller-repair descriptor and archive
- `https://agents.samedaydesk.com` under `/.well-known/useful-result-reuse/`, for the grantless retained discover and retained read
- `https://registry.npmjs.org`, for the compatibility-query install from the pinned lockfile

A loopback HTTP origin is accepted only when a local pin substitutes it for the retained read. Any other origin, and any URL with a username, password, or fragment, is refused before a connection. Caller task text, caller authority, and caller notes are not fields of those requests. `export-result --note` stores a caller-asserted note in the local log. It is not sent.

Hashes and byte lengths live in `references/pins.json` and `references/library-delivery.json`. A mismatched archive is a tampered-archive refusal. It is not executed.

Caller inputs are the request file and the flags the command documents. A missing real input returns `missing_input` and a next action. It does not load a bundled example. A changed task, a changed quota observation, or a reused stale authority is a refusal. It is not a payment demand.

Output scope is the caller directory. `scripts/dispatch.mjs` writes the acquired tree, the child home, and the child temp under `--work`, and writes events only to `--log`. `scripts/task-distribution/cli.mjs` execute writes only under `--work`, and a referral only to `--out`. `scripts/library-delivery.mjs` acquire writes only under `--work`. The caller home directory and the system temp directory are not outputs. Child processes do not inherit `HOME`, npm tokens, proxy variables, or the rest of the shell environment.

The default path is free. `--pay`, `--settle`, and `--sign` are refused. `budget.pay` true is refused. A paid intent is refused before source access. Nothing on this path purchases, signs, or reserves funds. The maintained-observation replay increments the pinned projection's `sellers_30d` value so the library can report a change. That is not a seller ranking and not a payment.

Discover the same command this file installs:

`node scripts/dispatch.mjs discover --public-root PUBLIC`

Qualify one request. Exit 0 classifies a match, a useful refusal, no-fit, or coverage that is still unknown. Exit 3 rejects reuse of an authority whose owner, input, version, or expiry does not match. Exit 2 rejects `--pay` and a tampered archive.

`node scripts/dispatch.mjs qualify --request references/requests/walletless-trial.json --public-root PUBLIC`

Replay the matched library's fixed contract from exact public bytes. The work directory is caller-owned. A successful replay is not evidence that the caller's separate task was solved.

`node scripts/dispatch.mjs run --request references/requests/walletless-trial.json --public-root PUBLIC --work WORK --log events.jsonl`

Run caller mode when the request says `executionMode` `caller`, or pass `--mode caller` when that request agrees. A missing real input returns `missing_input` and a next action. It does not load a bundled example, a fixed date, a fixed network, or a fixed task.

`node scripts/dispatch.mjs run --mode caller --request REQUEST --public-root PUBLIC --work WORK --log events.jsonl`

`export-output` binds the exact admitted request. Pass `--attempt` when more than one success matches. A task id alone is not a selector. `useful`, settlement, and later use stay null. A caller `executionSucceeded` flag is not promoted. `export-result` remains the only caller-asserted usefulness feedback. The export is this log's schema, not an external execution witness.

`node scripts/dispatch.mjs export-output --log events.jsonl --request REQUEST`

The native provider route is `/.well-known/skills/received-useful-work/SKILL.md`. The installed command is `scripts/dispatch.mjs`. Request and observation identity use `scripts/delivery-contracts/contracts.mjs`. Provider routes in the pins are the existing machine-entry documents, not new services.

`budget.timeoutMs` is one absolute deadline. It starts before acquisition and covers body reads, extraction, dependencies, and every child. `budget.outputBytes` is one cumulative stdout+stderr budget for that same operation, shared by acquisition, setup, probes, and every owned child. An overrun stops later owned children. A timeout, flooded stream, signal, parse failure, or missing output is a failed execution. It is not a useful refusal. Downloads, setup, exit 0, and HTTP 200 do not decide usefulness. The caller records that with `export-result`.

The pinned tasks are `crt-100198-capability-preflight-reuse`, `grantless-retained-read`, `caller-owned-no-spend-composition`, `hold-sellers`, and `current-compatibility-query`. This command already serves those five. It does not add a retained-read catalog. Customer execution stays unknown until `export-result`.

Install the same command through the enrolled Hermes receiver. Record that exact runtime. Do not describe the enrolled release as the newest Hermes.

A missing `standard402` field, or a declaration by itself, does not create a paid need. The accepted-derivative package is not marked received here.

## Current reusable delivery

`scripts/library-delivery.mjs discover` reads the four current library pins in
`references/library-delivery.json`. Acquire one exact library and its declared
dependencies into a fresh caller directory:

`node scripts/library-delivery.mjs acquire --library task-economics-delivery --work CALLER-WORK`

Use `maintained-useful-delivery` or `task-distribution` as appropriate. Local QA
can explicitly supply `--public-root PUBLIC`; it is recorded as local receiving.
The command returns the acquired entrypoint and dependency roots. Run it with
your own task and inputs. Source qualification, repair compatibility, maintained
permission and payment are separate checks; unsupported composition stays unknown.
Candidate acquisition and QA do not establish hosting, outside usefulness or settlement.

For scoped CRT sharing or retained compatibility, acquire `evidence-referral-consumer`.
Run the returned `bin/referral.mjs` command with caller-owned `--config` and
`--request` files; its acquired README defines the complete task contract.
CRT `--allow-qa yes` requires a disposable owning authority and grants no
production enrollment. Receive/reuse reads current permission and exact artifact
bytes again, including correction or withdrawal after execution. The optional
referral records caller-asserted usefulness; it carries no payment or execution
authority. Seller task referrals use the separate command below.

The task-specific repair extension uses the owning seller descriptor and exact
MIT bytes. Root336 owns that separate publication; an unavailable seller stays
a source refusal. Supply your complete task according to
`references/taREDACTED-SECRET.json`:

`node scripts/task-distribution/cli.mjs run --request MY-TASK.json --execute yes --work CALLER-WORK --share yes --out REFERRAL.json`

Sharing retains a 24-hour command reference. A later caller rechecks source,
terms, task scope and expiry and executes with its own consent:

`node scripts/task-distribution/cli.mjs reuse --request LATER-TASK.json --packet REFERRAL.json --execute yes --work CALLER-WORK`

One deadline and cumulative input/source and output allowances begin before raw
caller intake and cover the owned children. A failed or uncertain packet write
is refused; preserve its file for exact review and use a fresh output path.

## Caller tasks named in the description

The three phrases are contiguous because that is how skill search matches a whole query. A match is not evidence the task ran.

`x402 integration repair` and `task distribution` use `scripts/task-distribution/cli.mjs`. The caller supplies the request. A health observation that already matches classifies as `free_sufficient`. A changed quota observation that lacks `quota.remaining` classifies as `missing_field_not_paid_demand`. Both keep the wrapper `paymentSent` false and `useful` null. The health classification can still set `useful` true with reason `observed_output_sufficient_declaration_incomplete`. The quota classification sets `useful` false. The seller client can exit 0 for that negative. `decision` `accepted` means the supplied request ran. It does not mean the repair is complete or that a payment is due. The received seller is 0.4.1. Its x402 pin is provenance and is not vendored. This command does not implement a new repair and does not spend. The separate scoped-repair-commerce 0.1.2 download is not this command.

`tool input compatibility` uses `scripts/dispatch.mjs` to qualify `compatibility-query`. The pinned output is a compatibility decision for the candidate envelope. Hosted acquisition of that envelope stays unverified. Import is refused.

## Bundle files the installer must fetch

Official URL install copies files this document names under `scripts/` and `references/`. These are the index files besides this document and `LICENSE`:

`references/LICENSE.txt`

`references/pins.json`
`references/caller-input-contract.json`
`references/requests/walletless-trial.json`
`references/requests/grantless-retained-read.json`
`references/requests/no-spend-composition.json`
`references/requests/maintained-observation.json`
`references/requests/compatibility-query.json`
`references/requests/seeded-stale-authority.json`
`scripts/dispatch.mjs`
`scripts/delivery-contracts/contracts.mjs`
`references/library-delivery.json`
`scripts/library-delivery.mjs`
`references/taREDACTED-SECRET.json`
`references/taREDACTED-SECRET.txt`
`scripts/task-distribution/cli.mjs`
`scripts/task-distribution/distribution.mjs`
`scripts/task-distribution/archive.mjs`
`scripts/task-distribution/source.mjs`
`scripts/task-distribution/delivery-contracts/contracts.mjs`
`scripts/task-distribution/delivery-contracts/durable.mjs`
`scripts/task-distribution/delivery-contracts/LICENSE`
