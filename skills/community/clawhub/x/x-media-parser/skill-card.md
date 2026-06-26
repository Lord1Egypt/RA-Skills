## Description: <br>
Parses X/Twitter posts to extract direct download links for images, videos, and GIFs through the vxtwitter API without requiring login. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ingress007](https://clawhub.ai/user/Ingress007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can use this skill to parse public X/Twitter status URLs, return direct media URLs and metadata, and optionally hand those URLs to Aria2 for downloading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Aria2 helper can create download jobs and save files locally using RPC settings. <br>
Mitigation: Inspect and change the Aria2 RPC endpoint, secret, and output directory before use, and run download actions only where local file creation is intended. <br>
Risk: Parsing sends X/Twitter status identifiers to an external vxtwitter API. <br>
Mitigation: Avoid passing sensitive or private tweet URLs, and use the parser only when external API requests are acceptable. <br>


## Reference(s): <br>
- [X Media Parser ClawHub release](https://clawhub.ai/Ingress007/x-media-parser) <br>
- [vxtwitter status API endpoint](https://api.vxtwitter.com/Twitter/status/{tweetId}) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Files] <br>
**Output Format:** [JSON responses with media URLs and metadata, plus shell command usage for optional Aria2 downloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Media output may include direct URLs, video and image URL arrays, thumbnails, duration, and resolution; the download helper can create Aria2 jobs that save files locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
