# CAP MCP Server Integration Guide

## Operation Safety

- **Classification**: `local-only`
- The CAP MCP server reads local CAP model/docs and has no bundled tenant credentials, destinations, tokens, or service keys.
- Keep examples read-only by default; explicit user approval is required before changing MCP config or running commands that deploy, publish, or affect remote systems.

## Overview

The CAP MCP (Model Context Protocol) server provides AI agents with live access to your CAP project's compiled model and documentation. This integration enables Claude Code agents to:

- **Search your CDS model** for entities, services, actions, and relationships
- **Query CAP documentation** semantically for syntax, patterns, and best practices
- **Understand your project structure** without reading every file
- **Provide context-aware assistance** based on your actual data model

The MCP server runs locally alongside your CAP project, with no external API calls or cloud dependencies.

## Installation

The CAP MCP server is distributed as an npm package that can be run directly with npx:

```bash
# No installation needed - npx auto-downloads and runs
npx -y @cap-js/mcp-server@0.0.5

# Or install globally for faster access
npm install -g @cap-js/mcp-server@0.0.5
```

**Requirements**:
- Node.js 18+ LTS
- CAP project with compiled model (run `cds build` first)

**No environment variables required** - unlike some MCP servers, CAP's has zero configuration dependencies.

## Available MCP Tools

### search_model

Fuzzy search for CDS definitions in your project's compiled Core Schema Notation (CSN) model.

**What it searches**:
- Entity definitions and their fields
- Service definitions and exposed entities
- Actions and functions (bound and unbound)
- Associations and compositions
- Annotations and metadata
- HTTP endpoints (auto-generated OData routes)

**Returns**:
- Definition details (type, properties, constraints)
- Relationships (associations, compositions)
- Annotations (UI, validation, authorization)
- HTTP endpoints with methods

**Use when**:
- Finding entities by name or pattern
- Checking what associations an entity has
- Discovering available services and their endpoints
- Looking up action/function signatures
- Understanding entity relationships

**Example use cases**:
```
"What entities exist related to orders?"
→ Uses search_model to find Orders, OrderItems, OrderStatus entities

"What associations does Books have?"
→ Uses search_model to show author, reviews, category associations

"What HTTP endpoints does CatalogService expose?"
→ Uses search_model to list all OData routes
```

### search_docs

Semantic search through preprocessed SAP CAP documentation using vector embeddings.

**What it searches**:
- CDS syntax and language features
- CAP Node.js/Java API references
- Service handler patterns
- Deployment guides
- Best practices and examples

**Search technology**:
- **Vector embeddings**: Converts your query to semantic representation
- **Similarity matching**: Finds documentation chunks with highest relevance
- **Locally cached**: No network calls, fully offline-capable
- **Semantic understanding**: Finds relevant docs even without exact keyword matches

**Use when**:
- Looking up CDS syntax (associations, compositions, annotations)
- Finding CAP API patterns (event handlers, CQL queries)
- Checking deployment configuration options
- Learning best practices for specific scenarios
- Troubleshooting common issues

**Example use cases**:
```
"How do I define a composition in CDS?"
→ Uses search_docs to find composition syntax with examples

"What's the API for registering a BEFORE CREATE handler?"
→ Uses search_docs to find srv.before() patterns

"How do I configure multitenancy?"
→ Uses search_docs to find multitenancy setup guide
```

## Integration with Claude Code

The sap-cap-capire plugin automatically configures the MCP server when enabled. The `.mcp.json` file at the plugin root defines the server connection:

```json
{
  "sap-cap-capire": {
    "command": "npx",
    "args": ["-y", "@cap-js/mcp-server@0.0.5"],
    "env": {}
  }
}
```

### For VS Code (Cline Extension)

Add to your Cline settings (`.vscode/cline_mcp_settings.json`):

```json
{
  "mcpServers": {
    "cap-mcp": {
      "command": "npx",
      "args": ["-y", "@cap-js/mcp-server@0.0.5"],
      "env": {}
    }
  }
}
```

### For opencode

Add to your MCP configuration (`~/.config/opencode/mcp.json`):

```json
{
  "mcp": {
    "cap-mcp": {
      "type": "local",
      "command": ["npx", "-y", "@cap-js/mcp-server@0.0.5"],
      "enabled": true
    }
  }
}
```

### For GitHub Copilot

Create or update `mcp.json` in your project root:

```json
{
  "servers": {
    "cap-mcp": {
      "command": "npx",
      "args": ["-y", "@cap-js/mcp-server@0.0.5"],
      "env": {},
      "type": "stdio"
    }
  }
}
```

## Rules for LLM Usage

**CRITICAL RULES from official CAP MCP documentation:**

### Rule 1: Always Search Model First

You MUST search for CDS definitions with `search_model` first. Only read `.cds` files if `search_model` fails.

