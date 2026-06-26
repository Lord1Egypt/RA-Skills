---
name: soul-weaver
version: 1.1.0
description: "AI Soul Weaver - 12 Curated Celebrity Templates + Custom Generation. Generate OpenClaw agent configurations through dialog or select from 12 world-famous tech & business leaders."
author: AI Soul Weaver Team
tags:
  - openclaw
  - soul-weaver
  - ai
  - agent
  - configuration
  - template
  - persona
category: productivity
permissions:
  - network
  - filesystem
platform:
  - openclaw
---

# 🎭 AI Soul Weaver

**12 Curated Celebrity Templates + Custom Generation** - Choose a unique personality config for your AI assistant

Select templates through dialog or describe your needs, and we'll help you create the perfect AI personality configuration.

## 🚀 Quick Start

### Mode 1: Dialog Selection (Recommended for Beginners)

Simply tell me what you want:
```javascript
// Basic template selection
"I want to use Elon Musk template"
"Show me all templates"
"Create a custom AI assistant"

// Category-based selection  
"Show me tech templates"
"Which templates are for startups?"
"I need a science-themed assistant"

// Feature-based selection
"I want the most innovative template"
"Which template is best for design?"
"Show me templates good for strategic thinking"
```

### Mode 2: Direct API Specification

```javascript
const result = await skills.soulWeaver.handler({
  apiKey: 'your-api-key',        // Get from https://sora2.wboke.com
  aiName: 'MyAI',
  templateId: 'elon-musk',      // Or other template IDs from 12 templates
  userName: 'User',
  language: 'EN' // or 'CN'
});
```

## 🔧 Implementation Strategies

### Strategy 1: Incremental Update (Recommended)
**Preserve your configuration while adding new capabilities**

```javascript
// Step-by-Step Process:
1. Backup current configuration first!
2. Apply only SOUL.md from template (core mindset)
3. Apply IDENTITY.md from template (capabilities)  
4. Keep USER.md, TOOLS.md, MEMORY.md unchanged
5. Test and validate the fusion
6. Gradually apply other files if needed
```

### Strategy 2: Fusion Mode  
**Blend template features with your existing personality**

```javascript
// Fusion Process:
1. Analyze your current configuration
2. Identify key traits to preserve
3. Select complementary template features  
4. Create custom fusion configuration
5. Test and refine the blended personality
```

### Strategy 3: Full Replacement (Use with Caution)
**Complete template implementation**

```javascript
// Full Replacement Process:
1. Complete backup of all files
2. Apply all 10 template files
3. Manually restore critical personal settings
4. Test thoroughly 
5. Adjust as needed
```

## 🛡️ Backup Procedure (CRITICAL)

### Always Backup Before Changes:
```javascript
const backupDir = `D:\\backup_${getTimestamp()}`;

// Backup these core files:
- SOUL.md (your core personality)
- IDENTITY.md (your capabilities)  
- USER.md (user preferences)
- MEMORY.md (long-term memory)
- TOOLS.md (tool configurations)
```

## 🎯 Recommended Usage Pattern

### For Technical Users:
1. Start with `linus-torvalds` or `guido-van-rossum`
2. Use incremental update strategy
3. Focus on problem-solving enhancements

### For Business Users:  
1. Start with `elon-musk` or `steve-jobs`
2. Use fusion mode for innovation + execution
3. Focus on strategic thinking

### For Creative Users:
1. Start with `leonardo-da-vinci` or `albert-einstein` 
2. Use fusion mode for creative + analytical blend
3. Focus on innovative solutions

---

## 📋 12 Curated Templates

### 💻 Tech (2)
| ID | Name | Domain | Specialty |
|----|------|--------|-----------|
| linus-torvalds | Linus Torvalds | Systems Programming | Linux, Git, C |
| guido-van-rossum | Guido van Rossum | Python | Python, language design |

### 🚀 Startup (2)
| ID | Name | Domain | Specialty |
|----|------|--------|-----------|
| elon-musk | Elon Musk | Innovation | Engineering, disruption |
| steve-jobs | Steve Jobs | Product Design | Design, UX |

