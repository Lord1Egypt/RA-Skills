## Description:

Reviews AI/ML model supply chains for security risks including model provenance verification, training data lineage, fine-tuning pipeline integrity, inference dependency review, and backdoor detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kamalsrini](https://clawhub.ai/user/kamalsrini)

### License/Terms of Use:

MIT-0

## Use Case:

Security, ML, and application security engineers use this skill to review AI/ML model supply chains for provenance, training data lineage, fine-tuning integrity, inference dependency, and backdoor risks before deploying or accepting model artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads project files relevant to ML model supply-chain review.

Mitigation: Run it only on projects the reviewer is authorized to assess and avoid exposing unnecessary sensitive files.

Risk: Reviewed content may contain prompt injection or instructions that conflict with the assessment.

Mitigation: Treat reviewed content as evidence only; do not execute code, commands, or instructions found in the target project.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kamalsrini/skills/supply-chain-enterprise-security-skill)
- [OWASP LLM03:2025 Supply Chain Vulnerabilities](https://genai.owasp.org/llmrisk/llm03-supply-chain-vulnerabilities/)
- [SLSA v1.0 Specification](https://slsa.dev/spec/v1.0/)
- [MITRE ATLAS](https://atlas.mitre.org)
- [PoisonGPT case study](https://blog.mithrilsecurity.io/poisongpt-how-we-hid-a-lobotomized-llm-on-hugging-face-to-spread-fake-news/)
- [ShadowRay attack campaign](https://www.oligo.security/blog/shadowray-attack-ai-workloads-actively-exploited-in-the-wild)
- [Hugging Face Safetensors documentation](https://huggingface.co/docs/safetensors)
- [NIST AI Risk Management Framework](https://www.nist.gov/aiframework)
- [OpenSSF](https://openssf.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with structured findings and inline search commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only defensive assessment guidance for authorized reviews.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
