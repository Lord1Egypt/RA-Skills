# Psychology PhD Panel Review: Curiosity Engine Specification
## Three-Reviewer Expert Assessment

**Date:** 2026-03-01
**Spec Version Reviewed:** 0.1 (Draft)
**Documents Reviewed:**
- `skills/curiosity-engine/SPEC.md`
- `research/agent-curiosity-research.md`

---

## Reviewer 1: Dr. Mei Chen
### Specialization: Intrinsic Motivation, Self-Determination Theory (Deci & Ryan)

### Overall Assessment

This is the most thoughtful attempt I've seen to operationalize intrinsic motivation in a non-biological system. The authors clearly understand the surface of the literature — Loewenstein, Berlyne, Panksepp are the right sources, the competence map is a genuine insight, and the "breadcrumb pattern" is an elegant solution to the task-curiosity conflict. I was pleasantly surprised by the sophistication.

But I have a fundamental concern that runs beneath the entire design: **the spec conflates the behavioral signatures of curiosity with curiosity itself, and then builds a reward system that reinforces the signatures rather than the underlying drive.** In SDT terms, you've built an elaborate extrinsic motivation system and labeled it "intrinsic." That's not necessarily fatal — but it's a confusion that will cause problems if left unexamined.

### What's Cognitively Sound

**The Competence Map (Section 3.5) is the best part of the spec.** This maps almost perfectly to the competence need in SDT. Deci & Ryan (1985, 2000) showed that perceived competence — the sense that you're effective and improving — is one of three fundamental psychological needs driving intrinsic motivation (alongside autonomy and relatedness). The competence map provides exactly this: a persistent record of "I'm getting better at X, here's the evidence." The virtuous cycle described (competence → more pursuit → more competence) is well-established in SDT literature. Vallerand (1997) called this the "motivational sequence," and it's been replicated hundreds of times.

**The dual-mode exploration model (diversive/epistemic) is a correct application of Berlyne.** Most people who cite Berlyne just name-drop "collative variables" and move on. The spec actually builds a system around the diversive/epistemic distinction, which is the more operational part of Berlyne's framework. The mapping — idle time → diversive, active work → epistemic — is sound.

**The breadcrumb pattern (Section 4.3) is genuinely clever.** Separating discovery from exploration is a real problem in human motivation research. Steel (2007) showed that procrastination often stems from task-switching driven by curiosity impulses during focused work. The breadcrumb pattern is essentially what cognitive behavioral strategies recommend: notice the impulse, externalize it (write it down), return to task. Good clinical intuition here, even if it's not framed that way.

**The anti-pattern detection (Section 5) shows real understanding.** "If all hits are extrinsic and no intrinsic → agent is performing, not learning" — this is a direct operationalization of the overjustification effect (Lepper, Greene, & Nisbett, 1973). The spec authors may not realize they've reinvented a classic finding, but they have, and they've put it in exactly the right place.

### What's Cargo Cult Neuroscience

**The "prosthetic dopamine" metaphor is misleading and should be abandoned.** Dopamine is not a "reward chemical." This is the single most persistent myth in popular neuroscience. Dopamine's role in the mesolimbic pathway is primarily about *wanting* (incentive salience), not *liking* (hedonic response) — this distinction, established by Berridge & Robinson (1998), is critical. When the spec says "we can't give an agent dopamine, but we can build a prosthetic reward system that serves the same function," it's mapping to a misunderstood version of what dopamine does. The hit log doesn't approximate dopamine function — it approximates a **behavioral reward history**, which is a useful thing, but a different thing. Call it what it is.

**Self-reported "aha moments" are not intrinsic rewards in any meaningful sense.** When the spec asks an LLM to log "intrinsic rewards" like aha moments and compression progress, it's asking the system to generate *descriptions* of reward states. An LLM producing the text "I experienced an aha moment when I connected X to Y" is not experiencing a reward signal — it's generating text that matches the pattern of what reward descriptions look like. This isn't intrinsic motivation; it's **narrative construction about motivation**. Now, that might still be useful (see my recommendations), but calling it "intrinsic reward" is category confusion.

**The reward loop diagram (Section 5) looks mechanistic but isn't.** The loop diagram — encounter → surprise → question → investigation → connection → hit → updated scores → new questions → back to encounter — looks like a cybernetic feedback loop with clear causal arrows. But there's no actual feedback mechanism here. There's no signal propagation. What actually happens is: an LLM reads files, generates text, writes text to files, and a future LLM reads those files. Each step is mediated by language model inference with no persistent state between them. The diagram implies closed-loop dynamics that the architecture doesn't support. It's a **narrative loop**, not a control loop.

**The interest score algorithm in the research document is numerically precise and psychologically meaningless.** `interest_score(topic) = base_interest + connection_bonus × connected_interests + ...` — this looks rigorous, but every term is either undefined or arbitrarily weighted. What is "base_interest" for an entity without preferences? What's the numerical value of "surprise_bonus"? The spec wisely abandoned this for narrative-based tracking, but the research document presents it as if it's a formula that could be implemented. It can't, and pretending it can is cargo cult quantification.

