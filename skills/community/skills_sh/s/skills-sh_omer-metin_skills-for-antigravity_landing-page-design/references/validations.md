# Landing Page Design - Validations

## Missing Hero CTA

### **Id**
missing-hero-cta
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <section[^>]*hero[^>]*>(?!.*<(button|a)[^>]*(cta|btn|button))
### **Message**
Hero section missing clear call-to-action button.
### **Fix Action**
Add prominent CTA button in hero section (e.g., <Button variant='primary'>Get Started</Button>)
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html

## Too Many CTAs in Hero

### **Id**
too-many-ctas-hero
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <section[^>]*hero[^>]*>.*<button.*<button.*<button
### **Message**
Hero section has too many CTAs. Limit to 1-2 primary actions.
### **Fix Action**
Reduce to one primary CTA and optionally one secondary action
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html

## Missing Social Proof

### **Id**
missing-social-proof
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - landing.*page
### **Message**
Landing page may be missing social proof elements (testimonials, logos, stats).
### **Fix Action**
Add social proof section with customer testimonials, company logos, or key metrics
### **Applies To**
  - *.tsx
  - *.jsx

## Weak Headline Copy

### **Id**
weak-value-proposition
### **Severity**
info
### **Type**
regex
### **Pattern**
  - <h1[^>]*>Welcome to|<h1[^>]*>Home|<h1[^>]*>Landing Page
### **Message**
Generic headline detected. Use clear value proposition.
### **Fix Action**
Replace with benefit-driven headline that answers 'What problem do you solve?'
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html

## Missing Trust Signals

### **Id**
missing-trust-signals
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - checkout|payment|signup
### **Message**
Payment/signup flow missing trust signals (security badges, guarantees).
### **Fix Action**
Add trust indicators: SSL badge, money-back guarantee, privacy assurance
### **Applies To**
  - *.tsx
  - *.jsx

## No Urgency Elements

### **Id**
no-scarcity-urgency
### **Severity**
info
### **Type**
regex
### **Pattern**
  - pricing|offer|deal
### **Message**
Pricing/offer section could benefit from urgency elements.
### **Fix Action**
Consider adding time-limited offers, countdown timers, or limited availability messaging
### **Applies To**
  - *.tsx
  - *.jsx

## Missing Above-Fold Benefits

### **Id**
missing-above-fold-benefit
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <section[^>]*hero[^>]*>(?!.*(benefit|feature|advantage|solution))
### **Message**
Hero section missing clear benefit statements.
### **Fix Action**
Add 2-3 key benefits or feature highlights above the fold
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html

## Too Much Text Above Fold

### **Id**
long-form-above-fold
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <p[^>]*>.{300,}</p>
### **Message**
Excessive text in hero section. Keep copy concise.
### **Fix Action**
Limit hero copy to 1-2 short sentences. Move details to sections below.
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html

## Text-Only Feature Section

### **Id**
missing-feature-visuals
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <section[^>]*feature[^>]*>(?!.*<(img|svg|video))
### **Message**
Feature section lacks visual elements (icons, images, illustrations).
### **Fix Action**
Add icons or illustrations to feature descriptions for visual hierarchy
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html

## Missing Section Hierarchy

### **Id**
no-clear-page-flow
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <main>.*</main>
### **Message**
Landing page should follow proven section flow.
### **Fix Action**
Structure: Hero → Benefits → Features → Social Proof → Pricing → FAQ → CTA
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html

## Missing FAQ Section

### **Id**
missing-faq-section
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - pricing
### **Message**
Landing page with pricing should include FAQ section.
### **Fix Action**
Add FAQ section to address common objections and questions
### **Applies To**
  - *.tsx
  - *.jsx

## Weak Bottom CTA

### **Id**
weak-final-cta
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <footer
### **Message**
Missing strong final CTA before footer.
### **Fix Action**
Add compelling final CTA section summarizing value and driving conversion
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html