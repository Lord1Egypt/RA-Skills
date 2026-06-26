## Description: <br>
Analyze video content, extract keyframes, search web for references, generate Feishu Wiki reports, and process batches with category-based publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow operators use this skill to process single videos or directories of videos into extracted frames, search references, Supabase records, and Feishu Wiki reports. It is suited for teams that need repeatable video analysis summaries and category index pages for batch runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses powerful Supabase and Feishu credentials and can store or publish video-derived content. <br>
Mitigation: Use least-privilege Supabase and Feishu credentials, verify the destination wiki space, and start with non-sensitive test videos. <br>
Risk: The package includes unrelated agent, watch, memory, and nested browser-skill files that may introduce behavior outside the video-analysis workflow. <br>
Mitigation: Remove or ignore those unrelated files unless those behaviors are explicitly intended for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/video-content-analyzer-batch) <br>
- [Feishu OpenAPI tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/) <br>
- [Feishu OpenAPI wiki nodes endpoint](https://open.feishu.cn/open-apis/wiki/v2/nodes) <br>
- [Google Custom Search API endpoint](https://www.googleapis.com/customsearch/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration] <br>
**Output Format:** [Markdown wiki reports, JSON-like status dictionaries, extracted frame image files, and Supabase records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch runs can create per-video reports, category index pages, batch job status records, and local frame outputs.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
