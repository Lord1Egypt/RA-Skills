## Description:

Translate TXT translates text files through configurable OpenAI-compatible APIs, with chunking, retry behavior, and context-aware translation for larger documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litousteven](https://clawhub.ai/user/litousteven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure translation credentials and translate .txt files into Chinese or another target language while preserving document structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source documents and derived context are sent to the configured external translation provider.

Mitigation: Use only approved HTTPS providers and avoid confidential or regulated files unless the provider is authorized for that data.

Risk: The setup flow can store the API key in a local .env file.

Mitigation: Prefer secure environment-based secret injection when possible, restrict access to local credential files, and rotate exposed keys.

Risk: A configurable base URL can direct requests to an untrusted endpoint.

Mitigation: Verify the endpoint before use and keep provider, model, and key settings under user review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litousteven/skills/smart-translate-txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and generated translated text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an output text file path after translation; translation quality, latency, and data handling depend on the configured API provider and model.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
