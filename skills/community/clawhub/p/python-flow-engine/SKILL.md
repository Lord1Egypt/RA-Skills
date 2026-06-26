---
name: python-flow-engine
version: "1.0.0"
description: "Lightweight Python flow orchestration library. Use when building data processing pipelines, workflow automation, ETL tasks, or any multi-step computation that needs serial/parallel/conditional execution. Triggers: pipeline, flow, orchestrate, workflow, ETL, data pipeline, process chain."
---

# Python Flow Engine

Lightweight Python flow orchestration — no external dependencies. Build pipelines with serial (>>), parallel (//), and conditional (|) node execution.

## Core API

### Node

```python
from pipeline import Node

def my_fn(context, data):
    # context: shared dict for the pipeline run
    # data: input from previous node
    return modified_data

node = Node(my_fn, name="step1", timeout=10, retry=1)
```

### Pipeline

```python
pipe = Pipeline()
pipe.add_node(node)
pipe.run(start_node, input_data)
```

### Connection Operators

| Operator | Mode | Behavior |
|----------|------|----------|
| `a >> b` | Serial | a runs, then b runs with a's output |
| `a // b` | Parallel | a and b run concurrently (bidirectional) |
| `a \| b` | Conditional | b runs based on a's output (use `connect`) |

For conditional connections, use `connect()`:

```python
pipe.connect(node_a, node_b, "conditional",
    condition=lambda ctx, data: ctx.get("is_valid", False))
```

Or use `Node.condition` parameter:

```python
node_b = Node(fn, condition=lambda ctx, data: data > 0)
```

### Visualization

```python
print(pipe.visualize())  # outputs Mermaid.js flowchart
```

### Error Handling

- **retry**: `Node(fn, retry=2)` retries up to 3 total attempts
- **timeout**: `Node(fn, timeout=5)` raises `RuntimeError` if execution exceeds 5s

## Available Scripts

- `scripts/pipeline.py` — Core library (importable, no dependencies)
- `scripts/pipeline_demo.py` — End-to-end demo (6 scenarios)

## Quick Start

```python
from pipeline import Node, Pipeline

def double(ctx, x): return x * 2
def add_one(ctx, x): return x + 1

pipe = Pipeline()
n1 = Node(double, name="double")
n2 = Node(add_one, name="add_one")
pipe.add_node(n1)
pipe.add_node(n2)
n1 >> n2

result = pipe.run(n1, 5)  # 5*2+1 = 11
print(result)  # 11
print(pipe.visualize())
```

Run the full demo:
```
python scripts/pipeline_demo.py
```
