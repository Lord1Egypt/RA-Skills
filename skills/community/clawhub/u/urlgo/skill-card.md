## Description:

urlgo lets an agent control a local browser through CDP to open pages, capture screenshots, read page text or HTML, and execute JavaScript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and interact with web pages through a local CDP-enabled browser, including screenshots, text snapshots, HTML source capture, clicks, typing, and JavaScript evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad CDP control over a local browser, including page navigation, clicks, typing, screenshots, and JavaScript evaluation.

Mitigation: Install only when browser automation is intended, review proposed browser actions before execution, and close the detached browser session when finished.

Risk: Screenshots, HTML source, snapshots, and JavaScript evaluation can expose private content from logged-in or sensitive pages.

Mitigation: Avoid sensitive logged-in accounts unless each action is explicitly approved, and treat captured page content as sensitive data.

Risk: The browser can remain running in the background after the CLI exits.

Mitigation: Check browser status before and after use, and close stale or unrelated tabs and browser processes when work is complete.

## Reference(s):

- [ClawHub urlgo Skill Page](https://clawhub.ai/fslong520/skills/urlgo)
- [ClawHub Publisher Profile: fslong520](https://clawhub.ai/user/fslong520)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and browser-derived text, HTML, or PNG screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local screenshot files and page content captured from the controlled browser.]

## Skill Version(s):

6.6.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
