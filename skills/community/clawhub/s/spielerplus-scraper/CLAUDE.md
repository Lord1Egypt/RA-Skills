# SpielerPlus Scraper - Claude Code Guide

## Quick Start

```bash
npm install
cp .env.example .env
# Edit .env with your credentials
npm run teams
```

## Common Tasks

```bash
# Get upcoming events
npm run events

# Get team finances
npm run finances

# Get participation statistics
npm run participation

# Full report for all teams
npm run all

# Specific team
npm run events "Männer"
npm run finances "Frauen"
```

## Development

```bash
# Test changes
node src/cli.js teams

# Validate syntax
node --check src/index.js
node --check src/cli.js
```

## Project Structure

```
src/
├── index.js    # Core scraper class
└── cli.js      # CLI interface
```

## Adding New Features

1. Add method to `src/index.js`
2. Add CLI command to `src/cli.js`
3. Update README.md
4. Test manually
