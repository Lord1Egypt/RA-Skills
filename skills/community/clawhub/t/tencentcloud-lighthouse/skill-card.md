## Description:

Manages Tencent Cloud Lighthouse instances, including creation, deletion, power actions, status queries, promotion lookup, and cost-control guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Tencent Cloud Lighthouse servers, compare predefined instance plans and images, and run lifecycle actions from an agent-assisted workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented CAM policy grants broad lighthouse and VPC permissions over all resources.

Mitigation: Use a least-privilege Tencent Cloud sub-user, remove unused VPC permissions, and scope actions and resources wherever Tencent Cloud IAM supports it.

Risk: The skill can create, renew, modify, stop, restart, and delete paid Lighthouse instances.

Mitigation: Require human confirmation before destructive or billable actions, and keep budget alerts enabled for accounts where the skill is used.

Risk: Tencent Cloud API credentials are loaded from environment configuration and troubleshooting material may encourage displaying config contents.

Mitigation: Do not paste or display .env or config contents in shared logs or chats; rotate sub-user keys regularly.

Risk: Runtime dependencies are installed into the Python environment used by the agent.

Mitigation: Use an isolated virtual environment with pinned versions for tencentcloud-sdk-python and python-dotenv.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ugpoor/skills/tencentcloud-lighthouse)
- [Tencent Cloud Lighthouse API](https://cloud.tencent.com/document/api/1170)
- [Tencent Cloud promotion center](https://cloud.tencent.com/act)
- [Tencent Cloud Lighthouse application image documentation](https://cloud.tencent.com/document/product/1170/38176)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tencent Cloud API actions that create, renew, stop, restart, modify, or delete paid Lighthouse resources.]

## Skill Version(s):

1.2.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
