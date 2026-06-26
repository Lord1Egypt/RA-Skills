# Sefaria MCP Skill for ClawHub

This skill provides guidance and helper tools for using the Sefaria API MCP server.

## Installation

1. Clone the repository
2. Install dependencies: `npm install`
3. Build the project: `npm run build`
4. Import the skill in ClawHub

## Tools

### connect
Starts the Sefaria API MCP server.

**Arguments:**
- `port` (optional): Port number (default: 8080)

### use
Shows example usage patterns for all available Sefaria MCP tools.

## Usage in ClawHub

Once installed, you can use the skill tools to:
1. Start the MCP server with `connect`
2. View examples with `use`
3. Access all Sefaria API tools through the MCP

## Available MCP Tools

The MCP server provides access to:
- Text retrieval (get_text, get_random_text, get_manuscripts)
- Search & discovery (search, find_refs, get_toc)
- Related content (get_related, get_links, get_topics)
- Lookup (get_index, get_shape, get_lexicon)
- Calendar (get_calendars)

See the main README for complete documentation.
