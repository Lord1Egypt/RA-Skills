# Scheduling/Booking Tools User Demand Research Report

## Overview

- **Scope**: Cal.com, Calendly, and similar scheduling/booking tools
- **Focus**: User pain points and feature gaps
- **Data Sources**: Reddit, X (Twitter), GitHub
- **Feedback Collected**: 150+ real user requests and complaints
- **Date**: January 2026

---

## Executive Summary

Users of scheduling/booking tools like Cal.com and Calendly experience significant friction around **time slot management**, **no-show prevention**, **integration limitations**, and **booking workflow inflexibility**. The most critical pain points revolve around meetings being scattered throughout the day (destroying focus time), last-minute cancellations/rescheduling, and limited customization options.

---

## Key Pain Points

### 1. Scattered Meetings Destroying Focus Time (High Priority)

Users are frustrated that scheduling tools allow bookings scattered throughout the day, fragmenting their work time.

| Issue | Sources | Votes |
|-------|---------|-------|
| Meetings get spread out (13:00, 15:00, 16:00) instead of batched | GitHub | 0 |
| Need "blocked schedule" - only book before/after existing meetings | X | **267** |
| Adjacency-only booking to preserve deep work blocks | GitHub | 0 |

**Representative Quotes:**
> "I have a large window for meetings, and what often happens is someone will book at 13:00, another one at 15:00 and then at 16:00. Each meeting is 30 minutes and instead of having all of them one after the other I have to wait." — @ilan-grif (GitHub)

> "User requests a feature in Calendly that allows booking only before or after existing meetings, creating blocks of time for focused work." — @JoshConstine (X, 267 likes)

**Opportunity**: Smart batching algorithm that groups meetings together automatically.

---

### 2. Last-Minute Cancellations & Rescheduling (High Priority)

Users lack control over when attendees can cancel or reschedule.

| Issue | Sources | Votes |
|-------|---------|-------|
| No limit for cancellation/rescheduling meetings | GitHub | 4 |
| Need auto-accept with disabled cancel/reschedule options | X | 0 |
| Automated reminders for no-show appointments | Reddit | 4 |

**Representative Quotes:**
> "There is a Minimum Limit (for event) that can be set up so people cannot book last minute meetings. Currently, there is no option for cancellation/rescheduling limits, which leads to frustration when users can reschedule or cancel last minute." — @barjoy01 (GitHub)

**Opportunity**: Cancellation/rescheduling policies with time limits and fees.

---

### 3. No-Show Management (High Priority)

No-shows waste time and revenue, but tools lack proactive prevention.

| Issue | Sources | Votes |
|-------|---------|-------|
| Need automated reminder sequences | X | 6 |
| Automated reminders until no-shows reschedule | Reddit | 4 |
| No-show prediction models | X | 0 |
| Over-booking systems to accommodate anticipated no-shows | X | 0 |

**Representative Quotes:**
> "User wants to automate sending reminders to clients marked as no-show until they reschedule their appointment, improving follow-up efficiency." — @jprime4 (Reddit)

**Opportunity**: AI-powered no-show prediction + aggressive reminder sequences + overbooking options.

---

### 4. Integration Gaps (Medium-High Priority)

Users need more native integrations with their existing tools.

| Missing Integration | Sources | Votes |
|--------------------|---------|-------|
| Nextcloud Talk video conferencing | GitHub | 3 |
| Zoho Meeting | GitHub | 4 |
| iDEAL payment method (Stripe) | GitHub | 0 |
| Todoist task creation on booking | GitHub | 3 |
| MCP (Model Context Protocol) for AI workflows | GitHub | 0 |
| Google Calendar sync issues | X | 1 |

**Representative Quotes:**
> "For users who self-host their infrastructure using Nextcloud, this means they cannot automatically generate video conference links for their scheduled meetings." — @onerpsystems (GitHub)

**Opportunity**: Broader integration ecosystem, especially for self-hosted and European tools.

---

### 5. Booking Slot Inflexibility (Medium Priority)

Time slot generation doesn't adapt well to real-world scenarios.

| Issue | Sources | Votes |
|-------|---------|-------|
| Non-standard slot times when gaps exist | GitHub | 0 |
| Calendar shows default times (9-5) even with custom settings | GitHub | 3 |
| Need location-specific time slots | Reddit | 1 |
| Booking slots start at odd times based on external calendar gaps | GitHub | 0 |

**Representative Quotes:**
> "When external calendar events create gaps in my availability, Cal.com offers booking slots that start at non-standard times based on when those gaps begin—rather than respecting my preferred scheduling intervals." — @ostahl8 (GitHub)

**Opportunity**: Smarter slot generation that respects user preferences even with external conflicts.

---

### 6. Post-Booking Editing Issues (Medium Priority)

Users cannot easily fix mistakes after booking.

| Issue | Sources | Votes |
|-------|---------|-------|
| Cannot edit booking details (email typos) after creation | GitHub | 0 |
| Cannot delete or cancel one-use links | Reddit | 2 |
| Cannot update location to Google Meet/Zoom after booking | GitHub | 0 |

