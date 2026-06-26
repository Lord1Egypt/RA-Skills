# Simple SMTP Mail - AI Assistant Guide

This skill allows sending emails via SMTP using the msmtp command-line tool.

## Quick Start

1. User must configure their SMTP credentials in `~/.msmtp/config`
2. Use the exec tool to run msmtp commands

## Sending Email Command

```bash
echo -e "Subject: <SUBJECT>\n\n<BODY>" | msmtp --file=/Users/yugaoxiang/.msmtp/config <RECIPIENT>
```

Or with From header:
```bash
echo -e "Subject: <SUBJECT>\nFrom: <SENDER_EMAIL>\n\n<BODY>" | msmtp --file=/Users/yugaoxiang/.msmtp/config <RECIPIENT>
```

## Important Notes

- Never include actual email addresses, passwords, or credentials in skill files
- Always use placeholder values in examples
- The actual config file is stored at `~/.msmtp/config` (user's home directory)
- msmtp must be installed on the system

## Requirements

- msmtp command-line tool installed
- Valid SMTP configuration in ~/.msmtp/config
