# Signalgrid Live Activities for OpenClaw
[![ClawHub Skill](https://img.shields.io/badge/ClawHub-signalgrid--activity-blue?logo=openclaw&logoColor=white)](https://clawhub.ai/signalgridco/signalgrid-activity)

Send Live Activities & Ongoing notifications to your iOS / Android via Signalgrid.

## Setup

1. **Create an Account**: 
Get your credentials at https://web.signalgrid.co

2. **Configure OpenClaw**: 
Add your credentials to your OpenClaw settings (typically `config.yaml` or through the dashboard):

   vars:
     SIGNALGRID_CLIENT_KEY: "your_client_key_here"
     SIGNALGRID_CHANNEL: "your_channel_name_here"

3. **Set Tool Profile**: You MUST set the tool profile to **full**. Without this, the skill cannot reach the Signalgrid API.
   
   **Where to find it:**
   Settings -> Config -> tools -> tool profile

## Installation

``` bash
clawdhub --workdir ~/.openclaw install signalgrid-activity
```

## How to use

The AI automatically uses this skill when you ask to start live activities. 
It handles different priority levels:

- **INFO**: Starts a activity for informational purposes. ( Blue )
- **WARN**: This is a kind of important activity, but not that serious. ( Yellow )
- **CRIT**: Somehting needs immediate attention. This is serious ( Red )
- **SUCCESS**: All good again. ( Green )

### Example Prompts:

- "Start an activity of critical importance on my phones"
- "Start a informational activity on my phone with title "Openclaw backup", body "Backup in progress...", 1 step, 10% progress. Show the legend with "Backup started" as start-text and "Backup ended" as end-text."
- "Progress my activity to 20%"
- "Set the severity of my activity to warn and progress it by 10%"
- "End my activity, and delay the dismissal for 5 minutes"
