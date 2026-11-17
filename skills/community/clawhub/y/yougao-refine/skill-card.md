## Description:

Uses Yougao to detect a manuscript, rewrite it to reduce AI indicators, recheck it, and decide on any retry against a target ratio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and editors use it to check and revise text through Yougao, compare human and AI indicator results, and receive the best verified draft with files and an editing link. A target is a comparison condition, not a guaranteed result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manuscript text is sent to Yougao, and the live service's retention practices were not verified in this review.

Mitigation: Submit only text you are comfortable sharing with Yougao.

Risk: Paid rewrites and retries can use account points; no points cap is enabled by default.

Mitigation: Set a points cap that covers the authorized checks, rewrites, and retries.

Risk: An API key with broader permissions can enable actions beyond rewriting and detection; local disconnect does not revoke it.

Mitigation: Use a key limited to rewriting and detection, protect saved credentials, and revoke keys through the service when needed.

Risk: Shared helpers also support publishing, which can make content public.

Mitigation: Require separate authorization and publishing permissions before using publishing features.

## Reference(s):

- [Comprehensive rewriting and recheck guide](references/refine.md)
- [Shared connection and run guide](references/client.md)
- [Yougao API integration guide](references/api.md)
- [Yougao API documentation](https://yougao.top/ai.md)
- [Machine-readable API contract](https://yougao.top/api/v1/openapi.json)
- [ClawHub skill page](https://clawhub.ai/dunkong/skills/yougao-refine)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML files]

**Output Format:** [Revised manuscript files, a text report with detection results, and an editing link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves the original and best verified version; input text is 100–10,000 characters. Target ratios are not guaranteed outcomes.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
