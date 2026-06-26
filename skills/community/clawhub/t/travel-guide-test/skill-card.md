## Description: <br>
Plan trips end-to-end and turn them into polished static travel-guide webpages deployed to Cloudflare Pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cianweeresinghe-sudo](https://clawhub.ai/user/cianweeresinghe-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel planners use this skill to shape trip routes, itineraries, lodging options, transport plans, and booking checklists around traveller preferences and constraints. Once the trip structure is stable, it can package the plan as an image-led static travel guide and prepare it for Cloudflare Pages deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish travel plans as a public Cloudflare Pages site, which may expose personal trip, family, or schedule details. <br>
Mitigation: Before deployment, review the final page for sensitive details and remove private information that should not be public. <br>
Risk: The skill may request Cloudflare access information to deploy a site. <br>
Mitigation: Use a secure secret mechanism, grant only the minimum required Cloudflare permissions, and confirm the target account and project before deployment. <br>
Risk: The security summary notes unclear final confirmation before publishing. <br>
Mitigation: Require an explicit user confirmation of the exact content and destination before deploying the travel guide. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cianweeresinghe-sudo/travel-guide-test) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown travel planning guidance, static HTML/CSS, deployment commands, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include route summaries, map links, image sourcing notes, hotel shortlists, booking checklists, and Cloudflare Pages URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
