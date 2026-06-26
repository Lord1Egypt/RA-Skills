# Worked Example: From Idea to 5Q to PR-FAQ

## Table of Contents

1. [The rough idea](#idea)
2. [5 Questions — drafted answers](#five-questions)
3. [Resulting PR-FAQ](#prfaq)

---

## The Rough Idea {#idea}

> "We should build a tool that helps small restaurant owners manage their online
> reviews across Google, Yelp, and TripAdvisor from one place. They waste hours
> checking each site and often miss negative reviews until it's too late."

---

## 5 Questions — Drafted Answers {#five-questions}

### 1. Who is the customer?

Independent restaurant owners and general managers operating 1-3 locations in the
US, with annual revenue between $500K-$5M. They are hands-on operators who
personally handle or oversee their restaurant's online reputation but have no
dedicated marketing staff. They are digitally literate enough to use a smartphone
app and email, but not technical — they do not want to learn new software.

### 2. What is the customer problem or opportunity?

These owners must manually check 3-5 review platforms daily to stay on top of
customer feedback. On average, they spend 45 minutes per day across platforms, and
negative reviews go unanswered for 3-5 days — by which point the customer has told
10 friends and moved on. A single unanswered 1-star review can reduce a
restaurant's click-through rate by 10%. They have no way to spot trends (e.g.,
"complaints about wait times spiked this month") without reading every review
manually.

### 3. What is the most important customer benefit?

Never miss a negative review again: get alerted within 15 minutes of any review
under 3 stars, with a suggested response ready to personalize and send — reducing
average response time from 3-5 days to under 2 hours.

### 4. How do we know what the customer needs or wants?

- Interviewed 23 restaurant owners in Q3 2025; 19/23 cited "keeping up with
  reviews" as a top-3 operational pain point.
- Analysis of 500 restaurants on Google shows that establishments responding to
  negative reviews within 24 hours have 0.3 stars higher average rating.
- Competitor analysis: existing tools (Birdeye, Podium) target multi-location
  enterprises at $300+/month. No affordable option exists for single-location
  restaurants.
- Restaurant owner Facebook groups (12,000+ members) show weekly posts asking
  "how do you keep up with reviews?"

### 5. What does the customer experience look like?

Maria owns a taqueria in Austin. She signs up via the website in 2 minutes by
connecting her Google Business and Yelp accounts. The next morning, she gets a push
notification: "New 2-star review on Google: 'Waited 40 minutes for tacos.'" The app
shows the review with a suggested response: "Hi [Name], I'm sorry about the wait.
We had an unusually busy evening. I'd love to make it right — your next meal is on
me. Please ask for Maria." She edits slightly and taps Send. The response posts to
Google within seconds. At the end of the week, she opens the app and sees a summary:
"12 new reviews this week (avg 4.2 stars). Trending topic: wait times mentioned in 4
reviews." She decides to adjust staffing on Friday nights.

---

## Resulting PR-FAQ {#prfaq}

### Press Release

# ReviewPulse — Never Miss a Review Again

**Austin, TX** — **January 15, 2026** — ReviewPulse today announced the launch of
its review management platform built specifically for independent restaurant owners
who want to stay on top of customer feedback without spending hours checking multiple
websites.

Independent restaurant operators spend an average of 45 minutes every day manually
checking Google, Yelp, and TripAdvisor for new reviews. When a negative review
appears, it often takes 3-5 days to notice and respond — long after the frustrated
customer has moved on and told their friends. For a small restaurant operating on
thin margins, a single unaddressed 1-star review can measurably reduce new customer
traffic.

ReviewPulse monitors all major review platforms in real time and alerts owners within
15 minutes of any review under 3 stars. Each alert includes a personalized response
suggestion that the owner can edit and post in one tap, without ever opening the
review site directly.

"Restaurant owners are passionate about their food and their guests, but they
shouldn't need to spend their mornings refreshing Yelp," said Alex Chen, CEO of
ReviewPulse. "We built ReviewPulse so owners can respond to feedback as fast as they
respond to a guest at the door."

When a new review appears on any connected platform, ReviewPulse sends a push
notification to the owner's phone. The owner sees the review text, star rating, and
a draft response tailored to the review's content. They edit if needed, tap "Send,"
and the response is posted. A weekly summary email highlights review trends — such as
recurring mentions of wait times or service — so owners can make operational changes
based on real customer data.

"I used to dread opening Yelp. Now I just handle it from my phone between the lunch
and dinner rush," said Maria Torres, owner of La Casita Taqueria in Austin. "Last
month I caught a bad review within 10 minutes and the customer actually came back and
updated it to 4 stars."

ReviewPulse is available today starting at $29/month for a single location. Sign up
at reviewpulse.com/start with a 30-day free trial.

---

### Frequently Asked Questions

#### External

**Q: What is ReviewPulse?**
A: ReviewPulse is a review management tool that monitors Google, Yelp, and
TripAdvisor for new reviews and alerts restaurant owners in real time, with suggested
responses ready to send.

**Q: Who is ReviewPulse for?**
A: Independent restaurant owners and managers operating 1-3 locations who want to
stay on top of online reviews without hiring dedicated marketing staff.

**Q: How does it work?**
A: Connect your Google Business, Yelp, and TripAdvisor accounts during a 2-minute
setup. ReviewPulse monitors for new reviews and sends push notifications for anything
under 3 stars within 15 minutes. Each alert includes a suggested response you can
personalize and post in one tap. A weekly email summarizes trends across all reviews.

**Q: How much does it cost?**
A: $29/month for a single location, $49/month for up to 3 locations. Annual plans
receive a 20% discount. All plans include a 30-day free trial.

**Q: How is this different from Birdeye or Podium?**
A: Birdeye and Podium are designed for multi-location enterprises with dedicated
marketing teams, starting at $300+/month. ReviewPulse is built for the independent
operator who wants a simple, affordable tool — not an enterprise platform.

**Q: Is my data secure?**
A: ReviewPulse uses read-only API access to review platforms where available and
OAuth authentication. We never store your platform passwords and all data is
encrypted in transit and at rest.

#### Internal

**Q: Why should we build this now?**
A: The restaurant industry's recovery from COVID has driven a surge in online
ordering and review activity. Review volume on Google for restaurants grew 35% YoY in
2025. Independent restaurants — 70% of all US restaurants — remain underserved by
existing enterprise-focused review tools.

**Q: How big is the opportunity?**
A: There are approximately 750,000 independent restaurants in the US. At $29/month,
capturing 1% of this market represents $2.6M ARR. The adjacent market (retail,
salons, hotels) offers significant expansion potential.

**Q: What are the biggest risks?**
A: (1) Platform API access — Google and Yelp could restrict API access or change
terms. Mitigation: use official APIs, maintain compliance, build relationships with
platform partner teams. (2) Response quality — AI-generated responses that sound
robotic could damage restaurant reputations. Mitigation: always require human review
before posting; optimize suggestion quality through customer feedback loops.

**Q: What are the key metrics for success?**
A: (1) Average response time to negative reviews <2 hours (from 3-5 day baseline).
(2) 70% of suggested responses sent with minimal edits. (3) 1,000 paying customers
within 6 months of launch. (4) Net Promoter Score >50.

**Q: What are we NOT doing?**
A: We are not building: review generation/solicitation features, social media
management, POS integration, or multi-language support in V1.
