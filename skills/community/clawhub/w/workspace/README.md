# Jira Work Log Management System

A simple API-based system to help you manage Jira work logs and never forget to log your time again.

## Features

- ✅ **Interactive work logging** with issue selection
- ✅ **Daily log templates** for tracking work
- ✅ **Reminder system** using Apple Reminders
- ✅ **Jira API integration** for self-hosted Jira
- ✅ **Simple CLI interface** for quick logging

## Setup Instructions

### 1. **Configure Jira Credentials**

```bash
# 1. Get your API token from:
#    https://id.atlassian.com/manage/api-tokens

# 2. Edit the configuration file
nano jira_config.json

# Fill in:
# - username: Your Jira username/email
# - api_token: Your API token
# - jira_url: https://jira.neor.space
# - default_project: Your main project key
```

### 2. **Test Connection**

```bash
./jira_log.sh test
```

### 3. **Install Python Dependencies (Optional)**

The script uses the Python `requests` library. If not installed:

```bash
python3 -m pip install requests
```

## Usage

### Quick Start

```bash
# Create today's work log
./create_daily_log.sh

# Log work to Jira (interactive)
./jira_log.sh log

# List your recent issues
./jira_log.sh list
```

### Set Up Daily Reminders

```bash
# Set reminders for logging (requires remindctl)
./jira_log.sh reminder
```

### Manual Logging

```bash
# Log work with specific issue
./jira_log.sh log --issue PROJ-123 --time "1h 30m" --comment "Fixed bug"

# Or use interactive mode
./jira_log.sh log
```

## File Structure

```
.
├── jira_config.json          # Your Jira credentials (DO NOT SHARE!)
├── jira_config.example.json  # Example config
├── jira_tools.py             # Python Jira API client
├── jira_log.sh               # Main CLI wrapper
├── create_daily_log.sh       # Daily log creator
├── daily_log_template.md     # Log template
├── daily_logs/               # Generated daily logs
│   └── 2025-01-15.md        # Example daily log
└── README.md                 # This file
```

## Daily Workflow

1. **Morning (9:00)**
   - Run `./create_daily_log.sh` to create today's log
   - Plan your day in the log file

2. **Throughout the day**
   - Use `./jira_log.sh log` to log work as you complete tasks
   - Update your daily log with notes

3. **End of day (17:00-18:00)**
   - Review your daily log
   - Ensure all work is logged to Jira
   - Add accomplishments and tomorrow's plan

## Tips

1. **Keep jira_config.json secure** - Never commit it to version control
2. **Use the reminder system** - Set up daily reminders
3. **Batch logging** - Log work at natural breaks (morning, after lunch, end of day)
4. **Use templates** - The daily log template helps structure your work

## Troubleshooting

### Connection Issues
```bash
# Test connection
./jira_log.sh test

# Check if jira_config.json exists and is valid
cat jira_config.json | python3 -m json.tool
```

### Python Issues
```bash
# Install required library
python3 -m pip install requests

# Check Python version
python3 --version
```

### Permission Issues
```bash
# Make scripts executable
chmod +x *.sh
```

## Integration with OpenClaw

You can create an OpenClaw skill from this system. Ask me to help you create a `SKILL.md` file for Jira work log management.

## Support

For issues or feature requests, update the scripts or ask for assistance!