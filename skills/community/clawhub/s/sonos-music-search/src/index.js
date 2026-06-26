const fetch = require('node-fetch');
const Sonos = require('sonos');

const BRAVE_SEARCH_BASE = 'https://api.search.brave.com/res/v1/web/search';
const DISCOVERY_TIMEOUT_MS = 5000;
const DEFAULT_SAFESEARCH = 'moderate';
const SITE_FILTER = 'site:open.spotify.com/track';

if (!process.env.BRAVE_API_KEY) {
  throw new Error('BRAVE_API_KEY environment variable is required');
}

const braveApiKey = process.env.BRAVE_API_KEY;

function extractSpotifyUri(url) {
  try {
    const parsed = new URL(url);
    const trackId = parsed.pathname.split('/track/')[1];
    if (!trackId) return null;
    return `spotify:track:${trackId}`;
  } catch {
    return null;
  }
}

async function discoverDevices(timeoutMs = DISCOVERY_TIMEOUT_MS) {
  return Promise.race([
    Sonos.DeviceDiscovery(),
    new Promise((_, reject) =>
      setTimeout(
        () => reject(new Error(`Sonos device discovery timed out after ${timeoutMs}ms`)),
        timeoutMs
      )
    ),
  ]);
}

async function searchAndPlay(speakerName, query, { safesearch = DEFAULT_SAFESEARCH } = {}) {
  // Search for music using Brave Search API
  const searchUrl = `${BRAVE_SEARCH_BASE}?q=${encodeURIComponent(`${query} ${SITE_FILTER}`)}&count=5&safesearch=${safesearch}`;
  const response = await fetch(searchUrl, {
    headers: { 'X-Subscription-Token': braveApiKey, Accept: 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`Brave Search API error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  const results = data.web?.results || [];

  if (results.length === 0) {
    throw new Error(`No results found for query: ${query}`);
  }

  // Extract Spotify URI from first result
  const firstResult = results[0];
  const spotifyUri = extractSpotifyUri(firstResult.url);

  if (!spotifyUri) {
    throw new Error(`Could not extract Spotify track URI from: ${firstResult.url}`);
  }

  // Find Sonos speaker
  const devices = await discoverDevices();
  const speaker = devices.find((d) => d.name === speakerName);

  if (!speaker) {
    const names = devices.map((d) => d.name).join(', ');
    throw new Error(`Speaker not found: "${speakerName}". Available: ${names || 'none'}`);
  }

  // Play the track
  await speaker.play(spotifyUri);

  return {
    success: true,
    track: firstResult.title,
    speaker: speakerName,
    uri: spotifyUri,
  };
}

async function getCurrentTrack(speakerName) {
  const devices = await discoverDevices();
  const speaker = devices.find((d) => d.name === speakerName);

  if (!speaker) {
    const names = devices.map((d) => d.name).join(', ');
    throw new Error(`Speaker not found: "${speakerName}". Available: ${names || 'none'}`);
  }

  const currentTrack = await speaker.currentTrack();
  return currentTrack;
}

// CLI usage
if (require.main === module) {
  const [, , command, speakerName, ...queryParts] = process.argv;
  const query = queryParts.join(' ');

  (async () => {
    try {
      if (command === 'play') {
        const result = await searchAndPlay(speakerName, query);
        console.log(`Playing "${result.track}" on ${result.speaker}`);
      } else if (command === 'current') {
        const track = await getCurrentTrack(speakerName);
        console.log(`Currently playing: ${track.title} by ${track.artist}`);
      } else {
        console.log('Usage: node index.js play <speaker-name> <search-query>');
        console.log('       node index.js current <speaker-name>');
        process.exit(1);
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  })();
}

module.exports = { searchAndPlay, getCurrentTrack, extractSpotifyUri, discoverDevices };
