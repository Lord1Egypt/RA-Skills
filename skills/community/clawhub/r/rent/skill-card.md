## Description:

Realtor searches public real-estate sites for long-term two-room apartment rentals in Odessa under 15,000 UAH with filters for district, area, furnishings, pets, and new builds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kapishdima](https://clawhub.ai/user/kapishdima)

### License/Terms of Use:


## Use Case:

External users looking for rentals in Odessa use this skill to have an agent browse listed real-estate sources and return matching long-term two-room apartment listings with prices, districts, floors, area, links, and source fallback notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may browse several public real-estate sites when rental trigger phrases are used.

Mitigation: Review or narrow the source list and criteria before installation if users need explicit confirmation before browsing.

Risk: Results are tied to fixed Odessa two-room rental criteria and may not match other cities, budgets, or languages.

Mitigation: Adjust the filters, sources, and trigger phrases before using it for a different rental search.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kapishdima/skills/rent)
- [OLX apartment rentals](https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/?currency=UAH)
- [DOM.RIA Odessa rentals](https://dom.ria.com/uk/search/?category=1&realty_type=2&operation=3&state_id=12&price_cur=1&wo_dupl=1&sort=inspected_sort&firstIteraction=false&limit=20&market=3&excludeSold=1&type=map&without_entity_group=1&city_ids=12&ch=246_244#map_state=30.72139_46.48608_0.0_10.0)
- [flatfy Odessa rentals](https://flatfy.ua/%D0%B0%D1%80%D0%B5%D0%BD%D0%B4%D0%B0-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80-%D0%BE%D0%B4%D0%B5%D1%81%D1%81%D0%B0)
- [rieltor Odessa rentals](https://rieltor.ua/ru/odessa/flats-rent/#10.5/0/0)
- [LUN Odessa rentals](https://lun.ua/rent/odesa/flats/ru?srsltid=AfmBOopj60sLsMOT7sdNo_rAx-Cwj4dAttnTGCIg4ms30rFTkdykFNjx)
- [Atlanta Odessa rentals](https://www.atlanta.ua/odessa/filters/arenda/kvartiry)
- [REM Odessa rentals](https://rem.ua/arenda-kvartir-odessa)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with rental listing links and fallback notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include links, prices, districts, floors, and apartment area; dependent on public listing availability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
