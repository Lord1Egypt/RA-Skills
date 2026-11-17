# Privacy and terms pages

The app already has `/privacy` and `/terms`. They show text from `src/lib/legal-content.ts`. This step fills it with an honest draft for this app.

## 1. Questions, one at a time

Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/legal-generate.mjs" <appDir>`. If details are missing it stops and lists exactly what it needs. Ask for each, one at a time, with a plain reason, and save with `node "${CLAUDE_PLUGIN_ROOT}/scripts/profile.mjs" set <path> <value>`:

- `company.legalName`: "Whose name is on the service: you as a person, or a company?" A person is fine; use their full name.
- `company.address`: "A postal address where you can be reached. It is shown publicly in many countries." If they work from home and do not want that shown, a business address or PO box is an option; say the law in their country decides.
- `company.contactEmail`: the public email for privacy questions.
- `owner.country`: where they live (decides governing law and which privacy authority is named).
- `company.phone`: asked only when the app takes payments. "A phone number customers can call about a purchase. A mobile number is fine." If they truly have none, save `none`.
- `company.vatId`: only if they have one; fine to leave empty.

Never invent a value. Use `--` before values that start with a dash.

## 2. Generate

Run `legal-generate.mjs <appDir>` again. It lists the services it found (Supabase and Vercel always; Resend, Stripe, OpenAI, OpenRouter, Google sign-in and others when the app uses them) and writes the file. Same input gives the same file, so running it again is safe.

## 3. Read it back

Tell the student in five bullets, in their words:
1. Who is responsible for the data (name and contact).
2. What you collect (account email, what they create, no card numbers: Stripe handles those).
3. Who else handles it (the list of services and where they are).
4. Their rights, including deleting their account in the app.
5. What the terms say about payments and cancelling, if billing is on (including the 14-day withdrawal right for EU and UK consumers).

Then say: "This is a draft made from your settings. Have it checked, especially before taking real money. I am not a lawyer." Offer to adjust wording, but do not weaken the user-rights, withdrawal or data sections.

## 4. Ship it

Branch, commit with the student's OK, pull request, green checks, merge, `deploy.mjs`. Then open `/privacy` and `/terms` on the live address and check they read well on a phone. `/admin/health` will still say "draft" for the legal check; that reminder is on purpose.

## Regenerate when

A service or module is added (billing, newsletter, an AI service, analytics), a price changes, the company details or country change, or the domain changes. Regenerating replaces the file, so tell the student hand edits will be lost; hand edits belong in the file's source data only if they ask for custom wording, and then re-apply them after.
