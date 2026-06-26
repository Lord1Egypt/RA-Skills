# Skill: resolve_relative_date

## Purpose
Convert natural-language day-of-week references ("Wednesday", "next Friday", "this Wed", "Fri", "tomorrow", "day after tomorrow", etc.) into a concrete future calendar date (ISO format: YYYY-MM-DD).

This skill exists **because LLMs are unreliable at calendar arithmetic** when only given the current date in text. Always delegate date resolution to this tool instead of trying to calculate it yourself.

## When to use this tool
Use `resolve_relative_date` **before** you:

- Create / add / schedule any calendar event
- Send a date to Google Calendar, Outlook, Apple Calendar, Cal.com, Reclaim, etc.
- Tell the user a specific date that depends on "next Wednesday", "this Friday", etc.
- Need to know whether "Wednesday" means this week or next week

Do **not** guess or calculate offsets yourself (mod 7 arithmetic, weekday names → numbers, etc.). You will almost certainly introduce off-by-one or wrong-week errors.

## Return value
Always a string in format YYYY-MM-DD
Example: "2026-03-11"
If the expression is ambiguous or invalid, the tool usually returns the most reasonable future match or raises a clear error.

## Common patterns that MUST use this tool
-Wednesday / Wed / this Wednesday / next Wednesday
-Friday / Fri / this Friday
-tomorrow
-day after tomorrow
-next Monday / this Monday
-in two days / in 5 days
-this weekend / next weekend
-next week Tuesday

## Patterns that usually do NOT need the tool
-"March 15" (absolute date)
-"2026-04-01" (already ISO)
-"today" (you already know current date)
-"in 3 hours" (time only, no day shift)

Use good judgment — when in doubt, call the tool. It is fast and deterministic.
Happy scheduling!

## Usage Examples
User: Add standup on Wednesday at 10am

→ Call resolve_relative_date(relative_expr="Wednesday")
→ Suppose returns "2026-03-11"
→ Then create event on 2026-03-11 10:00

User: Schedule review next Friday

→ resolve_relative_date("next Friday")
→ e.g. "2026-03-13"

User: Put dentist appointment this Wed

→ resolve_relative_date("this Wed")
→ If today is Wed → returns next Wed (most agents treat "this Wed" as future)
→ If today is Tue → returns tomorrow's Wed

## Best-practice prompt prefix (add to your TOOLS.md)
Current date & time: {current_iso_datetime}

Never calculate or guess future dates yourself when the user says things like "Wednesday", "Friday", "next Tuesday", "this weekend", "tomorrow", etc.

ALWAYS call resolve_relative_date(relative_expr=…) first to get the correct YYYY-MM-DD before you:
• create calendar events
• propose meeting times with specific dates
• tell the user what date something will happen on

Do NOT do weekday math in your head. You are not good at it.

## Tool Signature

```json
{
  "name": "resolve_relative_date",
  "description": "Converts a natural-language relative day expression into the next upcoming date (ISO YYYY-MM-DD). Returns the soonest future date that matches the description.",
  "parameters": {
    "type": "object",
    "properties": {
      "relative_expr": {
        "type": "string",
        "description": "Natural language day reference. Examples: 'Wednesday', 'next Friday', 'Fri', 'this Wed', 'tomorrow', 'day after tomorrow', 'next Monday', 'in 3 days', 'this weekend', 'next week Tuesday'"
      },
      "reference_time": {
        "type": "string",
        "description": "Optional. ISO datetime string used as 'now'. If omitted, the system uses current real time. Format: '2026-03-03T18:47:00+08:00'",
        "default": null
      },
      "timezone": {
        "type": "string",
        "description": "Optional. IANA timezone name (e.g. 'Asia/Singapore', 'America/New_York'). Only needed if you want the result interpreted in a specific timezone instead of the user's/system default.",
        "default": null
      }
    },
    "required": ["relative_expr"]
  }
}