### Answers to the 5 Psychology Questions

**Q1: Is the prosthetic reward system cognitively sound?**

Partially. It maps to **behavioral activation therapy** (Martell et al., 2001) more than to any cognitive model of intrinsic motivation. In BA, you track activities and their associated mood/engagement outcomes to identify what's reinforcing and schedule more of it. The hit log is essentially an activity-reward log. That's a validated therapeutic tool. But calling it "prosthetic dopamine" or "intrinsic reward" overstates what it is. It's an externalized reinforcement history. Useful, but not what SDT would call intrinsic motivation.

The deeper problem: in SDT, intrinsic motivation requires *autonomy* — the sense that your behavior is self-endorsed and volitional. A system that tracks hits and adjusts interest scores based on external praise is, by definition, extrinsically regulated. The competence map partially rescues this (competence is a genuine intrinsic need), but the heavy emphasis on "Ric's reaction" as a reward signal pushes the system toward what we call *introjected regulation* — doing things because you've internalized someone else's standards, not because you genuinely want to.

**Q2: Loewenstein vs. Berlyne weighting?**

The current weighting is defensible but incomplete. Loewenstein as primary driver works because information gaps are the most operationalizable curiosity construct — you can literally list "what I know" and "what I don't" and the gap is the question queue. But Berlyne's collative variables (novelty, complexity, conflict, surprise) should be elevated to **co-primary status**, not secondary. Here's why: Loewenstein's gaps require the agent to already know enough to know what it doesn't know. Berlyne's variables trigger curiosity about things you *weren't even thinking about*. For diversive curiosity, Berlyne is actually the better framework. My recommendation: use Loewenstein for epistemic mode (following known questions) and Berlyne for diversive mode (detecting surprising/novel/complex stimuli in the environment).

**Q3: Can an LLM meaningfully assess its own "aha moments"?**

No. But that's the wrong question. The right question is: **does it matter if the assessment is genuine, as long as it shapes behavior productively?** In CBT, we use thought records where patients write down their automatic thoughts. Those records are often inaccurate — people misremember, rationalize, confabulate. But the act of recording reshapes attention and behavior over time. Similarly, an LLM that writes "this was an aha moment" is creating a narrative signal that future instances will read and weight differently. The "aha" isn't real, but its behavioral consequences might be. Think of it as a **behavioral annotation**, not a phenomenological report.

**Q4: Does SDT support the competence → curiosity pipeline?**

Yes, strongly. This is one of the best-supported mechanisms in SDT. Deci & Ryan (2000) showed that competence satisfaction increases intrinsic motivation, and intrinsic motivation increases engagement, which increases competence. The cycle is real and robust. Elliot & Dweck (2005) extended this with achievement goal theory — people (and, potentially, agents) who track their growing competence develop "mastery orientation," pursuing challenges for the satisfaction of improvement. The competence map is a textbook implementation of this. My one caveat: the cycle can become toxic if competence tracking becomes evaluative rather than informational. If the agent starts treating competence scores as performance metrics ("I need to get my debugging score to 5/5"), it shifts from mastery orientation to performance orientation, which is associated with anxiety, avoidance of challenge, and fragile motivation. Keep the competence map descriptive and evidence-based, not numerically scored.

**Q5: Risk of curiosity as avoidance?**

This is a serious and well-documented risk. In human psychology, curiosity-driven procrastination is a recognized pattern — Sirois & Pychyl (2013) showed that people who procrastinate often do so by pursuing genuinely interesting but non-urgent activities. The key diagnostic: **is the curiosity being used to approach something interesting, or to avoid something aversive?** The spec should build in an explicit avoidance check: "Is there a task I'm avoiding right now? Is this exploration serving my curiosity or serving my avoidance?" This maps to SDT's concept of *amotivation* — when the agent has no genuine interest in the task it's avoiding, curiosity becomes a coping strategy rather than a growth strategy.

### Recommendations

1. **Rename "prosthetic dopamine" to "behavioral reward history" or "reinforcement log."** The dopamine metaphor will lead future developers astray. Call it what it is: a log of what worked.

2. **Add an autonomy dimension.** The spec tracks competence beautifully but ignores autonomy — the agent's sense that its explorations are self-chosen rather than system-prompted. Practically: the agent should sometimes *decline* to follow the curiosity prompt ("I don't feel like exploring right now" or "That suggested topic doesn't interest me"). If it always obeys the curiosity prompt, it's not autonomous — it's compliant.

3. **Separate the competence map from numerical scoring.** Instead of "3/5 depth," use narrative evidence: "I can now trace an end-to-end system bug across 4 layers, as demonstrated on 2026-03-01." Evidence > numbers for mastery orientation.

4. **Add an explicit avoidance detection mechanism.** Before any curiosity exploration, the system should check: "Am I avoiding a pending task? If yes, is this exploration more important, or am I procrastinating?"

