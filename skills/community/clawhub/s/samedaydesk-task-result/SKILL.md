---
name: samedaydesk-task-result
description: Acquire the published samedaydesk-caller-result 0.1.1 archive and retain a caller-supplied tool result, recovery checkpoint, or optional feedback statement. Use when a delivered MCP or HTTP result is already in hand and the caller wants the exact released client, including loss recovery and an optional free statement. Missing files return the next action.
license: MIT
compatibility: Requires Node.js 22 and npm. Public reads are anonymous GETs of the pinned descriptor and archive. The command does not create a payment, sign, or settle.
metadata:
  author: neomorphic
  version: "0.1.0"
  hermes:
    tags: [samedaydesk, caller-result, no-spend]
  openclaw:
    requires:
      bins:
        - node
        - tar
        - npm
---

# SameDayDesk task result

Install this skill, then acquire the already released caller and point it at caller-owned files. The executable is `scripts/task-result.mjs`. The byte pins are `references/caller-pin.json`. This skill's license is `references/LICENSE.txt`. The caller archive carries its own MIT license.

## Next action

Acquire the pinned 0.1.1 caller into a new directory:

`node scripts/task-result.mjs acquire --work DIR`

`DIR` must be a new directory. Add `--install yes` to run `npm ci --ignore-scripts --no-audit --no-fund` inside the extracted caller. That installs the locked dependencies from `https://registry.npmjs.org`. It is not an npm publication of `samedaydesk-caller-result`.

Retain a caller-owned result file without changing its bytes:

`node scripts/task-result.mjs retain --result RESULT.json --out COPY.json`

Recover with the caller's existing operation, checkpoint, and grant files:

`node scripts/task-result.mjs recover --caller DIR/caller --action start --operation operation.json --checkpoint checkpoint.json --grant grant.json`

Resume a lost result with:

`node scripts/task-result.mjs recover --caller DIR/caller --action resume --checkpoint checkpoint.json --grant grant.json`

Optional feedback uses the acquired client. For MCP, pass the caller endpoint and the retained result:

`node scripts/task-result.mjs feedback --caller DIR/caller --channel mcp --endpoint ENDPOINT --result RESULT.json --disposition useful`

HTTP stays unsent until `--send yes`. The acquired client posts only to an https origin and the exact free feedback path. `http://127.0.0.1` stays an untrusted origin and is not posted.

A missing result, operation, grant, disposition, or token returns `missing_input` and the next action. The command leaves bundled examples unused.

## What the command keeps

The direct data route is `@modelcontextprotocol/sdk` 1.30. The retained result is the full tool result, including `structuredContent`, `isError`, null, zero, and absent keys. `@x402/mcp` 2.16 is an optional projection and is not this archive. `bin/recover-mcp.mjs` prints a projection; this command also keeps the checkpoint result.

Tool refusal, transport failure, recovery pending, a restored result, and a caller-asserted acceptance stay separate. Usefulness stays `unknown`. The command creates no payment and permits no new payment.

## Boundaries

Public acquisition uses `https://neomorphic.io` and the paths in `references/caller-pin.json`. `--public-root` accepts only `http://127.0.0.1:port` or `http://[::1]:port` and records local receiving. Redirects and other origins are refused. The work directory is the directory you pass. An existing output is left in place.

Payment, signing, wallet access, and settlement stay outside this skill. `--pay`, `--settle`, `--sign`, and `--wallet` stop before any request. Running this command does not select or prove a native model.
