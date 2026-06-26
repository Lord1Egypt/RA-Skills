# MusicKit + MediaPlayer Extended Patterns

Overflow reference for the `musickit` skill. Contains advanced patterns that exceed the main skill file's scope.

## Contents

- [MusicKit SwiftUI Integration](#musickit-swiftui-integration)
- [Genre and Chart Browsing](#genre-and-chart-browsing)
- [Library Management](#library-management)
- [Playlist Access](#playlist-access)
- [Now Playing Session](#now-playing-session)
- [Background Audio Configuration](#background-audio-configuration)

## MusicKit SwiftUI Integration

### Music Player Manager with `@Observable`

```swift
import MusicKit
import MediaPlayer

@Observable
@MainActor
final class MusicPlayerManager {
    let player = ApplicationMusicPlayer.shared

    var currentSong: Song?
    var isPlaying = false
    var playbackTime: TimeInterval = 0
    var queue: [Song] = []
    var hasSubscription = false

    func setup() async {
        // Check authorization
        let status = await MusicAuthorization.request()
        guard status == .authorized else { return }

        // Check subscription
        if let subscription = try? await MusicSubscription.current {
            hasSubscription = subscription.canPlayCatalogContent
        }

        // Observe subscription changes
        Task {
            for await subscription in MusicSubscription.subscriptionUpdates {
                hasSubscription = subscription.canPlayCatalogContent
            }
        }
    }

    func play(_ song: Song) async throws {
        guard hasSubscription else { return }
        player.queue = [song]
        try await player.play()
        currentSong = song
        isPlaying = true
    }

    func togglePlayPause() {
        if player.state.playbackStatus == .playing {
            player.pause()
            isPlaying = false
        } else {
            Task {
                try? await player.play()
                isPlaying = true
            }
        }
    }

    func skip() async {
        try? await player.skipToNextEntry()
    }
}
```

### SwiftUI Player View

```swift
import SwiftUI
import MusicKit

struct MiniPlayerView: View {
    @Environment(MusicPlayerManager.self) private var manager

    var body: some View {
        HStack {
            if let song = manager.currentSong {
                if let artwork = song.artwork {
                    ArtworkImage(artwork, width: 44, height: 44)
                        .clipShape(.rect(cornerRadius: 6))
                }

                VStack(alignment: .leading) {
                    Text(song.title)
                        .font(.subheadline)
                        .lineLimit(1)
                    Text(song.artistName)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }

                Spacer()

                Button {
                    manager.togglePlayPause()
                } label: {
                    Image(systemName: manager.isPlaying ? "pause.fill" : "play.fill")
                        .font(.title2)
                }

                Button {
                    Task { await manager.skip() }
                } label: {
                    Image(systemName: "forward.fill")
                }
            }
        }
        .padding(.horizontal)
        .frame(height: 60)
    }
}
```

### Search View

```swift
struct MusicSearchView: View {
    @State private var searchText = ""
    @State private var results: MusicItemCollection<Song> = []
    @Environment(MusicPlayerManager.self) private var manager

    var body: some View {
        NavigationStack {
            List(results) { song in
                Button {
                    Task { try? await manager.play(song) }
                } label: {
                    HStack {
                        if let artwork = song.artwork {
                            ArtworkImage(artwork, width: 50, height: 50)
                                .clipShape(.rect(cornerRadius: 4))
                        }
                        VStack(alignment: .leading) {
                            Text(song.title)
                            Text(song.artistName)
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                }
            }
            .searchable(text: $searchText, prompt: "Search Apple Music")
            .onChange(of: searchText) {
                Task { await search() }
            }
            .navigationTitle("Search")
        }
    }

    private func search() async {
        guard !searchText.isEmpty else {
            results = []
            return
        }
        var request = MusicCatalogSearchRequest(term: searchText, types: [Song.self])
        request.limit = 25
        if let response = try? await request.response() {
            results = response.songs
        }
    }
}
```

## Genre and Chart Browsing

### Fetching Top Charts

```swift
func fetchTopSongs() async throws -> MusicItemCollection<Song> {
    var request = MusicCatalogChartsRequest(
        genre: nil,
        kinds: [.mostPlayed],
        types: [Song.self]
    )
    request.limit = 50
    let response = try await request.response()
    return response.songCharts.first?.items ?? []
}
```

### Fetching by Genre

```swift
func fetchSongsByGenre(_ genre: Genre) async throws -> MusicItemCollection<Song> {
    var request = MusicCatalogSearchRequest(term: genre.name, types: [Song.self])
    request.limit = 25
    let response = try await request.response()
    return response.songs
}
```

## Library Management

Library writes require MusicKit authorization and an enabled iCloud Music Library.
Check `MusicSubscription.current.hasCloudLibraryEnabled` before adding items or
modifying playlists.

### Adding to Library

```swift
func addToLibrary(_ song: Song) async throws {
    guard MusicAuthorization.currentStatus == .authorized else { return }
    let subscription = try await MusicSubscription.current
    guard subscription.hasCloudLibraryEnabled else { return }

    try await MusicLibrary.shared.add(song)
}

func addAlbumToLibrary(_ album: Album) async throws {
    guard MusicAuthorization.currentStatus == .authorized else { return }
    let subscription = try await MusicSubscription.current
    guard subscription.hasCloudLibraryEnabled else { return }

    try await MusicLibrary.shared.add(album)
}
```

### Fetching Library Content

```swift
func fetchLibrarySongs() async throws -> MusicItemCollection<Song> {
    var request = MusicLibraryRequest<Song>()
    request.sort(by: \.lastPlayedDate, ascending: false)
    request.limit = 50
    let response = try await request.response()
    return response.items
}
```

## Playlist Access

### Fetching User Playlists

```swift
func fetchPlaylists() async throws -> MusicItemCollection<Playlist> {
    var request = MusicLibraryRequest<Playlist>()
    request.sort(by: \.lastModifiedDate, ascending: false)
    let response = try await request.response()
    return response.items
}
```

### Adding Tracks to a Playlist

```swift
func addToPlaylist(_ playlist: Playlist, songs: [Song]) async throws {
    guard MusicAuthorization.currentStatus == .authorized else { return }
    let subscription = try await MusicSubscription.current
    guard subscription.hasCloudLibraryEnabled else { return }

    try await MusicLibrary.shared.add(songs, to: playlist)
}
```

## Now Playing Session

Use `MPNowPlayingSession` when your app manages multiple simultaneous audio
sessions (e.g., picture-in-picture video plus background music).

```swift
import MediaPlayer
import AVFoundation

func createNowPlayingSession(for player: AVPlayer) -> MPNowPlayingSession {
    let session = MPNowPlayingSession(players: [player])

    // Session-scoped remote command center
    session.remoteCommandCenter.playCommand.addTarget { _ in
        player.play()
        return .success
    }

    session.remoteCommandCenter.pauseCommand.addTarget { _ in
        player.pause()
        return .success
    }

    // Session-scoped now playing info
    session.nowPlayingInfoCenter.nowPlayingInfo = [
        MPMediaItemPropertyTitle: "Track Title",
        MPMediaItemPropertyArtist: "Artist Name"
    ]

    // Activate this session to become the "now playing" app
    session.becomeActiveIfPossible { success in
        print("Now playing session active: \(success)")
    }

    return session
}
```

## Background Audio Configuration

### Audio Session Setup

Configure the audio session before starting playback to enable background audio.

```swift
import AVFoundation

func configureAudioSession() throws {
    let session = AVAudioSession.sharedInstance()
    try session.setCategory(.playback, mode: .default)
    try session.setActive(true)
}
```

### Info.plist Background Mode

Add `audio` to `UIBackgroundModes` in Info.plist:

```xml
<key>UIBackgroundModes</key>
<array>
    <string>audio</string>
</array>
```

### Handling Interruptions

```swift
func observeInterruptions() {
    NotificationCenter.default.addObserver(
        forName: AVAudioSession.interruptionNotification,
        object: AVAudioSession.sharedInstance(),
        queue: .main
    ) { notification in
        guard let typeValue = notification.userInfo?[AVAudioSessionInterruptionTypeKey] as? UInt,
              let type = AVAudioSession.InterruptionType(rawValue: typeValue) else {
            return
        }

        switch type {
        case .began:
            // Pause UI, save state
            break
        case .ended:
            let options = notification.userInfo?[AVAudioSessionInterruptionOptionKey] as? UInt
            if let options, AVAudioSession.InterruptionOptions(rawValue: options).contains(.shouldResume) {
                // Resume playback
            }
        @unknown default:
            break
        }
    }
}
```

### Route Change Handling

Pause playback when headphones are unplugged to avoid unexpected speaker output.

```swift
func observeRouteChanges() {
    NotificationCenter.default.addObserver(
        forName: AVAudioSession.routeChangeNotification,
        object: AVAudioSession.sharedInstance(),
        queue: .main
    ) { notification in
        guard let reasonValue = notification.userInfo?[AVAudioSessionRouteChangeReasonKey] as? UInt,
              let reason = AVAudioSession.RouteChangeReason(rawValue: reasonValue) else {
            return
        }

        if reason == .oldDeviceUnavailable {
            // Headphones were unplugged -- pause playback
            pausePlayback()
        }
    }
}
```
