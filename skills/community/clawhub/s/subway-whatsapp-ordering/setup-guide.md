# Setup Guide: Subway-Style WhatsApp Agent (20 Minutes)

Follow these steps to get your automated ordering agent live on ClawHub.

## 1. Google Sheets Preparation (5 Mins)
- Create a new Google Sheet.
- Name Sheet 1 `Menu` (Columns: Item, Category, Price, Inventory, Status).
- Name Sheet 2 `Orders` (Columns: Timestamp, UserID, Items, Total, Status).
- Share the sheet with your OpenClaw service account.

## 2. Environment Configuration (5 Mins)
- Create a `.env` file in your skill directory.
- Add `SPREADSHEET_ID=your_id_here`.
- Add `WHATSAPP_API_TOKEN=your_token_here`.

## 3. ThumbGate Activation (2 Mins)
- Run `thumbgate import thumbgate-rules.md`.
- Verify rules are active with `thumbgate list`.

## 4. OpenClaw Deployment (8 Mins)
- Place `SKILL.md` in your `~/OpenClaw/Skills/` directory.
- Start OpenClaw and say: "Load skill: Subway-Style WhatsApp Ordering".
- Run a test order: "I want a footlong Subway Club and a Coke".
