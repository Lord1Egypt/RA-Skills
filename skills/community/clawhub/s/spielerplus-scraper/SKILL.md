---
name: spielerplus-scraper
description: "Scraper for SpielerPlus/TeamPlus team management platform. Extracts events, members, absences, finances, participation stats, and more."
tags: [spielerplus, teamplus, scraper, team-management, sports]
permissions: [network]
metadata:
  clawdbot:
    requires:
      env: [SPIELERPLUS_EMAIL, SPIELERPLUS_PASSWORD]
---

# SpielerPlus Scraper

Scrapes data from SpielerPlus for team management.

## Configuration

Requires environment variables:
```
SPIELERPLUS_EMAIL=your@email.com
SPIELERPLUS_PASSWORD=yourpassword
```

## Available Commands

| Command | Description |
|---------|-------------|
| `teams` | List all teams |
| `events` | Upcoming events |
| `event [n]` | Event details (index n) |
| `team` | Team members |
| `absences` | Vacation/sick leave |
| `finances` | Team cashbox |
| `participation` | Attendance stats |
| `profile` | Team profile |
| `roles` | Roles & permissions |
| `all` | Full report |

## Usage

```bash
# Install dependencies
npm install

# List teams
npm run teams

# Get events for specific team
npm run events "Männer"

# Full report
npm run all

# JSON output
npm run events -- --json
```

## Programmatic Usage

```javascript
const SpielerPlusScraper = require('./src/index.js');

const scraper = new SpielerPlusScraper({
  email: process.env.SPIELERPLUS_EMAIL,
  password: process.env.SPIELERPLUS_PASSWORD
});

await scraper.init();
const events = await scraper.getEvents();
await scraper.close();
```
