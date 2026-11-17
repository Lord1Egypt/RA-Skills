# Acceptance

Walk every line before calling the pipeline done. Report each with its evidence: a command output,
a run link, or a pull request link. A line that could not be checked is reported as unchecked, not
as passed.

## Configuration

- `DOMAIN` in `infra/agents/web-scribe.prompt.ts` is the company's own domain, `PAGES` are the
  site's real sections, and `COMPETITORS` names the competitors worth watching with their pricing
  and changelog URLs, 20 URLs at most in all.
- `node --import tsx evals/contract.mjs` passes, run from the skill folder.

## Template and compiled graph

- `cargo-ai project check` prints `agent:web_scribe` bound to `<repo>#<branch>` at the repository root.
- `cargo-ai project plan` shows one agent, two bound connectors, one folder, and no model.

## First run

- One pull request, unmerged, titled `[web-capture] first run`, carrying
  `cadence/log/raw/web/pages/*.md`, `cadence/log/raw/web/competitors/*/*.md` and
  `cadence/log/raw/web/news/<date>.json`.
- Each page file is the full page the extract returned, written by the `node -e` line, not a
  summary; the run's output shows the "wrote" lines and any "not read" pages.
- The news file holds items naming the company and its competitors, each with a URL.
- Every domain that was empty is seeded; no existing file changed.
- Every factual sentence carries `[R: <url>]`, `[I: ...]` or `[TR: ...]`.
- `icp/` names at least one disqualifier and says the CRM verifies it later.
- Every `client/` file carries `reference_permission: unknown`; every `proof/` file cites its
  `client/` file and its URL.
- No `persona/` or `jtbd/` file was written.

## A later week

- With a change: one pull request adding `insight/<date>-web.md`, one tagged line per finding,
  each naming its company, new `client/` or `alternative/` files only for newly named customers or
  competitors, and any edit to an existing file proposed in the body, not made.
- A page whose text did not change on the site shows no diff.
- With nothing worth writing: no pull request.
- The news window started at the date of the last merged commit under `cadence/log/raw/web/`.
