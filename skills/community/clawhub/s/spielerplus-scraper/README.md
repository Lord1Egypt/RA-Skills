# SpielerPlus Scraper

A generic Node.js scraper for [SpielerPlus/TeamPlus](https://www.spielerplus.de) - the team management platform.

Extract team data including events, members, absences, finances, participation statistics, and more.

> ⚠️ **Note:** This tool is for personal use and educational purposes. Respect SpielerPlus' Terms of Service. Use responsibly.

## Features

- 📅 **Events** - Training, games, tournaments, events
- 👥 **Team Members** - List all team members
- 🏥 **Absences** - Vacation, sick leave, inactive status
- 💰 **Finances** - Team cashbox, transactions, contributions
- 📊 **Participation** - Attendance statistics per member
- 🏠 **Team Profile** - Team info, address, contact
- 👔 **Roles** - Team roles and permissions
- 🎁 **Benefits** - Active deals and offers

## Installation

```bash
npm install
```

## Configuration

Create a `.env` file in the project root:

```env
SPIELERPLUS_EMAIL=your@email.com
SPIELERPLUS_PASSWORD=yourpassword
```

Or export environment variables:

```bash
export SPIELERPLUS_EMAIL=your@email.com
export SPIELERPLUS_PASSWORD=yourpassword
```

## Usage

```bash
# Show available teams
npm run teams

# Scrape specific data
npm run events          # Upcoming events
npm run team            # Team members
npm run absences        # Absences
npm run finances        # Team finances
npm run participation   # Participation statistics
npm run profile         # Team profile
npm run roles           # Roles & permissions
npm run benefits        # Benefits/deals

# Event details with participants & carpool
npm run event 0        # First event
npm run event 1        # Second event

# Specify team (if you have multiple teams)
npm run events "Männer"
npm run finances "Herren"

# Full report for all teams
npm run all
```

## CLI Options

```bash
node src/cli.js <command> [team] [options]

Commands:
  teams         List all teams
  events        List upcoming events
  event [idx]   Event details (index, default: 0)
  team          Team members
  absences      Absences (vacation, sick, inactive)
  finances      Team finances & transactions
  participation Participation statistics
  profile       Team profile info
  roles         Roles & permissions
  benefits      Benefits & deals
  all           Full report for all teams

Options:
  -h, --help    Show help
  -j, --json    Output as JSON
  -t, --team    Team name to scrape
```

## Programmatic Usage

```javascript
const SpielerPlusScraper = require('./src/index.js');

const scraper = new SpielerPlusScraper({
  email: 'your@email.com',
  password: 'yourpassword'
});

async function main() {
  await scraper.init();
  
  // Get teams
  const teams = await scraper.getTeams();
  console.log('Teams:', teams);
  
  // Select specific team
  await scraper.selectTeam('My Team');
  
  // Get data
  const events = await scraper.getEvents();
  const members = await scraper.getTeamMembers();
  const finances = await scraper.getFinances();
  
  console.log({ events, members, finances });
  
  await scraper.close();
}

main();
```

## Data Output Example

```json
{
  "team": "SSG Humboldt Männer",
  "events": [
    { "date": "Di.31.03", "time": "19:15", "type": "Training", "meeting": "19:15" }
  ],
  "finances": {
    "balance": "EUR 301.63",
    "transactions": [
      { "type": "Beitrag", "name": "Max Mustermann", "amount": "EUR 10.00" }
    ]
  },
  "participation": {
    "summary": { "total": 24, "trainings": 13, "spiele": 11 },
    "players": [
      { "name": "Thomas Heine", "count": 18, "percentage": 75 }
    ]
  }
}
```

## Requirements

- Node.js >= 18.0.0
- Chrome/Chromium (installed automatically by Playwright)

## Troubleshooting

**Login fails?**
- Check your credentials in `.env`
- SpielerPlus might require email verification for new logins

**Headless browser issues?**
- Ensure Chromium is installed: `npx playwright install chromium`

**Premium features not accessible?**
- Some features require SpielerPlus Premium subscription

## License

MIT

## Disclaimer

This project is not affiliated with SpielerPlus/TeamPlus. Use at your own risk and respect the platform's Terms of Service.

---

## Release Process

Releases are automated via GitLab CI/CD:

1. Update version: `npm version patch`
2. Push with tags: `git push --follow-tags`
3. Pipeline publishes to:
   - **npm**: https://www.npmjs.com/package/spielerplus-scraper
   - **ClawHub**: https://clawhub.ai

### Required Setup

1. **npm Token** (GitLab CI/CD Variable: `NPM_TOKEN`)
   - https://www.npmjs.com → Profile → Access Tokens → Create Automation Token

2. **ClawHub** (optional, automatic)
   - Uses `clawdhub` in CI
