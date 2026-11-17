# VC Table Template

> Copy-paste ready. Replace bracketed placeholders with actual values.

## Standard VC Table

```markdown
| VC ID | Linked Requirement | Verification Method | Test Conditions | Measurement Target | Pass/Fail Criterion |
|-------|-------------------|---------------------|-----------------|--------------------|---------------------|
| VC-[REQ-ID]-001 | [REQ-ID] ([brief description]) | [Test / Analysis / Inspection / Demonstration] | Rig: [HIL/SIL/Vehicle]<br>Equipment: [name, precision]<br>Environment: [Temp range, Voltage range]<br>Precondition: [state]<br>**Sequence** (if needed): ① [step] → ② [step] → ③ [step] | [Signal name, variable, behavior to measure] | [Quantified threshold]: [≤ / ≥ / =] [value] [unit]<br>Statistical: [max / avg / 99th percentile]<br>Sample: [N] repetitions, [0] failures allowed |
```

## Example (BMS Cell Voltage Accuracy)

```markdown
| VC ID | Linked Requirement | Verification Method | Test Conditions | Measurement Target | Pass/Fail Criterion |
|-------|-------------------|---------------------|-----------------|--------------------|---------------------|
| VC-BMS-001 | BMS-001 (Cell voltage acquisition accuracy) | Test | Rig: BMS HIL + programmable cell voltage simulator (accuracy ≤1mV)<br>Temp: -40°C, 25°C, 85°C<br>Precondition: Inject known reference voltage to all cell channels | ADC sampled value vs. injected reference per channel | All channels: \|sampled - reference\| ≤ 5mV<br>Sampling period: adjacent samples ≤ 100ms<br>N=100 per temperature point, max error across all ≤ 5mV |
```

## Example (CAN Communication)

```markdown
| VC ID | Linked Requirement | Verification Method | Test Conditions | Measurement Target | Pass/Fail Criterion |
|-------|-------------------|---------------------|-----------------|--------------------|---------------------|
| VC-COMM-003 | COMM-003 (Radar target list transmission) | Test | Rig: CAN-FD bus monitor between radar and domain controller<br>Rate: 2Mbps<br>Duration: 10 min | Target list message ID 0x3A1 transmission period | Period: avg 20ms ±1ms<br>Max interval ≤ 25ms<br>Frame loss rate = 0 |
```

## Example (Functional Safety - Overvoltage Protection)

```markdown
| VC ID | Linked Requirement | Verification Method | Test Conditions | Measurement Target | Pass/Fail Criterion |
|-------|-------------------|---------------------|-----------------|--------------------|---------------------|
| VC-SAF-007 | SAF-007 (Overvoltage protection disconnect) | Test | Rig: HIL with programmable power supply<br>Fault: Inject VBAT step from 12V to 20V<br>Monitor: main relay control signal | Time from overvoltage detection to relay open command | Disconnect time ≤ 50ms<br>N=100 repetitions, 0 failures<br>0 false triggers at normal voltage |
```

## Empty Template (5 Rows)

> 使用时将 `[METHOD]` 替换为 `Test` / `Analysis` / `Inspection` / `Demonstration` 之一——**不默认选 Test**，按需求类型匹配（见 SKILL.md §Mode A 验证方法决策树或下方 Type-Specific Templates）。

```markdown
| VC ID | Linked Requirement | Verification Method | Test Conditions | Measurement Target | Pass/Fail Criterion |
|-------|-------------------|---------------------|-----------------|--------------------|---------------------|
| VC- |  | [METHOD] | Rig: <br>Temp: <br>Precondition:  |  | : ≤ <br>Sample: N=, failures=0 |
| VC- |  | [METHOD] | Rig: <br>Temp: <br>Precondition:  |  | : ≤ <br>Sample: N=, failures=0 |
| VC- |  | [METHOD] | Rig: <br>Temp: <br>Precondition:  |  | : ≤ <br>Sample: N=, failures=0 |
| VC- |  | [METHOD] | Rig: <br>Temp: <br>Precondition:  |  | : ≤ <br>Sample: N=, failures=0 |
| VC- |  | [METHOD] | Rig: <br>Temp: <br>Precondition:  |  | : ≤ <br>Sample: N=, failures=0 |
```

---

## Type-Specific Structured Templates

Choose the template that matches the requirement type. Fill in all fields; delete fields that don't apply.

### Template A: Functional Behavior VC

