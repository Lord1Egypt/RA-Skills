# Sample prompts

Use these to verify the agent picks up the WorkOS skill and connects to the
server correctly.

## Connection

> "Connect to the WorkOS MCP."

> "Set up workos.no in Claude Desktop."

## Reading

> "What open tasks do I have in my workspace?"

> "Find the document I wrote about Q1 strategy."

> "Show me all meetings from last week."

## Writing

> "Create a new page in the Notes group called 'Research ideas 2026'."

> "Add a task to the Tasks database: 'Order webinar equipment', due next Friday."

> "Write a summary of the meeting I uploaded yesterday."

## Organization

> "Move all pages about customer X into a new group called 'Customer X'."

> "Create a kanban view of the Tasks database grouped by Status."

## Sharing

> "Create a shareable link to the page 'Welcome to onboarding' that expires in a week."

> "Revoke share links older than 30 days."

## Expected behavior

For every prompt above, the agent should:

1. Confirm which workspace if there is more than one.
2. Fetch IDs through list/search tools before writing.
3. Confirm destructive operations with the user.
4. Return a short summary with a URL/ID after the action.
