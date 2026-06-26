# Framework Integrations

## Quick Start

### Python SDK

```python
from scripts.synapse_client import SynapseClient

client = SynapseClient(api_key="sk_connect_...")

# Save
client.remember("User prefers dark mode", agent="my-agent")

# Recall
memories = client.recall("user preferences", agent="my-agent")
```

### LangChain

```python
from synapse_layer import SynapseChatMessageHistory

history = SynapseChatMessageHistory(agent_id="my-agent", session_id="session-1")
history.add_user_message("I prefer concise answers.")
```

### CrewAI

```python
from synapse_layer import SynapseCrewStorage

storage = SynapseCrewStorage(agent_id="research-crew")
# Use with CrewAI: Memory(storage=storage)
```

### AutoGen

```python
from synapse_layer import SynapseAutoGenMemory

memory = SynapseAutoGenMemory(agent_id="autogen-agent")
# Attach to AutoGen agents
```

### LlamaIndex

```python
from synapse_layer import SynapseRetriever

retriever = SynapseRetriever(agent_id="llama-agent", top_k=5)
# Use in query engines
```

### Semantic Kernel

```python
from synapse_layer import SynapseChatHistory

history = SynapseChatHistory(agent_id="sk-agent", session_id="session-1")
# Use with Semantic Kernel functions
```

## Best Practices

### Agent ID Consistency

Use consistent `agent_id`:
- Production: `hermes`, `mel`, `research-agent`
- Development: `hermes-dev`, `mel-test`

### Confidence Scoring

```python
high_confidence = 0.9   # Facts, decisions
medium_confidence = 0.7 # Inferences, preferences
low_confidence = 0.5    # Uncertain info
```

### Metadata Usage

```python
client.remember(
    content="Decision made",
    agent="hermes",
    type="DECISION",
    importance=5,
    tags=["technical", "important"],
    project="website-redesign"
)
```

## Model Handover

Share memories between models:

```python
# Save with GPT-4
client_gpt.remember("Important fact", agent="shared-agent")

# Retrieve with Claude
memories_claude = client_claude.recall("important fact", agent="shared-agent")
```

## Troubleshooting

### Integration Issues

1. Verify API key is valid
2. Check network connectivity
3. Review Trust Quotient scores
4. Monitor quota usage

### Performance

- Use appropriate limits (not 100+ results)
- Batch operations when possible
- Cache frequent recalls
- Use cross-agent search sparingly
