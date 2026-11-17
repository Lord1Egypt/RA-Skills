# Diagnostic matrix

Follow the test order within the matching symptom category. Move to the next layer only after the current layer passes.

| Category | Typical symptom | Check order | Common hypotheses | Acceptance evidence |
| --- | --- | --- | --- | --- |
| `power` | No response, resets, or unstable operation | Battery condition -> connector polarity/fit -> controller power indicator -> voltage under load | Discharged battery, loose connector, overload, damaged wiring | Stable power during a low-load and motion test |
| `motion` | One or more wheels do not move | Mechanical binding -> individual servo test -> channel mapping -> controller command -> supply under load | Tight coupler, failed servo, wrong channel, insufficient current | Every servo moves independently and repeatably |
| `direction` | Cart drifts, spins, or moves in the wrong direction | Wheel orientation -> servo zero -> individual direction -> three-wheel vector mapping -> low-speed floor test | Reversed servo, inconsistent zero, incorrect wheel installation, mapping error | Straight, lateral, and turning commands match expected directions |
| `camera` | No image, frozen image, or high latency | USB connection -> device enumeration -> single-frame capture -> resolution/frame-rate -> application pipeline | Driver/device index error, bandwidth issue, blocked camera, processing delay | Repeated fresh frames with acceptable delay |
| `communication` | Agent produces a command but cart does not react | Direct controller command -> port/device availability -> permissions -> message format -> timeout/retry logs | Wrong port, protocol mismatch, permission problem, dropped messages | Same command reaches the controller repeatedly without errors |
| `agent` | Natural-language request is misunderstood | Raw user text -> model response -> structured plan -> schema validation -> controller translation | Ambiguous request, prompt drift, invalid plan, unit conversion error | A valid structured plan matches the intended movement |
| `obstacle` | Cart fails to avoid or stops unnecessarily | Camera view -> lighting/occlusion -> frame freshness -> detection result -> clearance threshold -> replanning | Blind area, stale frame, false detection, threshold error | Controlled obstacle tests lead to safe stop or reroute |

## Evidence discipline

Record each test as:

```text
Test:
Changed variable:
Observed result:
Pass/fail:
Next decision:
```

Use logs, images, measured values, and repeatable behavior where available. Label any unmeasured explanation as a hypothesis.

