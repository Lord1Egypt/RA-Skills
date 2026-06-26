## Description: <br>
Integrate and troubleshoot React Native Update OTA for Pushy and Cresc. Use when wiring react-native-update into React Native CLI, Expo prebuild, HarmonyOS, brownfield, monorepo, or mixed native apps; configuring update.json/appKey, Pushy/Cresc clients, UpdateProvider/useUpdate, iOS/Android/Harmony bundle loading, release baseline upload, checkStrategy/updateStrategy, canary/metaInfo flows, expo-updates conflicts, or OTA diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnylqm](https://clawhub.ai/user/sunnylqm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate React Native Update OTA workflows into React Native, Expo prebuild, HarmonyOS, brownfield, monorepo, and mixed native apps. It guides service selection, native bundle loading, provider wiring, release baseline upload, update publishing, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide package installs, native project edits, release builds, and uploads to Pushy or Cresc. <br>
Mitigation: Review generated configuration, service/account choices, and native changes before applying them to a production app. <br>
Risk: The diagnostic script inspects the app directory supplied by the user. <br>
Mitigation: Run the diagnostic script only against the React Native app intended for inspection. <br>
Risk: OTA behavior depends on matching the CLI, dashboard app records, update.json values, and JavaScript client service. <br>
Mitigation: Keep Pushy or Cresc choices consistent across CLI commands, dashboard records, update.json, and the initialized client. <br>


## Reference(s): <br>
- [React Native Update integration playbook](references/integration-playbook.md) <br>
- [React Native Update on ClawHub](https://clawhub.ai/sunnylqm/react-native-update) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include minimal integration diffs, verification checklists, troubleshooting guidance, and diagnostic command output interpretation.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
