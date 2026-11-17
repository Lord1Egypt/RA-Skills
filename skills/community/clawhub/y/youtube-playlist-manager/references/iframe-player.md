# YouTube IFrame Player API

Play a video, or a whole playlist built with this skill, inside your own web page or app. Playback doesn't use Data API quota.

## Key Facts

- The embedded player is the ToS-compliant way to play YouTube in your own UI. You can't pull the stream into AVPlayer or another native player.
- YouTube branding and the "Watch on YouTube" link stay. `modestbranding` (deprecated 2023) and `showinfo` (2018) no longer do anything, and `rel: 0` only limits suggestions to the same channel.
- Embeds must identify the site or app through the HTTP `Referer` header (YouTube's Required Minimum Functionality). In a web view, load your HTML with a `baseURL` whose host is your app ID, such as `https://com.example.yourapp`.
- iOS, iPadOS and macOS: use `WKWebView`. **tvOS has no WebKit**, so the IFrame player can't run in a tvOS app.

## Minimal HTML Player

```html
<div id="player"></div>
<script src="https://www.youtube.com/iframe_api"></script>
<script>
var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        height: '100%', width: '100%',
        playerVars: {
            listType: 'playlist', list: 'PLAYLIST_ID',  // or drop both and set videoId: 'VIDEO_ID'
            playsinline: 1,                             // iOS: play inline, not fullscreen
            autoplay: 1, fs: 0
        },
        events: {
            onReady: (e) => e.target.playVideo(),
            onStateChange: (e) => {
                window.webkit.messageHandlers.state.postMessage(e.data);
            }
        }
    });
}
</script>
```

## Player State Events

| Event | Value | Description |
|-------|-------|-------------|
| UNSTARTED | -1 | Video cued but not started |
| ENDED | 0 | Video finished |
| PLAYING | 1 | Currently playing |
| PAUSED | 2 | User paused |
| BUFFERING | 3 | Buffering |
| CUED | 5 | Video cued |

## Controlling Playback

`player.playVideo()`, `pauseVideo()`, `nextVideo()`, `previousVideo()`, `playVideoAt(index)`, `loadVideoById(id)`, `loadPlaylist({list: 'PLAYLIST_ID', listType: 'playlist', index: 0})`, `getCurrentTime()`, `getDuration()`, `getPlaylistIndex()`.

## Bridging to Swift (WKWebView)

```swift
let config = WKWebViewConfiguration()
config.allowsInlineMediaPlayback = true                // iOS only: needed for playsinline
config.mediaTypesRequiringUserActionForPlayback = []   // allow autoplay
config.userContentController.add(handler, name: "state")
config.userContentController.add(handler, name: "progress")

let webView = WKWebView(frame: .zero, configuration: config)
webView.loadHTMLString(html, baseURL: URL(string: "https://com.example.yourapp"))  // sets the Referer
```

Send events from the page with `window.webkit.messageHandlers.<name>.postMessage(...)` (handled by a `WKScriptMessageHandler`), and drive the player from Swift with `webView.evaluateJavaScript("player.nextVideo()")`.

Poll watch progress:

```javascript
setInterval(() => {
    const t = player.getCurrentTime();
    const d = player.getDuration();
    window.webkit.messageHandlers.progress.postMessage({
        time: t, duration: d, percent: d ? Math.round((t / d) * 100) : 0
    });
}, 1000);
```
