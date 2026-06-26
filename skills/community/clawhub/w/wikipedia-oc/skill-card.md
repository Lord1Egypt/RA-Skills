## Description: <br>
Searches, retrieves, and summarizes English Wikipedia content using the `wikipedia` Python module. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachmann-alexander](https://clawhub.ai/user/rachmann-alexander) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search English Wikipedia, retrieve candidate pages, and return concise summaries or structured page data with attribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wikipedia content can be inaccurate, incomplete, or insufficient for legal, medical, local, or time-sensitive topics. <br>
Mitigation: Verify the source article and important facts independently before relying on the answer for sensitive or current decisions. <br>
Risk: The skill deliberately searches English Wikipedia, even when the user asks in another language. <br>
Mitigation: Retrieve from English Wikipedia first, then translate only as post-processing while preserving the original meaning and source attribution. <br>
Risk: Ambiguous queries or missing pages can produce the wrong article or no useful result. <br>
Mitigation: Limit and inspect candidate results, handle disambiguation and page errors explicitly, and refine the query when needed. <br>
Risk: The public Wikipedia API may time out or rate-limit requests. <br>
Mitigation: Handle timeout errors, keep requests focused, and retry or defer work when the API is unavailable. <br>
Risk: An outdated `wikipedia` module can miss fixes or security improvements. <br>
Mitigation: Check whether a newer module version is available and disclose the current and latest versions to the user when an update is found. <br>


## Reference(s): <br>
- [wikipedia Python package](https://pypi.org/project/wikipedia/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-like structured text with title, summary, URL, or error details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should disclose Wikipedia as the source, include a page URL when content is fetched, prefer summaries by default, and avoid excessive raw page content unless explicitly required.] <br>

## Skill Version(s): <br>
0.1.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
