## Description:

Turn recipes into a Todoist Shopping list by extracting ingredients from recipe photos or web pages, comparing them against the existing Shopping project, skipping common pantry staples by default, summing matching quantities when units align, and saving cooked recipes into a workspace cookbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[borahm](https://clawhub.ai/user/borahm)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn recipe photos or confirmed recipe web content into a flat Todoist Shopping list and a local cookbook entry. It is intended for personal grocery planning workflows that can tolerate manual review of extracted ingredients and list updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill loads local credentials broadly through the shell wrapper.

Mitigation: Avoid the wrapper or replace its dotenv sourcing with an allowlisted parser for only GEMINI_API_KEY, GOOGLE_API_KEY, and TODOIST_API_TOKEN.

Risk: Normal execution can make live Todoist and workspace changes.

Mitigation: Run with --dry-run and --no-save first, and require confirmation before allowing Todoist updates.

Risk: Recipe photos or extracted recipe text may be sent to Gemini.

Mitigation: Install and run only when sending that recipe content to Gemini is acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON status output, Todoist task updates, markdown recipe files, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Gemini with recipe images or text, may update Todoist tasks, and may write recipe markdown files into recipes/ unless run with --dry-run or --no-save.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
