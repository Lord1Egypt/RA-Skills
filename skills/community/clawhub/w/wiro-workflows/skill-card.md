## Description:

Design, save, run, test, repair and edit Wiro AI workflows, the saved chains of model steps with their own inputs and results, through the Wiro MCP tools or the REST API, alone or with the Workflow Agent. Use when the user wants a repeatable pipeline on Wiro (for example product photo to ad video, text to voice-over to captions), or asks to run, resume, clone, change or debug a Wiro workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiroai](https://clawhub.ai/user/wiroai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to design and manage reusable Wiro workflows that chain model steps, utilities, and user inputs. It guides agents through choosing between one-off runs, saved workflows, and the Workflow Agent, and through running or troubleshooting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow text and referenced files may be sent to Wiro when a workflow runs.

Mitigation: Avoid sending sensitive or confidential material unless that transfer is authorized, and review what data the workflow uses.

Risk: The security scan was partial because some local references could not be resolved, so its evidence is incomplete.

Mitigation: Review referenced files and workflow behavior before installing or running the skill.

## Reference(s):

- [Wiro Workflows Documentation](https://wiro.ai/docs/workflows)
- [Wiro Workflow Agent Documentation](https://wiro.ai/docs/workflow-agent)
- [Wiro MCP Server Documentation](https://wiro.ai/docs/wiro-mcp-server)
- [Wiro Workflows](https://wiro.ai/workflows)
- [Wiro AI Workflows on ClawHub](https://clawhub.ai/wiroai/skills/wiro-workflows)

## Skill Output:

**Output Type(s):** [Workflow configuration, API calls, Guidance, Workflow results]

**Output Format:** [Workflow graph JSON, API requests, and text or media returned by workflow runs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the models and steps selected for each workflow.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
