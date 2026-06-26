---
name: sonos-music-search-skill
description: Search for music via Brave Search and play it on your Sonos speakers.
homepage: https://clawhub.com/skills/sonos-music-search-skill
metadata: { 'aren': { 'emoji': '🎵', 'requires': { 'env': ['BRAVE_API_KEY'], 'bins': ['node'], 'network': true } } }
---

# Sonos Music Search Skill

Search for music on Spotify via Brave Search and play it on your Sonos speakers — right from the command line.

## Features

- 🔍 Uses Brave Search API to find Spotify tracks
- 🔊 Plays found tracks on your specified Sonos speaker
- 🎶 View currently playing track
- ⏱️ Discovery timeout protection (won't hang on missing speakers)
- 🛡️ Safe search defaults to moderate

## Prerequisites

- **Node.js** >= 18
- **Brave Search API key** — [Get one here](https://brave.com/search/api/)
- **Sonos speaker** on the same local network
- **Spotify account linked** to your Sonos system

## Installation

```bash
npm install
```

## Configuration

Set your Brave Search API key:

```bash
export BRAVE_API_KEY=your-api-key
```

## Usage

### Play a track

```bash
node src/index.js play "Living Room" "pink floyd comfortably numb"
```

### View currently playing track

```bash
node src/index.js current "Living Room"
```

## Scripts

| Command                | Description                      |
| ---------------------- | -------------------------------- |
| `npm start`            | Run the CLI                      |
| `npm run audit`        | Run skill audit                  |
| `npm run format`       | Format JS and Markdown files     |
| `npm run format:check` | Check formatting without writing |

## License

MIT
