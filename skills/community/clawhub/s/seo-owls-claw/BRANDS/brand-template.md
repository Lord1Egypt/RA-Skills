# SEOwlsClaw — Brand Profile Template
# File: BRANDS/brand-template.md
# Usage: Copy this file → rename to BRANDS/<your-id>.md → fill in all fields
# Loaded in: Brain Step 2d

---

# Brand Profile — [BRAND NAME]
ID: your-brand-id
Industry: [e.g. E-Commerce / Photography / SaaS / Health]
Default Locale: [de / en / fr / es / pt]
Default Persona: [blogger / researcher / ecommerce-manager / vintage-expert / creative-writer]

---

## 🗣️ Voice & Tone

### Tone Sliders
# Scale: 1 (left extreme) → 5 (right extreme)
# These values OVERRIDE the default persona tone when /brand is active.

Formal      [1]←——————→[5] Casual        Value: [3]
Serious     [1]←——————→[5] Playful        Value: [2]
Expert      [1]←——————→[5] Approachable   Value: [2]
Reserved    [1]←——————→[5] Direct         Value: [4]

### Writing Notes
# Any free-text notes about voice that don't fit the sliders.
# Example: "Always use Sie-Form in German. Never use exclamation marks in H1."
Notes: |
  [Write free-text notes here]

---

## 📝 Brand Vocabulary

### Preferred Terms
# Terms the brand uses. Format: "use THIS → not THAT"
# These are injected as soft rules in Step 3 (variable generation).
preferred_terms:
  - "[preferred term] → not [avoided term]"
  - "[preferred term] → not [avoided term]"

### Banned Phrases
# Hard ban — if any of these appear in output, Step 6.6 FAILS.
# Be specific. Regex patterns allowed.
banned_phrases:
  - "[banned phrase 1]"
  - "[banned phrase 2]"

### Brand-Specific Terms
# Terms that must be spelled/capitalised a specific way.
brand_terms:
  - "[Term]: [correct spelling]"
  - "[Term]: [correct spelling]"

---

## 🔗 Default CTAs

# CTAs per language. Linked to LOCALE/ — these override the locale CTA defaults.
# Add only the languages you use. Missing languages fall back to LOCALE/base.md.

ctas:
  en:
    primary: "Buy Now"
    soft: "View Listing"
    newsletter: "Subscribe"
    contact: "Get in Touch"
  de:
    primary: "Jetzt kaufen"
    soft: "Zum Angebot"
    newsletter: "Jetzt anmelden"
    contact: "Kontakt aufnehmen"
  fr:
    primary: "Acheter maintenant"
    soft: "Voir l'annonce"
    newsletter: "S'abonner"
    contact: "Nous contacter"
  es:
    primary: "Comprar ahora"
    soft: "Ver oferta"
    newsletter: "Suscribirse"
    contact: "Contactar"
  pt:
    primary: "Comprar agora"
    soft: "Ver oferta"
    newsletter: "Inscrever-se"
    contact: "Entrar em contato"

---

## 🏆 Trust & Proof Priorities

# Ordered list — #1 is strongest/most prominent trust signal for this brand.
# The brain uses this order when selecting which trust elements to emphasise in Zone A.

trust_priorities:
  1: "[e.g. Years in business / certifications]"
  2: "[e.g. Customer reviews / testimonials]"
  3: "[e.g. Guarantees / return policy]"
  4: "[e.g. Awards / press coverage]"
  5: "[e.g. Case studies / portfolio]"

### Trust Block Texts
# Short trust statements for use in {BRAND_TRUST_BLOCK} variable.
trust_blocks:
  en: "[e.g. Every item personally inspected and verified.]"
  de: "[e.g. Jedes Produkt wurde persönlich geprüft und verifiziert.]"

---

## ⚖️ Compliance Profile

# Step 6.6 uses these rules to hard-check all output before release.
# Risk level determines how aggressive the check is.

compliance:
  industry: "[e.g. E-Commerce / Health / Finance / Legal]"
  risk_level: "[LOW / MEDIUM / HIGH]"
  # LOW    = e-commerce, general retail → basic checks
  # MEDIUM = supplements, coaching, financial services → no guarantee/claim language
  # HIGH   = medical, pharma, legal, financial advice → strict disclaimer required

  ### Banned Claim Patterns
  # These are HARD FAILS in Step 6.6 — output is blocked until fixed.
  # Use plain text patterns or regex. Case-insensitive.
  banned_claims:
    - "[e.g. guaranteed results]"
    - "[e.g. clinically proven]"     # if not medically certified
    - "[e.g. #1 in Germany]"         # if not verified by a study

  ### Required Disclosures
  # These phrases/blocks MUST be present somewhere in the output.
  # If missing → Step 6.6 flags as WARNING (not hard fail, unless risk_level = HIGH).
  required_disclosures:
    - "[e.g. Prices include VAT / Preise inkl. MwSt.]"
    - "[e.g. Used items manually inspected]"

  ### Urgency Limits
  # Controls how aggressive Zone B scarcity/urgency language is allowed to be.
  urgency_limit: "[NONE / SOFT / STANDARD / AGGRESSIVE]"
  # NONE       = no urgency language at all (e.g. luxury, legal)
  # SOFT       = "limited availability", "while stocks last"
  # STANDARD   = "only X left", "ends [date]"
  # AGGRESSIVE = countdown timers, "selling fast", "order now before it's gone"

  ### Artificial Scarcity Rule
  # Can the brand use fake countdown timers or fabricated stock numbers?
  artificial_scarcity_allowed: false   # true / false

---

## 📦 Variable Injections

# These go directly into the variable dictionary (Step 3) when this brand is active.
# Use {BRAND_*} in templates to reference them.

variables:
  BRAND_ID: "your-brand-id"
  BRAND_NAME: "[Brand Display Name]"
  BRAND_TAGLINE: "[Optional — short brand tagline]"
  BRAND_DISCLAIMER: "[Footer disclaimer text, e.g. MwSt note]"
  BRAND_TRUST_BLOCK: "[Short trust statement for inline use]"
  BRAND_RETURN_POLICY: "[e.g. 30-day return policy]"
  BRAND_SUPPORT_URL: "[e.g. https://example.com/contact]"
  BRAND_LOGO_URL: "[e.g. https://example.com/logo.svg]"

---

## 📋 Notes & Special Rules

# Any other free-text rules that don't fit the fields above.
# Examples: seasonal adjustments, campaign-specific overrides, client requests.
notes: |
  [Write any additional notes here]

---

*Template version: v0.1 — 2026-04-05*
*Copy → rename → fill in → add row to BRANDS/_index.md*
