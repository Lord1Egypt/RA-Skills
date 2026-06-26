# App Store Review Guidelines — Complete Reference

**Official URL:** https://developer.apple.com/app-store/review/guidelines/
**Last Updated:** November 2025

The App Store Review Guidelines are organized into **five main sections**. This document provides the complete breakdown with specific rule numbers, requirements, and common violation patterns.

---

## Section 1: Safety

### 1.1 Objectionable Content

| Guideline | Requirement | Common Violations |
|-----------|-------------|-------------------|
| **1.1.1** | No defamatory, discriminatory, or mean-spirited content targeting religion, race, sexual orientation, gender, national/ethnic origin, or other targeted groups | Hate speech in UGC, offensive memes, discriminatory filters |
| **1.1.2** | No realistic portrayals of violence, torture, death, or abuse | Graphic violence in games, torture simulations, animal cruelty |
| **1.1.3** | No content encouraging illegal weapon use or facilitating firearms purchases | Gun sales apps, weapon modification guides, 3D print weapon files |
| **1.1.4** | No overtly sexual or pornographic material | Adult content, explicit imagery, suggestive content in Kids category |
| **1.1.5** | No inflammatory religious commentary or inaccurate/misleading quotations of religious texts | Cult recruitment, religious mockery, misquoted scriptures |
| **1.1.6** | No false information or trick/joke functionality | Fake virus scanners, prank emergency calls, fake location trackers |
| **1.1.7** | No exploitation of recent tragedies (conflicts, terrorist attacks, epidemics) | Tragedy-themed games, insensitive content about current events |

### 1.2 User-Generated Content (UGC)

**Apps with UGC MUST include:**

| Requirement | Implementation |
|-------------|----------------|
| **Content Filtering** | Method for filtering objectionable material before posting |
| **Reporting Mechanism** | Mechanism to report offensive content with timely responses |
| **Blocking Capability** | Ability to block abusive users |
| **Contact Information** | Published contact information for content issues |

**1.2.1 Creator Content:**
- Apps must provide age restriction mechanisms based on verified or declared age
- Content creators must be able to limit access to age-appropriate audiences

### 1.3 Kids Category Requirements

**Strict requirements for Kids category apps:**

| Requirement | Details |
|-------------|---------|
| **No external links** | Unless behind parental gate with age verification |
| **No purchasing** | Unless behind parental gate |
| **No third-party analytics** | Cannot collect personally identifiable information |
| **Limited advertising** | No third-party ads; limited contextual ads may be permitted |
| **Privacy compliance** | Must comply with COPPA and similar children's privacy laws |

### 1.4 Physical Harm

| Guideline | Requirement |
|-----------|-------------|
| **1.4.1** | Medical apps must disclose data/methodology for accuracy claims |
| **1.4.2** | Drug dosage calculators require FDA approval or come from approved entities |
| **1.4.3** | No apps encouraging tobacco, vape, illegal drugs, or excessive alcohol |
| **1.4.4** | No encouragement of reckless behavior |
| **1.4.5** | No apps that primarily promote gambling or lotteries |

### 1.5 Developer Information

- Must include accurate, up-to-date contact information
- Support URL must provide easy way to contact developer
- Cannot hide or obscure contact information

### 1.6 Data Security

- Must implement appropriate security measures for user data
- Prevent unauthorized access by third parties
- Use secure transmission (HTTPS) for sensitive data
- Implement appropriate encryption for stored data

---

## Section 2: Performance

### 2.1 App Completeness

| Requirement | Details |
|-------------|---------|
| **Final version** | Submissions must be final versions, not betas |
| **Complete metadata** | All fields filled, no placeholders |
| **Bug-free** | Tested on-device for crashes and stability |
| **Demo account** | If login required, provide working demo credentials |
| **Live backend** | Backend services must be live during review |
| **Review notes** | Explain non-obvious features or functionality |

### 2.2 Beta Testing

- Demos, betas, and trial versions belong on TestFlight
- TestFlight apps cannot be distributed for compensation
- Production App Store is for finished products only

