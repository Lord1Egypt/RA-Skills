## Description: <br>
Download wallpapers in batch from wallhaven.cc via API v1 with flexible query parameters for search, category, purity, sorting, resolution, ratio, color, seed, and pagination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingyuan9527](https://clawhub.ai/user/jingyuan9527) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can use this skill when an agent needs to download one or more Wallhaven wallpapers into a target folder using explicit search filters or a Wallhaven search URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Wallhaven and saves wallpaper files locally. <br>
Mitigation: Install only for workflows that need Wallhaven downloads, use a dedicated output folder, and set a reasonable --count. <br>
Risk: A Wallhaven API key may be needed for gated results. <br>
Mitigation: Pass the key only through --apikey or WALLHAVEN_API_KEY; the script redacts the key in the generated manifest. <br>
Risk: Changing network targets could broaden where the agent sends requests. <br>
Mitigation: Keep the default HTTPS Wallhaven API endpoint and rely on the script's host allowlist and private-address checks. <br>


## Reference(s): <br>
- [Wallhaven API Search Endpoint](https://wallhaven.cc/api/v1/search) <br>
- [Wallhaven](https://wallhaven.cc) <br>
- [ClawHub Skill Page](https://clawhub.ai/jingyuan9527/wallhaven-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled script writes image files and a JSON manifest.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and curl. May use WALLHAVEN_API_KEY or --apikey for gated Wallhaven results.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
