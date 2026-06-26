# Singapore Pools Toto Result Sources

## Official page

- Main page: `https://www.singaporepools.com.sg/en/product/pages/toto_results.aspx`

The page JavaScript populates latest results by fetching generated HTML files from:

- Base path: `https://www.singaporepools.com.sg/DataFileArchive/Lottery/Output/`

## Draw type file mapping (EN)

- Normal: `toto_result_top_draws_en.html`
- Cascade: `toto_result_cascade_top_draws_en.html`
- Hongbao: `toto_result_hongbao_top_draws_en.html`
- Special: `toto_result_special_top_draws_en.html`

## Parsed fields and selectors

The parser extracts from the first `<li>` block in each file:

- Draw date: `class='drawDate'`
- Draw number: `class='drawNumber'`
- Winning numbers: `class='win1'` ... `class='win6'`
- Additional number: `class='additional'`
- Group 1 prize: `class='jackpotPrize'`
- Winning ticket link token: `encryptedQueryString='sppl=...'`

Single draw URL template:

- `https://www.singaporepools.com.sg/en/product/sr/Pages/toto_results.aspx?` + encrypted query string

## Maintenance note

If Singapore Pools updates HTML classes or output filenames, update:

- `DRAW_TYPE_TO_FILE` mapping
- regex selectors in `parse_latest_draw`
