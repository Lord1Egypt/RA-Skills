## Description: <br>
Reverse image search that helps an agent find an image source, visually similar images, and authenticity context using Yandex by default with optional Google Lens and Bing fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsonsleo](https://clawhub.ai/user/johnsonsleo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their users use this skill when an image URL or local image file needs source attribution, similar-image discovery, or context checks for authenticity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image URLs or uploaded local images are sent to third-party reverse image search services. <br>
Mitigation: Avoid private or sensitive images unless sharing them with Yandex, Google Lens, or Bing is acceptable. <br>
Risk: Yandex failure diagnostics can write debug HTML files under /tmp. <br>
Mitigation: Delete /tmp/openclaw-yandex-debug-*.html files after failed Yandex runs, especially in shared environments. <br>
Risk: Upstream scraper changes, anti-bot responses, or unpinned dependencies can affect reliability. <br>
Mitigation: Treat non-zero exits and diagnostic error objects as retry or fallback signals, and pin dependencies in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnsonsleo/yandex-image-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON results with URLs, titles, thumbnails, similarity when available, status fields, and diagnostic objects on Yandex failures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The engine argument selects yandex, google, bing, or all; the limit argument controls the maximum results returned per engine.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
