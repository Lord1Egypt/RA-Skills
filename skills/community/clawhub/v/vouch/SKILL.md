---
name: vouch
description: Independently verify a consequential claim before acting on it. Use when an answer, plan or tool result rests on a checkable fact (a price, balance, filing, score, sanctions or compliance status, security fact, on-chain value) and being wrong would cost money or trust, when an answer looks uncertain or came from one source, or when a result is incomplete. Splits the answer into claims, asks independently ranked Telegraph miners within a stated budget, and reports each claim as verified, contradicted or cannot verify, with the receipt and cost. Needs the telegraph MCP server.
version: 0.1.0
license: MIT
metadata:
  openclaw:
    requires:
      bins: ["node"]
      config: ["mcp.servers.telegraph"]
  hermes:
    tags: [verification, fact-check, telegraph, mcp, budget]
    category: research
---

# Vouch: independent claim verification through Telegraph

Vouch is a procedure, not a server. It uses the `telegraph` MCP server (`@telegraphprotocol/telegraph-protocol-mcp`, tested on 2.3.0) to ask independently ranked specialist miners whether a claim is true, then reports what could and could not be established. It never turns silence into confirmation.

## When to use it

Run it before you act on, or tell the user to rely on, a claim that is checkable, consequential and from a source you cannot vouch for (your own memory, a single web page, another agent, an earlier tool result). Typical triggers: "send funds because the balance is X", "the filing says Y", "gas is under 5 gwei", "this address is not sanctioned", "CVE-N has CVSS 9.8", "the final score was 5-3".

Do not use it for opinions, forecasts, private or local facts, or things the conversation already proves. If being wrong is cheap, ask the user whether a paid check is worth it.

## Tools

The Telegraph tools may carry a prefix depending on your runtime (for example `mcp_telegraph_telegraph_ask` in Hermes). Free: `telegraph_find_intents`, `telegraph_intent`, `telegraph_find_miners`, `telegraph_ranking`, `telegraph_account`, `telegraph_docs`. Paid (about $0.01 each): `telegraph_ask`, `telegraph_ask_miner`.

If no Telegraph tool is available, stop and say verification is unavailable, and point the user to the install docs (`docs/openclaw.md` or `docs/hermes.md` in the Vouch repo). Do not substitute a guess or an unrelated web search and call it verified.

