# Code recipes — plugging vemem into real pipelines

Concrete copy-paste code for the flows that come up constantly.

## Scope and privacy — read before copying

**vemem itself never sends image bytes over the network** (the one first-use InsightFace model download aside). But the recipes below include optional VLM and LLM calls that *can* send images to third-party APIs if you pick those providers.

The three recipes, ordered by data-locality:

1. **Ollama** — fully local. Images stay on your machine. Recommended for first-run and for privacy-sensitive deployments.
2. **OpenAI** — images encoded and sent to OpenAI's API. Review OpenAI's data retention policy before using in production.
3. **Anthropic (Claude)** — same as OpenAI: images sent to the API. Review Anthropic's retention policy.

If the user hasn't opted into remote VLM/LLM calls, stay on the Ollama path. vemem never requires a remote API; the composition is a deployer's choice.

---

## Pattern 1 — Camera frame → VLM + vemem + LLM

### Ollama (fully local, no API keys, no data egress)

```python
import ollama
from vemem import Vemem, Source

vem = Vemem()  # LanceDB at ~/.vemem, InsightFace face encoder

def on_new_frame(image_bytes: bytes) -> str:
    # Write path — ingest the image
    observations = vem.observe(image_bytes)
    candidates = vem.identify(image_bytes, k=3, min_confidence=0.4)

    # If we know someone, ask the VLM what they're doing and store that
    if candidates:
        scene = ollama.chat(
            model="qwen2-vl:7b",
            messages=[{
                "role": "user",
                "content": "Describe what this person is doing in one sentence.",
                "images": [image_bytes],
            }],
        )["message"]["content"]
        vem.remember(candidates[0].entity.id, scene, source=Source.VLM)

    # Read path — assemble context for the chat LLM
    context_lines = []
    for c in candidates:
        facts = "; ".join(f.content for f in c.facts)
        context_lines.append(f"- {c.entity.name} (conf {c.confidence:.2f}): {facts}")
    context = "People visible:\n" + "\n".join(context_lines) if context_lines else "No known faces."

    reply = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": f"Visual context:\n{context}"},
            {"role": "user", "content": "What's happening? Who's here?"},
        ],
    )
    return reply["message"]["content"]
```

### OpenAI (GPT-4o vision + chat)

```python
import base64
from openai import OpenAI
from vemem import Vemem, Source

client = OpenAI()
vem = Vemem()

def on_new_frame(image_bytes: bytes, user_msg: str) -> str:
    observations = vem.observe(image_bytes)
    candidates = vem.identify(image_bytes, k=3)

    if candidates:
        b64 = base64.b64encode(image_bytes).decode("ascii")
        scene = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe what this person is doing."},
                    {"type": "image_url",
                     "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                ],
            }],
        ).choices[0].message.content or ""
        vem.remember(candidates[0].entity.id, scene, source=Source.VLM)

    context = ""
    for c in vem.identify(image_bytes, k=3):
        context += f"- {c.entity.name}: {', '.join(f.content for f in c.facts)}\n"

    return (client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Visual context:\n{context}"},
            {"role": "user", "content": user_msg},
        ],
    ).choices[0].message.content or "")
```

### Claude (Anthropic vision + chat)

```python
import base64
from anthropic import Anthropic
from vemem import Vemem, Source

client = Anthropic()
vem = Vemem()

def on_new_frame(image_bytes: bytes, user_msg: str) -> str:
    observations = vem.observe(image_bytes)
    candidates = vem.identify(image_bytes, k=3)

    if candidates:
        b64 = base64.b64encode(image_bytes).decode("ascii")
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=256,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image",
                     "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}},
                    {"type": "text", "text": "Describe what this person is doing."},
                ],
            }],
        )
        scene = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
        vem.remember(candidates[0].entity.id, scene, source=Source.VLM)

    context = ""
    for c in vem.identify(image_bytes, k=3):
        context += f"- {c.entity.name}: {', '.join(f.content for f in c.facts)}\n"

    reply = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        system=f"Visual context:\n{context}",
        messages=[{"role": "user", "content": user_msg}],
    )
    return "".join(b.text for b in reply.content if getattr(b, "type", "") == "text")
```

---

## Pattern 2 — Correction after a wrong identify

When the user says *"that's not Charlie, that's Dana"*:

```python
candidates = vem.identify(image_bytes)
wrong_obs_id = candidates[0].matched_observation_ids[0]

# relabel emits a positive binding to the new entity AND a negative
# binding against the old entity. The auto-clusterer can never re-attach
# this observation to Charlie.
vem.relabel(wrong_obs_id, "Dana")
```

If the user says *"these two people are the same"* (e.g. "unknown_7 and Charlie are me from different lighting"):

