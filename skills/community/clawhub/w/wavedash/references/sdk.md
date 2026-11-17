# SDK Integration

Canonical docs:

- SDK overview: https://docs.wavedash.com/sdk/overview
- SDK setup: https://docs.wavedash.com/sdk/setup
- Players: https://docs.wavedash.com/sdk/players
- Achievements and stats: https://docs.wavedash.com/sdk/achievements
- Leaderboards: https://docs.wavedash.com/sdk/leaderboards
- Cloud saves: https://docs.wavedash.com/sdk/cloud-saves
- User-generated content: https://docs.wavedash.com/sdk/ugc
- Multiplayer lobbies: https://docs.wavedash.com/multiplayer/lobbies
- Networking: https://docs.wavedash.com/multiplayer/networking
- Events: https://docs.wavedash.com/sdk/events
- Types: https://docs.wavedash.com/sdk/types
- Functions: https://docs.wavedash.com/sdk/functions

## Required init

Every game must initialize Wavedash once when it is ready to show:

```javascript
Wavedash.init();
```

For games with loading work, report progress first:

```javascript
Wavedash.updateLoadProgressZeroToOne(0.0);
await loadAssets();
Wavedash.updateLoadProgressZeroToOne(1.0);
Wavedash.init();
```

For TypeScript/editor types:

```bash
npm install @wvdsh/sdk-js
```

```typescript
import Wavedash from "@wvdsh/sdk-js";

Wavedash.init({ debug: true });
```

The platform injects the SDK when the game runs on Wavedash. The npm package is
for types and import ergonomics.

## Feature routing

- Player identity: read `sdk/players`.
- Achievements or stats: define items in Developer Portal or CLI, then read
  `sdk/achievements`.
- Leaderboards: read `sdk/leaderboards`.
- Cloud saves: read `sdk/cloud-saves`.
- User-generated content: read `sdk/ugc`.
- Multiplayer: read `multiplayer/lobbies` first, then `multiplayer/networking`.
- Events and exact method names: read `sdk/events`, `sdk/functions`, and
  `sdk/types`.

## JavaScript quick reference

Use this only as a routing and sanity-check reference. Read the canonical docs
for the feature before implementing non-trivial behavior.

Load lifecycle:

```javascript
Wavedash.updateLoadProgressZeroToOne(0.5);
Wavedash.init({ debug: true, deferEvents: true });
Wavedash.readyForEvents();
```

Player:

```javascript
const user = Wavedash.getUser();
const userId = Wavedash.getUserId();
const username = Wavedash.getUsername();
const jwt = await Wavedash.getUserJwt();
```

Stats and achievements:

```javascript
await Wavedash.requestStats();
const kills = Wavedash.getStat("total_kills") || 0;
Wavedash.setStat("total_kills", kills + 1, true);
Wavedash.setAchievement("first_blood", true);
await Wavedash.storeStats();
```

Leaderboards:

```javascript
const lb = await Wavedash.getOrCreateLeaderboard(
  "high-scores",
  Wavedash.LeaderboardSortOrder.DESC,
  Wavedash.LeaderboardDisplayType.NUMERIC
);
if (lb.success) {
  await Wavedash.uploadLeaderboardScore(lb.data.id, score, true);
}
```

Cloud saves:

```javascript
await Wavedash.writeLocalFile("saves/slot1.json", bytes);
await Wavedash.uploadRemoteFile("saves/slot1.json");
await Wavedash.downloadRemoteFile("saves/slot1.json");
const bytes = await Wavedash.readLocalFile("saves/slot1.json");
```

Lobbies and P2P:

```javascript
Wavedash.on(Wavedash.Events.LOBBY_JOINED, (payload) => {
  console.log(payload.lobbyId, payload.users.length);
});
await Wavedash.createLobby(Wavedash.LobbyVisibility.PUBLIC, 4);
Wavedash.broadcastP2PMessage(0, true, new Uint8Array([1, 2, 3]));
const message = Wavedash.readP2PMessageFromChannel(0);
```

UGC:

```javascript
const ugc = await Wavedash.createUGCItem(
  Wavedash.UGCType.COMMUNITY,
  "Custom arena",
  "Uploaded from editor",
  Wavedash.UGCVisibility.PUBLIC,
  "ugc/levels/arena.wdc"
);
```

## Traps to avoid

- Do not call multiplayer join logic before subscribing to the relevant lobby
  events.
- Creating a lobby already joins it; do not immediately call join on the lobby
  returned by create unless the docs say otherwise.
- Do not invent identifiers for achievements/stats in code without making sure
  they exist in the game configuration.
- Do not assume local browser testing equals Wavedash testing; run `wavedash dev`
  or test an uploaded build.
