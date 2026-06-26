## Description: <br>
Compile Typst and LaTeX documents to PDF through the TypeTex API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gregm711](https://clawhub.ai/user/gregm711) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to submit Typst or LaTeX source, auxiliary files, fonts, images, and bibliographies to a remote compiler and receive a PDF result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents, images, fonts, bibliographies, and other auxiliary files are uploaded to the remote TypeTex compilation API. <br>
Mitigation: Use the skill for public or low-sensitivity content unless the user trusts the service and has approval to upload the material. <br>
Risk: Compilation can fail because of syntax errors, missing auxiliary files, unavailable packages, or timeout on complex documents. <br>
Mitigation: Check the success flag before decoding PDF output and use returned error text or LaTeX logs to correct the source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gregm711/typetex) <br>
- [TypeTex public compile API](https://studio-intrinsic--typetex-compile-app.modal.run) <br>
- [TypeTex](https://typetex.app) <br>
- [Typst documentation](https://typst.app/docs/) <br>
- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads, Python examples, curl commands, and PDF file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns base64-encoded PDF content on successful compilation and error text or LaTeX logs on failure.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
