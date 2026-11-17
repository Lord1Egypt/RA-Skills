## Description:

Integrate and troubleshoot React Native Update OTA for Pushy and Cresc.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnylqm](https://clawhub.ai/user/sunnylqm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate and troubleshoot React Native Update OTA flows across React Native CLI, Expo prebuild, HarmonyOS, brownfield, monorepo, and mixed native applications. It helps produce minimal integration diffs, verification checklists, and targeted troubleshooting guidance for Pushy or Cresc releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The app may be wired to the wrong OTA service if Pushy and Cresc commands, dashboard records, app keys, or JS client classes are mixed.

Mitigation: Confirm whether the app should use Pushy or Cresc before applying changes, and keep the CLI, dashboard, update.json records, and client class on the same service.

Risk: Package installation or CLI setup may introduce unreviewed dependency changes.

Mitigation: Prefer pinned project-local dependencies when the workflow allows it, and review lockfile changes before committing.

Risk: Release baseline upload and hot-update publishing can affect distributed app behavior.

Mitigation: Treat baseline uploads and hot-update publishing as reviewed release actions, and verify the uploaded baseline matches the package distributed to users.

Risk: Local update state may be committed unintentionally.

Mitigation: Do not commit the .update file; confirm it is ignored when present.

## Reference(s):

- [React Native Update integration playbook](references/integration-playbook.md)
- [ClawHub skill page](https://clawhub.ai/sunnylqm/skills/react-native-update)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code snippets, shell commands, file-specific diffs, checklists, and troubleshooting notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include release-build verification steps, baseline upload checks, and Pushy/Cresc service selection guidance.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
