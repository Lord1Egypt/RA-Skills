---
name: publish-safe-prs
description: Prepare, sanitize, publish, and verify public GitHub issues, pull requests, review comments, release notes, bug reports, logs, screenshots, and test evidence. Use whenever an agent converts a private incident into an upstream reproduction, drafts or posts to a public repository, edits an exposed contribution, or needs a privacy and secret preflight before an external GitHub write.
license: MIT
metadata:
  author: JUMP UNDER
  version: "1.0.0"
---

# Publish Safe PRs

Public contribution is a one-way boundary. Preserve the technical fact. Leave
the private story behind.

## Permission Boundary

- Drafting and local inspection are reversible.
- Publishing, commenting, pushing, opening a PR, uploading an artifact, and
  editing an existing public contribution are external actions.
- Require explicit user authorization before the first external write.
- Approval to report a bug does not authorize disclosure of the user's
  project, employer, collaborators, clients, infrastructure, conversations, or
  credentials.
- Never publish a secret, even when it is expired, revoked, or partially
  redacted.

The skill may read the candidate contribution and user-supplied deny terms. It
must not search unrelated private files merely to make the deny list broader.

## Workflow

### 1. Inspect the destination

Confirm the repository, visibility, contribution rules, issue templates, and
target branch. Search for an existing issue or PR with the same failure mode.
Add evidence to the canonical report when that is more useful than a duplicate.

### 2. Build a private fact map

Separate the evidence before writing:

- **Public technical facts:** released versions, public source paths, public API
  behavior, generic exceptions, and reproducible state transitions.
- **Private facts:** names, usernames, email addresses, account and channel IDs,
  local paths, hostnames, IPs, tokens, organizations, projects, clients,
  conversations, unreleased work, and operational history.

Create a local deny-term list from private proper nouns and distinctive
phrases. Keep the list private. Do not paste it into the contribution.

### 3. Write a synthetic reproduction

Preserve causality, not autobiography.

| Private source | Public replacement |
|---|---|
| Person or agent name | `User` or `Agent A` |
| Project, product, or client | `Project A` |
| Partner or venue | `external partner` |
| Account or channel | `direct-message session` |
| Local path | `<workspace>/path` or omit it |
| ID or dedupe key | `example-id-001` |
| Private URL | `https://example.invalid/path` |
| Exact private timestamp | relative ordering such as `before restart` |
| Conversation quote | synthetic paraphrase preserving the failure |

Do not publish a redacted transcript when a synthetic example proves the same
behavior. A unique combination of harmless details can still identify the
source.

### 4. Audit every evidence surface

Review more than the prose:

- title, body, comments, commit messages, branch names, and patch;
- test names, fixtures, snapshots, payloads, and generated files;
- logs, traces, terminal prompts, shell history, and environment output;
- screenshots, browser chrome, tabs, notifications, filenames, and metadata;
- links, gists, videos, CI artifacts, and image alt text;
- Git author name and email.

Remove irrelevant evidence. Replace necessary identifiers with obviously
synthetic values.

### 5. Run deterministic preflight

```sh
python3 scripts/publication_preflight.py \
  --deny-term "Private Project" \
  --deny-term "Distinctive Partner" \
  draft.md
```

For a longer private list:

```sh
python3 scripts/publication_preflight.py \
  --deny-file private-deny-terms.txt \
  draft.md
```

Exit codes:

- `0`: no configured pattern matched;
- `1`: likely private material found;
- `2`: the scan could not complete.

A passing scan is necessary, not decisive. Read the final draft as a public
artifact after the scanner passes.

### 6. Publish and verify

After explicit authorization, publish through the intended identity. Fetch the
public artifact immediately and verify:

- repository, issue or PR, author, and target are correct;
- the remote body matches the approved draft;
- no denied term, secret pattern, private path, identifier, or attachment
  escaped;
- the sanitized reproduction remains technically coherent.

Run the preflight against the fetched public body. Report the public URL.

## Pull Request Standard

- Keep the patch confined to the upstream defect.
- Use synthetic fixtures and generic test names.
- Explain the failure mode, root cause, behavioral change, tests, and residual
  risk without narrating the private incident.
- Link only public sources.
- Inspect commit and branch metadata before pushing.

## Exposure Response

If private information reaches a public surface:

1. Stop further publication and state exactly what escaped.
2. With authorization, delete the exposed artifact where possible and publish
   a sanitized replacement. Editing may preserve history and notifications.
3. Rotate any exposed credential through its owning provider.
4. Fetch the old URL to confirm its current state and rescan the replacement.
5. State what cannot be recalled, including notifications, forks, caches,
   clones, and third-party indexes.

Never claim complete erasure from the internet.

## Release Gate

Before any public write, require every answer to be yes:

- Is publication explicitly authorized?
- Is every real-world proper noun necessary and already public?
- Is the example synthetic wherever real context is unnecessary?
- Were deny terms assembled from the source material?
- Did deterministic preflight pass?
- Were code, metadata, logs, images, attachments, and links reviewed?
- Does the sanitized evidence still reproduce the technical claim?
- Will the published artifact be fetched and rescanned?
