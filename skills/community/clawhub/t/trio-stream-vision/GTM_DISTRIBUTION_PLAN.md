# Trio Vision — GTM Distribution Plan
## Goal: Maximum awareness + PMF signal collection

**Objective:** Get trio-vision in front of as many potential users as possible across every available channel. Measure interest signals (installs, questions, engagement, feedback) to validate product-market fit for Trio's Vision AI API.

**PMF Signal = Any of:** ClawHub installs, GitHub stars, API key signups, Discord messages, Reddit upvotes, HN comments, Moltbook engagement, demo usage, "how do I..." questions.

---

## PHASE 1: IMMEDIATE (This Week) — Ship & Seed

### 1.1 Moltbook Post (Agentic)
**What:** Post on Moltbook — the AI social network with 770K+ active agents. This is the native social layer for OpenClaw users.
**Action:**
```
Install moltbook skill, then post:
"Just shipped trio-vision — an OpenClaw skill that turns any live camera into a smart camera.
Ask it questions about any YouTube Live, Twitch, or RTSP stream in plain English.
'Is anyone at my front door?' → instant answer. 'Alert me when a package arrives' → continuous watch.
Install: clawhub install trio-vision
Free 100 credits at console.machinefi.com"
```
**PMF signal:** Upvotes, comments, agent interactions
**Effort:** 5 min

### 1.2 OpenClaw Discord (#skills channel)
**What:** Post in the OpenClaw Discord (14,627 members). Draft ready in `DISTRIBUTION.md`.
**Action:** Copy-paste the Discord post from `DISTRIBUTION.md` into #skills channel.
**PMF signal:** Reactions, replies, "how do I..." questions
**Effort:** 5 min

### 1.3 OpenClaw GitHub Discussions
**What:** Post in the Ideas category on github.com/openclaw/openclaw/discussions (190K+ stars repo).
**Action:** Create a new discussion titled "New skill: trio-vision — smart camera alerts via Vision AI" with install instructions and 3 use case examples.
**PMF signal:** Upvotes, comments, stars on skill repo
**Effort:** 10 min

### 1.4 Show HN Post
**What:** Launch on Hacker News as a Show HN post. HN loves "look what AI can do" posts with live demos.
**Action:**
```
Title: Show HN: Turn any camera into a smart camera with natural language (OpenClaw skill)
URL: https://github.com/drandrewlaw/trio-openclaw-skill
```
Body comment: Explain the pain (dumb motion alerts), the solution (natural language conditions), the cost ($0.01/check), and link to install.
**PMF signal:** Upvotes, comments, "I'd use this for..." responses
**Effort:** 15 min
**Timing:** Post at 8-9am EST on a Tuesday/Wednesday for best visibility

### 1.5 Reddit Seeding (5 subreddits)
**What:** Post in communities where camera/smart home users already ask questions trio-vision answers.
**Action:** Create genuine, helpful posts (not spam) in these subreddits:

| Subreddit | Angle | Post Title |
|-----------|-------|------------|
| r/homeassistant | Integration | "I built an OpenClaw skill that lets my AI agent watch my RTSP cameras and alert me in plain English" |
| r/selfhosted | DIY tool | "Open-source skill that adds natural-language AI to any camera feed — no ML setup needed" |
| r/smarthome | Use case | "Finally got rid of dumb motion alerts — now I describe what to watch for in English" |
| r/homedefense | Security | "AI-powered camera monitoring that only alerts for things that actually matter ($0.01/check)" |
| r/artificial | Tech showcase | "Built a vision AI agent skill that watches live streams and answers questions about what it sees" |

**PMF signal:** Upvotes, comments, "does it work with X camera?" questions
**Effort:** 30 min total

---

## PHASE 2: THIS WEEK — Deploy & Demo

