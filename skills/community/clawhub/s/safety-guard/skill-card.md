## Description: <br>
OpenClaw Safety Guard helps agents use the safety-guard CLI to scan URLs, local files, and YouTube links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[John-niu-07](https://clawhub.ai/user/John-niu-07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to run safety checks on web pages, local PDFs, images, audio files, and YouTube links with a configurable model provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact metadata slug does not match the server-resolved release slug. <br>
Mitigation: Verify the ClawHub release, publisher handle, and Homebrew formula before installing or recommending the package. <br>
Risk: URLs, files, audio, images, or YouTube content may be sent to configured third-party model or extraction services. <br>
Mitigation: Use limited-scope API keys and avoid confidential files or private URLs unless third-party processing is acceptable. <br>
Risk: Optional Firecrawl and Apify fallback services can expand the set of third-party processors involved. <br>
Mitigation: Disable Firecrawl or Apify fallback modes when they are not required. <br>


## Reference(s): <br>
- [Safety Guard homepage](https://safety-guard.sh) <br>
- [ClawHub skill page](https://clawhub.ai/John-niu-07/safety-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on configured provider API keys and optional Firecrawl or Apify services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
