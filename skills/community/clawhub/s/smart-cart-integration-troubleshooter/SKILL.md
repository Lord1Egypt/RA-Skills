---
name: smart-cart-integration-troubleshooter
description: Diagnose and document assembly, calibration, deployment, communication, camera, motion, and obstacle-avoidance problems for a lightweight OpenClaw smart cart using a 12V battery, a multi-channel servo controller, three ST3215 servos, omnidirectional wheels, and a USB camera. Use for symptom triage, safe test sequencing, root-cause isolation, acceptance checks, and repeatable integration-test reports.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🧰"
---

# Smart Cart Integration Troubleshooter

Turn a cart symptom into a safe, evidence-based diagnostic sequence. Separate confirmed observations from hypotheses and test one variable at a time.

## Workflow

1. Read [references/project-baseline.md](references/project-baseline.md) to anchor the diagnosis to the actual project configuration.
2. Classify the symptom as `power`, `motion`, `direction`, `camera`, `communication`, `agent`, or `obstacle`.
3. Apply the safety gate before touching hardware: stop motion, isolate the 12V supply when changing wiring, secure or lift the chassis for wheel tests, and keep hands clear of moving parts.
4. Collect the minimum evidence needed: command issued, visible response, battery/controller state, relevant logs, camera status, and whether the fault is repeatable.
5. Read [references/diagnostic-matrix.md](references/diagnostic-matrix.md) for likely causes and the required test order.
6. Diagnose from the lowest layer upward: mechanical and power, controller and servo, camera/driver, communication, then OpenClaw/LLM planning.
7. Generate a checklist with `python3 scripts/make_checklist.py CATEGORY` when file execution is available.
8. Return a report with symptom, confirmed facts, hypotheses, numbered tests, expected results, stop conditions, likely fix, and final acceptance test.

## Diagnostic Rules

- Never treat a hypothesis as a confirmed cause.
- Never change multiple wiring, calibration, and software variables in the same test.
- Never recommend bypassing protection, operating damaged batteries, or probing live wiring without suitable training and equipment.
- Stop immediately for battery swelling, overheating, smoke, damaged insulation, short-circuit signs, uncontrolled motion, or repeated controller resets.
- Do not blame the large model until power, mechanics, device enumeration, direct controller commands, and communication have been checked.
- Do not invent controller protocols, pin assignments, serial ports, API responses, or sensor values not present in the evidence.

## Output Template

Use this order:

1. `故障现象`
2. `已确认事实`
3. `可能原因（按优先级）`
4. `排查步骤` with one change and one expected result per step
5. `立即停止条件`
6. `建议修复`
7. `验收测试`

## Example

For `发出前进指令后，小车原地打转`, first verify wheel installation and mechanical binding, then test each servo independently, check zero-position calibration and direction mapping, and finally run a low-speed straight-line acceptance test. See [examples/sample-diagnosis.md](examples/sample-diagnosis.md).

