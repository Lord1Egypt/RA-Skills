## Description:

Classify cyber security incidents, CVEs, threat-intelligence reports, red-team write-ups, and vendor advisories using the TLCTC v2.7 taxonomy (10 cause-oriented threat clusters, 10 axioms, 17 R-* classification rules incl. the R-SCOPE scope gate and R-SPECIFIC, System Risk Event doctrine, DRE refinement tree, consequence chain, attack-path notation with Δt velocity and boundary operators). Use whenever the user asks to analyze, classify, deconstruct, or build attack paths for security documents, or references "TLCTC", "threat clusters", "attack path", "#1"–"#10" cluster IDs, or "TLCTC-XX.YY" identifiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barnes70](https://clawhub.ai/user/barnes70)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts and incident responders use this skill to classify incident reports, CVEs, threat intelligence, red-team write-ups, and vendor advisories under TLCTC v2.7. It helps describe causal threat clusters, attack paths, consequences, uncertainty, and control recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the broad activation rule may cause the skill to activate on ordinary numbered references and redirect unrelated requests; some static checks could not fully evaluate obfuscated instruction text.

Mitigation: Review the activation rule before installation and invoke the skill only for TLCTC or security-classification work; assess its outputs against the source material.

## Reference(s):

- [TLCTC framework homepage](https://www.tlctc.net)
- [TLCTC v2.7 core paper](https://doi.org/10.5281/zenodo.20633176)
- [TLCTC framework repository](https://github.com/Barnes70/TLCTC)
- [TLCTC Layer 3 JSON schemas](https://github.com/Barnes70/TLCTC/tree/main/json-schemas/layer-3)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Structured Markdown analysis with attack-path notation; optional JSON export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes framework-based classifications, confidence and uncertainty notes, and control recommendations when relevant.]

## Skill Version(s):

2.7.1 (source: frontmatter; confirmed by server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
