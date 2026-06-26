# Subscription Sentinel 🛡️

![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

Subscription Sentinel is an intelligent local AI Skill designed specifically for the **OpenClaw** framework. Acting as your "Personal Financial Data Agent", it securely parses your billing emails to automatically track, infer, and alert you about upcoming internet subscriptions (e.g., SaaS tools, streaming media, AI services). This helps you avoid unnecessary financial losses caused by "forgetting to cancel" or hidden auto-renewal dark patterns.

## ✨ Core Features

- 📧 **Invisible Bill Sniffing**: Securely filters and extracts recent payment receipts, invoices, and billing emails, completely ignoring marketing noise.
- 🧠 **State Inference Engine**: Automatically infers subscription cycles (Monthly/Quarterly/Annually) based on the amount and date relationships between multiple bills, accurately predicting the next billing date.
- 🚨 **Smart Early Warning**: Proactively issues an alert 5 days before the next expected deduction.
- 🛡️ **Tiered Cancellation Assistance**:
  - **Level 1**: If environment permits, utilizes the Agent's own web interaction capabilities to navigate and cancel on your behalf.
  - **Level 2**: Proactively searches for and provides the deepest direct link (Deep Link) to the cancellation page.
  - **Level 3**: Provides the standard step-by-step cancellation guide for the specific service.
- 🔒 **Privacy First**: As an OpenClaw Skill, all data processing and inference are performed entirely within your local environment and OpenClaw's context.

## ⚙️ How It Works

Subscription Sentinel is not a traditional backend program, but rather a structured collection of **Markdown prompts and decision flows (`SKILL.md`)**. It fully leverages the OpenClaw framework's intent-driven tool routing mechanism, instructing the Agent to orchestrate foundational capabilities already present in the host environment, such as `AgentMail`, `browser`, and `web_search`, to accomplish its tasks.

## 🚀 Installation & Usage

### Prerequisites
1. You must have **[OpenClaw](https://github.com/openclaw/openclaw)** installed, configured, and running.
2. Your OpenClaw environment must possess the capability to read emails (e.g., having an `AgentMail` Skill installed and configured with Gmail session authorization).
3. *(Optional)* If you want a fully automated cancellation experience, it is recommended to enable the `browser` (web control) capability and grant corresponding authorizations to your Agent.

### Installation Steps
1. Clone this repository into your OpenClaw skills directory:
   ```bash
   cd ~/.openclaw/skills  # Or locate your corresponding skills directory based on your OS and OpenClaw config
   git clone https://github.com/your-username/SubscriptionSentinel.git subscription-sentinel
   ```
2. Restart OpenClaw or instruct the Agent to reload the Skill list.

### How to Use

You can trigger the Skill using natural language or directly via a slash command:

```text
/subscription-sentinel Check my recent subscriptions for upcoming bills
```

Or naturally speak to your Agent:
> "Can you scan my email inbox for receipts and see if I have any upcoming subscriptions I forgot to cancel?"

## 📁 Directory Structure

```text
SubscriptionSentinel/
├── src/
│   └── SubscriptionSentinel.md     # Original PRD (Product Requirements Document) for reference
└── release/
    ├── README.md                   # Project documentation (This file)
    ├── SKILL.md                    # Core Skill definition file (Prompts, State Machine)
    └── scripts/
        └── data_manager.md         # Pure Markdown instructions for local data persistence
```

## ⚠️ Disclaimer

- This project is an experimental open-source AI Skill. It relies on the understanding capabilities of the underlying LLM and the connectivity of the configured email tools. The analysis results (especially for subscriptions billed through third-party proxies like Apple or PayPal) may encounter recognition omissions or errors. We highly recommend regularly checking your actual bank statements.
- Please safeguard your privacy data and email authorizations. Only run this Skill on localized OpenClaw nodes you trust or within privately deployed sandbox environments.

## 📄 License

This project is open-sourced under the [MIT License](LICENSE).
