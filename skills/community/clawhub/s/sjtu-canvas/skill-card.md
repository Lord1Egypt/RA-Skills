## Description:

SJTU Canvas 课程助手 helps users manage Canvas LMS courses, files, assignments, deadlines, grades, discussions, submissions, and course-material extraction for AI-assisted study workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhh678876](https://clawhub.ai/user/xhh678876)

### License/Terms of Use:

MIT-0

## Use Case:

External Canvas LMS users, especially SJTU students, use this skill to query course data, download and summarize course materials, track assignment deadlines, sync Apple Calendar events, review grades, and prepare study or assignment-support notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Canvas API token or course data exposure during configuration or local execution.

Mitigation: Use a limited-scope Canvas token where possible, keep config.json out of source control, and run the skill in a dedicated environment.

Risk: Bulk downloads or extracted course materials could overwrite local files or place files outside the intended workspace if paths are not reviewed.

Mitigation: Use a dedicated save directory, preview download targets, and review filenames and output paths before running bulk file workflows.

Risk: Apple Calendar synchronization runs local AppleScript and writes calendar events on macOS.

Mitigation: Run calendar sync only in a trusted macOS session and review calendar names, event titles, and event descriptions before syncing.

Risk: Assignment submission can affect a user's Canvas course record.

Mitigation: Require explicit user confirmation of course ID, assignment ID, and file paths before any submission action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xhh678876/skills/sjtu-canvas)
- [Source repository](https://github.com/xhh678876/sjtu-canvas.git)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [SJTU Canvas](https://oc.sjtu.edu.cn)
- [SJTU-Canvas-Helper inspiration project](https://github.com/Okabe-Rintarou-0/SJTU-Canvas-Helper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown and plain text responses with inline shell commands, configuration examples, Canvas API summaries, and locally generated or downloaded files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Canvas API token and may read or write local course-material and calendar data depending on the selected workflow.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
