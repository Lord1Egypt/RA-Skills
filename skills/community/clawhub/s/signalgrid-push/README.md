# Signalgrid Push for OpenClaw
[![ClawdHub Skill](https://img.shields.io/badge/ClawdHub-signalgrid--push-blue?logo=clawd&logoColor=white)](https://clawhub.ai/signalgridco/signalgrid-push)

Send push notifications to your iOS / Android / Web Browser via Signalgrid.

## Setup

1. **Create an Account**: Get your credentials at https://web.signalgrid.co

2. **Configure OpenClaw**: Add your credentials to your OpenClaw settings (typically `config.yaml` or through the dashboard):

   vars:
     SIGNALGRID_CLIENT_KEY: "your_client_key_here"
     SIGNALGRID_CHANNEL: "your_channel_name_here"

3. **Set Tool Profile**: You MUST set the tool profile to **full**. Without this, the skill cannot reach the Signalgrid API.
   
   **Where to find it:**
   Settings -> Config -> tools -> tool profile

## Installation

``` bash
clawdhub --workdir ~/.openclaw install signalgrid-push
```

## How to use

The AI automatically uses this skill when you ask for notifications or alerts. It handles different priority levels:

- **Critical/Error**: Triggers a loud, bypass-DND alert.
- **Warning**: High priority notification.
- **Success/Info**: Standard updates.

### Example Prompts:

- "Tell me on my phone when the backup is finished successfully."
- "Send a critical alert if the server load goes above 90%."

## Supported Types

The skill maps these keywords to the Signalgrid API:

- **crit**: critical, failure, error, alarm
- **warn**: warning, alert
- **success**: successful, ok, done
- **info**: default
