## Description:

通过调用 UCAP 平台的安全防护接口，快速识别文本或网页内容中的敏感数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[1227323804](https://clawhub.ai/user/1227323804)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content compliance teams use this skill to check text or fetched webpage content for sensitive information through UCAP. It supports direct text checks, URL content fetching, optional detection-type selection, and userKey-based UCAP access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL scanning can expose privileged networks to SSRF-style requests when the runtime has internal network or cloud metadata access.

Mitigation: Run URL scanning only in network-isolated environments with outbound egress controls; avoid privileged or private-network contexts.

Risk: Browser mode executes page JavaScript and can broaden request behavior beyond the initial URL.

Mitigation: Keep static mode enabled by default; enable browser mode only with an explicit ALLOWED_DOMAINS whitelist and strong sandboxing.

Risk: Scanned text and fetched page content are sent to UCAP.

Mitigation: Review data-sharing requirements before submitting sensitive or regulated content to the UCAP service.

Risk: Unpinned dependencies can change runtime behavior.

Mitigation: Pin dependency versions and review updates before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1227323804/skills/ucap-sensitive-check)
- [UCAP safeguard platform](https://safeguard.ucap.com.cn/)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON results with concise text or Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source URL and source type for URL checks; userKey is kept in the current process environment when supplied.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
