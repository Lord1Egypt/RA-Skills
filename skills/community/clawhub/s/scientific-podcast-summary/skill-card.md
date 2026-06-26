## Description: <br>
Automatically summarize scientific podcasts like Huberman Lab and Nature. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch Huberman Lab or Nature Podcast pages, send extracted text to an OpenAI-compatible model, and generate concise scientific podcast summaries in Markdown or JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched podcast content may be sent to the configured OpenAI-compatible model provider. <br>
Mitigation: Use only public, trusted podcast URLs, verify OPENAI_BASE_URL, and run with a limited API key. <br>
Risk: Unpinned Python dependencies can reduce reproducibility across environments. <br>
Mitigation: Install in a virtual environment and pin dependency versions for production or repeatable use. <br>
Risk: Optional file output can place generated summaries at user-provided paths. <br>
Mitigation: Write outputs only to approved workspace paths and review generated files before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/aipoch-ai/scientific-podcast-summary) <br>
- [Audit Reference](references/audit-reference.md) <br>
- [Huberman Lab Podcast Episodes](https://hubermanlab.com/category/podcast-episodes/) <br>
- [Nature Podcast Articles](https://www.nature.com/nature/articles?type=podcast) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files] <br>
**Output Format:** [Markdown or JSON scientific podcast briefing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include podcast title, release date, host or guest details, core topic overview, key scientific findings, practical advice, and resource links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
