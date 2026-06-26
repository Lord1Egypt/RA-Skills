## Description: <br>
Assists with PubMed-based clinical medical literature retrieval and analysis using confirmed search terms, JCR quartile filtering, impact-factor sorting, and comprehensive relevance ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flash9107](https://clawhub.ai/user/flash9107) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, clinicians, researchers, and review authors use this skill to formulate PubMed search strategies, screen clinical medicine literature, and produce ranked literature reports supported by JCR journal metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated literature rankings may be mistaken for clinical advice. <br>
Mitigation: Treat outputs as literature-triage support and have qualified users verify clinical relevance before applying findings. <br>
Risk: The skill depends on a user-provided JCR spreadsheet and a disclosed local override for International Journal of Surgery. <br>
Mitigation: Verify the spreadsheet source and confirm any local ranking overrides before relying on ranking or filtering results. <br>
Risk: PubMed search quality depends on the selected terms and filters. <br>
Mitigation: Review and confirm the proposed search strategy before executing searches or using generated literature reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flash9107/pubmed-literature-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown report with search terms, ranked tables, summaries, and distribution analyses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PubMed query strings, Top 10 literature recommendations, JCR quartile and impact-factor fields, research-type distributions, journal distributions, and publication-year trends.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
