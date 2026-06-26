# Jira Work Log Skill

Manage your self-hosted Jira work logs through OpenClaw. This skill helps you never forget to log your time and provides easy access to Jira work logging.

## Prerequisites

1. **Jira API Token** from https://id.atlassian.com/manage/api-tokens
2. **Self-hosted Jira instance** (e.g., https://jira.neor.space)
3. **Python 3.7+** with `requests` library

## Setup

### 1. Install Python Dependencies
```bash
python3 -m pip install requests --proxy http://localhost:2080 --user --break-system-packages
```

### 2. Configure Jira Credentials
```bash
# Copy the example config
cp jira_config.example.json jira_config.json

# Edit with your credentials
nano jira_config.json
```

Fill in:
- `username`: Your Jira username/email
- `api_token`: Your API token
- `jira_url`: https://jira.neor.space
- `default_project`: Your main project key
- `timezone`: Asia/Tehran

## Commands

### Test Connection
```
/jira test
```
Tests the connection to your Jira instance.

### List Recent Issues
```
/jira list
```
Shows your recent issues that need work logging.

### Quick Log Work
```
/jira log
```
Interactive work logging with issue selection.

### Create Daily Log
```
/jira today
```
Creates a daily work log template.

### Set Reminders
```
/jira reminder
```
Sets up Apple Reminders for daily work logging.

## Usage Examples

```bash
# Test your Jira connection
/jira test

# Log 1.5 hours to issue PROJ-123
/jira log --issue PROJ-123 --time "1h 30m" --comment "Fixed authentication bug"

# Interactive logging
/jira log

# Create today's work log
/jira today
```

## Integration with OpenClaw

This skill provides the following capabilities:

1. **API-based Jira integration** using Python requests
2. **Interactive CLI** for easy work logging
3. **Daily log templates** for tracking work
4. **Reminder system** using Apple Reminders
5. **Simple configuration** with JSON files

## Files

- `jira_config.json` - Your Jira credentials (DO NOT SHARE)
- `jira_tools.py` - Python API client
- `jira_log.sh` - CLI wrapper script
- `create_daily_log.sh` - Daily log creator
- `daily_log_template.md` - Log template
- `daily_logs/` - Generated daily logs

## Security Notes

1. **Never commit `jira_config.json`** to version control
2. **Use API tokens** instead of passwords
3. **Keep the workspace secure** with proper permissions
4. **Regularly rotate API tokens** for security

## Troubleshooting

### Connection Issues
```bash
# Test connection
./jira_log.sh test

# Check config file
cat jira_config.json | python3 -m json.tool
```

### Python Issues
```bash
# Check Python version
python3 --version

# Install requests with proxy
python3 -m pip install requests --proxy http://localhost:2080 --user --break-system-packages
```

### Permission Issues
```bash
# Make scripts executable
chmod +x *.sh
```

## Future Enhancements

1. **Webhook integration** for automatic logging
2. **Time tracking** with automatic reminders
3. **Reporting** for weekly/monthly summaries
4. **Integration with calendar** for meeting tracking
5. **Mobile notifications** for logging prompts