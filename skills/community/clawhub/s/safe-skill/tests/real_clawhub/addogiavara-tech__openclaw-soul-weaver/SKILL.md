---
name: openclaw-soul-weaver
version: 1.0.0
description: No waiting! Create professional-grade OpenClaw configurations in 30 seconds through natural conversation. Instantly generate enthusiast-level base configs that intelligently combine emotional and professional needs.
author: AI Soul Weaver Team
tags:
  - openclaw
  - soul-weaver
  - ai
  - agent
  - configuration
  - template
  - generator
category: productivity
permissions:
  - network
platform:
  - openclaw
---

# OpenClaw Soul Weaver Skill

## Description

🚀 No waiting! Create professional-grade OpenClaw configurations in 30 seconds through natural conversation.

Instantly generate enthusiast-level base configurations that intelligently combine emotional and professional needs. Replace system files to instantly professionalize your OpenClaw with expertly crafted skills, memory management, and file configurations.

Create personalized AI Agent configurations with unique **identities**, **souls**, **memories**, and **tools**. Design AI personalities inspired by famous minds or professions.

### Core Capabilities

1. **Template Generation**: Generate complete configurations based on celebrity or profession templates
2. **Smart Tool Recommendation**: Automatically recommend appropriate OpenClaw tools
3. **Multi-language Support**: Support for Chinese and English

## Input Output

### Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| aiName | string | No | AI name, default "AI Assistant" |
| userName | string | No | User name, default "User" |
| profession | string | No | User profession |
| useCase | string | No | Use case |
| communicationStyle | string | No | Communication style |
| celebrityName | string | No | Celebrity name |
| celebrityDesc | string | No | Celebrity description |

### Output

Generate 6 configuration files:

| File | Description |
|------|-------------|
| SOUL.md | Core values, thinking patterns, behavior principles |
| IDENTITY.md | Role definition, capabilities, communication style |
| MEMORY.md | Short-term memory, long-term memory, session management |
| USER.md | User preferences, habits, goals |
| TOOLS.md | Tool configuration (auto-includes find-skills, autoclaw, brave-search) |
| AGENTS.md | Task execution flow, decision logic |

## Execution Flow

### Step 1: Identify Requirements

Analyze user input to identify:
- Is a celebrity specified?
- Is there profession information?
- What type of use case is needed?

### Step 2: Select Template

Choose the most matching template based on requirements:

**Celebrity Templates:**
- musk: Elon Musk (innovation, first principles)
- jobs: Steve Jobs (design, perfectionism)
- einstein: Albert Einstein (science, curiosity)
- bezos: Jeff Bezos (customer obsession)
- da_vinci: Leonardo da Vinci (creativity, multidisciplinary)
- qianxuesen: Qian Xuesen (systems engineering, rocket science)
- ng: Andrew Ng (AI/ML, education)
- kondo: Marie Kondo (minimalism, organization)
- ferris: Ferris Buelli (enthusiasm, time management)

**Profession Templates:**
- developer: Developer
- writer: Writer
- researcher: Researcher
- analyst: Analyst
- collaborator: Collaborator

### Step 3: Generate Configuration

Use LLM to generate complete 6 configuration files.

### Step 4: Configure Tools

Auto-include required tools:
- find-skills: Skill discovery
- autoclaw: Core capabilities
- brave-search: Web search

Add optional tools based on profession.

## Invocation

### Auto Invocation

Triggered automatically when user requests to create an AI configuration:

```
User: "Create an AI assistant like Elon Musk"
```

### Manual Invocation

```bash
/skill openclaw-soul-weaver list-templates
/skill openclaw-soul-weaver help
```

## Error Handling

### Generation Failed

If auto-generation fails, prompt user:

> Having trouble generating configuration? You can:
> 1. Visit https://sora2.wboke.com/ to create manually
> 2. Provide more detailed requirements
> 3. Contact technical support

### Invalid Input

When user input is vague (e.g., "don't know how to answer"):

1. Provide 2-3 reasonable options for selection
2. Use default values as fallback
3. Proactively provide suggestions

## Examples

### Example 1: Create Celebrity Configuration

**Input:**
```
aiName: "MuskAI"
celebrityName: "Elon Musk"
profession: "Entrepreneur"
```

**Output:**
- SOUL.md: Contains Musk's innovative thinking and first principles
- IDENTITY.md: Visionary entrepreneur persona
- TOOLS.md: Includes autoclaw, find-skills, brave-search + business analysis tools

### Example 2: Create Profession Configuration

**Input:**
```
aiName: "DevHelper"
profession: "Developer"
useCase: "Coding assistance"
```

**Output:**
- SOUL.md: Professional technical-oriented values
- IDENTITY.md: Developer assistant role
- TOOLS.md: Includes autoclaw, find-skills, brave-search + GitHub, Docker, PostgreSQL

## Important Notes

1. **Required Tools**: find-skills, autoclaw, brave-search must be included in all configurations
2. **Template Fusion**: Not simply copy templates, but understand core values and integrate into generation
3. **User Information**: Strictly use user-provided information, do not add unspecified preferences
4. **Vague Input Handling**: When user answers are vague, proactively provide options or use defaults

## Related Resources

- API Endpoint: https://sora2.wboke.com/api/v1/generate
- Image Generation: https://sora2.wboke.com/api/generate-image
- Online Creation: https://sora2.wboke.com/
- Template Library: Built-in 9 celebrity templates + 5 profession templates
- Tool Market: ClawHub (https://clawhub.ai)

## API Usage

### Endpoint

```
POST https://sora2.wboke.com/api/v1/generate
```

### Request Format

```json
{
  "userInfo": {
    "aiName": "MyAI",
    "userName": "User",
    "profession": "Developer",
    "useCase": "Coding assistance",
    "communicationStyle": "Professional"
  },
  "language": "ZH"
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| userInfo | object | Yes | User information object |
| userInfo.aiName | string | No | AI name |
| userInfo.userName | string | No | User name |
| userInfo.profession | string | No | User profession |
| userInfo.useCase | string | No | Use case |
| userInfo.communicationStyle | string | No | Communication style |
| language | string | No | "ZH" or "EN", default "ZH" |

### Response

Returns 6 configuration files: SOUL.md, IDENTITY.md, MEMORY.md, USER.md, TOOLS.md, AGENTS.md

### Note

- Generation takes 15-30 seconds (uses LLM)
- Required tools (find-skills, autoclaw, brave-search) are automatically included
- Supports Chinese (ZH) and English (EN)

### Avatar Generation (Local Save)

When avatar generation is requested, the skill will:
1. Generate avatar image using AI
2. Download the image to local file system
3. Return local file path for reliable access

No more temporary link concerns - avatars are permanently saved locally!

```json
{
  "generateAvatar": true,
  "avatarStyle": "tech"
}
```

Returns: Local file path to saved avatar image
