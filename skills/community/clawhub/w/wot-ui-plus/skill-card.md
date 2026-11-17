## Description:

Wot UI Plus helps agents answer usage questions for the wot-ui-plus component library, including component APIs, composable APIs, global configuration, theming, examples, and API references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l-spaces](https://clawhub.ai/user/l-spaces)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building uni-app, Vue 3, and TypeScript applications use this skill to answer wot-ui-plus component questions, locate accurate props, events, slots, methods, and v-model patterns, and draft copy-ready usage examples from the bundled documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-ready upload examples may send user-selected files to demo or unintended endpoints.

Mitigation: Replace demo upload URLs with endpoints you control and consider disabling automatic upload until the user confirms the selected files.

Risk: Mini-program authorization and upload examples may expose profile, phone, file, or upload event payloads.

Mitigation: Review platform permission flows before use and avoid logging raw personal, file, or upload event payloads in production.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/l-spaces/skills/wot-ui-plus)
- [Artifact README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Button Reference](artifact/references/button.md)
- [ConfigProvider Reference](artifact/references/configProvider.md)
- [Upload Reference](artifact/references/upload.md)
- [useUpload Reference](artifact/references/use-upload.md)
- [Calendar Reference](artifact/references/calendar.md)
- [Toast Reference](artifact/references/toast.md)
- [useToast Reference](artifact/references/use-toast.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration guidance]

**Output Format:** [Markdown prose with Vue and TypeScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese answers and script setup examples when supported by the bundled component documentation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
