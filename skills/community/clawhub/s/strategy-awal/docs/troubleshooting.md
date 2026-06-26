# Troubleshooting

If the system encounters an error, check these common issues:

## 1. Emails not appearing in Telegram
- **Issue:** The `/check` command returns nothing, but there are unread emails.
- **Solution:** Verify the Gmail API connection. Run `gog auth list` in the terminal to ensure the OAuth token hasn't expired.

## 2. Classification is incorrect
- **Issue:** An email about Oman was classified as MENA.
- **Solution:** Review and update `context/email-classification-keywords.json`. Add the missing terms to the `primary` or `secondary` arrays.

## 3. Cannot create Google Docs/Sheets/Slides
- **Issue:** OpenClaw tries to create an asset but fails with a permission error.
- **Solution:** Ensure the OAuth scopes granted to `gog` include write access for Drive and Docs. Re-authenticate with `gog auth add strategy@awalcom.net --services gmail,calendar,drive,contacts,docs,sheets`.

## 4. Approval taking too long / Timeout
- **Issue:** The system drops the context before the user replies to an approval request.
- **Solution:** The MVP relies on asynchronous chat. If context drops, simply reply to the specific summary card with the desired action, and OpenClaw will reconstruct the context.