**Why**: The compiled CSN model is the source of truth. Raw CDS files may not reflect associations, resolved references, or computed metadata.

**Example workflow**:
```
User: "What fields does Books entity have?"
❌ WRONG: Read db/schema.cds directly
✅ CORRECT: Use search_model("Books", type="entity") first
```

### Rule 2: Always Search Docs Before Coding

You MUST search for CAP documentation with `search_docs` EVERY TIME you create or modify CDS models or use CAP APIs. Do NOT propose changes without checking documentation first.

**Why**: CAP syntax and APIs evolve. The MCP server's cached documentation is always current and includes official patterns.

**Example workflow**:
```
User: "Add an association to Categories"
❌ WRONG: Write association syntax from memory
✅ CORRECT: Use search_docs("association syntax CDS") to confirm current syntax
```

### Rule 3: Trust MCP Tools Over File Reads

MCP tools search the compiled model (CSN) and official docs. File reads show only source code, not the final compiled structure.

**Priority**:
1. search_model / search_docs (highest trust)
2. Read tool on specific files (when MCP tools return no results)
3. Grep/Glob for discovery (when you don't know what to search for)

## Troubleshooting

### Issue: MCP server not found

**Symptoms**: Tools not available, connection errors

**Solutions**:
```bash
# Option 1: Install globally for faster access
npm install -g @cap-js/mcp-server@0.0.5

# Option 2: Use npx (auto-installs on first run)
npx -y @cap-js/mcp-server@0.0.5

# Option 3: Add to project devDependencies
npm install --save-dev @cap-js/mcp-server@0.0.5
```

### Issue: search_model returns no results

**Possible causes**:
- Project not compiled yet
- Query too specific
- Entity/service name mismatch (case sensitivity)

**Solutions**:
```bash
# Compile your CAP project first
cds build

# Verify compilation succeeded
cds compile srv/ --to csn

# Try broader search terms
# Instead of "BookStore", try "Book"
```

### Issue: search_docs returns irrelevant results

**Possible causes**:
- Query too broad or too narrow
- Semantic mismatch (embeddings don't understand intent)

**Solutions**:
- **Be specific**: "composition syntax CDS" not "how to use CDS"
- **Use technical terms**: "srv.before CREATE handler" not "how to validate"
- **Include version**: "CAP Node.js multitenancy" not just "multitenancy"

### Issue: First run is slow

**Expected behavior**: The first `search_docs` call downloads and caches documentation embeddings (~50MB).

**Subsequent runs**: Instant (uses cached embeddings from `~/.cache/cap-mcp/`)

**Solution**: Just wait on first run. All subsequent searches will be fast.

## Performance

### search_model Performance

- **Speed**: Instant (local file read + fuzzy search)
- **Network**: Zero network calls
- **Dependency**: Requires compiled CSN (run `cds build`)

### search_docs Performance

- **First run**: 5-10 seconds (downloads embeddings)
- **Subsequent runs**: <100ms (uses cached embeddings)
- **Network**: Only on first run (then fully offline)
- **Cache location**: `~/.cache/cap-mcp/`

## Advanced Usage

### Using MCP Tools Directly (CLI)

You can use MCP tools from command line for testing:

```bash
# Install globally
npm i -g @cap-js/mcp-server@0.0.5

# Search compiled model
cds-mcp search_model . Books entity

# Search CAP documentation
cds-mcp search_docs "how to add columns to a select statement in CAP Node.js" 1
```

### Integration with Agents

The sap-cap-capire plugin provides 4 specialized agents that use MCP tools:

1. **cap-cds-modeler** (Blue): Uses `search_model` to find entities and `search_docs` for CDS syntax
2. **cap-service-developer** (Green): Uses `search_model` for services and `search_docs` for handler patterns
3. **cap-project-architect** (Purple): Uses `search_docs` for deployment and multitenancy configuration
4. **cap-performance-debugger** (Orange): Uses `search_model` to analyze relationships and `search_docs` for optimization patterns

Each agent automatically leverages MCP tools as part of their workflow.

## Security

**No credentials required**: CAP MCP server has no authentication requirements.

**Local only**: All operations are local file reads and cached documentation lookups.

**No data transmission**: Your CDS model never leaves your machine.

**Cache safety**: Documentation cache is read-only and contains only official CAP docs.

## References

- **Official GitHub**: https://github.com/cap-js/mcp-server
- **npm Package**: https://www.npmjs.com/package/@cap-js/mcp-server
- **Community Blog**: https://community.sap.com/t5/technology-blog-posts-by-sap/boost-your-cap-development-with-ai-introducing-the-mcp-server-for-cap/ba-p/14202849
- **License**: Apache-2.0
- **Version**: 0.0.3+ (updated regularly)

For illustrative workflow scenarios and planning assumptions, see [MCP Use Cases](mcp-use-cases.md).
