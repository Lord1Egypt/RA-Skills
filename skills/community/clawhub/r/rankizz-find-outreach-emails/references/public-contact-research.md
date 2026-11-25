# Public contact research standards

## Collection standard

Collect the least personal data needed for a specific business outreach purpose. Prefer an organization's role address over a named address when both reach the right team. Keep the exact source URL and checked date so the user can reassess relevance and removal requests.

Public availability does not establish consent, deliverability, or legal permission. The finder produces research, not a send list cleared for every country.

## Web access

- Follow the site's `robots.txt` instructions for automated fetching. RFC 9309 defines the Robots Exclusion Protocol: <https://www.rfc-editor.org/rfc/rfc9309.html>
- Use a bounded crawl and a truthful user agent when the runtime permits one.
- Do not bypass authentication, technical restrictions, or a site's stated contact preferences.
- Stop on repeated access errors or rate limits.

## Outreach-law checkpoints

- The US FTC says CAN-SPAM applies to commercial email, including business-to-business messages. It requires accurate headers and subjects, identification, a postal address, an opt-out method, and timely suppression: <https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business>
- The UK ICO says a public email does not by itself mean the person consented to direct marketing. UK rules differ between corporate subscribers, sole traders, and other individual subscribers, and personal-data use needs a lawful basis and privacy information: <https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-direct-marketing-using-electronic-mail/how-do-we-comply-with-the-pecr-electronic-mail-marketing-rules/>
- The ICO's business-to-business guidance explains legitimate-interest assessment, the right to object, and the duty to inform people when public personal data is collected: <https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing/>
- Canada's CRTC says commercial electronic messages generally require consent, identification, and unsubscribe. A conspicuously published address is not a blanket permission; relevance to the person's business role and any no-contact statement matter: <https://crtc.gc.ca/eng/com500/guide.htm>
- Gmail's sender guidance requires authentication and stronger unsubscribe and spam-rate controls for bulk promotional senders: <https://support.google.com/mail/answer/81126>

Laws and provider policies change. Check the recipient's and sender's jurisdictions before sending. When the lawful basis or consent is unclear, stop at research and recommend qualified legal review.

## Reporting vocabulary

Use:

- `publicly listed`
- `confirmed on the source page`
- `role-relevant`
- `fallback`
- `not confirmed`

Avoid:

- `verified` when no mailbox verification occurred
- `safe to email`
- `consented`
- `GDPR compliant`
- `guaranteed deliverable`

## Suppression and retention

The skill does not send messages, but reports should prepare users to handle outreach responsibly:

- keep opt-outs and objections in a suppression list;
- do not re-add suppressed contacts from a later crawl;
- retain only the source and context needed to explain collection;
- remove stale or irrelevant personal contacts;
- do not republish the report as a public email directory.