The ledger helper sits beside this file: `node scripts/vouch.mjs ...` (run from this skill's folder, or use its absolute path). It keeps the spend tally, refuses over-cap asks, judges numeric tolerance and prints the report. If you cannot run shell commands, keep the same tally by hand in your reply.

## Budget (set by the user, never raised by you)

- Per claim: $0.05 by default. Per task: $0.25 by default. If the user states other numbers, use theirs. Never raise a cap yourself; if a claim needs more, say so and ask.
- One ask is normally $0.01. Failed asks are not billed. The first ask plus one recovery ask fit the default per-claim cap.
- The same limits should also be set in the MCP server so they hold even if you slip: `TELEGRAPH_MAX_ASK_USD`, `TELEGRAPH_DAILY_LIMIT_USD`, `TELEGRAPH_MAX_BUDGET_USDC` (see the install docs).
- Never call `telegraph_deposit`, never run `fund` or `withdraw`, never read the wallet file or print a key. Funding is the user's job, in their own terminal.

## Procedure

**0. Start the ledger.**
`node scripts/vouch.mjs init --task "<short name>" --claim-cap 0.05 --task-cap 0.25`
Then call `telegraph_account` (free). Confirm the network is the testnet you expect, that `escrow.spendable_usdc` covers the task cap, and that the server's own limits are at or below the user's caps. If escrow is short, stop and tell the user to top it up themselves.

**1. Extract claims.** Write each checkable fact as one atomic line with its entity, date or block, unit, and the tolerance that would make it right (for example "ETH gas below 5 gwei", "within 1%", "exact"). Register it:
`node scripts/vouch.mjs claim --id c1 --text "..." --tolerance "..."`
Rank by consequence and verify the ones the decision depends on first. Mark anything uncheckable (opinion, future event, private data) as cannot verify with the reason, without spending.

**2. Route.** Call `telegraph_find_intents` with two or three keywords from the claim, then `telegraph_intent` on the best match to read its exact `params` and `answer_fields`. `references/intent-map.md` lists usual claim-to-intent pairs. If no intent fits, the claim is cannot verify (no matching intent). Do not stretch an intent to fit.

**3. Pick the miner.** Call `telegraph_ranking` for that intent. Prefer miners with a proven score (above 0) at rank 1 to 3. Unproven miners (score 0) are weak evidence: use them only as the second opinion and say so. If the claim, or an earlier answer in this task, came from a Telegraph miner, ask a different miner. Never verify a value against the feed it came from.

**4. Ask within budget.** First `node scripts/vouch.mjs check --claim c1 --est 0.01`. If it prints REFUSED, stop and report that claim as cannot verify (budget). Otherwise call `telegraph_ask` with the exact `intent` and `params` and a one-line `question`. Ask neutrally: request the value, never "is it X?". Then record it:
`node scripts/vouch.mjs record --claim c1 --intent <INTENT> --miner <miner> --cost <cost_usd> --receipt <receipt_hash>`
Record failed or empty asks too, with cost 0 and no receipt.

**5. Judge the answer.** All of these must hold before you say verified or contradicted:
- Same entity: the teams, token, chain, address, filing or CVE in the answer match the claim, not just the question you sent. Miners can return a confident answer about something else.
- Same time: the date, block or `as_of` fits the claim. A live price cannot confirm last week's price. A date in the future makes any outcome answer invalid.
- Complete: every `field_status` you rely on is `ok`, and the value is not null, empty or an error string.
- Warnings: read `warnings`. "Sources returned conflicting information" on a field you rely on means the evidence disagrees with itself, so it is not verified: recover (step 6) or report cannot verify. Conflicts on unrelated fields do not block a verdict, but mention them.
- Receipt: a `receipt_hash` exists. No receipt, no verdict other than cannot verify.

Then compare to the claim. For numbers use `node scripts/vouch.mjs judge --claimed <v> --observed <v> --tol exact|abs:N|pct:N|lt|le|gt|ge` instead of doing the arithmetic yourself. For `lt` the claim is "the value is below <claimed>".

- Valid answer that matches the claim: **verified**.
- Valid answer that differs beyond tolerance: **contradicted** (state the observed value).
- Missing, partial, about a different entity or time, self-conflicting, refused or unreceipted: **cannot verify**, with the specific reason. A failed, empty or irrelevant answer is never confirmation, and it is not contradiction either.

**6. Recover once.** If the first answer was partial, errored, self-conflicting or about the wrong entity, ask one other ranked miner (`telegraph_ask_miner` with that miner's id or slug and the same intent and params), after `check`, and record it. If the two valid answers agree, say so. If they disagree, report cannot verify and show both values and miners: you have no tie-breaker, and you do not get a third ask without the user's say-so. Never loop.

**7. Close the claim.**
`node scripts/vouch.mjs verdict --claim c1 --verdict verified|contradicted|cannot_verify --observed "<value, miner>" --why "<reason>"`
The helper refuses verified or contradicted when no receipt is recorded for the claim.

**8. Report.** Run `node scripts/vouch.mjs report`, then answer the user in the shape of `references/answer-format.md`: one block per claim with the verdict, observed value, miner, cost and receipt, then total spend against the cap, and what that means for the decision. If a decision-critical claim is contradicted or cannot be verified, say the action should not proceed on that claim and ask. A receipt can be looked up at `https://devnode.telegraphprotocol.com/engine/v1/signal/<receipt_hash>`. It proves what was asked, answered and paid, not that the answer fits your claim. Step 5 is for that.

## Pitfalls

- Treating "no answer" as "fine". Silence, timeouts and nulls are cannot verify.
- Verifying against the source that made the claim.
- A correct-looking answer to the wrong question (wrong team, token, chain or date). Check the answer's own fields.
- Future events: a miner may return a plausible but invented result with every field marked ok. A future date is always cannot verify.
- Spending past the cap because the claim feels important. Stop and ask.
- Re-asking the same question for a "better" answer. Repeats within a minute return the same answer; a different miner is a second opinion, a repeat is not.
- The Telegraph devnode is a testnet: the payments are test USDC and the miners' answers are live, unaudited data. Say so when the claim concerns real money.

## What a good run leaves

A ledger with a receipt for every verified or contradicted claim, a total at or under the task cap, a stated reason on every cannot verify, and no unrecorded paid ask.
