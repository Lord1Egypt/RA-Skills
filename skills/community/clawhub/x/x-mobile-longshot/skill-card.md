## Description:

Renders X (Twitter) posts, long articles, and mobile reading pages into mobile-style long screenshots and optional single-page PDFs using Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spyfree](https://clawhub.ai/user/spyfree)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to archive X posts or long-form mobile reading pages as phone-like dark-mode screenshots and optional single-page PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe output filename handling may execute local code when command arguments are controlled by untrusted users or prompts.

Mitigation: Avoid user-supplied output filenames, run the skill in an isolated workspace, and prefer a version that passes paths to Python as data rather than generated code.

Risk: Browser automation can be pointed at non-X URLs or internal network destinations.

Mitigation: Allow only vetted X URLs, block internal network destinations, and use limited network access for execution.

Risk: X overlay and page structure changes can leave sticky bars or modal prompts in screenshots.

Mitigation: Increase wait time or top replacement height, update overlay text patterns, or move to segmented capture and stitching when full-page capture is not clean enough.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spyfree/skills/x-mobile-longshot)
- [v1 design notes, limits, and iteration guidance](references/notes.md)
- [Main renderer script](scripts/render_x_longshot.js)

## Skill Output:

**Output Type(s):** [shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline bash commands that produce PNG screenshots and optional PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Playwright mobile emulation with dark mode and tunable wait and top-replacement options.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
