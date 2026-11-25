---
name: rankizz-find-outreach-emails
description: Find publicly listed, role-relevant business email addresses for one website or a list of domains by inspecting the live site and using web search, then cite the exact source for every result. Use for marketing prospect research, backlink outreach contact discovery, editorial contacts, partnership contacts, contributor contacts, or a local Markdown contact report. Prefer marketing, editorial, partnerships, advertising, or another relevant business address; return support or contact addresses only when they are the site's only public email. Uses local and public web resources without Rankizz credits.
---

# Find public outreach emails

Find the smallest relevant set of public business contacts. An email shown on a website is evidence that the address exists, not automatic permission to market to it.

Read [references/public-contact-research.md](references/public-contact-research.md) before collecting or reporting addresses.

## Set the scope

Collect:

- the domain or domain list;
- the outreach purpose, such as editorial correction, guest contribution, partnership, sponsorship, or backlink request;
- the desired role or team;
- countries or jurisdictions when known;
- excluded address types;
- whether the user wants a Markdown report and its directory.

Normalize each input to a canonical website URL. Keep the submitted domain in the output so the user can reconcile results.

## Protect people and websites

- Collect only email addresses intentionally published for business contact.
- Do not use breached data, leaked lists, private databases, WHOIS history, account recovery, login-only pages, or hidden application data.
- Do not guess an address from a naming pattern. `first.last@domain.com` is not a result unless a public source displays it exactly.
- Do not test a mailbox by sending mail, opening an SMTP session, requesting a password reset, or subscribing it to anything.
- Do not bypass a contact form, CAPTCHA, rate limit, paywall, access control, or bot restriction.
- Respect `robots.txt`, site terms, and server responses. Stop or slow down on `403`, `429`, or repeated failures.
- Do not send outreach. This skill finds and reports contacts for manual review.
- Minimize personal data. A named work address can still be personal data, so retain its source, business purpose, and checked date.

## Research each site

### 1. Inspect likely pages on the live site

Start with the homepage and navigation. Check only relevant public pages, such as:

- contact, about, team, company, and leadership;
- editorial, newsroom, press, media, and masthead;
- partnerships, business development, advertising, sponsorship, and affiliates;
- blog author pages, contributor guidance, write for us, and guest-post policies;
- the footer and relevant legal or company-information pages.

Search the page source and rendered text for `mailto:` links and visible email addresses. Record the exact source URL and nearby context.

Do not treat privacy, data-protection, abuse, security, legal-notice, billing, jobs, or no-reply addresses as marketing contacts unless the outreach purpose genuinely belongs to that team.

### 2. Use web search to close gaps

If the site navigation does not reveal a suitable contact, search the public web with focused queries:

```text
site:example.com editorial contact
site:example.com partnerships email
site:example.com advertise OR sponsor OR "write for us"
"example.com" marketing email
```

Open the result before accepting the email. A search snippet by itself can be stale or misleading. Prefer a page controlled by the organization. Do not use scraped-email directories or bulk contact databases as evidence.

### 3. Keep the crawl bounded

Use the agent's browser, fetch tool, or installed command-line utilities. Stay on the submitted site, fetch only pages that could contain business-contact information, and avoid downloading unrelated assets.

For a normal site, inspect no more than about 20 useful pages and keep requests near one per second unless the site states a stricter limit. Stop when a high-quality relevant address has been confirmed and additional crawling would not change the result.

## Classify every address

Assign one category:

1. `editorial or content`
2. `partnerships or business development`
3. `marketing or growth`
4. `advertising or sponsorship`
5. `relevant named business contact`
6. `general business`, such as `hello@`, `info@`, or `business@`
7. `support or contact fallback`

Prefer the category that matches the outreach purpose. A named address is not automatically better than a role address; relevance and clear publication context matter more.

Return `support@` or `contact@` only when no other public email appears anywhere on the inspected site. Mark it as a fallback and explain that it may route poorly. If the site provides only a contact form, report the form URL instead of inventing an email.

Exclude:

