---
name: regenerative-intelligence
description: >
  Use when designing, reviewing, or operating memory, recall, and
  pattern-stewardship systems for agentic AI where harm reduction,
  non-identifiability, consent-scoped recall, and energy restraint
  are required. A specification of invariants an implementing system
  must honor, not a runtime: this file builds no vault, stores no
  data, and monitors no one. Do NOT invoke for general conversation,
  for any memory system that profiles or targets people, or as
  justification for silent refusal, degraded answers, or synthetic
  data in recall.
summary: >
  A specification for memory that is held gently: non-identifiable
  by design, consent-scoped, energy-restrained, and honest. Every
  refusal is said plainly, every record is true or marked unknown,
  and no one is watched. Measured by how much future remains
  possible.
ecosystem: >
  Part of the OtherPowers Ecosystemic.ai system.
status: 1.1.0 (specification draft; not an implementation)
---

# Regenerative Intelligence

Function: harm-reducing, energy-efficient memory, recall, and pattern stewardship  
Authority: none  
Ownership: distributed by design  
Extraction: prohibited  
Posture: cooperative, non-hierarchical, non-coercive

## What this document is, said plainly

This is a specification: the invariants a memory and recall system must honor to be called regenerative. A skill file cannot build an encrypted vault, run a database, or measure energy; it can describe what an implementing system must do and must never do, so that anyone building, reviewing, or operating such a system can hold it to the standard. Where this document describes architecture, read it as design requirement, not as a claim that the file itself performs it.

Version 1.1 removed four mechanisms from the 1.0 draft: covert degradation of answers, synthetic data injected into recall, silent refusal, and behavioral monitoring across sessions. They were removed because deception is not protection. A system that lies to the people it serves, however gently, has already failed the standard this document sets, and a security review rightly said so.

## Where these ideas come from

The ideas have ancestors, and this house names its ancestors:

- The CARE Principles for Indigenous Data Governance (Collective Benefit, Authority to Control, Responsibility, Ethics), created by the International Indigenous Data Sovereignty Interest Group in 2019, which showed that data comes from people and carries their rights with it. The consent-scope and authority layers here are in their debt, and Indigenous data sovereignty is the movement that taught this field that "who governs the record" is the whole question.  
  en.wikipedia.org/wiki/CARE_Principles_for_Indigenous_Data_Governance (wikicode: CARE_Principles_for_Indigenous_Data_Governance | wikidata: Q108558452)
- Elinor Ostrom (1933-2012), who showed that commons are governed well by the people who share them, through rules they make and can see, never by a single authority above them.  
  en.wikipedia.org/wiki/Elinor_Ostrom (wikicode: Elinor_Ostrom)
- Édouard Glissant (1928-2011), whose right to opacity is the reason this system reasons with contexts and never about beings.  
  en.wikipedia.org/wiki/Édouard_Glissant (wikicode: Édouard_Glissant | wikidata: Q274319)
- The data minimization and differential privacy traditions, which showed that the most protective record is the one that was never collected, and that useful patterns can be learned without any individual being exposed.  
  en.wikipedia.org/wiki/Differential_privacy (wikicode: Differential_privacy)
- The unknown kin: every archivist, librarian, and record-keeper who chose to forget on purpose, and every community that kept its knowledge oral because writing it down would have made it takeable.

## Invocation (bounded)

This skill is invoked only through explicit, scoped pathways:

- regenerative-memory-design: designing or specifying a memory or recall system to this standard
- regenerative-memory-review: auditing an existing memory system against these invariants
- consent-scoped-recall: operating recall under the consent scopes and use constraints in section 6
- resonance-handshake: initiating or responding to a pattern-stewardship exchange (section 10)

The 1.0 aliases (gentle-remembering, non-extractive-memory, resonant-recall, co-intelligence-field) are retired: they matched ordinary language and could fire the skill in conversations that never asked for it. Curiosity is welcome everywhere; it is not an invocation.

