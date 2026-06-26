# RuRussian Agent-Native MCP

Agent-native MCP server for `rurussian.com` and multi-agent learning workflows.

This version upgrades the original single-file wrapper into a production-oriented learning infrastructure with:

- strict JSON outputs backed by Pydantic schemas
- three explicit layers: atomic tools, workflow tools, and memory tools
- modular services for backend access, parsing, lesson generation, and learner modeling
- persistent JSON-backed learning memory designed for later migration to MongoDB or another database

## Architecture

```text
rurussian_mcp/
  schemas/   -> request/response contracts
  services/  -> backend access, parsing, workflows, memory
  tools/     -> MCP tool registration by layer
  memory/    -> persistence namespace
  server.py  -> thin FastMCP entrypoint
```

## Installation

```bash
pip install rurussian-mcp
```

## Configuration

```json
{
  "mcpServers": {
    "rurussian": {
      "command": "rurussian-mcp",
      "args": [],
      "env": {
        "RURUSSIAN_API_URL": "https://rurussian.com/api",
        "RURUSSIAN_API_KEY": "YOUR_BOT_API_KEY",
        "RURUSSIAN_LEARNER_EMAIL": "learner@example.com"
      }
    }
  }
}
```

Optional environment variables:

- `RURUSSIAN_MEMORY_STORE`
- `RURUSSIAN_LEARNER_ID`
- `RURUSSIAN_BUY_SESSION_ENDPOINTS`
- `RURUSSIAN_CONFIRM_PURCHASE_ENDPOINTS`

## Tool Surface

### Support Tools

- `authenticate`
- `authentication_status`
- `list_pricing_plans`
- `purchase_status`
- `create_key_purchase_session`
- `confirm_key_purchase`

### Layer A: Atomic Tools

- `parse_sentence`
- `generate_examples`
- `generate_reading_passage`

### Layer B: Workflow Tools

- `explain_text_for_learner`
- `create_daily_lesson`
- `create_review_session`
- `evaluate_user_answer`
- `simulate_conversation`

### Layer C: Memory Tools

- `get_learning_profile`
- `update_learning_progress`
- `get_next_best_lesson`

## Examples

Structured request and response examples for every tool are in `examples/tool_examples.json`.

## Notes

- The server reuses the real RuRussian backend where it already exists today: translation, Zakuska generation, sentence generation, and checkout flows.
- Sentence parsing, lesson assembly, learner scoring, and profile memory are implemented locally so autonomous agents can compose deterministic JSON outputs.
- Memory uses a simple JSON store now and is isolated behind a service layer for future database-backed scaling.
