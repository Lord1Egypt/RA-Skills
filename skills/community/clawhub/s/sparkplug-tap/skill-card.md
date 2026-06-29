## Description: <br>
Consumes MQTT, Sparkplug B, and Unified Namespace data for bounded reads, decoded Sparkplug samples, node and device discovery, UNS browsing, and an off-by-default governed publish path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OT engineers use this skill to inspect MQTT/Sparkplug/UNS telemetry, decode captured Sparkplug B payloads, discover nodes and devices, and browse namespace topics through ot-aiops. It is consume-first; publish actions should remain in dry-run unless authorized for control changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connecting an agent to MQTT, Sparkplug, or UNS brokers can expose operational telemetry if used outside approved environments. <br>
Mitigation: Install and configure the skill only for authorized brokers and use approved endpoints, TLS, and scoped credentials. <br>
Risk: Publishing MQTT or Sparkplug command messages can change live control-system behavior when dry-run is disabled. <br>
Mitigation: Keep publish actions in dry-run unless change control, authorization, and topic safety have been confirmed. <br>


## Reference(s): <br>
- [Sparkplug Tap on ClawHub](https://clawhub.ai/zw008/skills/sparkplug-tap) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON result shapes and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bounded MQTT reads and samples; publish guidance defaults to dry-run.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
