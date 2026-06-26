# Landing Page Design - Sharp Edges

## Navigation Trap

### **Id**
navigation-trap
### **Summary**
Including full site navigation on landing pages
### **Severity**
critical
### **Situation**
  Landing page includes full nav: [Home] [About] [Features] [Pricing] [Blog] [Contact]
  Every link is an exit. You paid for that visitor. Navigation steals them.
  
### **Why**
  Landing pages have ONE goal. Every link that isn't that goal is a leak.
  Full navigation can reduce conversions by 30-50%. Visitors click "Blog",
  read an article, leave. Never convert.
  
### **Solution**
  # Remove all navigation
  Landing page ≠ Website page
  One goal = One action
  
  # What to KEEP:
  ✓ Logo (optionally linked to homepage)
  ✓ Same-page anchor links
  ✓ CTA button
  
  # What to REMOVE:
  ✗ Full navigation
  ✗ Footer with links
  ✗ Social links
  ✗ "Learn more" to other pages
  ✗ Blog links
  
### **Symptoms**
  - High navigation clicks
  - Low time on page before exit
  - Traffic leaking to other pages
  - Low conversion despite traffic
### **Detection Pattern**
<nav|navigation|class="nav"|class="menu"

## Slow Load Death

### **Id**
slow-load-death
### **Summary**
Page takes too long to load
### **Severity**
critical
### **Situation**
  Page load time: 5+ seconds. Mobile load time: 8+ seconds.
  Beautiful page that nobody ever sees.
  
### **Why**
  1 second delay = 7% conversion loss. 3 second delay = 32% will leave.
  5 second delay = 90% bounce probability. Speed is conversion.
  Google penalizes slow pages. Mobile is often 2x slower.
  
### **Solution**
  # Optimize images:
  - WebP format
  - Lazy loading
  - Right-sized (not scaled in browser)
  - Compressed
  
  # Minimize resources:
  - Critical CSS only
  - Defer non-essential JS
  - Reduce third-party scripts
  
  # Core Web Vitals targets:
  - LCP < 2.5s
  - FID < 100ms
  - CLS < 0.1
  
  # Speed targets:
  Desktop: <2s | Mobile: <3s
  
### **Symptoms**
  - High bounce rate
  - Users leaving before page loads
  - Poor Core Web Vitals scores
  - Mobile conversion much lower than desktop
### **Detection Pattern**


## Cta Cemetery

### **Id**
cta-cemetery
### **Summary**
CTAs buried, hidden, or missing above the fold
### **Severity**
high
### **Situation**
  Beautiful hero image, long headline, paragraph of text.
  CTA location: Below the fold. CTA visibility: Low contrast. CTA text: "Submit".
  
### **Why**
  If they can't find it, they can't click it. Most visitors never scroll.
  CTA must be immediately visible. Visual hierarchy should point to CTA.
  
### **Solution**
  # CTA requirements:
  1. Above the fold - Visible without scrolling
  2. High contrast color - Stands out from page
  3. Large enough - 44x44px minimum
  4. Action-oriented text - "Start free trial" not "Submit"
  5. Repeated throughout page
  
  # Squint test:
  Squint at your page. Can you still find the CTA?
  If not, it needs more prominence.
  
  # CTA placement:
  - After hero (above fold)
  - After benefits section
  - After social proof
  - Final section
  
### **Symptoms**
  - Low click-through rates
  - Users scrolling past CTA
  - Where do I sign up?
  - Heatmaps show no CTA engagement
### **Detection Pattern**


## Message Mismatch

### **Id**
message-mismatch
### **Summary**
Landing page doesn't match the ad that sent them there
### **Severity**
critical
### **Situation**
  Ad says: "50% off running shoes"
  Landing page says: "Explore our athletic collection"
  Visitor thinks: "Did I click the wrong link?" → Bounces
  
### **Why**
  Visitors arrive with expectations. You have 3 seconds to confirm them.
  Mismatch = immediate exit. They came for running shoes, you showed them generic catalog.
  
### **Solution**
  # Message match requirements:
  1. Ad headline → Landing page headline (same words)
  2. Same offer, same language
  3. Visual consistency (colors, imagery)
  4. Offer clearly visible
  
  # Dynamic landing pages:
  - Different versions for different ads
  - Keyword insertion in headlines
  - Personalized content
  
  # Bad:
  Ad: "Free project management software"
  LP: "The all-in-one productivity suite"
  
  # Good:
  Ad: "Free project management software"
  LP: "Free Project Management Software - Start today"
  
### **Symptoms**
  - High bounce rate from ads
  - Low quality scores in ads
  - "Scent" broken
  - Visitors confused on arrival
### **Detection Pattern**


