# 🌐 Tilda Publisher

> Publish articles to Tilda via browser automation. No write API needed — the agent operates the Tilda UI exactly like a human.

---

## What it does

- Creates new pages and article posts in any Tilda project
- Fills in title, body content, and SEO description
- Publishes the page and returns the live URL
- **Self-heals broken selectors** when Tilda updates its UI — saves learned selectors to avoid repeat failures
- **Guided onboarding** on first run — asks for credentials, tests the connection, confirms readiness

---

## Stack

Node.js · Playwright · Chromium (headless)

---

## Requirements

| Variable | Description |
|---|---|
| `TILDA_EMAIL` | Your tilda.cc account email |
| `TILDA_PASSWORD` | Your tilda.cc account password |
| `TILDA_PROJECT_NAME` | Target project name *(optional — auto-detected if only one project)* |

---

## Install

```bash
clawhub install tilda-publisher
```

---

## Usage

Just tell your agent:

> "Publish an article on Tilda. Title: Getting Started with OpenClaw. Content: ..."

The agent will handle the rest — login, page creation, content, SEO, and publishing.

---

## First run

On first use the agent will ask you:

1. Your Tilda email
2. Your Tilda password *(stored locally in `.env`, never sent anywhere)*
3. Project name *(optional)*

Then it runs a test login and confirms the skill is ready.

---

## Author

[@vspandexe](https://clawhub.ai/publishers/vspandexe) · MIT-0
