# Slack Channel IDs

## Operational Intelligence Channels

| Channel | ID | Purpose |
|---------|-------|---------|
| #manager-nudges | C0A5V9JL2KV | Morning pulse, live nudges |
| #margin-alerts | C0A5L7MG60P | Zero revenue, low margin alerts |
| #material-intel-systems | C0A5L7RB5EK | Material truth reports |
| #live-ops | TBD | ServiceTitan estimate alerts |
| #friend-zone | TBD | Raw ServiceTitan email alerts |

## System Integration Notes

- **#manager-nudges** receives multiple alert types - ensure proper formatting
- **#margin-alerts** should only receive revenue/margin issues  
- **#material-intel-systems** gets daily material/invoice reports
- **#live-ops** needs to be created for estimate reformatter
- **#friend-zone** is source for email-based alerts

## Channel Access

All operational intelligence posting uses the Slack bot token from:
`/Users/stephendobbins/.config/ranger/integrations.json`

```json
{
  "slack": {
    "bot_token": "xoxb-..."
  }
}
```