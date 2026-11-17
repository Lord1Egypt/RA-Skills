# Acceptance

Walk every line. A checked template without an evidence-backed consumer adaptation is incomplete.

## Before deploy

- `node --import tsx evals/contract.mjs` passes against the adapted graph: `linkedin_posts` capped,
  "Past week", scheduled; `surfaced_posts` holds no person; the only LinkedIn action is
  `searchPostComments`; `postMessage` with `channelId` locked; context read-only; one cron.
- `searchKeywords` was derived from the workspace context, and one manual `searchPosts` with the same
  keywords returned posts a buyer wrote, read out loud before keeping them.
- The live per-post and per-comment prices were read and said out loud, and `limit` was chosen
  against them.
- `channelId` is internal, read from the Slack connector's autocomplete, with the bot in it.

## First runs

Keep the Slack permalink, the ledger rows and the run transcript as evidence.

- **Sync.** The first sync landed no more than `limit` rows, all posted in the past week.
- **Digest.** One post in the `references/digest.md` shape. Every pick cites a context line and links
  its post; every engager quote exists on that post.
- **Ledger.** One row per pick plus `digest-<date>`; no column holds a person.
- **Re-run.** Sending the trigger text again the same day posts nothing and reads no comments.
- **Next week.** A post picked last week and still in the search is not picked again.
- **Quiet week.** With keywords that return nothing relevant, the digest says "Quiet week" once and
  still carries the Searched line.

## Isolation

- This is one root skill. Its supporting Markdown lives under `references/`, and no nested
  `SKILL.md` exists.
- No import leaves the folder.
- The transcript shows no LinkedIn call other than `searchPostComments`, and only on picked posts.
