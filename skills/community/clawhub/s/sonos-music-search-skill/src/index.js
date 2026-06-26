const { BraveSearch } = require('brave-search');
const Sonos = require('sonos');

if (!process.env.BRAVE_API_KEY) {
  throw new Error('BRAVE_API_KEY environment variable is required');
}

const braveSearch = new BraveSearch(process.env.BRAVE_API_KEY);

const SPEAKER_NAME_RE = /^[a-zA-Z0-9 _-]+$/;

function extractSpotifyUri(url) {
  const match = url.match(/open\.spotify\.com\/track\/([a-zA-Z0-9]+)/);
  if (!match) return null;
  return 'spotify:track:' + match[1];
}

async function discoverSpeakers(timeoutMs = 5000) {
  return Sonos.DeviceDiscovery({ timeout: timeoutMs });
}

async function searchAndPlay(speakerName, query, options = {}) {
  if (!speakerName || !SPEAKER_NAME_RE.test(speakerName)) {
    throw new Error(
      'Invalid speaker name. Use only letters, numbers, spaces, hyphens, or underscores.'
    );
  }

  if (!query || typeof query !== 'string' || query.trim().length === 0) {
    throw new Error('Search query must be a non-empty string.');
  }

  const safesearch = options.unsafe ? 'off' : 'moderate';

  let searchResults;
  try {
    searchResults = await braveSearch.web(`${query.trim()} site:spotify.com/track`, {
      count: 5,
      safesearch,
    });
  } catch (err) {
    if (err.status === 401) throw new Error('Invalid Brave API key. Check BRAVE_API_KEY.');
    if (err.status === 429) throw new Error('Brave Search rate limit exceeded. Try again later.');
    throw new Error(`Brave Search request failed: ${err.message}`);
  }

  if (!searchResults.web || searchResults.web.results.length === 0) {
    throw new Error(`No results found for query: ${query}`);
  }

  const firstResult = searchResults.web.results[0];
  const spotifyUri = extractSpotifyUri(firstResult.url);
  if (!spotifyUri) {
    throw new Error('Could not extract a Spotify track URI from search results.');
  }

  const devices = await discoverSpeakers();
  const speaker = devices.find((d) => d.name === speakerName);
  if (!speaker) {
    const available = devices.map((d) => d.name).join(', ');
    throw new Error(`Speaker not found: ${speakerName}. Available: ${available || 'none'}`);
  }

  await speaker.play(spotifyUri);

  return {
    success: true,
    track: firstResult.title,
    speaker: speakerName,
    uri: spotifyUri,
  };
}

async function getCurrentTrack(speakerName) {
  if (!speakerName || !SPEAKER_NAME_RE.test(speakerName)) {
    throw new Error('Invalid speaker name.');
  }

  const devices = await discoverSpeakers();
  const speaker = devices.find((d) => d.name === speakerName);
  if (!speaker) {
    const available = devices.map((d) => d.name).join(', ');
    throw new Error(`Speaker not found: ${speakerName}. Available: ${available || 'none'}`);
  }

  const currentTrack = await speaker.currentTrack();
  return currentTrack;
}

async function listSpeakers() {
  const devices = await discoverSpeakers();
  return devices.map((d) => ({ name: d.name, host: d.host }));
}

// CLI usage
if (require.main === module) {
  const [, , command, speakerName, ...queryParts] = process.argv;
  const query = queryParts.join(' ');
  const unsafe = queryParts.includes('--unsafe');

  (async () => {
    try {
      if (command === 'play') {
        const result = await searchAndPlay(speakerName, query.replace('--unsafe', '').trim(), {
          unsafe,
        });
        console.log(`Playing "${result.track}" on ${result.speaker}`);
      } else if (command === 'current') {
        const track = await getCurrentTrack(speakerName);
        console.log(`Currently playing: ${track.title} by ${track.artist}`);
      } else if (command === 'list') {
        const speakers = await listSpeakers();
        if (speakers.length === 0) {
          console.log('No Sonos speakers found on the network.');
        } else {
          speakers.forEach((s) => console.log(`- ${s.name} (${s.host})`));
        }
      } else {
        console.log('Usage:');
        console.log('  node index.js play <speaker-name> <search-query> [--unsafe]');
        console.log('  node index.js current <speaker-name>');
        console.log('  node index.js list');
        process.exit(1);
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  })();
}

module.exports = { searchAndPlay, getCurrentTrack, listSpeakers };
