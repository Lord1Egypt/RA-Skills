# Sports Events Query

Query sports events, fixtures, results, and team information via TheSportsDB free API. Covers soccer, basketball, tennis, baseball, and many more sports. Use when user asks about today's matches, upcoming games, league standings, team details, or sports results.

## Features

- **League Events**: Query events/results by league name
- **Team Search**: Get team details, stadium, capacity
- **Event Search**: Search for specific matches
- **Multi-sport Support**: Soccer, Basketball, Tennis, Baseball, NFL, NHL, etc.
- **No API Key Required**: Uses free TheSportsDB API

## Usage

```bash
# Query league events
python scripts/sports_api.py league "premier league"
python scripts/sports_api.py league "nba"
python scripts/sports_api.py league "la liga"

# Get team info
python scripts/sports_api.py team "Barcelona"
python scripts/sports_api.py team "Manchester United"

# Search events
python scripts/sports_api.py search "Real Madrid"

# List available leagues
python scripts/sports_api.py leagues
```

## Supported Leagues

- English Premier League
- La Liga
- Bundesliga
- Serie A
- Ligue 1
- NBA
- NFL
- And many more...

## API

This skill uses [TheSportsDB](https://www.thesportsdb.com/) free API - no API key required.

## Examples

### Premier League Results
```
$ python scripts/sports_api.py league "premier league"

📅 premier league 赛事
==================================================
  Liverpool 4 - 2 Bournemouth
  Aston Villa 0 - 0 Newcastle United
  Tottenham Hotspur 3 - 0 Burnley
  ...
```

### Team Information
```
$ python scripts/sports_api.py team "Barcelona"

🏟️ Barcelona
   简称: FCB
   主场: Spotify Camp Nou
   容量: 99354
   位置: Barcelona
   国家: Spain
```

## Installation

```bash
pip install requests
```
