# Threat Assessment & Defense Guide Generator — OpenClaw Skill 🛡️⚔️

Generate comprehensive cybersecurity threat assessments and defense guides with a single message to your OpenClaw agent.

## What It Does

Send a message like *"Assess ransomware threats for our healthcare organization"* via WhatsApp, Telegram, or Discord, and your OpenClaw agent will:

1. Analyze the threat landscape for your industry
2. Assess risks to your specific assets
3. Generate a tailored defense strategy
4. Provide detection, monitoring, and incident response guidance

## Quick Install

```bash
clawhub install threat-assessment-defense-guide

# Or manually
mkdir -p ~/.openclaw/skills/threat-assessment-defense-guide
cp SKILL.md ~/.openclaw/skills/threat-assessment-defense-guide/
```

## Configuration

Add to your `openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "threat-assessment-defense-guide": {
        "enabled": true,
        "env": {
          "TOOLWEB_API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

## Get Your API Key

1. Visit [portal.toolweb.in](https://portal.toolweb.in)
2. Sign up for a plan (free trial: 10 API calls)
3. Copy your API key from the dashboard

## Threat Types Covered

- Ransomware & Extortion
- Phishing & Social Engineering
- Advanced Persistent Threats (APT)
- DDoS Attacks
- Insider Threats
- Supply Chain Attacks
- Zero-Day Exploits
- Data Exfiltration
- Cloud Security Threats
- IoT/OT Threats

## Industries Supported

Technology, Healthcare, Finance, Manufacturing, Government, Education, Retail, Energy, and more.

## Example Usage

```
You: I'm worried about ransomware and phishing at our hospital.
     We need to protect our patient database and endpoint devices.

Agent: 🛡️ Threat Assessment & Defense Guide
       Industry: Healthcare
       Threats: Ransomware, Phishing
       ...
       ⚠️ Critical: Healthcare is #1 ransomware target
       🛡️ Priority: Deploy EDR on all clinical workstations
       🔍 Monitor: Email gateway for credential harvesting attempts
```

## Pricing

| Plan         | Price/month     | API Calls |
|-------------|----------------|-----------|
| Free Trial  | $0             | 10 calls  |
| Starter     | ₹2,999 (~$36)  | 500       |
| Professional| ₹9,999 (~$120) | 5,000     |
| Enterprise  | ₹49,999 (~$600)| Unlimited |

International users: Select PayPal at checkout for USD/EUR/GBP payments.

## Support

- 📧 info@mkkpro.com
- 🌐 https://toolweb.in
- 🔌 https://portal.toolweb.in
- 📺 YouTube: https://youtube.com/@toolweb

## License

MIT-0 (as required by ClawHub)

---

*Built by a CISSP & CISM certified security professional at [ToolWeb.in](https://toolweb.in)*