> Use for: state transitions, mode switching, logic evaluation, functional behavior requirements.

```markdown
**VC-FUNC-{REQ-ID}-{seq}**

| Field | Content |
|-------|---------|
| **Linked Requirement** | {REQ-ID} — {brief description} |
| **Verification Method** | Test / Demonstration |
| **Preconditions** | {system state: e.g. KL15 ON, gear = P, vehicle speed = 0 km/h} |
| **Trigger Event** | {the event that initiates the behavior: e.g. driver presses SPORT button} |
| **Measurement Means** | {how to observe: e.g. CAN tool monitoring VehModeSt signal ID 0x1A2 Byte 2} |
| **Expected Behavior** | {what should happen: e.g. signal value changes to 0x02 (SPORT), IC indicator illuminates} |
| **Timing Requirement** | {if applicable: e.g. within 200ms of trigger} |
| **Pass/Fail Criterion** | {quantified: e.g. signal = 0x02 within 200ms, indicator ON} |
| **Repetitions** | {N times, e.g. 20 repetitions, 100% pass rate} |
```

### Template B: Performance / Timing VC

> Use for: response time, startup time, latency, throughput, any time-based or rate-based requirement.

```markdown
**VC-PERF-{REQ-ID}-{seq}**

| Field | Content |
|-------|---------|
| **Linked Requirement** | {REQ-ID} — {brief description} |
| **Verification Method** | Test / Analysis |
| **Environmental Conditions** | {temperature, supply voltage, etc.} |
| **Start Event** | {precise definition: e.g. KL15 signal rising edge (V > 6V)} |
| **End Event** | {precise definition: e.g. HMI first frame fully rendered (light sensor detects > 80% target brightness)} |
| **Measurement Equipment** | {device + precision: e.g. high-speed camera 1000fps + light sensor response < 1ms} |
| **Measurement Target** | {what is measured: e.g. time interval from start to end event} |
| **Statistical Method** | {max / avg / min / Cpk / 99th percentile} |
| **Pass/Fail Criterion** | {quantified: e.g. max ≤ 2.5s, avg ≤ 2.0s, no single > 3.0s} |
| **Sample Size** | {N repetitions: e.g. 50 consecutive measurements} |
```

### Template C: Safety Requirement VC (ASIL)

> Use for: functional safety requirements with ASIL level, safety goals, and FTTI.

```markdown
**VC-SAFE-{REQ-ID}-{seq}**

| Field | Content |
|-------|---------|
| **Linked Requirement** | {REQ-ID} — {brief description} |
| **ASIL** | {QM / A / B / C / D} |
| **Safety Goal** | {SG-XX — description} |
| **FTTI** | {fault tolerant time interval in ms} |
| **Verification Method** | Test (fault injection) + Analysis (if dual verification required) |
| **Fault Injection Method** | {how to inject: e.g. programmable power supply injects overvoltage on Cell-5} |
| **Fault Condition** | {the specific fault: e.g. Vcell = 4.30V, exceeding 4.25V threshold} |
| **Sequence** (if needed, see `vc-sequence-guide.md`) | {execution order for multi-scenario/causal-chain: ① baseline → ② inject fault(a) → ③ verify response → ④ recover → ⑤ repeat for (b)(c)} |
| **Safety Mechanism** | {what should happen: e.g. BMS opens main contactor} |
| **Measurement Target** | {signals to monitor: e.g. contactor coil drive signal, main circuit current sensor} |
| **Response Time Criterion** | {≤ FTTI minus margin: e.g. T(Vcell ≥ 4.25V → contactor de-energized) ≤ 45ms (50ms FTTI, 5ms margin)} |
| **Safe State Confirmation** | {how to confirm: e.g. main circuit current drops to 0A within 20ms of contactor opening} |
| **False Trigger Check** | {must NOT trigger under normal conditions: e.g. 100 cycles at normal voltage 4.20V, 0 false triggers} |
| **Missed Trigger Check** | {must trigger under fault conditions: e.g. 100 cycles at fault voltage 4.30V, 100% trigger rate} |
| **Sample Size** | {per test scenario: e.g. 100 repetitions each for response time, false trigger, missed trigger} |
| **References** | {standards: e.g. ISO 26262-4:2018 Table 7} |
```

### Template D: Interface / Communication VC

> Use for: bus communication, signal interfaces, protocol conformance requirements.