```python
charlie = vem.store.find_entity_by_name("Charlie")
unknown = vem.store.find_entity_by_name("unknown_7")
winner = vem.merge([charlie.id, unknown.id], keep="oldest")
# Facts from both entities now live on `winner` with provenance tags
# so the caller LLM can see where each fact came from.
```

If the user says *"those are actually two different people"* (e.g. Charlie and Chad were conflated):

```python
charlie = vem.store.find_entity_by_name("Charlie")
charlie_obs = [o.observation_id for o in vem.store.bindings_for_entity(charlie.id)
               if o.valid_to is None and /* user confirmed is actually Charlie */]
chad_obs = [/* the other set */]

charlie_after, chad = vem.split(charlie.id, [charlie_obs, chad_obs])
# Cross-wise negative bindings are emitted — the clusterer can't re-merge.
```

---

## Pattern 3 — Privacy flows

### Forget (irreversible, GDPR Art. 17)

```python
# User: "delete everything you have on Sarah"
sarah = vem.store.find_entity_by_name("Sarah")
if sarah is None:
    return "No entity named Sarah."

# Confirm with the user before calling — forget is irreversible.
# After this: embeddings are physically pruned from LanceDB version
# history, observations / bindings / facts / events / relationships
# all deleted. The entity row remains as an opaque tombstone for audit.
counts = vem.forget(sarah.id)
return f"Deleted: {counts}"
```

### Restrict (reversible, GDPR Art. 18)

```python
# User: "don't use Sarah for identification for now"
vem.restrict(sarah.id)
# Sarah's facts still readable via recall(), but she's excluded from
# identify() until you call vem.unrestrict(sarah.id).
```

### Export (portability, GDPR Art. 20)

```python
import json
dump = vem.export(sarah.id, include_embeddings=False)
print(json.dumps(dump, indent=2))
# Hand to the user. `include_embeddings=True` adds raw biometric vectors
# which are usually not what they want.
```

---

## Pattern 4 — Composing with Mem0 / Letta / Supermemory

vemem owns visual identity. Mem0 / Letta / Supermemory own text conversational memory. They share an identity namespace if you use vemem's `entity_id` as their `user_id`:

```python
from mem0 import MemoryClient
from vemem import Vemem

vem = Vemem()
mem0 = MemoryClient()

# Resolve visual identity first
candidates = vem.identify(image_bytes)
if not candidates:
    return "Unknown face — ask the user who this is, then label it."
entity = candidates[0].entity

# mem0 keys on user_id — we use the vemem entity id
mem0_facts = mem0.search(query=user_message, user_id=entity.id)

# Assemble both contexts
visual_context = (f"Visible: {entity.name} (conf {candidates[0].confidence:.2f}). "
                  f"Visual facts: {[f.content for f in candidates[0].facts]}")
conversational_context = f"Past conversations: {mem0_facts}"

# Feed both to the LLM
# vemem gave you "who"; mem0 gave you "what we've talked about"
```

**Rule of thumb for which system gets a given fact:**

- Short, structural, about an entity → `vemem.remember(entity.id, fact)`. Example: *"Charlie works at Acme."*
- Conversational, distilled from chat turns → `mem0.add(message, user_id=entity.id)`. Example: *"Charlie seems stressed about the deadline based on our last three chats."*

vemem does NOT do LLM-based fact extraction. It takes you at your word.

---

## Running the MCP server

For Claude Desktop / Cursor / any MCP client:

```bash
pip install vemem  # or: uv pip install vemem
vemem-mcp-server   # stdio server, registered as a [project.scripts] entry
```

Paste into Claude Desktop's config:

```json
{
  "mcpServers": {
    "vemem": {
      "command": "vemem-mcp-server",
      "env": {"VEMEM_MCP_ACTOR": "mcp:alice"}
    }
  }
}
```

The server exposes all 14 tools — see `mcp-tools.md` in this folder for exact schemas.

---

## OpenClaw / Hermes Agent

First-party integration ships as `vemem.integrations.openclaw`. Install:

```bash
pip install vemem
vemem-openclaw-sidecar &   # HTTP sidecar on localhost
# then register the openclaw plugin per integrations/openclaw/README.md
```

Vemem slots in as the automatic image-understanding provider — the agent doesn't need to call a tool for it. Every image attachment in the conversation gets face-recognized and fact-recalled before the thinking LLM sees the message, same shape as mem0's conversational memory but for visual identity.

For other skills-compatible hosts (Hermes Agent, Goose, OpenHands, Letta, Claude Code, Cursor, etc.), the plain MCP server works. Point the host at `vemem-mcp-server` and you're done.
