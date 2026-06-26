## Description: <br>
Query and manage leads from the SMB Sales Boost B2B lead database, including lead search, preview, export, filter presets, email schedules, billing-related actions, and AI-assisted category and keyword workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomsonx232](https://clawhub.ai/user/tomsonx232) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and go-to-market teams use this skill to find, preview, export, and schedule delivery of SMB lead lists for cold outreach. It supports credit-aware queries, export controls, filter and keyword management, AI-assisted targeting, and subscription or credit management for SMB Sales Boost accounts. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an SMB Sales Boost API key and can access account, lead, export, schedule, and billing endpoints. <br>
Mitigation: Install only when the user trusts SMB Sales Boost with the API key and account authority; keep the key in SMB_SALES_BOOST_API_KEY and avoid sharing it in public channels. <br>
Risk: Lead exports may contain business phone numbers, email addresses, and other contact data. <br>
Mitigation: Use preview and credit caps before exporting, save exports only in secure locations, and avoid sharing exported files in public or unsecured channels. <br>
Risk: Purchase, credit, plan-change, and auto top-up endpoints can create real billing activity. <br>
Mitigation: Require explicit user confirmation before purchases, plan changes, cancellations, or auto top-up changes, and use maxCredits or maxResults to limit spend. <br>
Risk: Email schedule workflows can send lead files to configured recipients. <br>
Mitigation: Verify recipients and distribution settings before creating, updating, or manually triggering schedules. <br>


## Reference(s): <br>
- [SMB Sales Boost API](https://smbsalesboost.com/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/tomsonx232/smb-sales-boost-leads) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses, shell command examples, and exported CSV, JSON, or XLSX files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SMB_SALES_BOOST_API_KEY and an active SMB Sales Boost subscription for authenticated API actions.] <br>

## Skill Version(s): <br>
1.9.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
