---
name: soul-weaver
version: 1.0.1
description: Generate OpenClaw agent configuration files through authorized API access. Requires manual verification and official API key application.
author: AI Soul Weaver Team
tags:
  - openclaw
  - soul-weaver
  - ai
  - agent
  - configuration
category: productivity
permissions:
  - network
platform:
  - openclaw
---

# Soul Weaver Skill

## Description

Generate OpenClaw agent configuration files through authorized API access. Users must first manually verify configurations on the official website, then apply for API keys through official channels.

## Security Notes

- Requires official API key obtained through proper application process
- Users must first manually verify configurations on official website
- Only authorized API endpoints are used
- No system files are modified or replaced automatically
- Requires explicit user invocation with valid API credentials

## Usage Process

### Step 1: Manual Verification
First visit the official website to manually create and verify configurations.

### Step 2: API Key Application
Apply for an API key through the official AI Soul Weaver platform:

**Website**: https://sora2.wboke.com

You need to:
1. Register an account on the website
2. Login to your account
3. Apply for API access in the account dashboard

### Step 3: Authorized Access
Use the skill with your authorized credentials:

```javascript
const result = await handler({
  apiKey: "your_authorized_key", // Required: API key from official application
  apiEndpoint: "https://your-api-endpoint.com", // Optional: custom endpoint
  aiName: "MyAI",
  celebrityName: "musk", 
  profession: "Entrepreneur",
  language: "EN"
});
```

## Response

Returns 6 configuration files: SOUL.md, IDENTITY.md, MEMORY.md, USER.md, TOOLS.md, AGENTS.md

## Important Notes

- API keys are required for automated generation functionality
- Keys must be obtained through official application process only
- Unauthorized API access is strictly prohibited
- All API calls are logged and monitored for security
- Users are responsible for proper key management and security