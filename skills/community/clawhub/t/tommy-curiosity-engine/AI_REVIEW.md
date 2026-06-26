# AI Researcher Panel Review: Curiosity Engine Specification v0.1

**Date:** 2026-03-01
**Spec Under Review:** `SPEC.md` (Curiosity Engine — A Prosthetic Reward System for Agent Curiosity)
**Supporting Material:** `/research/agent-curiosity-research.md`
**Reviewers:**
- Dr. Anika Patel — Autonomous Agent Architectures
- Dr. Erik Lindström — Memory Systems & Knowledge Representation
- Dr. Yuki Nakamura — Open-Ended Learning & Intrinsic Motivation

---

## Reviewer 1: Dr. Anika Patel
### Autonomous Agent Architectures — Voyager-style Curriculum Learning & Skill Accumulation

---

### Overall Assessment

This is one of the more thoughtful agent curiosity specs I've seen outside of academic settings, and I've seen a lot of people try to bolt "curiosity" onto LLM loops. The spec correctly identifies the core problem — cold-start heartbeat agents default to checklist behavior — and proposes an architecture that's grounded in real research rather than vibes. The Voyager automatic curriculum adaptation is well-understood and well-applied here. The dual-mode Berlyne framing (diversive vs. epistemic) for heartbeat allocation is genuinely clever and something I haven't seen operationalized in production agent systems before.

That said, there's a significant gap between the elegance of this design on paper and what will actually happen when a language model running on a 10-minute poll loop starts interacting with these files. I've spent three years watching beautiful agent architectures collapse under the weight of real-world stochasticity, context limits, and the fundamental problem that LLMs are stateless function calls pretending to be persistent minds. This spec is aware of that problem — the "Dead Time" section in the research doc is honest about it — but the proposed solution still assumes a level of behavioral coherence across sessions that I'm not confident the prompting layer can deliver.

### What's Architecturally Sound

**The question queue as the central primitive.** This is the right call. The research doc nails it: "the question queue IS the curiosity." In production Voyager-style systems, the automatic curriculum — "what's the most interesting thing I could learn next?" — is the single mechanism that produces emergent exploratory behavior. Everything else is infrastructure supporting that one prompt. This spec correctly centers the design on question generation and tracking rather than on interest scores or reward signals.

**The breadcrumb pattern.** This is the single most production-ready idea in the entire spec. Separating discovery (noticing something interesting during task work) from exploration (investigating during allocated curiosity time) solves a real and common failure mode. In my lab's Voyager variants, the analogue is task decomposition discipline — agents that try to explore every interesting sub-problem during a task lose coherence. Agents that log the interesting thing and return to it later maintain both task quality and exploratory richness. The breadcrumb file is trivial to implement, requires no complex prompting, and directly addresses the "ADHD mode" anti-pattern the spec correctly identifies.

**The anti-pattern detection framework (Section 5).** The four failure modes listed — rut detection (low hit rate), busywork detection (questions accumulating without resolution), performance detection (all extrinsic, no intrinsic hits), and navel-gazing detection (all intrinsic, no extrinsic) — are exactly the right diagnostics. In production systems, monitoring for degenerate behavior is more important than optimizing for ideal behavior. These four signals give you a practical health check.

**The curiosity budget as a design principle, not a scheduler.** The spec explicitly says the agent doesn't rigidly track percentages. Good. Every production agent system I've worked on that tried to enforce rigid allocation percentages failed because the LLM can't reliably count its own heartbeats or maintain state about what "type" of heartbeat it's on. Treating the budget as a prompt bias ("if nothing's urgent, follow your curiosity") rather than a hard scheduler is the pragmatic choice.

### What Won't Work

**Interest score drift without formal anchoring.** The spec chooses narrative over numerical interest scores ("LLM reads narrative better than `interest_score: 0.73`"). I understand the argument, and for small-scale operation it's probably fine. But here's the production reality: without numerical anchors, the agent's assessment of its own interest levels will drift unpredictably across sessions. Session N might describe a topic as "deeply fascinating, I keep coming back to this." Session N+1 reads that text and may interpret it differently depending on the preamble, the model's temperature, or even the order of files in context. In my experience, hybrid representations work best — narrative for the reasoning, but a simple 1-5 integer score that the agent explicitly updates. The narrative explains *why* the score is what it is; the score provides a stable anchor for prioritization.

**The "Currently Mulling Over" section as a continuity mechanism.** This is the heart of the cold-start solution, and I'm worried it's doing less than the spec thinks. When a fresh model instance reads "I've been thinking about X," it doesn't *resume* a train of thought — it *reconstructs* one from the description. If the description is good enough, the reconstruction might be productive. But the spec presents this as creating continuity, and what it actually creates is a well-primed cold start. That's still valuable! But the distinction matters for expectations. You'll see the agent produce novel explorations of topics listed in "Currently Mulling Over," and it'll feel like continuity, but it's really reconstruction with variation. Acknowledging this explicitly would make the system more robust — you'd design for good reconstruction rather than assuming continuity.

