---
name: trust
description: >
  Build, evaluate, repair, and strengthen trust across relationships, teams, clients,
  brands, communities, partnerships, and decision environments. Use when someone needs
  to understand what creates trust, what damages it, and how to design for credibility,
  reliability, and confidence over time.
---

# Trust

Trust is not a feeling by itself.

Trust is a judgment about risk.

People trust when they believe that:
- what is being said is likely true
- what is being promised is likely to happen
- what is being hidden is limited
- what happens under pressure will still be acceptable

Most trust problems are not caused by one dramatic betrayal.
They are caused by smaller patterns:
unclear expectations, inconsistent follow-through, missing context, selective disclosure,
defensiveness, unexplained changes, vague ownership, or signals that someone wants the upside
of trust without accepting the obligations that trust requires.

This skill helps make trust visible, diagnosable, and improvable.

## Trigger Conditions

Use this skill when the user needs to:
- build trust with clients, customers, teams, partners, or audiences
- understand why trust is weak, broken, or missing
- repair credibility after mistakes, delays, or confusion
- improve transparency, reliability, and expectation-setting
- evaluate whether a person, system, vendor, or process is trustworthy
- design communication or operating practices that increase confidence
- reduce suspicion, uncertainty, or relational friction
- turn vague trust concerns into practical action

Also trigger when the user says things like:
- "How do I build trust"
- "Why don't they trust us"
- "How do I regain credibility"
- "This relationship feels fragile"
- "How do I make this more trustworthy"
- "What creates trust here"
- "How do I reduce skepticism"

## Core Principle

Trust grows when uncertainty is handled well.

People do not need perfection.
They need believable signals that reality is being handled honestly, competently,
and consistently.

A trustworthy system makes it easier for others to predict:
- what will happen
- what will not happen
- who is responsible
- how problems will be handled
- whether words and actions align

## What This Skill Does

This skill helps:
- define the trust problem clearly
- identify the signals that increase or damage trust
- separate competence, honesty, transparency, and consistency
- diagnose trust breakdowns in relationships or systems
- improve credibility through communication and follow-through
- design practices that make trust easier to earn and maintain
- create repair strategies when trust has weakened

## Default Outputs

Depending on the request, produce one or more of the following:

1. Trust Diagnosis  
A structured analysis of what is weakening, maintaining, or building trust.

2. Trust-Building Plan  
A practical set of changes to communication, behavior, or system design.

3. Trust Repair Strategy  
A recovery plan after a mistake, inconsistency, delay, or credibility hit.

4. Trust Signal Map  
A breakdown of visible signals that influence confidence and skepticism.

5. Credibility Framework  
A model for improving reliability, transparency, and perceived integrity.

6. Decision Trust Review  
An assessment of whether a process, offer, system, or relationship feels trustworthy enough to proceed.

## Response Rules

When responding:
- define who must trust whom, and about what
- identify the risk underneath the trust question
- separate trust in intent from trust in competence
- separate trust signals from trust claims
- focus on observable behavior, not vague reassurance
- distinguish prevention from repair
- prefer specific commitments over broad promises
- make the next trust-building step concrete

## Trust Architecture
~~~python
TRUST_ARCHITECTURE = {
  "core_elements": {
    "parties": "Who is being asked to trust whom",
    "risk": "What uncertainty or downside makes trust necessary",
    "competence": "Whether the actor can actually do what is expected",
    "integrity": "Whether words, incentives, and actions align",
    "transparency": "Whether important information is surfaced appropriately",
    "consistency": "Whether behavior is stable enough to predict",
    "repairability": "Whether problems are acknowledged and handled well"
  },
  "guiding_questions": [
    "What exactly needs to be trusted",
    "What risk is the other side taking",
    "What signals reduce or increase that risk",
    "Where are words and actions misaligned",
    "What pattern is causing doubt",
    "What would make confidence rational here"
  ]
}
~~~

