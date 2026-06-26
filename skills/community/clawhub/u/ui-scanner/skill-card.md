## Description: <br>
Given a website URL, crawl and analyze its visual design system - identify design style, color system, typography, component styles, and UI patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and UI engineers use this skill to inspect a website URL and produce a structured design-system specification for UI replication, design audits, competitive analysis, or style transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches a user-provided website URL, which can expose private internal pages or sensitive URLs if supplied as input. <br>
Mitigation: Use public or intended-for-review URLs unless you explicitly want the page content fetched and summarized locally. <br>
Risk: The generated design specification can include estimates when precise values are unavailable from static page assets. <br>
Mitigation: Review any estimated colors, typography, spacing, or component values before using the output as a production design-system source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/ui-scanner) <br>
- [OpenLark publisher profile](https://clawhub.ai/user/openlark) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown file with YAML frontmatter and structured design-system sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a {domain}_design.md file containing extracted colors, typography, spacing, border radii, component styles, and design guidelines.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
