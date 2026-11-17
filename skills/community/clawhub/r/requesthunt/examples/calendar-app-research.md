# RequestHunt Example: Deep Investigation into Calendar/Scheduling Apps

This is a complete conversation example showing how the requesthunt skill helps users conduct user demand research by collecting and analyzing real user feedback from Reddit, X (Twitter), and GitHub.

---

## Conversation

### User

> I want to use requesthunt skill to have a deep investigation into Calendar app.

### Assistant

I'll help you conduct a deep investigation into Calendar apps using RequestHunt. Let me first check the API setup and then gather user feedback data.

**Checking API Usage:**

```bash
requesthunt usage
```

```
tier: pro
credits_used: 65
credits_limit: 2000
credits_remaining: 1935
rate_limit: 60 req/min
```

API is working. Before I start collecting data, let me clarify the research scope:

**Questions to define the investigation:**

1. **Specific Calendar apps to focus on?** (e.g., Google Calendar, Apple Calendar, Outlook, Calendly, Cal.com, Notion Calendar, Fantastical, etc.)
2. **Research focus?** (General calendar apps / Scheduling tools / Team calendars / Personal productivity)
3. **What are you trying to learn?** (Feature gaps / Competitive analysis / Market opportunity)
4. **Platform preference?** Reddit, X, GitHub - or all three?

---

### User

> 1. cal.com and similar apps 2. Scheduling/booking tools 3. user pain points 4. all

### Assistant

*Starting data collection across all platforms...*

**Step 1: Scrape Topic**

```bash
requesthunt scrape start "scheduling-tools" --platforms reddit,x,github
```

```
# Scrape Job Started
- **Job ID**: kx71s2ccqederm61w3whaaqhvd7zd6cq
- **Topic**: scheduling-tools
- **Platforms**: reddit, x, github
- **Status**: pending
```

**Step 2: Search for Cal.com feedback**

```bash
requesthunt search "cal.com" --expand --platforms reddit,x,github --limit 50
```

**Results (50 requests):**

| Request | Platform | Votes |
|---------|----------|-------|
| Embed Cal.com Integration inside website | GitHub | 0 |
| Integrate NextCloudTalk with Cal.com | GitHub | 3 |
| Create Task Trigger on New Bookings (Todoist) | GitHub | 3 |
| Insights API for Booking Data | GitHub | 0 |
| Native Zoho Meeting Integration | GitHub | 4 |
| Limit Time for Cancelling/Rescheduling | GitHub | 4 |
| Add auto-accept feature for appointments | X | 0 |
| Allow rotating client secret | GitHub | 0 |
| Batch bookings together | GitHub | 0 |
| Add MCP integration for AI workflows | GitHub | 0 |

**Step 3: Search for Calendly feedback**

```bash
requesthunt search "calendly" --expand --platforms reddit,x,github --limit 50
```

**Results (18 requests):**

| Request | Platform | Votes |
|---------|----------|-------|
| Add 'blocked schedule' feature | X | **267** |
| Add reminders for scheduled appointments | X | 0 |
| Add location-specific time slots | Reddit | 1 |
| Implement booking routing based on multiple rules | Reddit | 3 |
| Implement automated reminders for no-show | Reddit | 4 |
| Add ability to delete/cancel one-use links | Reddit | 2 |

**Step 4: Search for appointment scheduling pain points**

```bash
requesthunt search "appointment scheduling" --expand --platforms reddit,x --limit 30
```

**Key findings:**
- SMS notifications for healthcare scheduling (8 votes)
- Flexible appointment times for therapy apps
- CRM automated follow-ups and scheduling (5 votes, 17 comments)
- Voice AI appointment reminders (16 votes)

**Step 5: Search for booking software feedback**

```bash
requesthunt search "booking software" --expand --platforms reddit,x --limit 30
```

**Key findings:**
- GP booking system usability overhaul (259 votes)
- Simple booking system for meeting rooms (20 votes, 41 comments)
- Price drop alerts for bookings (18 votes)

**Step 6: Search for scheduling pain points**

```bash
requesthunt search "scheduling pain" --expand --platforms reddit,x --limit 30
```

**Key findings:**
- NomadTime: suggest optimal meeting times across timezones
- Streamline scheduling to reduce back-and-forth
- Gang scheduling support for Kubernetes (28 votes)

**Step 7: Search for no-show management**

```bash
requesthunt search "no-show booking" --expand --platforms reddit,x --limit 20
```

**Key findings:**
- Automated reminder sequences (6 votes)
- No-show prediction models
- Over-booking systems to accommodate no-shows
- Improve refund process for no-show situations

---

## Generated Research Report

### Executive Summary

Users of scheduling/booking tools like Cal.com and Calendly experience significant friction around **time slot management**, **no-show prevention**, **integration limitations**, and **booking workflow inflexibility**. The most critical pain points revolve around meetings being scattered throughout the day (destroying focus time), last-minute cancellations/rescheduling, and limited customization options.

