## Description:

Resolves the signed video URL behind OceanEngine material-center video_player pages and can optionally download the MP4 stream.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suiside](https://clawhub.ai/user/suiside)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user provides an OceanEngine material-center video_player token URL and needs the real signed media URL or a local MP4 download. It is scoped to this OceanEngine flow and is not intended as a general-purpose video downloader.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader can render and fetch URLs outside the documented OceanEngine material-center flow.

Mitigation: Use only trusted OceanEngine video_player token URLs and prefer a release that enforces exact host and path allowlists before rendering or fetching.

Risk: Attacker-supplied @path inputs can hide or swap the URL that will be rendered and fetched.

Mitigation: Inspect @path files before use, avoid untrusted path inputs, and pass the intended URL directly when possible.

Risk: Redirects, cookies, and browser execution increase exposure if the browser environment is not isolated.

Mitigation: Validate redirects, limit cookies to the expected vck_* value, use an isolated temporary browser profile, and enable Chromium sandboxing where supported.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suiside/skills/tt-download)
- [OpenClaw documentation](https://docs.openclaw.ai/)
- [Usage contract](references/usage.json)
- [Troubleshooting guide](references/troubleshooting.md)
- [Chrome browser discovery paths](references/chrome-paths.json)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Plain text URL on stdout, optional MP4 file output, and progress or error messages on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, Python 3, and a local Chromium-based browser. Resolved signed URLs are short-lived and should not be cached for later download.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
