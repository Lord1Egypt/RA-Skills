## Description: <br>
Archives one-minute, delta-compressed spatial state data in a local SQLite memory vault with causal event logs and privacy-preserving external video pointers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building smart-space agents use this skill to simulate a local time-series memory layer for environment state, agent decisions, avatar mandates, and external camera references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes a local SQLite database and persists demo memory data in the directory where it is run. <br>
Mitigation: Run it from a dedicated project folder and delete s2_memory_vault/s2_chronos.db when the persisted data is no longer needed. <br>
Risk: Smart-home state or camera reference data used with the skill may be sensitive. <br>
Mitigation: Use mock or minimized inputs unless real data is intended, and avoid placing sensitive camera or smart-home identifiers in the input template. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-chronos-memzero) <br>
- [S2-SP-OS Ultimate Whitepaper: The Chronos Holographic Memory Array](artifact/S2-SP-OS-ltimate-Whitepaper.md) <br>
- [S2 Chronos Memory Whitepaper](artifact/S2 时空全息记忆阵列白皮书.md) <br>
- [Space2.world](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Configuration] <br>
**Output Format:** [Console text plus local SQLite database and JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Execution writes s2_memory_vault/s2_chronos.db in the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact manifest and SKILL.md list 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
