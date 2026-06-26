# Talk Analyzer

**AI-Powered Business Conversation Analysis**

Transform raw conversation data into actionable business intelligence. Automatically extract summaries, action items, decisions, and strategic insights from meetings, sales calls, and customer interactions.

---

## 🎯 What It Does

Talk Analyzer uses AI (Claude, GPT) to analyze business conversations and generate:

- **Meeting Summaries** - Key points, decisions, and action items
- **Sales Insights** - Objections, opportunities, and next steps
- **Support Quality** - Sentiment analysis and resolution assessment
- **Strategic Recommendations** - Data-driven follow-up suggestions
- **Speaker Analysis** - Individual participation and engagement metrics

---

## ✨ Key Features

### Multiple Analysis Types
- 📊 **Meeting** - Extract decisions and action items
- 💰 **Sales** - Identify objections and buying signals
- 🎧 **Support** - Evaluate service quality and satisfaction
- 🤝 **Negotiation** - Analyze positions and strategies
- 👥 **Interview** - Assess qualifications and fit
- 📝 **General** - Analyze any conversation

### Intelligent Extraction
- ✅ Automatic action item detection with owners and deadlines
- 💭 Sentiment analysis per participant
- 🎯 Topic detection and frequency tracking
- 📈 Trend analysis across multiple conversations
- 🔍 Custom focus areas (pricing, timeline, technical details, etc.)

### Flexible Output
- 📄 JSON format for programmatic use
- 📝 Markdown format for human reading
- 🔄 Batch processing for multiple files
- 📊 Comparison reports across conversations

---

## 🚀 Quick Start

### Installation

```bash
# Clone from GitHub
git clone https://github.com/ZhenRobotics/openclaw-talk-analyzer.git
cd openclaw-talk-analyzer
npm install

# Or install from npm (after publication)
npm install -g openclaw-talk-analyzer
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Add your AI API key (choose one)
ANTHROPIC_API_KEY=your-claude-api-key
# OR
OPENAI_API_KEY=your-openai-api-key
```

Get API keys:
- **Claude**: https://console.anthropic.com/
- **OpenAI**: https://platform.openai.com/api-keys

### First Analysis

```bash
# Analyze a meeting
openclaw-talk analyze \
  --input meeting.txt \
  --type meeting \
  --sentiment

# Analyze a sales call
openclaw-talk analyze \
  --input sales-call.txt \
  --type sales \
  --focus "objections,pricing,timeline" \
  --output report.json
```

---

## 💻 Usage Examples

### Basic Analysis

```bash
openclaw-talk analyze \
  --input conversation.txt \
  --type meeting
```

### Detailed Analysis with Speakers

```bash
openclaw-talk analyze \
  --input team-discussion.txt \
  --type meeting \
  --speakers "Alice,Bob,Charlie" \
  --sentiment \
  --detailed \
  --output detailed-report.json
```

### Batch Processing

Create `batch-config.json`:
```json
{
  "files": [
    {
      "input": "meeting-2024-03-01.txt",
      "type": "meeting",
      "speakers": ["Alice", "Bob"]
    },
    {
      "input": "sales-call-acme.txt",
      "type": "sales",
      "focus": ["objections", "pricing"]
    }
  ],
  "options": {
    "sentiment": true,
    "detailed": true
  }
}
```

Run batch analysis:
```bash
openclaw-talk batch --config batch-config.json --output-dir ./reports/
```

### Compare Conversations

```bash
openclaw-talk compare \
  --inputs "call1.txt,call2.txt,call3.txt" \
  --type sales \
  --output comparison-report.md
```

---

## 📊 Output Example

### Meeting Analysis Result

```json
{
  "type": "meeting",
  "summary": "Team discussed Q2 product roadmap and resource allocation. Decided to prioritize mobile app launch by end of April.",
  "key_points": [
    "Mobile app 70% complete",
    "Need 2 weeks for push notifications",
    "Beta testing with 50-100 users planned",
    "Marketing budget approved: $30,000"
  ],
  "action_items": [
    {
      "task": "Set up beta program",
      "owner": "Bob",
      "deadline": "Tomorrow",
      "priority": "high"
    },
    {
      "task": "Draft marketing strategy",
      "owner": "Charlie",
      "deadline": "Friday",
      "priority": "high"
    }
  ],
  "decisions": [
    {
      "decision": "Launch iOS and Android simultaneously",
      "made_by": "Alice",
      "rationale": "User base is evenly split"
    }
  ],
  "sentiment": {
    "overall": "positive",
    "participants": {
      "Alice": {"sentiment": "positive", "engagement_level": "high"},
      "Bob": {"sentiment": "neutral", "engagement_level": "medium"},
      "Charlie": {"sentiment": "positive", "engagement_level": "high"}
    }
  }
}
```

---

## 🎯 Use Cases

### 1. Sales Teams
- Analyze calls to identify objection patterns
- Track buying signals and urgency indicators
- Generate data-driven follow-up strategies
- Compare successful vs unsuccessful calls

