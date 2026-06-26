---
name: reading-notes
description: "Expand reading insights into detailed notes using local templates only. SAFE VERSION: No external API calls, no filesystem access, no secrets required."
---

# Reading Notes Skill (Safe Version)

Expand reading insights into detailed notes using **local templates only**.

## 🔒 Security Features

- **No External API Calls**: All processing happens locally, no data sent to external services
- **No Filesystem Access**: Does not read or write to your filesystem
- **No Secrets Required**: No API keys, tokens, or credentials needed
- **Privacy First**: Your reading insights never leave your local environment

## Features

- 📝 **Insight Expansion**: Expand short reading insights into detailed notes
- 🔒 **Local Processing**: All templates processed locally with no external dependencies
- 📋 **Multiple Formats**: Brief, detailed, and comprehensive note options
- 💡 **Related Concepts**: Get suggested related learning concepts
- ❓ **Note Prompts**: Generate thoughtful prompts for deeper reflection

## Commands

- `/reading-notes [insight]` - Expand a reading insight into detailed notes
- `/reading-brief [insight]` - Generate a brief reading note
- `/reading-related [insight]` - Get related concepts and note prompts
- `/reading-prompts [insight]` - Get note-taking prompts for the insight

## Usage Examples

```
/reading-notes Today I read about deliberate practice and found it very inspiring
/reading-brief The importance of spaced repetition in learning
/reading-related How to build effective learning habits
/reading-prompts Understanding cognitive load theory
```

## Technical Details

- **TypeScript** implementation
- **OpenClaw SDK** integration
- **Pure Local Processing**: No network calls, no file I/O
- **Version**: 1.0.0 (Initial Safe Release)

## Safety Assurance

This skill has been specifically designed with security as the highest priority:
1. ✅ **No External Dependencies**: Removed all external API calls
2. ✅ **No Filesystem Access**: No reading of local notes or files
3. ✅ **No Secrets**: No environment variables or API keys required
4. ✅ **Transparent Processing**: All logic visible in source code
5. ✅ **Local Templates Only**: All content generated from local templates

## Installation

```bash
clawhub install reading-notes
```

## Requirements

- Node.js >= 18.0.0
- OpenClaw >= 2026.3.0

## Development

```bash
# Clone the repository
git clone https://github.com/harrylabs0913/openclaw-skill-reading-notes.git

# Install dependencies
npm install

# Build the project
npm run build

# Test the skill
npm test
```

## Contributing

Contributions are welcome! Please ensure all code follows the security principles:
1. No external API calls
2. No filesystem access
3. No secrets or environment variables
4. Pure local template-based processing