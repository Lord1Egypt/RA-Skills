# Browser Workflows

Use browser automation for:
- Search
- Web scraping
- Login flows
- Form submission
- File upload/download
- Reading page content

## Preferred approach
- Use selectors over screen coordinates
- Wait for page state instead of sleeping blindly
- Verify visible text after major actions
- Reuse authenticated sessions when allowed

## Common failure modes
- Modal dialogs blocking clicks
- Dynamic content not yet loaded
- Anti-bot or login challenges
- Stale selectors after page redesign