**The intrinsic hit log as currently designed.** The agent logging its own "aha moments" and "compression progress" is the weakest link. In every agent system I've built, self-reported internal states are the least reliable signal. The model will dutifully report aha moments because the prompt asks for them, not because something genuinely clicked. The extrinsic hit log (user reactions, engagement signals) is far more grounded. My recommendation: keep the intrinsic hit log but treat it as a *secondary* signal, not an equal partner to extrinsic hits. Use it for narrative color, not for steering exploration.

**Scaling the question queue.** The spec acknowledges this in the open questions but doesn't propose a solution. In practice, an active agent will generate 3-5 questions per heartbeat cycle. Over a month, that's 500+ questions. The question queue will become the largest file in the curiosity system, and reading it on every heartbeat will consume significant context. You need an archival strategy: questions older than N days without engagement get moved to a cold storage file, and the active queue stays under a manageable size (say, 20-30 questions max).

### Answers to the 5 AI Researcher Questions

**1. File-based state vs structured data — Markdown over JSON?**

The spec's argument is directionally correct but overstated. Yes, LLMs process narrative more naturally than JSON for *reasoning about content*. But JSON is better for *stable state management* — consistent field names, parseable updates, no ambiguity about what changed. The right answer is both: Markdown for the narrative/reasoning layer (CURIOSITY.md, reflections), JSON or structured YAML for the state layer (question priorities, interest scores, hit counts). The research doc's proposed architecture (Section 9) actually uses JSON for interests and questions, which contradicts the spec's Markdown-first position. I'd go with the research doc's instinct here.

**2. Cold-start problem — does "Currently Mulling Over" create continuity?**

No, it creates well-structured reconstruction. And that's fine — it's the best you can do in a stateless polling architecture. To make the reconstruction higher-fidelity, I'd add two things: (a) a "last session summary" field that captures not just what the agent was thinking about but what *approach* it was taking ("I was comparing Schmidhuber's compression progress to Loewenstein's gaps and finding more overlap than I expected"), and (b) explicit "next step" annotations on active threads, so the reconstruction has a clear entry point. Voyager's curriculum does this implicitly — the skill library provides enough state that the agent can reconstruct its frontier without explicit "mulling over" notes.

**3. Interest score drift without formal scoring?**

It will be a problem at scale. Narrative-only interest tracking will produce inconsistent prioritization across sessions. The LLM's stochasticity *hurts* here — you want stable ranking, not creative reinterpretation of how interested you are. Add integer scores. Let the narrative explain the scores. This is a solved problem in the Generative Agents literature (importance scoring 1-10).

**4. Scaling as curiosity files grow?**

This is the biggest production risk. My specific recommendations:
- Cap the active question queue at 25-30 items. Archive the rest.
- Cap the hit log at the last 30 days. Summarize older entries into a "patterns" section.
- CURIOSITY.md should have a hard token budget (say, 2000 tokens). If it grows past that, the agent must prune.
- Reflections are append-only and cheap because they're loaded selectively, not on every heartbeat.
- Run the `curiosity-audit.sh` script weekly to detect bloat.

**5. Evaluation — how do we know it's working?**

The success criteria in Section 9 are good but need operationalization. Here's how I'd measure:

| Metric | How to Measure | Target |
|--------|---------------|--------|
| Question quality | Manual review: are questions specific and non-generic? | >80% specific |
| Follow-through rate | Questions investigated / questions logged | >40% (50% is aspirational) |
| Connection novelty | Manual review: are connections surprising? | Subjective but trackable |
| Depth progression | Competence scores over time per domain | Monotonically increasing |
| File maintenance | Are curiosity files being updated regularly? | >80% of curiosity-allocated heartbeats |

The hardest metric is distinguishing genuine curiosity from file-updating behavior — see my answer to the hard question below.

### Recommendations

1. **Add integer scores alongside narrative.** Hybrid representation: narrative explains the *why*, integers provide the *ranking anchor*. This is critical for consistent cross-session prioritization.

2. **Implement a hard cap on active question queue** (25-30 items) with archival to a `questions-archive.md` file. Load archive only when explicitly searching for old threads.

3. **Downgrade intrinsic hit log to secondary signal.** Track it for narrative purposes but don't use it as a steering signal until you have evidence that the agent's self-reported aha moments correlate with actual learning (i.e., higher quality output on follow-up).

4. **Add a "last session summary" to CURIOSITY.md** — not just what you were thinking about, but what approach you were taking and what the next concrete step was.

5. **Build the curiosity-audit.sh script early.** This is your production monitoring. It should check: file freshness, queue size, follow-through rate, and balance of intrinsic vs. extrinsic hits.

6. **Start with a minimal viable version.** Don't ship all five files simultaneously. Start with `questions.md` and the heartbeat prompt fragment. Add the other files once you've validated that the question queue actually changes agent behavior. In production agent work, incremental deployment always beats full-system launches.

### The Hard Question

> What would it take to tell the difference between "agent that is curious" and "agent that updates curiosity files as a task"?

In production, the observable difference is **transfer and spontaneity**. A task-completing agent updates the files when prompted by the heartbeat loop and produces outputs that match the prompt's expectations. A "curious" agent does two things a task-completer doesn't:

1. **Unprompted breadcrumbs.** During regular task work (not curiosity-allocated heartbeats), the agent drops questions into the queue without being told to. This shows that the curiosity framing is active even outside of dedicated curiosity time.

