# trim campaign mode

Adapted from OpenClaw's `test-audit/CAMPAIGN.md`, MIT License; see [openclaw-LICENSE](openclaw-LICENSE).

Campaign mode prunes one subsystem's whole test surface in one pass: a plugin, a package, or one core area. The value bar, retention bar, candidate evidence, and validation in [SKILL.md](../SKILL.md) apply to every lane. This file adds the order of work. Each step ends on its completion criterion; do not start the next step early.

The worked example throughout is OpenClaw's Telegram campaign (openclaw/openclaw#155040: +15,424 / -64,067 lines across 280 files), which this procedure was extracted from.

## 1. Baseline

Record the subsystem's test and support line counts and every test file's pass/fail state at a pinned default-branch SHA. Keep baseline failures in their own list. In the Telegram campaign, all three baseline failures were real delivery bugs, not stale tests.

Done when every in-scope test file has a recorded baseline result.

## 2. Lanes and inventory

Split the surface into **lanes** along production owner boundaries, not file prefixes. Telegram used accounts, commands, context, dispatch, inbound, outbound, persistence, transport, shared, harness, and live/QA scenarios. Include the subsystem's cases at shared core boundaries and its QA and live-proof harness tests.

Done when every test file and QA scenario the subsystem owns belongs to exactly one lane.

## 3. Read-only ledger per lane

Give each lane to its own read-only agent ([stations](../../stations/SKILL.md), or `brigade run` seats in a Brigade-wired repo). The agent reads every assigned test in full, including parameter tables, plus the production owners, their entry points, callers, history, and CI routing. Each test declaration goes into a written **ledger** with one mark. A parameterized test (`it.each`, `pytest.mark.parametrize`) is one declaration unless its rows need different marks; then mark each row.

- `R`: retain, naming the contract and the bug it catches. A retained test that only moves to a better-named file stays `R` with the move noted.
- `F`: retain the contract but repair the assertion, such as a vacuous negative that passes when only one of several items is missing.
- `C`: consolidate, naming the owner that absorbs the assertion first: a sibling table case, a stronger boundary suite, or the shared owner in another package.
- `D`: delete, naming the proof that remains, or why no contract exists.

Judge a test by its assertions, not its name. One Telegram test named for retiring a progress window asserted the window was *not* cleared.

Done when every declaration in the lane has a mark and an evidence line.

## 4. Layer plan per lane

The per-test ledger is input, not the edit list. A second read-only pass, starting from the ledger, looks for the redundant **layer**. In Telegram, several dispatch suites replayed the same shared compositor through one mocked preview, around stronger real-stream and HTTP-fixture suites. Name the **keeper** suite for each contract. Prefer the real transport boundary with a fake network over a mocked collaborator. Correct any ledger errors this pass finds.

Done when each lane plan names its retired files, its keeper per contract, the assertions to carry into keepers, and the test-only production seams unlocked.

## 5. Cutover

Edit lane by lane. Serialize changes to shared harnesses and support files through one owner. With each lane, remove the test-only production seams it unlocks: injection parameters, getters, reset exports, and indirection layers. Register moved suites in CI routing and test inventories. Update any shrink-only line-cap baselines. Unless repo policy says otherwise, put durable test-ownership rules in the subsystem's `AGENTS.md`, drawn only from mistakes this campaign actually found.

Done when every lane plan is applied and each lane's keepers pass.

## 6. Preservation review

Before claiming completion, have independent reviewers ([review](../../review/SKILL.md), one per boundary group) compare deleted coverage against the keepers. They look for contracts that lost their only proof, and for new assertions that cannot fail, such as a rejection row the production code never reaches. The Telegram review found nine real gaps and one unreachable assertion.

For each restored contract and every `C` or `D` row, make one deliberate **mutation** of the production owner and confirm the named keeper goes red. Then restore the source byte for byte.

Done when every reported gap is restored or rejected with source evidence, and every restored contract has a caught mutation.

## 7. Product defects

A baseline failure that survives into a keeper is a bug report. Fix it at its owner as a separate commit ([refire](../../refire/SKILL.md), then [taste](../../taste/SKILL.md)), and prove it through the real user flow, with a **control** run that reverts the fix and shows the old behavior. Record unrelated product discrepancies as follow-ups instead of fixing them in the campaign.

Done when each repaired defect has a failing control and a passing candidate on the same harness.

## 8. Reconcile and hand off

Campaigns outlive many default-branch commits. Unless repo policy says otherwise, merge the default branch rather than rebasing a long campaign. When the default branch modified a file the campaign deleted, keep the deletion, port the new contract into the keeper, and confirm every new regression it added still has a home. Rerun the whole subsystem suite and repeat live proof on the merged head.

Review tooling may show a truncated file list on a diff this large. Record maintainer decisions for compatibility flags in the PR evidence rather than editing gates.

Hand off with the SKILL.md output shape, plus:

- baseline and final test/support line counts, with production counted separately;
- lanes, retired layers, and keepers;
- preservation gaps found and their mutations;
- product defects with control and candidate proof.