## Form Field Fiasco

### **Id**
form-field-fiasco
### **Summary**
Forms with too many fields
### **Severity**
high
### **Situation**
  Lead capture form with 11 fields: name, email, phone, company,
  company size, job title, industry, budget, message, how did you hear...
  
### **Why**
  Each field = friction = drop-off. 4 fields → 3 fields = 50% more conversions.
  Users guard their information. Every field you don't need costs you leads.
  
### **Solution**
  # Minimum viable fields:
  - Lead gen: Email only (or + first name)
  - Trial signup: Email + password
  - Demo request: Name + email + company
  
  # Progressive profiling:
  - Get email first
  - Ask more later (in-product, email nurture)
  - Build profile over time
  
  # Field counts:
  Ideal: 1-3 fields
  Acceptable: 4-5 fields
  Too many: 6+ fields
  
  # For each field ask: "Do we need this NOW?"
  If no, remove it.
  
### **Symptoms**
  - Low form completion rate
  - Users abandoning mid-form
  - Fake data submitted
  - High cost per lead
### **Detection Pattern**


## Mobile Afterthought

### **Id**
mobile-afterthought
### **Summary**
Designing for desktop first or only
### **Severity**
critical
### **Situation**
  Desktop design: Beautiful. Mobile: Hero squashed, text unreadable,
  CTA tiny, form unusable, load time: 12 seconds.
  
### **Why**
  50-70% of traffic is mobile. Mobile has less patience, more friction.
  If 65% of your traffic is mobile and mobile converts at 1% vs desktop 5%,
  you're losing most of your potential customers.
  
### **Solution**
  # Mobile-first design:
  1. Design for mobile first, expand to desktop
  2. Touch-friendly: 44x44px minimum targets
  3. Readable without zoom: 16px minimum
  4. Fast on mobile: <3 seconds
  5. Thumb-zone CTA: Easy reach
  
  # Mobile checklist:
  □ CTA above fold on mobile
  □ Text readable without zoom
  □ Touch targets 44px+
  □ No horizontal scroll
  □ Form usable on phone
  □ No hover-only actions
  
### **Symptoms**
  - Mobile conversion much lower
  - Mobile bounce much higher
  - Pinch-to-zoom required
  - Touch targets missed
### **Detection Pattern**


## Social Proof Desert

### **Id**
social-proof-desert
### **Summary**
Landing page with no credibility signals
### **Severity**
high
### **Situation**
  Page claims: "The best project management tool. Trusted by teams worldwide."
  Proof: None. Logos: None. Testimonials: None. Numbers: None.
  
### **Why**
  Claims without proof are ignored. Trust must be established.
  Other customers' voices > your voice. "Says who? Prove it."
  
### **Solution**
  # Social proof types:
  1. Customer logos (5-7 recognizable brands)
  2. Testimonials (real quotes, real names, photos)
  3. Numbers ("10,000+ teams", "4.9/5 rating")
  4. Trust badges (security, awards, certifications)
  5. Media mentions
  
  # Strategic placement:
  - Hero: Logo bar
  - Benefits section: Testimonials
  - Near CTA: Reviews/ratings
  - Footer: Full logos
  
  # Make proof specific:
  Not: "Great tool!"
  But: "Saved us 10 hours/week on reporting" - Jane, Acme Corp
  
### **Symptoms**
  - Why should I trust you?
  - Low conversion despite traffic
  - High bounce after reading claims
  - No third-party validation
### **Detection Pattern**


## Value Prop Vacuum

### **Id**
value-prop-vacuum
### **Summary**
Headline doesn't communicate value proposition
### **Severity**
critical
### **Situation**
  Hero headline: "Welcome to our platform"
  Or: "Innovation meets simplicity"
  Or: "The future of [vague category]"
  
### **Why**
  You have 5 seconds to communicate value. Headline is your most important copy.
  If they don't understand what you do in 5 seconds, they leave.
  Clarity > cleverness. Every time.
  
### **Solution**
  # Value prop formula:
  [End result customer wants]
  [Specific period/method]
  [Address objection]
  
  Example: "Close more deals in less time without CRM complexity"
  
  # Test with strangers:
  Show for 5 seconds. Ask: "What does this company do?"
  If they can't answer, rewrite.
  
  # Bad headlines:
  "Welcome to Acme"
  "The future of work"
  "Next-generation platform"
  
  # Good headlines:
  "Project management for teams who ship"
  "Send invoices in 30 seconds"
  "Email marketing that grows with you"
  
### **Symptoms**
  - High bounce rate
  - What does this do?
  - Visitors confused in 5-second tests
  - Low engagement despite traffic
### **Detection Pattern**


