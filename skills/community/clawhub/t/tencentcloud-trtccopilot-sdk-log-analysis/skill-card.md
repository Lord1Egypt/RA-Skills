## Description:

Analyzes local Tencent Cloud TRTC, IM, and TUI SDK client logs by identifying log types, decoding .clog/.xlog files, building timelines, and offering a localhost preview for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to inspect user-provided SDK client logs, decode local binary log files, generate evidence-backed timelines, and diagnose TRTC, IM, and TUI issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-provided SDK logs, which may contain sensitive operational or user data.

Mitigation: Use it only with logs you intend to analyze in the agent environment, and redact or limit log inputs when possible.

Risk: The localhost preview server can expose decoded log contents on the local machine while it is running.

Mitigation: Keep preview access localhost-only and stop the preview server when review is finished.

Risk: A decoder fallback can use externally selected decoder settings if override environment variables are set.

Mitigation: Prefer the vendored decoder and avoid CLOG_DECODER_BIN, CLOG_DECODER_PACKAGE, or CLOG_DECODER_REGISTRY unless those values are trusted.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/tencent-adm/skills/tencentcloud-trtccopilot-sdk-log-analysis)
- [Reference index](references/README.md)
- [TRTC analysis playbook](references/trtc-analysis-playbook.md)
- [TRTC deep log patterns](references/trtc-deep-log-patterns.md)
- [TRTC known issues](references/trtc-known-issues.md)
- [TRTC audio diagnostics](references/trtc-audio-diagnostics.md)
- [TRTC screen share diagnostics](references/trtc-screen-share-diagnostics.md)
- [TRTC SDK versions](references/trtc-sdk-versions.md)
- [TRTC product concepts](references/trtc-product-concepts.md)
- [TRTC event ID mapping](references/trtc-event-id-mapping.md)
- [Web log patterns](references/web-log-patterns.md)
- [Native log patterns](references/native-log-patterns.md)
- [Mini Program log patterns](references/miniprogram-log-patterns.md)
- [IM xlog patterns](references/im-xlog-patterns.md)
- [Audio troubleshooting](references/audio-troubleshooting.md)
- [SDK crash analysis](references/sdk-crash-analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with evidence snippets, timeline files, JSON manifests, and local shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce localhost-only preview links and generated timeline artifacts for user-provided logs.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
