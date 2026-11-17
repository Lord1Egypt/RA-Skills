## Description:

SEO Compliance Checker helps agents review and generate Chinese marketing content by scanning for advertising-law banned words, keyword-density issues, platform-specific SEO requirements, and safer replacement language using API-backed shell scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, ecommerce operators, and content teams use this skill to check Chinese copy for banned-word and SEO issues across Baidu, Xiaohongshu, Douyin, Taobao, and JD workflows. Agents can also use it to draft platform-specific content and produce compliance-oriented rewrite guidance.

### Deployment Geography for Use:

Global (intended for Chinese-language content and Chinese platform workflows)

## Known Risks and Mitigations:

Risk: A helper script has a code-injection bug.

Mitigation: Install only after the suggestions.sh issue is fixed and review the script before execution.

Risk: Compliance checks submit user content to a remote API.

Mitigation: Do not send confidential drafts, client copy, regulated content, or secrets unless the API operator and data handling are trusted.

Risk: Default API endpoint and token configuration may not match an organization's security boundaries.

Mitigation: Review or restrict CN_SEO_API_BASE and CN_SEO_TOKEN configuration before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/seo-compliance-checker)
- [Compliance API endpoint](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com)
- [Compliance web app](https://1341839497-jv04655vcs.ap-shanghai.tencentscf.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with shell command examples and API-derived check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can submit content to a remote API; scripts may use optional CN_SEO_API_BASE and CN_SEO_TOKEN configuration.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