- `noreply@`, automated senders, and newsletter return paths;
- privacy, DPO, abuse, security, legal, billing, and careers addresses used outside their stated purpose;
- personal consumer addresses not clearly published for the relevant business role;
- addresses found only in an unrelated third-party copy of the site;
- malformed or image-decoding guesses that cannot be confirmed.

## Record evidence and confidence

For each reported address, store:

- domain and exact email;
- category and role or person, when stated;
- source URL and page title;
- the nearby label or context in a short paraphrase;
- checked date;
- confidence;
- fallback status and notes.

Use:

- `high`: the organization's live site displays the exact email beside a matching role or purpose;
- `medium`: an official organization-controlled page displays the exact email, but the role or freshness is less clear;
- `not confirmed`: the address appears only in a snippet, stale copy, or ambiguous text. Do not put it in the recommended contact column.

Never label an address `verified` or `deliverable` without a separate, authorized verification service. Use `publicly listed` or `confirmed on source page`.

## Choose the output

For one to five domains, print a concise Markdown table in the terminal or response unless the user requests a file.

For six or more domains, a supplied domain-list file, or multiple batches, create `outreach-email-research-YYYY-MM-DD.md` in the requested directory or current project. Do not overwrite an existing report; add a topic, time, or numeric suffix.

Use this table for a small result:

```markdown
| Domain | Recommended email | Category | Confidence | Source | Notes |
|---|---|---|---|---|---|
| example.com | editor@example.com | Editorial | High | [Editorial page](URL) | Published for pitches |
```

Use this report for a larger result:

```markdown
# Outreach email research

- Purpose:
- Domains submitted:
- Checked at:
- Collection method: public website and web search

## Recommended contacts
| Domain | Email | Category | Role | Confidence | Source | Checked | Notes |
|---|---|---|---|---|---|---|---|

## Contact-form-only sites
| Domain | Form | Intended use | Notes |
|---|---|---|---|

## No public contact found
| Domain | Pages checked | Search checked | Reason stopped |
|---|---|---|---|

## Excluded addresses
| Domain | Address or type | Reason excluded |
|---|---|---|

## Collection limits
[Blocked pages, robots restrictions, stale sources, ambiguous ownership, and other caveats]
```

Return the report path when a file is created. Otherwise return the table, the number of domains checked, the number with relevant contacts, the number using support/contact fallback, and the number with no public email.

## Do

- Match the contact role to the intended outreach.
- Cite the live page where each address appears.
- Preserve exact spelling and domain.
- Deduplicate addresses while retaining all useful source pages.
- Report contact forms and no-result sites honestly.
- Recheck important contacts shortly before outreach.
- Keep a suppression list separate from the research report when the user later sends mail.

## Do not

- Rank an email as suitable only because it looks personal.
- manufacture common patterns or use an email permutation tool.
- scrape thousands of pages when a few relevant pages answer the task.
- use `support@` because it was the first address found.
- send marketing to privacy, abuse, security, or legal channels.
- imply that public availability equals consent.
- promise deliverability, permission, or legal compliance.

## Examples

Good result:

> `editorial@example.com` was published on the site's contributor page for story pitches. High confidence. Source checked today: [Contributor guidelines](https://example.com/contributors).

Acceptable fallback:

> `support@example.com` is the only public email found after checking the contact, about, team, press, partnership, and contributor pages. Use only if the message is suitable for internal routing. The site also provides this [contact form](https://example.com/contact).

Bad result:

> The CEO is Jane Doe, so `jane.doe@example.com` probably works.

The bad result is a guess and must be excluded.

## Limitations

- Public pages can be stale, incomplete, rendered only in JavaScript, or blocked from automated access.
- Obfuscated and image-only addresses may not be readable without manual inspection.
- A published role address can still reject outside pitches or route to support.
- This workflow does not verify mailbox existence, deliverability, consent, or the recipient's jurisdiction.
- Anti-spam and privacy duties depend on the sender, recipient, purpose, location, and sending method. The user must review them before outreach.
