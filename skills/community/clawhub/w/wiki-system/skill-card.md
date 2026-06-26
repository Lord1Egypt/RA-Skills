## Description: <br>
Compilation-over-retrieval knowledge wiki for OpenClaw agents. Drop sources in, get structured cross-referenced pages out. Knowledge compounds instead of disappearing. Based on Andrej Karpathy's LLM Wiki pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dobrinalexandru](https://clawhub.ai/user/dobrinalexandru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to build and maintain a persistent local knowledge wiki from curated sources, with ingestion, query, and lint workflows for structured markdown memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill maintains persistent local memory and can add structured wiki content from queued sources. <br>
Mitigation: Review sources before ingestion, avoid queuing sensitive or untrusted URLs, and inspect wiki changes before relying on them. <br>
Risk: Optional cron automation can run ingestion or lint workflows without an active conversation. <br>
Mitigation: Enable cron only when scheduled autonomous maintenance is acceptable, and review the generated cron commands and reports. <br>
Risk: Optional SuperMemory sync can expose the wiki index to cloud memory workflows. <br>
Mitigation: Enable sync only when cloud visibility of the wiki index is acceptable for the workspace. <br>
Risk: Lint and uninstall workflows can modify or remove wiki files. <br>
Mitigation: Back up memory/wiki and work/wiki-sources before lint-heavy maintenance or uninstalling. <br>


## Reference(s): <br>
- [Karpathy's LLM Wiki Pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>
- [Karpathy LLM Wiki Pattern Reference](references/karpathy-llm-wiki.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dobrinalexandru/wiki-system) <br>
- [Dual-memory Plugin](https://clawhub.ai/skills/dual-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, wiki pages, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local wiki files under memory/wiki and work/wiki-sources; cron and cloud sync setup are opt-in.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
