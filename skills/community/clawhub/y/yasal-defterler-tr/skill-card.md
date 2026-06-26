## Description: <br>
Türkiye'de şirketlerin tutması gereken yasal defterler, e-defter uygulaması, defter tasdik tarihleri, belge arşivleme kuralları, personel özlük dosyaları ve çalışan dokümanı gereklilikleri hakkında rehberlik sağlar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayhanagirgol](https://clawhub.ai/user/ayhanagirgol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, founders, company managers, accounting teams, and advisors use this skill to answer Turkey-specific questions about required company books, e-defter, notarization timing, archiving practices, personnel files, and mandatory worker documents. <br>

### Deployment Geography for Use: <br>
Turkey <br>

## Known Risks and Mitigations: <br>
Risk: Evidence security guidance says installation should be limited to cases where the assistant is expected to control Ziniao Browser through a local ZClaw bridge. <br>
Mitigation: Install only in environments where that local browser-control behavior is intended and approved. <br>
Risk: Evidence security guidance says ZCLAW_API_KEY should be treated like a credential. <br>
Mitigation: Store the key securely, avoid sharing it in prompts or logs, and rotate it if exposure is suspected. <br>
Risk: Evidence security guidance says the skill may read page content, click or type in browser stores, take screenshots, run in-page JavaScript, and write files to Downloads when asked. <br>
Mitigation: Review requested browser actions before execution and avoid using the skill on sensitive pages unless the user explicitly authorizes that access. <br>


## Reference(s): <br>
- [Yasal Defterler Tr on ClawHub](https://clawhub.ai/ayhanagirgol/yasal-defterler-tr) <br>
- [8 Yasal Defter ve Hangi Şirketler İçin Zorunlu](references/defter_listesi.md) <br>
- [Defter Tasdik Tarihleri, E-Defter ve Belge Arşivleme](references/tasdik_ve_arsiv.md) <br>
- [Çalışan Türleri ve Zorunlu Dokümanlar](references/calisanlar_dokumanlari.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should stay within the artifact's Turkey-specific legal books, archiving, and employee documentation reference material.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
