## Description: <br>
Siluzan CSO helps agents create and revise content, manage personas, publish to social media accounts, query enterprise RAG knowledge bases, upload media, extract covers, and review tasks and operations reports through the siluzan-cso CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sigedev01-bit](https://clawhub.ai/user/sigedev01-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations teams use this skill to connect an agent to Siluzan CSO for social content production, persona management, RAG-backed brand answers, media uploads, publishing workflows, task tracking, and reporting. The skill is suited to operational CSO workflows across YouTube, TikTok, Instagram, LinkedIn, X, and Facebook accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can make persistent environment changes, including global CLI installation, global assistant-skill registration, npm registry changes, and credential storage under ~/.siluzan. <br>
Mitigation: Review the installer before running it, prefer a scoped manual install when possible, restore the npm registry after installation if needed, and protect or rotate stored credentials. <br>
Risk: Publishing, upload, account-group, and persona-create workflows can change CSO platform state. <br>
Mitigation: Require explicit user confirmation before write actions, preview generated configuration, and verify results with read-only CLI commands after execution. <br>
Risk: Content generation can introduce unsupported brand claims when RAG evidence is absent or insufficient. <br>
Mitigation: Use the documented RAG workflow for brand or product-specific claims, cite retrieved facts internally during drafting, and ask for more source material when evidence is weak. <br>


## Reference(s): <br>
- [Siluzan CSO ClawHub listing](https://clawhub.ai/sigedev01-bit/siluzan-cso) <br>
- [Siluzan website](https://www.siluzan.com) <br>
- [Installation and configuration](artifact/references/setup.md) <br>
- [Publishing workflow](artifact/references/publish.md) <br>
- [RAG knowledge base retrieval](artifact/references/rag.md) <br>
- [Persona management](artifact/references/persona.md) <br>
- [Three-library content workflow](artifact/three-lib-content-workflow/content-writer.workflow.md) <br>
- [CSO web pages](artifact/references/web-pages.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, the siluzan-cso CLI, and Siluzan authentication; workflows may produce local JSON snapshots, publishing configuration files, uploaded media references, and extracted cover images.] <br>

## Skill Version(s): <br>
1.1.29 (source: server release metadata and artifact installer scripts) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
