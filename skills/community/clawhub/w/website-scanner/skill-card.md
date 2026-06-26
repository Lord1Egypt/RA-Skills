## Description: <br>
Comprehensive website analysis and scanning tool that analyzes IP addresses, DNS records, WHOIS data, website content, SEO metrics, crawler files, structured data, and third-party data, with optional deep scanning for multiple pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hugogu](https://clawhub.ai/user/hugogu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and technical auditors use this skill to inspect a website or domain's infrastructure, crawler files, page metadata, structured data, and SEO signals. It is suited for authorized scans that produce shareable technical reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner makes outbound requests and may send target-derived domain or IP data to third-party services. <br>
Mitigation: Run it only for sites you are authorized to scan, and avoid targets or environments where sharing target-derived network data with third parties is not acceptable. <br>
Risk: Deep scans can follow sitemap URLs to unexpected hosts. <br>
Mitigation: Review the target sitemap and use conservative page limits; run deep scans from an isolated environment when scanning untrusted targets. <br>
Risk: The security review notes missing same-origin and private-address protections. <br>
Mitigation: Avoid running scans from sensitive networks until those protections are added, and prefer a sandboxed environment for untrusted targets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hugogu/website-scanner) <br>
- [ipapi geolocation endpoint](https://ipapi.co/{ip}/json/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, PDF, shell commands] <br>
**Output Format:** [Console report with optional JSON and PDF report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can include DNS, WHOIS, IP geolocation, content metadata, SEO findings, crawler-file excerpts, Google index checks, and optional deep-scan page results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
