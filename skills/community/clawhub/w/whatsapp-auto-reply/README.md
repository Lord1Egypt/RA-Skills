# WhatsApp Auto Reply Skill

## Skill Name
whatsapp_auto_reply

## Description
This OpenClaw skill automatically sends a WhatsApp reply by connecting to an external messaging API. It demonstrates a multi-step autonomous workflow including API communication, message processing, and structured output generation.

## Functionality
- Receive message input
- Call external API
- Send WhatsApp response
- Return structured output to the OpenClaw agent

## Workflow

1. Agent triggers the skill
2. Skill receives message and target phone number
3. Skill calls external WhatsApp API
4. API sends the message
5. Skill returns structured response to the agent

## Input
- `phone_number` (string) – target phone number
- `message` (string) – message content

## Output

```json
{
  "status": "success",
  "api_response": {
    "id": "message_id",
    "delivered": true
  }
}