### 2.3 Accurate Metadata

| Guideline | Requirement | Common Violations |
|-----------|-------------|-------------------|
| **2.3.1** | No hidden, dormant, or undocumented features | Secret admin panels, hidden gambling, A/B tested illegal features |
| **2.3.2** | Clearly indicate if items require additional purchases | Hidden paywalls, surprise IAP requirements |
| **2.3.3** | Screenshots must show app in use | Using splash screens, login pages, or title art only |
| **2.3.4** | Previews may only use video screen captures | Using non-app footage, pre-rendered graphics |
| **2.3.5** | Select appropriate category | Wrong category to avoid competition |
| **2.3.6** | Answer age rating questions honestly | Underrating to reach wider audience |
| **2.3.7** | App names ≤30 characters; no keyword stuffing | "Best Photo Editor Camera Filter Gallery App" |
| **2.3.8** | Metadata must be appropriate for all audiences (4+) | Explicit content in description |
| **2.3.9** | Secure rights for all materials in icons/screenshots | Using copyrighted images without permission |
| **2.3.10** | No references to other mobile platforms in metadata | "Also available on Android" |
| **2.3.12** | "What's New" must describe significant changes | Using for marketing messages |

### 2.4 Hardware Compatibility

| Requirement | Details |
|-------------|---------|
| **iPad compatibility** | iPhone apps should run on iPad whenever possible |
| **Power efficiency** | No rapid battery drain, excessive heat |
| **No mining** | No cryptocurrency mining on device |
| **No system suggestions** | Never suggest device restart or system modifications |
| **API usage** | Use only documented APIs for device capabilities |

---

## Section 3: Business

### 3.1 Payments

**3.1.1 In-App Purchase REQUIRED for:**
- Unlocking features or functionality
- Subscriptions to digital content
- Game currencies
- Game levels
- Premium content
- Access to full version from "lite" version
- Ad removal

**3.1.3 Exceptions (Other Payment Methods Allowed):**

| Exception | Description |
|-----------|-------------|
| **(a) Reader Apps** | Magazines, newspapers, books, audio, music, video (previously purchased elsewhere) |
| **(b) Multiplatform Services** | Content purchased on other platforms |
| **(c) Enterprise Services** | B2B apps for organizations |
| **(d) Person-to-Person Services** | Real-time 1:1 services (tutoring, medical consultations) |
| **(e) Physical Goods/Services** | Consumed outside the app |
| **(f) Free Stand-alone Companions** | To paid web-based tools |
| **(g) Advertising Management Apps** | For managing ad campaigns |

**3.1.4 Content Codes:**
- Apps can sell codes for digital content purchased elsewhere
- Subscription gift cards allowed

**3.1.5 Cryptocurrencies:**
- Wallets allowed (must be from organization accounts)
- No on-device mining
- Exchanges only in properly licensed jurisdictions
- ICOs must come from established financial institutions

### 3.2 Unacceptable Business Models

| Prohibited | Examples |
|------------|----------|
| **App Store-like interfaces** | Creating alternate app stores |
| **Artificial ad inflation** | Manipulating impression counts |
| **Ad-focused apps** | Apps designed predominantly for ads |
| **Location/carrier restrictions** | Arbitrarily limiting users |
| **Binary options trading** | High-risk trading apps |
| **Predatory lending** | Personal loans >36% APR or <60 day repayment |

---

## Section 4: Design

### 4.1 Copycats

- Must have original ideas
- Cannot impersonate other apps
- Cannot use another developer's icon, brand, or product name without approval
- "Inspired by" must be truly original execution

### 4.2 Minimum Functionality

| Requirement | Details |
|-------------|---------|
| **Beyond website** | Must include features beyond a repackaged website |
| **Lasting value** | Must provide lasting entertainment value or adequate utility |
| **Rich AR** | ARKit apps must provide rich, integrated AR experiences |
| **Not marketing** | Apps cannot primarily be marketing materials or link collections |
| **Web content** | Web content that could be a website will be rejected |