**Representative Quotes:**
> "Allow users to edit booking details, such as correcting email addresses, after a booking has been made instead of requiring cancellation and rebooking." — @mrkylegp (GitHub)

**Opportunity**: Post-booking editing capabilities with audit trail.

---

### 7. Analytics & Insights (Medium Priority)

Users want better visibility into their scheduling patterns.

| Issue | Sources | Votes |
|-------|---------|-------|
| Need built-in analytics dashboard | GitHub | 0 |
| Insights API for programmatic access | GitHub | 0 |
| Booking completed webhooks for stats | GitHub | 0 |
| Meeting cost calculator based on attendee time | X | **257** |

**Representative Quotes:**
> "Introduce a built-in analytics dashboard that gives users clear insights into their scheduling activity, displaying key metrics such as total bookings, cancellation rates, or event type usage." — @lohithg-15 (GitHub)

**Opportunity**: Native analytics with conversion funnels, no-show rates, and time utilization metrics.

---

### 8. Notification & Reminder Gaps (Medium Priority)

Current notification systems are insufficient.

| Issue | Sources | Votes |
|-------|---------|-------|
| Notifications via ntfy.sh (self-hosted) | GitHub | 0 |
| SMS notifications for healthcare | X | 8 |
| Voice AI appointment reminders | X | 16 |
| Reminders for scheduled appointments | X | 0 |

**Representative Quotes:**
> "User expresses frustration over the lack of notifications in the product, which they find to be an organizational hazard." — @justin-hackin (GitHub)

**Opportunity**: Multi-channel notifications (SMS, push, voice AI, self-hosted options).

---

### 9. Team & Routing Complexity (Medium Priority)

Business users need more sophisticated routing logic.

| Issue | Sources | Votes |
|-------|---------|-------|
| Booking routing based on multiple rules (HubSpot) | Reddit | 3 |
| Team visibility for reservations | Reddit | 2 |
| Admin override for high-priority bookings | GitHub | 0 |

**Representative Quotes:**
> "Currently, when an Event Type is set to 'Requires Confirmation,' the admin is blocked from approving a booking request if a conflicting event exists in that slot. An admin should be able to approve high-priority clients without changing the event settings temporarily." — @scopecreepsoap (GitHub)

**Opportunity**: Advanced routing rules + priority override system.

---

### 10. Embed & Localization Issues (Lower Priority)

Embedded calendars have UX issues.

| Issue | Sources | Votes |
|-------|---------|-------|
| Embedded calendars use browser language, not site language | GitHub | 0 |
| Pop-up loading slows down pages | GitHub | 0 |
| Mobile feature parity issues | GitHub | 0 |

**Opportunity**: Better embed customization and mobile experience.

---

## Competitive Landscape

### Cal.com vs Calendly - User Preferences

| Feature | Cal.com | Calendly | User Preference |
|---------|---------|----------|-----------------|
| Open source | Yes | No | Cal.com (self-hosters) |
| Pricing | Generous free tier | Limited free tier | Cal.com |
| Integrations | Growing | Mature | Calendly |
| Enterprise features | Developing | Mature | Calendly |
| Customization | Higher | Lower | Cal.com |

### Emerging Competitors Mentioned

- **Custom solutions**: Users building their own due to specific needs
- **Setmore**: Mentioned as lacking flexibility for service packages
- **10to8**: Criticized for half-hour scheduling assumptions

---

## Feature Request Summary by Priority

### Must-Have (Immediate Impact)
1. **Meeting batching/adjacency booking** - Preserve focus time
2. **Cancellation/reschedule time limits** - Reduce last-minute changes
3. **No-show automation** - Reminder sequences + prediction
4. **Post-booking editing** - Fix mistakes without rebooking

### Should-Have (Competitive Advantage)
5. **Native analytics dashboard** - Booking insights
6. **Broader integrations** - Zoho, Nextcloud, iDEAL
7. **Advanced routing rules** - Multi-factor booking assignment
8. **Multi-channel notifications** - SMS, voice AI, ntfy.sh

### Nice-to-Have (Differentiation)
9. **AI scheduling assistant** - MCP integration
10. **Meeting cost calculator** - Time = money awareness
11. **Travel time/mileage calculations** - Mobile service providers

---

## Methodology

This report analyzed **150+ real user feedback items** collected via RequestHunt from:
- **Reddit**: r/calendly, r/smallbusiness, r/productivity, r/CRM, r/remotework
- **X (Twitter)**: Direct feature requests and complaints
- **GitHub**: Cal.com issues repository and related projects

Data collection focused on:
- Feature requests with explicit pain points
- Complaints about existing functionality
- Comparison discussions between tools
- User workarounds indicating gaps

---

## Appendix: Top Voted Requests

| Request | Platform | Votes |
|---------|----------|-------|
| Block scheduling (only book adjacent to meetings) | X | 267 |
| Meeting cost calculator for invitees | X | 257 |
| GP booking system usability overhaul | X | 259 |
| Production-ready meeting bot API | X | 332 |
| Google Meet refund request for late meetings | X | 1,829 |
| Big calendar component for MUI | GitHub | 194 |

---

*Report generated using RequestHunt API - analyzing real user feedback from Reddit, X, and GitHub.*
