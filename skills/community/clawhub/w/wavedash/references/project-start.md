# Starting a Game From Zero

Canonical docs:

- Quickstart: https://docs.wavedash.com/getting-started/quickstart
- Engine guides: https://docs.wavedash.com/engines
- SDK setup: https://docs.wavedash.com/sdk/setup
- Best practices: https://docs.wavedash.com/tutorials/best-practices

Use this reference when the user asks to make a new game, prototype, demo, or
sample project for Wavedash rather than publish an existing build.

## Target shape

Create a browser-playable game that builds to static files:

- `index.html` in the build output
- JavaScript, WebAssembly, assets, and styles referenced with relative paths
- no required backend server for the core game loop
- a clear build command and output directory
- `wavedash.toml` pointing at that output directory

Good default for agents: a small Vite or plain TypeScript/JavaScript game with a
canvas, keyboard/gamepad input, audio gated behind user interaction, and a
production build to `dist`.

## From-zero workflow

1. Pick the simplest stack that matches the user request. If the user does not
   care, prefer a browser-native canvas/WebGL stack over a heavy engine.
2. Build an actual playable loop first: title/menu, start/restart, win/loss or
   score condition, keyboard/touch-friendly controls, and visible feedback.
3. Add Wavedash load lifecycle early:

   ```javascript
   Wavedash.updateLoadProgressZeroToOne(0.0);
   await loadAssets();
   Wavedash.updateLoadProgressZeroToOne(1.0);
   Wavedash.init();
   ```

4. Add requested Wavedash features from `references/sdk.md`.
5. Add a production build script and confirm the output contains `index.html`.
6. Run `wavedash init` or scripted init, then `wavedash dev`.
7. Upload only after local build and sandbox testing pass.
8. Publish only when the user explicitly asks.

## Feature-first scaffolds

- Achievements/stats: create identifiers first, then wire `requestStats`,
  `getStat`, `setStat`, `setAchievement`, and `storeStats`.
- Leaderboards: resolve a leaderboard name to an ID with `getLeaderboard` or
  `getOrCreateLeaderboard`, then upload scores with `uploadLeaderboardScore`.
- Cloud saves: write local bytes, then call `uploadRemoteFile`; load with
  `downloadRemoteFile` then `readLocalFile`.
- Multiplayer: subscribe to `LOBBY_JOINED` before `createLobby` or `joinLobby`;
  use P2P only after lobby membership and connection events are established.

## Quality bar for generated games

- No blank or placeholder-only screens.
- No instructions-only "game"; make the primary interaction playable.
- Keep UI text readable at common desktop and mobile widths.
- Do not rely on Escape as the only pause/menu key.
- Warm up shaders/materials before the first active gameplay moment.
- Handle tab focus loss, fullscreen exit, pointer-lock exit, and muted audio.
- Keep asset size reasonable for web loading.