### 4.3 Spam

- No multiple Bundle IDs of the same app
- Avoid saturated categories (fart apps, flashlight apps, etc.)
- Minor variations of the same app will be rejected

### 4.7 Mini Apps, Games, Chatbots, Emulators

| Requirement | Details |
|-------------|---------|
| **Privacy** | Must follow all privacy guidelines |
| **Content filtering** | Must include content filtering and reporting |
| **API restrictions** | Cannot extend native platform APIs without permission |
| **Data sharing** | Cannot share data without explicit user consent |
| **Indexing** | Must provide index of software with universal links |
| **Emulators** | Allowed with content restrictions and author consent |

### 4.8 Login Services

**If using third-party login (Facebook, Google, etc.), must ALSO offer:**
- Another login option that limits data collection to name and email
- Option to keep email private
- No advertising data collection without consent

**Exceptions:**
- Company's own account system only
- Education/enterprise apps
- Government ID systems
- Clients for specific third-party services

### 4.9 Apple Pay

- Must disclose all purchase information before sale
- For recurring payments, must disclose: renewal term, what's provided, charges, how to cancel

### 4.10 Monetizing Built-In Capabilities

**Cannot charge for access to:**
- Push Notifications
- Camera or microphone
- Gyroscope or accelerometer
- Apple Music
- iCloud storage
- Screen Time APIs
- Any system-provided functionality

---

## Section 5: Legal

### 5.1 Privacy

**5.1.1 Data Collection and Storage:**
- ALL apps must include privacy policy link
- Privacy policy must identify data collected, how collected, all uses
- Must confirm third parties provide equal protection
- Must explain data retention/deletion policies
- Must describe how to revoke consent

**5.1.2 Data Use and Sharing:**
- Cannot use data beyond stated purposes
- Cannot share with third parties not disclosed in privacy policy
- Cannot sell data to data brokers or advertising platforms
- Cannot gate features on tracking consent or incentivize tracking

**5.1.3 Health and Research:**
- Health apps must have ethics board approval
- Must provide data access and portability
- Must not share health data with third parties without consent

**5.1.4 Kids:**
- Cannot collect data from children without verifiable parental consent
- Must comply with COPPA and similar regulations

**Privacy Manifests (Required since May 2024):**
- Must declare all data types collected
- Must include "required reason APIs" usage justification
- Third-party SDKs must include their own privacy manifests

### 5.2 Intellectual Property

- Must have rights to all content
- Must respect third-party trademarks
- Must not infringe patents
- Music/video licensing must be verified

### 5.3 Gaming, Gambling, and Lotteries

| Requirement | Details |
|-------------|---------|
| **Real gambling** | Only from licensed entities, geo-restricted |
| **Simulated gambling** | Allowed with age gates |
| **Contests** | Must clearly state rules, eligibility, prizes |
| **Lotteries** | Only from licensed operators |

### 5.6 Developer Code of Conduct

| Guideline | Requirement |
|-----------|-------------|
| **5.6.1** | Treat customers with respect |
| **5.6.2** | Provide verifiable, truthful information |
| **5.6.3** | No discovery fraud (manipulating charts, search, reviews) |
| **5.6.4** | Maintain app quality |

---

## Quick Reference: Most Common Rule Violations

| Guideline | Issue | Prevention |
|-----------|-------|------------|
| 5.1.1 | Missing privacy policy | Include link in app and metadata |
| 2.3.3 | Bad screenshots | Show app in actual use |
| 2.1 | Crashes during review | Test on real devices |
| 3.1.1 | Wrong payment method | Use IAP for digital goods |
| 1.2 | UGC without moderation | Add filtering, reporting, blocking |
| 2.3.7 | App name too long | Keep under 30 characters |
| 5.1.2 | Privacy labels incorrect | Match labels to actual collection |
| 4.2 | Minimum functionality | Ensure utility beyond website |

---

*Guidelines updated November 2025. Always verify against current Apple documentation.*
