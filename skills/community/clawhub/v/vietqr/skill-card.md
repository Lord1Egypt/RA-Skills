## Description: <br>
Generate VietQR payment image URLs for Vietnamese bank transfers from bank/account details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phucisstupid](https://clawhub.ai/user/phucisstupid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate VietQR payment image URLs or Markdown QR previews for Vietnamese bank transfers, with optional amount, note, account-name, and template fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Opening or previewing generated VietQR image URLs can disclose payment details embedded in the URL to img.vietqr.io. <br>
Mitigation: Avoid unrelated private information in transfer notes, and return raw URLs when the user needs control over whether the external image is fetched. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phucisstupid/vietqr) <br>
- [Publisher profile](https://clawhub.ai/user/phucisstupid) <br>
- [VietQR image service endpoint](https://img.vietqr.io/image) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text URL or Markdown image syntax] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated URLs may include bank, account, amount, transfer note, account-name, and template values.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
