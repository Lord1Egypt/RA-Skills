# Telegram Analyzer Skill

Access and manage your SaaS contacts and messages.

## Tools

### search_contacts
Search for contacts by name, phone, or username.
- query (string, required): The search term.

### get_recent_messages
Get the 10 most recent incoming messages.

### contact_action
Update contact stage, tags, or add notes.
- contact_id (string, required): Contact UUID.
- action (string, required): \"update_stage\", \"add_tag\", or \"add_note\".
- value (string, required): The new value.