## Distraction Disaster

### **Id**
distraction-disaster
### **Summary**
Too many competing elements on the page
### **Severity**
high
### **Situation**
  Page contains: three different offers, seven CTAs, blog sidebar,
  newsletter popup, chat widget, social feeds, partner links,
  autoplay video, animations everywhere.
  
### **Why**
  Confused minds don't convert. One page, one goal. Every distraction costs conversions.
  Attention is finite. Split it and you lose it.
  
### **Solution**
  # Single goal:
  Define the ONE thing you want them to do.
  Remove everything that isn't that.
  
  # Distraction audit:
  For every element ask: "Does this help them convert?"
  If no → remove it.
  
  # Elements to question:
  - Popup immediately on load?
  - Chat widget visible?
  - Sidebar content?
  - Multiple offers?
  - Autoplay video?
  - Excessive animations?
  
  # Focus test:
  Squint at page. Is there ONE obvious focal point?
  If not, simplify.
  
### **Symptoms**
  - Visitors don't know where to look
  - Multiple CTAs compete
  - Heatmaps show scattered attention
  - Low conversion despite engagement
### **Detection Pattern**


## Scroll Assumption

### **Id**
scroll-assumption
### **Summary**
Assuming visitors will scroll to see important content
### **Severity**
high
### **Situation**
  Hero: Beautiful image (no copy). Value prop: Scroll 1. Benefits: Scroll 2.
  Social proof: Scroll 3. CTA: Scroll 4. 85% of visitors see hero only.
  
### **Why**
  Many never scroll. Those who do scroll skim. Above-the-fold real estate is gold.
  If 85% never scroll, 85% of your value is hidden.
  
### **Solution**
  # Complete story above fold:
  - Value prop: Clear
  - What you do: Clear
  - Who it's for: Clear
  - Primary CTA: Visible
  
  # Above-the-fold must-haves:
  □ Clear headline
  □ Subheadline with benefit
  □ Primary CTA button
  □ Some form of proof
  
  # Scroll motivation:
  - Partial content visible below fold
  - Visual cue to scroll
  - Promise more value below
  
  # Sticky elements:
  - Sticky CTA button
  - Follows as they scroll
  
### **Symptoms**
  - Key content never seen
  - Low scroll depth
  - High bounce despite good hero
  - CTA at bottom never reached
### **Detection Pattern**


## Generic Stock Photos

### **Id**
generic-stock-photos
### **Summary**
Using inauthentic stock photos that signal generic product
### **Severity**
medium
### **Situation**
  Handshake photo, smiling people at laptops, multicultural boardroom,
  woman looking at chart, puzzle pieces connecting.
  
### **Why**
  Stock photos are recognized. Generic = forgettable. Trust decreases.
  "This looks like every other site." Authenticity builds trust.
  
### **Solution**
  # Better than stock:
  1. Product screenshots - Real interface
  2. Team photos - Actual people
  3. Customer photos - Real users
  4. Custom illustrations - Unique style
  
  # Stock clichés to avoid:
  ✗ Business handshake
  ✗ Happy office workers
  ✗ Light bulb / brain
  ✗ Puzzle pieces
  ✗ Rocket ship
  
  # If stock is necessary:
  - Choose realistic, unstaged
  - Diverse but natural
  - Avoid obvious clichés
  
### **Symptoms**
  - Page looks like competitors
  - No memorable visuals
  - Trust signals feel fake
  - Brand personality absent
### **Detection Pattern**


## Objection Silence

### **Id**
objection-silence
### **Summary**
Not addressing common objections before the CTA
### **Severity**
high
### **Situation**
  Page covers features, benefits, social proof, CTA. Doesn't address:
  "Is this secure?" "What if I don't like it?" "How hard is setup?"
  
### **Why**
  Every visitor has hesitations. Unaddressed objections = friction.
  Objection in mind → doesn't convert. Overcome before they become blockers.
  
### **Solution**
  # Identify common objections:
  - Talk to sales
  - Read support tickets
  - Survey abandoners
  
  # Address proactively:
  - Near relevant sections
  - Before the CTA
  - FAQ section
  
  # Risk reversal:
  - "30-day money-back guarantee"
  - "Free trial, no credit card"
  - "Cancel anytime"
  
  # Common objections:
  - Price: "Is it worth it?" → ROI calculator, guarantee
  - Risk: "What if it fails?" → Free trial, guarantee
  - Complexity: "Is it hard?" → Setup time, onboarding
  - Trust: "Is my data safe?" → Security badges
  
### **Symptoms**
  - Visitors leave at CTA
  - Sales handles same objections
  - High cart abandonment
  - Support gets pre-sale questions
### **Detection Pattern**
