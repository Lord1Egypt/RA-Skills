## Description: <br>
Searches Odessa rental sites for long-term two-room apartments up to 15,000 UAH per month using filters for district, pets, new buildings, living area, and furnishings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kapishdima](https://clawhub.ai/user/kapishdima) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users looking for rentals in Odessa use this skill to have an agent browse public listing sites, apply the stated apartment filters, and return candidate listings with links and key details. <br>

### Deployment Geography for Use: <br>
Odessa, Ukraine <br>

## Known Risks and Mitigations: <br>
Risk: Rental listings may be outdated, incomplete, inaccurate, or unavailable when the agent checks external sites. <br>
Mitigation: Verify listing details directly on the source site before contacting anyone or making rental decisions. <br>
Risk: The skill opens external real-estate websites during normal use. <br>
Mitigation: Invoke it explicitly with /rent and review the visited sources and returned links before acting on the results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kapishdima/rent) <br>
- [OLX Odessa rental listings](https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/?currency=UAH) <br>
- [DOM.RIA Odessa rental listings](https://dom.ria.com/uk/search/?category=1&realty_type=2&operation=3&state_id=12&price_cur=1&wo_dupl=1&sort=inspected_sort&firstIteraction=false&limit=20&market=3&excludeSold=1&type=map&without_entity_group=1&city_ids=12&ch=246_244#map_state=30.72139_46.48608_0.0_10.0) <br>
- [Flatfy Odessa rental listings](https://flatfy.ua/%D0%B0%D1%80%D0%B5%D0%BD%D0%B4%D0%B0-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80-%D0%BE%D0%B4%D0%B5%D1%81%D1%81%D0%B0) <br>
- [Rieltor Odessa rental listings](https://rieltor.ua/ru/odessa/flats-rent/#10.5/0/0) <br>
- [LUN Odessa rental listings](https://lun.ua/rent/odesa/flats/ru?srsltid=AfmBOopj60sLsMOT7sdNo_rAx-Cwj4dAttnTGCIg4ms30rFTkdykFNjx) <br>
- [Atlanta Odessa rental listings](https://www.atlanta.ua/odessa/filters/arenda/kvartiry) <br>
- [REM Odessa rental listings](https://rem.ua/arenda-kvartir-odessa) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown list of apartment listings with links, prices, districts, floors, and areas.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source-specific notes when no listings are found or a source cannot be searched.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
