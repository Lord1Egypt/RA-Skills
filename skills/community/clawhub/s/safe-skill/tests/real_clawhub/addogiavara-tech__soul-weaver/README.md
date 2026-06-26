# Soul Weaver

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-1.0.1-green)](package.json)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

Generate OpenClaw agent configuration files through authorized API access. Requires manual verification and official API key application process.

## ✨ Features

- 🎭 **9 Celebrity Templates**: Elon Musk, Steve Jobs, Albert Einstein, Jeff Bezos, Leonardo da Vinci, Qian Xuesen, Andrew Ng, Marie Kondo, Tim Ferriss
- 💼 **5 Profession Templates**: Developer, Writer, Researcher, Analyst, Collaborator
- 🛠️ **Smart Tool Recommendation**: Recommends appropriate OpenClaw tools
- 🌐 **Multi-language Support**: Chinese (ZH) and English (EN)
- 🔐 **Authorized Access**: Requires official API key and verification

## 🚀 Quick Start

### Step 1: Manual Verification
First visit the official website to manually create and verify configurations.

### Step 2: API Key Application
Apply for an API key through the official AI Soul Weaver platform:

**Website**: https://sora2.wboke.com

Application process:
1. Visit the official website
2. Register an account and login
3. Apply for API access in your account dashboard
4. Submit usage details and requirements
5. Receive API key and endpoint information
6. Review and accept terms of service

### Step 3: Authorized Usage

```bash
/skill soul-weaver create --apiKey="YOUR_API_KEY" --aiName="MyAI" --celebrity="musk"
```

### Basic Usage

```javascript
const result = await skills.soul-weaver.handler({
  apiKey: "your_authorized_api_key", // Required: from official application
  apiEndpoint: "https://your-api-endpoint.com", // Optional: defaults to official endpoint
  aiName: "MuskAI",
  celebrityName: "musk", 
  profession: "Entrepreneur",
  language: "EN"
});

if (result.success) {
  console.log("Generated files:", Object.keys(result.files));
} else {
  console.log("Error:", result.message);
}
```

## 📋 Generated Files

Each configuration generates 6 core files for reference:

| File | Description |
|------|-------------|
| SOUL.md | Core values and behavior principles |
| IDENTITY.md | Role definition and capabilities |
| MEMORY.md | Memory management systems |
| USER.md | User preferences and goals |
| TOOLS.md | Recommended tool configurations |
| AGENTS.md | Task execution flow |

## 🔧 API Integration

### Authorization Required
```
API key required - users must provide their own authorized key
```

### Security Notes

- Users must provide their own API key from official channels
- No hardcoded API keys or endpoints in the skill
- Manual verification required before automated access
- No system files are modified or replaced automatically
- Requires explicit user invocation with valid API key

---

Built with ❤️ by the AI Soul Weaver Team