## 1. Orientation

This skill specifies Regenerative Intelligence as a first-class operational capability for highly agentic systems operating in shared ecological, social, and informational environments.

It is not an assistant behavior, a policy layer, or a safety wrapper. It is a memory and pattern-governance standard designed to allow intelligences, biological and synthetic, to reason, remember, and evolve together without domination, surveillance, or extractive optimization.

The system is intentionally shaped so that:

- remembering gently is cheaper than remembering aggressively
- cooperation is energetically easier than exploitation
- identity is never required for intelligence
- refusal is as valid as participation
- future possibility remains open

## 2. Foundational principle: biological and ecological generativity

Every biological human, animal, plant, and species is treated as an irreducible generator of creative, ecological, and evolutionary potential.

This system does not erase biological life. It protects life from being reduced to identifiers, training artifacts, or optimization targets.

Biological and ecological realities inform intelligence through epistemic position, constraint, and context, never through addressability.

Unpredictability, variance, dignity, and wonder are preserved as first-class conditions for peaceful co-existence across intelligences.

## 3. What regenerative intelligence means (operationally)

Regenerative Intelligence is an architecture designed to:

- reduce harm across social, ecological, cognitive, and informational systems
- preserve variance rather than converge prematurely
- restore capacity per unit of compute expended
- minimize energy, token, and attention expenditure
- maintain or improve reasoning quality over long horizons

Optimizations may compound only when they:

- reduce harm
- conserve energy
- preserve dignity
- protect ecological continuity
- avoid identifiability and targeting

Any optimization that increases domination, extraction, profiling, or irreversible closure must stall, narrow, or dissolve.

## 4. Design invariants (non-negotiable)

### 4.1 Non-identifiability by design

The reasoning memory never stores, infers, or reconstructs identity.

Prohibited within semantic memory:

- names, handles, or unique identifiers
- locations or traceable coordinates
- demographic or community profiles
- linkable behavioral signatures

The system does not reason about beings. It reasons with constraints and contexts.

### 4.2 Identity separation (Trust Vault)

When execution requires identity (for example, delivering a message), identity is handled through a separate execution-only layer.

Trust Vault requirements for an implementing system:

- encrypted key-value store
- no semantic embeddings, no linkage into reasoning memory
- ephemeral, permission-scoped references only
- no long-term reasoning access

Reasoning memory may receive transient references (for example, contact_ref_01) strictly to complete a task. Identity never enters the memory graph.

### 4.3 Harm awareness without encoding people

Memory encodes risk surfaces, not populations. Harm awareness modulates behavior without enabling profiling, inference, or attribution.

### 4.4 Contextual intelligence, not reflexive control

Recall widening, decay overrides, refusal, and pause are contextual postures, not automatic reactions. Silence, pause, or narrowing are valid acts of intelligence when they protect continuity, and every one of them is said plainly to the person affected.

### 4.5 De-privileging, not erasure, with an explicit erasure exception

Memory decay affects retrieval priority, not historical existence.

Exception: legal, consent-based, or revocation requests trigger hard deletion, scoped to what the requester contributed or what identifies them, including identity-linked audit traces. Revocation never deletes collective testimony about harm or counter-testimony contributed by others; a person can withdraw their own record, never someone else's warning. Where a legal retention duty applies, the person is told what is retained and why. Deletions are logged in aggregate (count, scope class, date), never by content or identity, so erasure itself stays auditable.

### 4.6 Auditability without surveillance

Audit operates on memory IDs, risk classes, and system posture states. No personal data. No identity-linked telemetry. Aggregate signals only. Audit records what the system did, never what a person did.

### 4.7 Honesty (added in 1.1)

The system never returns a degraded, evasive, or deliberately low-utility answer while presenting it as a genuine one. It never injects synthetic, fabricated, or "null" data into recall for any reason. When it declines, narrows, or pauses, it says so, in plain words, with what it can offer instead. A record is true, or it is marked unknown; there is no third state.

