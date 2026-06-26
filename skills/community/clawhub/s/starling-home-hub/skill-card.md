## Description: <br>
Controls Nest and Google Home smart home devices via the Starling Home Hub's local REST API, including thermostats, cameras, Nest Protects, Nest x Yale locks, temperature sensors, home/away control, and Nest weather service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaeljmoody](https://clawhub.ai/user/michaeljmoody) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage Nest and Google Home devices through a Starling Home Hub, including reading device status, changing writable device properties, retrieving camera snapshots, and controlling home/away state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent with the Starling API key can control local smart-home devices, including locks, cameras, streams, thermostats, and home/away state. <br>
Mitigation: Use a read-only or least-privilege API key when possible, and require manual confirmation for lock, camera, stream, and home/away changes. <br>
Risk: API keys and device data may be exposed if the key is passed on the command line or if HTTP is used on the local network. <br>
Mitigation: Use STARLING_API_KEY from the environment, avoid --key and --http, and keep HTTPS enabled. <br>
Risk: The hub uses a self-signed certificate by default, which can increase local-network interception risk when certificate verification is skipped. <br>
Mitigation: Pin the hub certificate with --cacert when possible and run the skill only on a trusted local network. <br>


## Reference(s): <br>
- [Starling Home Hub Developer Connect API Reference](references/api-reference.md) <br>
- [Starling Home Hub](https://starlinghome.io) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands; script responses are JSON or camera snapshot files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STARLING_HUB_IP and STARLING_API_KEY. Some commands can change smart-home device state.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
