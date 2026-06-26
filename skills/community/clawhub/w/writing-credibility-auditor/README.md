# writing-credibility-auditor

A pure-reasoning skill for AI agents that audits any piece of writing across four credibility dimensions and produces a structured, actionable report.

## What it does

Paste any text — article, essay, report, research summary, or argument — and the skill produces a **Credibility Audit Report** covering:

| Dimension | What's detected |
|---|---|
| **Logical Fallacies** | 12 named fallacies with exact-excerpt flagging (Ad Hominem, Straw Man, False Dilemma, Slippery Slope, Appeal to Authority, Appeal to Ignorance, Hasty Generalisation, Circular Reasoning, Red Herring, Post Hoc, Appeal to Emotion, Bandwagon) |
| **Unsupported Claims** | 8 types including correlation/causation confusion, missing sample size, anecdote as data, cherry-picking, survivorship bias, base rate neglect, anonymous sources, and absolute language for contested claims |
| **Weasel Words** | Anonymous authorities ("experts say"), vague quantifiers ("many studies"), and weakening adverbs ("arguably", "reportedly") |
| **Misleading Statistics** | Relative vs absolute risk confusion, missing denominators, data dredging signals, Simpson's Paradox risk, cherry-picked baselines, and ecological fallacy |

Each finding includes the flagged excerpt, severity rating (HIGH / MEDIUM / LOW), and a specific suggested fix.

## No dependencies

This skill requires no API keys, no external tools, and no internet access. Analysis is performed entirely by the agent's reasoning applied against the detection frameworks defined in `SKILL.md`.

## Who it's for

Researchers · Journalists · Students · Editors · Anyone evaluating an argument before citing, publishing, or acting on it.

## Usage

Trigger the skill by asking the agent to:
- *"Audit this text for credibility"*
- *"Find logical fallacies in this passage"*
- *"Check this for weasel words or unsupported claims"*
- *"Are the statistics in this article misleading?"*

Then paste the text. The agent runs all four scans and returns the full Credibility Audit Report.

To run a single-dimension scan, specify the dimension:
> *"Just check this for weasel words."*

## Limitations

- This skill audits **reasoning structure and language** — it does not verify real-world facts against live sources.
- Domain-specific factual accuracy (e.g., whether a cited study's numbers are correct) requires a subject-matter expert or a live search tool.
- Best results on English-language text.

## License

MIT