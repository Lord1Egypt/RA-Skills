---
name: agent-custom-mermaid
description: How to send Mermaid diagrams to Ray for agent output
metadata:
  tags: agent, mermaid, diagram, payload, custom
---

## Agent Custom Mermaid Payload

The agent custom Mermaid payload renders Mermaid diagrams in Ray for visualizing flowcharts, sequence diagrams, and other diagram types.

### When to Use

Use the agent custom Mermaid payload when you want to:

- Visualize flowcharts and process flows
- Show sequence diagrams for system interactions
- Display class diagrams for code architecture
- Render state diagrams, ER diagrams, Gantt charts, or pie charts
- Explain complex relationships visually

### Payload Structure

```json
{
  "type": "ai_custom_mermaid",
  "content": {
    "mermaid": "graph TD\n    A[Start] --> B[End]",
    "label": "Diagram"
  },
  "origin": {
    "function_name": "code-agent",
    "file": "code-agent",
    "line_number": 1,
    "hostname": "my-computer"
  }
}
```

### Content Fields

| Field     | Type   | Required | Description                                             |
| --------- | ------ | -------- | ------------------------------------------------------- |
| `mermaid` | string | Yes      | Valid Mermaid diagram code (without code fences).       |
| `label`   | string | No       | Label for the log entry (e.g., "Architecture Diagram"). |

### Supported Diagram Types

- **Flowcharts** (`graph TD`, `graph LR`)
- **Sequence diagrams** (`sequenceDiagram`)
- **Class diagrams** (`classDiagram`)
- **State diagrams** (`stateDiagram-v2`)
- **Entity Relationship diagrams** (`erDiagram`)
- **Gantt charts** (`gantt`)
- **Pie charts** (`pie`)
- **Git graphs** (`gitGraph`)
- **Mind maps** (`mindmap`)

### HTTP API Examples

#### Simple Flowchart

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"ai_custom_mermaid","content":{"mermaid":"graph TD\n    A[Start] --> B{Is it working?}\n    B -->|Yes| C[Great!]\n    B -->|No| D[Debug]\n    D --> B","label":"Flowchart"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Sequence Diagram

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"ai_custom_mermaid","content":{"mermaid":"sequenceDiagram\n    participant Client\n    participant API\n    participant Database\n    Client->>API: POST /users\n    API->>Database: INSERT user\n    Database-->>API: Success\n    API-->>Client: 201 Created","label":"API Flow"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Class Diagram

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"ai_custom_mermaid","content":{"mermaid":"classDiagram\n    class User {\n        +String name\n        +String email\n        +login()\n        +logout()\n    }\n    class Admin {\n        +manageUsers()\n    }\n    User <|-- Admin","label":"Class Diagram"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### State Diagram

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"ai_custom_mermaid","content":{"mermaid":"stateDiagram-v2\n    [*] --> Idle\n    Idle --> Processing: Start\n    Processing --> Success: Complete\n    Processing --> Error: Fail\n    Error --> Idle: Reset\n    Success --> [*]","label":"State Machine"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### ER Diagram

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"ai_custom_mermaid","content":{"mermaid":"erDiagram\n    USER ||--o{ ORDER : places\n    ORDER ||--|{ LINE_ITEM : contains\n    PRODUCT ||--o{ LINE_ITEM : in","label":"ER Diagram"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Pie Chart

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"ai_custom_mermaid","content":{"mermaid":"pie title Test Results\n    \"Passed\" : 85\n    \"Failed\" : 10\n    \"Skipped\" : 5","label":"Test Results"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

### MCP Tool

When using the Ray MCP server, you can use the `send_mermaid_diagram` tool.

**Tool name:** `send_mermaid_diagram`

| Parameter     | Type   | Required | Description                                       |
| ------------- | ------ | -------- | ------------------------------------------------- |
| `mermaid`     | string | Yes      | Valid Mermaid diagram code (without code fences). |
| `projectName` | string | Yes      | The Ray project name.                             |
| `llmName`     | string | No       | Name of the LLM for labeling.                     |
| `hostname`    | string | No       | The hostname.                                     |

### Tips

1. **No code fences**: Don't include `mermaid or ` in the mermaid content.
2. **Indentation**: Use consistent indentation for readability.
3. **Node IDs**: Use descriptive IDs for nodes (e.g., `UserAuth` instead of `A`).
4. **Labels**: Add labels to connections to clarify relationships.
5. **Direction**: Choose appropriate direction (`TD` top-down, `LR` left-right) based on the diagram.

### Mermaid Documentation

For full syntax reference, see the [Mermaid documentation](https://mermaid.js.org/intro/).
