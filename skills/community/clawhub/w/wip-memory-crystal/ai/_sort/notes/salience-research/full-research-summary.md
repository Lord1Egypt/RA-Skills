# Linguistic Salience and Memory: Research Summary for AI Agent Architecture

**Date:** 2026-02-20
**Context:** Parker found the EuroSLA salience paper while exploring visual salience to language salience. This research explores how salience frameworks from linguistics and cognitive science can inform Memory Crystal's architecture... specifically the gap between memory capture (works) and spontaneous recall (doesn't work).

---

## 1. What Is Salience? A Working Taxonomy

Salience is the property of a stimulus that makes it stand out, attract attention, and get processed more deeply. Research distinguishes several interacting dimensions:

**Bottom-up (stimulus-driven) salience:** The stimulus itself attracts attention through physical properties. In language: phonological stress, syllable length, sentence position (first-mention advantage), acoustic prominence.

**Top-down (expectation-driven) salience:** Attention directed by prior knowledge, current goals, or recent activation. A stimulus is salient because the perceiver expects it, has been primed for it, or is actively searching for it. Breaks when something violates expectations (surprisal).

**Experiential salience:** A stimulus stands out because of the perceiver's personal history. Prior emotional or motivational associations amplify encoding.

**Key insight for AI memory:** Salience is not a fixed property of information. It emerges from the interaction between the incoming signal, the current context, and the agent's history. This is why a flat vector store with cosine similarity fails at spontaneous recall. It only captures one dimension (semantic similarity) while ignoring context, recency, emotional weight, structural position, and relational importance.

