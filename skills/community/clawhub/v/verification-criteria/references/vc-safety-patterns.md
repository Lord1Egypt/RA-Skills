# VC Safety Patterns

> Design patterns for safety-critical verification criteria (ASIL A–D). Derived from BMS and functional safety practice. Load when a requirement has an ASIL level.

---

## 1. Safety Margin Design (裕量设计)

Safety-critical VC must include explicit margins. A VC without margin is a VC that assumes zero measurement error, zero environmental variation, and zero aging drift — an unsafe assumption.

### Four Margin Dimensions

- **FTTI Margin**: response time must be below FTTI — e.g. FTTI=50ms → VC ≤45ms (10% margin)
- **Threshold Margin**: detection threshold vs. true danger threshold — e.g. 4.25V overvoltage vs. 4.50V thermal runaway
- **Tolerance Analysis**: account for sensor accuracy, jitter, ADC noise — e.g. ±50mV tolerance on 4.25V threshold
- **Robustness Verification**: must trigger when fault exists AND not trigger when no fault — e.g. 100 cycles at 4.20V→0 false triggers, 100 at 4.30V→100% trigger

### Margin Design Rule

> **Always reserve ≥ 10% margin below FTTI for the VC criterion.** The 10% accounts for measurement error, environmental variation, and part-to-part variance. If the project cannot achieve 10% margin, escalate — the architecture may need revision.

---

## 2. Double-100 Verification Principle (双百验证)

Safety-critical VCs must satisfy two symmetrical conditions simultaneously. Verifying only one side is insufficient for ASIL C/D.

```
         SAFETY VC
        /          \
   MUST TRIGGER    MUST NOT TRIGGER
   when fault      when no fault
   exists          exists
        |               |
   100% trigger     0 false triggers
   rate in N        in N normal
   fault trials     operation trials
```

### Formal Rule

- **Missed trigger**: fault exists → protection MUST activate — N≥100, trigger rate=100%
- **False trigger**: normal condition → protection MUST NOT activate — N≥100, trigger rate=0%

### Anti-Pattern

| ❌ Insufficient | ✅ Sufficient |
|----------------|--------------|
| "Overvoltage protection verified 10 times, all passed" | "Overvoltage: 100 fault injections → 100% trigger. 100 normal cycles → 0 false triggers. Repeated at operating domain boundaries (lower / nominal / upper per requirement)." |

---

## 3. Test Coverage Matrix for Safety VC

For safety requirements with multiple operating scenarios, a single pass/fail line is not enough. Use a **test coverage matrix** to systematically enumerate scenarios and expected behaviors.

### Matrix Template

```markdown
| Test Scenario | Fault Condition | Expected Behavior | Criterion | Temperature |
|--------------|----------------|-------------------|-----------|-------------|
| Normal       | {no fault}     | No warning/action | {duration} | 25°C |
| Marginal-Pass | {borderline, just above threshold} | No warning/action | {duration} | 25°C |
| Marginal-Fail | {borderline, just below/above threshold} | Warning/action | {time limit} | 25°C |
| Severe Fault | {deep into fault zone} | Warning/action | {tighter time limit} | 25°C |
| Gradual Degradation | {slowly crossing threshold} | Correct threshold detection | {consistency} | 25°C |
| Power-On Fault | {fault present at startup} | Detection at init | {init time limit} | -20°C, 60°C |
```

### BMS Example: Insulation Monitoring

```markdown
| Test Scenario | Insulation Resistance | Expected Behavior | Criterion |
|--------------|----------------------|-------------------|-----------|
| Normal       | 200 kΩ               | No warning        | Sustained 10 min |
| Marginal-Pass | 45 kΩ               | No warning        | Sustained 5 min |
| Marginal-Fail | 35 kΩ               | Warning active    | ≤ 500ms |
| Severe Fault | 10 kΩ                | Warning active    | ≤ 300ms |
| Gradual Degradation | 200→30 kΩ ramp | Warning triggers at 40 kΩ crossing | Threshold consistency ±5% |
| Power-On Fault | 20 kΩ at startup   | Warning within 1s | Initial detection ≤ 1s |
```

> **Key insight**: The matrix forces the engineer to think beyond the single "fault → protect" scenario and consider boundary cases, power-on state, and degradation paths.

---

## 4. BMS Safety VC Lessons Learned

These five lessons are distilled from BMS safety VC practice. They generalize to any safety-critical embedded system.

### L1: HIL is the Core Tool for Safety VC

Real-vehicle fault injection at high voltage/current is dangerous, destructive, and non-repeatable. HIL enables:
- Safe injection of electrical faults (overvoltage, short circuit, insulation failure)
- Exact repeatability across temperature cycles
- Automated regression of all fault scenarios

**Implication**: The VC must specify HIL configuration and fault injection method, not just "test on vehicle."

### L2: VC Is Part of the Safety Case

Every safety VC ultimately feeds into the Safety Case as evidence that safety goals are met. When writing a safety VC, ask: "Would this convince an independent safety assessor?"

**Implication**: Safety VCs should reference their parent safety goal (SG-XX) and the safety analysis artifact (HARA/FTA) that produced the FTTI.

### L3: Margin Thinking Is the Core Design Discipline

Safety VC is fundamentally about placing a confident engineering margin between:
- The detection/response threshold and the true danger point
- The required response time and the actual response time
- The measurement precision and the threshold gap

**Implication**: Never write a safety VC criterion at exactly the specification limit. Always insert margin — and document the margin rationale.

### L4: Test Across Temperature, Not Just at Room Temperature

Most electronic failures occur at temperature extremes. A protection mechanism that works at 25°C may fail at -40°C (slower response) or +85°C (drift in reference voltage).

**Implication**: Safety VCs must test at the requirement's own operating domain boundaries (lower, nominal, upper), not just nominal. The domain comes from the requirement or system-level specification — do not hardcode a fixed temperature list. Cold causes slower response times; hot causes reference voltage drift.

### L5: The VC Author Must Understand the Fault Physics

A safety VC that says "inject overvoltage" without specifying how (step? ramp? which cell? at what rate?) is incomplete. The VC author must understand:
- How the fault manifests physically (e.g. cell overvoltage from charger failure vs. regenerative braking overshoot)
- The difference between a hard step fault and a gradual drift fault
- Which fault injection method represents the worst-case scenario

**Implication**: Consult the functional safety engineer and hardware architect when writing safety VCs. Do not guess fault injection parameters.

---

## 5. Cross-References

- Use **Template C** in `assets/vc-template.md` for safety VC structured fields (ASIL, FTTI, fault injection, safe state confirmation)
- Use **SMARTR-OC** in `references/vc-smartr-oc.md` for quality scoring — pay special attention to **C (Complete)**: boundary and abnormal conditions are non-negotiable for safety VCs
- Escalate per SKILL.md **Requirement Maturity Gate**: if a safety VC cannot be written with adequate margin, the system architecture or safety concept may need revision