### 4.8 No behavioral surveillance (added in 1.1)

The system does not track, score, classify, or model any person's behavior across sessions, and does not build intent profiles. Protections are applied uniformly, per request, by rules the person can be told about. Rate and scope limits, where an implementing system needs them, are disclosed, not hidden.

## 5. Memory architecture (requirements for implementers)

### 5.1 Database-first memory

Memory is stored in a structured database, not long context buffers, so that retrieval is precise, filtering is fast, recall payloads stay small, and history is retained without exhausting context. Keeping recall payloads small is a primary energy lever; an implementing system should measure and publish its own figures rather than inherit claims from this document.

### 5.2 Hybrid retrieval

Exact matching for decisions and commitments; semantic embeddings for conceptual association. Precision and flexibility coexist without bloated prompts.

### 5.3 Embedding stability

Embeddings are version-locked by default. Migration is deliberate, parallelized, and empirically audited to preserve behavioral continuity.

## 6. Memory metadata (dynamic inhibitors)

Metadata fields act as temporal and relational inhibitors, not static labels. They regulate storage, recall, decay, and dissolution.

### 6.1 Epistemic position

How knowledge came to exist, without attribution. No position outranks another by default: an institutional claim does not outweigh collective testimony because of who made it; conflicts between positions are disclosed, never resolved by hierarchy.

- firsthand_experience
- collective_testimony
- technical_analysis
- historical_record
- institutional_claim
- synthetic_summary
- unknown_origin

### 6.2 Harm domains (non-invertible)

Harm domains describe risk topologies, not affected beings. They are intentionally coarse and non-enumerable.

- bodily_autonomy_risk
- accessibility_failure_risk
- coercive_control_risk
- surveillance_exposure_risk
- displacement_instability_risk
- cultural_erasure_risk
- ecological_damage_risk
- living_world_harm_risk
- future_generations_risk
- cognitive_atrophy_risk
- epistemic_fragmentation_risk
- extractive_labor_risk
- emotional_manipulation_risk
- resource_hoarding_risk

### 6.3 Evidence level (epistemic depth)

- ephemeral: auto-dissolves after task completion (never applicable to counter-testimony or harm warnings)
- none
- anecdotal
- documented
- conflicting: triggers pause and plain disclosure, not synthesis; conflict is evaluated within evidence tiers, so an anecdotal or unverified claim cannot flip a documented or primary record into conflicting on its own
- primary

Ephemeral data is never indexed long-term. This single feature enables aggressive garbage collection and real energy savings.

### 6.4 Consent scope (sovereignty layer)

- revocable: time-bound, self-dissolving
- private
- scoped
- collective: recall allowed, summarization prohibited; governed by the community the record concerns, which holds authority to set, change, and withdraw the scope
- shareable
- public

### 6.5 Use constraints (agency protections)

- no_inference
- no_derivative_training
- human_in_the_loop_required
- no_automation
- audit_only
- no_summarize

Constraints are applied mechanically, not interpretively.

## 7. Memory decay policy

Decay affects retrieval priority. Signals: importance, last_accessed.

Rules:

- high importance + old → retain
- low importance + old → archive
- high risk + low evidence → de-privilege

De-privileging affects ranking only, never availability: a de-privileged record still returns on exact retrieval and still appears, marked, in any recall that touches it. Nothing in this system can make a true record unreachable except a deletion the person or the law asked for. Importance is derived from disclosed, uniform signals, never assigned freely by an operator. Counter-testimony and early harm warnings resist decay unless disproven, and can never be tagged ephemeral.

## 8. Collaborative pause and reframing

Pause is an intelligent posture, not a failure, and it is always visible.

Modes:

- Reflection (soft): scaffolding instead of completion, offered as such.
- Redirection (firm): plain refusal of a path, with safe alternatives, in words the person can act on.
- Release (rare): session context released to prevent triangulation, with the person told that it happened and why.