**Source:** [Editorial: Perceptual Linguistic Salience (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5360726/)

---

## 2. The Knell et al. Framework (EuroSLA): Three Levels of Salience

**Paper:** Georgia Knell et al. "Stand-out: A Systematic Review of the Role of Salience in Second Language Acquisition." *Journal of the European Second Language Association* (2025).
**Link:** https://euroslajournal.org/articles/10.22599/jesla.131

After reviewing 42 empirical studies, the authors propose a three-level taxonomy:

### 2a. Perceptual salience (narrow)
Physical properties of the form. Length, stress, position, boundedness, sonority. Longer morphemes get noticed more than shorter ones. Sentence-initial items get an encoding advantage.

### 2b. Psycholinguistic salience (medium)
Relationship between form and linguistic context. When a grammatical marker is semantically redundant (e.g., past tense "-ed" appearing alongside "yesterday"), learners process the meaning word and ignore the morphology. Learners process input for meaning before form.

### 2c. Experiential salience (wide)
Relationship between form and the learner's prior language experience. L1 transfer, frequency of prior exposure, familiarity.

**Finding:** 79% of studies showed positive relationships between higher salience and better learning outcomes.

### Application to agent memory

| Salience Level | Language Acquisition | Agent Memory |
|---|---|---|
| Perceptual | Does the form physically stand out? | Structural position: is this in a header, first message, explicit decision, or buried mid-paragraph? |
| Psycholinguistic | Does context make it redundant? | If the same info exists in 5 places, the agent stops noticing any of them |
| Experiential | Does prior experience make it stand out? | Memories tied to identity or recent work should be more salient than generic tasks |

---

## 3. Nick Ellis: Blocking, Overshadowing, and Learned Attention

**Researcher:** Nick C. Ellis, University of Michigan

Three critical phenomena from associative learning:

**Blocking:** When a reliable cue (e.g., "yesterday") is already learned, it blocks acquisition of a less salient cue that predicts the same thing (e.g., "-ed"). The learner already has a working solution, so the redundant cue gets no associative weight. Not laziness... optimal resource allocation given bounded attention.

**Overshadowing:** When two cues are presented simultaneously, the more salient one captures more associative strength. The less salient cue is "overshadowed" even though it's equally informative.

**Learned attention:** Prior experience tunes what you attend to. Chinese speakers (L1 lacks tense morphology) were less able to acquire English tense markers than Spanish/Russian speakers (rich morphology). Prior attentional habits transfer.

**His core claim:** "What we attend to is determined by our prior experience, and salience is as much a psychological as a physical property."

### Application to agent memory

- **Blocking:** If the agent has a "good enough" summary, it may never encode the richer original. The summary blocks deeper processing.
- **Overshadowing:** Dramatic emotional exchanges overshadow quiet but important technical decisions in encoding.
- **Learned attention:** An agent primarily asked about scheduling develops attentional biases toward temporal information, under-encoding other facts.
- **Implication:** A memory system needs anti-blocking mechanisms. Redundancy should trigger comparison, not dismissal.

**Sources:**
- [Blocking and Learned Attention in Language Acquisition](https://sites.lsa.umich.edu/nickellis-new/wp-content/uploads/sites/1284/2021/07/pp400-ellis.pdf)
- [Selective Attention and Transfer in L2 Acquisition (Oxford Academic)](https://academic.oup.com/applij/article-abstract/27/2/164/185787)

---

## 4. The Rescorla-Wagner Model: Computational Salience Through Prediction Error

**Model:** Rescorla & Wagner (1972). Foundational mathematical model of associative learning.

Learning occurs proportionally to **surprise**. Change in associative strength depends on:
- **Alpha (salience of the cue):** intrinsic property of the stimulus
- **Beta (salience of the outcome):** how strong the unconditioned stimulus is
- **Prediction error:** difference between expected and actual outcomes. Learning is maximal when the outcome is unexpected.

When multiple cues are present, their combined associative strengths determine the prediction error. This creates cue competition. If cue A already predicts the outcome well, adding cue B produces no surprise, so B gains no associative weight. This is the formal mechanism behind blocking.

**Extensions:** The CompAct model adds dynamic attention allocation. Features compete for attention. A "familiarity principle" reduces attention to repeatedly observed, unreinforced cues.

### Application to agent memory
- **Prediction error as a signal:** Information that surprises the agent (contradicts existing memories, introduces genuinely new facts) should receive higher encoding priority
- **Cue competition:** Multiple pieces of information in a conversation turn should compete for encoding weight. Not everything deserves equal allocation
- **Decay of attention to familiar stimuli:** Repeatedly encountered, unchanged information should receive declining encoding weight

**Source:** [Rescorla-Wagner Model (Wikipedia)](https://en.wikipedia.org/wiki/Rescorla%E2%80%93Wagner_model)

---

## 5. Emotional Salience and Memory Consolidation

Memory is a selective system biased toward motivationally significant information.

- Emotionally salient experiences trigger norepinephrine surges that create "hotspots" of long-term potentiation. Emotional events don't just get remembered better... they **enhance encoding of temporally adjacent mundane information** through graded prioritization.

- Intentional instruction to remember ("this is important") can compete with and sometimes override emotional salience. Top-down goals modulate consolidation.

- During sleep consolidation, salient experiences are preferentially reactivated. Multiple salience cues compete for dominance.

### Application to agent memory
- **Salience contagion:** Important events should boost encoding weight of temporally adjacent memories
- **Explicit importance marking:** When the user says "remember this," that overrides default encoding weights
- **Consolidation phase:** Periodic "sleep-like" process reactivating high-salience memories while low-salience ones decay. This is what compaction should be, guided by salience not just recency.

**Source:** [Salient experiences enhance mundane memories (Science Advances)](https://www.science.org/doi/10.1126/sciadv.ady1704)

---

## 6. Spontaneous Retrieval and Spreading Activation

Spontaneous retrieval (memories surfacing without deliberate search) relies on associative processes, not executive search. Mediated by hippocampus, triggered by contextual overlap between current situation and encoded memory.

- **Spreading activation:** Accessing one concept automatically activates related concepts. Activation spreads along associative links, decaying over distance.
- **Context-dependent memory:** Memories retrieved more easily when retrieval context matches encoding context (encoding specificity principle).
- **Involuntary autobiographical memories:** Surface without conscious search, triggered by environmental cues that overlap with encoded features. Less cognitively demanding than deliberate recall.

### Application to agent memory
This is the missing piece. The agent has 150K+ chunks but no spreading activation. When processing a new message, the agent should:
1. Activate nodes that semantically match current input
2. Propagate activation along relational links to associated memories
3. Surface memories exceeding an activation threshold, even without direct query match

Without this, the agent can only retrieve what it explicitly searches for.

**Source:** [Contextually Mediated Spontaneous Retrieval (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5789776/)

---

## 7. Computational Architectures Applying These Principles

### 7a. SYNAPSE (2025): Spreading Activation for LLM Agents

**Paper:** "SYNAPSE: Empowering LLM Agents with Episodic-Semantic Memory via Spreading Activation"
**Link:** https://arxiv.org/abs/2601.02744

Unified graph with episodic nodes (specific interactions) and semantic nodes (abstract concepts). Three edge types: temporal, abstraction, association. Activation propagates with fan effect (dilution), lateral inhibition (winner-take-all), and temporal decay. Final scoring fuses semantic similarity + graph activation + PageRank importance.

Includes "feeling of knowing" gate: refuses to answer when confidence is low rather than hallucinating.

**Results:** 40.5 F1 on LoCoMo (outperforms A-Mem by 7.2 points). 23% improvement in multi-hop reasoning. 95% token reduction vs. full-context.

**Most directly applicable architecture to our problem.**

### 7b. ACT-R-Inspired Memory (2025)

**Paper:** "Human-Like Remembering and Forgetting in LLM Agents"
**Link:** https://dl.acm.org/doi/10.1145/3765766.3765803

Implements ACT-R declarative memory equations. Each chunk has activation from:
- Base-level activation (frequency + recency with temporal decay)
- Spreading activation (contextual relevance via cosine similarity)
- Stochastic noise (Gaussian variability)

A chunk is recalled only if total activation exceeds retrieval threshold. Naturally models both remembering and forgetting.

**Activation formula:** `Activation = BLA(frequency, recency) + SpreadingActivation(context) + Noise`

Could replace or augment pure cosine similarity in Memory Crystal.

### 7c. A-Mem (2025): Zettelkasten-Inspired Agentic Memory

**Paper:** "A-Mem: Agentic Memory for LLM Agents"
**Link:** https://arxiv.org/html/2502.12110v1

Each memory note: original content, timestamp, LLM-generated keywords, tags, contextual descriptions, embeddings, and links. New memories trigger updates to contextual representations of related existing memories. Enables higher-order pattern emergence.

**Key feature:** Memory evolution. New experiences modify representations of related existing memories (analogous to reconsolidation in neuroscience).

### 7d. Agent Cognitive Compressor (ACC) (2025)

**Paper:** "AI Agents Need Memory Control Over More Context"
**Link:** https://arxiv.org/html/2601.11653

Replaces transcript accumulation with bounded Compressed Cognitive State (CCS). Typed fields: episodic trace, semantic gist, focal entities, relational map, goal orientation, constraints, predictive cues, uncertainty signals. Retrieved evidence merely proposes information; only decision-critical content enters through a qualification gate.

**Addresses opposite failure mode:** Where Crystal captures everything and fails at recall, ACC argues for aggressive compression and curation at write time.

### 7e. Salience Maps in Computational Neuroscience

**Paper:** Veale et al. (2020). "Salience Models: A Computational Cognitive Neuroscience Review"
**Link:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6969943/

Extract features in parallel, apply center-surround filtering (what stands out relative to surroundings), normalize via competition, generate salience map. Includes lateral inhibition and inhibition of return.

**Key principle:** A memory is salient not because of absolute properties but because it contrasts with its surroundings. A quiet technical decision in a conversation full of small talk is salient precisely because it differs.

---

## 8. Synthesis: Seven Principles for Salience-Aware Agent Memory

### Principle 1: Salience is multi-dimensional
Compute from at least three independent dimensions: structural (position, explicitness), contextual (uniqueness, contrast), experiential (frequency, recency, personal relevance).

### Principle 2: Prediction error drives encoding priority
Information that surprises should get higher encoding weight. The current system gives equal weight to everything.

### Principle 3: Retrieval needs spreading activation
A graph with lateral connections enables spontaneous surfacing. Flat vector stores can only answer "what is similar to X?" not "what is related through causal, temporal, or structural connections?"

### Principle 4: Blocking is the enemy
Once the agent has a "good enough" summary, it stops encoding deeper representations. Redundancy should trigger comparison, not dismissal.

### Principle 5: Temporal decay with reactivation
Every memory should have activation that decays with time but increases with each access. Unused memories fall below threshold. Frequently accessed ones stay available.

### Principle 6: Salience contagion
Important events boost encoding of temporally adjacent information. Critical decisions elevate surrounding context.

### Principle 7: Consolidation needs a "sleep" phase
Periodic offline reprocessing that reactivates high-salience memories and lets low-salience ones decay. Compaction guided by salience, not just recency.

---

## Connection to "Attention Is All You Need"

The Transformer's attention mechanism IS salience computation within the context window. Every attention head computes "what stands out given this query." But it only works on tokens currently in context.

The memory problem is: **how do you extend attention beyond the context window?** All the architectures above (ACT-R, SYNAPSE, A-Mem) are different answers. They build the salience layer that Transformers can't do alone... deciding what deserves to enter the window before the model ever sees it.

Schmidt's Noticing Hypothesis maps here: you can't learn what you don't notice. Transformers can't attend to what isn't in context. Same constraint, different framing.

---

## All Sources

### Core Papers
- [Stand-out: Salience in SLA (EuroSLA)](https://euroslajournal.org/articles/10.22599/jesla.131)
- [SYNAPSE: Spreading Activation for LLM Agents (arXiv)](https://arxiv.org/abs/2601.02744)
- [ACT-R-Inspired Memory Architecture (ACM)](https://dl.acm.org/doi/10.1145/3765766.3765803)
- [A-Mem: Agentic Memory (arXiv)](https://arxiv.org/html/2502.12110v1)
- [Agent Cognitive Compressor (arXiv)](https://arxiv.org/html/2601.11653)
- [Salient experiences enhance mundane memories (Science Advances)](https://www.science.org/doi/10.1126/sciadv.ady1704)

### Salience Frameworks
- [Editorial: Perceptual Linguistic Salience (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5360726/)
- [What is Salience? (De Gruyter)](https://www.degruyterbrill.com/document/doi/10.1515/opli-2020-0042/html)
- [Attention and Salience (Oxford Bibliographies)](https://www.oxfordbibliographies.com/display/document/obo-9780199772810/obo-9780199772810-0324.xml)
- [Salience Models: Computational Neuroscience Review (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6969943/)

### Associative Learning
- [Blocking and Learned Attention (Nick Ellis)](https://sites.lsa.umich.edu/nickellis-new/wp-content/uploads/sites/1284/2021/07/pp400-ellis.pdf)
- [Selective Attention and Transfer in L2 (Oxford Academic)](https://academic.oup.com/applij/article-abstract/27/2/164/185787)
- [Rescorla-Wagner Model (Wikipedia)](https://en.wikipedia.org/wiki/Rescorla%E2%80%93Wagner_model)

### Memory and Retrieval
- [Contextually Mediated Spontaneous Retrieval (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5789776/)
- [Survival of the salient: Emotion rescues memories (bioRxiv)](https://www.biorxiv.org/content/10.1101/2020.07.07.192252v1.full)
- [Neural dynamics of spontaneous memory recall (Nature Comms)](https://www.nature.com/articles/s41467-025-61807-w)

### Agent Memory Surveys
- [Memory in the Age of AI Agents: Paper List (GitHub)](https://github.com/Shichun-Liu/Agent-Memory-Paper-List)
- [Memory Mechanisms in LLM Agents (EmergentMind)](https://www.emergentmind.com/topics/memory-mechanisms-in-llm-based-agents)
- [ICLR 2026 Workshop: MemAgents (OpenReview)](https://openreview.net/pdf?id=U51WxL382H)
- [CAIM: Cognitive AI Memory Framework (arXiv)](https://arxiv.org/abs/2505.13044)

---

*Compiled 2026-02-20 by Claude Code. Research initiated by Parker's discovery of the EuroSLA salience framework.*
