# Email on your own domain

What works in production (6x7.gr, October 2026): domain at Papaki, ImprovMX free plan forwards every `@6x7.gr` address (a catch-all) to one Gmail, Resend sends the apps' emails, and Gmail "Send mail as" over Resend SMTP lets the owner write and reply as `hello@6x7.gr`. Sections marked **new, untested in production** are written from provider docs, not from that setup.

The pieces do not clash: forwarding uses MX records on the main domain; Resend uses `send.<domain>` (return path) and a `resend._domainkey` DKIM record.

## 1. DNS: where to paste records

Open the registrar's DNS page for the domain and add each record exactly. The **name/host** is the part before the domain: `@` (or empty) for the domain itself, `_dmarc` for DMARC. Never type the full domain in the name field: many registrars add it again (`_dmarc.example.com.example.com`).

- **Papaki** (used for 6x7.gr): the domain's DNS management page in the Papaki account. Record type is "Τύπος εγγραφής", name is "Όνομα / Host / Alias", the value is the destination field; MX records also take a priority. Papaki answers on `dns1.papaki.gr` / `dns2.papaki.gr`; changes showed up within minutes for 6x7.gr.
- **Cloudflare** (new, untested in production): Dashboard > the domain > DNS > Records > Add record. Mail records (MX, TXT) are never proxied; for the website's Vercel records choose "DNS only" (grey cloud). Cloudflare Email Routing is a free alternative to ImprovMX; turn on one or the other, not both (they both want the MX records).
- **Any other registrar**: look for "DNS", "DNS records", "Advanced DNS" or "Zone editor". If the domain's nameservers point somewhere else (Cloudflare, Vercel), edit records there instead; `email-check.mjs` reads the live answer, so it shows which one counts.

After each change run `email-check.mjs <domain>` again. Most changes show within 5 to 30 minutes; allow up to a day before calling it broken.

## 2. Receive: ImprovMX catch-all to Gmail

1. The student signs up at improvmx.com with the Gmail that should receive (free plan: forwarding only, no sending).
2. Add the domain in ImprovMX. Turn on the catch-all (`*` alias) to the Gmail address so every `<anything>@<domain>` arrives. Add named aliases too (6x7.gr has `hello@`, `filippos@`, `admin@`) so they keep working if the catch-all is ever switched off.
3. Add at the registrar:
   - `MX  @  mx1.improvmx.com  priority 10`
   - `MX  @  mx2.improvmx.com  priority 20`
   - `TXT @  v=spf1 include:spf.improvmx.com ~all` . If the domain already has a `v=spf1` line, add `include:spf.improvmx.com` to that line instead: two SPF lines break both.
4. Remove any old MX records for the domain only if the student confirms nothing else receives mail there.
5. Test: from a different account, send to `hello@<domain>` and to a made-up `test123@<domain>` (proves the catch-all). Both should arrive in Gmail within a few minutes; check Spam the first time and mark "Not spam".

## 3. Reply as that address in Gmail ("Send mail as")

**Mandatory route: Resend SMTP.** Measured on 6x7.gr (October 2026, mail-tester.com): Gmail send-as through `smtp.gmail.com` scored **5.7/10**; the same addresses through Resend SMTP scored **10/10**. Through smtp.gmail.com the envelope-from stays `gmail.com` and the DKIM signature is Google's, so neither SPF nor DKIM aligns with `<domain>` and **DMARC fails**. Adding `_spf.google.com` to SPF does not change that. Resend signs as `<domain>`, so SPF, DKIM and DMARC all pass.

