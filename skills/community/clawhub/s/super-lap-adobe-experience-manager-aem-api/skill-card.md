## Description:

Provides agent guidance for working with Adobe Experience Manager API endpoints, including setup, authentication, system operations, content management, asset handling, and platform automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to map AEM administration and content-management requests to the appropriate API endpoints, authentication setup, and request patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers privileged AEM administration and destructive POST or DELETE operations.

Mitigation: Use least-privilege tokens, verify the target AEM host, and require explicit confirmation before mutating or deleting resources.

Risk: The bundled CLI examples use npx to run lapsh commands.

Mitigation: Pin or review the lapsh package before running generated npx commands.

Risk: The security evidence reports insufficient scoping, confirmation, and safe-use guidance for powerful AEM actions.

Mitigation: Test outside production first and review generated requests before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/subaru0573/skills/super-lap-adobe-experience-manager-aem-api)
- [LAP](https://lap.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with endpoint mappings, setup guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require an Adobe Experience Manager API credential supplied as ADOBE_EXPERIENCE_MANAGER_AEM_API_KEY.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