---

### Top 10 Pain Points

#### 1. Scattered Meetings Destroying Focus Time (HIGH PRIORITY)

**Votes: 267** (X)

Users are frustrated that scheduling tools allow bookings scattered throughout the day, fragmenting their work time.

> "I have a large window for meetings, and what often happens is someone will book at 13:00, another one at 15:00 and then at 16:00. Each meeting is 30 minutes and instead of having all of them one after the other I have to wait." — @ilan-grif (GitHub)

> "User requests a feature in Calendly that allows booking only before or after existing meetings, creating blocks of time for focused work." — @JoshConstine (X, 267 likes)

**Opportunity**: Smart batching algorithm that groups meetings together automatically.

---

#### 2. Last-Minute Cancellations & Rescheduling (HIGH PRIORITY)

**Votes: 4** (GitHub)

> "There is a Minimum Limit (for event) that can be set up so people cannot book last minute meetings. Currently, there is no option for cancellation/rescheduling limits."

**Opportunity**: Cancellation/rescheduling policies with time limits and fees.

---

#### 3. No-Show Management (HIGH PRIORITY)

**Votes: 6** (X)

> "User wants to automate sending reminders to clients marked as no-show until they reschedule their appointment."

**Opportunity**: AI-powered no-show prediction + aggressive reminder sequences + overbooking options.

---

#### 4. Integration Gaps (MEDIUM-HIGH)

| Missing Integration | Votes |
|--------------------|-------|
| Nextcloud Talk | 3 |
| Zoho Meeting | 4 |
| iDEAL payment (Stripe) | 0 |
| Todoist task creation | 3 |
| MCP for AI workflows | 0 |

---

#### 5. Booking Slot Inflexibility (MEDIUM)

> "When external calendar events create gaps in my availability, Cal.com offers booking slots that start at non-standard times based on when those gaps begin—rather than respecting my preferred scheduling intervals."

---

#### 6. Post-Booking Editing Issues (MEDIUM)

> "Allow users to edit booking details, such as correcting email addresses, after a booking has been made instead of requiring cancellation and rebooking."

---

#### 7. Analytics & Insights (MEDIUM)

**Votes: 257** (X)

> "Introduce a built-in analytics dashboard that gives users clear insights into their scheduling activity."

> "Meeting cost calculator based on attendee time" — 257 votes on X

---

#### 8. Notification & Reminder Gaps (MEDIUM)

| Request | Votes |
|---------|-------|
| Voice AI reminders | 16 |
| SMS notifications | 8 |
| ntfy.sh support | 0 |

---

#### 9. Team & Routing Complexity (MEDIUM)

> "Currently, when an Event Type is set to 'Requires Confirmation,' the admin is blocked from approving a booking request if a conflicting event exists in that slot."

---

#### 10. Embed & Localization Issues (LOWER)

> "Embedded calendars use browser language, not site language."

---

### Feature Priority Matrix

| Priority | Feature | Impact |
|----------|---------|--------|
| **Must-Have** | Meeting batching/adjacency booking | Preserve focus time |
| **Must-Have** | Cancellation/reschedule time limits | Reduce last-minute changes |
| **Must-Have** | No-show automation | Reminder sequences + prediction |
| **Must-Have** | Post-booking editing | Fix mistakes without rebooking |
| **Should-Have** | Native analytics dashboard | Booking insights |
| **Should-Have** | Broader integrations | Zoho, Nextcloud, iDEAL |
| **Should-Have** | Advanced routing rules | Multi-factor booking assignment |
| **Nice-to-Have** | AI scheduling assistant | MCP integration |
| **Nice-to-Have** | Meeting cost calculator | Time = money awareness |

---

### Top Voted Requests (Appendix)

| Request | Platform | Votes |
|---------|----------|-------|
| Google Meet refund request for late meetings | X | **1,829** |
| Production-ready meeting bot API | X | 332 |
| Block scheduling (only book adjacent) | X | 267 |
| GP booking system usability overhaul | X | 259 |
| Meeting cost calculator | X | 257 |
| Big calendar component for MUI | GitHub | 194 |

---

### Methodology

This report analyzed **150+ real user feedback items** collected via RequestHunt from:
- **Reddit**: r/calendly, r/smallbusiness, r/productivity, r/CRM, r/remotework
- **X (Twitter)**: Direct feature requests and complaints  
- **GitHub**: Cal.com issues repository and related projects

**API Usage:**
- 7 search queries with realtime expansion
- 1 topic scrape job
- Total: ~75 realtime requests consumed

---

## Key Takeaways

1. **`requesthunt scrape start`** triggers background scraping for a topic across platforms
2. **`requesthunt search --expand`** fetches fresh data in realtime (uses credits)
3. **Multiple search terms** help capture different aspects of the same problem
4. **Quantitative data** (votes, comments) helps prioritize findings
5. **Final report** synthesizes patterns into actionable insights
