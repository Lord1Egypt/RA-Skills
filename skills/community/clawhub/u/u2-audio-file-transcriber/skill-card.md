## Description: <br>
Transcribes recorded audio files through the UniCloud ASR API from UniSound, with support for common file formats and finance, customer service, and general domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaiccee](https://clawhub.ai/user/aaiccee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run UniSound cloud transcription for prerecorded audio files and return plain-text or JSON transcripts. It is suited to customer service, finance, and other domain-specific recordings when UniSound credentials and endpoint configuration are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio files may contain sensitive content and are uploaded to a cloud ASR service. <br>
Mitigation: Review the UniSound service and privacy terms before use, and avoid private or regulated recordings unless the deployment has approved data handling controls. <br>
Risk: The default endpoint is a UniSound UAT URL over plain HTTP. <br>
Mitigation: Configure a trusted HTTPS UniSound endpoint before processing sensitive, customer-service, financial, or production audio. <br>
Risk: The skill requires UniSound credentials. <br>
Mitigation: Use scoped credentials supplied through environment variables or the host application's secret store, and do not share credentials in chat or commit them to files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaiccee/u2-audio-file-transcriber) <br>
- [UniSound ASR endpoint](http://af-asr.uat.hivoice.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcript, JSON transcription result, or Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save transcript output to a user-specified file and can include timestamps and confidence metadata in JSON mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
