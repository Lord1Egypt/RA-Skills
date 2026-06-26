## Description: <br>
Classifies incoming tasks by domain and routes them to specialized system prompts, tuned model choices, and retrieval strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephenlthorn](https://clawhub.ai/user/stephenlthorn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill as a first-pass router that classifies coding and analysis requests into specialist domains and returns the prompt, model, and metadata needed for focused handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task text or file-path context could expose credentials, customer data, or sensitive business details to the configured LLM endpoint. <br>
Mitigation: Limit file_context to the intended project and avoid sensitive data in ambiguous requests unless the LLM endpoint is approved for that data. <br>
Risk: A routing or classification error could send a task to an unsuitable specialist prompt or model. <br>
Mitigation: Review the returned domain, specialist, and model before using the generated prompt in high-impact coding, trading, VC, or infrastructure workflows. <br>


## Reference(s): <br>
- [Route Specialist on ClawHub](https://clawhub.ai/stephenlthorn/route-specialist) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Structured routing metadata with prompt text and model recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes domain, specialist, system_prompt, model, detected frameworks, iOS version, multi-hop status, project path, and hard-gate status when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