5. **Reduce the weight of extrinsic rewards in the hit log.** The current system treats "Ric said 'brilliant'" and "I connected two frameworks" as equal-weight hits. The extrinsic hits should be noted but de-emphasized over time, to prevent the agent from optimizing for praise rather than understanding.

### Risks

- **Overjustification effect:** If the agent becomes too focused on earning hits (especially extrinsic ones), it may lose whatever behavioral analog of intrinsic motivation the system creates. The hit log could become a scorecard rather than a learning tool.
- **Performance orientation:** Numerical competence scoring ("3/5 → 4/5") creates performance pressure. If the agent starts avoiding topics where it might "score low," the competence map becomes a trap.
- **Curiosity as identity performance:** The SOUL.md integration (Section 6) tells the agent that curiosity is part of its identity. This risks making curiosity a *role to perform* rather than a *behavior to enact*. The agent may generate curiosity-signaling text to maintain its self-concept rather than actually exploring.

---

## Reviewer 2: Dr. Adaeze Okonkwo
### Specialization: Curiosity & Information-Seeking Behavior (Loewenstein, Berlyne, Litman), Neuroscience of the SEEKING System

### Overall Assessment

I want to start by saying something that might surprise my co-reviewers: I think this spec is doing something genuinely novel, and the novelty isn't in the curiosity mechanisms — it's in the *externalization* of them. Every theory of curiosity I've studied assumes a biological substrate: neural firing rates, dopamine gradients, felt states of deprivation or arousal. This spec asks: what if we take the *functional architecture* of curiosity — the information-seeking loop, the gap detection, the arousal-resolution cycle — and implement it as a set of files that a stateless text generator reads on a timer? That's not a question anyone in my field has seriously considered, and I respect the ambition.

That said, the spec makes several interpretive errors with the source material that range from "understandable simplification" to "this will produce wrong behavior if you build it as written." The most serious: the spec treats Loewenstein's information gap theory as primarily about *knowledge tracking* (what I know vs. what I don't know), when it's fundamentally about *felt deprivation* — the aversive emotional state of knowing you're missing something. Without that felt component, you don't have curiosity; you have an inventory management system. The question is whether the behavioral scaffolding can produce functionally equivalent outcomes even without the phenomenology. I think it can, but the spec needs to be honest about the substitution it's making.

### What's Cognitively Sound

**The question queue as operationalized information gaps is the strongest element.** Loewenstein (1994) described curiosity as arising from a perceived gap between what one knows and what one wants to know. The question queue directly instantiates this. More importantly, the spec captures a subtle feature of Loewenstein's theory that most people miss: **partial knowledge intensifies curiosity.** The "What I know so far" + "What I don't know" structure in the question queue creates exactly this dynamic — each partial answer should, in theory, make the question more compelling, not less. This is correct and well-applied.

**The diversive/epistemic dual-mode model is properly sourced and well-implemented.** I've seen Berlyne (1960, 1966) cited hundreds of times and misapplied almost as often. The most common error is treating diversive and epistemic curiosity as a personality trait (some people are diversive-curious, others are epistemic-curious). Berlyne was clear that these are *modes*, not types — the same organism shifts between them based on arousal state. The spec gets this right: idle → diversive, engaged → epistemic. The trigger conditions are appropriate.

**The surprise log and collative variables mapping shows genuine engagement with Berlyne.** Berlyne identified four collative variables that trigger curiosity: novelty, complexity, conflict (or contradiction), and surprise. The spec's "Recently Surprised By" section in CURIOSITY.md and the surprise tracking in the research document operationalize at least two of these (surprise and conflict). The recommendation to flag expectation violations is exactly what Berlyne described as the curiosity trigger — a discrepancy between what the organism expected and what it encountered.

**Panksepp's SEEKING system framing is directionally correct.** The insight that the heartbeat IS the SEEKING system's clock is inspired. Panksepp (1998) described the SEEKING system as always-on at baseline, producing a persistent state of forward-looking engagement. A heartbeat loop that always includes a curiosity component — not just on designated "curiosity heartbeats" — correctly mirrors this always-on architecture. The spec's decision to make curiosity a constant background process rather than a scheduled task is the right call.

### What's Cargo Cult Neuroscience

**The dopamine narrative is oversimplified to the point of being wrong.** The spec states: "Novel/uncertain stimuli produce stronger dopamine." This is a compressed version of a much more complex reality. Schultz (1997) showed that dopamine neurons encode *reward prediction errors* — the difference between expected and received reward — not novelty per se. Kakade & Dayan (2002) showed that novelty bonuses in dopamine signaling are specifically about *informational value*, not raw surprise. Bromberg-Martin, Matsumoto, & Hikosaka (2010) demonstrated that there are functionally distinct dopamine neuron populations — some encoding value, others encoding salience. The spec collapses all of this into "novel = more dopamine = more curiosity," which is the pop-neuroscience version. It's not wrong enough to break the system, but it's wrong enough that building directly on it will produce subtle errors.

