# Screenshots, listing and developer accounts

## Screenshots without a phone

- Use Playwright with a phone-sized viewport and `deviceScaleFactor` (for example 440x956 at 3x gives 1320x2868), signed in as the demo account against the live data or a local dev server pointed at it.
- Panoramic sets: render one wide image (headline text over a background, with app screenshots placed across it) and slice it into equal store-sized pieces with `sharp` so the set reads as one strip when scrolled. Keep text off the cut lines.
- Sizes: Apple 6.9 inch 1320x2868 (up to 10). Google Play phone screenshots between 320 and 3840 pixels on each side, 16:9 or 9:16 (at least 2, up to 8), plus the **feature graphic 1024x500** (no important text near the edges).
- Show only demo data, never a real user's.

## Listing text

Write `listing.md` with: app name (30 characters), subtitle (Apple, 30), short description (Play, 80), full description (4000), keywords (Apple, 100), category, support and marketing addresses, privacy policy address, review notes with the demo login (kept out of git), and the age rating answers.

## App Privacy (Apple) and Data safety (Google)

Answer from the audit's data list, the same facts as the privacy policy: for each data type (email, user content such as notes, audio, photos, identifiers, diagnostics) say whether it is collected, linked to the user, used for tracking (usually no), its purpose (app functionality), whether it is encrypted in transit (yes, HTTPS) and that users can request deletion (give the web deletion address). Listing a third party that processes data (AI provider, email sending) counts as sharing in Google's form only when it is not a service provider acting for you; say which you chose and why.

## Developer accounts

- **Apple Individual**: your personal name shows as the seller. Quick, $99 a year.
- **Apple Organization**: the company name shows. Needs a legal entity (for example a Danish ApS, a company with its own CVR) and a D-U-N-S number for it (free, can take days to weeks). Sole proprietorships (enkeltmandsvirksomhed and similar) do not qualify as organizations; they sign up as Individual. Moving later from Individual to Organization is possible but takes a support request.
- **Google personal**: $25 once. New personal accounts must run a closed test with at least 12 testers for 14 days in a row before production access. Find testers early.
- **Google organization**: needs a D-U-N-S number and the organization's details, and skips the 12-tester rule.
- The student signs up and pays themselves. Identity checks can take days, so start the accounts while the build work is going on.
