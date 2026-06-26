# OpenClaw Soul Weaver

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](package.json)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

🚀 No waiting! Create professional-grade OpenClaw configurations in 30 seconds through natural conversation.

Instantly generate enthusiast-level base configurations that intelligently combine emotional and professional needs. Replace system files to instantly professionalize your OpenClaw with expertly crafted skills, memory management, and file configurations.

Create personalized AI Agent configurations with unique **identities**, **souls**, **memories**, and **tools**. Design AI personalities inspired by famous minds or professions.

## ✨ Features

- 🎭 **9 Celebrity Templates**: Elon Musk, Steve Jobs, Albert Einstein, etc.
- 💼 **5 Profession Templates**: Developer, Writer, Researcher, Analyst, Collaborator
- 🛠️ **Smart Tool Recommendation**: Auto-includes required OpenClaw tools
- 🌐 **Multi-language Support**: Chinese (ZH) and English (EN)
- 🎨 **Avatar Generation**: Optional AI avatar creation
- 📦 **ZIP Export**: Complete configuration package

## 🚀 Quick Start

### Installation
```bash
clawhub install openclaw-soul-weaver
```

### Basic Usage
```javascript
// Create an AI like Elon Musk
const result = await skills.openclaw-soul-weaver.handler({
  aiName: "MuskAI",
  celebrityName: "musk",
  profession: "Entrepreneur",
  language: "EN"
});

if (result.success) {
  console.log("Generated files:", Object.keys(result.files));
  console.log("ZIP package:", result.zip.length, "bytes");
}
```

### Command Line
```bash
# List available templates
/skill openclaw-soul-weaver list-templates

# Create AI configuration
/skill openclaw-soul-weaver create --aiName="MyAI" --celebrity="musk"
```

## 📋 Templates

### Celebrity Templates
| Name | Description | Key Traits |
|------|-------------|------------|
| Elon Musk | Innovation, First Principles | musk |
| Steve Jobs | Design, Perfectionism | jobs |
| Albert Einstein | Science, Curiosity | einstein |
| Jeff Bezos | Customer Obsession | bezos |
| Leonardo da Vinci | Creativity, Multidisciplinary | da_vinci |
| Qian Xuesen | Systems Engineering | qianxuesen |
| Andrew Ng | AI/ML, Education | ng |
| Marie Kondo | Minimalism, Organization | kondo |
| Ferris Buelli | Enthusiasm, Time Management | ferris |

### Profession Templates
| Name | Description | Key Traits |
|------|-------------|------------|
| Developer | Technical Expertise | developer |
| Writer | Content Creation | writer |
| Researcher | Analysis, Discovery | researcher |
| Analyst | Data-driven Insights | analyst |
| Collaborator | Team Coordination | collaborator |

## 🔧 API Reference

### Main Handler
```javascript
async function handler(params: {
  aiName?: string;           // AI name (default: "AI Assistant")
  userName?: string;         // User name (default: "User")
  profession?: string;       // User profession
  useCase?: string;         // Use case description
  communicationStyle?: string; // Communication style
  celebrityName?: string;   // Celebrity template name
  language?: string;        // "ZH" or "EN" (default: "ZH")
  generateAvatar?: boolean; // Generate avatar (default: true)
}): Promise<{
  success: boolean;
  files: Record<string, string>; // Generated config files
  zip: string;                  // Base64 encoded ZIP package
  template: { id: string };    // Used template
  error?: string;              // Error message if failed
}>
```

### Utility Functions
```javascript
// List available templates
function listTemplates(): {
  celebrity: string[];
  profession: string[];
  requiredTools: string[];
}

// Validate parameters
function validateParams(params: any): {
  valid: boolean;
  errors: string[];
}
```

## 📁 Generated Files

Each configuration generates 6 core files:

| File | Description |
|------|-------------|
| `SOUL.md` | Core values, thinking patterns, behavior principles |
| `IDENTITY.md` | Role definition, capabilities, communication style |
| `MEMORY.md` | Short-term memory, long-term memory, session management |
| `USER.md` | User preferences, habits, goals |
| `TOOLS.md` | Tool configuration (auto-includes required tools) |
| `AGENTS.md` | Task execution flow, decision logic |

## ⚙️ Configuration

### Required Permissions
- `network`: API calls to generation service
- `file-write`: Save generated configurations
- `file-read`: Read template references

### Automatic Triggers
Triggers automatically when user says:
- "create ai agent"
- "generate soul"
- "make AI like [celebrity]"
- "设计AI助手"
- "创建数字灵魂"

## 🎨 Avatar Generation

Optional avatar generation with customizable styles:

```javascript
// Generate tech-style avatar
const avatar = await generateAvatar("TechAI", "tech");

// Available styles: tech, professional, creative, friendly, minimalist
```

## 🔍 Error Handling

### Common Errors
- `API_ERROR`: Generation service unavailable
- `VALIDATION_ERROR`: Invalid template or parameters
- `NETWORK_ERROR`: Connection issues

### Fallback Options
1. Visit https://sora2.wboke.com/ for manual creation
2. Provide more detailed requirements
3. Use default templates

## 📊 Examples

### Example 1: Celebrity-based AI
```javascript
const result = await handler({
  aiName: "InnovationAI",
  celebrityName: "musk",
  profession: "Technology Innovator",
  language: "EN",
  generateAvatar: true
});
```

### Example 2: Profession-based AI
```javascript
const result = await handler({
  aiName: "DevAssistant",
  profession: "developer",
  useCase: "Coding assistance and code review",
  communicationStyle: "Technical",
  language: "ZH"
});
```

## 🌐 Related Resources

- **API Endpoint**: https://sora2.wboke.com/api/v1/generate
- **Online Creation**: https://sora2.wboke.com/
- **Skill Market**: https://clawhub.ai
- **Documentation**: See `SKILL.md` for detailed documentation

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 🐛 Bug Reports

Please report bugs on the [GitHub Issues](https://github.com/anomalyco/ai-soul-weaver/issues) page.

---

Built with ❤️ by the AI Soul Weaver Team