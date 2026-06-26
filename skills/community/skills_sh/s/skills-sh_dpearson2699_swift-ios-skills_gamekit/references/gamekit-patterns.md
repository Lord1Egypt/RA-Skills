# GameKit Patterns

Advanced GameKit patterns for player identity verification, legacy voice chat,
saved games, custom matchmaking UI, leaderboard images, challenge handling, and
rule-based matchmaking.

## Contents

- [Server-Side Identity Verification](#server-side-identity-verification)
- [Voice Chat](#voice-chat)
- [Saved Games](#saved-games)
- [Custom Matchmaking UI](#custom-matchmaking-ui)
- [Leaderboard Images and Sets](#leaderboard-images-and-sets)
- [Challenge Handling](#challenge-handling)
- [Rule-Based Matchmaking](#rule-based-matchmaking)
- [Player Groups and Attributes](#player-groups-and-attributes)
- [Hosted Matches](#hosted-matches)
- [Turn-Based Data Exchanges](#turn-based-data-exchanges)
- [Friend Management](#friend-management)
- [Nearby Player Discovery](#nearby-player-discovery)
- [SharePlay Integration](#shareplay-integration)

## Server-Side Identity Verification

Verify the local player on a backend server using a cryptographic signature
from the async identity-verification API:

```swift
enum GameKitIdentityError: Error {
    case missingBundleIdentifier
}

func verifyPlayerOnServer() async throws {
    let (publicKeyURL, signature, salt, timestamp) =
        try await GKLocalPlayer.local.fetchItemsForIdentityVerificationSignature()

    // Send these values plus the bundle ID and a scoped player identifier.
    // Use teamPlayerID for most games, or gamePlayerID for Apple Arcade games.
    let playerID = GKLocalPlayer.local.teamPlayerID
    guard let bundleID = Bundle.main.bundleIdentifier else {
        throw GameKitIdentityError.missingBundleIdentifier
    }
    sendToServer(publicKeyURL, signature, salt, timestamp, playerID, bundleID)
}
```

The server fetches the public key from the URL Apple provides, then verifies
that Apple signed it. Verify the signature over this byte sequence:
`teamPlayerID` (or Apple Arcade `gamePlayerID`) as UTF-8, bundle ID as UTF-8,
timestamp as big-endian `UInt64`, then salt. Reject stale timestamps and trust
only fields covered by the signature.

## Voice Chat

`GKVoiceChat` is deprecated. Prefer SharePlay for new voice or social audio
work. Keep this section only for maintaining existing GameKit voice chat.
Each named channel supports independent volume and mute controls.

### Prerequisites

Add `NSMicrophoneUsageDescription` to Info.plist, activate an audio session, and
check `GKVoiceChat.isVoIPAllowed()` before creating channels.

```swift
import AVFoundation

func configureAudioSession() throws {
    let session = AVAudioSession.sharedInstance()
    try session.setActive(true)
}
```

### Creating and Starting a Channel

Create voice chat channels from a `GKMatch` object:

```swift
func startVoiceChat(in match: GKMatch) {
    guard GKVoiceChat.isVoIPAllowed() else { return }

    guard let voiceChat = match.voiceChat(withName: "teamChat") else { return }
    voiceChat.volume = 0.8
    voiceChat.start()
    voiceChat.isActive = true

    voiceChat.playerVoiceChatStateDidChangeHandler = { player, state in
        switch state {
        case .connected:
            print("\(player.displayName) joined voice chat")
        case .disconnected:
            print("\(player.displayName) left voice chat")
        case .speaking:
            // Update UI to show speaking indicator
            self.showSpeakingIndicator(for: player)
        case .silent:
            self.hideSpeakingIndicator(for: player)
        case .connecting:
            break
        @unknown default:
            break
        }
    }
}
```

### Multiple Channels

Create separate channels for different purposes, such as team chat and global
chat. A player can only have their microphone active in one channel at a time:

```swift
let teamChat = match.voiceChat(withName: "team")
let allChat = match.voiceChat(withName: "all")

// Start both but activate only one microphone at a time
teamChat?.start()
allChat?.start()
teamChat?.isActive = true
allChat?.isActive = false

// Switch active channel
func switchToAllChat() {
    teamChat?.isActive = false
    allChat?.isActive = true
}
```

### Muting Players

```swift
func mutePlayer(_ player: GKPlayer, in voiceChat: GKVoiceChat) {
    voiceChat.setPlayer(player, muted: true)
}

func unmutePlayer(_ player: GKPlayer, in voiceChat: GKVoiceChat) {
    voiceChat.setPlayer(player, muted: false)
}
```

### Stopping Voice Chat

```swift
func stopVoiceChat(_ voiceChat: GKVoiceChat) {
    voiceChat.isActive = false
    voiceChat.stop()
}
```

## Saved Games

GameKit stores game data in the player's iCloud account, accessible from devices
using the same Game Center account. The player must have an iCloud account and
iCloud Drive enabled, and the app needs the iCloud capability with an iCloud
container identifier. Saved games are managed through `GKLocalPlayer` and
represented by `GKSavedGame`.

### Saving Game Data

Encode game state and save with a descriptive name:

```swift
func saveGame(state: GameState, name: String) async throws {
    let data = try JSONEncoder().encode(state)
    try await GKLocalPlayer.local.saveGameData(data, withName: name)
}
```

Saving with an existing filename overwrites that file. Use unique filenames for
multiple save slots. Duplicate filenames from multiple devices are conflicts
that your game must resolve.

### Fetching Saved Games

```swift
func fetchSavedGames() async throws -> [GKSavedGame] {
    try await GKLocalPlayer.local.fetchSavedGames()
}
```

### Loading Saved Game Data

```swift
func loadSavedGame(_ savedGame: GKSavedGame) async throws -> GameState {
    let data = try await savedGame.loadData()
    return try JSONDecoder().decode(GameState.self, from: data)
}
```

`GKSavedGame` properties: `name`, `modificationDate`, `deviceName`.

### Resolving Conflicts

When the same save name exists from multiple devices, GameKit may report
conflicts. Resolve them by choosing the authoritative data:

```swift
func resolveConflicts(_ conflicts: [GKSavedGame], using data: Data) async throws {
    try await GKLocalPlayer.local.resolveConflictingSavedGames(
        conflicts, with: data
    )
}
```

### Listening for Saved Game Events

Implement `GKSavedGameListener`, or `GKLocalPlayerListener` if the same object
handles multiple Game Center events, to respond to save events from other
devices:

```swift
extension GameManager: GKSavedGameListener {
    func player(_ player: GKPlayer, didModifySavedGame savedGame: GKSavedGame) {
        // Another device modified a save. Refresh local data.
        Task { await refreshSavedGames() }
    }

    func player(_ player: GKPlayer,
                hasConflictingSavedGames savedGames: [GKSavedGame]) {
        // Resolve conflicts using game-specific merge logic.
        Task { await resolveConflictingGames(savedGames) }
    }
}
```

Register the listener:

```swift
GKLocalPlayer.local.register(gameManager)
```

### Deleting Saved Games

```swift
func deleteSavedGame(name: String) async throws {
    try await GKLocalPlayer.local.deleteSavedGames(withName: name)
}
```

## Custom Matchmaking UI

Build a custom interface for finding players instead of using
`GKMatchmakerViewController`. Use `GKMatchmaker` directly.

### Finding a Match Programmatically

```swift
actor MatchManager {
    private var currentMatch: GKMatch?

    func findMatch(minPlayers: Int, maxPlayers: Int) async throws -> GKMatch {
        let request = GKMatchRequest()
        request.minPlayers = minPlayers
        request.maxPlayers = maxPlayers

        let match = try await GKMatchmaker.shared().findMatch(for: request)
        GKMatchmaker.shared().finishMatchmaking(for: match)
        currentMatch = match
        return match
    }

    func cancelMatchmaking() {
        GKMatchmaker.shared().cancel()
    }
}
```

### Adding Players to an Existing Match

```swift
func addPlayers(to match: GKMatch, request: GKMatchRequest) async throws {
    try await GKMatchmaker.shared().addPlayers(
        to: match,
        matchRequest: request
    )
}
```

### Querying Matchmaking Activity

Check how many players are currently looking for matches:

```swift
func checkActivity() async throws -> Int {
    try await GKMatchmaker.shared().queryActivity()
}

func checkGroupActivity(group: Int) async throws -> Int {
    try await GKMatchmaker.shared().queryPlayerGroupActivity(group)
}
```

### Inviting Specific Players

```swift
func invitePlayers(_ players: [GKPlayer]) async throws -> GKMatch {
    let request = GKMatchRequest()
    request.minPlayers = 2
    request.maxPlayers = 4
    request.recipients = players
    request.inviteMessage = "Play a round?"
    request.recipientResponseHandler = { player, response in
        switch response {
        case .accepted:
            print("\(player.displayName) accepted")
        case .declined:
            print("\(player.displayName) declined")
        default:
            break
        }
    }

    return try await GKMatchmaker.shared().findMatch(for: request)
}
```

## Leaderboard Images and Sets

### Loading Leaderboard Images

Leaderboard images configured in App Store Connect are not loaded with the
leaderboard data. Fetch them separately:

```swift
func loadLeaderboardImage(leaderboardID: String) async throws -> UIImage? {
    let leaderboards = try await GKLeaderboard.loadLeaderboards(
        IDs: [leaderboardID]
    )
    guard let leaderboard = leaderboards.first else { return nil }
    return try await leaderboard.loadImage()
}
```

### Leaderboard Sets

Leaderboard sets group related leaderboards together. Load sets and then load
the leaderboards within each set:

```swift
func loadLeaderboardSets() async throws -> [GKLeaderboardSet] {
    try await GKLeaderboardSet.loadLeaderboardSets()
}

func loadLeaderboards(in set: GKLeaderboardSet) async throws -> [GKLeaderboard] {
    try await set.loadLeaderboards()
}
```

### Leaderboard Entry Properties

`GKLeaderboard.Entry` provides these properties for display:

```swift
func displayEntry(_ entry: GKLeaderboard.Entry) {
    let playerName = entry.player.displayName
    let rank = entry.rank
    let score = entry.score
    let formatted = entry.formattedScore
    let context = entry.context    // Game-defined value submitted with the score
    let date = entry.date
}
```

### Submitting Scores with Context

Use `context` to store additional metadata with a score, such as the level
where the score was achieved:

```swift
try await GKLeaderboard.submitScore(
    score,
    context: levelID,
    player: GKLocalPlayer.local,
    leaderboardIDs: ["com.mygame.scores"]
)
```

## Challenge Handling

Players can challenge friends to beat their scores or complete achievements.

### Achievement Challenges

```swift
func challengeFriends(
    achievementID: String,
    message: String,
    players: [GKPlayer]
) {
    let achievement = GKAchievement(identifier: achievementID)
    let vc = achievement.challengeComposeController(
        withMessage: message,
        players: players
    ) { composeVC, issued, sentPlayers in
        composeVC.dismiss(animated: true)
    }
    present(vc, animated: true)
}
```

### Finding Challengeable Players

```swift
func loadChallengeableFriends() async throws -> [GKPlayer] {
    try await GKLocalPlayer.local.loadChallengableFriends()
}
```

### Selecting Players Who Can Earn an Achievement

Filter players who haven't already completed an achievement:

```swift
func findEligiblePlayers(
    for achievementID: String,
    from players: [GKPlayer]
) async throws -> [GKPlayer] {
    let achievement = GKAchievement(identifier: achievementID)
    return try await achievement.selectChallengeablePlayers(players)
}
```

### Opening the Challenges View

```swift
GKAccessPoint.shared.triggerForChallenges { }
```

## Rule-Based Matchmaking

Configure matchmaking rules in App Store Connect to refine player matching
based on game-specific criteria. Rules evaluate player properties to determine
compatible matches. `queueName`, `properties`, `recipientProperties`,
`GKMatch.properties`, and `GKMatch.playerProperties` require iOS 17.2+ or the
equivalent platform releases.

`queueName` must be a case-sensitive reverse-DNS-style identifier using only
letters, numbers, hyphens, and periods. `properties` and `recipientProperties`
must be JSON-serializable, and the key `gc` is reserved by GameKit.

### Setting Up Rule-Based Matching

```swift
func findRuleBasedMatch(skill: Int, region: String) async throws -> GKMatch {
    let request = GKMatchRequest()
    request.minPlayers = 2
    request.maxPlayers = 4
    request.queueName = "com.mygame.competitive"
    request.properties = [
        "skill": skill,
        "region": region
    ]

    let match = try await GKMatchmaker.shared().findMatch(for: request)
    GKMatchmaker.shared().finishMatchmaking(for: match)
    return match
}
```

### Accessing Match Properties

After a match is found, read the properties that matchmaking rules evaluated:

```swift
func inspectMatchProperties(_ match: GKMatch) {
    // Local player's properties (includes rule additions)
    let myProps = match.properties

    // Other players' properties
    for (player, props) in match.playerProperties ?? [:] {
        print("\(player.displayName): \(props)")
    }
}
```

### Rule-Based Matching with Invited Players

Set properties for invited recipients. Every key in `recipientProperties` must
also be present in `recipients`.

```swift
func inviteWithRules(
    players: [GKPlayer],
    properties: [String: Any]
) async throws -> GKMatch {
    let request = GKMatchRequest()
    request.minPlayers = 2
    request.maxPlayers = 4
    request.queueName = "com.mygame.competitive"
    request.recipients = players
    request.properties = properties

    var recipientProps: [GKPlayer: [String: Any]] = [:]
    for player in players {
        recipientProps[player] = ["skill": 1000]  // Default skill for invitees
    }
    request.recipientProperties = recipientProps

    return try await GKMatchmaker.shared().findMatch(for: request)
}
```

When `queueName` is set, `playerGroup` and `playerAttributes` are ignored.

## Player Groups and Attributes

Use player groups and attributes for simple matchmaking without rules.

### Player Groups

Restrict matching to players in the same group. Groups are identified by an
integer value:

```swift
let request = GKMatchRequest()
request.minPlayers = 2
request.maxPlayers = 4
request.playerGroup = 42  // Only matches players in group 42
```

Use groups to separate players by game mode, difficulty, or map.

### Player Attributes

Use `playerAttributes` only for simple non-rule-based matchmaking. If the value
is nonzero, GameKit tries to combine players so the bitwise OR of all
participants' masks equals `0xFFFFFFFF`:

```swift
let attackerMask: UInt32 = 0x000000FF
let defenderMask: UInt32 = 0x0000FF00
let supportMask:  UInt32 = 0xFFFF0000

let request = GKMatchRequest()
request.minPlayers = 3
request.maxPlayers = 3
request.playerAttributes = attackerMask
```

Use matchmaking rules for modern skill, region, version, party-code, and team
assignment logic. When `queueName` is set, GameKit ignores `playerGroup` and
`playerAttributes`.

## Hosted Matches

For server-hosted games, use `GKMatchmaker` to find players but handle
networking through your own infrastructure.

```swift
func findPlayersForHostedMatch() async throws -> [GKPlayer] {
    let request = GKMatchRequest()
    request.minPlayers = 2
    request.maxPlayers = 8

    let players = try await GKMatchmaker.shared().findPlayers(
        forHostedRequest: request
    )
    // Connect players through your game server
    return players
}
```

### Hosted Match with Matchmaking Rules

```swift
func findPlayersWithRules() async throws -> GKMatchedPlayers {
    let request = GKMatchRequest()
    request.minPlayers = 2
    request.maxPlayers = 8
    request.queueName = "com.mygame.ranked"
    request.properties = ["elo": 1500]

    let matchedPlayers = try await GKMatchmaker.shared().findMatchedPlayers(
        request
    )

    // matchedPlayers.players - the matched players
    // matchedPlayers.properties - the local player's properties
    // matchedPlayers.playerProperties - other players' properties
    return matchedPlayers
}
```

## Turn-Based Data Exchanges

Exchange data between participants in a turn-based match without waiting for
turns. Useful for trading items, sending gifts, or requesting actions.

### Sending an Exchange

```swift
enum TurnExchangeError: Error {
    case dataTooLarge
}

func sendExchange(
    match: GKTurnBasedMatch,
    to recipients: [GKTurnBasedParticipant],
    data: Data
) async throws -> GKTurnBasedExchange {
    guard data.count <= match.exchangeDataMaximumSize else {
        throw TurnExchangeError.dataTooLarge
    }

    try await match.sendExchange(
        to: recipients,
        data: data,
        localizableMessageKey: "EXCHANGE_REQUEST",
        arguments: [],
        timeout: GKExchangeTimeoutDefault
    )
}
```

### Handling Exchange Events

```swift
extension GameManager: GKTurnBasedEventListener {
    func player(
        _ player: GKPlayer,
        receivedExchangeRequest exchange: GKTurnBasedExchange,
        for match: GKTurnBasedMatch
    ) {
        // Process the exchange request and reply
        let responseData = buildResponse(for: exchange)
        Task {
            try await exchange.reply(
                withLocalizableMessageKey: "EXCHANGE_REPLY",
                arguments: [],
                data: responseData
            )
        }
    }

    func player(
        _ player: GKPlayer,
        receivedExchangeReplies replies: [GKTurnBasedExchangeReply],
        forCompletedExchange exchange: GKTurnBasedExchange,
        for match: GKTurnBasedMatch
    ) {
        // All recipients replied. Merge exchange data into match state.
        Task {
            let mergedData = mergeExchangeData(exchange, replies: replies)
            try await match.saveMergedMatch(
                mergedData,
                withResolvedExchanges: [exchange]
            )
        }
    }
}
```

### Exchange Limits

- `exchangeDataMaximumSize`: maximum size per exchange payload
- `exchangeMaxInitiatedExchangesPerPlayer`: maximum concurrent outgoing exchanges

### Ending a Turn-Based Match with Scores

Submit leaderboard scores and achievements when the match ends:

```swift
func endMatchWithScores(
    match: GKTurnBasedMatch,
    data: Data,
    scores: [GKLeaderboardScore],
    achievements: [GKAchievement]
) async throws {
    for participant in match.participants {
        participant.matchOutcome = determineOutcome(for: participant)
    }
    try await match.endMatchInTurn(
        withMatch: data,
        leaderboardScores: scores,
        achievements: achievements
    )
}
```

## Friend Management

### Loading Friends

Requires the `NSGKFriendListUsageDescription` key in Info.plist:

```swift
func loadFriends() async throws -> [GKPlayer] {
    let status = try await GKLocalPlayer.local.loadFriendsAuthorizationStatus()
    guard status == .authorized else { return [] }
    return try await GKLocalPlayer.local.loadFriends()
}
```

### Presenting Friend Request UI

```swift
func sendFriendRequest(from viewController: UIViewController) async {
    guard !GKLocalPlayer.local.isPresentingFriendRequestViewController else {
        return
    }
    try? await GKLocalPlayer.local.presentFriendRequestCreator(
        from: viewController
    )
}
```

### Loading Recent Players

```swift
func loadRecentPlayers() async throws -> [GKPlayer] {
    try await GKLocalPlayer.local.loadRecentPlayers()
}
```

## Nearby Player Discovery

Find players on the same local network or via Bluetooth for local multiplayer:

```swift
func startBrowsingForNearbyPlayers() {
    GKMatchmaker.shared().startBrowsingForNearbyPlayers { player, reachable in
        if reachable {
            self.addNearbyPlayer(player)
        } else {
            self.removeNearbyPlayer(player)
        }
    }
}

func stopBrowsing() {
    GKMatchmaker.shared().stopBrowsingForNearbyPlayers()
}
```

## SharePlay Integration

Use GameKit's SharePlay bridge when a FaceTime or Messages SharePlay session
should add players to a GameKit match. Keep full GroupActivities session design
outside this GameKit reference.

```swift
func startSharePlayMatch() {
    GKMatchmaker.shared().startGroupActivity { player in
        // A player from the FaceTime call joined.
        // Connect them to the game session.
        self.addSharePlayPlayer(player)
    }
}

func stopSharePlayMatch() {
    GKMatchmaker.shared().stopGroupActivity()
}
```

This creates a group activity on behalf of the player. Combine with
GroupActivities framework for full SharePlay integration in your game UI.
