# Router NIMIMORE

Smart model router for OpenClaw. Automatically selects the optimal AI model based on query characteristics, balancing cost and performance.

## Description

Router NIMIMORE analyzes your queries and automatically routes them to the most appropriate AI model:

- **Simple queries** → Economy models (save 85% cost)
- **Code tasks** → Standard models (save 47% cost)  
- **Complex reasoning** → Premium models (best quality)

## Tools

- `router.select` - Select optimal model for query
- `router.analyze` - Analyze query characteristics
- `router.demo` - Run routing demonstration

## Usage

```bash
# Route a query
python scripts/router.py --query "帮我写个Python函数"

# Run demo
python scripts/router.py --demo

# With context length
python scripts/router.py --query "总结文档" --context-length 5000
```

## Configuration

No configuration required. Works out of the box.

## Supported Models

| Model | Tier | Cost/1k | Use Case |
|-------|------|---------|----------|
| moonshot/kimi-k2.5 | Premium | $0.015 | Complex reasoning |
| bailian/qwen-max | Standard | $0.008 | Code & Chinese |
| bailian/qwen-plus | Standard | $0.004 | General tasks |
| bailian/qwen-turbo | Economy | $0.002 | Simple queries |

## Features

- ✅ Automatic model selection
- ✅ Query characteristic analysis
- ✅ Cost optimization
- ✅ Multi-provider support
- ✅ Context-aware routing

## Author

Franco

## License

MIT-0
