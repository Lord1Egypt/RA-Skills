## Description:

Generates sales copy by extracting FAB selling points, choosing emotional hooks, adapting tone for target platforms, and adding CTA language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketers, and content creators use this skill to turn product topics and optional brand information into platform-adapted promotional copy. It supports product launches, livestream promotion, ecommerce detail pages, social media seeding, and time-limited campaign copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests read and command-execution capability that is not clearly necessary for generating marketing copy.

Mitigation: Run it in a constrained agent environment, deny exec unless specifically needed, and review requested file access before use.

Risk: Marketing-copy generation can produce inaccurate or misleading promotional claims if inputs are incomplete or exaggerated.

Mitigation: Review generated copy against product facts, advertising rules, and platform policies before publishing.

Risk: Environment variables or API keys could be exposed to a skill with broad execution capability.

Mitigation: Do not expose sensitive environment variables or API keys to the skill unless its behavior has been reviewed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured JSON-style response plus generated marketing copy in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a product topic and target platform; brand information, emotional hook type, and CTA type are optional.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
