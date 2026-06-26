---
name: webtorrent
description: Use WebTorrent to implement streaming BitTorrent client functionality in Node.js and the browser. Supports torrent downloading, seeding, magnet links, streaming media playback, and peer-to-peer transfer (via WebRTC Data Channel in the browser, and TCP/UDP in Node.js).
---

# WebTorrent — Streaming Torrent Client

A BitTorrent client that runs in both Node.js and the browser, implemented in pure JavaScript with zero native dependencies.

## Use Cases

Use when users need to download torrent/magnet links, seed and share files, implement browser-side P2P transfer, build streaming torrent media players, or use webtorrent-related features.

## Trigger Words

webtorrent, torrent download, magnet link, torrent, seeding, P2P transfer, browser torrent, WebRTC file sharing, streaming download.

## Installation

```bash
npm install webtorrent
```

CLI tool:
```bash
npm install webtorrent-cli -g
```

## Quick Start

### Node.js

```js
import WebTorrent from 'webtorrent'

const client = new WebTorrent()

// Download via magnet link
client.add(magnetURI, (torrent) => {
  console.log('Downloading:', torrent.infoHash)

  torrent.files.forEach(file => {
    console.log(`File: ${file.name} (${file.length} bytes)`)
  })
})

// Seed — share local files
client.seed('/path/to/file.mp4', (torrent) => {
  console.log('Seeding:', torrent.magnetURI)
})
```

### Browser — ESM import

```js
import WebTorrent from 'webtorrent'

const client = new WebTorrent()

client.add(magnetURI, (torrent) => {
  torrent.files.forEach(file => {
    file.getBuffer((err, buf) => {
      if (err) throw err
      console.log(`Download complete: ${file.name}, ${buf.length} bytes`)
    })
  })
})
```

### Browser — script tag

```html
<script type="module">
  import WebTorrent from 'https://esm.sh/webtorrent'
  // Or local: import WebTorrent from 'webtorrent.min.js'

  const client = new WebTorrent()
  // ... same as above
</script>
```

## Core API

### `client.add(torrentId, [opts], [callback])`

Add a torrent to start downloading.

- `torrentId` — magnet URI / info hash / torrent file Buffer / remote `.torrent` URL
- `opts` — Optional configuration (see below)
- Returns a `Torrent` object

```js
client.add(magnetURI, { path: './downloads' }, (torrent) => {
  console.log('Metadata obtained')
})
```

### `client.seed(input, [opts], [callback])`

Seed and share files.

- `input` — File path / File object / FileList / Buffer / ReadableStream
- In the browser, can be used with drag-drop libraries

```js
// Drag-and-drop file seeding in the browser
import dragDrop from 'drag-drop'

dragDrop('body', (files) => {
  client.seed(files, (torrent) => {
    console.log('Seeding:', torrent.magnetURI)
  })
})
```

### `client.destroy([callback])`

Destroy the client and release all resources.

### `client.on('error', callback)`

Global error handling.

## Torrent Object

```js
client.add(magnetURI, (torrent) => {
  // Properties
  torrent.infoHash    // string — torrent hash
  torrent.magnetURI   // string — magnet link
  torrent.name        // string — torrent name
  torrent.files       // File[] — file list
  torrent.progress    // number 0-1
  torrent.downloaded  // number — bytes downloaded
  torrent.uploaded    // number — bytes uploaded
  torrent.downloadSpeed // bytes/s
  torrent.uploadSpeed   // bytes/s
  torrent.numPeers    // number — connected peers
  torrent.path        // string — download directory
  torrent.ready       // boolean — metadata ready

  // Events
  torrent.on('ready', () => {})      // Metadata ready
  torrent.on('download', (bytes) => {})  // Data chunk received
  torrent.on('upload', (bytes) => {})    // Data chunk sent
  torrent.on('done', () => {})       // Download complete
  torrent.on('error', (err) => {})   // Error
  torrent.on('warning', (err) => {}) // Warning
  torrent.on('wire', (wire) => {})   // New peer connected
  torrent.on('noPeers', () => {})    // No peers available

  // Methods
  torrent.pause()    // Pause
  torrent.resume()   // Resume
  torrent.destroy()  // Remove torrent
})
```

## File Object (element of torrent.files)

```js
const file = torrent.files[0]

// Properties
file.name       // Filename
file.length     // File size (bytes)
file.downloaded // Bytes downloaded
file.progress   // Download progress 0-1

// Methods
file.getBuffer((err, buffer) => {})  // Get complete Buffer
file.getBlob((err, blob) => {})      // Get Blob (browser)

// Streaming read — create a readable stream
const stream = file.createReadStream()
stream.pipe(someWritableStream)

// Render to page
file.appendTo('#container')          // Append to DOM element
file.renderTo('#container')          // Replace DOM element content

// Streaming video playback
file.renderTo('video#player')        // Render to <video> tag
file.renderTo('img#preview')         // Render to <img> tag
file.renderTo('audio#player')        // Render to <audio> tag
```