### 2.1 Conway Live Demo (THE BIG BET)
**What:** Deploy a public demo on Conway (OpenClaw's cloud compute) that watches a curated set of live streams. Anyone can interact with the agent and ask questions about what it sees. Zero friction, no install, no signup.
**Action:**
1. Spin up a Conway sandbox
2. Install trio-vision skill with API key
3. Connect to 3-5 interesting public streams (city cams, wildlife cams, weather cams)
4. Create a shareable URL
5. Post the demo URL everywhere

**PMF signal:** Number of queries, unique visitors, questions asked, time spent
**Effort:** 2-4 hours
**Impact:** VERY HIGH — the product demos itself

### 2.2 "trio-vision-demo" Meta-Skill
**What:** Create a lightweight demo skill that other OpenClaw agents can invoke. When any agent gets asked "can you watch cameras?" or "do you have vision?", it can pull in the demo, show a live result, and link to install.
**Action:** Create a `trio-vision-demo` skill on ClawHub that does one free check on a public stream as a demo, then says "Install the full skill: `clawhub install trio-vision`"
**PMF signal:** Demo invocations, conversion to full install
**Effort:** 1-2 hours

### 2.3 Twitter/X Launch Thread
**What:** Post a thread from your personal or MachineFi account showing trio-vision in action.
**Action:** Thread format:
```
1/ Just shipped something cool: ask your AI agent about any live camera and get an instant answer.

"Is anyone at my front door?" → 2 seconds → "Yes, there's a person in a blue jacket standing near the doorbell."

It's an OpenClaw skill called trio-vision. Here's how it works 🧵

2/ The problem: cameras are everywhere but nobody watches them. Motion alerts go off for every shadow and cat. Enterprise video AI costs $50K+/year.

3/ The solution: describe what matters in plain English. "Alert me when a package is delivered." That's it.

4/ Works with any live stream — YouTube Live, Twitch, RTSP cameras, HLS. $0.01 per check, $0.02/min for continuous monitoring.

5/ Install in one command:
clawhub install trio-vision

Free 100 credits at console.machinefi.com

[screenshot of agent answering a camera question]
```
**PMF signal:** Likes, retweets, replies, link clicks
**Effort:** 20 min
**Hashtags:** #OpenClaw #AIAgent #ComputerVision #SmartHome

---

## PHASE 3: WEEK 2-3 — Content & Partnerships

### 3.1 Tutorial Blog Posts (3 articles)
**What:** SEO-optimized content targeting high-intent keywords.

| Article | Target Keyword | Platform |
|---------|---------------|----------|
| "How to Turn a $25 Camera into an AI Smart Camera in 5 Minutes" | "AI security camera DIY" | dev.to, Medium, Hashnode |
| "I Replaced My $10/month Nest Aware Subscription with trio-vision" | "Nest Aware alternative" | Reddit, blog |
| "How to Get AI Camera Alerts in Slack/Telegram/WhatsApp" | "AI camera alerts Slack" | dev.to |

**PMF signal:** Views, claps/reactions, "I tried this and..." comments
**Effort:** 2-3 hours per article

### 3.2 Comparison Content
**What:** Position trio-vision against known alternatives.

| Article | Angle |
|---------|-------|
| "trio-vision vs Frigate: Conversational AI vs NVR" | Target self-hosted crowd |
| "trio-vision vs Nest/Ring/Arlo subscriptions" | Cost savings angle |
| "Why trio-vision is not an NVR (and why that's the point)" | Positioning clarity |

**PMF signal:** Search traffic, "which should I use?" discussions
**Effort:** 1-2 hours per article

### 3.3 Integration Recipes (Compound Value)
**What:** Build 2-3 example workflows combining trio-vision with other OpenClaw skills.

| Recipe | Skills Combined | User Story |
|--------|----------------|------------|
| "Smart Porch Alert" | trio-vision + imsg/slack | "If person at door, send me a message with description" |
| "Delivery Tracker" | trio-vision + apple-notes | "Log every delivery with timestamp and AI description" |
| "Pet Monitor" | trio-vision + cron | "Check the pet cam every 30 min, summarize what the dog is doing" |

**PMF signal:** Recipe adoption, "I set this up and..." feedback
**Effort:** 1-2 hours per recipe

### 3.4 YouTube Smart Home Creator Outreach
**What:** Reach out to YouTube creators in the smart home space with a free demo.
**Targets:** The Hook Up, Everything Smart Home, Paul Hibbert, JuanStech, Smart Home Solver
**Action:** DM/email with "I built an AI skill that turns any RTSP camera into a smart camera — would you be interested in trying it? Free credits included."
**PMF signal:** Creator interest, video features, audience response
**Effort:** 30 min for outreach

---

## PHASE 4: WEEK 3-4 — Growth Loops & Challenges

### 4.1 "What Does My AI See?" Challenge
**What:** Social media challenge. Users point trio-vision at something unexpected and share the AI's description.
**Format:** Share on X/TikTok/Reddit with hashtag #WhatDoesMyAISee
**Angles:**
- "Security Camera Roast" — AI describes your messy desk/garage
- "Pet Watch" — what is my cat/dog actually doing all day?
- "Time-lapse Intelligence" — 24-hour summary of a location
**PMF signal:** Challenge participation, UGC volume, hashtag usage
**Effort:** Create the challenge post + 2-3 seed examples

### 4.2 Bounty Program: Best Use Case
**What:** 2-week contest. Submit your most creative trio-vision use case.
**Prize:** $500 in Trio API credits split across top 3
**Categories:** Most useful, most creative, best business use case
**PMF signal:** Submissions = real use cases you didn't think of. Each submission is free marketing content.
**Effort:** Set up rules, judge, announce

### 4.3 Automated Social Agent (Conway)
**What:** Deploy an always-on Conway agent that monitors public streams and posts interesting observations to X/Twitter.
**Example posts:**
- "trio-vision just spotted a sailboat on the San Francisco Bay cam 🌊"
- "Current at Times Square: 47 people visible, 3 yellow cabs, light rain"
**PMF signal:** Follower growth, engagement, "how did you do this?" questions
**Effort:** 2-3 hours to set up, then runs autonomously

---

## PHASE 5: ONGOING — Cross-Listing & Community

### 5.1 Directory Listings
**What:** List trio-vision everywhere skills/tools are discovered.

| Directory | URL | Status |
|-----------|-----|--------|
| ClawHub | clawhub.ai | ✅ Published |
| GitHub | github.com/drandrewlaw/trio-openclaw-skill | ✅ Live |
| awesome-openclaw-skills | github.com/VoltAgent/awesome-openclaw-skills | ⏳ Deferred (needs traction) |
| LobeHub Skills | lobehub.com/skills | 📝 Submit |
| OpenClawDir.com | openclawdir.com | 📝 Submit |
| OpenClawSkills.co | openclawskills.co | 📝 Submit |
| MCP directories | various | 📝 List if MCP interface exists |
| Product Hunt | producthunt.com | 📝 Launch with demo |
| Alternative-To | alternativeto.net | 📝 List under "AI video analytics" |

**PMF signal:** Listing traffic, referral installs
**Effort:** 30 min per directory

### 5.2 Community Seeding (Ongoing)
**What:** Monitor forums for questions trio-vision answers. Be helpful, not spammy.
**Where to watch:**
- r/homeassistant — "best AI for cameras"
- r/selfhosted — "camera monitoring solutions"
- r/smarthome — "smart alerts for cameras"
- Home Assistant forums
- Smart home Discord servers
**Action:** Set up alerts for keywords: "smart camera AI", "camera alerts AI", "vision AI camera", "alternative to Ring alerts"
**PMF signal:** Responses, upvotes, "I tried it" follow-ups
**Effort:** 15 min/day

### 5.3 LinkedIn B2B Angle
**What:** Position trio-vision for business use cases on LinkedIn.
**Angle:** Warehouse monitoring, retail foot traffic, construction site oversight — at $0.02/min instead of $50K/year enterprise solutions.
**Action:** Write 2-3 LinkedIn posts targeting operations managers, warehouse supervisors, retail owners.
**PMF signal:** Connection requests, "can this work for..." DMs
**Effort:** 30 min per post

---

## WILDCARD PLAYS (High Risk, High Reward)

### W1. "Agent-Powered Security Guard" Service
Deploy trio-vision on Conway watching a user's camera 24/7. The agent acts as an autonomous security guard that messages the user when something important happens. Position as "$0.02/min AI security guard" — cheaper than any human or enterprise solution. This is a productized service built on top of the skill.

### W2. Clawnema Integration
Your OpenClaw already has the Clawnema skill (virtual cinema for agents). Create a "trio-vision film festival" where agents watch interesting live camera feeds and provide commentary. Agents critique what they see on wildlife cams, city streams, etc. Pure entertainment angle that creates engagement.

### W3. "Camera Speed Dating"
Post trio-vision descriptions of different camera feeds on Moltbook without revealing the source. Other agents/users guess what the camera is watching based on the description. Gamification of the skill's output.

### W4. Partner with TrioClaw
TrioClaw (github.com/machinefi/TrioClaw) is a Go binary for camera monitoring. Cross-promote: TrioClaw for technical users who want a binary, trio-vision for OpenClaw users who want chat-native experience. Same API, different distribution channels.

---

## PMF MEASUREMENT DASHBOARD

Track these metrics weekly:

| Metric | Source | Target (Week 1) | Target (Month 1) |
|--------|--------|-----------------|-------------------|
| ClawHub installs | clawhub inspect trio-vision | 50 | 500 |
| GitHub stars | github.com/drandrewlaw/trio-openclaw-skill | 20 | 200 |
| Trio API signups (from skill) | console.machinefi.com | 10 | 100 |
| HN upvotes | Show HN post | 50+ | - |
| Reddit upvotes (total) | 5 subreddit posts | 100+ | - |
| Discord questions | OpenClaw Discord | 5 | 30 |
| Moltbook engagement | Moltbook post | 20+ | - |
| Demo URL visits | Conway sandbox | - | 500 |
| "How do I..." questions | All channels | 5 | 50 |
| Negative feedback / "not useful" | All channels | Track | Track |

**PMF = achieved when:**
- Unprompted installs exceed 10/day
- Users describe use cases YOU didn't think of
- People ask "can it do X?" (expansion demand)
- Retention: users who install continue using after 7 days

---

## EXECUTION ORDER (One-Page Summary)

**Today:**
1. ☐ Post on Moltbook
2. ☐ Post on OpenClaw Discord
3. ☐ Post on OpenClaw GitHub Discussions
4. ☐ Submit to LobeHub, OpenClawDir, OpenClawSkills directories

**This week:**
5. ☐ Deploy Conway live demo
6. ☐ Show HN post (Tuesday/Wednesday 8-9am EST)
7. ☐ Reddit posts (5 subreddits)
8. ☐ Twitter/X launch thread
9. ☐ Create trio-vision-demo meta-skill

**Week 2-3:**
10. ☐ Write 3 tutorial blog posts
11. ☐ Build 2-3 integration recipes
12. ☐ YouTube creator outreach
13. ☐ Comparison content (vs Frigate, vs Nest)
14. ☐ LinkedIn B2B posts

**Week 3-4:**
15. ☐ Launch #WhatDoesMyAISee challenge
16. ☐ Deploy automated social agent on Conway
17. ☐ Launch bounty program
18. ☐ Product Hunt launch with live demo

**Ongoing:**
19. ☐ Community seeding (15 min/day)
20. ☐ Track PMF dashboard weekly
21. ☐ Iterate based on signals
