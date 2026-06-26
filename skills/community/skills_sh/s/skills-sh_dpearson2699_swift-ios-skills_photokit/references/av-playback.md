# AV Playback

Patterns for media playback with AVPlayer, streaming HLS content, audio
session configuration, background audio, Now Playing integration, remote
command handling, and Picture-in-Picture.

## Contents

- [AVPlayer and AVPlayerViewController Setup](#avplayer-and-avplayerviewcontroller-setup)
- [AVPlayerItem and AVAsset Loading](#avplayeritem-and-avasset-loading)
- [Playback Controls](#playback-controls)
- [Observing Player State and Time](#observing-player-state-and-time)
- [Streaming HLS Content](#streaming-hls-content)
- [AVAudioSession Configuration](#avaudiosession-configuration)
- [Background Audio Setup](#background-audio-setup)
- [Now Playing Info Center](#now-playing-info-center)
- [MPRemoteCommandCenter](#mpremotecommandcenter)
- [Picture-in-Picture](#picture-in-picture)

## AVPlayer and AVPlayerViewController Setup

`AVPlayer` manages playback of a single media asset. Use
`AVPlayerViewController` (AVKit) for the system-standard playback UI with
transport controls, or `AVPlayerLayer` for a custom player interface.

Docs: [AVPlayer](https://sosumi.ai/documentation/avfoundation/avplayer),
[AVPlayerViewController](https://sosumi.ai/documentation/avkit/avplayerviewcontroller)

### AVPlayerViewController in SwiftUI

```swift
import SwiftUI
import AVKit

struct VideoPlayerView: View {
    let url: URL
    @State private var player: AVPlayer?

    var body: some View {
        VideoPlayer(player: player)
            .onAppear {
                player = AVPlayer(url: url)
                player?.play()
            }
            .onDisappear {
                player?.pause()
                player = nil
            }
    }
}
```

### AVPlayerViewController in UIKit

```swift
import UIKit
import AVKit

final class VideoViewController: UIViewController {
    private var player: AVPlayer?

    func presentVideo(url: URL) {
        player = AVPlayer(url: url)
        let controller = AVPlayerViewController()
        controller.player = player
        present(controller, animated: true) {
            self.player?.play()
        }
    }
}
```

### Custom Player with AVPlayerLayer

For full control over the player UI, embed an `AVPlayerLayer`:

```swift
import AVFoundation
import UIKit

final class PlayerView: UIView {
    override class var layerClass: AnyClass { AVPlayerLayer.self }

    var playerLayer: AVPlayerLayer { layer as! AVPlayerLayer }

    var player: AVPlayer? {
        get { playerLayer.player }
        set { playerLayer.player = newValue }
    }

    func configure() {
        playerLayer.videoGravity = .resizeAspect
    }
}
```

## AVPlayerItem and AVAsset Loading

`AVAsset` represents the static media (duration, tracks, metadata).
`AVPlayerItem` adds the dynamic state (current time, buffering status) needed
for playback.

Docs: [AVPlayerItem](https://sosumi.ai/documentation/avfoundation/avplayeritem),
[AVAsset](https://sosumi.ai/documentation/avfoundation/avasset)

```swift
import AVFoundation

// Local file
let localURL = Bundle.main.url(forResource: "intro", withExtension: "mp4")!
let localItem = AVPlayerItem(url: localURL)

// Remote file
let remoteURL = URL(string: "https://example.com/video.mp4")!
let remoteItem = AVPlayerItem(url: remoteURL)

// From an existing AVAsset (for more control)
let asset = AVURLAsset(url: remoteURL, options: [
    AVURLAssetPreferPreciseDurationAndTimingKey: true
])

// Load properties asynchronously before playback (iOS 15+)
let duration = try await asset.load(.duration)
let tracks = try await asset.load(.tracks)
let isPlayable = try await asset.load(.isPlayable)

let item = AVPlayerItem(asset: asset)
let player = AVPlayer(playerItem: item)
```

### Replacing the Current Item

Reuse a single `AVPlayer` and swap items:

```swift
let nextItem = AVPlayerItem(url: nextVideoURL)
player.replaceCurrentItem(with: nextItem)
player.play()
```

### Queue Playback with AVQueuePlayer

```swift
let items = videoURLs.map { AVPlayerItem(url: $0) }
let queuePlayer = AVQueuePlayer(items: items)
queuePlayer.play()
// Automatically advances to the next item
```

## Playback Controls

```swift
// Play
player.play()

// Pause
player.pause()

// Set playback rate (1.0 = normal, 2.0 = 2x, 0.5 = half speed)
player.rate = 1.5

// Seek to a specific time
let targetTime = CMTime(seconds: 30, preferredTimescale: 600)
await player.seek(to: targetTime)

// Seek with tolerance (for precise seeking, e.g., scrubbing)
await player.seek(
    to: targetTime,
    toleranceBefore: .zero,
    toleranceAfter: .zero
)

// Seek to a percentage of duration
func seekToPercentage(_ percentage: Double) async {
    guard let duration = player.currentItem?.duration,
          duration.isNumeric else { return }
    let targetSeconds = duration.seconds * percentage
    let target = CMTime(seconds: targetSeconds, preferredTimescale: 600)
    await player.seek(to: target)
}
```

## Observing Player State and Time

### Periodic Time Observer

Use `addPeriodicTimeObserver` to update UI elements like a progress bar:

```swift
import AVFoundation

@Observable
@MainActor
final class PlayerManager {
    let player = AVPlayer()
    var currentTime: Double = 0
    var duration: Double = 0
    var isPlaying = false

    private var timeObserver: Any?

    func startObserving() {
        // Fire every 0.5 seconds on the main queue
        let interval = CMTime(seconds: 0.5, preferredTimescale: 600)
        timeObserver = player.addPeriodicTimeObserver(
            forInterval: interval,
            queue: .main
        ) { [weak self] time in
            guard let self else { return }
            self.currentTime = time.seconds
            self.duration = self.player.currentItem?.duration.seconds ?? 0
            self.isPlaying = self.player.timeControlStatus == .playing
        }
    }

    func stopObserving() {
        if let observer = timeObserver {
            player.removeTimeObserver(observer)
            timeObserver = nil
        }
    }

    deinit {
        if let observer = timeObserver {
            player.removeTimeObserver(observer)
        }
    }
}
```

### Observing Player Status with KVO

Check player and item readiness before playing:

```swift
import AVFoundation
import Combine

// Using Combine
var cancellables = Set<AnyCancellable>()

player.publisher(for: \.status)
    .sink { status in
        switch status {
        case .readyToPlay:
            print("Ready to play")
        case .failed:
            print("Failed: \(player.error?.localizedDescription ?? "")")
        case .unknown:
            print("Status unknown")
        @unknown default:
            break
        }
    }
    .store(in: &cancellables)

// Observe buffering state
player.publisher(for: \.timeControlStatus)
    .sink { status in
        switch status {
        case .playing: print("Playing")
        case .paused: print("Paused")
        case .waitingToPlayAtSpecifiedRate:
            print("Buffering: \(player.reasonForWaitingToPlay?.rawValue ?? "")")
        @unknown default: break
        }
    }
    .store(in: &cancellables)
```

### Detecting Playback End

```swift
NotificationCenter.default.addObserver(
    forName: .AVPlayerItemDidPlayToEndTime,
    object: player.currentItem,
    queue: .main
) { _ in
    // Playback finished -- loop, show replay button, or advance
    player.seek(to: .zero)  // Loop
}
```

## Streaming HLS Content

HTTP Live Streaming (HLS) works directly with `AVPlayer`. Pass the `.m3u8`
URL and AVFoundation handles adaptive bitrate selection, buffering, and
failover.

```swift
let hlsURL = URL(string: "https://example.com/stream/master.m3u8")!
let player = AVPlayer(url: hlsURL)
player.play()

// AVPlayer automatically selects the best variant based on:
// - Network bandwidth
// - Device capabilities
// - Display resolution
```

### Preferred Bitrate and Resolution

```swift
let item = AVPlayerItem(url: hlsURL)

// Limit maximum resolution (e.g., for cellular)
item.preferredMaximumResolution = CGSize(width: 1280, height: 720)

// Limit peak bitrate (bits per second)
item.preferredPeakBitRate = 2_000_000  // 2 Mbps

// For forward buffering duration
item.preferredForwardBufferDuration = 5  // seconds; 0 = system default
```

## AVAudioSession Configuration

Configure `AVAudioSession` to tell the system how your app intends to use
audio. This affects audio routing, mixing behavior, and background playback.

Docs: [AVAudioSession](https://sosumi.ai/documentation/avfaudio/avaudiosession),
[AVAudioSession.Category](https://sosumi.ai/documentation/avfaudio/avaudiosession/category-swift.struct)

### Categories and Modes

| Category | Behavior | Common Use |
|---|---|---|
| `.playback` | Audio plays even with silent switch on; can play in background | Music, podcasts, video |
| `.playAndRecord` | Simultaneous input and output | Voice/video calls, recording with monitoring |
| `.ambient` | Mixes with other audio; silenced by switch | Game sound effects, casual audio |
| `.soloAmbient` | Default; silences other audio; silenced by switch | Default app behavior |

```swift
import AVFAudio

func configureAudioSession(forPlayback: Bool = true) throws {
    let session = AVAudioSession.sharedInstance()

    if forPlayback {
        // Media playback: audio continues with silent switch, supports background
        try session.setCategory(
            .playback,
            mode: .default,
            options: []
        )
    } else {
        // Mix with other apps (e.g., game sounds over user's music)
        try session.setCategory(
            .ambient,
            mode: .default,
            options: [.mixWithOthers]
        )
    }

    try session.setActive(true)
}

// For video calls
try AVAudioSession.sharedInstance().setCategory(
    .playAndRecord,
    mode: .videoChat,
    options: [.defaultToSpeaker, .allowBluetooth]
)
```

### Handling Audio Interruptions

```swift
NotificationCenter.default.addObserver(
    forName: AVAudioSession.interruptionNotification,
    object: AVAudioSession.sharedInstance(),
    queue: .main
) { notification in
    guard let info = notification.userInfo,
          let typeValue = info[AVAudioSessionInterruptionTypeKey] as? UInt,
          let type = AVAudioSession.InterruptionType(rawValue: typeValue) else {
        return
    }

    switch type {
    case .began:
        // Pause playback -- system has interrupted audio
        player.pause()
    case .ended:
        let options = info[AVAudioSessionInterruptionOptionKey] as? UInt ?? 0
        if AVAudioSession.InterruptionOptions(rawValue: options).contains(.shouldResume) {
            player.play()
        }
    @unknown default:
        break
    }
}
```

### Handling Route Changes

```swift
NotificationCenter.default.addObserver(
    forName: AVAudioSession.routeChangeNotification,
    object: AVAudioSession.sharedInstance(),
    queue: .main
) { notification in
    guard let info = notification.userInfo,
          let reasonValue = info[AVAudioSessionRouteChangeReasonKey] as? UInt,
          let reason = AVAudioSession.RouteChangeReason(rawValue: reasonValue) else {
        return
    }

    if reason == .oldDeviceUnavailable {
        // Headphones unplugged -- pause playback (Apple HIG requirement)
        player.pause()
    }
}
```

## Background Audio Setup

To play audio when the app is in the background, two things are required:

1. Enable the `audio` background mode in your app's capabilities.
2. Configure `AVAudioSession` with the `.playback` category.

### Info.plist Configuration

```xml
<key>UIBackgroundModes</key>
<array>
    <string>audio</string>
</array>
```

Or enable "Audio, AirPlay, and Picture in Picture" in Xcode's Signing &
Capabilities tab.

### Activating Background Audio

```swift
import AVFAudio

func enableBackgroundAudio() throws {
    let session = AVAudioSession.sharedInstance()
    try session.setCategory(.playback, mode: .default)
    try session.setActive(true)
}
```

**Rules:**
- Call `setCategory` before `setActive`.
- The `.playback` category is required; `.ambient` and `.soloAmbient` do not
  support background audio.
- Deactivate the session when playback ends to let other apps use audio:

```swift
func deactivateAudioSession() {
    try? AVAudioSession.sharedInstance().setActive(
        false,
        options: .notifyOthersOnDeactivation
    )
}
```

## Now Playing Info Center

Update `MPNowPlayingInfoCenter` so the system displays track information on
the lock screen, Control Center, and connected accessories (CarPlay, AirPods).

Docs: [MPNowPlayingInfoCenter](https://sosumi.ai/documentation/mediaplayer/mpnowplayinginfocenter)

```swift
import MediaPlayer

func updateNowPlayingInfo(
    title: String,
    artist: String,
    albumTitle: String? = nil,
    duration: TimeInterval,
    currentTime: TimeInterval,
    artwork: UIImage? = nil
) {
    var info: [String: Any] = [
        MPMediaItemPropertyTitle: title,
        MPMediaItemPropertyArtist: artist,
        MPMediaItemPropertyPlaybackDuration: duration,
        MPNowPlayingInfoPropertyElapsedPlaybackTime: currentTime,
        MPNowPlayingInfoPropertyPlaybackRate: 1.0,
        MPNowPlayingInfoPropertyMediaType: MPNowPlayingInfoMediaType.audio.rawValue
    ]

    if let albumTitle {
        info[MPMediaItemPropertyAlbumTitle] = albumTitle
    }

    if let artwork {
        info[MPMediaItemPropertyArtwork] = MPMediaItemArtwork(
            boundsSize: artwork.size
        ) { _ in artwork }
    }

    MPNowPlayingInfoCenter.default().nowPlayingInfo = info
}

// Update elapsed time during playback
func updateElapsedTime(_ seconds: TimeInterval, rate: Float = 1.0) {
    var info = MPNowPlayingInfoCenter.default().nowPlayingInfo ?? [:]
    info[MPNowPlayingInfoPropertyElapsedPlaybackTime] = seconds
    info[MPNowPlayingInfoPropertyPlaybackRate] = rate
    MPNowPlayingInfoCenter.default().nowPlayingInfo = info
}
```

## MPRemoteCommandCenter

Register handlers for lock screen, Control Center, and accessory controls
(play, pause, skip, seek). Without these, the system controls won't work.

Docs: [MPRemoteCommandCenter](https://sosumi.ai/documentation/mediaplayer/mpremotecommandcenter)

```swift
import MediaPlayer

func setupRemoteCommands(player: AVPlayer) {
    let commandCenter = MPRemoteCommandCenter.shared()

    // Play
    commandCenter.playCommand.isEnabled = true
    commandCenter.playCommand.addTarget { _ in
        player.play()
        return .success
    }

    // Pause
    commandCenter.pauseCommand.isEnabled = true
    commandCenter.pauseCommand.addTarget { _ in
        player.pause()
        return .success
    }

    // Toggle play/pause (headphone button, etc.)
    commandCenter.togglePlayPauseCommand.isEnabled = true
    commandCenter.togglePlayPauseCommand.addTarget { _ in
        if player.timeControlStatus == .playing {
            player.pause()
        } else {
            player.play()
        }
        return .success
    }

    // Skip forward (e.g., 15 seconds)
    commandCenter.skipForwardCommand.isEnabled = true
    commandCenter.skipForwardCommand.preferredIntervals = [15]
    commandCenter.skipForwardCommand.addTarget { event in
        guard let skipEvent = event as? MPSkipIntervalCommandEvent else {
            return .commandFailed
        }
        let currentTime = player.currentTime().seconds
        let target = CMTime(
            seconds: currentTime + skipEvent.interval,
            preferredTimescale: 600
        )
        player.seek(to: target)
        return .success
    }

    // Skip backward (e.g., 15 seconds)
    commandCenter.skipBackwardCommand.isEnabled = true
    commandCenter.skipBackwardCommand.preferredIntervals = [15]
    commandCenter.skipBackwardCommand.addTarget { event in
        guard let skipEvent = event as? MPSkipIntervalCommandEvent else {
            return .commandFailed
        }
        let currentTime = player.currentTime().seconds
        let target = CMTime(
            seconds: max(0, currentTime - skipEvent.interval),
            preferredTimescale: 600
        )
        player.seek(to: target)
        return .success
    }

    // Scrubbing (seek bar on lock screen)
    commandCenter.changePlaybackPositionCommand.isEnabled = true
    commandCenter.changePlaybackPositionCommand.addTarget { event in
        guard let positionEvent = event as? MPChangePlaybackPositionCommandEvent else {
            return .commandFailed
        }
        let target = CMTime(
            seconds: positionEvent.positionTime,
            preferredTimescale: 600
        )
        player.seek(to: target)
        return .success
    }

    // Disable unsupported commands to remove them from UI
    commandCenter.nextTrackCommand.isEnabled = false
    commandCenter.previousTrackCommand.isEnabled = false
}
```

### Cleanup

```swift
func teardownRemoteCommands() {
    let commandCenter = MPRemoteCommandCenter.shared()
    commandCenter.playCommand.removeTarget(nil)
    commandCenter.pauseCommand.removeTarget(nil)
    commandCenter.togglePlayPauseCommand.removeTarget(nil)
    commandCenter.skipForwardCommand.removeTarget(nil)
    commandCenter.skipBackwardCommand.removeTarget(nil)
    commandCenter.changePlaybackPositionCommand.removeTarget(nil)
}
```

## Picture-in-Picture

`AVPictureInPictureController` enables floating video playback that continues
when the user navigates away. Requires the `audio` background mode.

Docs: [AVPictureInPictureController](https://sosumi.ai/documentation/avkit/avpictureinpicturecontroller),
[Adopting Picture in Picture in a Custom Player](https://sosumi.ai/documentation/avkit/adopting-picture-in-picture-in-a-custom-player)

### With AVPlayerViewController (Automatic)

`AVPlayerViewController` supports PiP automatically when the background audio
capability is enabled. No extra code needed.

```swift
let controller = AVPlayerViewController()
controller.player = player
controller.allowsPictureInPicturePlayback = true  // true by default
```

### With a Custom Player

```swift
import AVKit

@Observable
@MainActor
final class PiPManager: NSObject, AVPictureInPictureControllerDelegate {
    private var pipController: AVPictureInPictureController?
    var isPiPActive = false
    var isPiPPossible = false

    func setup(playerLayer: AVPlayerLayer) {
        guard AVPictureInPictureController.isPictureInPictureSupported() else {
            return
        }

        pipController = AVPictureInPictureController(playerLayer: playerLayer)
        pipController?.delegate = self

        // Auto-start PiP when app goes to background
        pipController?.canStartPictureInPictureAutomaticallyFromInline = true
    }

    func togglePiP() {
        guard let pipController else { return }
        if pipController.isPictureInPictureActive {
            pipController.stopPictureInPicture()
        } else {
            pipController.startPictureInPicture()
        }
    }

    // MARK: - AVPictureInPictureControllerDelegate

    nonisolated func pictureInPictureControllerWillStartPictureInPicture(
        _ controller: AVPictureInPictureController
    ) {
        Task { @MainActor in isPiPActive = true }
    }

    nonisolated func pictureInPictureControllerDidStopPictureInPicture(
        _ controller: AVPictureInPictureController
    ) {
        Task { @MainActor in isPiPActive = false }
    }

    nonisolated func pictureInPictureController(
        _ controller: AVPictureInPictureController,
        restoreUserInterfaceForPictureInPictureStopWithCompletionHandler
        completionHandler: @escaping (Bool) -> Void
    ) {
        // Restore your player UI here, then call the handler
        Task { @MainActor in
            // Navigate back to the player view
            completionHandler(true)
        }
    }
}
```

### PiP Requirements Checklist

- [ ] `UIBackgroundModes` includes `audio` in Info.plist
- [ ] `AVAudioSession` category set to `.playback`
- [ ] Check `AVPictureInPictureController.isPictureInPictureSupported()` before setup
- [ ] Implement `restoreUserInterfaceForPictureInPictureStop` delegate method
- [ ] Call completion handler in the restore delegate method (failure to call causes hangs)
