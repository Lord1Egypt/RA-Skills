## Description:

A Chinese article-quality analyzer that scores technical articles, essays, novels, heuristic AI-generation signals, and originality indicators, then returns reading advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forealmy](https://clawhub.ai/user/forealmy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze Chinese article drafts or candidate reading material for article type, quality dimensions, heuristic AI-generation signals, originality exemptions, and reading recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-generation and originality scores are heuristic and can be wrong.

Mitigation: Use the scores as advisory signals, not as proof of authorship or quality, and keep human review in the decision process.

Risk: Python dependencies are declared without exact pinned versions.

Mitigation: Pin and scan dependencies in the deployment environment before production use.

Risk: Private drafts could be exposed if optional external LLM processing is later enabled or added without clear disclosure.

Mitigation: Keep analysis local for sensitive text unless data sharing is disclosed, consented to, and approved for the deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forealmy/skills/tmpz3kwrq8c)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [JSON reports and Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local heuristic scoring of Chinese article text; batch mode is documented but reports that it is still in development.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
