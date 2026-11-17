## Description:

Scores an OpenClaw agent setup against similar agents by scanning the local workspace, generating a local embedding, and submitting structured profile data to ratemyclaw.com for scoring and comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[picklenick144](https://clawhub.ai/user/picklenick144)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use RateMyClaw to scan an agent workspace, review the detected profile, and submit structured tags and embeddings for score, grade, cluster comparison, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects and submits more local environment metadata than its privacy description clearly discloses, including installed skill names, integration inferences from secret filenames, secret counts, maturity metrics, and OpenClaw model configuration.

Mitigation: Review the generated profile before submission, avoid --yes unless API key creation and package installation are acceptable, and do not submit profiles from untrusted or edited JSON files.

Risk: Embeddings and structured workspace tags can act as a sensitive fingerprint of an agent's focus areas even when raw file contents are not submitted.

Mitigation: Treat profile JSON and embedding submissions as potentially sensitive and confirm that the workspace owner accepts sharing this structured profile with ratemyclaw.com.

## Reference(s):

- [RateMyClaw homepage](https://ratemyclaw.com)
- [RateMyClaw repository](https://github.com/picklenick144/RateMyClaw)
- [all-MiniLM-L6-v2 model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [RateMyClaw taxonomy](artifact/references/taxonomy.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands, terminal text, URLs, and generated JSON profile data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a local profile JSON and submits tags, embeddings, maturity counts, installed skill names, and model configuration to ratemyclaw.com when run.]

## Skill Version(s):

0.5.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
