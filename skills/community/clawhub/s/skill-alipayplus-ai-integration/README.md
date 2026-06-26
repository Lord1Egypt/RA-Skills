# Alipay+ Payment Integration Skill

🤖 An AgentSkill that helps Acquirers and Mobile Payment Service Providers quickly integrate Alipay+ payments by referencing official online documentation.

---

## 📖 Overview

This skill provides Alipay+ payment integration guidance for both **ACQP (Acquirer Service Provider)** and **MPP (Mobile Payment Service Provider)**. It always fetches the latest official documentation before providing any integration guidance, ensuring you work with up-to-date API parameters, flows, and code examples.

This skill empowers AI to rapidly access the Alipay+ knowledge base, provide accurate responses to Alipay+ integration queries, and generate integration code, thereby helping enterprises substantially reduce the time, complexity, and development effort associated with payment integration.

### Supported Payment Scenarios

| Scenario | ACQP | MPP |
|----------|------|-----|
| **UPM (User-presented Mode) Payment** | ✅ | ✅ |
| **MPM (Merchant-presented Mode) Payment** | ✅ | ✅ |
| **Online Cashier Payment** | ✅ | ✅ |
| **Online Auto Debit** | ✅ | ✅ |

---

## 🚀 Quick Start

### Usage

Trigger directly in conversation:

```
"How to integrate with Alipay+?"
"I'm an acquirer, want to integrate online cashier payment"
"We're a wallet app, how to support auto debit?"
```

### ⚠️ Role Clarification

Before starting, please confirm your role:

| Role | Description |
|------|-------------|
| **ACQP** | Acquirer Service Provider — Payment service providers integrating with merchants |
| **MPP** | Mobile Payment Service Provider — E-wallet providers integrating with Alipay+ |

---

## 📋 Integration Workflow

The skill follows a structured workflow to ensure you always reference the latest documentation:

**Step 1: Fetch Role-Specific Documentation**

```bash
# ACQP:
curl -sL "https://docs.alipayplus.com/alipayplus/llms.txt" | awk '/^## ACQP/{found=1} /^## MPP/{found=0} found'

# MPP:
curl -sL "https://docs.alipayplus.com/alipayplus/llms.txt" | awk '/^## MPP/{found=1} found'
```

**Step 2: Read Getting Started Guide**

- **ACQP**: [Get started with Alipay+ integration](https://docs.alipayplus.com/alipayplus/alipayplus/get_started_acq/get_started_integration_acq.md)
- **MPP**: [Get started with Alipay+ integration](https://docs.alipayplus.com/alipayplus/alipayplus/get_started_mpp/get_started_integration.md)

**Step 3: Fetch Developer Center User Guide**

Access the Alipay+ Developer Center guide for your role to learn about sandbox testing, API debugging, and production launch.

**Step 4: Develop and Test**

Develop and test your integration using the Alipay+ Developer Center tools (iTest, iMock, iNotify, iScan, etc.).

---

## 📁 File Structure

```
alipayplus-integration/
├── README.md        # This file
└── SKILL.md         # Skill definition (AgentSkill spec)
```

> **Note**: This skill fetches all reference documentation dynamically from `https://docs.alipayplus.com/alipayplus/llms.txt`. No local reference files are included.

---

## 🔧 Prerequisites

Before integrating, ensure you have:

1. **Alipay+ Developer Center Account** — Register at [Alipay+ Partner Workspace](https://docs.alipayplus.com/alipayplus/alipayplus/worksp_acq/overview_what_is.md)
2. **Application Created** — Create an application in the Developer Center to obtain PartnerId, ClientId, and API keys
3. **Keys and Certificates** — Generate RSA2048 key pair and obtain Alipay+ public key
4. **Sandbox Environment** — Test your integration in sandbox before going to production

---


## 🔗 Official Documentation

All documentation is fetched dynamically from:

- **Main Documentation**: https://docs.alipayplus.com/alipayplus/llms.txt
- **ACQP Getting Started**: https://docs.alipayplus.com/alipayplus/alipayplus/get_started_acq/get_started_integration_acq.md
- **MPP Getting Started**: https://docs.alipayplus.com/alipayplus/alipayplus/get_started_mpp/get_started_integration.md

---



_Last updated: 2026-04-23_