### 2. Product Managers
- Extract feature requests from user interviews
- Identify common pain points across conversations
- Prioritize roadmap based on customer feedback
- Track sentiment trends over time

### 3. Customer Success
- Monitor support conversation quality
- Evaluate agent performance objectively
- Identify at-risk customers early
- Improve training based on conversation analysis

### 4. Executives
- Get meeting summaries without attending
- Track team decision patterns
- Identify strategic opportunities from customer conversations
- Monitor team engagement and morale

---

## 🛠️ Available Commands

```bash
# Analyze single conversation
openclaw-talk analyze [options]

# Batch process multiple files
openclaw-talk batch --config <file>

# Compare multiple conversations
openclaw-talk compare --inputs <files>

# List available AI engines
openclaw-talk engines

# View analysis history
openclaw-talk history
```

**Command Aliases:**
- `openclaw-talk` - Primary command
- `talk-analyzer` - Alternative command
- `talkz` - Quick shorthand

---

## 🔧 Configuration Options

### Analysis Options
- `--type` - Analysis type (meeting, sales, support, negotiation, interview, general)
- `--input` - Input conversation file path
- `--output` - Output file path (optional, defaults to stdout)
- `--format` - Output format (json, markdown)
- `--sentiment` - Enable sentiment analysis
- `--speakers` - Comma-separated list of speaker names
- `--focus` - Specific aspects to focus on (comma-separated)
- `--detailed` - Include detailed analysis and quotes
- `--model` - AI model to use (claude-sonnet-4, gpt-4, etc.)

---

## 📚 Documentation

- **Full README**: [GitHub Repository](https://github.com/ZhenRobotics/openclaw-talk-analyzer)
- **Quick Start Guide**: See QUICKSTART.md in repository
- **Example Files**: Sample conversations included in `examples/` directory
- **API Documentation**: TypeScript definitions in `src/core/types.ts`

---

## 🔐 Privacy & Security

- **No Data Storage**: Conversations are not stored on external servers (except when using cloud AI APIs)
- **Local Processing**: Support for local LLM models for sensitive conversations
- **API Key Security**: Keys stored locally in `.env` file, never committed to version control
- **GDPR Compliant**: Designed with privacy regulations in mind

---

## 🌟 Why Choose Talk Analyzer?

### Compared to Manual Summarization
- ⚡ **10x Faster** - Analyze in seconds vs. 30+ minutes manual work
- 🎯 **More Consistent** - No human bias or fatigue
- 📊 **Structured Output** - Ready for database/CRM integration
- 🔄 **Scalable** - Process hundreds of conversations easily

### Compared to Generic AI Tools
- 🎯 **Purpose-Built** - Optimized for business conversations
- 📋 **Structured Results** - JSON output with typed fields
- 🔧 **Customizable** - Focus on specific aspects relevant to your business
- 🚀 **CLI & API** - Easily integrate into workflows

---

## 🛣️ Roadmap

### v1.1.0 (Coming Soon)
- Real-time audio transcription integration
- PDF report generation
- Web dashboard for visualization
- Local LLM support (Ollama)

### v1.2.0 (Planned)
- Multi-language support
- CRM integrations (Salesforce, HubSpot)
- Slack/Teams bot integration
- Advanced analytics dashboard

### v2.0.0 (Future)
- Team collaboration features
- Custom analysis templates
- API webhooks for automation
- Enterprise features (SSO, RBAC)

---

## 🤝 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/ZhenRobotics/openclaw-talk-analyzer/issues)
- **Documentation**: [Full docs and guides](https://github.com/ZhenRobotics/openclaw-talk-analyzer#readme)
- **Examples**: Check the `examples/` directory for sample conversations

---

## 📄 License

MIT License - Free for personal and commercial use

---

## 🚀 Getting Started Checklist

- [ ] Install Node.js 18+ and npm
- [ ] Clone repository or install from npm
- [ ] Get API key from Claude or OpenAI
- [ ] Configure `.env` file with API key
- [ ] Try analyzing example conversation files
- [ ] Analyze your own conversation transcripts
- [ ] Explore batch processing for multiple files
- [ ] Integrate into your workflow

---

## 📝 Example Conversation Format

For best results, format your conversation files like this:

```
Alice: Hi everyone, thanks for joining today's meeting.

Bob: Happy to be here. Let's discuss the project timeline.

Charlie: I think we can launch by end of Q2 if we focus on core features.

Alice: Agreed. Bob, can you lead the technical planning?

Bob: Sure, I'll have a proposal ready by Friday.
```

---

## 💡 Tips for Best Results

1. **Clear Speaker Attribution** - Use consistent speaker names
2. **Minimum Length** - At least 50 characters for meaningful analysis
3. **Context Matters** - Provide background in metadata or focus parameters
4. **Specific Focus** - Use `--focus` to highlight important aspects
5. **Review Output** - AI analysis is highly accurate but review for critical decisions

---

**Transform your conversations into actionable intelligence with AI!**

For more information, visit: https://github.com/ZhenRobotics/openclaw-talk-analyzer
