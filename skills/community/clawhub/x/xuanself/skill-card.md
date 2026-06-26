## Description: <br>
Xuanself is a Russia medical-device market-research workflow that combines multilingual search, patient data, government monitoring, and professional Word report export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxuan1992asia-svg](https://clawhub.ai/user/wangxuan1992asia-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business teams use Xuanself to generate Russia-focused medical-device market research reports with current industry news, patient statistics, medical progress, government policy, tenders, pricing, and competitive analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live web and API searches can return outdated, incomplete, or source-dependent market information. <br>
Mitigation: Review generated reports for source URLs, collection dates, and consistency before using or sharing them. <br>
Risk: The skill uses locally stored API keys for services such as SerpAPI and optional TGStat. <br>
Mitigation: Use limited-scope keys where possible and do not commit or share data_sources.json after filling in credentials. <br>
Risk: The skill can create local DOCX report files that may contain sensitive market or business analysis. <br>
Mitigation: Review report contents and output paths before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxuan1992asia-svg/xuanself) <br>
- [Clawdis homepage](https://github.com/workbuddy/xuanself) <br>
- [SerpAPI](https://serpapi.com) <br>
- [TGStat](https://tgstat.ru) <br>
- [IDF Diabetes Atlas](https://diabetesatlas.org) <br>
- [Russia data in IDF Diabetes Atlas](https://diabetesatlas.org/data-by-location/country/russian-federation/) <br>
- [Russian Ministry of Health](https://minzdrav.gov.ru) <br>
- [Russian diabetes federal project page](https://minzdrav.gov.ru/poleznye-resursy/natsionalnye-proekty-rossii-prodolzhitelnaya-i-aktivnaya-zhizn-novye-tehnologii-sberezheniya-zdorovya/struktura-i-klyuchevye-meropriyatiya-federalnogo-proekta-borba-s-saharnym-diabetom) <br>
- [National Medical Research Center for Endocrinology](https://www.endocrincentr.ru) <br>
- [Russian Diabetes Association](https://www.diabetes-ru.org) <br>
- [Kommersant](https://www.kommersant.ru) <br>
- [Russia unified procurement system](https://zakupki.gov.ru) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese market-research report text or Markdown with optional DOCX file export.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided API keys for best search quality and may create local DOCX report files.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, MANIFEST.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
