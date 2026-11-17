# Invitation examples

Use these as field-accurate patterns, then replace copy and paths with truthful study-specific values. Allowed values are:

- `launcher.icon`: `feedback`, `bug`, `research`
- `presentation_mode`: `passive`, `contextual`, `direct_link`
- `panel.reward.kind`: `gift`, `product`, `community`, `access`
- placement corners: `bottom-left`, `bottom-right`

`contextual` and `direct_link` require `panel`. A passive Invitation may omit it. Visibility v1 supports `enabled`, include/exclude rules with `exact` or `subtree`, optional widget languages, integer `priority`, and integer `order`.

## Spontaneous bug report, no reward

Use a passive launcher available broadly. Define participants behaviorally as people who just encountered a problem; exclude test accounts and duplicate reports. State the bias: voluntary reports overrepresent noticeable failures and motivated active users.

```json
{
  "invitation": {
    "launcher": { "label": "Report a problem", "icon": "bug" },
    "presentation_mode": "passive",
    "brand_color": { "light": "#c46f4f" },
    "placement": { "desktop": "bottom-right", "mobile": "bottom-right" }
  },
  "visibility": { "version": 1, "enabled": true, "rules": [], "priority": 0, "order": 0 }
}
```

Offer: “About 5 minutes · No reward.” Ask “What were you trying to do?” and “What happened?” without qualification rules.

## Frustrated or churned customer by email

Use `direct_link`. Email only distributes the generated `recruitment_url`: special URL → expanded Invitation → explicit Start. Do not auto-start permissions or recording, and do not encode identity in the link. Bias: reachable customers willing to re-engage exclude silent and unreachable churn.

```json
{
  "invitation": {
    "launcher": { "label": "Share your experience", "icon": "feedback" },
    "panel": {
      "eyebrow": "Customer research",
      "headline": "Tell us about your recent experience",
      "body": "We want to understand what worked and what did not.",
      "duration_minutes": 15,
      "cta": "Start interview"
    },
    "presentation_mode": "direct_link",
    "brand_color": { "light": "#c46f4f" },
    "placement": { "desktop": "bottom-right", "mobile": "bottom-right" }
  },
  "visibility": {
    "version": 1,
    "enabled": true,
    "rules": [{ "effect": "include", "match": "exact", "pathname": "/account" }],
    "priority": 0,
    "order": 0
  }
}
```

Neutral Intake: “Which best describes your use in the last 90 days?” with balanced options such as “Use regularly,” “Use occasionally,” “Stopped using,” and “Have not used.” Keep the qualifying option hidden in `qualification_rules`.

```json
{
  "intake_create": {
    "title": "Recent product experience",
    "welcome_message": "A few questions will confirm whether this interview is a fit.",
    "consent_text": "By continuing, you agree to take part in this research interview and to the recording described here. You may stop at any time.",
    "max_participants": 12,
    "questions": [{
      "question_text": "Which best describes your use in the last 90 days?",
      "question_type": "single_choice",
      "required": true,
      "options": ["Use regularly", "Use occasionally", "Stopped using", "Have not used"],
      "qualification_rules": { "qualify": ["Stopped using"] }
    }]
  },
  "intake_update": {
    "disqualified_message": "Thank you for your interest. This interview is not the right match today."
  }
}
```

## 20-minute consumer interview, $25 gift card

```json
{
  "launcher": { "label": "Join a 20-minute interview", "icon": "research" },
  "panel": {
    "eyebrow": "Product research",
    "headline": "Tell us how you choose and use this product",
    "body": "20 minutes · $25 gift card",
    "duration_minutes": 20,
    "reward": {
      "kind": "gift",
      "label": "$25 gift card",
      "eligibility": "For invited adults who complete the interview; one reward per person.",
      "delivery": "Sent by email within 5 business days after completion."
    },
    "cta": "Start interview"
  },
  "presentation_mode": "contextual",
  "brand_color": { "light": "#c46f4f" },
  "placement": { "desktop": "bottom-right", "mobile": "bottom-right" }
}
```

The $25 is the actual fixed offer. Do not justify it by converting the human-moderated marketplace benchmark.

## B2B participant unable to accept personal gifts

Use the same duration and research copy, omit `reward`, and say “No personal reward” in the offer. Intake wording: “Which option best describes your organization's policy for research thank-yous?” with balanced options. Do not make accepting a gift the qualifying answer. If product credit or a community contribution is approved instead, use the matching example below and state eligibility before Start.

## Product credit

```json
{
  "kind": "product",
  "label": "$30 account credit",
  "eligibility": "Applied to the participating customer's active paid account after a completed interview.",
  "delivery": "Applied within 5 business days; expires 12 months after issue."
}
```

## Community or charity contribution

```json
{
  "kind": "community",
  "label": "$25 contribution to one listed community organization",
  "eligibility": "Available after a completed interview; participant selects from the listed organizations.",
  "delivery": "Contributions are made in aggregate within 30 days; no personal payment is issued."
}
```

## Early-access research

```json
{
  "kind": "access",
  "label": "Early access to the tested workflow",
  "eligibility": "For participants whose account supports the preview and who complete the interview.",
  "delivery": "Enabled within 3 business days through the end of the preview period."
}
```

Do not imply that access has a cash value or is guaranteed beyond the stated preview.

## Direct-link new-feature test

Use `direct_link` with a panel such as “Try the new export flow,” an exact duration, and an explicit Start CTA. Set the first Visibility include pathname to the customer page where the generated recruitment URL should land. Direct-link Studies are selected only by their opaque recruitment reference, not by automatic Visibility ranking.

Use neutral Intake questions such as “How often have you exported data in the last 30 days?” and “Which export methods have you used?” Include non-use options. Track the distribution wave with non-identifying UTM tags, preserve `ut_research`, and state that an early-access or customer-list sample overrepresents engaged users.

## Consent and control copy

Use concise consent text that names participation, capture, purpose, and withdrawal without making legal claims. Example: “By continuing, you agree to take part in this research interview and to the recording described here. You may stop at any time.” Ask optional recontact separately: “May we contact you about this research?” Recontact is not an Intake qualifier. Do not model it as an ordinary question while claiming it persists UserTold's `consent_followup`; verify that the host participant flow captures that dedicated consent or leave recontact off.

Every plan must preserve explicit Start, remembered Minimize/Hide, and the rule that a new Invitation never interrupts an active intake, interview, or completion flow.
