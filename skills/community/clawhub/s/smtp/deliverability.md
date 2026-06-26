# Deliverability - SMTP

Use this file when the SMTP transaction succeeds but inbox placement or reputation still fails.

## Minimum checks

1. SPF covers the actual return-path or sending service.
2. DKIM signs with a domain the user expects to trust.
3. DMARC aligns with the visible From domain.
4. The visible From, envelope sender, and authenticated path are coherent.
5. The first message goes to a canary inbox with spam-folder inspection.

## High-signal interpretation rules

- SPF pass with DKIM fail can still land in spam if DMARC alignment fails.
- DKIM pass on a different domain may not help the visible From domain.
- A provider queue acceptance code does not override downstream mailbox filtering.
- New domains and low-volume senders need smaller ramps and cleaner canary evidence.

## What to inspect in headers or logs

- `Received` chain for the actual handoff path
- `Authentication-Results` for SPF, DKIM, and DMARC
- return-path or envelope sender
- DKIM `d=` domain
- final mailbox folder: inbox, promotions, spam, or bounce

## Safe escalation order

1. prove connection and auth
2. prove sender identity alignment
3. prove canary inbox placement
4. only then increase content richness or recipient count