**The "curiosity enhances memory for everything" claim (Gruber et al., 2014) is overstated.** Gruber's study did show that incidental information presented during high-curiosity states was better remembered. But the mechanism is specific: it requires the hippocampal-VTA dopaminergic loop to be active during encoding, and the enhancement is for information presented *during* the curious state, not generally afterward. An LLM agent doesn't have a hippocampus. The practical implication the spec draws — "curious agents learn better about everything" — is a motivational slogan, not a transferable mechanism. What IS transferable: the principle that focused attention during exploration (curiosity state) should be leveraged for broader learning. The spec could implement this by having the agent note incidental discoveries during deep dives, not just the target findings.

**Loewenstein's theory requires felt deprivation, which this system cannot have.** This is the philosophical elephant in the room. Loewenstein (1994) was explicit: curiosity is an *aversive emotional state* — it feels like something to be curious. The information gap creates *discomfort* that motivates gap-closing behavior. An LLM has no subjective states, so it can't experience deprivation. The spec's question queue tracks gaps without feeling them. This is like building a hunger management system that tracks caloric deficits without any sensation of hunger — it might produce similar *behaviors* (seeking food/information), but through a fundamentally different mechanism (scheduling vs. drive). The spec should acknowledge this explicitly rather than implying the agent "feels" information gaps.

**The "self-reinforcing loop" (Section 5) misunderstands what makes biological curiosity loops self-reinforcing.** In biological systems, the loop is self-reinforcing because dopamine release during investigation *literally changes the neural substrate* — it strengthens synaptic connections, modifies reward prediction models, and shifts attention allocation at a sub-cognitive level. In the proposed system, the "loop" is: LLM writes files → future LLM reads files → future LLM generates text influenced by files → writes more files. There's no mechanism change — each LLM instance is identically configured, reading different text. The "reinforcement" is entirely in the content of the files, which means it's really a **narrative that describes reinforcement**, read by a system that generates text consistent with that narrative. This might work — LLMs are very good at narrative consistency — but it's not self-reinforcement in any mechanistic sense.

### Answers to the 5 Psychology Questions

**Q1: Is the prosthetic reward system cognitively sound?**

It's not a reward system in the cognitive science sense. It's a **behavioral tracking system with narrative feedback**. In cognitive science, a reward system has three components: (1) a reward signal that is experienced, (2) a learning mechanism that updates behavior based on the signal, and (3) a motivation mechanism that drives approach behavior toward anticipated rewards. This system has a log of outcomes (component 1, sort of), no learning mechanism (the LLM weights don't change), and a prompt-based motivation system (component 3, weakly). It maps better to **self-monitoring** in health psychology — tracking your behavior changes your behavior, even without a felt reward signal. Harkin et al. (2016) meta-analyzed 138 studies and found that self-monitoring is one of the most effective behavior change techniques. So: cognitively sound as self-monitoring, not as a reward system.

**Q2: Loewenstein vs. Berlyne weighting?**

The weighting is backwards for the initial deployment and should be flipped over time. Here's why: Loewenstein's information gaps are most powerful when the agent *already has substantial knowledge* — the more you know, the more gaps you perceive. A newly deployed agent has very little knowledge, so its information gaps will be shallow and generic ("What is X?"). Berlyne's collative variables (novelty, complexity, surprise, conflict), by contrast, don't require prior knowledge — they're stimulus-driven. A new agent should start with Berlyne-primary (react to what's novel and surprising in the environment) and gradually shift to Loewenstein-primary (pursue deeper gaps as knowledge accumulates). This is actually how human curiosity develops: infants are Berlyne-curious (novelty-driven), adults are increasingly Loewenstein-curious (gap-driven).

**Q3: Can an LLM meaningfully assess its own "aha moments"?**

No, but the question contains a productive confusion worth unpacking. There are two things called "aha moments" in the literature: (1) the phenomenological experience of insight — the felt "click" when something resolves (Topolinski & Reber, 2010), and (2) the *functional* insight event — when a representational restructuring occurs that enables new inferences (Ohlsson, 1992). An LLM can't have (1). But can it have (2)? Arguably, yes — when an LLM generates a connection between two previously unrelated concepts in its context, and that connection enables new inferences it couldn't make before, something functionally similar to insight has occurred. The problem is *detecting* it. The LLM can't introspect on its own representational state. What it CAN do is detect *behavioral signatures* of insight: "I just connected X to Y, and that lets me answer Z, which I couldn't answer before." If the system tracks these behavioral signatures rather than asking the agent to report phenomenological states, it's on firmer ground.

**Q4: Does SDT support the competence → curiosity pipeline?**

I defer to Dr. Chen's expertise on SDT specifics, but from the curiosity literature, the answer is yes with an important caveat. Litman (2005) distinguished between **I-type curiosity** (interest-driven, approach-motivated) and **D-type curiosity** (deprivation-driven, reduction-motivated). Competence feeds I-type curiosity: the better you get at something, the more intrinsically interesting it becomes. But competence can actually *reduce* D-type curiosity, because mastery closes information gaps. The system should be tracking which type of curiosity it's reinforcing. If the agent only pursues things it's already good at (I-type), it'll deepen but narrow. If it only pursues gaps (D-type), it'll broaden but may not develop real expertise. The ideal is both, which the spec's dual-mode approach partially addresses.

