# Disclosures

Insider trades, institutional holdings, activist stakes and Congress trades.

## Insider trades

`GET /disclosures/insiders` (scope `research`, cursor-paged)

Every Form 4 transaction, newest filing first: officers, directors and 10% owners buying, selling, exercising and receiving stock. Two years back, new ones within a minute of filing.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Tickers, comma separated, e.g. `AAPL,NVDA`. Default every company. |
| `type` | query | string | Comma separated: `buy`, `sell`, `grant`, `exercise`, `tax`, `gift`, `conversion`, `disposition`, `expiration`, `inheritance`, `other`. |
| `min_value` | query | number | Smallest `value_usd`, e.g. `1000000`. |
| `from` | query | string | Filed on or after, `YYYY-MM-DD` or an RFC 3339 time. |
| `to` | query | string | Filed on or before. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `filed_at` | string | When the Form 4 was accepted, UTC. |
| `transaction_date` | string | Trade date, `YYYY-MM-DD`. |
| `symbol, company, cik` | mixed | The company and its SEC CIK. |
| `insider, insider_cik` | mixed | Who traded and their SEC CIK. |
| `relationship` | string | Their ties to the company, e.g. `Chief Financial Officer`, `Director, 10% owner`. |
| `form` | string | `4` or `4/A`. |
| `security` | string | What was traded, e.g. `Common Stock`, `Stock Option (Right to Buy)`. |
| `derivative` | boolean | An option, unit or other derivative. |
| `transaction_code` | string | The SEC code, e.g. `P`, `S`, `A`, `M`, `F`. |
| `type` | string | The code in a word: `buy`, `sell`, `grant`, `exercise`, `tax`, `gift`, … |
| `direction` | string | `acquired` or `disposed`. |
| `shares, price` | number | Shares (or derivative units) and price per share. |
| `value_usd` | number | Shares times price. |
| `shares_owned_after` | number | Holding after the trade. |
| `ownership` | string | `direct` or `indirect`. |
| `rule_10b5_1` | boolean | The filing's Rule 10b5-1 plan box; null on forms without it (before April 2023). |
| `accession` | string | The Form 4 filing. |

Request: `GET https://tradytics.com/api/public/v1/disclosures/insiders?symbol=NVDA&apiKey=YOUR_API_KEY`

## Institutional holders

`GET /disclosures/institutions` (scope `research`, cursor-paged)

Every institution that reported a stock on its 13F for a quarter, biggest position first, with what it bought or sold since the quarter before. The last 8 quarters.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker symbol, e.g. `AAPL`. Required. |
| `quarter` | query | string | Quarter end, `YYYY-MM-DD` or `2026Q2`. Default the latest quarter past its 45-day filing deadline. |
| `put_call` | query | string | `call` or `put`. Returns option positions instead of shares. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `quarter` | string | Quarter end, `YYYY-MM-DD`. |
| `manager` | string | The institution. |
| `cik` | integer | Its SEC CIK. |
| `symbol` | string | Ticker of the security, null when unknown. |
| `issuer, cusip` | string | Security as filed and its CUSIP. |
| `put_call` | string | `call` or `put` for an option position, else null. |
| `shares` | number | Shares (or principal) held at quarter end. |
| `prior_shares` | number | Shares the quarter before, null if new. |
| `shares_change` | number | Shares bought (sold if negative) over the quarter. |
| `change_pct` | number | Change in shares, percent. |
| `value_usd` | number | Market value at quarter end in dollars; a 13F filed in thousands is multiplied by 1,000. |
| `weight` | number | Share of the manager's reported book, decimal. |
| `new, closed` | boolean | Opened this quarter; sold out this quarter (`shares` 0). `new` and the changes are null when the quarter before isn't on file. |
| `filed_at` | string | When the 13F was accepted, UTC. |
| `accession` | string | The 13F filing. |

Request: `GET https://tradytics.com/api/public/v1/disclosures/institutions?symbol=AAPL&apiKey=YOUR_API_KEY`

## Institution holdings

`GET /disclosures/institutions/{cik}` (scope `research`, cursor-paged)

