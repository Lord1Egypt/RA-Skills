# Store readiness audit

Run this on the live app before writing any native code. Give the student a tick/cross list with file paths. Each cross is a likely rejection.

## Checklist

- **Account deletion, two ways.** A delete button inside the app (Settings) that really deletes the user, their rows and their stored files (every storage bucket, not only the database), and a public web page (for example `/delete-account`) that explains how to delete and works when signed out. Google Play asks for that web address in the Data safety form; Apple asks for deletion inside the app. Make the page public in the proxy or middleware list of public routes.
- **Sign in with Apple when there is social login.** If the iOS app offers Google (or any third-party) sign-in, Apple guideline 4.8 wants Sign in with Apple, or an equal privacy-friendly option, next to it. Email links or codes alone do not trigger this.
- **OAuth in the system browser, back by deep link.** Google blocks its sign-in inside embedded web views. Open OAuth in the system browser (`@capacitor/browser`), return to a custom scheme or universal link (for example `myapp://auth/callback`), catch it with `@capacitor/app` `appUrlOpen`, and exchange the code on a native callback route. Add the deep-link address to the Supabase auth redirect URL list.
- **Permission strings.** Every native permission used needs a clear reason in `Info.plist` (`NSMicrophoneUsageDescription`, `NSCameraUsageDescription`, `NSPhotoLibraryUsageDescription` and so on) saying what the app does with it. Ask only for what the app uses; on Android remove unused permissions from the manifest.
- **Apple 4.2, minimum functionality.** A website in a frame gets rejected. Have at least one native piece in the main flow (share sheet, haptics, push, native status bar and splash, microphone capture), a designed offline screen instead of a browser error, and no links to buy digital goods outside in-app purchase.
- **Privacy policy matches the data.** Read the code, not the old policy: every table, storage bucket (voice clips, attachments), email sent (digests, alerts), third party (AI providers, email provider, hosting, analytics) and how long each is kept. If a single delete does not remove a file, say so honestly or fix the code. The same facts feed the App Privacy and Data safety forms, so they must agree.
- **Reviewer login.** Reviewers cannot receive your email codes. Add a small, unobtrusive "Sign in with password" link on the sign-in page (Supabase `signInWithPassword`) without touching the normal sign-in, and create a demo account with sample data. Put the email and password in the review notes of both stores, never in the repo.
- **Demo data.** Seed the demo account with a script (realistic notes, projects, a few items in every list) so screenshots and review show a full app.
- **Basics.** Stable HTTPS address, public privacy and terms pages, support email, an app id chosen once (reverse domain, cannot change), icons and splash, and `store-check.mjs` all ticks.

## Report

Group crosses by "blocks submission", "likely rejection" and "nice to have", each with the file to change.