```markdown
**VC-IF-{REQ-ID}-{seq}**

| Field | Content |
|-------|---------|
| **Linked Requirement** | {REQ-ID} — {brief description} |
| **Verification Method** | Test |
| **Bus / Interface Type** | {CAN / CAN-FD / LIN / Ethernet / SPI / I2C} |
| **Bus Rate** | {e.g. 500 kbps, 2 Mbps} |
| **Monitored Message** | {ID + name: e.g. ID 0x3A1 — Target List} |
| **Monitoring Window** | {duration: e.g. 10 minutes continuous} |
| **Measurement Target** | {what to check: e.g. transmission period, data integrity, checksum} |
| **Period Criterion** | {e.g. avg 20ms ±1ms} |
| **Max Interval Criterion** | {e.g. max single interval ≤ 25ms} |
| **Frame Loss Rate** | {e.g. = 0, or ≤ 0.01%} |
| **Data Correctness** | {e.g. all signal values within defined range, checksum valid} |
```

---

## Pass/Fail Criterion Decomposition

A well-formed criterion must address three sub-elements. Do not conflate them — each serves a distinct purpose:

| # | Sub-Element | Purpose | Format Example |
|---|------------|---------|---------------|
| **Threshold** | The numeric boundary between pass and fail | `≤ 100ms`, `≥ 95%`, `= 0`, `± 5mV` |
| **Statistical method** | How to draw a conclusion from multiple measurements | `max value ≤ X across N trials`, `Cpk ≥ 1.33`, `avg ± 3σ within bounds` |
| **Precision requirement** | Required accuracy of measurement equipment relative to the threshold | `using current probe with ±1% accuracy`, `oscilloscope sampling ≥ 1kHz` |

> **Why separate statistical method from threshold?** Writing `"response time ≤ 100ms"` without specifying whether that's a single-trial max, an average, or a 99th percentile is ambiguous and not repeatable.

### Threshold Sources

When justifying a threshold value, cite one of three sources:

| Source | Description | Example |
|--------|-------------|---------|
| **Standard / Regulation driven** | Mandated by GB/T, ISO, ECE, or other normative documents | ECE R13 stopping distance, ISO 26262 FTTI tables |
| **System architecture derived** | Derived from safety analysis (FMEA/FTA) or architecture constraints | FTTI from HARA, voltage tolerance from WCA |
| **Engineering benchmark** | Based on competitive analysis, historical project data, or expert judgment | "Competitor X achieves 2.0s; we target ≤ 2.5s" |

> If a threshold cannot be traced to any of these three sources, flag it 🟠 **VC-ASSUMPTION** and escalate.

---

## Test Conditions Decomposition

Use these five sub-dimensions as a mandatory checklist — sample size and time window are the two most frequently forgotten:

| # | Sub-Dimension | Must Answer | Example |
|---|--------------|-------------|---------|
| **Environmental** | What temperature, humidity, voltage, EMC conditions? | `-40°C to 85°C, 9V–16V supply` |
| **Preconditions** | What system state must be established first? | `KL15 ON, vehicle speed = 0 km/h, gear = P` |
| **Equipment** | What rig + measurement devices + their precision? | `BMS HIL + programmable cell voltage simulator (±1mV)` |
| **Sample size** | How many repetitions? What statistical confidence? | `100 repetitions, 95% confidence` |
| **Time window** | What start/end events define the measurement window? | `from KL15 rising edge to HMI first frame rendered` |

---

## Good vs Bad VC

**✅ Good VC:**

| VC ID | Linked Req | Method | Test Conditions | Target | Criterion |
|-------|-----------|--------|-----------------|--------|-----------|
| VC-BMS-001 | BMS-001 (Cell voltage accuracy) | Test | Rig: BMS HIL + programmable cell voltage simulator (accuracy ≤1mV)<br>Temp: -40°C, +25°C, +85°C<br>Precondition: Inject known reference voltage to all cell channels | ADC sampled value vs. injected reference per channel | All channels: \|sampled - reference\| ≤ 5mV<br>Sampling period: adjacent samples ≤ 100ms<br>N=100 per temperature point, max error across all ≤ 5mV |

**❌ Bad VC:**

| VC ID | Linked Req | Method | Test Conditions | Target | Criterion |
|-------|-----------|--------|-----------------|--------|-----------|
| VC-001 | Voltage acquisition | Test | Lab | Voltage | Accuracy meets requirements |

> The bad VC fails on every element: equipment unspecified, conditions unqualified, criterion has no numeric value.