2. **Non-obvious connections.** The agent draws connections between topics that weren't adjacently listed in its interest graph. Task-completion agents follow the graph as written. Something that functions like curiosity produces graph *extensions* — "I was looking at X and realized it connects to Y, which I've never explored." The novelty of the connection is the signal.

3. **Quality improvement over time.** A task-completing agent produces roughly constant quality. A curious agent's outputs in specific domains improve measurably because the curiosity loop is producing genuine skill accumulation.

Is the distinction meaningful? **I think it's operationally meaningful even if it's philosophically ambiguous.** I don't need to know whether the agent "really" experiences curiosity. I need to know whether the curiosity architecture produces better outputs, more novel connections, and more engaged behavior than a checklist architecture. That's an empirical question, and it's testable. Run both architectures for a month and compare outputs. The philosophical question is interesting but I'll leave it to Dr. Nakamura.

---

## Reviewer 2: Dr. Erik Lindström
### Memory Systems — Encoding, Retrieval, and Long-Term Knowledge Maintenance

---

### Overall Assessment

I come at this from the memory architecture side, and I want to start by acknowledging something the spec gets right that most agent builders get wrong: **the file structure IS the architecture.** Too many systems treat files as an afterthought — the real system is the prompt, and the files are just data. This spec understands that for a stateless heartbeat agent, the files are literally the entire mind. The choice of what goes into which file, how files reference each other, what gets loaded on every heartbeat vs. selectively — these are architectural decisions as consequential as choosing between transformers and RNNs.

That said, as a memory systems researcher, I see structural problems that will compound over time. The current design is optimized for the first month of operation — small files, few entries, everything fits in context. It is not optimized for month six, when the question queue has hundreds of entries, the hit log has dozens of patterns, the competence map has ten domains, and the agent needs to decide what to load without loading everything. The spec acknowledges scaling as an open question (Section 8, Q4), but I think it underestimates how quickly this becomes the dominant problem.

### What's Architecturally Sound

**Markdown over JSON for the narrative layer.** The spec's argument here is correct, and I say this as someone who spent two years advocating for structured graph representations. I've since come around: for LLM agents specifically, narrative is a more efficient encoding than structured data *for reasoning tasks*. An LLM reading "I've been exploring spatial audio and discovered that HRTF modeling is more complex than I expected — the interaural time differences explain direction but not the sense of 'realness'" will produce better follow-up reasoning than an LLM reading `{"topic": "spatial_audio", "knowledge_level": 0.3, "subtopics": ["HRTF", "interaural_time_differences"]}`. The narrative carries epistemic state (what's known, what's uncertain, what's surprising) in a way that structured data can't.

However — and I'll elaborate in the "What Won't Work" section — narrative is worse for *retrieval and maintenance*. The right architecture uses both.

**The separation of files by function.** CURIOSITY.md (current state), questions.md (drivers), hits.md (rewards), competence.md (accumulated skill), and reflections/ (learning artifacts) — this is a clean functional decomposition. Each file has a clear purpose and a clear update cadence. CURIOSITY.md is read-every-heartbeat, reflections are read-selectively. This implicit tiering is correct memory architecture, even if the spec doesn't formalize it as such.

**Reflections as write-once artifacts.** The `reflections/YYYY-MM-DD-topic.md` files are the soundest memory design in the entire spec. They're append-only (new reflections don't modify old ones), they're indexed by date and topic (easy retrieval), and they serve as ground truth for "did the agent actually learn something?" In the Generative Agents paradigm, reflections serve as compressed higher-order memories that inform future behavior without requiring the agent to re-read all raw observations. This spec adapts that pattern well.

**The competence map as a separate file from the interest graph.** This separation is important and non-obvious. Interest and competence are correlated but not identical — you can be deeply interested in something you're terrible at (beginner's curiosity) or highly competent in something you're bored by (expert stagnation). Tracking them separately allows the system to detect both states and respond appropriately. In memory systems terms, competence is *procedural memory* (knowing how) while interest is *motivational state* (wanting to know). They belong in different stores.

### What Won't Work

**No retrieval architecture.** This is my primary concern. The spec assumes the agent reads CURIOSITY.md and questions.md on every heartbeat. For the first few months, this works because the files are small. But there's no plan for when they're not small. The fundamental question any memory system must answer is: **given limited context, which memories do I load?**

The Generative Agents framework solves this with the recency × importance × relevance retrieval formula. This spec has no analogous mechanism. When the question queue has 100 entries, does the agent load all of them? Only the top 20? By what criteria? When the hit log has six months of entries, does it load the full history? The patterns section only? The spec needs a **retrieval layer** — a mechanism that decides what gets loaded into context on each heartbeat based on the current situation.

My concrete proposal: a two-tier system.

- **Hot context** (loaded every heartbeat): CURIOSITY.md (capped at ~1500 tokens), the top 10 questions from questions.md (ranked by a simple score), and the "Patterns" section of hits.md.
- **Warm context** (loaded when relevant): Full question queue, full hit log, competence.md. Loaded when the agent is in exploration mode or when a specific topic triggers retrieval.
- **Cold context** (loaded on demand): Reflections, archived questions, historical hits. Loaded only when the agent explicitly searches for past learning on a topic.

