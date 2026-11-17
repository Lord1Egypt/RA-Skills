## Description:

Builds complete, modern multi-page React websites for local businesses using Vite, React, Tailwind CSS, React Router, Framer Motion, and Lucide React.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to scaffold and generate polished five-page React websites for local or small businesses. It supports common business categories with page templates, design guidance, image selection guidance, and production build verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated local-business sites can include placeholder or unverified claims such as awards, reviews, statistics, licenses, contact details, and response-time promises.

Mitigation: Before publishing, replace placeholder business details and verify all reviews, licenses, awards, statistics, and service claims against authoritative business records.

Risk: The setup flow installs npm dependencies and includes a preview-server command that may bind beyond localhost if copied directly.

Mitigation: Install in an isolated project environment, review and pin npm dependencies before running setup, and bind the development server to localhost unless remote access is intentional.

Risk: The sample contact form can display success and privacy messaging without evidence of a connected backend or operational privacy process.

Mitigation: Connect the contact form to a real backend and privacy process before launch, or remove success and privacy claims that the deployed site cannot support.

## Reference(s):

- [React Local Business Website Skill Page](https://clawhub.ai/maverick-software/skills/react-local-biz)
- [Business Types: Color Palettes & Image Packs](artifact/references/business-types.md)
- [Design System Reference](artifact/references/design-system.md)
- [Page Templates Reference](artifact/references/page-templates.md)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline bash commands and React/Tailwind file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a five-page Vite React site structure with reusable components, route configuration, responsive page templates, image guidance, and build verification steps.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
