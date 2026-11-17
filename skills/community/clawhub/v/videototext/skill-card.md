## Description:

Guides agents through stable Bilibili official subtitle retrieval, troubleshooting login-visible tracks, and generating Chinese summaries through an OpenAI-compatible chat-completions service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willguo715](https://clawhub.ai/user/willguo715)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to parse Bilibili video links, retrieve official subtitle tracks with cookie-aware troubleshooting, and produce concise Chinese summaries. It is useful when handling Bilibili subtitle failures, login-visible tracks, language selection, subtitle validation, and OpenAI-compatible summary configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bilibili cookies and LLM API keys are secrets and could be exposed if handled carelessly.

Mitigation: Use a low-value Bilibili account, store SESSDATA, BILI_JCT, DEDEUSERID, and LLM API keys only in local secret configuration, and avoid logging or sharing those values.

Risk: User-supplied URLs and redirects can cause unintended network requests.

Mitigation: Review or patch the network handling before deployment, including cookie host validation and redirect validation for Bilibili short links and subtitle URLs.

Risk: Subtitle text may be sent to a configured OpenAI-compatible LLM endpoint.

Mitigation: Prefer a local-only or otherwise trusted LLM endpoint for sensitive content, and disable LLM summaries when external processing is not acceptable.

Risk: Unpinned dependency ranges can change runtime behavior over time.

Mitigation: Pin and review dependency versions before deploying the bundled code subset.

## Reference(s):

- [Skill reference](reference.md)
- [Bundled code README](code/README.md)
- [ClawHub skill page](https://clawhub.ai/willguo715/skills/videototext)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration notes, and code references; bundled helpers can produce subtitle text, subtitle segments, SRT, and Chinese summary text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Bilibili cookies for login-visible subtitles and optional OpenAI-compatible LLM settings for model summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
