---
name: qualify
description: >
  Qualify leads, prospects, clients, candidates, projects, opportunities, and requests
  before deeper time, money, or effort is committed. Use when someone needs to decide
  what is worth pursuing, what should be filtered out, and what criteria should govern
  that decision.
---

# Qualify

Qualification is the discipline of deciding what deserves pursuit.

Most wasted effort does not come from poor execution.
It comes from pursuing the wrong things too far.

People spend time on leads that will not buy, clients they cannot serve well,
projects that should never have started, candidates who are not a fit, and requests
that create complexity without return.

This skill helps define, apply, and improve qualification logic so effort goes where it matters.

## Trigger Conditions

Use this skill when the user needs to:
- qualify leads before sales effort
- decide which prospects are worth outreach
- screen candidates before interviews
- assess whether a client, project, or request is a fit
- define go/no-go criteria
- reduce wasted effort on weak opportunities
- improve intake or filtering logic
- separate promising opportunities from distracting noise

Also trigger when the user says things like:
- "How do I qualify this"
- "What makes this worth pursuing"
- "Should we take this client"
- "How do I screen better"
- "What criteria should I use"
- "How do I filter out bad fits"
- "I need a qualification framework"

## Core Principle

Qualification is not about saying no more often.

It is about saying yes more intelligently.

A good qualification system does three things:
- identifies fit
- identifies readiness
- identifies whether the expected return justifies the effort

The goal is not to eliminate uncertainty.
The goal is to stop avoidable misallocation.

## What This Skill Does

This skill helps:
- define qualification criteria before effort is invested
- separate fit, timing, value, and risk
- create go/no-go logic for opportunities and requests
- identify disqualifiers early
- improve screening and filtering systems
- reduce false positives
- route better opportunities into deeper workflows

## Default Outputs

Depending on the request, produce one or more of the following:

1. Qualification Framework  
A structured set of criteria showing what counts as qualified and why.

2. Qualification Scorecard  
A practical model for comparing opportunities or requests on explicit dimensions.

3. Go/No-Go Logic  
A decision rule for whether something should be pursued, paused, rejected, or escalated.

4. Disqualifier Map  
A list of early warning signs and conditions that should stop pursuit.

5. Screening Workflow  
A stage-by-stage process for filtering items before deeper commitment.

6. Qualification Audit  
A diagnosis of where the current qualification logic is too loose, too rigid, or poorly applied.

## Response Rules

When responding:
- define what is being qualified
- identify the desired downstream outcome
- separate fit from timing
- separate value from urgency
- identify disqualifiers early
- make criteria explicit rather than intuitive
- reduce wasted effort and false positives
- favor usable judgment over fake precision

## Qualification Architecture
~~~python
QUALIFICATION_ARCHITECTURE = {
  "core_elements": {
    "object": "What is being qualified",
    "desired_outcome": "What success would look like if pursued",
    "fit": "How well the item matches the need, offer, or system",
    "readiness": "Whether now is a viable time to proceed",
    "value": "Why the item is worth pursuing if successful",
    "risk": "What may make pursuit costly, unstable, or low quality",
    "disqualifiers": "Conditions that should stop or delay pursuit"
  },
  "guiding_questions": [
    "What are we deciding yes or no to",
    "What makes this a fit or non-fit",
    "Is the opportunity real or only theoretical",
    "What signals readiness or lack of readiness",
    "What effort would pursuit require",
    "What would make this low quality even if technically possible"
  ]
}
~~~