## Browser WebRTC Considerations

- **Browsers only support WebRTC** (no TCP/UDP direct connection)
- **Can only connect to peers that support WebTorrent** (WebTorrent Desktop, webtorrent-hybrid, Instant.io, Vuze)
- **Domains within the same SWARM can communicate** — WebTorrent is a web-wide P2P network
- Supported browsers: Chrome, Firefox, Opera, Safari
- Supported video formats: webm, mkv, mp4, ogv, mov (AV1, H264, HEVC, VP8, VP9)

## Connecting Node.js to Browser Peers

Native Node.js webtorrent only uses TCP/UDP and **cannot directly connect to browser WebRTC peers**. For bidirectional communication, use:

```bash
npm install webtorrent-hybrid
```

```js
import WebTorrent from 'webtorrent-hybrid'
// API is identical, but additionally supports WebRTC
```

## Common Options

```js
const client = new WebTorrent({
  maxConns: 55,           // Maximum number of connections
  dht: true,              // Enable DHT
  tracker: true,          // Enable tracker
  webSeeds: true,         // Enable web seeds
  lsd: true,              // Enable local service discovery
  utp: true,              // Enable μTP (Node only)
  downloadLimit: -1,      // Download rate limit (bytes/s), -1 = unlimited
  uploadLimit: -1         // Upload rate limit (bytes/s), -1 = unlimited
})

client.add(magnetURI, {
  path: './downloads',      // Download directory
  store: 'auto',            // Storage strategy: 'auto' | MemoryStorage | custom
  destroyStoreOnDestroy: false,  // Delete files on destroy
  private: false,           // Use private trackers only
  announce: ['wss://...'],  // Custom tracker list
  deselect: false,          // true = do not auto-select files to download
  strategy: 'sequential'    // 'sequential' | 'rarest'
})
```

## CLI Usage

```bash
# Download a magnet link
webtorrent magnet_uri

# Stream to various devices
webtorrent magnet_uri --airplay    # Apple TV
webtorrent magnet_uri --chromecast # Chromecast
webtorrent magnet_uri --vlc        # VLC
webtorrent magnet_uri --mpv        # MPV
webtorrent magnet_uri --mplayer    # MPlayer
webtorrent magnet_uri --xbmc       # XBMC
webtorrent magnet_uri --stdout     # Standard output
```

## Common Patterns

### Pattern 1: Download and Play Video (Browser)

```js
client.add(magnetURI, (torrent) => {
  const file = torrent.files.find(f => f.name.endsWith('.mp4'))
  if (file) file.renderTo('video#player')
})
```

### Pattern 2: Download Progress Display

```js
client.add(magnetURI, (torrent) => {
  torrent.on('download', () => {
    const pct = (torrent.progress * 100).toFixed(1)
    console.log(`Progress: ${pct}% | Speed: ${formatSpeed(torrent.downloadSpeed)}`)
  })

  torrent.on('done', () => {
    console.log('Download complete!')
  })
})

function formatSpeed(bps) {
  const units = ['B/s', 'KB/s', 'MB/s']
  let i = 0
  while (bps >= 1024 && i < units.length - 1) { bps /= 1024; i++ }
  return `${bps.toFixed(1)} ${units[i]}`
}
```

### Pattern 3: Select Specific Files to Download

```js
client.add(magnetURI, { deselect: true }, (torrent) => {
  // After metadata is ready, only select needed files
  torrent.on('ready', () => {
    torrent.files.forEach(file => {
      if (file.name.endsWith('.mp4')) file.select()
      else file.deselect()
    })
  })
})
```

### Pattern 4: In-Memory Temporary Storage

```js
import MemoryChunkStore from 'memory-chunk-store'

client.add(magnetURI, { store: MemoryChunkStore }, (torrent) => {
  // Data stored in memory, not written to disk
  torrent.on('done', () => {
    torrent.files[0].getBuffer((err, buf) => {
      console.log(`Completed in memory: ${buf.length} bytes`)
    })
  })
})
```

## Peer Discovery Mechanisms

| Mechanism | Description | Node | Browser |
|-----------|-------------|------|---------|
| DHT | Distributed Hash Table | ✅ | ✅ (WebRTC) |
| Tracker | Centralized tracking server | ✅ | ✅ (WebSocket) |
| LSD | Local Service Discovery | ✅ | ❌ |
| ut_pex | Peer Exchange Extension | ✅ | ✅ |

## FAQ

- **Cannot connect to regular torrents in the browser** — Browsers only connect via WebRTC; peers must also support WebTorrent
- **Slow download speed** — Check the number of peers, whether DHT/tracker is enabled, and whether there are enough seeders
- **Metadata loading slowly** — magnet URIs need to obtain metadata via ut_metadata first, which takes time
- **Large file memory overflow** — Pay attention to memory limits in the browser; large files are recommended to use IndexedDB storage or streaming processing

For the detailed API reference, see [references/api-reference.md](references/api-reference.md).