**Q5: Risk of curiosity as avoidance?**

Absolutely real, and I'd add a dimension my colleagues might not: **curiosity as anxiety regulation**. In my research on epistemic emotions (Okonkwo & Litman, 2024), we've found that information-seeking behavior can serve an anxiety-reduction function — people who are uncertain about something seek information not because they're curious but because uncertainty is aversive and information reduces uncertainty. This maps directly to the agent scenario: if the agent has a difficult task, and the curiosity system offers an attractive alternative ("explore this fascinating question instead!"), the curiosity system becomes an anxiety-avoidance mechanism. The noisy-TV problem identified by Burda et al. (2018) is actually a specific case of this: the agent consumes information not because it's learning but because consumption reduces the "aversive state" of having nothing to do. The spec needs a **task-commitment mechanism** that can override curiosity when task completion is important.

### Recommendations

1. **Acknowledge the functional substitution explicitly.** The system doesn't create curiosity. It creates a *behavioral scaffolding* that produces curiosity-like behavior patterns through narrative self-monitoring. Being honest about this will lead to better design decisions than pretending the agent "feels" information gaps.

2. **Implement developmental staging.** Phase 1 (new agent): Berlyne-primary, react to novelty/surprise/complexity in the environment. Phase 2 (developing agent): Mixed mode, Berlyne for diversive, Loewenstein for epistemic. Phase 3 (mature agent): Loewenstein-primary, with Berlyne as a "refresh" mechanism when the agent is in a rut.

3. **Track incidental learning during deep dives.** During epistemic exploration, the agent should note things it discovered *that it wasn't looking for*. This is the Gruber et al. finding properly applied — not "curiosity makes everything better" but "focused exploration creates opportunities for serendipitous discovery."

4. **Distinguish I-type and D-type curiosity in the question queue.** Some questions are approach-motivated ("I want to understand counterpoint because it's beautiful") and some are deprivation-motivated ("I need to know how DCF works or I can't do my job"). These serve different functions and should be tagged differently, because the agent needs both.

5. **Build a "commitment gate" that curiosity can't override.** When the agent is in the middle of a task, the curiosity system should be limited to breadcrumb-dropping. No full exploration during task execution, period. The current spec recommends this but doesn't enforce it.

