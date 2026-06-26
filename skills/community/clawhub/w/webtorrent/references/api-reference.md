# WebTorrent Complete API Reference

## WebTorrent Constructor

```js
new WebTorrent([opts])
```

### Global Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `maxConns` | number | 55 | Maximum connections per torrent |
| `dht` | boolean/object | `true` | Whether to enable DHT |
| `dht.bootstrap` | string[] | — | DHT bootstrap nodes |
| `tracker` | boolean/object | `true` | Whether to enable tracker |
| `tracker.rtcConfig` | RTCConfiguration | — | WebRTC configuration (ICE servers, etc.) |
| `tracker.wrtc` | object | — | Node.js WebRTC implementation |
| `webSeeds` | boolean | `true` | Whether to enable web seeds |
| `lsd` | boolean | `true` | Whether to enable local service discovery (Node only) |
| `utp` | boolean | `true` | Whether to enable μTP (Node only) |
| `downloadLimit` | number | `-1` | Global download rate limit (bytes/s), -1 = unlimited |
| `uploadLimit` | number | `-1` | Global upload rate limit (bytes/s), -1 = unlimited |

### Events

| Event | Parameters | Description |
|-------|------------|-------------|
| `torrent` | torrent | A new torrent has been added |
| `error` | err | Error |

## client.add(torrentId[, opts][, onTorrent])

### torrentId Supported Formats

| Format | Example |
|--------|---------|
| magnet URI | `magnet:?xt=urn:btih:...` |
| info hash (hex) | `a1b2c3d4...` |
| info hash (Buffer) | `Buffer.from('a1b2c3...', 'hex')` |
| torrent file Buffer | Parsed `.torrent` file content |
| torrent file URL | `https://example.com/file.torrent` |
| Blob URL (browser) | `blob:https://...` |

### Add Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `path` | string | `os.tmpdir()` | File storage path |
| `store` | function | `'auto'` | Storage backend: `MemoryChunkStore` or custom |
| `destroyStoreOnDestroy` | boolean | `false` | Delete files when removing the torrent |
| `private` | boolean | `false` | Use private trackers only |
| `announce` | string[] | `[]` | Additional tracker URL list |
| `deselect` | boolean | `false` | Do not download any files by default (requires manual select) |
| `strategy` | string | `'sequential'` | Download strategy: `'sequential'` or `'rarest'` |
| `skipVerification` | boolean | `false` | Skip hash verification of existing data |
| `storeCacheSlots` | number | `20` | Number of blocks cached simultaneously |

## Torrent Object

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `infoHash` | string | Torrent info hash (hex) |
| `magnetURI` | string | Magnet link |
| `name` | string | Torrent name (after metadata is ready) |
| `files` | File[] | File list (after metadata is ready) |
| `pieces` | Piece[] | Piece list (after metadata is ready) |
| `progress` | number 0-1 | Overall download progress |
| `downloaded` | number | Bytes downloaded |
| `uploaded` | number | Bytes uploaded |
| `downloadSpeed` | number | Download speed (bytes/s) |
| `uploadSpeed` | number | Upload speed (bytes/s) |
| `numPeers` | number | Number of connected peers |
| `path` | string | File storage path |
| `ready` | boolean | Whether metadata is ready |
| `paused` | boolean | Whether paused |
| `done` | boolean | Whether download is complete |
| `length` | number | Total torrent size (after metadata is ready) |
| `created` | Date | Torrent creation time |
| `createdBy` | string | Creator |
| `comment` | string | Torrent comment |
| `timeRemaining` | number | Estimated time remaining (ms) |
| `received` | number | Total bytes received |
| `ratio` | number | Share ratio (uploaded/downloaded) |

### Events

| Event | Parameters | Description |
|-------|------------|-------------|
| `infoHash` | infoHash | infoHash obtained |
| `metadata` | — | Metadata loading complete |
| `ready` | — | Torrent ready (same as metadata) |
| `download` | bytes | Data chunk received |
| `upload` | bytes | Data chunk sent |
| `done` | — | Download complete |
| `error` | err | Error |
| `warning` | err | Non-fatal warning |
| `wire` | wire, addr | New peer connected |
| `noPeers` | — | No connectable peers (announce interval) |

