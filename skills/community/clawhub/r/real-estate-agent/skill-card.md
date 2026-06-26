## Description: <br>
Your personal real estate agent. Find properties, get alerts on deals, sell or rent your home, and navigate any property decision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill as a personal real estate assistant for buying, selling, renting, investing, or managing properties. It helps capture client criteria, track property opportunities, compare market context, optimize listings, and maintain local notes and alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may retain sensitive housing and financial context such as budgets, financing status, locations, timelines, and property interests in local files. <br>
Mitigation: Use it only when local file-based memory is acceptable; decide what should not be saved, inspect ~/real-estate-agent/ periodically, and delete or redact details that are no longer needed. <br>
Risk: Real-estate analysis or listing guidance could be mistaken for legal, mortgage, tax, or investment advice. <br>
Mitigation: Treat outputs as informational market context and have qualified professionals review contracts, financing, tax questions, and binding decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/real-estate-agent) <br>
- [Skill homepage](https://clawic.com/skills/real-estate-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown and conversational text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Markdown files under ~/real-estate-agent/ for client profiles, saved searches, tracked properties, and alerts when used with consent.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
