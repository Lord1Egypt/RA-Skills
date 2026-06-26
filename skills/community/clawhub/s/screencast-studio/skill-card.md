## Description: <br>
Screencast Studio helps agents scaffold and run a Playwright-based workflow that records browser UI demos, post-processes them into narrated MP4s with synthetic cursor and click effects, and generates review screenshots for visual and privacy checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tatsuko-tsukimi](https://clawhub.ai/user/tatsuko-tsukimi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill to turn browser-based product walkthroughs into polished demo, tutorial, bug reproduction, or feature-review screencasts. It is especially aimed at rapid visual verification after changing a web UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the default workflow in an existing project folder can delete unrelated files during cleanup. <br>
Mitigation: Use a fresh disposable screencast folder, or inspect and remove the cleanup step before running it in an existing project. <br>
Risk: Login state, screenshots, videos, summaries, and review frames may contain private session data or sensitive UI content. <br>
Mitigation: Use demo or low-privilege accounts, keep generated artifacts out of git and shared archives, and delete or rotate sessions after recording. <br>
Risk: A finished recording may still expose personally identifiable or internal information if mask regions are incomplete. <br>
Mitigation: Review the sensitive screenshot pass before sharing, add selector or box masks for exposed regions, and rerender until sensitive content is unreadable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tatsuko-tsukimi/screencast-studio) <br>
- [README](README.md) <br>
- [Walkthrough flow example](examples/walkthrough-flow.md) <br>
- [Prerequisites](references/prerequisites.md) <br>
- [Helpers API](references/helpers-api.md) <br>
- [events.json schema](references/events-schema.md) <br>
- [ffmpeg pipeline](references/ffmpeg-pipeline.md) <br>
- [Known pitfalls](references/known-pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript template files and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Playwright and ffmpeg project files plus local video, screenshot, event log, and review artifacts in the selected screencast working directory.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata and templates/package.json; SKILL.md frontmatter lists 0.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
