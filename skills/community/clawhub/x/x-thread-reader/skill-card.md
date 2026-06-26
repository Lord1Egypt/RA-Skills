## Description: <br>
Fetch full text or generate a PDF from any X/Twitter thread using twitter-thread.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ngmeyer](https://clawhub.ai/user/ngmeyer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to retrieve readable text from public X/Twitter threads or save thread content as a PDF for citation, archiving, notes, or follow-on analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tweet or thread IDs are sent to twitter-thread.com when fetching content. <br>
Mitigation: Use only when sending the target public thread identifier to that third-party service is acceptable. <br>
Risk: PDF mode depends on local browser tooling and can write or overwrite a PDF at the chosen path. <br>
Mitigation: Review the output path before running PDF mode and confirm Chrome or agent-browser behavior in the local environment. <br>
Risk: Content extraction depends on twitter-thread.com indexing and page structure. <br>
Mitigation: If text output is empty or incomplete, confirm the thread is indexed and compare against the PDF output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ngmeyer/x-thread-reader) <br>
- [twitter-thread.com](https://twitter-thread.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Plain text or PDF file, with shell command guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text mode prints title, author, source links, and extracted thread content; PDF mode writes a PDF to the requested local path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
