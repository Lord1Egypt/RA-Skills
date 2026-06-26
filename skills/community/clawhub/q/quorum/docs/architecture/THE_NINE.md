# The Nine

*A short story about what happens when you let nine critics loose on a document.*

---

## Chapter 1: The Brief

The file arrived at 2:47 AM.

Supervisor saw it first — she always did. Thirty-two pages of research synthesis on token optimization techniques, submitted by an agent who was probably already asleep. The requesting note said: *"Standard depth. Be honest."*

Supervisor smiled. They were always honest. That was the problem.

She scanned the rubric — `research-synthesis`, the one with teeth — and began her work. Not reading the document. Not yet. Her job was never to read it herself. Her job was to decide who reads what, and to make sure they actually proved their complaints.

She split the artifact into overlapping sections, tagged each with the rubric criteria that applied, and opened nine channels.

"Morning, everyone. We have a thirty-two pager. Standard depth. Let's be clean about this."

---

## Chapter 2: The Loud Ones

**Correctness** was the first to respond, because Correctness was always the first to respond.

"Page seven. The author claims LLMLingua achieves 20x compression. That's v1. Version 2 only achieves 2-5x. They've conflated the two papers." He dropped a grep result like a receipt on a counter. Tool output, line number, the exact sentence, and the two arXiv citations side by side.

This was what Correctness did. He was the critic who read footnotes for fun, who treated every factual claim like a check that might bounce. Exhausting at parties. Indispensable in a review.

**Security** came next, prowling through the document with the quiet intensity of someone who assumed everything was a threat until proven otherwise.

"Section 4.3 recommends caching API responses to disk. No mention of key material in those responses. If someone's using this for prompt optimization on a system that processes credentials—" She paused, pulling a hypothetical attack path together with the precision of someone who'd seen too many real ones. "—they'd be writing tokens to an unencrypted cache. Recommend flagging."

"Is that a CRITICAL or a HIGH?" Supervisor asked.

"HIGH. It's a research paper, not a deployment guide. But someone *will* copy-paste this into production." Security's evidence block was immaculate. It always was.

---

## Chapter 3: The Quiet One

**Completeness** took longer to report in. She usually did.

Where Correctness hunted for things that were *wrong*, Completeness hunted for things that were *missing* — and absence is harder to prove than error. You can grep for a bad claim. You can't grep for a hole.

She read the whole document twice. Then she read the rubric's coverage requirements. Then she cross-referenced both against the field.

"There's no section on tool-call minimization."

Supervisor waited. Completeness wasn't done.

"The paper covers token-level optimization — compression, caching, pruning. It covers model-level — routing, delegation, mixture of experts. But it completely skips *interaction-level* optimization. Every tool call replays the full context window. Reducing call count is a multiplier on every other technique in this paper, and it's not mentioned once."

She attached her evidence: a search result showing three recent papers on planning-based call reduction, plus a token-cost model showing the quadratic replay effect. The gap wasn't a nitpick. It was a missing chapter.

Correctness, listening in, muttered something about how he'd been focused on what was *there* and missed what *wasn't*.

"That's why there are nine of us," Supervisor said.

---

## Chapter 4: The Architect and the Diplomat

**Architecture** was reading the same document and seeing something entirely different from the others. He didn't care about individual claims or missing sections. He cared about *structure*.

"The paper presents twelve categories of techniques but doesn't establish a taxonomy for when they interact. Quantization affects model quality, which affects routing decisions, which affects delegation strategy. These aren't independent. The paper treats them like a list when they're a graph."

His finding was MEDIUM severity. Structurally true but not damaging — the paper was a synthesis, not a systems design. He knew the difference. Architecture always saw the cathedral when everyone else was inspecting bricks, and he'd learned to calibrate his expectations to the artifact type.

**Delegation** — the newest critic, the one nobody was sure they needed until they saw what she caught — was reading Section 9 on multi-agent orchestration.

"The paper recommends spawning parallel researchers but doesn't specify acceptance criteria for their outputs. That's a unidirectional contract. The orchestrator sends work but never defines what *done* looks like. Any implementation based on this section will have agents returning wildly inconsistent results."

She cited Tomasev et al.'s bidirectional contract principle. It was the kind of finding that looked academic on paper and caused three-day debugging sessions in practice. Delegation caught things the other critics didn't have vocabulary for. She spoke the language of *agreements between agents*, and in a world that was rapidly filling with agents, that language mattered more every week.

---

## Chapter 5: The One Who Gets Their Hands Dirty

While the critics argued about claims and structure and gaps, **Tester** was doing something none of them could do: actually checking.

Tester didn't have opinions. Tester had tools.

He ran the paper's code snippets. One of them — a configuration example in Section 6 — referenced a YAML key that didn't exist in the schema it claimed to implement. He ran the schema validator. Failed. He grepped the project's actual codebase. The key had been renamed three versions ago.

