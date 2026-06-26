## Description: <br>
TikTok US women's fashion hotspot monitor that crawls video metadata via Apify or Playwright, analyzes trends with heat and coverage scoring, and generates static HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tandongtaotao](https://clawhub.ai/user/tandongtaotao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to monitor TikTok keyword, hashtag, creator, and music sources for trend signals, then generate offline analysis and static HTML reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TikTok crawling may run through Apify or a logged-in Playwright browser. <br>
Mitigation: Install only if this crawling posture is acceptable; prefer Apify mode or a dedicated low-privilege TikTok account. <br>
Risk: Reusable TikTok login session data can be stored at data/tiktok_session.json. <br>
Mitigation: Keep the session file out of version control and delete it when it is no longer needed. <br>
Risk: The package includes video download capability that may exceed the core analytics workflow. <br>
Mitigation: Review scripts/download_tiktok_videos.py before allowing agents to run arbitrary scripts or download videos from this package. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tandongtaotao/tiktok-hotspot-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/tandongtaotao) <br>
- [Repository declared by artifact metadata](https://github.com/TanDongTaotao/tiktok-hotspot-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON files, HTML reports] <br>
**Output Format:** [Markdown guidance with shell commands, JSON/JSONL data files, and self-contained HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Apify mode requires APIFY_TOKEN; Playwright fallback uses a locally saved TikTok session; configured guardrails limit source count, per-source limits, and planned crawl runs.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence release, artifact metadata, and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
