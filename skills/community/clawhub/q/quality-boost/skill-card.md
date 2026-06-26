## Description: <br>
Provides Chinese prompt-engineering checklists, templates, and evaluation methods for improving large language model answer quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jx-76](https://clawhub.ai/user/jx-76) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to apply quality rules, prompt templates, and self-check workflows that reduce hallucination, drift, verbosity, omissions, and unwanted additions in model responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Global auto-apply or systemPrompt prepend configuration can change the style and flow of all future agent responses. <br>
Mitigation: Review the prompt first, note or back up the OpenClaw configuration, and test the manual quick-apply templates before enabling global behavior. <br>
Risk: Strict quality rules may constrain tasks that intentionally need creative freedom, brainstorming, or role-play. <br>
Mitigation: Use manual application for those tasks or disable the skill when the artifact's stated non-applicable scenarios match the user workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jx-76/quality-boost) <br>
- [Primary skill documentation](artifact/SKILL.md) <br>
- [Quick-apply templates](artifact/quick-apply.md) <br>
- [System prompt template](artifact/system-inject.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with prompt templates and inline code/configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only; may optionally be applied globally through OpenClaw configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