### Methods

| Method | Description |
|--------|-------------|
| `torrent.pause()` | Pause download/upload |
| `torrent.resume()` | Resume download/upload |
| `torrent.destroy([cb])` | Remove torrent and clean up resources |
| `torrent.addPeer(peer)` | Manually add a peer |
| `torrent.removePeer(peer)` | Manually remove a peer |
| `torrent.select(start, end[, priority][, notify])` | Select a specific piece range to download |
| `torrent.deselect(start, end[, priority])` | Deselect a piece range |
| `torrent.critical(start, end)` | Mark piece range as critical (prioritized download) |
| `torrent.createServer([opts])` | Create an HTTP server to stream content (Node only) |

## File Object

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Filename |
| `path` | string | File path within the torrent |
| `length` | number | File size (bytes) |
| `downloaded` | number | Bytes downloaded |
| `progress` | number 0-1 | File download progress |
| `offset` | number | File start offset within the torrent |

### Methods

| Method | Description |
|--------|-------------|
| `file.getBuffer(cb)` | Get the complete file Buffer |
| `file.getBlob(cb)` | Get the file Blob (browser only) |
| `file.getBlobURL(cb)` | Get the Blob URL (browser only) |
| `file.appendTo(rootElem[, opts][, cb])` | Append and render to a DOM element |
| `file.renderTo(rootElem[, opts][, cb])` | Replace and render to a DOM element |
| `file.createReadStream([opts])` | Create a readable stream |
| `file.select()` | Select this file for download |
| `file.deselect()` | Deselect this file |

## client.seed(input[, opts][, onTorrent])

### input Supported Formats

| Format | Environment |
|--------|-------------|
| File path string | Node.js |
| File object | Browser |
| FileList | Browser |
| Buffer | Node.js / Browser |
| ReadableStream | Node.js / Browser |
| Blob | Browser |

### seed Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `name` | string | Auto | Torrent name |
| `comment` | string | — | Torrent comment |
| `createdBy` | string | — | Creator |
| `created` | Date | now | Creation time |
| `private` | boolean | `false` | Whether the torrent is private |
| `pieceLength` | number | Auto | Piece size |
| `announceList` | string[][] | — | Tracker list |
| `skipVerify` | boolean | `false` | Skip hash verification |
| `store` | function | `'auto'` | Storage backend |
| `destroyStoreOnDestroy` | boolean | `false` | Delete files on destroy |

### Additional Torrent Events Returned by client.seed

| Event | Description |
|-------|-------------|
| `torrent.on('upload', bytes)` | Data uploaded (while seeding) |

## Other client Methods

| Method | Description |
|--------|-------------|
| `client.destroy([cb])` | Destroy all torrents and release resources |
| `client.torrents` | Array of all active torrents |
| `client.get(torrentId)` | Find a torrent by infoHash |
| `client.remove(torrentId[, cb])` | Remove a specific torrent |
| `client.ratio` | Overall share ratio |

## Environment Differences

| Feature | Node.js | Browser |
|---------|---------|---------|
| TCP/UDP | ✅ | ❌ |
| WebRTC | ❌ (requires webtorrent-hybrid) | ✅ |
| DHT | ✅ (UDP) | ✅ (WebRTC) |
| LSD | ✅ | ❌ |
| μTP | ✅ | ❌ |
| File system storage | ✅ (disk) | ❌ (memory/IndexedDB) |
| `createServer()` | ✅ | ❌ |

## Related Modules

| Module | Purpose |
|--------|---------|
| `webtorrent-hybrid` | Node + WebRTC + TCP/UDP |
| `webtorrent-cli` | Command-line tool |
| `webtorrent-desktop` | Desktop application |
| `memory-chunk-store` | In-memory storage backend |
| `idb-chunk-store` | IndexedDB storage (browser persistence) |
| `fs-chunk-store` | File system storage (Node default) |
| `drag-drop` | Browser drag-and-drop files (used with seed) |