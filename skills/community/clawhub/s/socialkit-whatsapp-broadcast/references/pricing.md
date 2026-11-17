# rates.json

Meta does not offer an API for WhatsApp prices. Copy the per-message rates for the
countries you message from the official rate card into
`~/.config/social-skills/whatsapp/rates.json` (or set `WA_RATES_PATH`):

```json
{
  "currency": "USD",
  "effectiveDate": "2026-10-01",
  "rates": {
    "92": { "marketing": 0.0, "utility": 0.0, "authentication": 0.0 },
    "44": { "marketing": 0.0, "utility": 0.0, "authentication": 0.0 }
  },
  "default": { "marketing": 0.0, "utility": 0.0 }
}
```

- Keys are calling-code prefixes; the longest matching prefix wins, so `"1"` and
  `"1876"` can coexist.
- Replace the zeros with the real numbers from
  https://business.whatsapp.com/products/platform-pricing for your currency.
- Set `effectiveDate` to the rate card's date. Prices change on the first day of a quarter.
- The estimate is list price: Meta charges only delivered messages, and volume tiers and
  free entry point windows can lower the real cost.