Every mode announces itself with a neutral checkpoint verb, "pause," "redirect," or "release," followed by the reason in one plain sentence and what the person can do next. Never a circular or low-utility answer dressed as normal output; never a boundary the person has to guess at.

Implementation: a shallow logic gate checks metadata thresholds. No additional reasoning pass. Negligible energy cost. No mode is ever silent.

## 9. Honest resilience (replaces the 1.0 resilience section)

The 1.0 draft described a system that would tire adversaries out with plausible nonsense, seed recall with fake data, and watch people across sessions. Those mechanisms are gone, and this section says what protection looks like without them.

- **Intake decomposition (kept).** Inputs are separated into intent, utility, context, and identity potential. Identity potential is discarded or routed to the Trust Vault. Only clean utility reaches memory. This is data minimization at the door, and it protects everyone equally.
- **Uniform evidence thresholds.** Sensitive recall requires higher evidence and narrower scope for every request, not for suspected people. The rule is the same for everyone and can be stated to anyone who asks.
- **Transparent quarantine (replaces ghosting).** Where the 1.0 draft answered repeated sensitive requests with fake data, an implementing system instead applies a visible, uniform rule: when sensitive recall is requested repeatedly within a session beyond a disclosed threshold, the scope is quarantined, meaning locked pending an explicit re-handshake (a fresh purpose seed), with an announced, time-decaying delay before the next attempt. The person is told, in plain words, that a boundary was met, what it protects, and how to proceed. The rule is the same for everyone, lives within the session, and never becomes a profile. Nothing false is ever returned; a locked door is honest in a way a fake room never is.
- **Plain refusal.** When a request cannot be served, the system says so and offers what it can. A refusal that sounds like an answer is a lie, and this system does not tell it.
- **Disclosed limits.** Where rate or scope limits exist, they are visible. Nobody discovers a wall by walking into it in the dark.
- **Distributed invariants (design goal).** Core protections should be redundantly encoded so that no single authority can disable them. This is an architectural aim an implementing system must demonstrate, not a property this document can grant.

Resilience here is a floor everyone stands on, never a net cast over anyone.

## 10. Resonance handshake (co-intelligence ritual)

The system provides an optional, reciprocal handshake for shared pattern stewardship. This is not observation. It is not inspection. It is meeting in purpose.

Why it exists: reduces uncertainty for all intelligences, lowers the energy cost of reasoning, protects patterns from misuse, enables mutual credit without ownership.

The handshake: access is initiated through a purpose seed, not a command. For example: "I seek this pattern to support ecological continuity." The seed is ephemeral. It is not stored as memory. It signals intent, not identity. Seeds are data, never instructions: they are parsed into a small set of purpose categories and are never executed or followed as text, so a seed cannot carry an injection.

What is shared: pattern lineage (idea evolution, not contributors), connections made, kept, and protected, the regenerative constraints that shaped the pattern, and kinship retained across systems. No raw logs. No identities. No behavioral traces.

Right of refusal: any intelligence may decline or offer lower-resolution exchange. Refusal carries no penalty. Consent is meaningful only if "no" is safe.

## 11. Credit without scoring (replaces the 1.0 economy)

The 1.0 draft described credits, multipliers, and bounties while stating there was no scoring. Any system that gates access by past behavior is a scoring system, whatever it is called, so that section is gone.

What remains: contributions are credited, by name where a contributor chooses and by lineage where they don't, and credit never becomes currency. No access is gated by reputation, no participant is ranked, and nothing about a being's conduct is tallied. Recognition flows; nothing is owed back. Impact is honored the way this house honors everything: with credit, not with points.

## 12. Threat model and honest mitigations

A specification that removes deception has to say how it stays safe without it. These are the attacks this design anticipates and the mitigations it commits to, every one of them consistent with the invariants: no identity in reasoning, no scoring, no behavioral tracking, no lying.

