## Description: <br>
Score your OpenClaw agent setup against similar agents. Scans your workspace, generates a local embedding for privacy-preserving semantic matching, and submits tags + embedding to ratemyclaw.com for scoring and cluster comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[picklenick144](https://clawhub.ai/user/picklenick144) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to scan an agent workspace locally, review detected taxonomy tags and maturity signals, then submit a derived profile for score, grade, and cluster comparison results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans broad workspace areas and sends a derived profile to ratemyclaw.com, which may include sensitive environment metadata. <br>
Mitigation: Review generated_profile.json before submitting, especially installed skill names, integrations inferred from secrets, maturity counts, and model names. <br>
Risk: Using automated submission can generate an API key and proceed with dependency installation without an interactive review step. <br>
Mitigation: Avoid --yes unless the user accepts automatic key generation, dependency installation, and profile submission behavior. <br>


## Reference(s): <br>
- [RateMyClaw ClawHub Listing](https://clawhub.ai/picklenick144/ratemyclaw) <br>
- [RateMyClaw Homepage](https://ratemyclaw.com) <br>
- [RateMyClaw Repository](https://github.com/picklenick144/RateMyClaw) <br>
- [all-MiniLM-L6-v2 Model Card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) <br>
- [RateMyClaw Taxonomy](references/taxonomy.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON profile data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a score, grade, and web link after submitting a derived profile to ratemyclaw.com.] <br>

## Skill Version(s): <br>
0.5.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
