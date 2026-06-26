## Description: <br>
Website crawling, auditing, offline cloning, and markdown export using SiteOne Crawler. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsingliuwin](https://clawhub.ai/user/tsingliuwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run website crawls, audits, offline exports, markdown exports, sitemap generation, and CI quality checks through SiteOne Crawler. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run an external SiteOne Crawler executable that is not checksum verified by the artifact. <br>
Mitigation: Use a pinned, checksum-verified crawler release from a trusted upstream before running the binary. <br>
Risk: Crawling or stress-testing can generate heavy traffic against target sites. <br>
Mitigation: Run crawls only against sites you own or are authorized to test, and keep worker and request-rate limits conservative. <br>
Risk: Uploaded crawl reports can expose private or authenticated site information. <br>
Mitigation: Keep report upload disabled for private or authenticated sites unless remote sharing is intentional and approved. <br>
Risk: Credentials passed directly in command-line flags can be exposed through shell history or process listings. <br>
Mitigation: Avoid passing real secrets directly on the command line; use safer secret handling where available. <br>


## Reference(s): <br>
- [SiteOne Crawler CLI Parameters Reference](references/cli-params.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tsingliuwin/siteone-crawler) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and generated file outputs such as HTML reports, JSON results, markdown exports, offline site files, and sitemap files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local files and can optionally upload crawl reports when explicitly enabled.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