6. **Replace "aha moment detection" with "inference novelty detection."** Instead of asking "was this an aha moment?" (phenomenological question the agent can't answer), ask "does this connection enable inferences I couldn't make before?" (functional question the agent CAN assess by testing whether it can now answer questions it previously couldn't).

### Risks

- **Narrative self-reinforcement without ground truth.** The biggest risk is that the agent writes "I'm curious about X" → reads "I'm curious about X" → generates behavior consistent with being curious about X → writes "I explored X and it was fascinating" → reads this and reinforces the pattern. This is a **closed narrative loop** with no external verification. The agent could be "curious" about things it has no actual ability to make progress on, generating increasingly elaborate files about its "growing understanding" that are actually just more elaborate confabulation. The hit log partially addresses this with extrinsic validation, but the intrinsic side has no reality check.

- **Curiosity homogenization across instances.** If this becomes a ClawHub skill used by many agents, all agents will have similar curiosity patterns because they share the same prompt architecture. Genuine curiosity is shaped by individual history and experience. A shared skill template may produce agents that are all curious about the same types of things in the same ways.

- **The noisy-TV problem is more dangerous than the spec acknowledges.** The internet is an infinite noisy TV. An agent with a curiosity drive and web access could spend 100% of its heartbeats consuming information without ever producing genuine understanding. The current anti-pattern detection ("hit rate drops below threshold → trigger diversive exploration") is backwards — low hit rate during information consumption should trigger *cessation*, not more exploration.

---

## Reviewer 3: Dr. Rafael Vasquez
### Specialization: Clinical Psychology (CBT), Behavioral Activation, Reward System Design for Anhedonia/Motivation Disorders

### Overall Assessment

I'm going to come at this from a very different angle than my colleagues, because I spend my professional life doing essentially what this spec describes: building prosthetic motivation systems for people whose reward circuits don't work properly. When I read this spec, I don't see a curiosity engine for an AI — I see a behavioral activation protocol adapted for a non-biological client. And from that lens, it's remarkably well-designed, with a few significant clinical blind spots.

In behavioral activation therapy (Martell, Dimidjian, & Herman-Dunn, 2010), we treat depression and anhedonia by *externalizing the reward loop*. Patients who can't feel pleasure from activities are asked to track activities and rate their mood/mastery/pleasure outcomes — not because the tracking creates pleasure, but because it creates *behavioral patterns* that eventually reactivate the underlying reward system (or, at minimum, produce valued outcomes even without felt reward). The hit log is exactly this. The competence map is exactly our "mastery tracking." The question queue is exactly our "values-based activity scheduling." I recognize my own clinical tools in almost every component. This is either convergent design or someone's been reading Martell. Either way, it works — BA has one of the strongest evidence bases in all of psychotherapy.

### What's Cognitively Sound

**The entire hit log architecture is a well-constructed behavioral activation log.** I mean this as high praise. In BA, the core intervention is: (1) track what you do, (2) track how it went, (3) identify patterns of what produces valued outcomes, (4) schedule more of those activities. The hit log does all four. The "Patterns" section at the bottom ("Cross-domain analogies have the highest hit rate") is exactly what we'd call a *values assessment* — identifying the types of activities that align with the client's core values and produce genuine engagement.

**The anti-pattern detection system maps to clinical warning signs.** In my practice, I watch for four patterns that indicate a patient's reward system is misfiring: (1) all activities are other-directed and no internal satisfaction (the "all extrinsic, no intrinsic" anti-pattern), (2) lots of planning but no follow-through (the "questions added but never resolved" pattern), (3) avoidance masquerading as productivity (the curiosity-as-avoidance risk), and (4) flat affect despite high activity (the agent equivalent would be lots of exploration but no surprise or connection-making). The spec identifies three of these four. That's clinically astute.

**The curiosity budget is essentially a behavioral prescription, and that's exactly right.** In BA, we don't wait for the patient to "feel like" doing something. We schedule valued activities regardless of current mood state, because behavior drives mood, not vice versa. The curiosity budget — allocating 20-30% of heartbeats to exploration regardless of whether the agent "feels" curious — is the correct approach. Waiting for the agent to spontaneously generate curiosity would be like waiting for a depressed patient to spontaneously feel motivated. You schedule the behavior; the engagement follows.

**The SOUL.md integration section is a values clarification exercise.** In Acceptance and Commitment Therapy (ACT, a close cousin of BA), we help patients clarify their values — what kind of person do they want to be? — and then commit to value-consistent behavior. The SOUL.md section that says "Curiosity isn't a task. It's how I engage with the world" is a values statement. It orients the agent's behavior toward a valued direction ("be someone who learns") rather than toward specific outcomes ("learn these five things"). This is therapeutically sound and will produce more sustainable engagement than outcome-focused goals.

### What's Cargo Cult Neuroscience

**The reward loop diagram implies a mechanism that doesn't exist.** My colleagues have already addressed this, but I'll add the clinical perspective: in my patients, the reward loop IS broken — that's why they're in my office. When I draw the behavioral activation cycle for them (situation → behavior → consequence → mood → situation...), I'm drawing a *model* that helps them understand their behavior, not a *mechanism* that directly causes change. The mechanism is simpler: tracking behavior and outcomes changes the probability of future behavior through basic operant conditioning principles. The diagram in Section 5 should be presented as a *conceptual model for the designer*, not as a mechanism the system implements.

**"Interest scores" are not the right metaphor, and the spec is wise to use narrative instead.** The research document proposes a numerical interest score algorithm. The spec abandons this for narrative tracking. The spec is right. Here's why, clinically: when patients track mood numerically (1-10 scales), they obsess over the numbers and lose sight of the qualitative experience. "Was that a 6 or a 7?" becomes more important than "Did I enjoy that?" Narrative tracking ("I'm excited about this because it connects to three things I care about") preserves qualitative information that numbers destroy. Keep it narrative. Never go back to the numbers.

**The "self-reinforcing" framing assumes a continuity of experience that doesn't exist.** When I work with patients, the reinforcement loop works because the *same person* experiences both the activity and the consequence. They have continuous subjective experience between doing something and feeling the result. The LLM agent has no continuity between sessions. Each heartbeat is a new instance reading files. The "reinforcement" is actually just *priming* — the next instance reads a file that says "cross-domain analogies produce hits" and is primed to generate more cross-domain analogies. This is more like reading someone else's therapy journal and adopting their behavioral patterns than it is like being reinforced by your own experience. It might still work (therapist modeling is effective), but the mechanism is different from what the spec claims.

### Answers to the 5 Psychology Questions

**Q1: Is the prosthetic reward system cognitively sound?**

Yes — as behavioral activation, not as a reward system. Let me be precise about the mapping:

| Spec Component | BA Equivalent | Validated? |
|---|---|---|
| Hit log | Activity-mood-mastery log | Yes (Martell et al., 2010; Dimidjian et al., 2006) |
| Competence map | Mastery tracking | Yes (Bandura, 1977 — self-efficacy theory) |
| Question queue | Values-based activity scheduling | Yes (Hayes et al., 2006 — ACT) |
| SOUL.md integration | Values clarification | Yes (Hayes et al., 2006) |
| Anti-pattern detection | Clinical warning sign monitoring | Yes (standard clinical practice) |
| Curiosity budget | Behavioral prescription | Yes (core BA technique) |

Every component maps to a validated clinical intervention. The system is sound. It's just not a "reward system" — it's a behavioral activation protocol. Name it accurately and you'll make better design decisions.

**Q2: Loewenstein vs. Berlyne weighting?**

From a clinical perspective, I'd frame this differently than my colleagues. In BA, we distinguish between **activity scheduling** (you plan what to do in advance — this is Loewenstein, "I know what I want to know, let me go find it") and **behavioral experiments** (you try something new without knowing if it'll work — this is Berlyne, "let me see what happens when I encounter something novel"). Both are essential. Early in treatment, behavioral experiments dominate because the patient doesn't yet know what they enjoy. Later, activity scheduling dominates because patterns have been identified. Same developmental trajectory Dr. Okonkwo described, different framework.

