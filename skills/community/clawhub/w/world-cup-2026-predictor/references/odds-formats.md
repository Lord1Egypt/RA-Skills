# Odds Formats

Always identify the format before reading the market. The same number can mean different things across books.

## Ambiguity Rejection

- Every quote must declare its odds format. Never infer the format from the number, bookmaker region, sign, or surrounding prose.
- Reject ambiguous inputs such as bare `0.85`, `-0.85`, or `1.20`; each could mean a different return under decimal, Hong Kong, Malay, Indo, or handicap notation.
- Keep the Asian handicap line separate from its water price. For example, `home -0.75 @ 0.92 HK` contains a signed handicap and a Hong Kong price; neither may replace the other.
- Reject decimal odds at or below `1.0`, zero American odds, malformed fractional odds, and values outside the declared format's valid domain.
- If a screenshot or source does not label the format, report it as unavailable until corroborated. Do not guess and do not feed it into consensus.

## Main Markets

| Market | What it answers | Use |
| --- | --- | --- |
| European decimal 1X2 | Home/draw/away in 90 minutes | Convert to implied probability; compare with moneyline. |
| US moneyline | Team/draw price in 90 minutes | Convert to implied probability; useful on US sites. |
| Qualification/to-lift | Who advances or wins tie/tournament | Separate from 90-minute result; reveals extra-time/penalty risk. |
| Asian handicap | Margin and protection line | Do not treat as winner market; use to judge cover and underdog protection. |
| Totals | Total goals line | Score-shape input. |
| BTTS | Whether both teams score | Score-shape input, especially 1-1 vs 2-0. |

## Conversion Quick Reference

Use approximate implied probability before comparing prices:

| Format | Example | Conversion |
| --- | --- | --- |
| Decimal/European | 1.80 | `1 / 1.80 = 55.6%` |
| Fractional | 4/5 | decimal `1.80`, probability `55.6%` |
| American negative | -150 | `150 / (150 + 100) = 60.0%` |
| American positive | +240 | `100 / (240 + 100) = 29.4%` |
| Hong Kong water | 0.92 | decimal `1.92`, probability `1 / 1.92 = 52.1%` |
| Malay positive | 0.85 | decimal `1.85`, probability `54.1%` |
| Malay negative | -0.85 | probability `0.85 / 1.85 = 45.9%` |
| Indo positive | 1.20 | decimal `2.20`, probability `45.5%` |
| Indo negative | -1.20 | probability `1.20 / 2.20 = 54.5%` |

These raw probabilities include bookmaker margin. De-vig each complete bookmaker market before comparing it with another book or fitting the score model.

## Asian Handicap Reading

For favorites, more negative lines are stronger:

- `-1.0 -> -1.25 -> -1.5` means the favorite cover expectation is strengthening.
- `-1.5 -> -1.25 -> -1.0` means the market is protecting the underdog or doubting the blowout.
- If the line strengthens but favorite water rises sharply, cover is not fully confirmed.
- If the favorite ML strengthens while Asian handicap weakens, split the call: favorite can win, but the handicap may fail.

For underdogs, more positive protection or falling underdog water is meaningful:

- `+1.5` with falling water suggests the book expects the underdog to stay within the number.
- In knockout matches, underdog protection plus under 2.5 often points to `1-0`, `1-1`, or `2-0`, not a runaway favorite score.
