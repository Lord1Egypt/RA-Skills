# Contributing to SpielerPlus Scraper

Thank you for your interest!

## Development Setup

1. Clone the repository
2. Install dependencies: `npm install`
3. Copy `.env.example` to `.env` and fill in your credentials
4. Test with `npm run teams`

## Code Style

- Use ES6+ features
- Add JSDoc comments for public methods
- Keep methods focused and testable

## Adding New Features

1. Add the scraping logic to `src/index.js` as a new method
2. Add CLI command to `src/cli.js`
3. Update README.md with documentation
4. Test thoroughly before submitting PR

## Testing

Test manually by running different commands:
```bash
npm run teams
npm run events
npm run finances
# etc.
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with your own SpielerPlus account
5. Submit a PR with description of changes
