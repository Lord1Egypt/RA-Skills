## Description: <br>
TokenSaver Korean helps agents store, search, compress, tier, and archive Korean-first context using hybrid keyword and embedding search, deduplication, WAL-backed persistence, and entity extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorongss](https://clawhub.ai/user/dorongss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to reduce context tokens by storing Korean-first memories, retrieving relevant summaries, and escalating from abstract to full content when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive context in local memory storage. <br>
Mitigation: Review memory content before storing it; do not store secrets, credentials, regulated personal data, or confidential business context unless persistent local storage is acceptable. <br>
Risk: Embedding search can send saved memory text or search queries to Fireworks when FIREWORKS_API_KEY is configured. <br>
Mitigation: Set FIREWORKS_API_KEY only when Fireworks is approved to receive that data; otherwise use keyword search fallback. <br>
Risk: The init_bora_context.py artifact imports local OpenClaw profile and identity files into searchable memory. <br>
Mitigation: Do not run init_bora_context.py unless that import is intentional and the source files are appropriate for indexing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dorongss/token-saver-korean) <br>
- [TokenSaver documentation](https://docs.token-saver.ai) <br>
- [Fireworks embeddings API endpoint](https://api.fireworks.ai/inference/v1/embeddings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local memory tiers and use Fireworks embeddings when FIREWORKS_API_KEY is configured.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
