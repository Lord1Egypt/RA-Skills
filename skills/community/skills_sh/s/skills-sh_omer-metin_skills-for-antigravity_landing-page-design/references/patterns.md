# Landing Page Design

## Patterns


---
  #### **Name**
Inverted Pyramid Structure
  #### **Description**
Front-load the most critical conversion elements, progressively revealing supporting details
  #### **When**
Structuring any landing page with a single conversion goal
  #### **Example**
    1. Hero (above fold):
       - Value proposition headline (what you get)
       - Subheadline (who it's for, why it matters)
       - Primary CTA (clear action)
       - Hero image/video (showing product/outcome)
    
    2. Social proof (immediately after):
       - Logos, testimonials, metrics that build trust
    
    3. Features/benefits (scannable):
       - 3-5 key benefits with icons
       - Focused on outcomes, not features
    
    4. How it works (optional):
       - 3-step process if clarity needed
    
    5. Pricing/CTA (repeat):
       - Remove final objections, convert
    

---
  #### **Name**
Friction Audit
  #### **Description**
Systematically identify and eliminate every barrier between visitor and conversion
  #### **When**
Optimizing an existing landing page or before launching a new one
  #### **Example**
    Friction sources to eliminate:
    ✓ Form fields (every field costs 5-10% conversion)
    ✓ Unclear CTAs ("Submit" → "Get Free Trial")
    ✓ Page load time (>3s kills 50% of visitors)
    ✓ Confusing navigation (no nav menu on landing pages)
    ✓ Walls of text (break into scannable bullets)
    ✓ Missing trust signals (no social proof = low trust)
    ✓ Unclear value prop (visitor can't tell what you do in 5s)
    
    After removing friction, add motivation (urgency, scarcity, specificity)
    

---
  #### **Name**
One-Column Flow
  #### **Description**
Design with a single visual path from top to bottom, no competing attention
  #### **When**
Maximizing conversion rate for a focused action
  #### **Example**
    Bad (multi-column):
    [Hero] [Sidebar CTA] [Feature 1] [Feature 2] [Testimonials] [Footer links]
    → Eye bounces, attention splits, visitor gets lost
    
    Good (single column):
    [Hero with CTA]
       ↓
    [Social proof]
       ↓
    [3 key benefits]
       ↓
    [CTA repeat]
       ↓
    [Final objection handling]
       ↓
    [Final CTA]
    
    Only one thing to do: scroll down and convert
    

---
  #### **Name**
Specificity Over Vagueness
  #### **Description**
Replace generic claims with concrete, measurable outcomes
  #### **When**
Writing headlines, CTAs, and benefit statements
  #### **Example**
    Generic: "Improve your productivity"
    Specific: "Save 3 hours per week on email"
    
    Generic: "Join thousands of users"
    Specific: "Join 12,847 marketers using this daily"
    
    Generic: "Try for free"
    Specific: "Start your 14-day free trial (no card required)"
    
    Specificity builds credibility. Vagueness breeds skepticism.
    

---
  #### **Name**
Progressive Disclosure for Forms
  #### **Description**
Ask for minimal information upfront, collect more only after commitment
  #### **When**
Designing signup or lead capture forms
  #### **Example**
    Step 1 (landing page):
    [Email input] → "Start Free Trial"
    
    Step 2 (after click):
    [Name, Password, Company] → "Complete Setup"
    
    Step 3 (after signup):
    [Additional profile questions]
    
    Each step increases commitment, making abandonment less likely.
    First step should be <30 seconds to complete.
    

---
  #### **Name**
Speed Budget Enforcement
  #### **Description**
Treat page load time as a conversion feature, not a technical detail
  #### **When**
Building or optimizing any landing page
  #### **Example**
    Speed budget:
    - First Contentful Paint: <1.5s
    - Largest Contentful Paint: <2.5s
    - Total page size: <1MB
    - Hero image: <200KB (WebP format)
    - No blocking scripts above fold
    
    Every 100ms delay = 1% conversion loss
    Test on 3G connection (not just fiber)
    
    Use: Lighthouse, WebPageTest, real device testing
    

## Anti-Patterns


---
  #### **Name**
Navigation Menu on Landing Pages
  #### **Description**
Including site-wide navigation that offers exit paths from the conversion funnel
  #### **Why**
Every link is a leak. Navigation gives visitors an escape route instead of forcing a decision.
  #### **Instead**
    Landing pages should have:
    - Logo (optionally links to home, but subtle)
    - Primary CTA in header (sticky)
    - NO menu, NO sidebar links, NO footer navigation maze
    
    Exception: Legal links (Privacy, Terms) in footer are fine—they're trust signals.
    

---
  #### **Name**
Generic Stock Photos
  #### **Description**
Using smiling business people or abstract imagery instead of product-specific visuals
  #### **Why**
Generic imagery is invisible. Visitors scroll past it. It communicates nothing about your product.
  #### **Instead**
    Show the actual product:
    - Screenshots of the interface
    - Video of the product in action
    - Diagram of the workflow/outcome
    - Real customer photos (with permission)
    
    If you can swap your hero image with a competitor's and still make sense, it's too generic.
    

---
  #### **Name**
Burying the CTA
  #### **Description**
Placing the call-to-action below the fold or at the end of long content
  #### **Why**
50% of visitors never scroll. If CTA isn't visible immediately, half your traffic never sees it.
  #### **Instead**
    CTA placement:
    - Above the fold in hero (primary)
    - After social proof section (secondary)
    - After each major benefit section (tertiary)
    - Sticky header CTA (always visible)
    
    Visitor should never have to hunt for "how do I sign up?"
    

---
  #### **Name**
Multiple Competing CTAs
  #### **Description**
Offering several different actions (signup, demo, contact, learn more, download)
  #### **Why**
Choice paralysis. Visitors don't know which action to take, so they take none.
  #### **Instead**
    One page = One primary action
    
    Primary CTA: "Start Free Trial" (high-contrast, repeated)
    Secondary CTA (if needed): "Watch 2-min Demo" (lower contrast, once)
    
    Test: Remove secondary CTA entirely. It often increases primary conversions.
    

---
  #### **Name**
Feature Lists Instead of Benefits
  #### **Description**
Describing what the product has rather than what the user gets
  #### **Why**
Users don't care about features. They care about outcomes and transformations.
  #### **Instead**
    Feature: "Advanced analytics dashboard"
    Benefit: "See which campaigns actually drive revenue"
    
    Feature: "Cloud-based storage"
    Benefit: "Access your files from anywhere, never lose work"
    
    Feature: "AI-powered recommendations"
    Benefit: "Save 5 hours/week on content planning"
    
    Always translate features into user outcomes.
    

---
  #### **Name**
Walls of Text
  #### **Description**
Long paragraphs of dense copy that require reading effort
  #### **Why**
People scan, they don't read. Walls of text get skipped. Conversion requires zero effort.
  #### **Instead**
    Make it scannable:
    - Headlines (communicate value in 5 words)
    - Subheadlines (add context in 10 words)
    - Bullet points (3-5 max per section)
    - Bold key phrases
    - Short paragraphs (2-3 lines max)
    - White space between sections
    
    Test: Can someone understand your offer in 10 seconds of scrolling?
    