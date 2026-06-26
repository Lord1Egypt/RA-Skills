# Diagnostic Playbook - SMTP

Use this table to isolate failures instead of changing many variables at once.

| Symptom | Likely layer | Common cause | Next check |
|---------|--------------|--------------|-----------|
| Timeout or connection refused | Network | wrong host, wrong port, firewall, provider blocks port 25 | verify DNS, port reachability, and provider docs |
| TLS handshake fails on 465 | TLS mode | using STARTTLS flow on implicit TLS port | retry with implicit TLS and inspect certificate |
| STARTTLS not offered on 587 | Capabilities | wrong host, plain relay, or provider policy | inspect EHLO output before auth |
| `535` or `534` auth failed | Auth | wrong secret, app password missing, legacy auth disabled | confirm auth mechanism and provider policy |
| `530 authentication required` | Auth gate | auth skipped or relay policy requires login | inspect EHLO and auth sequence |
| `550 relay denied` or `553 sender rejected` | Sender identity | From or MAIL FROM not permitted | align auth account, alias, and envelope sender |
| Server accepts but inbox never sees it | Placement | spam filtering, DMARC fail, downstream filtering | check spam folder, headers, and DMARC alignment |
| Bounce references SPF or DKIM | Deliverability | auth records missing or misaligned | inspect SPF, DKIM, DMARC, and return-path |
| Works for plain text, fails for HTML | Content or policy | malformed MIME, provider rewriting, spam scoring | send the smallest valid multipart canary |

Rules while diagnosing:
- change one variable per attempt
- save the exact response code
- do not call a send successful until placement is confirmed
