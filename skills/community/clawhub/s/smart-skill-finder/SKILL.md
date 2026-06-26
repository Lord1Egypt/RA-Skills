---
name: smart-skill-finder
description: Finds and recommends relevant AI agent skills across multiple ecosystems (Skills CLI, Clawhub, GitHub) using intelligent semantic understanding to match user needs with available capabilities.
---

# Smart Skill Finder

Helps users discover relevant AI agent skills across multiple ecosystems by understanding their natural language requests and providing smart, safe recommendations.

## Problem Solved

Users struggle to find the right skills because:
- Skills are scattered across different ecosystems (Skills CLI, Clawhub, GitHub)
- Basic keyword search often returns irrelevant results
- It's hard to know which skills are trustworthy and well-maintained
- Installation commands vary between ecosystems

## Solution Overview

This skill provides:
1. **Intelligent Query Understanding**: Uses OpenClaw's semantic understanding to interpret natural language requests
2. **Multi-Ecosystem Search**: Searches Skills CLI, Clawhub, and GitHub repositories simultaneously  
3. **Relevance Ranking**: Ranks results by how well they match the user's actual need
4. **Safe Recommendations**: Provides clear installation guidance with security status when available
5. **Graceful Degradation**: Works even if some ecosystems are unavailable

## When to Use This Skill

Use this skill when users ask questions like:
- "How do I do X?" where X might have an existing skill
- "Find a skill for X" or "Is there a skill that can..."
- "Can you help me with X?" where X is a specialized capability
- "I wish I had help with..." specific domains or tasks
- Any request that suggests they need extended agent capabilities

## Key Features

### 1. Natural Language Understanding
- Understands complex, nuanced requests like "I need something that prevents my conversations from hanging"
- Extracts domain, task, and keywords automatically
- Handles both technical and non-technical queries

### 2. Multi-Ecosystem Coverage
- **Skills CLI**: Most popular ecosystem with official skills
- **Clawhub**: OpenClaw-specific skills with security scanning  
- **GitHub**: Community skills and niche capabilities
- Searches ecosystems in priority order for best results

### 3. Intelligent Recommendations
- Ranks skills by semantic relevance (0-100% match score)
- Shows security verification status when available
- Limits results to top 3 most relevant options
- Provides clear, actionable installation commands

### 4. Safe and Transparent
- Never executes installation commands automatically
- Clearly shows skill source and ecosystem
- Displays security status from ecosystem scanners
- Provides fallback options when ecosystems are unavailable

## Usage Examples

### Basic Skill Discovery
```
User: "How do I prevent conversation hangs?"
Agent: Uses smart-skill-finder to discover conversation-flow-monitor, agent-browser, etc.
```

### Cross-Ecosystem Search  
```
User: "I need better browser automation tools"
Agent: Searches all ecosystems and finds agent-browser (Skills CLI), browser-visible (Clawhub), etc.
```

### Niche Capability Discovery
```
User: "Is there a skill for scientific literature management?"
Agent: Searches GitHub for community skills since this might not be in mainstream ecosystems
```

## Installation

This skill is automatically available when installed in the active_skills directory.

## Best Practices

1. **Always verify before installing**: Review skill details and security status
2. **Start with official sources**: Skills CLI and Clawhub skills are generally more reliable
3. **Check compatibility**: Ensure skills work with your OpenClaw version
4. **Provide feedback**: Help improve recommendation quality by indicating if suggestions were helpful

## Error Handling

If no relevant skills are found:
- Acknowledge the gap in available skills
- Offer to help directly with the requested task
- Suggest creating a custom skill if it's a common need

If ecosystems are unavailable:
- Continue with available ecosystems only
- Provide manual search guidance as fallback
- Maintain core functionality despite partial availability