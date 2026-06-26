# Multi-Turn Analysis Example

## Scenario: Iterative Investigation

**Question**: "Who opened the watermelon and what tool did they use?"

### Turn 1: Initialize Memory

```python
import json
from pathlib import Path

memory = {
  "question": "Who opened the watermelon and what tool did they use?",
  "findings": [],
  "hypotheses": [],
  "next_actions": ["Get video info", "Explore beginning"]
}
Path("videoarm_memory.json").write_text(json.dumps(memory, indent=2))
```

### Turn 2: Explore

```bash
videoarm-scene --video video.mp4 \
  --ranges '[{"start_frame":0,"end_frame":1000}]' \
  --num-frames 30
```

Update memory:
```python
memory["findings"].append({
  "tool": "scene",
  "result": "Person in white suit with watermelon on table",
  "confidence": 0.6
})
memory["next_actions"] = ["Identify person's name", "Find tool used"]
```

### Turn 3: Identify Person

```bash
videoarm-analyze-clip --video video.mp4 \
  --start-frame 0 --end-frame 1000 \
  --question "What is the name of the person in the white suit?"
```

### Turn 4: Find Tool

```bash
videoarm-analyze-clip --video video.mp4 \
  --start-frame 0 --end-frame 1000 \
  --question "What tool is being used to open the watermelon?"
```

### Final Answer

Combine findings from memory to answer the original question.
