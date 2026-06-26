# Deliverability Notes - SMTP

Use this file as the baseline for `~/smtp/deliverability-notes.md`.

Track only reusable evidence. Ignore one-off noise.

## Domain Checklist

- SPF record present and not split into multiple SPF TXT records
- DKIM selector known and verified
- DMARC policy and rua or ruf visibility understood
- Return-path alignment checked
- PTR or reverse DNS checked when sending from owned infrastructure

## Placement Notes

- Which canary inboxes reached inbox vs spam
- Whether HTML-only messages behaved worse than plain text
- Whether the provider rewrote bounce addresses or return-path
- Which error codes or bounce subjects repeat for this domain

## Reminder

- SPF passing alone does not prove deliverability.
- DKIM signing alone does not prove alignment.
- A queued message without inbox evidence is still unresolved.
