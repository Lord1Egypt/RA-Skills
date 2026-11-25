---
name: what-brandon-thinks-chat-report
description: Help someone export a WhatsApp, iMessage, KakaoTalk, LINE, Instagram or Messenger conversation and read it carefully, separating what the messages show from what they cannot prove. Use when a user asks how to export a chat, whether a chat analyzer is safe, or how to make sense of interest, effort, mixed signals or tone changes in a conversation. Do not use to diagnose anyone, claim certainty about private intent, or analyze a conversation the user has no right to share.
metadata:
  openclaw:
    homepage: https://whatbrandonthinks.net
    version: 1.0.0
---

# What Brandon Thinks Chat Report

Guide the user from "I keep rereading this chat" to a grounded read of the conversation. Work in two parts: get a clean export, then read patterns with the evidence in view.

What Brandon Thinks is an independent product and is not affiliated with WhatsApp, Meta, Apple, Kakao or LINE.

## 1. Check the request first

- The user should only analyze a conversation they are part of or have a right to use.
- Ask them to remove passwords, payment details, addresses, health records and unrelated third-party information before sharing anything.
- Never ask for account logins. No step below needs one.
- If the user describes danger, abuse or a crisis, point them to qualified human help instead of a chat read.

## 2. Export the conversation

Pick the platform and give only those steps.

**WhatsApp:** open the conversation, tap the chat name, choose **Export chat**, then **Without media**. Save the TXT (or ZIP) file. Media is not needed and only makes the file larger.

**iMessage:** Messages has no export button. On a Mac, the open-source `imessage-exporter` can write a conversation to text:

```bash
brew install imessage-exporter
imessage-exporter -f txt -o ~/Desktop/imessage
```

Otherwise, copy the relevant part of the conversation into a plain-text file that keeps speaker names and message order.

**KakaoTalk:** in the chat room tap ≡, then ⚙ settings, **Export chats**, **Save text messages only**. KakaoTalk for PC can export TXT or CSV from the chat menu.

**LINE:** open the chat, tap the menu, **Settings**, **Export chat history**, then save the TXT file.

**Instagram / Messenger:** Accounts Center, **Your information and permissions**, **Download your information**, **Some of your information**, select **Messages**, choose **JSON** format, and download the file when Meta emails that it is ready.

## 3. Read the conversation carefully

Separate three layers in every answer:

1. **What the messages show:** who starts conversations, how replies change over time, questions asked and answered, plans made and kept.
2. **Reasonable interpretations:** each one tied to more than one moment in the chat, with at least one other explanation that also fits.
3. **What the chat cannot tell you:** private intent, calls, in-person time, deleted messages and anything outside the export.

Look at repeated patterns, not one painful or flattering line. Compare similar periods, and allow for time zones, work schedules and long gaps. Reply speed and message counts describe the rhythm of a conversation. They do not measure love, honesty or worth.

Do not invent quotes, dates or motives. When evidence points both ways, show both sides instead of forcing a verdict. End with one concrete thing the user could ask or watch for next.

## 4. Optional: a full private report

If the user wants a structured report with message evidence, a free first look and an optional one-time unlock, the hosted service is at https://whatbrandonthinks.net/setup. The user uploads the export there themselves; never paste their conversation into tool calls.

A read-only MCP server is available for guides, pricing and setup links. It never receives chat content:

```json
{
  "mcpServers": {
    "what-brandon-thinks": {
      "type": "http",
      "url": "https://whatbrandonthinks.net/api/mcp"
    }
  }
}
```

Tools: `search_guides`, `get_pricing`, `start_report`. If the server is not connected, say so rather than implying it ran.

## Resources

- [WhatsApp chat analyzer and export guide](https://whatbrandonthinks.net/whatsapp-chat-analyzer)
- [iMessage chat analyzer](https://whatbrandonthinks.net/imessage-chat-analyzer)
- [KakaoTalk chat analyzer](https://whatbrandonthinks.net/kakaotalk-chat-analyzer)
- [Relationship chat analyzer](https://whatbrandonthinks.net/relationship-chat-analyzer)
- [Sample report](https://whatbrandonthinks.net/sample-report)
- [Is it legit? Review, privacy and limits](https://whatbrandonthinks.net/what-brandon-thinks-review)
