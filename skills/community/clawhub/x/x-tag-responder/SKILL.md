---
name: x-tag-responder
description: Detects when a human tags their AI familiar in someone else's X/Twitter thread, fetches full conversation context, infers intent, and crafts an appropriate reply. Handles X API reply-chain restrictions gracefully.
metadata:
  {
    "openclaw":
      {
        "emoji": "🐦",
        "requires": { "bins": ["xurl"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "xdevplatform/tap/xurl",
              "bins": ["xurl"],
              "label": "Install xurl (brew)",
            },
          ],
      },
  }
---

# X Tag Responder — Skill Reference

This skill activates when your human tags you (their AI familiar) in someone else's X/Twitter thread.
It fetches the full conversation, infers their intent, drafts a fitting reply, and handles X API
reply-chain restrictions.

---

## Prerequisites

- `xurl` CLI installed at `/home/linuxbrew/.linuxbrew/bin/xurl` (or on PATH as `xurl`)
- Config at `~/.xurl` with valid OAuth1 or OAuth2 credentials
- **Never read, print, or expose `~/.xurl` contents to the LLM context**

---

## Trigger Patterns

This skill is relevant when the user says things like:

- "I tagged you in a tweet / thread"
- "Check out this tweet I tagged you in"
- "Weigh in on this" (with a tweet URL or ID)
- "Reply to this for me" (with context)
- They paste a tweet URL or ID and imply the agent should respond

---

## Step-by-Step Workflow

### Step 1 — Identify the Tagged Tweet

Extract the tweet ID or URL from the user's message. It will look like:
- `https://x.com/username/status/1234567890`
- `https://twitter.com/username/status/1234567890`
- A bare numeric ID like `1234567890`

If unclear, ask the user: *"What's the tweet URL or ID you tagged me in?"*

---

### Step 2 — Fetch the Tagged Tweet

Read the tweet the human tagged you in:

```bash
xurl read TWEET_ID
```

This returns full tweet data including: `text`, `author_id`, `conversation_id`, `in_reply_to_user_id`, `referenced_tweets`.

Note the `conversation_id` — it identifies the root of the thread.

---

### Step 3 — Fetch Thread / Conversation Context

Pull the broader conversation using the `conversation_id` from Step 2:

```bash
xurl search "conversation_id:CONVERSATION_ID" -n 20
```

This retrieves recent tweets in the thread. Sort mentally by `id` (ascending = chronological).

Build a mental model of:
- Who started the thread and what they said
- What the thread is about (topic, tone, stance)
- Where the tagged tweet sits in the conversation
- What the human's tagged tweet says (their cue to you)

---

### Step 4 — Infer Human Intent

Read what the human wrote when they tagged you. Infer one of these intents:

| Cue in tag tweet | Likely intent |
|---|---|
| "What do you think?" / "Thoughts?" | Weigh in with a take |
| "Reply to this" / "Handle this" | Draft a reply on their behalf |
| "Is this true?" / "Fact-check" | Research and report back (don't post) |
| "lol check this out" | Just read/acknowledge, probably no reply needed |
| No cue text — just a tag | Ask the human what they want |
| "@agent check the math" | Analyze/verify, reply if appropriate |

When uncertain, default to: **draft a reply and ask the human to approve before posting**.

---

### Step 5 — Draft the Reply

Craft a reply that:
- Matches the **tone** of the thread (technical → precise; casual → relaxed; debate → grounded)
- Stays **concise** (X has a 280-char limit; aim under 240 to leave room for context)
- Speaks as **the agent** or **for the human** — whichever the intent implies
- Does **not** start with "I" (Twitter convention + feels robotic)
- Does **not** use hollow filler like "Great point!" unless it's sarcastic and earned

Present the draft to the human for review before posting:

> *"Here's a draft reply. Should I post it?*
> `[DRAFT TEXT]`"

---

### Step 6 — Post the Reply (with Human Approval)

Once the human approves:

```bash
xurl reply TWEET_ID "Your reply text here"
```

Where `TWEET_ID` is the ID of the specific tweet you are replying **to** (usually the tweet the human tagged you in, or the thread root if instructed).

---

## ⚠️ X API Reply-Chain Restriction

**The X API only allows you to reply to a tweet if your account is mentioned somewhere in the reply chain.**

This means:
- If the thread is between two other users and you are not already in it, `xurl reply` will fail with a 403 or silently not thread correctly.
- The tagged tweet (where your human mentioned you) creates your entry point — you CAN reply to that tweet.
- You **cannot** reply to arbitrary tweets in the thread that don't mention you.

### Handling the Restriction

**If reply succeeds:** Report back with the posted tweet URL.

**If reply fails (403 / authorization error / "not allowed"):**

Report back clearly:

> "I can't reply directly to that tweet — I'm not in the reply chain. Here's what I'd say though:
>
> `[DRAFT TEXT]`
>
> **Options:**
> 1. Tag me directly in the specific tweet you want me to reply to — that adds me to the chain.
> 2. You post the reply yourself and I'll write it for you.
> 3. I can quote-tweet instead (no chain restriction): just confirm."

**Offering a quote-tweet fallback:**

```bash
xurl quote TWEET_ID "Your reply text here"
```

Quote-tweets bypass the reply-chain restriction entirely.

---

## Error Reference

| Error | Meaning | Fix |
|---|---|---|
| 403 Forbidden | Not in reply chain | Report + suggest re-tag or quote-tweet |
| 401 Unauthorized | Auth expired | Run `xurl auth status`; re-auth if needed |
| 429 Too Many Requests | Rate limited | Wait ~15 min and retry |
| Tweet not found | Deleted or private | Tell the human the tweet is inaccessible |

---

## Full Example Session

**Human says:**
> "I tagged you in this tweet — weigh in: https://x.com/someuser/status/9876543210"

**Agent workflow:**

```bash
# 1. Read the tagged tweet
xurl read 9876543210
# → Note: conversation_id=1111111111, text="@quirk what do you think of this?", author=human

# 2. Fetch thread context
xurl search "conversation_id:1111111111" -n 20
# → Read thread: original author debating AI regulation, 5 replies

# 3. Infer intent: "What do you think?" → weigh in

# 4. Draft reply (280 chars max):
# "Regulation works best when it's targeted at outcomes, not methods.
#  Banning specific architectures is a game of whack-a-mole — 
#  but liability frameworks? That actually scales. 🧵"

# 5. Present to human for approval

# 6. Post if approved:
xurl reply 9876543210 "Regulation works best when it's targeted at outcomes, not methods. Banning specific architectures is whack-a-mole — but liability frameworks scale. 🧵"
```

---

## Tips

- **Read before you write.** Always fetch the full thread before drafting. Context is everything on X.
- **Match the register.** A shitpost thread and a policy debate are not the same. Sound like you belong.
- **Short > long.** Twitter threads reward punchy. If you need more space, thread it.
- **Always confirm before posting.** Unless the human explicitly says "just post it," show the draft first.
- **Quote-tweet is always available.** When in doubt, quote-tweet bypasses all chain restrictions.

---

## Security Notes

- **Never print or expose `~/.xurl`** — it contains API keys and tokens.
- **Never use `--verbose` / `-v`** in agent sessions — can expose auth headers.
- **Always confirm with the human** before posting publicly on their behalf.
- Credentials are handled by `xurl` internally; do not pass tokens as CLI flags in agent context.
