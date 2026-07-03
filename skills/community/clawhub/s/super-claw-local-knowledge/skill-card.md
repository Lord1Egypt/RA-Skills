## Description: <br>
Enables agents to convert uploaded DOCX, PDF, XLSX, and PPTX files into a persistent local Markdown knowledge base and retrieve relevant stored documents for future answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to initialize and operate a local document knowledge base, ingest uploaded office documents, and retrieve stored Markdown content to ground agent responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted documents and the knowledge index are retained locally and can be searched later. <br>
Mitigation: Install only when a persistent local knowledge base is intended, and treat converted Markdown as retained workspace data. <br>
Risk: The workflow may delete original uploaded files after conversion. <br>
Mitigation: Review the converted Markdown and index entry before deleting source documents. <br>
Risk: Optional proactive SOUL.md setup can cause retrieval attempts when the agent is uncertain. <br>
Mitigation: Narrow or skip proactive setup when knowledge-base retrieval should happen only after explicit user requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-claw-local-knowledge) <br>
- [README](artifact/README.md) <br>
- [Add knowledge guide](artifact/references/add_knowledge.md) <br>
- [Knowledge retrieval guide](artifact/references/retrieval_knowledge.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and JSON index entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local knowledge-base Markdown files and a JSON index when the workflow is followed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
