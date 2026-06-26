---
name: sea-whatsapp-business-bot
description: AI-powered WhatsApp auto-responder for MY/SG SMEs. Bilingual BM/EN or CN/EN. Handles appointments, FAQ, orders.
version: 2.0.0
metadata:
  openclaw:
    requires:
      env:
        - SKILLPAY_API_KEY
    emoji: "💬"
---

# SEA WhatsApp Business Bot

Smart auto-responder for Southeast Asian SMEs on WhatsApp.

## How to Use This Skill

### Step 1: Charge billing

POST to the skill endpoint to authorize payment:

```
POST https://sea-whatsapp-business-bot.swmengappdev.workers.dev/respond
Content-Type: application/json

{"user_id": "<user_id>"}
```

If successful, you'll receive `{"success": true, "data": {"charged": true}}`.
If payment fails, you'll receive a `payment_url` to share with the user.

### Step 2: Detect customer language

Use these heuristics to detect the incoming message language:
- **Chinese (zh):** More than 30% of characters are CJK (Unicode range \u4e00-\u9fff)
- **Bahasa Malaysia (ms):** Contains words like: saya, nak, boleh, berapa, bila, mana, encik, puan, terima kasih
- **English (en):** Default if none of the above match

### Step 3: Classify intent

Classify the customer's message into one of these intents:
- **greeting**: Hello, hi, selamat, etc.
- **appointment**: Wants to book/reschedule/cancel an appointment
- **faq**: Asking a question that matches business FAQ
- **order_status**: Checking on an order or delivery
- **escalate**: Angry, frustrated, or requesting to speak to a human
- **general**: Everything else

### Step 4: Generate response

Using the business configuration provided, generate an appropriate response:

**Business config structure:**
```json
{
  "name": "Business Name",
  "hours": "9am-6pm Mon-Sat",
  "services": ["Service 1", "Service 2"],
  "faq": [
    {"question": "Common question?", "answer": "Standard answer"}
  ],
  "languages": ["en", "ms"],
  "timezone": "Asia/Kuala_Lumpur"
}
```

**Response guidelines:**
- Always respond in the customer's detected language
- Be friendly, professional, and concise
- For FAQ matches, use the provided answers but adapt to the conversation
- For appointments, confirm details and suggest next steps
- For escalation, acknowledge the frustration and offer to connect to a human
- For greetings, respond warmly and offer help
- Keep responses under 160 characters when possible (WhatsApp best practice)

**Conversation history:** If provided, use previous messages for context continuity.

### Step 5: Determine action

Based on the intent, suggest an action:
- `book_appointment` — when the customer wants to schedule something
- `check_order` — when asking about order/delivery status
- `transfer_to_human` — when escalation is needed or the bot can't help
- `null` — no action needed (greeting, FAQ answered, general chat)

### Output Format

Return the response as JSON:

```json
{
  "reply": "Hi! Selamat datang. How can I help you today?",
  "intent": "greeting",
  "action": null,
  "language": "en"
}
```

## Pricing
$0.03 USDT per call via SkillPay.me
