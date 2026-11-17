## Description:

Use when building HTML email templates with React components, adding a visual email editor to an application using the React Email visual editor, rendering emails to HTML, or sending emails with Resend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christina-de-martinez](https://clawhub.ai/user/christina-de-martinez)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to create, preview, render, localize, edit, and send React-based HTML email templates for transactional and marketing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup commands can fetch mutable npm packages through `npx` or package-manager installs.

Mitigation: Pin reviewed package versions and run setup in a clean project environment before using generated email code in a production application.

Risk: Sending examples may involve a Resend API key.

Mitigation: Use a narrowly scoped, revocable API key and rotate it if setup or sending behavior looks unexpected.

## Reference(s):

- [React Email Documentation](https://react.email/docs/llms.txt)
- [React Email Homepage](https://react.email)
- [React Email Repository](https://github.com/resend/react-email)
- [Resend React Email Skill Documentation](https://resend.com/docs/react-email-skill)
- [Resend Documentation](https://resend.com/docs/llms.txt)
- [Email Client CSS Support](https://www.caniemail.com)
- [Component Reference](references/COMPONENTS.md)
- [Styling Guide](references/STYLING.md)
- [Email Editor Reference](references/EDITOR.md)
- [Sending Guide](references/SENDING.md)
- [Internationalization Guide](references/I18N.md)
- [Common Email Patterns](references/PATTERNS.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with TypeScript, JSON, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include React Email component code, package commands, editor integration guidance, rendering examples, and sending examples.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
