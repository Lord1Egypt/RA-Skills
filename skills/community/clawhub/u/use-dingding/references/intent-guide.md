# Intent Guide - Disambiguation

This guide helps distinguish between similar user requests that map to different DingTalk products.

## Report vs Todo

**User says:** "Create a task to submit weekly report"

**Analysis:**
- If they want to **track** the work → `todo task create`
- If they want to **actually submit** the report → `report create`

**Decision tree:**
```
Is the user asking to:
├─ Track/remember to do something? → todo
│  └─ "remind me to...", "create a task to...", "add to my todo"
└─ Actually perform the action? → specific product
   └─ "submit a report" → report create
   └─ "send a message" → chat message send
   └─ "schedule a meeting" → calendar event create
```

## Calendar Event vs Meeting Room Booking

**User says:** "Book a meeting room for tomorrow"

**Analysis:**
- Room booking alone → `calendar room book`
- Meeting with participants + room → `calendar event create` (includes room)

**Recommended workflow:**
1. Check participant availability: `calendar participant busy`
2. Find available room: `calendar room search`
3. Create event with room: `calendar event create`

See script: `scripts/calendar_schedule_meeting.py`

## Chat Message vs DING Message

**User says:** "Send an urgent message to the team"

**Analysis:**
- Normal message → `chat message send` or `chat message send-by-bot`
- Urgent notification (SMS/push) → `ding message send`

**Decision:**
- Regular communication → chat
- Requires immediate attention → ding (use sparingly)

## Contact Search vs Department Query

**User says:** "Find all engineers"

**Analysis:**
- Search by keyword → `contact user search --keyword "engineer"`
- Get specific department members → `contact dept members --dept-id <id>`

**Recommended:**
1. Try search first: `contact user search --keyword "engineer"`
2. If need structured results, find department: `contact dept search --keyword "Engineering"`
3. Then get members: `contact dept members --dept-id <deptId>`

## AITable Record vs Todo

**User says:** "Add a new task to the project tracker"

**Analysis:**
- Personal task management → `todo task create`
- Team project tracking in a table → `aitable record create`

**Clues:**
- Mentions "table", "tracker", "spreadsheet" → aitable
- Personal reminder → todo
- Team visibility needed → likely aitable

## Approval vs Todo

**User says:** "I need to approve the leave request"

**Analysis:**
- Formal approval workflow → `oa approval approve`
- Personal task to remember → `todo task create`

**Decision:**
- If there's a formal approval instance → oa approval
- If just tracking → todo

## Common Ambiguous Scenarios

### "Send a notification"
- To chat group → `chat message send-by-bot`
- As urgent DING → `ding message send`
- As report → `report create`

**Ask for clarification:** "Do you want to send a chat message, a DING notification, or create a report?"

### "Check who's available"
- Calendar availability → `calendar participant busy`
- Contact info → `contact user search`
- Attendance status → `attendance record list`

**Ask for clarification:** "Do you want to check calendar availability, contact information, or attendance records?"

### "Create a new entry"
- Todo task → `todo task create`
- AITable record → `aitable record create`
- Calendar event → `calendar event create`

**Ask for clarification:** "What type of entry? A task, a table record, or a calendar event?"
