## Description: <br>
Plan and execute mission-driven X growth operations, including monitoring KOL posts, detecting emerging discussions, turning briefs or uploaded docs into a growth mission, drafting replies or posts, ranking opportunities, and executing approved actions with a local audit trail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JimmyWangJimmy](https://clawhub.ai/user/JimmyWangJimmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators, founders, marketers, and developers use this skill to turn a brief into a review-first X growth workflow: create a mission, import or search opportunities, rank them, draft posts or interactions, and execute only approved actions through X credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live X execution can post through authenticated credentials. <br>
Mitigation: Use least-privilege credentials where possible, keep scripts/.env private, and execute live actions only after reviewing the proposed action. <br>
Risk: The local dashboard and live posting paths are not fully protected by server-side approval or authentication. <br>
Mitigation: Avoid leaving the dashboard running unattended and prefer dry-run or review mode until the publisher adds stronger server-side approval and authentication. <br>
Risk: Live search/import may rely on Desearch network access that is not fully documented in the artifact. <br>
Mitigation: Treat DESEARCH_API_KEY as optional, review live-search behavior before use, and operate on imported JSON or manual notes when the endpoint is not trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JimmyWangJimmy/x-growth-operator) <br>
- [Mission schema and scoring reference](references/mission-schema.md) <br>
- [X API endpoint](https://api.x.com) <br>
- [Twitter API endpoint](https://api.twitter.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and generated JSON files such as mission, scored opportunities, action plans, action proposals, execution logs, and memory state.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review-first workflow; real X posting requires configured OAuth credentials and explicit approval.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
