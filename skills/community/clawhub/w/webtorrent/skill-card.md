## Description: <br>
Use WebTorrent to implement streaming BitTorrent client functionality in Node.js and the browser, including torrent downloading, seeding, magnet links, streaming media playback, and peer-to-peer transfer via WebRTC in browsers and TCP/UDP in Node.js. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add WebTorrent-based downloading, seeding, browser peer-to-peer transfer, and streaming media playback to Node.js or browser applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BitTorrent and WebTorrent activity can expose users to peer-to-peer privacy, legal, and content-trust risks. <br>
Mitigation: Use legal torrents, obtain explicit consent before seeding local files, and treat downloaded content as untrusted. <br>
Risk: Peer discovery, seeding, and upload behavior may be broader than a deployment needs. <br>
Mitigation: Limit or disable DHT, tracker, LSD, or upload behavior when not required, and set download paths deliberately. <br>
Risk: Unpinned global or CDN package installs can introduce dependency supply-chain uncertainty. <br>
Mitigation: Pin production dependencies and prefer controlled package installation paths over ad hoc global or CDN installs. <br>


## Reference(s): <br>
- [WebTorrent Complete API Reference](references/api-reference.md) <br>
- [WebTorrent skill page](https://clawhub.ai/openlark/webtorrent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with JavaScript, HTML, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides implementation guidance for WebTorrent APIs, CLI usage, browser and Node.js environment differences, and safe torrent handling practices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
