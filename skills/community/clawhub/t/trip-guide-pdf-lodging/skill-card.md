## Description: <br>
Research, plan, revise, and deliver lodging-anchored travel guides as HTML/PDF with verified route data, hotel selection, fallback hotel swaps, curated screenshots, and formal copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allensu0314](https://clawhub.ai/user/allensu0314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel planners and agents use this skill to build or revise lodging-anchored itineraries, especially when hotel choice, availability, price, or location changes affect route feasibility. It guides research, source selection, HTML drafting, PDF export, and lodging-swap revisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route times, distances, opening hours, and lodging details can become inaccurate or stale. <br>
Mitigation: Verify schedule-critical numbers with maps, official scenic pages, or structured listings before drafting and re-check them after any lodging change. <br>
Risk: Review sites and social posts may provide subjective or unreliable signals for hotel, dining, or local-fit decisions. <br>
Mitigation: Separate hard data from soft signals, use review content only for qualitative tradeoffs, and avoid relying on social posts for schedule-critical numbers. <br>
Risk: Screenshots and generated local files can include irrelevant, cluttered, or misleading material. <br>
Mitigation: Keep screenshots sparse and decision-relevant, reject blank or cluttered captures, and review HTML output before PDF export. <br>
Risk: Using the optional cn-review-sites-cdp helper may require permissions beyond this instruction-only skill. <br>
Mitigation: Review that helper's permissions separately before allowing the agent to invoke it. <br>


## Reference(s): <br>
- [Source Selection for Lodging Guides](references/source-selection.md) <br>
- [QA Checklist for Lodging Guides](references/qa-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, guidance] <br>
**Output Format:** [HTML/PDF travel guides, concise itinerary prose, selected screenshots, and supporting notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local HTML/PDF files and selected screenshots; route, lodging, and schedule-critical data should be verified before final export.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
