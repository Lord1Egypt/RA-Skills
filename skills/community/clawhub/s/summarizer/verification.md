# Faithfulness and Coverage Audit

Scope: checking a summary before delivering it, and diagnosing one that went wrong. Two passes in two directions, plus what the automated metrics can and cannot see. Frequency is governed by `verify_pass`.

**When the user reports a defect**, read `## Corrections` in `~/Clawic/data/summarizer/memory.md` (or `corrections.md` per the `## Boxes` index) first: a repeated correction is a standing instruction, and re-learning it every month is the failure this box exists to prevent.

**Contents:** [Two Passes, Two Directions](#two-passes-two-directions) · [Pass 1: Faithfulness](#pass-1-faithfulness) · [Pass 2: Coverage](#pass-2-coverage) · [Error Taxonomy](#error-taxonomy) · [The Number Check](#the-number-check) · [High-Risk Regions](#high-risk-regions) · [Automated Metrics](#automated-metrics) · [LLM-as-Judge](#llm-as-judge) · [Diagnosing a Complaint](#diagnosing-a-complaint) · [The Correction Loop](#the-correction-loop)

## Two Passes, Two Directions

They catch different failures and neither substitutes for the other.

| Pass | Direction | Catches | Question |
|---|---|---|---|
| Faithfulness | Summary → source | Hallucination, distortion, unsupported claims | Is everything I wrote in the source? |
| Coverage | Source → summary | Omission of load-bearing material | Is everything that matters in what I wrote? |

Order matters: faithfulness first, because a summary with a fabricated claim fails regardless of its coverage, and fixing a fabrication frequently frees space that changes the coverage answer.

When `verify_pass: long-only`, both passes run above ~2,000 source words and on anything legal, medical, financial, or externally published. Below that, the Output Gates in `SKILL.md` are the check.

## Pass 1: Faithfulness

Sentence by sentence through the summary. For each one:

1. **Point to the span** in the source that supports it. Not a section — a sentence or a figure.
2. **No span** → the sentence is cut, or rewritten as "the source does not state X", or moved outside the summary and labelled as your judgment.
3. **A span that supports a weaker version** → weaken the sentence to what the span supports. This is the most frequent repair and the least often made.
4. **Check the modifiers, not just the claim.** The claim usually has a span; the "significantly", the "always", the "since 2023" often do not. Contamination of a true claim by an unsupported modifier is the characteristic failure of a fluent summary.
5. **Check attribution direction**: A said X about B, not B said X about A. Swapping the parties keeps every word and inverts the meaning.
6. **Check causal language** against the source's own: sequence, correlation, and causation are three different claims.

A summary that survives this pass can be defended line by line to someone holding the source, which is the actual standard.

## Pass 2: Coverage

From the source side, and it cannot be done by re-reading your summary.

1. **List the source's load-bearing claims independently** — before looking at what you wrote. Load-bearing means a reader acting on the summary would decide differently without it.
2. **Check each against the summary**: present, compressed, or absent.
3. **Absent and material** → it goes in, and something else comes out (the point budget is fixed, SKILL.md Rule 2).
4. **Absent and not material** → it goes in the omission line if it belongs to a protected class: dissent, limitation, cost, deadline, risk.
5. **Check the structural classes** the compression tends to eat wholesale: the counter-argument, the negative result, the thing that did not work, the caveat on the headline number, the minority position, and anything in the last 10% of the source.

## Error Taxonomy

Naming the class tells you where to look for more of the same, because these failures cluster.

| Class | What it is | Example |
|---|---|---|
| Extrinsic hallucination | Content not in the source at all, usually plausible world knowledge | Adding a competitor the report never mentions |
| Intrinsic hallucination | Contradicts the source while using its own material | Reversing which arm improved |
| Entity merge | Two similar entities collapse into one | Two subsidiaries with similar names become one company |
| Relation swap | Correct entities, inverted relationship | "A acquired B" for "B acquired A" |
| Quantifier upgrade | "some" → "most" → "all" | "several teams" becomes "the company" |
| Hedge removal | Modal dropped | "may reduce" becomes "reduces" |
| Negation loss | The "not" disappears | "no significant difference" becomes "a difference" |
| Certainty inflation | Proposal reported as decision | "we should consider" becomes "we will" |
| Temporal drift | Wrong period, or a planned thing reported as done | Guidance reported as results |
| Scope creep | A qualified finding stated generally | An EU pilot's result stated as global |
| Attribution collapse | Claim loses its source | A vendor's uptime figure becomes a fact |
| Causal upgrade | Correlation stated as cause | "associated with" becomes "leads to" |
| Number drift | Magnitude, unit, currency, or precision moved | 4.2M EUR becomes $4.2M; 26.4% becomes "about 30%" |
| Citation drift | A claim attributed to the wrong source in a synthesis | Claim from source C footnoted to source A |
| Omission of the counter | The one dissent or limitation is gone | Consensus manufactured by deletion |

## The Number Check

Numbers are checked separately from prose, because they are checked differently: character by character, not by meaning.

- Every digit string in the summary is matched to a digit string in the source. A number with no match in the source is either derived (label it or cut it) or wrong.
- **Unit, currency, and magnitude** are part of the match. `4.2M` ≠ `4,200` ≠ `4.2%`.
- **Percentage vs percentage point** (`data.md`).
- **Dates**: absolute dates match; relative dates resolve against the source's own date and the resolution is checked.
- **N and denominators**: "3 of 40" must not become "3" or "7.5%" unless the source did it.
- Do this pass last, on the final text — numbers get edited during shortening more often than during drafting.

## High-Risk Regions

Where errors concentrate; check these first when time is short.

| Region | Why |
|---|---|
| The first and last sentences | Written most freely, most likely to contain your framing rather than the source's |
| Anything you found striking | Surprise correlates with mis-transcription (`media.md`) and with misreading |
| Chunk seams in a long source | A claim split across chunks reassembles wrongly (`long-sources.md`) |
| Sentences that merge two source sentences | Merging is where relations get swapped |
| Anything shortened in a second pass | The cut that made it fit is the cut that removed the qualifier |
| Numbers next to each other in the source | Adjacent figures get crossed |
| Names that resemble each other | Entity merge |
| The conclusion sentence | The place where an implied finding becomes a stated one |

## Automated Metrics

Useful as regression signals, dangerous as gates. Each is blind to something the human reader will notice immediately.

| Metric | Measures | Cannot see |
|---|---|---|
| ROUGE (n-gram overlap with a reference) | Lexical similarity to a reference summary | Hallucination that reuses source vocabulary; any correct summary phrased differently from the reference |
| BLEU | Precision of n-grams against a reference | The same blind spots, with a shorter memory |
| BERTScore / embedding similarity | Semantic closeness | Negation, quantifier, and number errors — the exact failures that matter, because they barely move an embedding |
| Compression ratio | Length only | Whether anything survived |
| Entailment / NLI scoring per sentence | Whether the source entails each summary sentence | Omission, entirely — a summary of one sentence can score perfectly |
| Question-answering consistency | Whether questions generated from the source get the same answer from the summary | Only the dimensions the generated questions happen to cover |

The pattern: reference-based metrics measure similarity to someone else's summary, and none of them measure coverage. Use them to detect a regression across many summaries; never as the reason to ship one.

## LLM-as-Judge

- **The source must be in the judge's context.** A judge scoring a summary alone measures fluency and plausibility, which is how a confident hallucination scores highest.
- **Judge one dimension at a time** with a binary or three-point rubric — faithfulness, coverage, length compliance, format compliance. A single 1-10 "quality" score collapses into fluency.
- **Ask for the span.** A judge required to quote the supporting span for each claim catches what a judge asked "is this faithful?" waves through.
- **Position and length bias**: judges prefer longer and prefer the first option shown. When comparing two summaries, swap the order and run twice.
- **Self-critique is a real gain and a weak one.** A model reviewing its own summary against the source finds omissions and unsupported claims reliably; it defends its own phrasing. Give the critique pass a rubric and the source, not "improve this".

## Diagnosing a Complaint

| Complaint | Usual cause | Fix |
|---|---|---|
| "You missed the most important part" | Ranked by the source's emphasis rather than the reader's need | Ask what they will do with it; re-rank (Razor Questions) |
| "That's not what it says" | Hedge, quantifier, or attribution lost | Faithfulness pass on that sentence; check the whole summary for the same class |
| "Where did that come from?" | Extrinsic hallucination, often a plausible detail | Cut it; check every unsourced specific |
| "Too long" | Level not agreed before writing | Name the level and target words up front (SKILL.md Rule 1) |
| "Too vague" | Shortened by cutting adjectives instead of branches | Fewer points, each with its number (Rule 2) |
| "This is just the headings" | Topic labels instead of outcomes | Every point states an outcome or a number |
| "It reads like the source" | Extractive output presented as abstractive, or the source's voice inherited | Rewrite in the neutral register (`audience.md`) |
| "You changed the meaning" | Merged two sentences, or upgraded causality | Un-merge; restore the source's causal verb |
| "It's wrong about the numbers" | Derived a figure the source did not state | Number check; never derive (`data.md`) |
| Anything else | Unknown | Ask which sentence, then classify it in the taxonomy above |

## The Correction Loop

A correction is worth more than the summary that produced it: it is a standing instruction about this user, this domain, or this source type.

- **Record the class, not just the instance.** "Dropped the dissent" is reusable; "missed Priya's objection on 14 July" is not.
- **A correction repeated twice becomes a rule** — a key in `config.yaml` under the restrictions area if it is a preference, a line in `## Corrections` if it is a fidelity pattern.
- **Check the box before summarizing the same source type again.** That is the read hook at the top of this file, and it is the only mechanism that makes the second month better than the first.

**After any correction or failed summary**, write it to `## Corrections` in `~/Clawic/data/summarizer/memory.md` — date, source type, error class from the taxonomy, and the rule that would have prevented it — and split it to `corrections.md` when the section passes the threshold in `memory-template.md`, keeping the same headings. If the correction is a stated preference rather than an error, it goes to `config.yaml` instead. Formats and thresholds: `memory-template.md`.
