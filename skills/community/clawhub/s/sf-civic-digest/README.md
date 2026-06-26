# CivicClaw — SF Civic Intelligence Skill

CivicClaw is a set of scripts and prompts that collect and synthesize San Francisco government data and journalism sources. It allows your agent to answer questions about what's happening in your neighborhood, tell you what hearings or events are coming up that you could attend, and show you where decisions that affect you are being made.

I use it to give me a weekly digest of what happened in my neighborhood and if there are any public hearings or trash pickups I might want to attend. The nature of skills means you can mold it to be whatever you want, do research on your elected officials, track specific projects, the sky is the limit. All 11 SF supervisorial districts supported.

## Why I Built This

I was frustrated not knowing where decisions that affect me were being made, or how my city government actually works. Why has 400 Divisadero been an abandoned car wash for years? Who decides what art to put in Golden Gate Park? I didn't know, but I wanted to — and I wanted to move the needle on issues I care about. I wanted to show up and advocate for more housing.

## Getting Started

Point your agent at `SKILL.md`. It'll take it from there.

## What It Covers

**Government bodies:** Board of Supervisors, Planning Commission, Historic Preservation Commission, Zoning Administrator, Board of Appeals, SFMTA (Engineering Hearings + Board), Rent Board, Rec & Park Commission, BART Board, SFUSD Board of Education, SF County Transportation Authority

**Data layers:** Building permits, housing pipeline (AB 2011/SB 35/density bonus), 311 service requests, Ethics Commission (lobbyist contacts + campaign contributions), eviction notices

**Journalism:** Mission Local, Streetsblog SF, SForF YIMBY, 48 Hills, SF Standard

**Community:** Volunteer cleanup events (Refuse Refuse SF + DPW)

---

## Known Limitations

- **Legistar historical data**: RSS feed covers ~3 weeks. Older Board of Supervisors vote history requires manual archive building.
- **SF Examiner**: RSS feed returns 404 — not currently monitored.
- **Journalism Sources**: Picked according to my own taste and bias. Feel free to adjust.
- **MOHCD affordable housing pipeline**: Not yet integrated.