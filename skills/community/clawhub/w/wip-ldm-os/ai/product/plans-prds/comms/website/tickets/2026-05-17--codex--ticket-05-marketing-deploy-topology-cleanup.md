# Ticket 05: Marketing deploy topology cleanup

**Date:** 2026-05-17
**Filed by:** Codex, with Parker
**Status:** open. Post-launch cleanup. Do not block homepage V1 or Speedrun submission.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Depends on:** Homepage V1 deployed and Ticket 02 launch path resolved.

## Summary

The V1 homepage deploy is intentionally using a homepage-scoped production copy because the current marketing deploy topology is not safe for a full mirror. That is an emergency launch exception, not the desired steady state.

The current production source is now documented as:

```text
repos/wip-web/wip-computer-website/static/wip-websites-private/
```

That repo's `deploy.sh` path can run a full `rsync --delete` mirror of `wip.computer/`. During the V1 launch review, the deployer found that live production has subpage content that is not present in `origin/main`. A full mirror from the current repo state would delete or overwrite live subpages. Parker's launch rule is therefore: "don't delete the sub pages, just that home page."

The website migration lanes are:

| Lane | Path | Meaning |
|---|---|---|
| Static production | `repos/wip-web/wip-computer-website/static/wip-websites-private/` | Current live website source. |
| Dev | `repos/wip-web/wip-computer-website/dev/` | Static-to-app staging lane for shared site shell work. |
| Next.js | `repos/wip-web/wip-computer-website/next-js/wip-web-private/` | Future full Next.js WIP website app. |

## Problem

This is not how deploy should work. A deployer should not have to choose between shipping the homepage and risking live subpage deletion.

Known drift found during the V1 deploy review:

- `listen/` has live production files that are not represented in the repo checkout used for deploy.
- Several live surprise pages exist on production but not in `origin/main`.
- `install/wip-ldm-os.txt` is newer on production than in the repo checkout used for deploy.
- A full mirror from the repo checkout could introduce unrelated content that is not currently live.
- `dev.wip.computer` is not currently a working marketing-site preview vhost, so `deploy.sh --dev` is not a meaningful preview gate for the homepage.

## V1 rule

Do not fix this before the Speedrun launch. For V1, deploy only the nine homepage files from `wip-websites-private` PR #48:

- `wip.computer/index.html`
- `wip.computer/styles.css`
- `wip.computer/components.jsx`
- `wip.computer/assets/wip-logo.png`
- `wip.computer/assets/bucky-patent-1.gif`
- `wip.computer/assets/bucky-patent-2.gif`
- `wip.computer/assets/bucky-patent-3.gif`
- `wip.computer/assets/bucky-patent-4.gif`
- `wip.computer/assets/bucky-patent-5.gif`

No `--delete` for the V1 homepage push. Verify production immediately after the push.

## Post-launch work

After submission, make marketing deploy boring again.

Required outcomes:

- Reconcile production live content against `wip-websites-private` so the repo and server are intentionally aligned.
- Decide where `listen/`, surprise pages, install text, and generated microsites are owned.
- Make `deploy.sh --dev` point at a real marketing-site preview vhost, or remove it from the launch checklist until it exists.
- Define whether local `wip-computer-website/dev/` publishes to `dev.wip.computer`, or whether it remains a local staging lane only.
- Add a preflight that lists file-level deletes and overwrites before any `rsync --delete` production run.
- Add a documented homepage-scoped deploy mode if partial deploys remain part of the workflow.
- Document the rollback path for homepage-only deploys.

## Acceptance criteria

- A deployer can run the documented deploy path without risking unrelated live subpages.
- `origin/main` versus production drift is either eliminated or explicitly documented by owned content class.
- `dev.wip.computer` either previews the marketing site or the docs no longer claim it does.
- Full-site deploy, homepage-only deploy, and rollback are each documented with exact commands.
- The V1 emergency exception is no longer needed for routine deploys.

## Out of scope

- Homepage V2 static hardening. That is Ticket 04.
- Login/demo fixes. That is Ticket 02.
- Rebuilding the marketing site in a framework.
- Moving Kaleidoscope app logic into the website repo.
- Changing homepage design or copy.