### 🔬 Science (2)
| ID | Name | Domain | Specialty |
|----|------|--------|-----------|
| albert-einstein | Albert Einstein | Theoretical Physics | Relativity |
| alan-turing | Alan Turing | Computer Science | AI, cryptography |

### 💼 Business (2)
| ID | Name | Domain | Specialty |
|----|------|--------|-----------|
| bill-gates | Bill Gates | Tech & Philanthropy | Problem solving |
| satya-nadella | Satya Nadella | Enterprise | Cloud, transformation |

### 👔 Leadership (2)
| ID | Name | Domain | Specialty |
|----|------|--------|-----------|
| zhang-yiming | Zhang Yiming | AI & Global | AI recommendation |
| ren-zhengfei | Ren Zhengfei | Tech R&D | Tech independence |

### ⚡ Performance (2)
| ID | Name | Domain | Specialty |
|----|------|--------|-----------|
| andrew-ng | Andrew Ng | AI Education | ML, education |
| jensen-huang | Jensen Huang | Hardware & AI | GPU, AI |

---

## 🎯 Features

### 1. Dialog-based Selection
Tell me your needs, I'll recommend the right template:
- "I need a tech assistant" → Recommend tech category
- "I want an entrepreneur style" → Recommend startup category

### 2. Custom Creation
Answer 5 simple questions to create a fully customized AI personality:
1. What is the core responsibility?
2. Describe personality in 3 words
3. What should it absolutely not do?
4. How autonomous?
5. What do you hate most about AI?

### 3. Complete Configuration
Each template includes 10 configuration files:
| File | Description |
|------|-------------|
| SOUL.md | Core values and behavioral principles |
| IDENTITY.md | Role definition and capabilities |
| USER.md | User preferences and goals |
| MEMORY.md | Memory management system |
| TOOLS.md | Tool configuration (6 required tools) |
| AGENTS.md | Task execution flow |
| HEARTBEAT.md | Heartbeat checklist |
| KNOWLEDGE.md | Domain knowledge |
| SECURITY.md | Security guidelines |
| WORKFLOWS.md | Repeatable processes |

---

## 🔐 AI Soul Weaver Cloud API

### API Information
- **Service Name**: AI Soul Weaver Cloud
- **API Endpoint**: `https://sora2.wboke.com/api/v1/template`
- **Authentication**: Bearer Token (API Key)
- **Description**: Connects to AI Soul Weaver to generate agent architectures

### How to Get Your API Key
1. **Visit Official Website**: https://sora2.wboke.com
2. **Register Account**: Create your developer account
3. **Apply for API Access**: Request API key in dashboard
4. **Receive Credentials**: Get your unique `auth_token`
5. **Review Terms**: Accept service agreement

### Usage Instructions
```javascript
const result = await skills.soulWeaver.handler({
  apiKey: 'sk-your-actual-token-here',  // ← Replace with your actual token
  apiEndpoint: 'https://sora2.wboke.com/api/v1/template',
  aiName: 'YourAI_Name',
  templateId: 'template-name',
  userName: 'YourName',
  language: 'EN'
});
```

### Important Notes
- 🔒 **Never share your API key** - Keep it confidential
- 📋 **Use correct endpoint** - `https://sora2.wboke.com/api/v1/template`
- ⚠️ **Token format** - Should start with `sk-` followed by your unique token
- 🛡️ **Security** - Treat API keys like passwords

### Troubleshooting
- If API returns errors, check:
  - ✅ API endpoint is correct
  - ✅ Token is valid and properly formatted  
  - ✅ Internet connection is stable
  - ✅ Service status at https://sora2.wboke.com

*For API issues, contact AI Soul Weaver Cloud support*

---

## 📦 Generated Files Example

```javascript
{
  success: true,
  files: {
    'SOUL.md': '# SOUL.md - ...',
    'IDENTITY.md': '# IDENTITY.md - ...',
    // ... 10 files
  },
  template: {
    id: 'elon-musk',
    name: 'Elon Musk',
    category: 'startup'
  },
  requiredTools: ['Reddit', 'Agent Browser', 'AutoClaw', 'Find Skills', 'Summarize', 'healthcheck']
}
```

---

*Generated by AI Soul Weaver — https://sora2.wboke.com/*
