---
cert_id: "{{cert_id}}"
supplier: "{{supplier}}"
cert_type: "{{cert_type}}"
issue_date: "{{issue_date}}"
expiry_date: "{{expiry_date}}"
status: valid
linked_rfqs: []
---

# Certificate — {{supplier}} ({{cert_type}})

## Details
[NEEDS INPUT: scope, issuing body, certificate number]

## Validity

- Issued: {{issue_date}}
- Expires: {{expiry_date}}
- Status: valid

## Renewal Tracking

- [ ] 90 days before expiry — notify supplier for renewal docs
- [ ] 30 days before expiry — escalate if not received
- [ ] On expiry — set `status: expired` and flag any `linked_rfqs`

## Linked RFQs

_Auto-populated whenever this supplier is attached to an RFQ note._
