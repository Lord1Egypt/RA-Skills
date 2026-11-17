## Description:

Virtual User Skill helps agents retrieve local user-research scenarios, generate virtual user profiles, simulate interview responses, and produce product-evaluation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuxin-wenxiang](https://clawhub.ai/user/chuxin-wenxiang)

### License/Terms of Use:

MIT-0

## Use Case:

Product researchers, product teams, and developers use this skill to explore user needs by matching a research question against local scenario data, generating virtual user types, running simulated interviews, and summarizing findings in a report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive local user-research data and encryption keys may be exposed through unsafe data-handling paths.

Mitigation: Remove key printing, avoid plaintext sample exports by default, and require explicit user-selected import files before processing research data.

Risk: Deployment examples can expose the skill as a public service without sufficient controls.

Mitigation: Use authentication, localhost binding or network allowlists, rate limits, least-privilege service configuration, and a reviewed service unit before any server deployment.

Risk: Unpinned dependencies may change behavior or introduce supply-chain risk during installation.

Mitigation: Pin dependency versions and review dependency updates before release or installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chuxin-wenxiang/skills/virtual-user-skill)
- [Publisher profile](https://clawhub.ai/user/chuxin-wenxiang)
- [BAAI bge-large-zh-v1.5 model](https://huggingface.co/BAAI/bge-large-zh-v1.5)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated virtual user lists, simulated dialogue, scenario-search JSON, and Markdown interview reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
