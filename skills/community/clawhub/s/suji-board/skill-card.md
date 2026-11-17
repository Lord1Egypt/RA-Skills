## Description:

Suji Board is a zero-dependency, single-file front-end web app for collecting fragmented text, managing images, organizing notes and files, and exporting structured notes to Word .docx files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weijunz766-collab](https://clawhub.ai/user/weijunz766-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to deliver or operate a local-first note collection board for pasted text, images, folder-based document organization, reminders, and Word export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deleted images and files may remain in browser-local storage after user-facing deletion actions.

Mitigation: Avoid storing highly sensitive documents or images until local deletion cleanup is fixed, and clear browser site data when removing sensitive content.

Risk: The app is mostly local but not strictly offline because update checks, upgrade links, and feedback links can contact ClawHub or Google.

Mitigation: Use it in a network-restricted context or avoid update and feedback actions when strict offline behavior is required.

## Reference(s):

- [Product introduction](references/product-intro.md)
- [ClawHub skill page](https://clawhub.ai/weijunz766-collab/skills/suji-board)

## Skill Output:

**Output Type(s):** [code, markdown, guidance]

**Output Format:** [Markdown guidance with a bundled single-file HTML application]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled app stores notes in localStorage, images and file blobs in IndexedDB, and exports Word .docx files from the browser.]

## Skill Version(s):

1.8.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
