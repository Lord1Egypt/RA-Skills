# Sonos Music Search Skill

Search for music via Brave Search and play it on your Sonos speakers directly from the command line.

## Features

- Search for Spotify tracks using Brave Search
- Play found tracks on a specified Sonos speaker
- View the currently playing track
- List available Sonos speakers on the network
- Safe search enabled by default (opt into unrestricted with `--unsafe`)

## Prerequisites

- Node.js >= 18
- A Brave Search API key ([get one here](https://brave.com/search/api/))
- At least one Sonos speaker on the same network

## Installation

```bash
npm install
```

## Configuration

Set your Brave Search API key as an environment variable:

```bash
export BRAVE_API_KEY=your-api-key
```

## Usage

### Play a track

```bash
node src/index.js play "Living Room" "pink floyd comfortably numb"
```

Add `--unsafe` to disable safe search:

```bash
node src/index.js play "Living Room" "explicit track name" --unsafe
```

### View currently playing track

```bash
node src/index.js current "Living Room"
```

### List available speakers

```bash
node src/index.js list
```

## Programmatic API

```js
const { searchAndPlay, getCurrentTrack, listSpeakers } = require('sonos-music-search-skill');

// Play a track
const result = await searchAndPlay('Living Room', 'pink floyd comfortably numb');
// { success: true, track: '...', speaker: 'Living Room', uri: 'spotify:track:...' }

// Get current track
const track = await getCurrentTrack('Living Room');
// { title: '...', artist: '...', ... }

// List speakers
const speakers = await listSpeakers();
// [{ name: 'Living Room', host: '192.168.1.50' }, ...]
```

## Scripts

| Command                | Description                      |
| ---------------------- | -------------------------------- |
| `npm start`            | Run the CLI                      |
| `npm run audit`        | Run the skill audit              |
| `npm run format`       | Format JS and Markdown files     |
| `npm run format:check` | Check formatting without writing |

## License

MIT
