## Description:

Reads X (Twitter) Articles aloud using macOS text-to-speech, accepting X Article URLs and automatically selecting Chinese or English voices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ewangchong](https://clawhub.ai/user/ewangchong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch accessible X Article content from a supplied URL, read it aloud with macOS text-to-speech, and optionally save the spoken output as an audio file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores reusable X session data under the skill directory.

Mitigation: Install only after review, avoid sharing or backing up the browser_state directory, and remove the saved session when the skill is no longer needed.

Risk: The browser launch disables sandboxing and uses weak scoping for authenticated browsing.

Mitigation: Prefer a revised release that removes --no-sandbox, validates x.com article URLs before navigation, and narrows authenticated browser use to trusted article pages.

Risk: Dependencies are installed without pinned versions.

Mitigation: Pin and review dependency versions before deploying the skill in a managed environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ewangchong/skills/x-article-reader)
- [Project homepage](https://github.com/ewangchong/x-article-reader)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and command-line output, with optional AIFF audio file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS text-to-speech, patchright/Chromium, and a saved X browser session for authenticated article access.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