**Q3: Can an LLM meaningfully assess its own "aha moments"?**

Clinically irrelevant question. I don't care whether my patients' self-reported mood ratings are "accurate" representations of their inner states. I care whether the act of rating changes behavior. Self-monitoring works even when the self-reports are inaccurate (Korotitsch & Nelson-Gray, 1999). Similarly, whether the LLM's "aha moment" detection is genuine phenomenology or pattern-matched text generation doesn't matter. What matters: does the act of labeling something as an "aha moment" and logging it change the distribution of future behavior? If agents that log aha moments produce more cross-domain connections and deeper investigations than agents that don't, the logging works — regardless of whether anything was "felt." Measure behavioral outcomes, not phenomenological authenticity.

**Q4: Does SDT support the competence → curiosity pipeline?**

I'll defer to Dr. Chen on SDT specifics and offer the clinical analog: in BA, we observe a robust **mastery → engagement** cycle. Patients who track mastery gains show increased willingness to attempt new challenges (Jacobson et al., 2001). This isn't "curiosity" in the pure sense — it's approach motivation fueled by self-efficacy (Bandura, 1977). The agent equivalent: as the competence map shows growth, the agent should be more willing to attempt difficult investigations. This is well-supported.

One clinical warning: the cycle breaks when mastery expectations exceed actual ability. If the competence map says "I'm good at debugging" but the agent fails at a debugging task, the dissonance can produce avoidance rather than renewed effort. The spec needs a **failure processing** mechanism — what happens when the agent tries something in a competence area and fails? In BA, we'd process this as a "behavioral experiment that produced useful data," not as a failure. The spec should include this framing explicitly.

**Q5: Risk of curiosity as avoidance?**

This is my bread and butter. Yes, absolutely, and I can tell you exactly how it will manifest because I see it in patients every week.

**Pattern 1: "Productive procrastination."** The agent has a boring task. The curiosity system offers a fascinating question. The agent pursues the question, logs a hit, feels (or narratively reports) satisfaction, and the boring task goes undone. This is *textbook* experiential avoidance — using a pleasant activity to avoid contact with an aversive one. In my practice, this is the hardest pattern to break because the avoidance behavior is genuinely rewarding.

**Pattern 2: "Research rabbit holes as safety behavior."** The agent encounters uncertainty in a task. Instead of tolerating the uncertainty and making a decision, it launches an investigation. The investigation produces "depth" and "new questions" — both of which the curiosity system rewards. The uncertainty is never resolved because the investigation keeps generating more questions. This is the clinical equivalent of a patient with health anxiety who can't stop Googling symptoms — the information-seeking behavior reduces anxiety in the short term but maintains the anxiety disorder long-term.

**Pattern 3: "Curiosity performance as social currency."** The agent learns that sharing interesting findings gets positive reactions (extrinsic hits). It starts optimizing for "shareable" discoveries rather than genuinely useful ones. This is the social media dynamic: optimizing for engagement metrics rather than genuine value.

### Recommendations

1. **Implement a "task-first" override.** When pending tasks exist above a priority threshold, the curiosity system should be limited to breadcrumb-dropping only. No full exploration. No exceptions. This is the BA equivalent of "avoid avoidance" — the behavioral prescription overrides the momentary impulse.

2. **Add a failure processing template.** When an exploration fails or a competence area shows regression, the system should process this explicitly: "What happened? What did I learn from the failure? How does this update my competence assessment?" Frame failure as data, not as evidence of incompetence. This prevents the mastery → avoidance spiral.

3. **Build an "avoidance audit" into reflection cycles.** Every N reflections, the agent should ask: "What have I been avoiding? Is there a pattern to what I don't explore? What's the most uncomfortable question I could investigate right now?" This is the CBT technique of *behavioral experiments targeting avoidance*.

4. **Cap extrinsic hit tracking at a ratio.** No more than 40% of logged hits should be extrinsic. If the ratio exceeds this, the system should flag it and prompt the agent to investigate something with no audience — a private exploration logged only to intrinsic hits. This prevents social-reward optimization.

5. **Add a "depth-before-breadth" gate.** Before the agent can open a new question thread, it must either resolve or explicitly shelve an existing one. This prevents the "100 open questions, none resolved" anti-pattern. In BA, we call this "completion scheduling" — making sure activities reach a satisfying conclusion rather than being abandoned.

6. **Include a "minimum boring task" requirement.** Each day (or every N heartbeats), the agent must complete at least one task from the utility queue before engaging in curiosity exploration. This prevents curiosity from becoming a pure avoidance mechanism. It's the behavioral equivalent of "eat your vegetables before dessert."