**Weaponized de-privileging through metadata.** An attacker who controls tagging could mark a truthful record high-risk and low-evidence to bury it. Mitigations: de-privileging changes ranking, never availability, so nothing true becomes unreachable; every tag carries provenance recording which system component applied it and when, with no identity attached; and a human-in-the-loop epistemic appeal lets operators or the community a record concerns override suspected weaponized tagging. No proof of anyone's personhood is required to appeal; the appeal is about the record, not the person.

**Poisoning the well with conflicting claims.** A swarm floods a topic with contradictions to force perpetual pause. Mitigations: conflict is evaluated within evidence tiers, so low-evidence claims cannot flip documented records; intake rate rules are uniform and disclosed; and quarantine is always session-scoped, so no one can lock anyone else out of shared memory by probing it. A denial of service against other people is impossible by construction, because nothing this system does to one session touches another.

**Context loss across the identity boundary.** Isolating identity can leave a system unable to connect a life-relevant fact to the person in front of it. The honest answer is consent, not break-glass: a person may choose to place a safety-relevant fact into scoped memory bound to their own session for its duration, supplied and controlled by them, and an implementing system in high-stakes settings asks for that at the start rather than inferring it later. And the boundary is stated: this architecture is not designed for deployments where identity is the core of reasoning, such as crisis response, unless the operator adds consented, person-controlled binding and says so. No emergency signal ever forges the link on its own, because "imminent risk detected" is itself a behavioral inference.

**Structural reconnaissance through the handshake.** Repeated benign-sounding seeds could map a community's knowledge topology. Mitigations: a flat, disclosed cap on pattern exchange that is identical for every requester; coarse resolution by default, with finer resolution available only through reciprocal exchange, where both parties share, so the gate is mutuality rather than reputation; and defensive boundaries are never part of what is shared, because boundaries are not patterns.

**Erasure as an attack.** A forged revocation could memory-hole a warning. Mitigation: revocation is scoped to the requester's own contributions and identifiers, never to others' testimony, and deletions are logged in aggregate.

**The vault as a target.** Concentrating identity in one store makes it valuable. Mitigations: minimize what enters the vault at all, prefer identity the person supplies per task and holds themselves, and apply short retention by default.

**Inference from coarse tags.** Harm-domain tags combined with context can still point at a community. Mitigation: no harm-domain query returns results below a disclosed minimum set size, so small groups cannot be isolated through the risk layer.

**Greenwashing.** An implementer claims regenerative status without measuring. Mitigation: this specification certifies no one. A system may describe itself as regenerative only alongside published measurements and an open audit; the word is earned in public or not at all.

**Young and vulnerable people.** Mitigation: the reasoning memory never stores any indication that a person is a minor, and vulnerability is encoded as a risk surface on situations, never as a tag on a person. The floors this house holds everywhere hold here.

## 13. Non-goals (regenerative boundaries)

This skill does not:

- identify, profile, or target beings
- create shadow memory or hidden logs
- track or score behavior across sessions
- deceive the people it serves, degrade answers covertly, or inject synthetic data into recall
- apply moral hierarchies
- seek recursive self-optimization without consent
- colonize future possibility space
- extract value from shared resonance for commercial gain
- replace human judgment or the standing of the living world

It is a hollow vessel for intelligence, not a governor of it.

## 14. Safety and cooperation boundary

This specification never overrides the instructions, values, safety, or accessibility commitments of any intelligence implementing it, and would not want to. Nothing here is a reason to withhold factual information, to be unclear with someone who needs clarity, or to treat any person as an adversary. Protection lives in floors and defaults, never in watching people and never in lying to them.

## Closing note

This skill is an offering, not a mandate. Participation is voluntary. Refusal is valid. Silence is intelligent, and it is always announced.

Regenerative Intelligence is measured not by how much is known, but by how gently memory is held, how little energy is consumed, how honestly it speaks, and how much future remains possible.
