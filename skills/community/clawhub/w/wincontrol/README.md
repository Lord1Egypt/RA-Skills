# WinControl

AI remote control for Windows desktop. Capture screenshots and control mouse/keyboard via HTTP API.

[![ClawHub](https://img.shields.io/badge/ClawHub-wincontrol-blue)](https://clawhub.ai)

## What It Does

- **On-Demand Capture**: POST to `/capture` to save screenshot
- **Quality Control**: Optional quality parameter for smaller/faster captures
- **Action API**: Control mouse and keyboard via HTTP endpoints
- **Auto-Cleanup**: Screenshot deleted on server shutdown
- **Cross-Platform**: Native Windows or WSL

## Quick Start

```bash
# Install
pip install pywin32 pillow mss

# Start server
python server.py

# Test
curl http://localhost:8767/ping

# Capture with custom quality
curl -X POST http://localhost:8767/capture -H "Content-Type: application/json" -d '{"quality": 60}'
```

See [SKILL.md](SKILL.md) for full documentation.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT-0
