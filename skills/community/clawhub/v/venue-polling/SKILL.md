---
name: venue-polling
description: Use this skill when the user wants to poll gym venue availability, inspect or modify the `venue_polling.py` order-signing flow, or run the bundled signature replay and public-key verification helpers for the mini-program booking APIs.
---

# Venue Polling

## Overview

This skill packages the local venue polling and order-signing workflow for the gym mini-program APIs. Use it when the task involves polling `listAreaLease`, attempting `createOrder`, or debugging the RSA-based request signature logic used by the booking flow.

## Workflow

1. Start by reading `scripts/venue_polling.py` to understand the current polling settings, request headers, and signing logic.
2. If the task is signature debugging rather than live polling, use:
   - `scripts/signature_replay_test.py` to compare local signatures with a captured request
   - `scripts/public_key_verify_test.py` to verify candidate sign strings against a captured signature
3. If the user wants code changes, modify the bundled scripts instead of rewriting the workflow from scratch.
4. If you need request or reverse-engineering context, read:
   - `references/create-order-analysis.md`
   - `references/captured-create-order.txt`
   - `references/captured-list-area-lease.txt`

## Notes

- `scripts/venue_polling.py` expects a local `rsa_private_key.pem` file in the working directory when run directly.
- The current bundled workflow uses custom `X-Ca-*` headers and RSA signing, but the exact upstream signing preimage may still differ from the mini-program runtime.
- Prefer the replay and verification helpers before assuming a signature-format fix.