1. The domain must be verified in Resend first (`/shipyard:launch` `references/domain-email.md`; `email-check.mjs <domain> --gmail-send-as` checks it).
2. In Resend make a sending-only API key for this, named "Gmail". The student creates it in the Resend dashboard and pastes it only into Gmail, never into chat or a file in the repo.
3. Gmail on a computer: Settings > See all settings > Accounts and Import > "Send mail as". New address: "Add another email address" (name, `hello@<domain>`, untick "Treat as an alias" so replies go to that address, which ImprovMX forwards back). An address already set up with smtp.gmail.com: click "edit info" next to it and go to the SMTP step.
4. SMTP server `smtp.resend.com`, port `587` (TLS) or `465` (SSL), username `resend`, password: the Resend API key from step 2.
5. New address: Gmail sends a confirmation code to `hello@<domain>`; it arrives through ImprovMX. Paste it.
6. Repeat for every `@<domain>` send-as address. Optional: "When replying: reply from the same address the message was sent to".
7. Test (required): get an address at mail-tester.com, send to it from Gmail as `hello@<domain>`, and aim for **9/10 or better**. In "Show original" on a copy received by another account, SPF, DKIM and DMARC should say PASS, with DKIM `d=<domain>`.

### SPF in plain words

SPF is a public list, kept in the domain's DNS, of the mail servers allowed to send as `@<domain>`. Keep exactly **one** TXT line starting `v=spf1` and merge every `include:` into it; two SPF lines make both invalid. `include:_spf.google.com` is optional and harmless (for example `v=spf1 include:spf.improvmx.com include:_spf.google.com ~all`), but it is **not** the fix for Gmail send-as: use Resend SMTP (above). Resend's own SPF lives on its return-path subdomain, so the root line does not need it.

## 4. SPF, DKIM and DMARC

- **SPF** (which servers may send as the domain): exactly one TXT line on `@` starting `v=spf1`, with one `include:` per service that sends as `@<domain>` (for example ImprovMX; Google is optional and not needed with Resend SMTP). Max 10 DNS lookups in total. Resend does not need to be here when it sends from `send.<domain>`; its own SPF lives on that subdomain.
- **DKIM** (a signature proving the mail was not changed): Resend gives a `resend._domainkey` TXT record when the domain is added (`launch-email.mjs` prints it). ImprovMX free does not sign outgoing mail (it does not send).
- **DMARC** (what receivers do when SPF/DKIM fail, and where reports go): `TXT _dmarc  v=DMARC1; p=none; rua=mailto:dmarc@<domain>`. With the catch-all, reports land in Gmail; make a Gmail filter to label them. 6x7.gr runs `p=none`. After two weeks of clean reports move to `p=quarantine` (new, untested in production for 6x7.gr).

## 5. Deliverability test

1. `email-check.mjs <domain>`: all ticks.
2. Receive: send to two addresses at the domain from an outside account (section 2, step 5).
3. Send: from Gmail as `hello@<domain>` (through Resend SMTP, section 3) and from the app (or `notify.mjs ... --kind custom`), write to the check address at mail-tester.com and to a Gmail and an Outlook.com account. Aim for 9/10 or better; fix whatever it names first.
4. Gmail > the received message > three dots > "Show original": SPF, DKIM and DMARC should say PASS. A DMARC FAIL with SPF PASS usually means the sending service is missing from the SPF line or is signing with its own domain.
5. Never set a free-mail Reply-To (an @gmail.com, @hotmail.com, ... address) on mail sent from `@<domain>`. Spam filters score that as forged (`FREEMAIL_FORGED_REPLYTO`, -2.5 on mail-tester). Leave Reply-To out, or use an address at the domain such as `hello@<domain>`, which ImprovMX forwards. Measured on 6x7.gr (October 2026): Gmail send-as scored 5.7/10 through smtp.gmail.com and 10/10 through Resend SMTP; the same Resend app email scored 10/10 without it and 7.6/10 with a Gmail Reply-To.
6. New domains: a few emails a day to people who expect them for the first weeks; ask a couple to reply or mark "Not spam".

## If something fails

- Mail to the domain bounces: no MX (check 1) or ImprovMX does not show the domain as verified yet; wait 30 minutes and recheck.
- Gmail confirmation code never arrives: forwarding is not working yet (fix section 2 first) or it is in Spam.
- "Username and password not accepted" in Gmail: username must be exactly `resend` and the password a Resend API key with sending access; check the domain shows Verified in Resend.
- Gmail send-as mail fails DMARC or scores low on mail-tester: the address still uses `smtp.gmail.com`; edit info and switch it to `smtp.resend.com`.
- Two SPF lines: merge them. `email-check.mjs` flags this.
