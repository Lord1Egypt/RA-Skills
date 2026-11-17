## Description:

uView UI helps agents provide component references, setup guidance, and Vue examples for uni-app Vue 2 projects using the uView UI 2.x component library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufengsheng](https://clawhub.ai/user/wufengsheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill while building uni-app Vue 2 mobile and multi-platform pages with uView UI components, utility functions, layout patterns, and common interaction examples. It supports fast lookup of component APIs and generation of Vue-oriented implementation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTTP interceptor or token-injection examples could expose credentials or apply authentication logic too broadly.

Mitigation: Review generated request configuration, token handling, and interceptor behavior before using it in production.

Risk: Upload and rich-text parsing examples can process untrusted files, URLs, or markup.

Mitigation: Validate uploads server-side and sanitize or constrain rendered rich-text content before deployment.

Risk: OTP and sharing examples can affect user verification flows or global page behavior.

Mitigation: Confirm rate limits, backend verification, and global mixin scope before integrating these examples.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wufengsheng/skills/uview-ui)
- [uView UI Introduction](https://www.uviewui.com/components/intro.html)
- [uView UI Installation](https://www.uviewui.com/components/install.html)
- [uView UI Quickstart](https://www.uviewui.com/components/quickstart.html)
- [uView UI Compatibility Notes](https://www.uviewui.com/components/feature.html)
- [uView HTTP Utility](https://www.uviewui.com/js/http.html)
- [uView Upload Component](https://www.uviewui.com/components/upload.html)
- [uView Parse Component](https://www.uviewui.com/components/parse.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with Vue, JavaScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include component API summaries, setup steps, code snippets, and review notes for security-relevant examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