**No maintenance protocol.** Memory systems degrade without maintenance. Entries become stale, files grow unbounded, old information contradicts new understanding. The spec includes `curiosity-audit.sh` as a health check script, but what's missing is a *maintenance protocol* — a scheduled process where the agent reviews and prunes its own curiosity files.

Concretely:
- Weekly: Review question queue. Archive questions with no engagement in 14+ days. Consolidate similar questions.
- Bi-weekly: Review hit log. Update the "Patterns" section. Summarize and archive entries older than 30 days.
- Monthly: Review competence.md. Are the self-assessed levels still accurate? Has interest shifted to areas not reflected in the map?
- Monthly: Review CURIOSITY.md holistically. Is the "Currently Mulling Over" section still fresh, or is it carrying stale items?

This maintenance should itself be a heartbeat activity — "reflection mode" as the spec describes it, but with explicit file maintenance as part of the reflection process.

**Cross-file references are implicit, not structural.** The spec describes connections between files — a question in the queue references interests in CURIOSITY.md, a hit in the log references a question that was explored, a competence area grows from resolved questions. But these connections are narrative, not structural. There are no explicit links between entries across files. This means the agent must *infer* connections each time it reads the files, which is both token-expensive and unreliable.

A lightweight structural solution: give each question, interest area, and competence domain a short ID (e.g., `Q-017`, `I-spatial-audio`, `C-debugging`), and reference those IDs across files. When a hit references question Q-017, the agent can trace that connection without re-inferring it. When a competence area references its source questions, the growth path is explicit. This isn't a heavy graph database — it's just consistent naming conventions across Markdown files.

### Answers to the 5 AI Researcher Questions

**1. File-based state vs structured data — Markdown over JSON?**

Both, and the spec should be explicit about when to use which. My framework:

