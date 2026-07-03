## Description: <br>
Manage a vending machine fleet by sending credits, inspecting device health, querying sales and inventory, and triggering firmware updates through MQTT RPC and Supabase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nodestark](https://clawhub.ai/user/nodestark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External fleet operators and developers use this skill to monitor VMflow vending devices, review sales and inventory, diagnose device health, and prepare signed device commands for authorized machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to issue credit, restart, out-of-sequence, and firmware update actions against real vending machines. <br>
Mitigation: Require manual approval for device-changing commands and prefer read-only diagnostics before any operational command. <br>
Risk: The skill depends on Supabase credentials and per-device passkeys that can authorize fleet data access or signed device commands. <br>
Mitigation: Install only for authorized VMflow fleet operators, keep credentials out of logs and chat output, and limit agent access to the minimum required environment variables. <br>


## Reference(s): <br>
- [VMflow skill page](https://clawhub.ai/nodestark/skills/vmflow) <br>
- [Publisher profile](https://clawhub.ai/user/nodestark) <br>
- [VMflow project homepage](https://github.com/nodestark/mdb-esp32-cashless) <br>
- [Firmware RPC handler](https://github.com/nodestark/mdb-esp32-cashless/blob/main/mdb-slave-esp32s3/main/mdb-slave-esp32s3.c) <br>
- [Supabase schema migrations](https://github.com/nodestark/mdb-esp32-cashless/tree/main/docker/supabase/migrations) <br>
- [VMflow dashboard](https://vmflow.xyz/dashboard) <br>
- [Agent context and BLE payload spec](artifact/AGENTS.md) <br>
- [RPC helper script](artifact/tools/rpc.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include signed MQTT command examples, Supabase REST queries, operational playbooks, and device diagnostic summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
