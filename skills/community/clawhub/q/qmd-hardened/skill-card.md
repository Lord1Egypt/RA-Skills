## Description: <br>
Local search/indexing CLI (BM25 + vectors + rerank) with MCP mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to operate qmd for local document indexing, BM25, vector, and hybrid search, and MCP-mode workflows while preserving local data boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and operates third-party qmd code. <br>
Mitigation: Review the upstream qmd repository before installing or upgrading the CLI. <br>
Risk: Indexed files and embedding requests may contain private or sensitive text. <br>
Mitigation: Index only intended directories and keep embedding and rerank endpoints local unless a remote endpoint is explicitly trusted. <br>
Risk: Search or get results may expose credentials, API keys, tokens, or private keys. <br>
Mitigation: Inspect results for secrets and redact or summarize sensitive values before sharing output. <br>
Risk: Deleting, clearing, or rebuilding qmd indexes can destroy local search state. <br>
Mitigation: Require explicit confirmation before destructive index operations. <br>
Risk: Piping qmd output to network-transmitting commands can exfiltrate indexed content. <br>
Mitigation: Do not pipe or redirect qmd output to network destinations; review results locally before any manual sharing. <br>


## Reference(s): <br>
- [Qmd Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/qmd-hardened) <br>
- [qmd upstream package](https://github.com/tobi/qmd) <br>
- [qmd homepage](https://tobi.lutke.com) <br>
- [Faberlens qmd safety evaluation](https://faberlens.ai/explore/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with qmd command examples and redacted or summarized search-result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local qmd indexes, Ollama endpoint configuration, MCP mode, and safety checks for sensitive indexed content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
