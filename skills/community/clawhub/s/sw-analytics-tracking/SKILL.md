# Analytics Tracking Skill

## Trigger
When the user wants to set up, improve, or audit analytics tracking and measurement.

**Trigger phrases:** "set up tracking", "GA4", "Google Analytics", "conversion tracking", "event tracking", "UTM parameters", "tag manager", "GTM", "analytics implementation", "tracking plan"

## Process

1. **Understand**: Product type, key conversion actions, current setup
2. **Design**: Event taxonomy, conversion funnels, UTM strategy
3. **Implement**: Tracking code, GTM configuration, custom events
4. **Verify**: Testing plan to confirm data accuracy
5. **Dashboard**: KPI definitions and reporting structure

## Output: Tracking Plan

```markdown
# Tracking Plan — [Product]

## Key Conversions
| Event | Trigger | Parameters | Priority |
|-------|---------|------------|----------|
| sign_up | Form submission | method, source | P0 |
| purchase | Checkout complete | value, currency, items | P0 |
...

## Event Taxonomy
### Naming Convention
- Format: `[object]_[action]` (e.g., `button_click`, `form_submit`)
- Always lowercase, underscore separated
- Include: event name, category, label, value

### User Properties
| Property | Type | Description |
|----------|------|-------------|
| user_type | string | free / pro / enterprise |
| signup_date | date | Account creation date |
...

## UTM Strategy
| Campaign Type | Source | Medium | Campaign |
|--------------|--------|--------|----------|
| Newsletter | newsletter | email | [YYYY-MM-topic] |
| Social organic | twitter/linkedin | social | [topic] |
| Paid ads | google/meta | cpc | [campaign-name] |
...

## Conversion Funnels
### Primary: Visitor → Signup → Activation → Purchase
1. page_view (landing page)
2. cta_click (signup button)
3. sign_up (form submitted)
4. onboarding_start
5. key_action_complete (activation event)
6. purchase

## Dashboard KPIs
| KPI | Definition | Target |
|-----|-----------|--------|
| Conversion rate | signups / visitors | >3% |
...
```

## Rules
- Always define events before implementing — plan first
- Use consistent naming conventions across all events
- Test every event in debug mode before going live
- Document everything — future you will thank present you
- GDPR: always include consent mechanism before tracking EU users