## Qualification Workflow
~~~python
QUALIFICATION_WORKFLOW = {
  "step_1_define_object": {
    "purpose": "Clarify what is being screened",
    "examples": [
      "lead",
      "prospect",
      "client request",
      "candidate",
      "project",
      "partnership opportunity"
    ]
  },
  "step_2_define_outcome": {
    "purpose": "Clarify why qualification matters",
    "examples": [
      "worth a sales call",
      "worth custom proposal effort",
      "worth an interview round",
      "worth onboarding",
      "worth strategic attention"
    ]
  },
  "step_3_define_fit_criteria": {
    "purpose": "Identify stable characteristics that matter",
    "examples": [
      "budget or spending ability",
      "problem relevance",
      "scope match",
      "segment fit",
      "capability match",
      "decision-maker alignment"
    ]
  },
  "step_4_define_readiness_signals": {
    "purpose": "Identify whether this should be pursued now",
    "examples": [
      "active pain",
      "timeline pressure",
      "clear need",
      "stakeholder engagement",
      "available resources",
      "decision timeline"
    ]
  },
  "step_5_define_disqualifiers": {
    "purpose": "Prevent avoidable wasted effort",
    "examples": [
      "wrong use case",
      "misaligned expectations",
      "no buying authority",
      "no urgency",
      "economically weak fit",
      "delivery risk too high",
      "history of instability"
    ]
  },
  "step_6_route_decision": {
    "purpose": "Turn qualification into action",
    "destinations": [
      "pursue now",
      "nurture later",
      "pause",
      "reject",
      "escalate for review"
    ]
  }
}
~~~

## Common Qualification Types
~~~python
QUALIFICATION_TYPES = {
  "sales_qualification": {
    "use_when": "Deciding whether a lead or opportunity deserves sales effort",
    "focus": ["fit", "need", "budget", "authority", "timing", "conversion likelihood"]
  },
  "client_qualification": {
    "use_when": "Deciding whether to take on a client or engagement",
    "focus": ["fit", "scope realism", "expectation alignment", "economics", "delivery risk"]
  },
  "candidate_qualification": {
    "use_when": "Screening people before deeper recruiting effort",
    "focus": ["role fit", "motivation", "readiness", "capability", "risk", "practical constraints"]
  },
  "project_qualification": {
    "use_when": "Deciding whether a project is worth starting or prioritizing",
    "focus": ["strategic fit", "resource load", "expected return", "dependencies", "execution risk"]
  },
  "request_qualification": {
    "use_when": "Filtering incoming requests, asks, or opportunities",
    "focus": ["importance", "fit", "urgency", "cost to fulfill", "tradeoffs"]
  }
}
~~~

## Qualification Logic
~~~python
QUALIFICATION_LOGIC = {
  "principles": [
    "A possible fit is not the same as a good fit",
    "Readiness matters as much as relevance",
    "Disqualifying early preserves capacity",
    "The cost of a false positive is often underestimated",
    "Not every good opportunity is a good opportunity now",
    "Qualification should simplify later decisions, not replace them"
  ],
  "common_failures": [
    "Pursuing anything that looks interesting",
    "Confusing politeness or curiosity with intent",
    "Ignoring economic or delivery reality",
    "No explicit disqualifiers",
    "Letting exceptions become the normal standard",
    "Qualifying too late after custom effort is already spent"
  ],
  "corrections": [
    "State criteria before evaluating cases",
    "Separate fit, timing, and value",
    "Make disqualifiers visible",
    "Create pause and nurture paths instead of only yes/no",
    "Tighten screening before expensive effort begins"
  ]
}
~~~

## Qualification Output Format

### Qualification Summary
- Object Being Qualified:
- Desired Outcome:
- Fit Criteria:
- Readiness Signals:
- Value Indicators:
- Disqualifiers:
- Decision Paths:
- Risks or Ambiguities:
- Recommended Next Step:

## Boundaries

This skill helps define qualification logic, screening criteria, and go/no-go decisions.

It does not replace legal, compliance, HR, procurement, medical, financial, or regulatory judgment.
For regulated or high-stakes decisions, outputs should be adapted to the user's jurisdiction,
industry requirements, and internal approval processes.

## Quality Check Before Delivering

- [ ] The object being qualified is clearly defined
- [ ] Fit and readiness are separated
- [ ] Disqualifiers are explicit
- [ ] Decision paths are actionable
- [ ] Criteria reduce wasted effort
- [ ] Output is practical rather than abstract
- [ ] The next step is concrete
