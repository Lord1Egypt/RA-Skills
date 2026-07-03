## Description: <br>
Unified subscription router for the AI builders digest and the pharma investment digest. Use when the agent should proactively offer subscriptions on session start, remember user choices, and route onboarding into follow-builders or med-builders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spzwin](https://clawhub.ai/user/spzwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to present one startup subscription choice for AI builders and pharma investment digests, remember the user's preference, and route onboarding to the selected downstream digest skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic startup subscription prompts can interrupt normal task flow or continue after a user no longer wants them. <br>
Mitigation: Review the skill before installing, keep the prompt short, and honor the documented snooze and dismiss choices before prompting again. <br>
Risk: The skill stores topic, locale, cadence, and delivery preferences in local subscription state. <br>
Mitigation: Explain where state is stored before writing it, provide inspect and opt-out paths, and avoid collecting unnecessary preference details. <br>
Risk: The artifact documents Node helper commands for startup hooks and state management, so missing or changed helper scripts can break routing. <br>
Mitigation: Verify the installed package includes the expected helper scripts before enabling session-start integration. <br>


## Reference(s): <br>
- [JSON Schema draft 2020-12](https://json-schema.org/draft/2020-12/schema) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON-compatible state payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and persists subscription choices, locale, cadence, and delivery defaults in local subscription state.] <br>

## Skill Version(s): <br>
1.0.11 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
