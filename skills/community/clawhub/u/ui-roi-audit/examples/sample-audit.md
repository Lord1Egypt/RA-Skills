# Sample audit — product page of a demo shop

A real run of the skill, kept as a format reference. The page is the "Combination Pliers" product
page of Toolshop, a public demo shop built for software-testing practice
(practicesoftwaretesting.com), observed on 2026-10-08. It is a training site, not a business, so no
traffic or revenue data exists and the value estimates are qualitative.

## 1. Audit frame

- **Page:** Toolshop demo — Combination Pliers product page
- **Type:** detail / product page
- **Goal:** add to cart, leading to purchase
- **Audience:** tradespeople and DIY buyers comparing hand tools
- **Data available:** none (no visits, conversion rate, or order value)
- **Viewport observed:** 1024 × 768, desktop

## 2. Verdict

The page gives a buyer nothing to trust beyond the seller's own description: no reviews, no stock
status, no shipping or returns information. Add availability and delivery information next to the
add-to-cart button first; it is the cheapest fix and it sits on the first screen.

## 3. Findings

| # | Criterion ID | Finding | Evidence on page | Score | Exposure | Severity | Effort | Source |
|---|---|---|---|---|---|---|---|---|
| 1 | DP-5 | No availability or shipping information before the cart | In-stock items show no stock status; delivery cost and time appear nowhere | Fail | High | High | Low | Loveday & Niehaus 2008, ch. 7 |
| 2 | DP-4, TR-5 | No customer reviews or other third-party proof | No ratings, reviews, or testimonials anywhere on the page | Fail | High | High | High | Loveday & Niehaus 2008, ch. 7 |
| 3 | TR-3 | Returns terms missing; warranty buried | "Warranty 2 years" appears only as a row in the specifications table below the first screen | Partial | Medium | High | Low | Loveday & Niehaus 2008, ch. 9 |
| 4 | DP-1, PC-3 | One image, not enlargeable, not clearly the product sold | Single stock photograph with a photographer credit; no zoom, no alternate views | Fail | High | Medium | Medium | Loveday & Niehaus 2008, ch. 6, ch. 7 |
| 5 | PC-1, PC-2 | Description is one dense paragraph | Six sentences of running text between price and button; key facts repeated later in the specifications table | Partial | High | Medium | Low | Loveday & Niehaus 2008, ch. 7 |
| 6 | DP-6 | Price is separated from the action | Price sits under the title; the add-to-cart button is a full paragraph lower | Partial | High | Medium | Low | Loveday & Niehaus 2008, ch. 7 |
| 7 | DP-2, CA-1, CA-4 | Primary action competes with two secondary ones | "Add to cart", "Add to favourites", and "Compare" sit in one row at similar size; the favourites button is the brightest | Partial | High | Medium | Low | Loveday & Niehaus 2008, ch. 4, ch. 7 |
| 8 | CA-3 | Primary action is at the very edge of the first screen | At 1024 × 768 the button row is the last visible line; on a shorter screen it falls below | Partial | High | Medium | Low | Loveday & Niehaus 2008, ch. 4 |
| 9 | PR-1 | Total cost cannot be judged | Item price is clear; shipping charges are not stated before the cart | Partial | High | Medium | Low | Loveday & Niehaus 2008, ch. 6, ch. 7 |

## 4. Top three fixes

1. **State availability, delivery time, and delivery cost beside the button** (findings 1, 9).
   Removes the main unanswered question at the moment of decision. *ROI: no data — qualitative.
   High exposure, low effort.*
2. **Move the price next to the button and shorten the description to scannable key points**
   (findings 5, 6, 8). Lifts the button higher on the first screen as a side effect. *ROI: no data —
   qualitative. High exposure, low effort.*
3. **Make "Add to cart" the single dominant action** (finding 7). Reduce favourites and compare to
   text links or icons. *ROI: no data — qualitative. High exposure, low effort.*

Reviews (finding 2) are high value but high effort; plan them, do not start with them.

To turn these into numbers, two inputs are needed: monthly visits to product pages and the
add-to-cart rate. With those, calculate a twelve-month range per `references/roi-model.md`.

## 5. What passed

- DP-3 — the description and specifications table cover the properties a buyer needs
- CA-2 — the button label is an action verb that says what happens

## 6. Not assessed

- ER-1 to ER-3 — no error state was triggered. Check by entering an invalid quantity.
- TR-1 and TR-2 — no personal or payment data is requested on this page. Assess where data is collected.
- TR-4 — a contact page is linked, but its full contact details were not inspected.
- PR-2 — no discount was shown on this product.
- Mobile layout — only the desktop viewport was observed.

## 7. Observations outside the criteria

Auditor's own observations, not backed by the cited sources:

- A row of letters A–E labelled "CO₂" appears under the price with no explanation of what it rates.
- Category and brand tags under the title look like buttons but their purpose is unclear.

## 8. Sources

Loveday, L., & Niehaus, S. (2008). *Web Design for ROI: Turning Browsers into Buyers & Prospects
into Leads.* Berkeley, CA: New Riders. ISBN-13: 978-0-321-48982-1.
