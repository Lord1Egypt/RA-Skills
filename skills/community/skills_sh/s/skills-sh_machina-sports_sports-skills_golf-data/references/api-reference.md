# Golf Data — API Reference

## Commands

### get_leaderboard
Get the current tournament leaderboard with all golfer scores.
- `tour` (str, required): "pga", "lpga", or "eur"

Returns the current/most recent tournament with:
- Tournament name, venue, status, current round, and `field_size`
- `leaderboard[]` sorted by position with golfer `id`, `name`, `country`, `score`, and `rounds[]`

Each golfer in `leaderboard[]` has:
- `position`: Leaderboard rank
- `name`: Golfer name
- `country`: Nationality
- `score`: Total score relative to par (e.g., "-17", "E", "+2")
- `rounds[]`: Array with `round`, `strokes`, and `score` (score-to-par) per round

### get_schedule
Get full season tournament schedule.
- `tour` (str, required): "pga", "lpga", or "eur"
- `year` (int, optional): Season year. Defaults to current.

Returns `tournaments[]` with tournament name, ID, start/end dates.

### get_player_info
Get individual golfer profile.
- `player_id` (str, required): ESPN athlete ID
- `tour` (str, optional): "pga", "lpga", or "eur". Defaults to "pga".

Returns golfer details: name, age, nationality, birthplace, height/weight, turned pro year, college, headshot URL, and ESPN profile link.

**Note:** LPGA player profiles are not available through ESPN — the command automatically tries PGA and EUR as fallback.

### get_player_overview
Get detailed golfer overview with season stats, rankings, and recent results.
- `player_id` (str, required): ESPN athlete ID
- `tour` (str, optional): "pga", "lpga", or "eur". Defaults to "pga".

Returns season statistics (scoring average, earnings, wins, top-10s), world/tour rankings, and recent tournament results.

### get_scorecard
Get hole-by-hole scorecard for a golfer in the current/most recent tournament.
- `tour` (str, required): "pga", "lpga", or "eur"
- `player_id` (str, required): ESPN athlete ID

Returns `rounds[]` with hole-by-hole scores (strokes, score relative to par) for each completed round.

### get_news
Get golf news articles.
- `tour` (str, required): "pga", "lpga", or "eur"

Returns `articles[]` with headline, description, published date, and link.

## Reading Golf Scores

Scores are relative to par:
- **Negative score** = under par (good). "-17" = 17 strokes under par.
- **"E"** = even par.
- **Positive score** = over par. "+2" = 2 strokes over par.
- **Strokes** = actual stroke count for that round (e.g., par 72 course → 63 strokes = -9).

## Common Player IDs

| Player | ID | Player | ID |
|--------|-----|--------|-----|
| Scottie Scheffler | 9478 | Nelly Korda | 9012 |
| Rory McIlroy | 3470 | Jin Young Ko | 9758 |
| Jon Rahm | 9780 | Lydia Ko | 7956 |
| Collin Morikawa | 10592 | Lilia Vu | 9401 |
| Xander Schauffele | 10404 | Nasa Hataoka | 10484 |
| Viktor Hovland | 10503 | Atthaya Thitikul | 10982 |
| Hideki Matsuyama | 5765 | Celine Boutier | 9133 |
| Ludvig Aberg | 4686088 | Lexi Thompson | 6843 |

Player IDs also appear in `get_leaderboard` results (`id` field on each golfer). ESPN golf URLs also contain the ID: `espn.com/golf/player/_/id/9478/scottie-scheffler` → ID is `9478`.

## Major Championships

| Tournament | Months | Course(s) |
|-----------|--------|-----------|
| The Masters | April | Augusta National |
| PGA Championship | May | Varies |
| U.S. Open | June | Varies |
| The Open Championship | July | Links courses (UK) |

See also: `references/majors.md` and `references/player-ids.md` for extended references.
