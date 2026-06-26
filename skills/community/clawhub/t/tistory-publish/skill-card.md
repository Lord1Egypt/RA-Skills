## Description: <br>
Tistory Publish automates Tistory blog publishing through OpenClaw Playwright CDP, including TinyMCE content insertion, OG cards, banner uploads, tags, category selection, and representative image setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garibong-labs](https://clawhub.ai/user/garibong-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content publishers use this skill to publish HTML-based Tistory posts via browser automation when a logged-in OpenClaw Chrome session is available. It supports optional banners, tags, category selection, representative images, and private or public publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publishing workflow can create public Tistory posts through a logged-in browser without a final confirmation step. <br>
Mitigation: Run test publishes with --private first and review the target blog, title, body, category, tags, and banner before removing --private. <br>
Risk: The mk-review template includes a hard-coded default blog when --blog is omitted. <br>
Mitigation: Always pass an explicit --blog value, and review or remove the template default before use. <br>
Risk: Kakao credentials may be used by the separate login helper for session recovery. <br>
Mitigation: Store any credential file outside shared locations with strict local permissions and provide it only through --cred-file or TISTORY_CRED_FILE when login recovery is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/garibong-labs/tistory-publish) <br>
- [Publisher profile](https://clawhub.ai/user/garibong-labs) <br>
- [README](artifact/README.md) <br>
- [Simple post runbook](artifact/templates/simple-post/RUNBOOK.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON status] <br>
**Output Format:** [Markdown guidance with inline bash commands; publishing scripts return JSON status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can publish to a real Tistory blog through an authenticated browser session; use --private for test runs before public publishing.] <br>

## Skill Version(s): <br>
5.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
