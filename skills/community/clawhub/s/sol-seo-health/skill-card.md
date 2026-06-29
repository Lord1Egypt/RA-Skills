## Description: <br>
Daily SEO health check that validates blog post SEO completeness, sitemap, robots.txt, meta tags, broken links, and RSS feed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amrree](https://clawhub.ai/user/amrree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site maintainers use this skill to run routine SEO health checks for a blog or static site and identify missing metadata, broken internal links, duplicate titles, and feed or sitemap issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references a hardcoded site repository path. <br>
Mitigation: Confirm the path is correct for the deployment environment before enabling the audit. <br>
Risk: The skill is intended to read site files, make web requests, and write a local log. <br>
Mitigation: Grant file and network access only in the expected site workspace and review generated findings before acting on them. <br>
Risk: The skill describes a daily launchd schedule after site builds. <br>
Mitigation: Confirm the schedule is appropriate and disable or adjust it if automated post-build checks are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amrree/skills/sol-seo-health) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command and configuration details, plus local text log output from the described audit workflow.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes issue counts and individual problem listings to logs/sol-seo.log.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