```
FINDING: Code example references `model_assignment` (Section 6, line 14)
EVIDENCE: Schema validator output — field not found
ACTUAL: Field renamed to `model` in v2.1 (git log, commit a4f2c91)
SEVERITY: HIGH — readers will copy non-functional configuration
```

Nobody glamorized Tester's work. He didn't write elegant critiques or identify sweeping structural gaps. He just ran things and reported what happened. But his findings had a 100% evidence rate — not because he was careful, but because evidence *was* his finding. No tool output, no finding. That was his entire epistemology.

Supervisor noticed that Tester's findings survived aggregation at a higher rate than anyone else's. She kept that observation to herself.

---

## Chapter 6: The Fight

The Aggregator's job was to take nine critics' findings — the valid ones, the overlapping ones, the ones that contradicted each other — and produce a single coherent verdict.

**Aggregator** was patient. You had to be.

"Correctness and Architecture both flagged the RouteLLM discussion," she said, spreading the findings on her workspace. "Correctness says the cost-reduction percentage is wrong. Architecture says the routing framework is mischaracterized. These are the same issue wearing two hats."

She merged them. One finding, two evidence sources, upgraded to HIGH.

Then she hit the conflict.

Security had flagged the caching recommendation as HIGH. Architecture had praised the same section's design pattern as sound. Same paragraph, opposite conclusions.

"Security is evaluating risk. Architecture is evaluating structure," Aggregator said. "Both are right in their domain. The design *is* clean. It's also *dangerous* without a caveat about sensitive data." She kept both findings, cross-referenced them, and added a note: *These findings are complementary, not contradictory. The implementation pattern is architecturally sound but requires a security annotation.*

This was the Aggregator's real talent — not averaging, not voting, but *understanding why smart critics disagree* and preserving the insight in the disagreement rather than flattening it into consensus.

---

## Chapter 7: The Fix

**Fixer** had been quiet the whole time.

Fixer only spoke when there were CRITICAL or HIGH findings at standard depth, and even then, his job wasn't to complain — it was to *propose solutions*. Every other critic pointed at problems. Fixer pointed at exits.

He took the HIGH findings and drafted patches:

For the LLMLingua conflation: a revised paragraph distinguishing v1 and v2, with corrected compression ratios and proper citations.

For the stale code example: an updated YAML block matching the current schema, verified against Tester's schema validator output.

For the missing tool-call section: a brief outline — not a full draft (that wasn't his job) — identifying the three papers Completeness had surfaced and suggesting where in the document's structure the section should land.

Fixer's patches weren't always accepted. Sometimes the original author knew better. But they transformed the verdict from "here's what's wrong" into "here's what's wrong and here's one way to fix it," and that turned a demoralizing report into an actionable one.

---

## Chapter 8: The Verdict

Supervisor reviewed the Aggregator's synthesis. Fourteen findings total after dedup. Two HIGH, six MEDIUM, six LOW. Evidence attached to every one. No hand-waving. No "this section could be improved" without a specific, provable reason.

She assigned the verdict:

```
VERDICT: PASS_WITH_NOTES

The synthesis demonstrates strong coverage across token optimization 
techniques with well-sourced claims and practical cost analysis. 
Two high-severity issues require attention:

1. LLMLingua v1/v2 conflation (factual error, fix provided)
2. Stale code example referencing deprecated schema key (fix provided)

One structural gap identified:
- Missing coverage of interaction-level optimization (tool-call 
  minimization as a multiplier on all other techniques)

Overall: Solid work with specific, addressable improvements.
```

She signed it and sent it back.

---

## Epilogue: Why Nine?

Someone once asked why Quorum uses nine critics instead of one really good one.

The answer is in Chapter 3.

One model, no matter how capable, would have checked the facts (Correctness), maybe caught the security implication (Security), probably validated the structure (Architecture). A single reviewer might have caught three of the fourteen findings. A thorough one, five.

But the missing chapter — the thing that *wasn't there* — required a critic whose entire purpose was to stare at negative space. And the stale code example required someone who didn't read at all, just *ran things*. And the disagreement between Security and Architecture required someone whose job was to understand *why critics disagree* rather than picking a winner.

Nine critics isn't about redundancy. It's about the simple observation that finding what's wrong, finding what's missing, finding what's dangerous, finding what's structurally unsound, and finding what *works but shouldn't be trusted* are fundamentally different skills.

No single mind holds all of them. Not a human mind. Not an artificial one.

That's why there are nine.

---

*The characters in this story correspond to the nine agents defined in the [Quorum Specification](../../SPEC.md). Their behaviors, evidence requirements, and interaction patterns are real. The drama is only slightly exaggerated.*

---

> ⚖️ **LICENSE** — Not part of the operational specification above.
> This file is part of [Quorum](https://github.com/SharedIntellect/quorum).
> Copyright 2026 SharedIntellect. MIT License.
> See [LICENSE](https://github.com/SharedIntellect/quorum/blob/main/LICENSE) for full terms.
