<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: workflows

## `slk api workflows step-completed [options]`

- What: workflows\_stepCompleted — write (GET /workflows.stepCompleted)
- Call: `GET /workflows.stepCompleted`, effect: write

| Flag | Required | What |
|---|---|---|
| `--workflow-step-execute-id <value>` | yes | Context identifier that maps to the correct workflow step execution. |
| `--outputs <value>` | no | Key-value object of outputs from your step. Keys of this object reflect the configured \`key\` properties of your \[\`outputs\`\](https://api.slack.com/reference/workflows/workflow\_step#output) array from your \`workflow\_step\` object. |

## `slk api workflows step-failed [options]`

- What: workflows\_stepFailed — write (GET /workflows.stepFailed)
- Call: `GET /workflows.stepFailed`, effect: write

| Flag | Required | What |
|---|---|---|
| `--workflow-step-execute-id <value>` | yes | Context identifier that maps to the correct workflow step execution. |
| `--error <value>` | yes | A JSON-based object with a \`message\` property that should contain a human readable error message. |

## `slk api workflows update-step [options]`

- What: workflows\_updateStep — write (GET /workflows.updateStep)
- Call: `GET /workflows.updateStep`, effect: write

| Flag | Required | What |
|---|---|---|
| `--workflow-step-edit-id <value>` | yes | A context identifier provided with \`view\_submission\` payloads used to call back to \`workflows.updateStep\`. |
| `--inputs <value>` | no | A JSON key-value map of inputs required from a user during configuration. This is the data your app expects to receive when the workflow step starts. \*\*Please note\*\*: the embedded variable format is set and replaced by the workflow system. You cannot create custom variables that will be replaced at runtime. \[Read more about variables in workflow steps here\](https://api.slack.com/workflows/steps#variables). |
| `--outputs <value>` | no | An JSON array of output objects used during step execution. This is the data your app agrees to provide when your workflow step was executed. |
| `--step-name <value>` | no | An optional field that can be used to override the step name that is shown in the Workflow Builder. |
| `--step-image-url <value>` | no | An optional field that can be used to override app image that is shown in the Workflow Builder. |
