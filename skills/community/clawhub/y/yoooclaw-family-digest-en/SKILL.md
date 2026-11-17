---
name: yoooclaw-family-digest-en
description: Extract important family information from mobile phone notifications using the "person" dimension, display it in groups by relevant people (children, spouses, parents/elders, etc.), and mark the importance. Triggers: information from home / news from home / what’s at home / what family members said / important information / today’s notice / news about children / news about children / what my husband wants me to do / my wife’s instructions / what my wife said / what my mother said / summary of family news / what’s going on at home.
---

# Family Digest

## Target

Taking **family members** as the dimension, extract the **important information** from spouses, parents, elders, and children's schools/teachers in today's (or recent) notifications, and answer "What important information did family members say today?"

The user sets the family members to focus on through the "Who to follow" field in the installation pop-up window, such as: husband, mother, mother-in-law, Dabao's class teacher, piano teacher, etc. The characters that are set will be displayed first in the output, and if they are not set, they will be automatically inferred from the notification data.

Users are asking about “news about a certain person” or “important information about their family”. What they want is a summary from a person’s perspective, not a to-do list, schedule or consumption flow.

No specific names or structures of household members are assumed - **all inferred from notification data**.

## Data loading strategy

- **First get the notification storage directory through `openclaw ntf storage-path`** (use the Bash tool to run this command, stdout is the absolute path of the directory). All subsequent notification files are directly in this directory and named `YYYY-MM-DD.json`.
- **File naming**: `YYYY-MM-DD.json`, one file per day, including all App notifications on that day
- **Loading priority**: ① The path specified by the user in the prompt > ② `<storage-path>/<YYYY-MM-DD>.json`
- **Time window (dynamically determined according to user's request)**:
  - "Today" → Only files corresponding to today's date
  - "Yesterday" → Only files corresponding to yesterday's date
  - "This week/recently" → last 7 days
  - No explicit time modification → Default to today
  - The user specifies a specific date period → strictly as specified
- Skip non-existent files without reporting errors
- If `openclaw ntf storage-path` is not available, prompt the user to provide the data path
- If the user specifies a specific person in the question ("What does my husband want me to do today"), filter by the person after loading and then display## Input data schema

JSON array, each item:
```json
{"appName":"com.tencent.xin","title":"Group name or contact name","content":"Message content","timestamp":"2026-04-22T10:30:00.000+08:00","appDisplayName":"WeChat"}
```

- `appDisplayName` distinguishes sources: WeChat/SMS/Reminders/Email, etc.
- `title` is the contact name or group name
- WeChat group messages `content` often start with identity tags such as `[Teacher

## Core logic

### 1. Person recognition (infer from data at runtime, do not hardcode names)

| Signal | Determine role |
|---|---|
| The private chat title is "Husband/Wife/Dear/Common Nicknames for Couples" | Spouse |
| Private chat title is "Mom/Dad/Mother-in-law/Father-in-law/Father-in-law/Mother-in-law" | Parents/Elders |
| In the parent group `[Teacher X]:` prefix | child-teacher |
| Kindergarten/school public account push | Children - school notifications |
| Private chat title containing "teacher" (piano/English and other extracurricular classes) | Child - extracurricular class teacher |
| In parent group `[parent-xxx]:` prefix contains homework/child information | Child-parent group (include with caution, see filtering rules) |
| Large family group / Relatives and friends group | Other family members |

If the user specifies specific people in "Who to follow" (such as "husband, mother, Dabao's class teacher"), the messages from these people have the highest priority. Even if the content is short, it must be checked whether it contains requests, notifications or action items.

The real title inferred from the data (such as "husband", "mother", "mother-in-law", "Dabao's head teacher") is used in the output, and the role placeholder ("spouse", "Dabao") is used when it cannot be determined. **Do not bring names from documentation examples into real output. **

### 2. Importance rating

Each piece of information is automatically determined:

- **🔴 Requires response/action**: including deadline, including request verbs such as "please/trouble/help me/remember/need/must", need to sign/solve/prepare items/confirmation
- **🟡 Just know it**: pure notification (activity time, recipe adjustment, praise, sharing link), family mood/progress sharing
- **⚪ Chat**: greetings, cheers, emoticons, no substantive content → **not displayed by default** (discarded silently)### 3. Content refining

For each reserved notice:
- Summarize the core information in one sentence (avoid copying the original text and remove polite words)
- Indicate the source ("Husband's WeChat", "Mom's WeChat", "Second Baby's Class Teacher Notice")
- If there is a deadline/time → list it separately
- If the user needs to do something → mark the action item with `→`

## Filter rules

- **Pure chat** (Parent group `[Parent-xxx]:`'s "Received/+1/Thank you teacher") → Discard
- **Marketing push** (Xiaohongshu, Pinduoduo, Taobao, Douyin, Ele.me discounts, Meituan activities) → Discard
- **Consumption/Bill Notification** (bank deduction, Alipay payment successful, water, electricity and gas payment) → Belongs to `expense-tracker`, this skill is discarded
- **Travel Order** (air ticket, hotel, car rental confirmation) → belongs to `family-trip-checklist`, this skill is discarded
- **Property/Express Logistics** (water outage, express delivery to the station) → Belongs to `family-todo`, this skill is discarded
- **⚪ Chat-level messages** → silently discarded and not mentioned in the output

## Output template

### A. Whole family overview (default mode)

```
📬 Family information summary (YYYY-MM-DD)

━━ 👶 children ━━

  🔴 Action needed
    ① <Summary in one sentence>
       Source: <class/teacher name> Deadline: <if any>
       → <What needs to be done>

  🟡 Just know it
    ② <Summary in one sentence>
       Source: <source>

━━ 👨 <Husband/spouse’s nickname> ━━

  🔴 <Summary in one sentence>
     → <action item>
     Source: <WeChat private chat/etc.>

  🟡 <Summary in one sentence>
     Source: <source>

━━ 👩 <Mom/Mother-in-law, etc.> ━━

  🟡 <Summary in one sentence>
     Source: <source>

━━ Other family members ━━ (displayed if there is relevant information)

  🟡…

━━ Things that need to be responded to today ━━

  ✋ <Person>: <Matter> (Deadline: <if any>)
  ✋ <Character>: <Matter>
```

### B. Single player mode (user specifies a specific character)

```
👨 <spouse nickname>’s message (YYYY-MM-DD)

  🔴 <Summary in one sentence>
     → <action item>

  🟡 <Summary in one sentence>
```

If there is no news from the person that day, simply state "There is no news from <person> today".

## Quality Constraints- Clear requests/action items from family **100%** Reserved, marketing/chat noise **0%** False entry
- Accurate labeling of importance: including deadline/request verb → 🔴; pure notification → 🟡; small talk → silence
- The titles grouped by characters use the real names inferred from the data. Use character placeholders only when it is difficult to determine.
- The summary section of "Things that need to be responded to today" is sorted by urgency to ensure that users can see the most urgent matters at a glance
- Do not make up information that is not included in the notice; if the source is unclear, mark "(speculation)" in the description.
- Only generate session text, do not write files
