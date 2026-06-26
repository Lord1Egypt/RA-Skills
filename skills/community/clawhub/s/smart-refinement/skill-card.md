## Description: <br>
Smart Refinement System refines ambiguous user prompts, matches them against a local skill database, integrates context, and returns suggested execution steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[janussilence](https://clawhub.ai/user/janussilence) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to clarify underspecified user requests, identify relevant skill categories, and produce structured next-step guidance before an agent acts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested tools or execution steps may be inappropriate for the user's actual task if the original prompt is ambiguous. <br>
Mitigation: Treat suggestions as recommendations only, review the refined prompt, and ask for clarification before taking consequential actions. <br>
Risk: Context supplied to the refinement flow may contain secrets or sensitive project history. <br>
Mitigation: Avoid passing secrets or sensitive project history unless the user is comfortable with the host agent retaining it in session memory. <br>
Risk: The skill can recommend command, file, or network-related tool categories, but it does not enforce execution safety. <br>
Mitigation: Keep normal agent approval controls for command, file, and network actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/janussilence/smart-refinement) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Structured JSON-like Python dictionaries and Markdown execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include refined prompts, matched skill scores, suggested actions, integrated context, and processing statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
