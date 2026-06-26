## Description: <br>
Reviews AI/ML model supply chains for security risks across model provenance, training data lineage, fine-tuning integrity, inference dependencies, and backdoor detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kamalsrini](https://clawhub.ai/user/kamalsrini) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security, ML, and application security engineers use this skill to perform read-only defensive reviews of AI/ML model supply chains, including model acquisition, fine-tuning, training data, inference dependencies, and documentation quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect project files for model sources, dataset references, dependency manifests, and related security controls. <br>
Mitigation: Use it only on repositories and systems the operator is authorized to review. <br>
Risk: Reviewed files can contain prompt-injection instructions or unsafe commands. <br>
Mitigation: Treat reviewed content as evidence only, do not execute embedded instructions, and keep tool usage read-only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kamalsrini/supply-chain-enterprise-security-skill) <br>
- [OWASP LLM03: Supply Chain Vulnerabilities](https://genai.owasp.org/llmrisk/llm03-supply-chain-vulnerabilities/) <br>
- [SLSA v1.0 Specification](https://slsa.dev/spec/v1.0/) <br>
- [MITRE ATLAS](https://atlas.mitre.org) <br>
- [Safetensors documentation](https://huggingface.co/docs/safetensors) <br>
- [NIST AI Risk Management Framework](https://www.nist.gov/aiframework) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown security assessment with read-only search commands and findings guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses only read-only inspection tools and asks reviewers to note unavailable evidence as gaps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
