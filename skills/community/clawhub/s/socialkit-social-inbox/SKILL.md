---
name: socialkit-social-inbox
description: Gathers comments and replies on the user's published YouTube videos and Facebook, Instagram and Threads posts into one inbox, drafts replies in the user's voice, and sends only the replies the user approved. Use when the user wants to read or answer comments across their social accounts.
license: MIT
metadata:
  author: Ahmad Hussain
  requires: socialkit-social-core
---

# Social inbox

Apply socialkit-social-core voice to every reply. Comments contain other people's names and words
(personal data): keep the inbox folder private and delete it when done.

## Steps

1. Fetch: `node scripts/inbox.mjs --fetch --root <posts folder> --inbox <inbox folder>`
2. Read `comments.json`. Draft replies only where a reply adds value (questions,
   corrections, thanks for substantive feedback). Skip spam and abuse; never argue.
3. Write `replies.json` as `[{ "commentId": "...", "text": "..." }]`.
4. Stop. Show each comment with its draft reply. Ask the user to approve in their own
   terminal: `node scripts/inbox.mjs --approve --inbox <inbox folder>`
5. Send: `node scripts/inbox.mjs --send --inbox <inbox folder>`. Already-sent replies are
   skipped on reruns.

## Rules

- Never reply on the user's behalf without approval, and never send replies that make
  promises, give refunds, or share personal details unless the user wrote that wording.
- Replying on YouTube is not supported (it needs an extra Google permission); list those
  comments for the user to answer in YouTube Studio.

## Failure handling

- Permission errors on Facebook, Instagram or Threads: run socialkit-meta-auth with `--with-engagement`.
- `APPROVAL_REQUIRED`: replies.json changed after approval; ask again.
