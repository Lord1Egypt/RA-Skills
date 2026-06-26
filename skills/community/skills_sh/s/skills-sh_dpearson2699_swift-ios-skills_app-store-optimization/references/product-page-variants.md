# Product Page Variants

Custom Product Pages, product page optimization (A/B testing), and in-app event configuration for App Store discoverability and conversion.

## Contents

- [Custom Product Pages](#custom-product-pages)
- [Product Page Optimization Tests](#product-page-optimization-tests)
- [In-App Event Configuration](#in-app-event-configuration)
- [Screenshot Caption Copywriting](#screenshot-caption-copywriting)

## Custom Product Pages

### Setup in App Store Connect

1. Navigate to **App Store Connect > App > Custom Product Pages**.
2. Create a new Custom Product Page -- each page needs a reference name (internal only) and a locale.
3. Customize screenshots, app preview videos, promotional text, and assigned keywords for the target audience.
4. Submit the page for review -- Custom Product Pages go through App Review like regular submissions.
5. Once approved, the page is visible through its unique URL and, if configured, through assigned App Store search keywords.

### URL structure

Custom Product Pages use the format:

```
https://apps.apple.com/app/id{APP_ID}?ppid={CUSTOM_PAGE_ID}
```

The `ppid` parameter directs users to the custom page instead of the default product page. Use these URLs in:

- Apple Search Ads ad group URLs
- Social media campaign links
- Email marketing campaigns
- Web landing pages
- QR codes in physical marketing

### Search visibility and deep links

- You can create up to 70 Custom Product Pages per app.
- Assign keywords from the latest approved app version to make an approved, visible custom page appear for matching App Store searches instead of the default page.
- Use unique keyword sets per custom page so App Store search can choose the most relevant page.
- Optional app deep links can send users on iOS 18 or iPadOS 18 or later to specific in-app content after they tap Open. Deep links must be approved with the custom page before they work for users.

### Campaign-to-page mapping

Plan Custom Product Pages around distinct acquisition channels:

| Channel | Page name convention | Screenshot strategy |
|---------|---------------------|---------------------|
| Search Ads -- brand terms | `Search-Brand` | Highlight brand trust and breadth |
| Search Ads -- feature terms | `Search-{Feature}` | Lead with the specific feature the user searched for |
| Search Ads -- competitor terms | `Search-Competitor` | Emphasize differentiators vs. category norms |
| Social -- Instagram/TikTok | `Social-Visual` | Visual-first screenshots matching social creative style |
| Social -- Twitter/X | `Social-Utility` | Feature-focused, less visual polish |
| Email -- existing users | `Email-Upgrade` | New feature highlights for re-engagement |
| Web -- blog/PR | `Web-Editorial` | Award badges, press quotes, credibility signals |

### Management

- Audit Custom Product Pages quarterly. Remove pages for ended campaigns.
- Track performance per page in App Analytics -- compare conversion rates against the default page.
- App Analytics reports custom page metrics after the page receives at least five first-time downloads.
- Custom Product Pages count toward the 70-page limit per app. Reserve capacity for seasonal or ad-hoc campaigns.

## Product Page Optimization Tests

### Test design patterns

Each test compares the original product page against up to three treatments. For clearer results, design each test around one hypothesis even when you create multiple treatments.

#### Icon test

- **Hypothesis:** A revised icon with [specific change] will increase tap-through rate by improving shelf appeal.
- **Treatment:** Alternate app icon that [describes the specific difference].
- **Duration:** 7-14 days minimum.
- **Success metric:** Conversion rate (impressions to first-time downloads).

#### Screenshot order test

- **Hypothesis:** Leading with [screen X] instead of [screen Y] will increase conversion by showing the primary value proposition sooner.
- **Treatment:** Reorder the first 3 screenshots.
- **Duration:** 7-14 days minimum.
- **Success metric:** Conversion rate.

#### Screenshot content test

- **Hypothesis:** Benefit-oriented captions will outperform feature-descriptive captions.
- **Treatment:** Replace captions on the first 3 screenshots with benefit-focused copy.
- **Duration:** 7-14 days minimum.
- **Success metric:** Conversion rate.

### Running a test

1. In App Store Connect, go to **Product Page Optimization**.
2. Choose up to three treatments and the element to test (icon, screenshots, or preview video).
3. Upload the treatment assets.
4. Set the traffic proportion. App Store Connect splits that treatment traffic evenly across treatments.
5. Select the localizations to include; all supported localizations are selected by default.
6. Start the test and monitor App Analytics. A test runs for up to 90 days or until manually stopped.

### Interpreting results

- App Store Connect reports conversion rate for control vs. treatment with a confidence interval.
- Results appear after at least five first-time downloads are associated with the test.
- Do not apply a treatment until the result shows 90%+ confidence.
- A 2-5% conversion lift is meaningful at scale -- do not dismiss small wins.
- If App Store Connect marks a test as likely inconclusive, the current traffic and lift may not be enough to reach confidence within the 90-day window. Consider a stronger creative change or a higher-traffic period.
- After applying a winner, wait at least one release cycle before starting the next test to establish a clean baseline.

### Limitations

- Only one test at a time per app.
- Product Page Optimization tests are unavailable for Custom Product Pages, Apple Watch product pages, and iMessage product pages.
- Low-traffic apps may need longer to reach 90% confidence, and some tests may remain inconclusive.
- App icons used in treatments must be included in the app binary for the current App Store version. Applying a treatment applies screenshots and previews; make an icon the default in a future app version if that icon should persist broadly.

## In-App Event Configuration

### Event metadata template

| Field | Limit | Guidelines |
|-------|-------|-----------|
| **Event name** | 30 chars | Keyword-rich, action-oriented. "Spring Fitness Challenge" not "Our Spring Event" |
| **Short description** | 50 chars | One compelling sentence visible on the event card |
| **Long description** | 120 chars | Expand on what the user will experience or win |
| **Event card image** | 1920x1080 (16:9) | High-contrast, legible at small sizes, no text smaller than 24pt |
| **Badge** | Preset options | Match badge type to event nature (see SKILL.md table) |
| **Deep link** | URL | Optional. Links to the in-app event content |

### Scheduling strategy

Plan events to maintain continuous App Store visibility:

```
Week 1-2:  [Event A -- "Spring Challenge" (Challenge badge)]
Week 3-4:  [Event B -- "New Workout Library" (Major Update badge)]
Week 5-6:  [Event C -- "Summer Kickoff" (Special Event badge)]
```

Overlap the end of one event with the start of the next by 1-2 days. This prevents gaps where the app has no event card in search results.

### Event timing rules

- Events can be published up to 14 days before they start.
- Events must run at least 15 minutes and can run for up to 31 days.
- You can publish up to 10 In-App Events on the App Store at a time and keep up to 15 approved events per app in App Store Connect.
- Events are visible in search results and on the product page during their active window.
- Ended events are removed from the store automatically.
- Schedule events around real moments (feature releases, content drops, seasonal relevance) -- manufactured events without real in-app content feel hollow and may be rejected by App Review.

### Maximizing search impact

- Use the event name and short description as visible search-result copy. Include terms that match the event's real content and user intent.
- Choose a badge type that matches the actual event nature -- the badge appears prominently on the event card.
- In-app events can appear on the Today tab, in search results, and on the app's product page. Apple's editorial team curates which events are featured.

## Screenshot Caption Copywriting

### Benefit-oriented vs. feature-descriptive

| Feature-descriptive (weak) | Benefit-oriented (strong) |
|---------------------------|--------------------------|
| Calendar View | Never miss a deadline |
| Dark Mode | Easy on your eyes, day or night |
| Cloud Sync | Your data, everywhere |
| Analytics Dashboard | See what is working |
| Collaboration Tools | Build together in real time |
| Offline Mode | Works without internet |
| Custom Themes | Make it yours |
| Push Notifications | Stay in the loop |

### Caption structure

The strongest captions follow one of three patterns:

1. **Outcome-first:** State the result the user gets. "Track every mile" > "GPS Running Tracker".
2. **Problem-solver:** Name the pain point and imply the solution. "No more forgotten passwords" > "Password Manager".
3. **Social proof:** Imply scale or trust. "Join 10M users" > "Popular App".

### Per-audience caption variants

Different Custom Product Pages should use different captions for the same screenshots:

| Screenshot | Search Ads -- fitness terms | Social -- visual audience | Email -- lapsed users |
|-----------|---------------------------|--------------------------|----------------------|
| Workout screen | "Hit your goals every week" | "Your workout, beautifully tracked" | "We added 50 new workouts" |
| Progress chart | "See your streak grow" | "Watch your progress unfold" | "Your history is still here" |
| Social feature | "Challenge your friends" | "Share your wins" | "Your friends are still active" |

Tailor the emotional angle to the acquisition channel while keeping the screenshot content consistent.