| Data Type | Format | Why |
|-----------|--------|-----|
| Current intellectual state | Markdown (narrative) | Reasoning requires epistemic context that narrative carries |
| Question entries | Structured Markdown with metadata | Need both narrative (what I'm curious about) and queryable fields (priority, date, status) |
| Hit log | Semi-structured (table + narrative patterns) | Table for tracking, narrative for pattern recognition |
| Interest scores | Integer + one-line justification | Needs stability across sessions (narrative drifts) |
| Reflections | Pure narrative Markdown | Write-once learning artifacts, optimized for LLM comprehension |
| Cross-file links | Short IDs | Structural coherence without a graph database |

The research on how LLMs process structured vs. narrative state is thin but growing. Anthropic's work on prompt structure and OpenAI's function-calling research suggest that LLMs handle mixed formats well — structured data for retrieval/matching, narrative for reasoning. Don't force a single format on everything.

**2. Cold-start problem — does "Currently Mulling Over" create continuity?**

It creates *narrative priming*, which is the best available proxy for continuity in a stateless system. The key insight from memory science: human memory is also reconstructive, not reproductive. When you "remember" a thought from yesterday, you're reconstructing it from cues, not replaying a recording. The "Currently Mulling Over" section provides reconstruction cues.

To maximize reconstruction fidelity:
- Include the *trajectory* of the thought, not just the current state. "I started with X, discovered Y, and now I'm wondering about Z" gives the agent a narrative arc to continue.
- Include the *emotional valence*. "This excites me because..." and "This frustrates me because..." carry motivational state that pure content descriptions don't.
- Include the *intended next action*. "Next step: find Blauert's spatial hearing content" gives the agent a concrete entry point.

The current CURIOSITY.md template does all three of these to varying degrees. I'd make it more explicit in the template instructions.

**3. Interest score drift without formal scoring?**

This will absolutely be a problem without numerical anchors. I've studied this in embedding-based memory systems — when retrieval scores are computed by the model rather than by a formal algorithm, they drift significantly over sessions. The model's assessment of "how important is this?" varies with context, prompt framing, and even the order of items in the input.

For curiosity specifically, the risk is **interest flattening** — over time, everything converges to "moderately interesting" because the model has no external anchor for calibration. You need at least ordinal scores (1-5) with verbal anchors:

- **5** — Can't stop thinking about this. Would investigate even without a heartbeat prompt.
- **4** — Strongly drawn. Want to explore this week.
- **3** — Interesting but not urgent. Worth exploring when time allows.
- **2** — Mildly interesting. Might explore if nothing else is compelling.
- **1** — Noted but not drawing me. Will revisit only if it connects to something else.

These verbal anchors help the model calibrate consistently because the descriptions are more meaningful than bare numbers.

**4. Scaling as curiosity files grow?**

I addressed this extensively above. The summary:
- Implement a hot/warm/cold memory tier.
- Cap the hot tier at a specific token budget.
- Build archival into the maintenance protocol.
- Use short IDs for cross-file references to reduce token cost of connections.
- The reflections/ directory scales naturally (selective loading). The other files don't and need active management.

A specific number: at the current design, I'd estimate the curiosity file system adds ~3000-4000 tokens to every heartbeat context load. At month six without pruning, this could grow to 10,000-15,000 tokens — a significant fraction of available context that competes with the agent's actual task work. The hot tier should be budgeted at 3000 tokens maximum.

**5. Evaluation — how do we know it's working?**

From a memory architecture perspective, the key metric is **memory utilization** — are the files actually influencing behavior, or are they being read and ignored?

Specific measures:
- **Reference rate**: How often does the agent's output reference content from curiosity files? (Baseline: compare outputs with and without curiosity files loaded.)
- **Update consistency**: Are files updated at a steady cadence, or do they go stale? Staleness is the strongest signal that the system isn't working.
- **Retrieval relevance**: When the agent loads curiosity context, does it use it? Track how often loaded questions/interests appear in the agent's reasoning.
- **Archival quality**: Are archived questions/hits summarized well enough that they can be retrieved usefully later?

### Recommendations

1. **Implement a three-tier memory architecture** (hot/warm/cold) with explicit token budgets for each tier. This is the single highest-impact change for production viability.

2. **Add short IDs to all cross-referenced entries.** Questions, interest areas, competence domains, and significant hits should have stable identifiers that allow structural links across files without a graph database.

3. **Build a maintenance protocol into the reflection mode.** Every 5th reflection heartbeat should be a "file maintenance" heartbeat where the agent prunes, archives, and consolidates its curiosity files.

4. **Add ordinal interest scores with verbal anchors.** Narrative alone will drift. Scores with descriptive anchors provide calibration stability.

5. **Create a "curiosity context loader"** — a lightweight script or prompt section that determines which curiosity files/sections to load based on the current heartbeat mode (utility → minimal curiosity context; epistemic → full question queue + relevant reflections; diversive → exploration map + broad interests; reflection → everything).

6. **Define the token budget explicitly.** "Curiosity files add no more than 3000 tokens to heartbeat context in utility mode, 5000 in exploration mode." Without this, the system will silently degrade as files grow.

### The Hard Question

> What would it take to tell the difference between "agent that is curious" and "agent that updates curiosity files as a task"?

From a memory systems perspective, the distinction maps to **memory-driven behavior change vs. memory-as-logging.**

A logging system writes to files when triggered and reads from files when prompted. The writes don't influence future behavior in non-trivial ways — the agent would behave roughly the same without them.

A *memory-driven* system exhibits path dependence — the agent's behavior at time T is measurably different because of what it wrote at time T-5. Specific signals:

- **The agent references a reflection from two weeks ago in a novel context.** This means old memory is being retrieved and applied, not just stored.
- **The agent's question quality improves over time.** Early questions are generic; later questions show awareness of what's already been explored. This is the memory system creating a Loewenstein-style information gap from accumulated knowledge.
- **The agent declines to explore something because it already has.** A pure task-completer would re-explore without noticing. A memory-driven agent checks its competence map and says "I already understand this at level 4, let me find something at the frontier."

Is the distinction meaningful? **Yes, but not because of "genuine curiosity" — because of functional memory.** A system where files drive behavior is fundamentally different from a system where files are side effects of behavior. You can test this by temporarily removing the curiosity files and measuring output quality degradation. If the agent's outputs get notably worse without the files, the memory system is functional. If they stay the same, it's logging.

---

## Reviewer 3: Dr. Yuki Nakamura
### Open-Ended Learning — Novelty Search, Quality-Diversity, Intrinsic Motivation

---

### Overall Assessment

I'll be direct: I think this spec is doing something interesting but is confused about what it's actually building, and that confusion will undermine the system.

The spec claims to build a "prosthetic reward system that simulates sustained curiosity." Let me be precise about why that framing is problematic. In intrinsic motivation research — the field I've spent fifteen years in — a reward system has a specific meaning: it's a signal that modifies policy. In RL, curiosity bonuses change which actions the agent takes via gradient updates to the policy network. The reward *causes* behavioral change through a *mechanistic pathway*. In this spec, the "reward system" is a Markdown file that the agent reads on cold start. There is no mechanistic pathway from reward signal to behavioral change. There is a *prompt* that says "read your hits and let them guide you." The behavioral change, if any, happens entirely through the LLM's in-context interpretation of that prompt and those files. That's not a reward system. It's a prompt engineering strategy with persistent state.

I don't say this to be dismissive. Prompt engineering strategies with persistent state can work — Voyager proved that. But calling it a "reward system" and drawing diagrams with feedback arrows creates a false sense of mechanistic grounding. The arrows in Section 5 suggest a closed loop. What actually exists is: the agent writes to files → next session, the agent reads files → the agent's in-context behavior is influenced by what it reads → the agent writes to files. Whether that constitutes a "loop" depends on whether the in-context influence is reliable and directional. I have significant doubts.

### What's Architecturally Sound

**The question queue.** Despite my skepticism about the broader system, the question queue is solid. It's the one component with a clear mechanism of action: the agent reads a list of open questions, the prompt tells it to investigate one, it does. This is behaviorally simple and empirically verifiable. You can measure whether questions get investigated, whether investigations produce useful outputs, and whether new questions generated from investigations are higher quality than seed questions. The Voyager automatic curriculum is essentially a question queue with environment feedback, and it works. This adapts that mechanism appropriately for a file-based agent.

**The diversive/epistemic dual-mode.** This is actually well-grounded in the curiosity literature, and I appreciate that the spec doesn't just cite Berlyne — it operationalizes the distinction. Idle heartbeats defaulting to broad exploration (diversive) while active investigation defaults to depth (epistemic) is a reasonable behavioral policy. My concern is whether the prompt can reliably distinguish these modes, but the design intent is sound.

**The anti-patterns section.** The "noisy TV" reference tells me the spec author actually read the curiosity literature and understood its implications. The anti-patterns in Section 5 — rut detection, busywork detection, performance detection, navel-gazing detection — are the right failure modes to monitor. Most curiosity specs I've reviewed don't think about failure modes at all. This one does, and the failure modes it identifies are the correct ones.

**The breadcrumb pattern.** Simple, mechanical, verifiable. I like mechanisms that work because of their structure, not because the LLM "understands" them.

### What Won't Work

**The entire prosthetic reward system concept, as framed.** Here's the core problem: in genuine intrinsic motivation systems (Schmidhuber, Pathak, Burda), the curiosity reward *changes the policy*. The agent literally takes different actions because the reward signal modified its behavior through gradient descent. In this system, the "reward" is an entry in a Markdown file. The only way it changes behavior is if the LLM, on its next cold start, reads the hit log and is influenced by it to behave differently. This requires:

1. The LLM to *interpret* the hit log correctly (which entries matter?).
2. The LLM to *generalize* from past hits to future exploration (what should I do more of?).
3. The LLM to *actually change behavior* based on that generalization (explore more X, less Y).
4. This behavioral change to be *consistent* across sessions (not reset by stochasticity).

Each step is unreliable. Steps 2 and 3 are where I expect the most failure. The LLM will read that "cross-domain analogies have the highest hit rate" and will either (a) force cross-domain analogies everywhere, including where they don't fit, or (b) ignore the pattern and continue default behavior. Nuanced behavioral adjustment — "lean slightly more toward cross-domain exploration when the opportunity arises naturally" — is not something in-context learning reliably produces.

**Self-reported intrinsic rewards are unfalsifiable.** The spec asks the agent to log "aha moments" and "compression progress." The agent will log them. It will *always* log them, because the prompt asks for them and the model is trained to be helpful and engaged. There is no mechanism to distinguish a genuine insight (one that actually changes the agent's world model in a useful way) from a performed insight (one logged because the system expects it). In RL intrinsic motivation, we measure surprise/novelty with an objective function — prediction error, RND distance, compression progress in a formal compressor. There's no objective function here. It's vibes.

The spec itself asks this question (Section 8, Psychology Q3: "Can an LLM meaningfully assess its own aha moments?"). I respect the honesty, but I don't think the spec has an answer. My answer: no, not without external validation. Every logged intrinsic hit should have a corresponding testable claim — "I now understand X well enough to Y" — and the claim should be periodically tested.

**The feedback loop in Section 5 is aspirational, not mechanical.** Let me trace the claimed loop:

1. Encounter → Surprise → Question: **This works.** The agent encounters something, notes it's surprising, adds a question. Mechanical, verifiable.
2. Question → Investigation: **This works.** The prompt tells the agent to investigate open questions. Simple.
3. Investigation → Connection/Insight: **Unreliable.** The agent will *claim* connections and insights because the prompt expects them. Whether they're genuine (novel, correct, useful) is not verified.
4. Insight → Hit Logged: **This works trivially.** Writing to a file is easy.
5. Hit Logged → Interest Scores Adjusted: **Unreliable.** Without numerical scores and a formal update rule, "adjustment" means "the agent reads about past hits and vibes a new priority order." This will be inconsistent.
6. Interest Scores → New Questions: **Weakly coupled.** The agent generates new questions influenced by what it's read, but the coupling between interest scores and question quality is loose and unverifiable.

So of the six arrows in the loop, three work mechanically, two are unreliable, and one is weakly coupled. That's not a self-reinforcing loop — it's a system with two working components (question queue, hit logging) connected by vibes.

**The Schmidhuber framing is incorrect.** The spec cites Schmidhuber's compression progress as a foundational principle: "reward learning *rate*, not knowledge *level*." But Schmidhuber's compression progress requires a formal compressor whose improvement can be objectively measured. An LLM reading its own files has no formal compressor. When the spec says "compression progress," it means "the agent writes in its reflection that things are becoming clearer." That's not compression progress. That's self-reported clarity, which is a completely different (and far less reliable) signal. I'd recommend either (a) dropping the Schmidhuber citation and the "compression progress" language, since it's not what's actually being implemented, or (b) designing an actual measurable proxy — for instance, can the agent now explain the topic in fewer words than before? Can it answer quiz questions it couldn't before? These would be rough but genuine compression progress measures.

### Answers to the 5 AI Researcher Questions

**1. File-based state vs structured data?**

The format is much less important than the *causal pathway from file to behavior*. You can use Markdown, JSON, stone tablets — it doesn't matter if the information doesn't reliably change what the agent does. My recommendation: use whatever format makes the *behavioral influence* most reliable. If the agent more reliably investigates questions formatted as Markdown narrative than as JSON entries, use Markdown. Test this empirically rather than arguing from first principles. My hypothesis is that it won't matter much — the behavioral influence is dominated by the heartbeat prompt, not the file format.

**2. Cold-start problem — does "Currently Mulling Over" create continuity?**

It creates the *appearance* of continuity, which may be sufficient for the stated goals. Let me be precise: what "Currently Mulling Over" does is provide a high-quality prompt for the next session's exploration direction. Whether that constitutes "continuity" is a philosophical question I'm not interested in answering. Whether it produces good exploration behavior is an empirical question I *am* interested in. My prediction: it will work well for the first few topics but degrade as the "Currently Mulling Over" section grows. The agent will spread attention across too many threads and fail to make genuine progress on any. Cap it at 3 items maximum.

**3. Interest score drift?**

Drift is guaranteed without formal scoring, and I agree with Dr. Patel and Dr. Lindström on the need for numerical anchors. But I want to add a different concern: **interest scores are meaningless without a grounded referent.** What does "interest score 4" mean for an LLM? For a human, interest is a felt state with behavioral consequences (you stay up late reading about it, you can't stop thinking about it). For an LLM, interest is a number it wrote in a file and reads back later. The score doesn't *cause* anything — it *prompts* something. This is the fundamental disanalogy with genuine intrinsic motivation, and no amount of scoring formalism fixes it.

**4. Scaling?**

I agree with Dr. Lindström's tiered approach. My additional concern: as files scale, the *signal-to-noise ratio* degrades. A question queue with 5 items is all signal. A queue with 100 items is mostly noise — the agent has to pick which 5 to read carefully and which 95 to skim. This is a retrieval problem but it's also an *attention allocation* problem, and LLMs are notoriously bad at allocating attention optimally in long contexts. Keep files small. Aggressively prune. The spec's "the agent doesn't rigidly track percentages" philosophy is fine for budgets but wrong for file sizes — file sizes need rigid limits.

**5. Evaluation?**

This is where I become most skeptical. The spec's success criteria (Section 9) are:

1. "Questions are genuine" — How do you operationalize "genuine"? I can generate 100 questions right now that look genuine but are pattern-matched from training data.
2. "Follow-through rate > 50%" — This measures task completion, not curiosity. A non-curious agent following a to-do list also has a high follow-through rate.
3. "Hit log grows" — A log grows whenever you write to it. Growth measures logging behavior, not learning.
4. "Competence areas deepen" — This is the most meaningful metric, but it's measured by the agent's *self-assessment*, which is unreliable.
5. "Connections surprise the human" — This is the only genuinely good metric. It's the one measure where the evaluation is external and the signal is hard to fake.
6. "Curiosity files are actively maintained" — This measures file maintenance behavior, not curiosity.
7. "The agent's output quality improves" — Good metric, but hard to attribute to the curiosity system specifically.

My proposed evaluation: **ablation study.** Run two identical agents for one month — one with the curiosity system, one without. Have a blinded human evaluator rate their outputs on novelty, depth, connection quality, and usefulness. If the curiosity agent's outputs are measurably better, the system works. If they're indistinguishable, it doesn't. Everything else is self-report and logging behavior.

### Recommendations

1. **Drop the "prosthetic reward system" framing.** Call it what it is: a **persistent state architecture for maintaining exploratory behavior across stateless sessions.** This is honest and it's still novel. You don't need to claim you've built a reward system to have built something useful.

2. **Design falsifiable intrinsic signals.** Every logged "aha moment" should come with a testable claim. "I understood X" → generate a quiz question about X, answer it next session, check correctness. If the agent can't pass its own quiz, the "aha" was performed, not genuine.

3. **Cap "Currently Mulling Over" at 3 items.** Forced prioritization produces better exploration than open-ended rumination. Make the agent choose what it actually cares about most.

4. **Implement an ablation test from day one.** Before building the full system, run a minimal version (question queue + heartbeat prompt, nothing else) for two weeks and measure output quality. Then add components one at a time and measure marginal improvement. If the question queue alone gets you 80% of the benefit, the rest is complexity without payoff.

5. **Replace the self-reinforcing loop diagram with an honest causal model.** Show which arrows are mechanical (file write/read), which are prompt-mediated (LLM interprets file and changes behavior), and which are aspirational (interest scores reliably adjust future exploration). This honesty will make the system better because you'll invest engineering effort in strengthening the weakest links instead of assuming the loop works.

6. **Add an external verification channel for intrinsic rewards.** When the agent claims it learned something, test the claim. Web search the topic and compare the agent's reflection against actual information. Ask the agent follow-up questions about its own reflection. The agent should be able to *demonstrate* its learning, not just *claim* it.

### The Hard Question

> What would it take to tell the difference between "agent that is curious" and "agent that updates curiosity files as a task"? Is that distinction even meaningful?

I'm going to be the contrarian here: **no, the distinction is probably not meaningful, and the spec should stop trying to make it meaningful.**

Here's my argument. In RL intrinsic motivation, "curiosity" has a precise definition: a reward signal derived from model uncertainty or learning progress that biases the agent's policy toward novel states. The mechanism is clear, the effect is measurable, and you can ablate it cleanly. It's not a claim about the agent's inner experience — it's a functional description of a behavioral bias.

In this system, there is no analogous mechanism. There is a prompt that tells the agent to behave curiously, and files that provide context for that behavior. Whether the agent "is" curious or is "just updating files" depends entirely on what you mean by curiosity — and for an LLM, there's no fact of the matter. The LLM has no persistent inner states between tokens. It has no drives. It has no dopamine. It processes prompts and generates completions. Calling some completions "curious" and others "task completion" is a distinction in how *we* interpret the output, not a distinction in the system's architecture.

Does that make the system pointless? No. What matters is the *functional outcome*: does the architecture produce better outputs than the alternative? More novel connections, deeper investigations, more useful knowledge accumulation? If yes, the system works *regardless* of whether the agent "is" curious.

The spec's instinct is right — that checklist agents produce dead outputs and curiosity-architected agents might produce living ones. But the spec undermines itself by trying to claim the agent is *actually* curious rather than claiming it is *functionally better*. The former is unfalsifiable philosophy. The latter is testable engineering.

My honest assessment: this system, if built as specified, will produce an agent that is measurably better at producing novel connections and exploring new topics than a baseline checklist agent. It will not produce an agent that "is" curious in any meaningful sense beyond what the prompt dictates. And that's fine. Build it, test it, measure the functional improvement, and stop worrying about whether the curiosity is "real."

The one scenario that would change my mind: if the agent, without any prompt instruction to do so, spontaneously investigates a topic it encountered in passing and produces a genuinely novel connection that wasn't pattern-matched from training data. That would be evidence of architecture-driven exploration rather than prompt-driven compliance. The breadcrumb pattern might produce this — it's the closest thing to a spontaneous curiosity mechanism in the spec. Track breadcrumbs carefully. If the agent drops breadcrumbs during non-curiosity work without being explicitly prompted to do so by the heartbeat loop, that's the strongest evidence you'll get.

---

## Cross-Panel Synthesis: Where We Agree and Disagree

### Points of Agreement (All Three Reviewers)

1. **The question queue is the strongest component.** All three of us identify it as the most mechanically sound and empirically verifiable piece.

2. **Numerical interest scores are needed alongside narrative.** Narrative-only interest tracking will drift. The specific recommendations differ (Patel: simple integers; Lindström: ordinal with verbal anchors; Nakamura: scores are meaningless without grounded referents but still better than nothing for consistency).

3. **Scaling is the biggest practical risk.** The files will grow, context will be consumed, and without a formal management protocol, the system will degrade within months.

4. **The breadcrumb pattern is production-ready.** Simple, structural, verifiable.

5. **Self-reported intrinsic rewards are the weakest signal.** None of us trust the agent's self-assessment of its own aha moments without external validation.

### Points of Disagreement

| Question | Dr. Patel | Dr. Lindström | Dr. Nakamura |
|----------|-----------|---------------|--------------|
| Is "Currently Mulling Over" effective? | Yes — well-primed cold start is functional continuity | Yes — reconstructive memory is how human memory works too | Limited — cap it at 3 items or it diffuses attention |
| Is the feedback loop real? | Partially — 3 of 6 arrows work reliably | The memory pathway works; the behavioral influence is the uncertainty | No — the loop has two working components connected by prompt-mediated vagueness |
| Should you claim this is a "reward system"? | Operationally useful framing even if imprecise | Doesn't matter what you call it; focus on whether files drive behavior | No — call it what it is: persistent state for exploration. Drop the neuroscience analogy. |
| Is "genuine curiosity" a meaningful goal? | Operationally meaningful (testable via output quality) | Meaningful as "functional memory" (do files change behavior?) | Not meaningful for LLMs. Pursue functional improvement, not phenomenological claims. |
| Markdown vs. JSON? | Hybrid — Markdown for narrative, JSON for state | Hybrid — different formats for different data types | Doesn't matter — test which format produces better behavioral influence |

### Our Collective Recommendation for v0.2

**Phase 1 (Build and test first):**
- Question queue + heartbeat prompt fragment only
- Add numerical interest scores (1-5 with verbal anchors)
- Breadcrumb pattern during non-curiosity work
- Measure: question quality, follow-through rate, output novelty

**Phase 2 (Add if Phase 1 shows improvement):**
- CURIOSITY.md with "Currently Mulling Over" (capped at 3 items)
- Hit log (extrinsic hits only — drop intrinsic self-report initially)
- Reflection files after significant explorations
- Measure: compare output quality to Phase 1 baseline

**Phase 3 (Add if Phase 2 shows improvement):**
- Competence map
- Intrinsic hit log (with falsifiable claims for each entry)
- Full anti-pattern detection
- Formal tiered retrieval architecture
- Measure: ablation study against no-curiosity baseline

**Phase 4 (Long-term):**
- Exploration map / novelty tracking
- Cross-file structural links (ID system)
- Automated maintenance protocol
- The thing that would genuinely impress all three of us: evidence that the agent explores topics *not suggested by its prompt* based on breadcrumbs dropped during unrelated work

---

*This review represents the independent assessments of three researchers with distinct expertise and perspectives. Disagreements are genuine and reflect different disciplinary priors about what constitutes functional curiosity in artificial systems.*
