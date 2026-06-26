# OpenClaw Volcengine Skill

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Volcano Engine](https://img.shields.io/badge/Provider-Volcano%20Engine-orange)](https://www.volcengine.com/product/ark)

Official Volcano Engine (Volcengine) integration skill for OpenClaw. This skill enables seamless integration with Volcengine's AI models including Doubao Seed 2.0, GLM, DeepSeek V3.2, and Qwen through OpenAI-compatible API endpoints.

**Note**: Published as `volcano-engine` (original `volcengine` slug was already taken).

## Features

- **Multi-Model Support**: Doubao Seed 2.0 Pro/Lite/Mini/Code, GLM-4.7, DeepSeek V3.2, Qwen 3
- **Full Multimodal**: Text, image, and video input support
- **Full API Coverage**: Complete OpenAI-compatible API implementation
- **Security Best Practices**: API key quotas, permission controls, project isolation
- **Comprehensive Documentation**: Based on official Volcengine API + live API model list

## Quick Start

### 1. Install via ClawHub
```bash
clawhub install volcano-engine
```

**Note**: The slug `volcengine` was already taken, so this skill is published as `volcano-engine`.

### 2. Configure API Key
```bash
openclaw onboard --auth-choice volcengine-api-key
```

### 3. Test Connection
```bash
pwsh ./scripts/run-tests.ps1
```

## Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation and usage guide
- **[Configuration Guide](references/configuration.md)** - Detailed configuration options
- **[Models Reference](references/models.md)** - Complete model specifications
- **[API Parameters](references/api-parameters.md)** - Full API parameter reference
- **[Roadmap](ROADMAP.md)** - Development roadmap and future plans

## Supported Models

### LLM Models (Text Generation)
- `doubao-1-5-pro-32k-250115` - Doubao 1.5 Pro 32K (131K context, function calling)
- `glm-4-7-251222` - GLM-4.7 (200K context, 128K output)
- `deepseek-v3-2-251201` - DeepSeek V3.2 (131K context)
- `qwen3-32b-20250429` - Qwen 3 32B

### VLM Models (Text + Image + Video)
- `doubao-seed-2-0-pro-260215` - Doubao Seed 2.0 Pro (262K context, 131K output)
- `doubao-seed-2-0-lite-260215` - Doubao Seed 2.0 Lite (fast, balanced)
- `doubao-seed-2-0-mini-260215` - Doubao Seed 2.0 Mini (cost-efficient)
- `doubao-seed-2-0-code-preview-260215` - Doubao Seed 2.0 Code (code-optimized)

### Video & Image Generation
- `doubao-seedance-2-0-260128` - Seedance 2.0 (multimodal→video)
- `doubao-seedream-5-0-260128` - Seedream 5.0 (text→image)

> See [`models.md`](references/models.md) for the complete list including 3D, embedding, and third-party models.

## Scripts

- `scripts/run-tests.ps1` - Comprehensive test suite
- `scripts/test-connection.ps1` - Basic connection test
- `scripts/quick-start.ps1` - Quick setup and configuration
- `scripts/generate-config.ps1` - Generate OpenClaw configuration

## Development

```bash
# Clone repository
git clone https://github.com/openclaw/skills.git
cd skills/volcengine

# Run tests
npm test
# or
./scripts/run-tests.ps1 -ApiKey YOUR_API_KEY
```

## License

This skill is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## Support

- **Documentation**: [OpenClaw Docs](https://docs.openclaw.ai)
- **Community**: [Discord](https://discord.com/invite/clawd)
- **Issues**: [GitHub Issues](https://github.com/openclaw/skills/issues)

## Acknowledgments

- Volcano Engine for providing excellent AI services
- OpenClaw community for feedback and testing
- All contributors who helped improve this skill

---

**Skill Version**: 1.1.0  
**Last Updated**: 2026-04-25  
**OpenClaw Compatibility**: >=2026.4.0