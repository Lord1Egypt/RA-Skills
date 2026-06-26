# Interfaces

Interfaces are an abstraction layer over integrations. They define a standard contract (a set of actions) that multiple integrations can implement. The ADK uses interfaces to call the same logical action across different integrations without writing integration-specific code.

## Key Concepts

- **Interfaces are built-in.** The ADK automatically includes a fixed set of interfaces in every project. Interfaces are provided by the ADK — they are resolved automatically based on installed integrations.
- **Interfaces map to integration actions.** At build time, the ADK discovers which installed integrations implement each interface and generates a mapping from interface actions to concrete integration actions.
- **The runtime resolves calls automatically.** When code calls an interface action (e.g., `startTypingIndicator`), the runtime looks up the correct integration action for the current conversation's integration.

## Built-in Interfaces

Every ADK project includes these interfaces (defined in `@botpress/adk` constants):

| Interface          | Version | Purpose                                                    |
| ------------------ | ------- | ---------------------------------------------------------- |
| `typing-indicator` | `0.0.3` | Start/stop typing indicators across messaging integrations |
| `llm`              | `9.0.0` | Standard LLM operations                                    |
| `listable`         | `0.0.2` | List operations on integration resources                   |

These are hard-coded in the ADK and synced automatically during `adk dev` and `adk build`. Users cannot modify this list.

> **Naming:** Interface package names use kebab-case (`typing-indicator`), but the runtime uses camelCase (`typingIndicator`). The ADK handles this translation automatically.

## What Interfaces Enable

### Typing Indicators in Conversation Handlers

The `typing-indicator` interface powers `conversation.startTyping()` and `conversation.stopTyping()`. These work automatically for any integration that implements the interface (webchat, Slack, etc.) with no integration-specific code needed:

```typescript
import { Conversation } from '@botpress/runtime'

export const Chat = new Conversation({
  channel: 'webchat.channel',

  async handler({ conversation, execute }) {
    await conversation.startTyping()

    // Do work...

    await execute({
      instructions: 'Help the user',
    })
    // Typing stops automatically when a message is sent
  },
})
```

If the conversation's integration does not implement `typing-indicator`, the calls silently no-op (errors are caught and swallowed).

### CLI Commands

```bash
# List built-in interfaces
adk interfaces list

# Show details about a specific interface
adk interfaces info llm

# Both commands support --format json
adk interfaces list --format json
```

### Generated Type Files

The ADK generates interface types in `.adk/interfaces/`. Each interface gets:

- `<interface_name>/index.ts` - Type and const exports
- `<interface_name>/actions.ts` - Per-integration action types and mapping constants

These are aggregated in:

- `.adk/interfaces.d.ts` - Global `Interfaces` type declaration
- `.adk/interfaces.ts` - Runtime `Interfaces` const (the mapping object)

## Relationship to Integrations

Interfaces and integrations are complementary. See **[integrations.md](./integrations.md)** for integration management.

- **Integrations** are concrete connections to external services (Slack, webchat, Linear). You add them with `adk integrations add`.
- **Interfaces** are abstract contracts. An integration _implements_ an interface by declaring compatible actions with matching schemas.
- When you add an integration that implements an interface, the ADK automatically detects this and generates the mapping. No user action is required.

## Scope and Limitations

- Interfaces are **not user-configurable** in the current ADK. The set of built-in interfaces is fixed.
- Users cannot define custom interfaces or map integrations to interfaces manually.
- Interface resolution is **per-integration** at the conversation level. The runtime determines which integration a conversation belongs to and resolves interface actions accordingly.
- If no installed integration implements an interface, the generated mapping for that interface will be empty (no actions).
- The `llm` and `listable` interfaces may have empty mappings if no installed integration declares support for them.
- Plugins can depend on interfaces for runtime resolution. See [plugins.md](./plugins.md) for how plugin interface dependencies are wired.

## See Also

- [Integrations](./integrations.md) — Integration management overview
- [Integration Actions](./integration-actions.md) — Calling integration actions from code
- [Plugins](./plugins.md) — Plugins that depend on interfaces for runtime resolution
