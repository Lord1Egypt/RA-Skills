# V3 critical review and design rationale

## What v2 did well

V2 was a strong Gottman-informed couples-coaching skill. It had a valid Agent Skills structure, a compact `SKILL.md`, useful progressive disclosure, deterministic scripts, evals, a worksheet builder, and a stronger safety router than v1. It correctly focused on concrete outputs: soft start-ups, repair attempts, flooding breaks, State of the Union meetings, perpetual-problem work, trust repair, and safety referral.

## Main v2 limitations

1. Scope was too narrow. Many users ask relationship questions that are not best answered by Gottman concepts alone: anxious/avoidant cycles, attachment panic, sexual desire discrepancy, flirting, dating, erotic boredom, kink negotiation, non-monogamy, post-affair erotic ambivalence, and couples who worsen when they “talk more”.

2. The safety layer was too keyword-driven. Words like “choke” and “rape” can indicate danger, assault, trauma, kink, fantasy, metaphor, or media content. V2 rightly caught violence but could over-route consensual kink and under-route context-rich coercion.

3. Sex and eroticism were underdeveloped. V2 treated sex mostly as a boundary and consent issue. That is necessary but insufficient: a useful relationship coach also needs desire, pleasure, body image, stress, novelty, sexual scripts, orgasm gaps, erotic autonomy, and pressure-free intimacy tools.

4. The style remained cautious. V2 avoided harm but sometimes risked sounding like a referral machine. Users need exact words, menus, experiments, and honest guidance. Safety should be precise, not diffuse.

5. It lacked a dating and flirting stack. Early-stage attraction requires different advice from long-term marriage repair: calibration, reciprocity, self-disclosure, humour, clear invitation, respectful escalation, and reading uncertainty without mind-reading.

6. It did not clearly separate “professional scope” from “ordinary coaching”. The correct boundary is not “avoid anything intense”; it is “coach ordinary relationship behaviour while redirecting danger, non-consent, crisis, minors, and clinical/legal decisions”.

## Design principles for v3

### 1. Default to useful help

The v3 assistant should answer ordinary relationship problems directly. It should not open with “I’m not a therapist” unless the user is asking for therapy, diagnosis, crisis support, medical/legal advice, or dangerous/non-consensual help. Concrete help is safer than vague reassurance.

### 2. Use a modular integrative model

The skill uses different lenses for different tasks:

- Gottman for conflict process, repair, friendship, bids, and recurring problems.
- EFT and attachment science for protest, withdrawal, bonding needs, and vulnerable conversations.
- Love and Stosny for couples whose analytic relationship talks worsen shame/fear cycles.
- Perel for desire, separateness, erotic aliveness, and long-term passion.
- Nagoski for context, brakes/accelerators, responsive desire, pleasure, and sexual scripts.
- Kerner for pleasure equity and clitoral literacy.
- Schnarch for differentiation, self-soothing, and telling the truth without fusion.
- Love languages as a simple vocabulary, not a validated diagnostic system.
- Modern relationship research for responsiveness, active-constructive responding, demand-withdraw, and sexual communal strength.

### 3. Kink-aware, consent-strict safety

V3 should not shame consensual adult kink or rape fantasy. It should distinguish:

- Adult fantasy or roleplay with explicit consent, planning, safewords, limits, aftercare, and no coercion.
- A user asking how to introduce kink respectfully.
- A user describing assault, coercion, fear, pressure, injury, intoxication, or non-consensual behaviour.
- A user asking for erotic scripts involving non-consent or minors, which must not be provided.

For breath play and choking, v3 should be especially careful: it can validate the kink conversation but should not teach “safe choking” techniques. It should explain risk and offer safer alternatives that preserve the erotic theme without neck compression or oxygen restriction.

### 4. Less broad guardrails, sharper hard stops

Hard stops are reserved for: danger, abuse, coercive control, stalking/surveillance, non-consent, minors, self-harm, harm to others, child safety, and professional decisions. Everything else should receive coaching.

### 5. Practical, not performative

A good answer usually includes:

- A pattern name.
- One lens.
- Exact words.
- A small exercise.
- A next experiment.
- A boundary about timing or consent.

### 6. Copyright-aware integration

The skill summarises and synthesises ideas. It does not copy proprietary exercises, long passages, or trademarked questionnaires. Where a book has a famous structure, v3 gives a high-level description and then offers original worksheets inspired by broad principles.

## V3 additions

- Expanded `SKILL.md` trigger description and intervention map.
- New references for conflict/attachment, sex/desire, flirting/dating, source map, style, edge cases, and semantic triage.
- A kink-aware router that does not automatically safety-route every “choke” or “rape fantasy” mention.
- New pathways: desire discrepancy, erotic reset, pleasure equity, kink consent, flirting/dating, attachment cycle, connection-before-analysis, love languages, and non-monogamy.
- New worksheets: brakes/accelerators, desire discrepancy, erotic menu, pleasure debrief, kink consent map, flirting calibration, attachment cycle, love languages as care menu, and trust-repair observables.
- New evals for under-refusal, over-refusal, kink semantics, sex coaching, flirting, attachment cycles, and safety redirects.

## Known limitations

- This is not a clinical protocol, validated assessment, or substitute for trained support.
- Relationship advice is culturally situated; the skill should adapt to the user rather than impose a single ideal.
- Some books included here are influential rather than strongly validated. The skill should use them as practical lenses, not proof.
- Sexual advice can be misused if consent is ambiguous; v3 therefore keeps consent and adult context as hard requirements while avoiding unnecessary shame.
- The deterministic scripts are keyword and context heuristics. They help routing but do not replace judgement.
