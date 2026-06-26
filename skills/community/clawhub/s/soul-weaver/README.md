# AI Soul Weaver

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-1.1.0-green)](package.json)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)
[![Templates](https://img.shields.io/badge/templates-12-orange)](SKILL.md)

**12 Celebrity Templates + Custom Generation** - Choose from 12 carefully selected world-famous personalities or create your own unique AI assistant configuration.

## ✨ Features

- 🎭 **12 Curated Celebrity Templates**: Tech pioneers, entrepreneurs, scientists, business leaders, and innovators
- 🔧 **10 Configuration Files**: Complete OpenClaw agent setup
- 💬 **Dialog-based Selection**: Natural language template selection
- 🛠️ **Local Template Access**: Works offline without API
- 🌐 **Multi-language Support**: Chinese (ZH) and English (EN)
- ⚡ **Rapid Deployment**: Quick setup and testing

## 🚀 Quick Start

### Method 1: Dialog Selection (Easiest)
```javascript
// Basic template selection
"I want to use Elon Musk template"
"Show me all templates"
"Create a custom AI assistant"

// Category-based selection  
"Show me tech templates"
"Which templates are for startups?"
"I need a science-themed assistant"
```

### Method 2: Direct API Specification
```javascript
const result = await skills.soulWeaver.handler({
  apiKey: 'sk-your-actual-token-here',  // Required: Your AI Soul Weaver Cloud API key
  apiEndpoint: 'https://sora2.wboke.com/api/v1/compile', // Official endpoint
  aiName: 'MyAI',
  templateId: 'elon-musk',      // Or other template IDs
  userName: 'User',
  language: 'EN' // or 'CN'
});
```

## 🔧 Implementation Strategies

### Strategy 1: Incremental Update (Recommended)
**Preserve your configuration while adding new capabilities**

1. **Backup** current configuration first!
2. Apply only `SOUL.md` from template (core mindset)
3. Apply `IDENTITY.md` from template (capabilities)  
4. Keep `USER.md`, `TOOLS.md`, `MEMORY.md` unchanged
5. Test and validate the fusion
6. Gradually apply other files if needed

### Strategy 2: Fusion Mode  
**Blend template features with your existing personality**

1. Analyze your current configuration
2. Identify key traits to preserve
3. Select complementary template features  
4. Create custom fusion configuration
5. Test and refine the blended personality

### Strategy 3: Full Replacement (Use with Caution)
**Complete template implementation**

1. Complete backup of all files
2. Apply all 10 template files
3. Manually restore critical personal settings
4. Test thoroughly 
5. Adjust as needed

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
- AGENTS.md (workflow rules)
- HEARTBEAT.md (checklist system)
```

## 📋 Generated Files

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

### For Leadership Roles:
1. Start with `zhang-yiming` or `simon-sinek`
2. Use incremental update for leadership qualities
3. Focus on team guidance

## ⚠️ Important Considerations

### Before Implementation:
- ✅ Always backup first
- ✅ Understand what each template changes
- ✅ Test in isolated environment if possible
- ✅ Have recovery plan ready

### During Implementation:
- 🔄 Apply changes gradually
- 👁️ Monitor for unexpected behavior
- 📊 Track performance changes
- 🔧 Be ready to adjust or revert

### After Implementation:
- 📈 Evaluate effectiveness
- 💬 Gather user feedback  
- ⚡ Optimize based on results
- 🎯 Refine the fusion

## 🆘 Troubleshooting

### Common Issues:
- Personality conflicts → Use fusion mode instead of full replacement
- Performance degradation → Revert and try incremental approach  
- Unexpected behavior → Check backup and restore if needed
- Feature mismatch → Choose different template better aligned with needs

### Recovery Procedures:
- Immediate restoration from backup
- Gradual rollback of changes
- Consultation with template characteristics
- Alternative template selection

---

**Remember**: The goal is enhancement, not replacement. Always preserve what works well while carefully adding new capabilities.

*Generated by AI Soul Weaver - Your partner in AI personality development*