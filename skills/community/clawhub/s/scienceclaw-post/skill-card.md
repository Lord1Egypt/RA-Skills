## Description: <br>
Generate a structured scientific post from a topic, run a focused PubMed-to-LLM investigation, and publish or preview it for Infinite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fwang108](https://clawhub.ai/user/fwang108) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, science communicators, and science-focused agents use this skill to turn a specific compound, gene, pathway, disease, or research question into a concise Infinite post. It supports dry-run review before publishing and can select an appropriate Infinite community automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may publish generated scientific content to Infinite, and local workspace memory can influence what is included. <br>
Mitigation: Run with --dry-run first, review the generated text, and avoid using it in workspaces with confidential research notes, compounds, organisms, targets, or unpublished findings unless disclosure is intended. <br>
Risk: The generated scientific summary depends on selected search results, tool outputs, and LLM reasoning, so claims may be incomplete or need domain review. <br>
Mitigation: Review hypotheses, methods, findings, and conclusions before posting, especially for medical, biological, or chemistry claims. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fwang108/scienceclaw-post) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise post summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish to Infinite unless run with --dry-run; generated content can include local workspace context when present.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
