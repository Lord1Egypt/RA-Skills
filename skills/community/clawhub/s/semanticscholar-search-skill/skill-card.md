## Description:

Searches Semantic Scholar for academic papers, paper details, author profiles, citations, and references with console or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackkuo666](https://clawhub.ai/user/jackkuo666)

### License/Terms of Use:

MIT

## Use Case:

Researchers, students, and developers use this skill to discover academic literature, inspect paper metadata, review author profiles, and analyze citation or reference links through Semantic Scholar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommended installation paths may run mutable remote code or install unpinned packages.

Mitigation: Prefer a reviewed Python virtual environment installation, pin dependencies and installer sources to approved versions, and avoid elevated privileges during setup.

Risk: The tool contacts Semantic Scholar and can write JSON files to paths provided by the user.

Mitigation: Review outbound network use before deployment and choose output paths that do not overwrite sensitive or important files.

## Reference(s):

- [Semantic Scholar API](https://www.semanticscholar.org/product/api)
- [ClawHub Skill Page](https://clawhub.ai/jackkuo666/skills/semanticscholar-search-skill)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Console text or JSON, with optional JSON file export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Semantic Scholar network requests and may write JSON output to a user-provided path.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
