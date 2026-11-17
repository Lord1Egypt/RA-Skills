# Publishing

Canonical docs:

- Upload a build: https://docs.wavedash.com/publishing/upload
- Publish a build: https://docs.wavedash.com/publishing/publish
- Metadata: https://docs.wavedash.com/publishing/metadata
- Pricing: https://docs.wavedash.com/publishing/pricing
- Content guidelines: https://docs.wavedash.com/publishing/content-guidelines

## Upload versus publish

Uploading creates an immutable build. Publishing makes one uploaded build live
for players. Do not publish unless the user explicitly asks to make the build
live.

CLI flow:

```bash
wavedash build push --json --no-color --no-update-check
wavedash publish BUILD_ID --json --no-color --no-update-check
```

Developer Portal flow:

1. Open the game in Developer Portal.
2. Go to Builds.
3. Upload a build folder or zip.
4. Publish the selected build when ready.

## Store page

Before launch, guide the user to prepare:

- clear title
- concise description with a one-sentence hook
- cover art that reads as the game at a glance
- 3-5 gameplay screenshots
- optional short trailer
- accurate tags
- pricing

## Content rules

Games must not include or promote:

- cryptocurrency, NFT, or blockchain features
- real-money gambling
- hateful targeting based on protected characteristics
- impersonation of other games
- malware or browser-crashing behavior

Also check:

- game loads reliably
- browser tab does not crash
- expected progress is saved
- cover art is square, includes the game title, and does not include extra text

## Final launch check

- Correct game ID and build ID.
- Production build uploaded, not a dev artifact.
- SDK init and requested SDK features work.
- Game tested on Wavedash in a fresh browser.
- Metadata, pricing, and content guidelines reviewed.
