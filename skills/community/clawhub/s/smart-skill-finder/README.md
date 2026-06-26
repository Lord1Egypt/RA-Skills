# Smart Skill Finder

A smart skill discovery tool that leverages OpenClaw's semantic understanding to find relevant skills across multiple ecosystems (Skills CLI, Clawhub, GitHub) and provide personalized recommendations.

## 🎯 Problem Solved

**Finding the right skill is hard because:**
- ❌ Current tools only search single ecosystems
- ❌ Basic keyword search misses relevant skills  
- ❌ No understanding of user intent or context
- ❌ Manual browsing is time-consuming and inefficient

**This skill provides the solution!**

## ✨ Key Features

### 🔍 **Smart Query Understanding**
- Uses OpenClaw's built-in semantic understanding to comprehend natural language queries
- Extracts problem domain, specific tasks, and relevant keywords automatically
- Understands complex requests like "I need something that prevents conversation hangs"

### 🌐 **Multi-Ecosystem Discovery** 
- Searches **Skills CLI** (581K+ skills) - most popular ecosystem
- Searches **Clawhub** (25K+ skills) - OpenClaw native skills  
- Searches **GitHub** repositories with agent-skill topics
- Aggregates results from all ecosystems into unified recommendations

### 🏆 **Smart Recommendations**
- Ranks skills by relevance to your specific query (0-100% score)
- Shows security verification status when available
- Provides clear installation commands for each ecosystem
- Limits to top 3-5 most relevant options to avoid overwhelming choices

### 🔒 **Safe by Design**
- Only provides installation commands - never executes them automatically
- Displays security status from VirusTotal and OpenClaw scanners
- Transparent about skill sources and ecosystem origins
- Graceful degradation if APIs are unavailable

## 🚀 Quick Start

### Installation
```bash
# Via Clawhub (recommended once published)
clawhub install edkuo7/smart-skill-finder

# Manual installation
git clone https://github.com/edkuo7/smart-skill-finder.git ~/.openclaw/skills/smart-skill-finder
```

### Basic Usage
Simply ask natural language questions about what you need:

```text
User: "How do I prevent my conversations from getting stuck?"

Agent: "I found some relevant skills for your needs:

🥇 conversation-flow-monitor (Clawhub)
   • Prevents conversations from getting stuck due to YAML front matter issues
   • Relevance: 94%
   • ✅ Security verified
   • Install: clawhub install edkuo7/conversation-flow-monitor

🥈 agent-browser (Skills CLI)  
   • Reliable browser automation with built-in timeout protection
   • Relevance: 87%
   • ✅ Security verified
   • Install: npx skills add vercel-labs/agent-browser@agent-browser

🥉 reliable-agent-guardian (GitHub)
   • General conversation reliability toolkit
   • Relevance: 82%  
   • ⚠️ Security scan pending
   • Install: git clone https://github.com/user/reliable-agent-guardian.git ~/.openclaw/skills/reliable-agent-guardian"
```

## 📋 Supported Ecosystems

| Ecosystem | Skills Available | Installation Method | Security Scanning |
|-----------|------------------|-------------------|-------------------|
| **Skills CLI** | 581K+ | `npx skills add <package>` | Basic validation |
| **Clawhub** | 25K+ | `clawhub install <author>/<skill>` | VirusTotal + OpenClaw |
| **GitHub** | 10K+ | `git clone <repo> ~/.openclaw/skills/<name>` | Community validation |

## 🛠️ Configuration

The skill uses sensible defaults but can be configured via `config.json`:

```json
{
  "max_results": 3,
  "ecosystem_priority": ["skills_cli", "clawhub", "github"],
  "timeout_seconds": 10,
  "enable_github_search": true
}
```

## 🧪 Examples

### 1. Conversation Reliability
```text
User: "My conversations keep hanging during browser automation"

Response: Recommends conversation-flow-monitor, agent-browser, and related skills
```

### 2. Document Processing  
```text
User: "I need to work with PDF files and extract text"

Response: Recommends pdf skill, document-processing tools, and related utilities
```

### 3. Error Handling
```text
User: "How do I make my agent more reliable and handle errors better?"

Response: Recommends self-improving-agent, error-handling patterns, and monitoring tools
```

## 🔧 Integration with OpenClaw

### Workspace Awareness
- Reads your existing skills to avoid duplicates
- Considers your project context and domain
- Learns from your preferences over time

### Memory Integration  
- Can reference past skill discovery conversations
- Builds knowledge of your preferred ecosystems
- Adapts recommendations based on feedback

## 📈 Performance Impact

- **Minimal overhead**: <1% performance impact
- **Fast responses**: Typically 3-8 seconds for complete search
- **Lightweight**: ~22KB total code size
- **Efficient**: Stops searching once good results are found

## 🛡️ Best Practices

1. **Always review skills** before installing - check security status and source
2. **Start with official skills** from verified authors (Vercel Labs, Anthropic, Microsoft)
3. **Test in isolation** before using in production workflows
4. **Provide feedback** to help improve recommendation quality

## 🤝 Contributing

This skill follows OpenClaw best practices. If you discover new skill ecosystems or improvement opportunities:

1. Log findings to `.learnings/FEATURE_REQUESTS.md`
2. Consider creating enhancement PRs for ecosystem support
3. Share successful use cases to improve query understanding

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

**💡 Pro Tip**: This skill works best when combined with other reliability-focused skills like `conversation-flow-monitor` and `self-improving-agent` for comprehensive agent capabilities!