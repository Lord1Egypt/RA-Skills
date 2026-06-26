---
name: secondhand-furniture-listing-check
description: "Review a secondhand furniture listing before pickup with seller questions, photo requests, measurement checks, transport planning, hygiene and pest warnings, recall reminders, and safer meetup guidance. Use when the user wants a practical buying checklist without legal advice or valuation claims."
---
# Secondhand Furniture Listing Check

## Purpose

Help the user evaluate an online used-furniture listing before they commit to pickup. The skill turns a listing into a practical readiness sheet: seller questions, photo checklist, dimensions, transport needs, hygiene concerns, pest warnings, safer meetup planning, and recall reminders.

This is a prompt-only organization and safety workflow. It does not provide legal advice, authenticate items, predict resale value, or guarantee that an item is safe, clean, pest-free, or worth the asking price.

## Use This Skill When

Use this skill when the user is considering used furniture from a marketplace, neighborhood group, thrift listing, estate sale post, resale app, or social media listing and asks about:

- What to ask the seller before pickup.
- Whether the photos show enough detail.
- How to confirm dimensions, elevator fit, stairs, vehicle fit, or transport needs.
- How to inspect couches, mattresses, upholstered chairs, wood tables, dressers, bookcases, desks, cribs, or shelving.
- How to prepare for pickup, payment, loading, and safer meeting logistics.
- How to think about pests, odors, hygiene, damage, recalls, or missing hardware.

Do not use it to determine legal rights, negotiate claims, appraise value, authenticate designer goods, certify safety, or accuse a seller of wrongdoing.

## Best Inputs

Ask for only the details needed to make the checklist useful. If the user cannot share the listing, proceed with a generic version.

- Item type, brand or model if known, and listed condition.
- Price, location, pickup window, and whether delivery is offered.
- Listing photos or the user's description of visible wear, stains, cracks, missing parts, labels, or odors.
- Dimensions from the listing and the user's door, stair, elevator, vehicle, and room constraints.
- Household sensitivities: pets, allergies, smoke, children, shared building, or pest concerns.
- Pickup plan: solo or with help, daylight or evening, public place or residence, payment method, tools, straps, blankets, or cart.

## Workflow

1. **Capture the listing basics.** Summarize item type, location, pickup deadline, price as listed, seller claims, missing facts, and why the user is interested.
2. **Check fit first.** Compare item dimensions with doorways, stair turns, elevator size, vehicle cargo space, hallway clearance, and the target room.
3. **Request better evidence.** Create a short photo checklist: front, back, underside, seams, legs, drawers, hardware, labels, serial/model tags, stains, cracks, water marks, and closeups of damage.
4. **Ask condition questions.** Build a seller script covering age, source, repairs, odors, smoke exposure, pets, pests, storage location, missing hardware, weight, disassembly, and pickup constraints.
5. **Flag hygiene and pest risks.** For upholstered, cushioned, wood, wicker, or mattress-like items, warn about bed bugs, fleas, roaches, strong odors, mold, heavy staining, and cleaning limits. Suggest passing or seeking expert inspection when risk is high.
6. **Check recalls where relevant.** For cribs, children's furniture, bunk beds, recliners, dressers, wall beds, folding furniture, or items with moving parts, remind the user to verify current recall and safety information from an official source before use.
7. **Plan pickup safely.** Prefer daylight, a public or well-lit location when practical, bringing another person, sharing the plan with someone trusted, keeping communication in-app, and avoiding pressure to enter unsafe spaces or rush.
8. **Prepare transport.** List tools and supplies: measurements, straps, moving blankets, gloves, screwdriver or hex key, labels for hardware, dolly, helper count, and cleanup bags.
9. **Create the go/no-go card.** Summarize unanswered questions, visible risks, required photos, fit status, pickup plan, and a personal decision line for the user.

## Output Format

Return the listing check in this order:

1. **Listing Snapshot**

| Field | Notes |
|---|---|
| Item | |
| Seller location or pickup area | |
| Listed condition | |
| Dimensions | |
| Pickup deadline | |
| Known risks | |
| Missing facts | |

2. **Ask the Seller Script**

A concise message the user can send, with no accusations and no legal claims.

3. **Photo Checklist**

| Photo needed | Why it matters |
|---|---|
| Full front/back/sides | |
| Underside and legs | |
| Seams, cushions, drawers, or joints | |
| Labels, model, serial, or tags | |
| Damage closeups | |
| Hardware and disassembly points | |

4. **Fit and Transport Box**

| Constraint | Measurement or plan | Status |
|---|---|---|
| Item dimensions | | |
| Doorway and hallway | | |
| Stairs or elevator | | |
| Vehicle cargo space | | |
| Helper count | | |
| Tools and supplies | | |

5. **Risk Flags**

Separate practical concerns into: pests, hygiene or odor, structural damage, missing hardware, recall or safety verification, and unsafe meetup or pickup pressure.

6. **Pickup Readiness Card**

A short checklist the user can use before leaving: confirmed time, address or meetup spot, helper, daylight plan, payment plan, transport supplies, inspection points, and pass conditions.

7. **Open Questions**

List the missing facts that most affect the user's decision.

## Message Style

- Stay practical, neutral, and non-judgmental about the seller or the item.
- Use cautious language: "ask for," "verify," "consider passing if," and "official recall source."
- Keep the seller script polite and brief.
- Do not pressure the user to buy quickly because a listing may disappear.
- Make personal safety and hygiene concerns visible without alarmism.

## Safety Boundary

- Do not provide legal advice, contract interpretation, marketplace policy claims, liability analysis, or claims about the seller's obligations.
- Do not appraise, authenticate, estimate resale value, or declare an item a good investment.
- Do not guarantee that an item is pest-free, safe, sanitary, genuine, structurally sound, or recall-free.
- Warn about pests, especially bed bugs, fleas, roaches, larvae, droppings, eggs, shed skins, and signs hidden in seams, cracks, drawers, and undersides.
- Warn about hygiene concerns such as stains, odors, smoke exposure, mold, pet contamination, mattresses, upholstered items, and items stored outdoors or in damp spaces.
- Warn about safer pickup practices: daylight, well-lit location, bring help, share plans, keep communication in-app, avoid unsafe residences or isolated spots, and leave if pressured.
- For children's furniture, cribs, dressers, bunk beds, recliners, wall beds, or items with moving parts, tell the user to verify current recalls and safety guidance through official sources before use.

## Example Prompts

- "I found a used couch online. What should I ask before pickup?"
- "Can you turn this marketplace dresser listing into a checklist?"
- "What photos should I request for a secondhand dining table?"
- "Help me decide what to check before buying a used crib."
- "Make a pickup readiness card for a secondhand bookshelf."
