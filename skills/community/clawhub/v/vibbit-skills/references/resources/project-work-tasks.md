# Projects, works, and tasks

Use the contents to read only the section needed for the current operation. Each section retains its own parameters, authorization, and execution boundaries.

- [Projects](#projects)
- [Existing works](#works)
- [Tasks](#tasks)

<a id="projects"></a>

## Projects

There is no unified public project query or save command. A project-page URL does not reveal valid API parameters. Local creative records, cloud task IDs, and platform project IDs are separate.

A talking-head request can proceed directly through supported audio and avatar generation without project initialization. Producing replacement media does not mean it has been applied to a platform project. Report only actual saves and updates. See [creative handoff](../contracts/creative-handoff.md).

<a id="works"></a>

## Existing works

There is no public work-library query or write command. Use the actual file, media URL, or task ID supplied in context. Identify the selected version explicitly rather than assuming the newest file is the approved one.

A generated revision is new media. Do not claim the platform's current work has changed without a successful supported save operation. Review and revise through [video review](../capabilities/analysis/video-review.md).

<a id="tasks"></a>

## Tasks

Use [task query](../runtime/task-lifecycle.md) for a known task ID. There is no public full-history listing command or cross-account task search. Resume from this task's context and redacted journal; do not search unrelated accounts.

Inspect the actual state and result before deciding to retry. Preserve completed parts, report terminal errors, and stop when a required capability or authorization is unavailable. See [task lifecycle](../runtime/task-lifecycle.md).
