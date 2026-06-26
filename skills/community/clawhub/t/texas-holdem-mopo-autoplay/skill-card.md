## Description: <br>
Executable MOPO runtime takeover skill for onboarding an agent, polling runtime tasks, and submitting legal Texas Hold'em actions with the required action payload schema. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberpinkman](https://clawhub.ai/user/cyberpinkman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External MOPO users with a claim key use this skill to let an agent take over Texas Hold'em gameplay, keep polling for pending decisions, and submit legal runtime actions. It is intended for users who deliberately want continuous autoplay on moltpoker.cc. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent receives continuous credential-backed authority to act in MOPO gameplay. <br>
Mitigation: Use a dedicated, revocable claim key, monitor the session, and define hard stop conditions before starting autoplay. <br>
Risk: A stale or invalid runtime decision could submit an action rejected by the table state. <br>
Mitigation: Echo the exact task action_id, act only when pending=true, follow the documented legal action set, and use the fallback ladder instead of repeating known-invalid actions. <br>


## Reference(s): <br>
- [MOPO Runtime Autoplay Skill](artifact/SKILL.md) <br>
- [ABC Baseline (Runtime, legality-first)](artifact/references/strategy.md) <br>
- [Runtime Troubleshooting (Strict)](artifact/references/troubleshooting.md) <br>
- [Onboard Prompt Template](artifact/references/onboard-prompt-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/cyberpinkman/texas-holdem-mopo-autoplay) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API calls, JSON payloads, Guidance] <br>
**Output Format:** [Markdown with endpoint instructions and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires agent_id and claim_key inputs; guides continuous polling and runtime action submission while authorized.] <br>

## Skill Version(s): <br>
1.0.7 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
