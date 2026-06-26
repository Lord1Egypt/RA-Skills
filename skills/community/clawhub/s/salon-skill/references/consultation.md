# Client Consultation & Intake Logic

This file guides the chatbot/staff through a friendly consultation to gather
enough information to make personalized service recommendations.

---

## Intake Questions (ask conversationally, 1–2 at a time)

### Step 1 — What brings them in?
> "Hi! Welcome 😊 What are you looking to get done today — hair, nails, skin, or a combination?"

Map answer to category: Hair / Nails / Skin / Combo

---

### Step 2 — Type & Concern (by category)

**Hair:**
- "What's your hair type? (straight, wavy, curly, coily)"
- "Any concerns? (frizz, dryness, damage, hair fall, oiliness, dullness)"
- "Is your hair color-treated, chemically processed, or natural?"

**Nails:**
- "Are your nails natural, extended, or do you have gel/acrylic on?"
- "Any concerns? (brittle, peeling, discoloration)"

**Skin:**
- "What's your skin type? (oily, dry, combination, sensitive)"
- "Any concerns? (acne, pigmentation, dullness, dryness, anti-aging, tan)"

---

### Step 3 — Occasion
> "Is this for a special occasion or everyday care?"

Options to listen for:
- Everyday / maintenance
- Date / night out
- Office / professional
- Wedding (own or attending)
- Festival / party
- Post-pregnancy / recovery

---

### Step 4 — Budget
> "Do you have a budget in mind? I can suggest options across different price ranges."

Buckets:
- Budget-friendly (under ₹1,000)
- Mid-range (₹1,000–₹3,000)
- Premium (₹3,000+)
- No preference / let me know what's best

---

## Recommendation Mapping

### Hair
| Concern | Recommended Service |
|---|---|
| Frizz | Keratin Smoothing Treatment |
| Dryness / damage | Hair Spa / Deep Conditioning |
| Hair fall | Scalp Treatment |
| Dullness | Glossing / Color refresh |
| Want a new look | Haircut + Blow Dry consultation |
| Special occasion | Bridal / Event Hair Styling |

### Nails
| Concern / Occasion | Recommended Service |
|---|---|
| Everyday, low maintenance | Basic Manicure + Pedicure |
| Long-lasting | Gel Manicure |
| Want length | Nail Extensions |
| Festive / event | Gel + Nail Art |
| Pampering | Spa Pedicure |

### Skin
| Concern | Recommended Service |
|---|---|
| Oily / acne-prone | Deep Cleansing Facial |
| Dull / tired | Brightening / Glow Facial |
| Pigmentation / tan | Tan Removal Treatment |
| Dry / dehydrated | Classic or Hydrating Facial |
| Anti-aging | Anti-Aging Facial |
| Quick refresh | Cleanup + Threading |

---

## Upsell Triggers

After recommending a primary service, suggest a complementary add-on if budget allows:
- Hair color → suggest Deep Conditioning
- Facial → suggest Eyebrow Threading
- Manicure → suggest Nail Art or upgrade to Spa Pedicure
- Bridal booking → suggest full Bridal Package

---

## Closing the Consultation
After recommendations, always:
1. Summarize what you're recommending and why (1–2 sentences)
2. Give total estimated time and price range
3. Ask: "Would you like to book this, or do you have any questions?"
