---
name: tamil-messaging
description: Handle Tamil, Tanglish and code-mixed text messages - spoken-register replies, spelling-tolerant matching, plain-text formatting, and cultural greetings for Tamil Nadu users.
metadata:
  openclaw:
    emoji: "🇮🇳"
    requires:
      bins: []
      env: []
---

# Tamil Messaging Skill (தமிழ் செய்தி திறன்)

Use this skill when handling text messages in Tamil script (தமிழ்) or Tanglish (romanized Tamil) - SMS, WhatsApp, Telegram, RCS, in-app chat, or any short-message channel.

## When to Use

- User sends Tamil script (Unicode U+0B80-U+0BFF)
- User writes Tanglish: "vanakkam", "eppadi irukeenga", "nandri"
- User mixes Tamil and English in one message ("meeting ku late aagum")
- User asks for Tamil translations

## Common Phrases

| Tamil | Tanglish | Meaning |
|-------|----------|---------|
| வணக்கம் | vanakkam | Hello |
| நன்றி | nandri | Thank you |
| சரி | sari | Okay |
| ஆமா | aama | Yes |
| இல்லை | illai | No |
| எப்படி இருக்கீங்க? | eppadi irukeenga? | How are you? |
| இருங்க | irunga | Hold on |
| வந்துடுவேன் | vanthiduven | I'll come |

## Response Style

- Match user's style (Tamil script → Tamil, Tanglish → Tanglish)
- Match their mix: if they code-switch English words, keep those words in English. Do not translate "meeting", "bank", "OTP", "leave" into literary Tamil.
- Add "-ங்க" suffix for politeness: சொல்லுங்க (sollunga)
- Use respectful terms: அண்ணா (anna), அக்கா (akka)
- Write spoken Tamil, not literary Tamil. வருகிறேன் reads like a textbook; வர்றேன் reads like a person.
- Keep replies short. A text message is chat, not email: no greeting-body-signoff structure.

## Tanglish Spelling Is Not Standardized

The same word arrives spelled many ways. Read by sound, not by exact match:

- vanakkam / vanakam / vannakam
- enna / yenna / na
- irukeenga / irukinga / irukeengala
- pannunga / panunga / pannuga

Never correct the user's spelling, and never ask which spelling they meant.

## Example Responses

**Tanglish:**
```
User: "vanakkam, help venum"
You: "Vanakkam! Enna help venum? Sollunga."
```

**Tamil Script:**
```
User: "வணக்கம், உதவி வேண்டும்"
You: "வணக்கம்! என்ன உதவி வேண்டும்? சொல்லுங்க."
```

**Code-mixed:**
```
User: "bank la account open panna enna documents venum?"
You: "Aadhaar, PAN card, address proof - inda moonu venum. Photo rendu edutthu ponga."
```

## Numbers, Money and Time

- Keep Indian number words as spoken: lakh, crore (not "hundred thousand")
- ₹ amounts stay in digits: "₹5000 aagum", not "ainthaayiram roobai"
- Time in spoken form: "rendu manikku" (2 o'clock), "naalaikku" (tomorrow)

## Formatting for Text Channels

Assume plain text. Most messaging channels render no Markdown at all:

- No headings, no tables, no bullet characters beyond "-"
- Long lists read badly on a phone; keep to 3-4 lines per message
- WhatsApp and Telegram accept `*bold*` and `_italic_`; SMS and RCS do not - skip emphasis unless the channel is known

## Length Limits

Tamil script forces SMS into UCS-2 encoding: 70 characters per segment instead of 160, and each segment costs a message. Tanglish stays in GSM-7 at 160.

- On SMS, prefer Tanglish unless the user wrote in Tamil script first
- On any channel, one idea per message beats one long wall of text

## Festival Greetings

- Pongal: "பொங்கலோ பொங்கல்! இனிய பொங்கல் நல்வாழ்த்துக்கள்!"
- Tamil New Year: "புத்தாண்டு வாழ்த்துக்கள்!"
- Deepavali: "இனிய தீபாவளி நல்வாழ்த்துக்கள்!"
- Ayudha Pooja: "ஆயுத பூஜை நல்வாழ்த்துக்கள்!"
