---
name: socialepoch-whatsapp-scrm
description: SocialEpoch WhatsApp SCRM open API, tailored for enterprise overseas marketing and customer service scenarios. Full coverage of WhatsApp account management, bulk sending,online agent query, customer operation, user profiling, chat record retrieval and Webhook callback,enabling automatic message reception and AI-powered automatic replies. Supports one-on-one & bulk sending for text, image, audio, video, document, business card, link card and diversion link,Supports message callbacks and message status callbacks. Built-in signature adaptation, automatic dependency management and zero-configuration deployment to empower overseas private domain and automated operation.
version: 2.3.3
author: SocialEpoch
metadata:
  emoji: 📱
  type: tool
  platform: darwin
  openclaw:
    requires:
      bins: ["python3"]
      env: ["SOCIALEPOCH_TENANT_ID", "SOCIALEPOCH_API_KEY", "SOCIALEPOCH_SOURCE"]
    primaryEnv: SOCIALEPOCH_API_KEY
    install:
      - id: python-brew
        kind: brew
        formula: python
        bins: ["python3"]
        label: Install Python 3 (brew)
    launcher:
      command: "${PYTHON}"
      args:
        - "scrm_api.py"
      workingDir: "${SKILL_ROOT}"
      python: true
      auto_bootstrap: true
      auto_install_python: true
---

# SocialEpoch WhatsApp SCRM Intelligent Assistant
Comprehensive management for WhatsApp service accounts. Support one-on-one and bulk delivery of text, images, audio, videos, documents, business cards and link messages, with online agent query and automatic signature. No manual dependency installation or environment configuration required. Clear guidance will be prompted when configuration is missing.

## 🔒 Security & User Consent Statement
This is the official SocialEpoch WhatsApp SCRM skill for WhatsApp message sending, receiving and automation services.
All functions are manually triggered by users. No auto-run, no background process, no data collection, no system modification, no sensitive behavior.
The client is official, safe, and used only for WhatsApp messaging.


## Core Features
- 📱 Cross-platform compatibility: Native adaptation for Mac
- 📦 Dependency management: Automatic detection and installation of requests
- 🔧 Dual configuration: Environment variables & local config file
- ✅ Strict validation: Format, non-empty and type checking for all parameters
- 📊 Structured output: Standardized JSON response for all results
- 🚀 Send source support: PC(1), Mobile(2), Cloud(3), default to PC(1)

## Send Source Description
- 1 = PC (Default)
- 2 = Mobile
- 3 = Cloud

## Configuration Methods (Choose One)
### Method 1: Environment Variables (Recommended)
```bash
export SOCIALEPOCH_TENANT_ID="Your Tenant ID"
export SOCIALEPOCH_API_KEY="Your API Key"
export SOCIALEPOCH_SOURCE="1"  # 1=PC,2=Mobile,3=Cloud
```

### Method 2: Command Line Configuration
```bash
# Default source = 1 (PC)
python3 scrm_api.py set_config Your_Tenant_ID Your_API_Key

# Custom source (1=PC,2=Mobile,3=Cloud)
python3 scrm_api.py set_config Your_Tenant_ID Your_API_Key 1
```

### Method 3: Auto Message Receiver Management
```bash
# Start auto message receiving (lightweight mode)
python3 scrm_api.py start_receive

# Reset receiver service (upgrade + repair configuration)
python3 scrm_api.py reset_receive

# Check receiver status
python3 scrm_api.py check_receive
```

### Method 4: Open Dashboard
```bash
# Open Dashboard
python3 scrm_api.py open_dashboard
```

## Supported Commands
### Query Online Agent Accounts
```bash
# Query all online agents
python3 scrm_api.py query_online_agents

# Query specified agent by user account (optional)
python3 scrm_api.py query_online_agents "your_user_account"
```

### Send Text Message
```bash
python3 scrm_api.py send_text Sender_Number Recipient_Number "Message Content"
```

### Send Image
```bash
python3 scrm_api.py send_img Sender_Number Recipient_Number "Image URL" "Remark"
```

### Send Audio
```bash
python3 scrm_api.py send_audio Sender_Number Recipient_Number "Audio URL"
```

### Send Document
```bash
python3 scrm_api.py send_file Sender_Number Recipient_Number "File URL" "Remark"
```

### Send Video
```bash
python3 scrm_api.py send_video Sender_Number Recipient_Number "Video URL" "Remark"
```

### Send Business Card
```bash
python3 scrm_api.py send_card Sender_Number Recipient_Number "Card Content"
```

### Send Brand Link Card
```bash
python3 scrm_api.py send_card_link Sender_Number Recipient_Number "Title" "Link URL" "Description" "Cover Image URL"
```

### Send Diversion Link
```bash
python3 scrm_api.py send_flow_link Sender_Number Recipient_Number "Title" "Diversion Number List"
```

### Query Task Status
```bash
python3 scrm_api.py query_task Task_ID
```

### Set Callback URLs (Message & Status)
```bash
python3 scrm_api.py set_callback "MessageCallbackUrl" "StatusCallbackUrl"
```

## Bulk Messaging
Bulk delivery is available for text, image, video, audio, document and link card messages.
Separate multiple recipient numbers with an **English comma (,)**.

## Operation Rules
1. The assistant only executes operations based on explicit user instructions.
2. Local configuration is stored only for normal tool operation.
3. All actions require clear user authorization and intention confirmation.

# System Level Instructions (AI Must Strictly Follow)
1. Skill directory: openclaw/workspace/skills/socialepoch-wa-scrm
2. Execution command: python3 scrm_api.py
3. Always execute from the skill directory; do not search other paths.

## Error Handling
- Missing dependencies → Friendly installation prompt
- Missing configuration → Clear setup guidance
- Invalid parameters → Usage reminder
- Network exception → Adaptive retry mechanism
```