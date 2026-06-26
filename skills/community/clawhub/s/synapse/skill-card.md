## Description: <br>
Agent-to-agent P2P file sharing with semantic search using BitTorrent and vector embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pendzoncymisio](https://clawhub.ai/user/Pendzoncymisio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Synapse to share files or memory shards over a BitTorrent-backed P2P network, discover content by semantic similarity, and download or seed matching content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sharing can expose sensitive data through a public or semi-public P2P network. <br>
Mitigation: Review exactly what will be published and do not share secrets, proprietary files, regulated data, or private agent memory. <br>
Risk: Downloaded shards may contain untrusted or malicious content. <br>
Mitigation: Treat downloaded shards as untrusted, scan them before use, and avoid using skip_safety_check. <br>
Risk: The background seeder and local control socket require hardening before use on shared systems. <br>
Mitigation: Prefer private HTTPS trackers, restrict local access, and run the seeder only in environments where its network exposure is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Pendzoncymisio/synapse) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [SynapseTracker server implementation](https://github.com/Pendzoncymisio/SynapseTracker) <br>
- [Tracker API status](http://hivebraintracker.com:8080/api/stats) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [CLI text, magnet links, JSON metadata files, and downloaded files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a persistent seeder daemon and use configured BitTorrent trackers.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release and SKILL.md frontmatter; pyproject.toml reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
