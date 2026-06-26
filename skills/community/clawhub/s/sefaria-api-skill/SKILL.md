# Sefaria API MCP

MCP server for accessing the Sefaria API - the largest open-source database of Jewish texts.

## Description

This skill provides guidance and helper tools for using the Sefaria API MCP server. Access the complete library of Jewish texts including Torah, Talmud, Mishnah, commentaries, and more through a simple MCP interface.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/davad00/sefaria-api-mcp.git
cd sefaria-api-mcp
```

2. Install dependencies:
```bash
npm install
```

3. Build the project:
```bash
npm run build
```

## Tools

### connect
Starts the Sefaria API MCP server.

**Arguments:**
- `port` (optional): Port number (default: 8080)

**Example:**
```javascript
{
  "name": "connect",
  "arguments": {
    "port": 8080
  }
}
```

### use
Shows example usage patterns for all available Sefaria MCP tools.

**Example:**
```javascript
{
  "name": "use"
}
```

## Available MCP Tools

Once the MCP server is running, you have access to:

### Text Retrieval
- `get_text` - Get text by reference (e.g., 'Genesis 1:1', 'Shabbat 2b')
- `get_text_v1` - Legacy v1 text endpoint
- `get_random_text` - Get random text segment
- `get_manuscripts` - Get manuscript variants

### Search & Discovery
- `search` - Full-text search across library
- `find_refs` - Parse text to find Sefaria references
- `get_toc` - Table of contents (all available texts)
- `get_category` - Texts in a specific category

### Related Content
- `get_related` - All related content (links, sheets, topics)
- `get_links` - Cross-references to other sources
- `get_topics` - Topic details
- `get_all_topics` - List all topics
- `get_ref_topic_links` - Topics linked to a reference

### Lookup
- `get_index` - Text metadata (structure, versions)
- `get_shape` - Text structure
- `get_lexicon` - Hebrew word definitions
- `get_versions` - Available translations

### Calendar
- `get_calendars` - Get today's Torah readings and Jewish calendar information

## Example Usage

```javascript
// Get Genesis 1:1
{
  "name": "get_text",
  "arguments": { "tref": "Genesis 1:1" }
}

// Search for "love"
{
  "name": "search",
  "arguments": { "q": "love", "limit": 5 }
}

// Parse references from text
{
  "name": "find_refs",
  "arguments": { "text": "As it says in Shabbat 31a" }
}

// Get today's readings
{
  "name": "get_calendars"
}
```

## Configuration

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "sefaria": {
      "command": "node",
      "args": ["path/to/sefaria-api-mcp/dist/index.js"]
    }
  }
}
```

## Links

- [GitHub Repository](https://github.com/davad00/sefaria-api-mcp)
- [Sefaria API Documentation](https://developers.sefaria.org/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## License

MIT License - Free to use, modify, and redistribute.

## Support

For issues or questions:
- Open an issue on [GitHub](https://github.com/davad00/sefaria-api-mcp/issues)
- Check the [Sefaria API docs](https://developers.sefaria.org/)
