## Description:

Build, edit, debug, and package Xiaomi Vela JS quick apps for wearable devices such as Xiaomi Band 10.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tlrenhb](https://clawhub.ai/user/tlrenhb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, modify, build, debug, and package Xiaomi Vela JS quick apps for wearable devices. It is especially suited for scaffolding Vela projects, editing `.ux` pages, resolving `npx aiot build` errors, adapting interfaces for Xiaomi Band or Watch screens, and producing `.rpk` packages after a successful build.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The normal workflow can run unpinned npm/npx build tooling that may fetch and execute changing third-party code.

Mitigation: Pin `aiot-toolkit`, commit a lockfile, install reproducibly with `npm ci`, and prefer a local executable or `npx --no-install` before allowing build steps.

## Reference(s):

- [Dev Workflow](references/dev-workflow.md)
- [Vela Docs Map](references/docs-map.md)
- [UX Gotchas](references/ux-gotchas.md)
- [Vela Notes](references/vela-notes.md)
- [Xiaomi Vela Project Structure](https://iot.mi.com/vela/quickapp/zh/guide/start/project-overview.html)
- [Xiaomi Vela Framework Overview](https://iot.mi.com/vela/quickapp/zh/guide/framework/)
- [Xiaomi Vela Components](https://iot.mi.com/vela/quickapp/zh/components/)
- [Xiaomi Vela Feature APIs](https://iot.mi.com/vela/quickapp/zh/features/)
- [Xiaomi Vela Sensor APIs](https://iot.mi.com/vela/quickapp/zh/features/system/sensor.html)
- [Xiaomi Vela AIoT IDE Quick Start](https://iot.mi.com/vela/quickapp/zh/guide/start/use-ide.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code snippets, shell commands, file paths, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify Vela project files and identify generated `.rpk` package paths after a successful build.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
