## Description: <br>
Resolve Beagle closes explicit open questions and latent gaps in brainstorm-beagle specs by researching answers, proposing them for approval, and rewriting the spec in place. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill after brainstorm-beagle has produced a spec that still contains open questions, placeholders, contradictions, or other latent gaps. It helps turn that draft into an implementation-ready spec by gathering evidence, presenting one decision proposal at a time, and applying accepted answers to the document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Accepted proposals could introduce incorrect or misleading guidance into a spec. <br>
Mitigation: Review each recommendation and its cited evidence before accepting it, then use the final self-review pass to catch contradictions or unresolved gaps. <br>
Risk: The skill may ask the agent to perform repository searches or external research before editing a spec. <br>
Mitigation: Install it only when its purpose matches the intended workflow and review any commands or research actions before they run. <br>


## Reference(s): <br>
- [Subagent Prompt Templates](artifact/references/subagent-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown gap lists, evidence-backed proposals, and rewritten spec text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Presents proposals one at a time and requires evidence before applying spec changes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