One institution's whole 13F book for a quarter, biggest position first, with the changes from the quarter before.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `cik` | path | integer | The manager's SEC CIK, e.g. `1067983` (Berkshire Hathaway). Required. |
| `quarter` | query | string | Quarter end, `YYYY-MM-DD` or `2026Q2`. Default its latest. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `quarter` | string | Quarter end, `YYYY-MM-DD`. |
| `manager` | string | The institution. |
| `cik` | integer | Its SEC CIK. |
| `symbol` | string | Ticker of the security, null when unknown. |
| `issuer, cusip` | string | Security as filed and its CUSIP. |
| `put_call` | string | `call` or `put` for an option position, else null. |
| `shares` | number | Shares (or principal) held at quarter end. |
| `prior_shares` | number | Shares the quarter before, null if new. |
| `shares_change` | number | Shares bought (sold if negative) over the quarter. |
| `change_pct` | number | Change in shares, percent. |
| `value_usd` | number | Market value at quarter end in dollars; a 13F filed in thousands is multiplied by 1,000. |
| `weight` | number | Share of the manager's reported book, decimal. |
| `new, closed` | boolean | Opened this quarter; sold out this quarter (`shares` 0). `new` and the changes are null when the quarter before isn't on file. |
| `filed_at` | string | When the 13F was accepted, UTC. |
| `accession` | string | The 13F filing. |

Request: `GET https://tradytics.com/api/public/v1/disclosures/institutions/1067983?apiKey=YOUR_API_KEY`

## Activist stakes

`GET /disclosures/activists` (scope `research`, cursor-paged)

Schedule 13D (activist) and 13G (passive) filings of holders of 5% or more, newest first. Two years back.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Tickers, comma separated, e.g. `AAPL,NVDA`. Default every company. |
| `form` | query | string | `13d` or `13g`. |
| `from` | query | string | Filed on or after, `YYYY-MM-DD` or an RFC 3339 time. |
| `to` | query | string | Filed on or before. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `filed_at` | string | When it was accepted, UTC. |
| `symbol, company, cik` | mixed | The company and its SEC CIK. |
| `filer, filer_cik` | mixed | Who filed it. |
| `form` | string | `13D` or `13G`. |
| `amendment` | boolean | An amendment to an earlier filing. |
| `owned_pct` | number | Percent of the class owned. |
| `shares` | number | Shares owned. |
| `event_date` | string | Date of the event that required it, `YYYY-MM-DD`. |
| `cusip` | string | CUSIP of the class. |
| `accession` | string | The filing. |

Request: `GET https://tradytics.com/api/public/v1/disclosures/activists?form=13d&apiKey=YOUR_API_KEY`

## Congress trades

`GET /disclosures/congress` (scope `research`, cursor-paged)

Stock trades members of the House and Senate disclosed, newest disclosure first. Three years back.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Tickers, comma separated, e.g. `AAPL,NVDA`. Default every company. |
| `chamber` | query | string | `house` or `senate`. |
| `type` | query | string | Comma separated: `buy`, `sell`, `exchange`, `other`. |
| `from` | query | string | Disclosed on or after, `YYYY-MM-DD`. |
| `to` | query | string | Disclosed on or before, `YYYY-MM-DD`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `chamber` | string | `house` or `senate`. |
| `member, member_id` | string | The member and their Bioguide id, e.g. `P000197`. |
| `party` | string | `democrat`, `republican` or `independent`. |
| `state, district` | string | e.g. `CA` and `11`; no district for senators. |
| `symbol, asset, asset_type` | string | What was traded, as reported. |
| `owner` | string | `self`, `spouse`, `joint` or `child`. |
| `type` | string | `buy`, `sell`, `exchange` or `other`. |
| `amount` | string | The range reported, e.g. `$1,001 - $15,000`. |
| `amount_min_usd, amount_max_usd` | number | Its bounds; an exact amount is both, an `Over` range has no max. |
| `transaction_date, disclosure_date` | string | `YYYY-MM-DD`. |
| `link` | string | The report. |

Request: `GET https://tradytics.com/api/public/v1/disclosures/congress?symbol=NVDA&apiKey=YOUR_API_KEY`
