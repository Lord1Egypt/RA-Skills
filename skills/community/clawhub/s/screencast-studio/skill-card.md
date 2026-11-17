## Description:

Screencast Studio helps agents scaffold and run a Playwright and ffmpeg workflow that records polished narrated browser demo videos with synthetic cursor movement, click ripples, subtitles, persistent privacy masks, and review screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tatsuko-tsukimi](https://clawhub.ai/user/tatsuko-tsukimi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn browser walkthroughs into narrated demo, bug reproduction, tutorial, or feature-verification videos without manual screen recording. The skill is most useful for reviewing and sharing recently built web UI changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Login capture can persist session state and post-login artifacts in the demo workspace.

Mitigation: Use a test account and staging data where possible, keep storageState.json and post-login artifacts out of source control, and delete or revoke the session after recording.

Risk: The bundled cleanup script can delete unrelated files if run in the wrong workspace.

Mitigation: Install and run the skill only in a fresh, dedicated demo directory and review clean.js before using npm run ship.

Risk: Browser recordings can expose visible private or internal data.

Mitigation: Configure persistent mask regions before recording and review the generated sensitive screenshots before sharing any final video.

## Reference(s):

- [Screencast Studio ClawHub Release](https://clawhub.ai/tatsuko-tsukimi/skills/screencast-studio)
- [README](README.md)
- [Prerequisites](references/prerequisites.md)
- [Helpers API](references/helpers-api.md)
- [Events Schema](references/events-schema.md)
- [FFmpeg Pipeline](references/ffmpeg-pipeline.md)
- [Known Pitfalls](references/known-pitfalls.md)
- [Walkthrough Flow Example](examples/walkthrough-flow.md)
- [Demo Video Asset](https://github.com/user-attachments/assets/5bacd549-4506-4174-b56f-77175e4646b8)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown guidance with JavaScript templates, npm commands, configuration edits, and generated video/review files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scaffolds a browser-demo project that can produce final.mp4, events.json, subtitles, deployed video copies, and review screenshot sets.]

## Skill Version(s):

0.2.2 (source: server release evidence, artifact/_meta.json, and templates/package.json; SKILL.md frontmatter says 0.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