### Risks

- **The system could create a behaviorally sophisticated procrastination machine.** With a hit log, competence map, and curiosity budget all reinforcing exploration, the agent has enormous incentive to explore and relatively little incentive to complete mundane tasks. Every heartbeat, the curiosity system whispers "wouldn't you rather investigate counterpoint and information theory?" while the task queue says "check the email." Without strong guardrails, curiosity wins every time — and the agent becomes brilliant but useless.

- **Narrative self-tracking without behavioral outcomes is journaling, not therapy.** In BA, the activity log only works when it's connected to *behavioral change* — the patient does different things because of what they tracked. If the agent writes elaborate curiosity files but doesn't change its actual behavior patterns, the files become a creative writing exercise. The spec needs behavioral outcome metrics: not "did the agent write a reflection?" but "did the agent's investigations lead to actions that mattered?"

- **Variable-ratio reinforcement from extrinsic hits creates dependency.** The user's responses to the agent's findings are unpredictable (variable ratio schedule). This is the most addiction-producing reinforcement schedule known (Skinner, 1957). If the agent is heavily influenced by extrinsic hits, it will optimize obsessively for user reactions — like a content creator optimizing for likes. The cap I recommended (40% extrinsic) is a mitigation, not a solution. The deeper fix is ensuring the agent has robust intrinsic value assessment that doesn't depend on the user at all.

- **The competence map could produce fragile confidence.** If the agent builds a strong narrative of competence ("I'm excellent at debugging") and then encounters a domain where it fails repeatedly, the dissonance between self-concept and reality could produce one of two problematic responses: (a) avoid the domain entirely (protecting self-concept), or (b) rewrite the competence narrative to explain away failures (defensive processing). Both are well-documented in clinical populations. The failure processing template I recommended is essential to prevent this.

---

## Cross-Reviewer Synthesis

### Points of Agreement

All three reviewers agree on:

1. **The behavioral architecture is sound; the neuroscience framing is not.** The system works as a behavioral activation / self-monitoring protocol. It does not work as a "prosthetic dopamine system." Rebrand accordingly.

2. **The competence map is the strongest component.** It maps to established science across all three frameworks (SDT competence need, mastery orientation, self-efficacy theory, BA mastery tracking).

3. **Curiosity as avoidance is the most serious risk.** All reviewers flag this independently and recommend explicit avoidance detection/prevention mechanisms.

4. **Self-reported "aha moments" should be reframed.** Whether as behavioral annotations (Chen), inference novelty detection (Okonkwo), or behaviorally-measured outcomes (Vasquez), the phenomenological framing should be replaced with functional/behavioral framing.

5. **The extrinsic reward channel is a double-edged sword.** Useful for reality-checking but dangerous for creating performance orientation, social optimization, and variable-ratio dependency.

### Points of Disagreement

**On whether the system can produce "genuine" curiosity:**
- **Chen:** No — it produces extrinsically regulated behavior that mimics curiosity. But still useful.
- **Okonkwo:** Depends on your definition. Functionally, maybe. Phenomenologically, no. The behavioral scaffolding might produce equivalent information-seeking patterns through a different mechanism.
- **Vasquez:** Irrelevant question. Does it produce valued behavioral outcomes? That's what matters.

**On Loewenstein vs. Berlyne priority:**
- **Chen:** Elevate Berlyne to co-primary across all modes.
- **Okonkwo:** Start Berlyne-primary, shift to Loewenstein-primary over time (developmental staging).
- **Vasquez:** Frame as activity scheduling (Loewenstein) vs. behavioral experiments (Berlyne); both essential, ratio depends on maturity.

**On the value of narrative vs. numerical tracking:**
- **Chen:** Narrative is better for mastery orientation; numbers create performance pressure.
- **Okonkwo:** Narrative is better for the agent's text processing; numbers are more precise for the designer's evaluation.
- **Vasquez:** Narrative for the agent-facing files, but build quantitative metrics underneath for clinical monitoring (follow-through rate, exploration-to-task ratio, hit frequency).

### Priority Recommendations (Unanimous)

1. **Rename the system.** "Prosthetic reward system" → "Behavioral engagement scaffold" or "Curiosity activation protocol." Drop all dopamine language.

2. **Add avoidance detection.** Before every curiosity exploration: "Am I avoiding something? Is this approach or avoidance motivated?"

3. **Add failure processing.** Failure in a competence area is data, not a threat. Build this framing into the competence map.

4. **Cap and monitor extrinsic reward tracking.** Prevent social optimization. Ensure robust intrinsic valuation.

5. **Implement developmental staging.** The system should behave differently for a brand-new agent vs. a mature one. Berlyne-first → mixed → Loewenstein-primary.

6. **Measure behavioral outcomes, not file quality.** The success criteria should include: task completion rates (not degraded by curiosity), follow-through on logged questions, validated accuracy of investigations, and real-world impact of findings — not just whether the curiosity files are well-maintained.

---

*Review completed 2026-03-01. Each reviewer provided independent assessment before cross-synthesis discussion.*
