# VC Definition Framework & Methodology Reference

> Condensed from ASPICE SYS.2 BP5 practice, INCOSE Handbook, ISO/IEC 29148.

## VC Definition (What, Why, When, Who)

**Verification Criteria (VC)** is a measurable, repeatable judgment condition that determines whether a system requirement has been met.

A qualified VC must answer three questions:
1. **What to verify**: Which aspect of which requirement?
2. **How to verify**: What method (Analysis/Inspection/Test/Demonstration)?
3. **Pass/Fail criterion**: What result counts as pass?

```
Requirement: "System shall respond to CAN wake-up signal within 500ms"
       ↓
VC:  "Under normal supply voltage (9V~16V), send CAN network wake-up frame via CAN tool,
      measure at ECU Wake-Up pin the time from frame transmission end to pin level rise,
      repeat 100 times, max ≤ 500ms, no single measurement > 550ms."
      ↑ What              ↑ How                         ↑ Criterion
```

> VC enables bidirectional traceability: Stakeholder Req → System Req → VC → Test Case → Test Result.

### When — VC Timing

| Timing | Approach | Consequence |
|--------|----------|-------------|
| ✅ Synchronous | Write VC simultaneously with requirement | Mutual calibration, built-in quality |
| ❌ Post-freeze | Batch-fill VC after requirement baseline | VC becomes a documentation task, disconnected from requirements |
| ❌ Testing phase | Test engineers reverse-derive VC | Requirement intent distorted, insufficient verification |

### Who — VC Ownership

- **Primary**: System Requirements Engineer (VC is part of requirement definition)
- **Reviewer**: Test Engineer (provides testability feedback)
- **Approver**: Technical lead / review committee
- **Consultant**: Functional safety engineer (for ASIL requirements)

## VC Classification System

### By Verification Method (4-Type Method)

- **Analysis** — mathematical models, simulation, calculation: thermal analysis, EMC simulation, WCA, reliability prediction
- **Inspection** — visual review, document review: connector selection, PCB layout, wiring check
- **Test** — running system/component under controlled conditions: functional, performance, durability, HIL/SIL
- **Demonstration** — actual operation walkthrough: UI workflow, maintenance accessibility, assembly feasibility

### By Requirement Type

- **Functional**: input-output behavior, state transitions — e.g. "Press SPORT → VehModeSt = 0x02 within 200ms, 10 reps, 0 failures"
- **Performance**: quantified metric + conditions + statistical method — e.g. "CAN load ≤ 50% at 500kbps, 1h avg"
- **Reliability**: confidence + sample size + failure criterion — e.g. "95% confidence, 80% reliability, 1000 cycles"
- **Timing**: start/end event + time window — e.g. "KL15 ON → HMI rendered ≤ 2.5s"
- **Safety (ASIL)**: safety goal + FTTI + safe state — e.g. "overvoltage → disconnect ≤ 50ms"
- **Interface**: signal + timing + data integrity — e.g. "CAN-FD 0x3A1: 20ms ±1ms avg, max ≤25ms, loss=0"

> SMARTR-OC 8-point scoring rubric → `references/vc-smartr-oc.md`

## VC-First Methodology — Four Layers

> L1 Mindset + L2 Principles → `../SKILL.md` §VC-First Methodology + §Key Principles

- **L3 Process**: Understand intent → Select method → Define criterion → Set conditions → Write VC → Self-check (SMARTR-OC) → Peer review
- **L4 Tools**: VC template library, quality checklist, verification method decision tree, classification reference

### Key Cognitive Shifts

| From (Traditional) | To (VC-First) |
|--------------------|---------------|
| "What should the system do?" | "How do we prove the system did it?" |
| Requirements frozen first, testing adapts later | Requirements and verification co-evolve |
| VC is test team's job | VC is requirement engineer's core responsibility |
| VC as documentation appendix | VC as integral part of requirement |
| Quality found in testing phase | Quality built-in at requirement definition phase |

> VC-First 7-step operating loop with mermaid diagram → `references/vc-workflow-a.md` §VC-First Operating Loop

## Traceability Chain

```
Stakeholder Req (SYS.1) → System Req (SYS.2) → VC (SYS.2 BP5) → Test Case (SYS.5) → Test Result
```

Every link must have bidirectional traceability. Breakage at any point = ASPICE non-conformance.
