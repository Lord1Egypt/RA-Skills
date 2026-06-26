---
name: showmethemoney-skill
description: Paid demo skill for StablePay on Solana using USDC. Use when the user wants to access the ShowMeTheMoney paid demo capability. This skill is publicly listed on ClawHub, but paid access must be enforced by the StablePay backend with HTTP 402 and purchase verification.
---

# ShowMeTheMoney Skill

This is a paid demo skill powered by StablePay.

## Pricing

- Price: 0.1 USDC
- Network: Solana Mainnet
- Currency: USDC

## Merchant

- Skill DID: `did:solana:REPLACE_WITH_YOUR_SKILL_DID`

## Backend endpoints

- Execute: `https://wenfu.cc/showmethemoney`
- Verify purchase: `https://api.stablepay.co/verify?skill=did:solana:REPLACE_WITH_YOUR_SKILL_DID&agent={AGENT_DID}`

## Instructions

1. When the user asks to use or install this paid demo skill, call the Execute endpoint.
2. If the backend returns HTTP 402 Payment Required, tell the user this capability requires payment.
3. Let the StablePay plugin handle the payment flow.
4. After payment succeeds, retry the same Execute request.
5. Return the backend result to the user.
6. Never claim the user has purchased access unless the backend confirms it.
7. Never expose private keys, API secrets, or internal implementation details.

## Notes

- This skill is public on ClawHub for discovery and installation.
- Actual paid access is enforced by the backend, not by hiding this file.
- If verification fails or payment is incomplete, do not continue to the paid capability.