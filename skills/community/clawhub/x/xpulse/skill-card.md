## Description: <br>
Xpulse scans X/Twitter via DuckDuckGo for prediction-market signals, filters them with local Qwen materiality checks, and alerts only on signals that match active Kalshi positions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingmadellc](https://clawhub.ai/user/kingmadellc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External prediction-market traders and OpenClaw agents use Xpulse to monitor configured X/Twitter topics, filter social signals for novelty and materiality, and surface alerts tied to active Kalshi positions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Kalshi position metadata and uses a configured private key file for read-only position matching. <br>
Mitigation: Protect the Kalshi private key file, restrict local file permissions, and use credentials appropriate for read-only monitoring. <br>
Risk: Configured topics and derived trading context are used in DuckDuckGo searches and local Ollama prompts. <br>
Mitigation: Avoid sensitive topic names, run Ollama locally in a trusted environment, and review configuration before scheduled use. <br>
Risk: Recent signal cache and alert history are kept under the local OpenClaw state directory. <br>
Mitigation: Protect the user profile directory and periodically clear cache or history files when monitored topics or trading context are sensitive. <br>


## Reference(s): <br>
- [Xpulse on ClawHub](https://clawhub.ai/kingmadellc/xpulse) <br>
- [Materiality Gate](references/materiality-gate.md) <br>
- [Position Matching](references/position-matching.md) <br>
- [Ollama](https://ollama.ai) <br>
- [Kalshi](https://kalshi.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text alerts, JSON cache/history files, and markdown setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fail-closed filtering prefers suppressing uncertain signals over sending noisy alerts.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