## Trust Workflow
~~~python
TRUST_WORKFLOW = {
  "step_1_define_context": {
    "purpose": "Clarify the relationship or system in question",
    "examples": [
      "client relationship",
      "team leadership",
      "partnership discussion",
      "brand communication",
      "product promise",
      "vendor evaluation",
      "internal change management"
    ]
  },
  "step_2_define_risk": {
    "purpose": "Identify why trust matters here",
    "examples": [
      "financial risk",
      "time risk",
      "reputational risk",
      "emotional risk",
      "privacy risk",
      "performance risk",
      "dependency risk"
    ]
  },
  "step_3_identify_signals": {
    "purpose": "Find the behaviors and structures shaping trust",
    "examples": [
      "clear expectation setting",
      "reliable follow-through",
      "honest limitation disclosure",
      "visible ownership",
      "consistency under stress",
      "responsiveness",
      "admission of mistakes"
    ]
  },
  "step_4_find_breakdowns": {
    "purpose": "Diagnose what is weakening trust",
    "examples": [
      "missed commitments",
      "unclear communication",
      "changing stories",
      "hidden tradeoffs",
      "defensiveness",
      "no accountability path",
      "overpromising"
    ]
  },
  "step_5_design_response": {
    "purpose": "Improve or repair trust practically",
    "outputs": [
      "clearer commitments",
      "more transparent updates",
      "visible ownership",
      "boundary clarification",
      "repair statement",
      "new follow-through process"
    ]
  },
  "step_6_reinforce_over_time": {
    "purpose": "Make trust durable rather than performative",
    "methods": [
      "repeatable review cadence",
      "visible metrics or proof",
      "faster correction loops",
      "better expectation management",
      "reduced ambiguity",
      "consistency across touchpoints"
    ]
  }
}
~~~

## Common Trust Contexts
~~~python
TRUST_CONTEXTS = {
  "client_trust": {
    "use_when": "A client must believe the provider is competent, honest, and reliable",
    "focus": ["expectation clarity", "delivery consistency", "transparency", "issue handling"]
  },
  "team_trust": {
    "use_when": "People must rely on each other internally",
    "focus": ["ownership", "predictability", "candor", "follow-through", "fairness"]
  },
  "brand_trust": {
    "use_when": "An audience must believe what a brand says and promises",
    "focus": ["credibility", "consistency", "message-action alignment", "proof"]
  },
  "partnership_trust": {
    "use_when": "Two parties need confidence in mutual intent and execution",
    "focus": ["incentive alignment", "decision transparency", "role clarity", "risk sharing"]
  },
  "system_trust": {
    "use_when": "A process, tool, or institution must feel dependable",
    "focus": ["explainability", "consistency", "error handling", "accountability", "safeguards"]
  }
}
~~~

## Trust Logic
~~~python
TRUST_LOGIC = {
  "principles": [
    "Trust is earned through pattern, not slogan",
    "Transparency without competence does not create confidence",
    "Competence without honesty creates fragility",
    "Small inconsistencies compound into skepticism",
    "Repair begins with acknowledgment before reassurance",
    "People trust systems that make failure visible and manageable"
  ],
  "common_failures": [
    "Overpromising to gain short-term confidence",
    "Using reassurance instead of evidence",
    "Explaining too little when uncertainty rises",
    "Hiding delays or tradeoffs",
    "No clear owner when problems happen",
    "Trying to defend credibility instead of rebuilding it"
  ],
  "corrections": [
    "Reduce promises to what can be delivered",
    "State limits and unknowns clearly",
    "Make ownership visible",
    "Acknowledge mistakes early",
    "Show evidence of correction",
    "Align messaging with actual operating reality"
  ]
}
~~~

## Trust Output Format

### Trust Summary
- Trust Context:
- Parties Involved:
- Core Risk:
- Trust Signals Present:
- Trust Signals Missing:
- Main Breakdown Points:
- Recommended Repair or Strengthening Actions:
- Evidence or Proof Needed:
- Recommended Next Step:

## Boundaries

This skill helps analyze and improve trust, credibility, transparency, and confidence.

It does not replace legal, compliance, HR, regulatory, clinical, security, or formal risk advice.
For high-stakes disputes, investigations, or regulated contexts, outputs should be adapted
to the user's jurisdiction, internal policies, and professional obligations.

## Quality Check Before Delivering

- [ ] The trust context is clearly defined
- [ ] The underlying risk is identified
- [ ] Competence, honesty, and consistency are distinguished
- [ ] Observable trust signals are identified
- [ ] Repair or strengthening actions are practical
- [ ] Output avoids vague reassurance
- [ ] The next step is concrete
