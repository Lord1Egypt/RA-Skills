# Why the checkpoints exist

## YouTube policy

- YouTube's channel monetization policies treat mass-produced, repetitive or
  template-driven content as "inauthentic content" and can remove monetization from the
  whole channel. Human review of each video, with real editorial changes, is what keeps a
  channel on the right side of this. https://support.google.com/youtube/answer/1311392
- Realistic altered or synthetic content (for example AI-generated people, voices or
  events that look real) must be disclosed. The upload script exposes this as
  `--synthetic-media`, which sets `status.containsSyntheticMedia`.
  https://support.google.com/youtube/answer/14328491
- Every upload must declare whether it is made for kids (COPPA). `metadata.json` must set
  `madeForKids` explicitly.

## What the checkpoints cover

| Checkpoint | Files hashed | What the person checks |
| - | - | - |
| script | script.md | facts, claims, voice, originality |
| metadata | metadata.json, thumbnail | title and thumbnail match the content; no clickbait |
| upload | video, metadata.json, thumbnail, upload-plan.json | final cut, privacy, schedule, disclosure |

## Limits of enforcement

Approvals need an interactive terminal and are bound to file hashes, so an agent
running commands without a terminal cannot approve, and any edit after approval blocks
upload. Someone with write access to `state.json` can still forge an approval; the
checkpoints are an audit trail and a guard rail, not a security boundary.
