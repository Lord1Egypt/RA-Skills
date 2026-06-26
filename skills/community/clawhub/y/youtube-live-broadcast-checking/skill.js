const { google } = require('googleapis');
const { getYoutubeApiKey } = require('./config');
const store = require('./store');

// YouTube API client (lazy init)
let youtubeClient = null;

function getYouTubeClient() {
  if (youtubeClient) return youtubeClient;
  const apiKey = getYoutubeApiKey();
  if (!apiKey) {
    throw new Error('Missing YOUTUBE_API_KEY environment variable');
  }
  youtubeClient = google.youtube({
    version: 'v3',
    auth: apiKey
  });
  return youtubeClient;
}

function isValidChannelId(channelId) {
  return typeof channelId === 'string' && (channelId.startsWith('UC') || channelId.startsWith('PL'));
}

async function resolveChannelId(identifier, youtube) {
  if (!identifier || typeof identifier !== 'string') {
    return { error: 'Invalid channel identifier' };
  }

  const trimmed = identifier.trim();

  if (isValidChannelId(trimmed)) {
    return { channelId: trimmed };
  }

  try {
    const urlMatch = trimmed.match(/(?:youtube\.com\/(?:channel\/|@|user\/)?([^\/\?]+))/);
    if (urlMatch) {
      const possibleId = urlMatch[1];
      if (isValidChannelId(possibleId)) {
        return { channelId: possibleId };
      }
    }
  } catch {
    // continue to search
  }

  try {
    const searchResp = await youtube.search.list({
      part: ['snippet'],
      q: trimmed,
      type: ['channel'],
      maxResults: 1
    });

    const items = searchResp.data.items || [];
    if (items.length > 0) {
      return { channelId: items[0].id.channelId };
    }
  } catch (err) {
    console.error('Channel resolve error:', err.message);
    return { error: `Could not resolve channel: ${err.message}` };
  }

  return { error: 'Could not resolve channel identifier' };
}

async function getUpcomingForChannel(channelId, youtube) {
  try {
    const searchResp = await youtube.search.list({
      part: ['snippet'],
      channelId: channelId,
      eventType: 'upcoming',
      type: 'video',
      maxResults: 10
    });

    const upcomingVideos = searchResp.data.items || [];
    if (upcomingVideos.length === 0) {
      return null;
    }

    const videoIds = upcomingVideos.map(v => v.id.videoId).join(',');
    const detailsResp = await youtube.videos.list({
      part: ['liveStreamingDetails'],
      id: videoIds
    });

    const detailsMap = {};
    (detailsResp.data.items || []).forEach(vid => {
      detailsMap[vid.id] = vid.liveStreamingDetails || {};
    });

    const results = upcomingVideos.map(v => {
      const details = detailsMap[v.id.videoId] || {};
      return {
        video_id: v.id.videoId,
        title: v.snippet.title,
        scheduled_start_time: details.scheduledStartTime || null,
        thumbnail_url: v.snippet.thumbnails?.high?.url || v.snippet.thumbnails?.default?.url || '',
        video_url: `https://www.youtube.com/watch?v=${v.id.videoId}`
      };
    }).filter(r => r.scheduled_start_time);

    if (results.length === 0) {
      return null;
    }

    results.sort((a, b) => new Date(a.scheduled_start_time) - new Date(b.scheduled_start_time));
    return results[0];
  } catch (err) {
    console.error(`Error fetching upcoming for channel ${channelId}:`, err.message);
    throw err;
  }
}

async function withResolvedChannel(params, handler) {
  const { channel_id } = params;
  if (!channel_id) {
    return { error: 'channel_id is required' };
  }

  const youtube = getYouTubeClient();
  const resolved = await resolveChannelId(channel_id, youtube);
  if (resolved.error) {
    return resolved;
  }

  return handler({ channel_id: resolved.channelId, youtube });
}

// Tool: add_channel
async function addChannel(params) {
  return withResolvedChannel(params, async ({ channel_id }) => {
    if (store.findChannel(channel_id)) {
      return { success: false, message: `Channel ${channel_id} is already in the watchlist` };
    }

    try {
      const youtube = getYouTubeClient();
      const response = await youtube.channels.list({
        part: ['snippet'],
        id: channel_id,
        maxResults: 1
      });

      if (!response.data.items || response.data.items.length === 0) {
        return { error: `Channel ${channel_id} not found` };
      }

      const channelInfo = response.data.items[0];
      const channelName = channelInfo.snippet.title;

      store.addChannel({
        id: channel_id,
        name: channelName,
        added_at: new Date().toISOString()
      });

      return { id: channel_id, name: channelName, status: 'added' };
    } catch (err) {
      console.error('YouTube API error:', err.message);
      if (err.message.includes('API key') || err.response?.status === 400) {
        return { error: 'YouTube API key is invalid or missing' };
      } else if (err.response?.status === 403) {
        return { error: 'Quota exceeded' };
      } else if (err.response?.status === 404) {
        return { error: 'Channel not found' };
      } else {
        return { error: `YouTube API error: ${err.message}` };
      }
    }
  });
}

// Tool: remove_channel
async function removeChannel(params) {
  return withResolvedChannel(params, async ({ channel_id }) => {
    if (!store.removeChannelById(channel_id)) {
      return { error: `Channel ${channel_id} not found in watchlist` };
    }
    return { removed: true };
  });
}

// Tool: list_channels
async function listChannels() {
  return store.getWatchlist();
}

// Tool: get_next_broadcast
async function getNextBroadcast(params) {
  return withResolvedChannel(params, async ({ channel_id }) => {
    try {
      const youtube = getYouTubeClient();
      const result = await getUpcomingForChannel(channel_id, youtube);
      if (!result) {
        return null;
      }

      let channelName = 'Unknown Channel';
      const fromWatchlist = store.findChannel(channel_id);
      if (fromWatchlist) {
        channelName = fromWatchlist.name;
      } else {
        try {
          const channelResp = await youtube.channels.list({
            part: ['snippet'],
            id: channel_id,
            maxResults: 1
          });
          if (channelResp.data.items?.[0]?.snippet?.title) {
            channelName = channelResp.data.items[0].snippet.title;
          }
        } catch (_) {}
      }

      return {
        channel_id: channel_id,
        channel_name: channelName,
        video_id: result.video_id,
        title: result.title,
        scheduled_start_time: result.scheduled_start_time,
        thumbnail_url: result.thumbnail_url,
        video_url: result.video_url
      };
    } catch (err) {
      console.error('YouTube API error:', err.message);
      if (err.response?.status === 403) {
        return { error: 'Quota exceeded' };
      } else {
        return { error: `YouTube API error: ${err.message}` };
      }
    }
  });
}

// Tool: check_upcoming_broadcasts
async function checkUpcomingBroadcasts(params) {
  const { channel_ids } = params;
  let channelIdentifiers = channel_ids;

  if (!channelIdentifiers || channelIdentifiers.length === 0) {
    // Get watchlist; convert stored channel objects to IDs
    const watchlist = store.getWatchlist();
    channelIdentifiers = watchlist.map(ch => ch.id);
  }

  if (!Array.isArray(channelIdentifiers) || channelIdentifiers.length === 0) {
    return [];
  }

  try {
    const youtube = getYouTubeClient();
    const results = [];
    const channelPromises = [];

    for (const identifier of channelIdentifiers) {
      channelPromises.push((async () => {
        try {
          // Resolve identifier to a channel ID
          const resolved = await resolveChannelId(identifier, youtube);
          if (resolved.error) {
            console.error(`Skipping channel ${identifier}: ${resolved.error}`);
            return;
          }
          const channelId = resolved.channelId;

          // Determine channel name
          let channelName = 'Unknown Channel';
          const fromWatchlist = store.findChannel(channelId);
          if (fromWatchlist) {
            channelName = fromWatchlist.name;
          } else {
            try {
              const channelResp = await youtube.channels.list({
                part: ['snippet'],
                id: channelId,
                maxResults: 1
              });
              if (channelResp.data.items?.[0]?.snippet?.title) {
                channelName = channelResp.data.items[0].snippet.title;
              }
            } catch (_) {}
          }

          const upcoming = await getUpcomingForChannel(channelId, youtube);
          if (upcoming) {
            results.push({
              channel_id: channelId,
              channel_name: channelName,
              video_id: upcoming.video_id,
              title: upcoming.title,
              scheduled_start_time: upcoming.scheduled_start_time,
              thumbnail_url: upcoming.thumbnail_url,
              video_url: upcoming.video_url
            });
          }
        } catch (err) {
          console.error(`Error processing channel ${identifier}:`, err.message);
          if (err.response?.status === 403) {
            throw err;
          }
        }
      })());
    }

    await Promise.all(channelPromises);

    results.sort((a, b) => new Date(a.scheduled_start_time) - new Date(b.scheduled_start_time));
    return results;
  } catch (err) {
    console.error('YouTube API error:', err.message);
    if (err.response?.status === 403) {
      return { error: 'Quota exceeded' };
    } else {
      return { error: `YouTube API error: ${err.message}` };
    }
  }
}

// Tool: get_live_broadcast
async function getLiveBroadcast(params) {
  return withResolvedChannel(params, async ({ channel_id }) => {
    try {
      const youtube = getYouTubeClient();

      const searchResp = await youtube.search.list({
        part: ['snippet'],
        channelId: channel_id,
        eventType: 'live',
        type: 'video',
        maxResults: 1
      });

      if (!searchResp.data.items || searchResp.data.items.length === 0) {
        return null;
      }

      const video = searchResp.data.items[0];
      const videoId = video.id.videoId;

      const videoResp = await youtube.videos.list({
        part: ['snippet', 'liveStreamingDetails'],
        id: videoId
      });

      const videoInfo = videoResp.data.items?.[0] || video;
      const snippet = videoInfo.snippet || video.snippet;

      return {
        channel_id: channel_id,
        video_id: videoId,
        title: snippet.title,
        description: snippet.description,
        thumbnail_url: snippet.thumbnails?.high?.url || snippet.thumbnails?.default?.url,
        video_url: `https://www.youtube.com/watch?v=${videoId}`,
        actual_start_time: videoInfo.liveStreamingDetails?.actualStartTime || null,
        concurrent_viewers: videoInfo.liveStreamingDetails?.concurrentViewers || null
      };
    } catch (err) {
      console.error('YouTube API error (get_live_broadcast):', err.message);
      if (err.response?.status === 403) {
        return { error: 'Quota exceeded or live streaming not enabled for this channel' };
      } else {
        return { error: `YouTube API error: ${err.message}` };
      }
    }
  });
}

// Deprecated
async function checkLiveStatus() {
  return { error: 'check_live_status is deprecated. Use check_upcoming_broadcasts instead.' };
}

// Tool: check_full_status
async function checkFullStatus(params) {
  const channel_ids = params.channel_ids || [];
  // Resolve all identifiers to channel IDs first
  const youtube = getYouTubeClient();
  const resolved = await Promise.all(
    channel_ids.map(async (id) => {
      const result = await resolveChannelId(id, youtube);
      return result.channelId || null;
    })
  );
  const validIds = resolved.filter((id) => id);

  // Run both checks in parallel
  const [live, upcoming] = await Promise.all([
    getLiveBroadcast({ channel_ids: validIds }),
    checkUpcomingBroadcasts({ channel_ids: validIds })
  ]);

  return {
    channels: validIds,
    live: live,
    upcoming: upcoming
  };
}

// Helper: get current HKT time string
function hktNow() {
  const now = new Date();
  // HKT is UTC+8
  const hktOffset = 8 * 60; // minutes
  const localOffset = now.getTimezoneOffset(); // minutes (negative if ahead of UTC)
  const hktTime = new Date(now.getTime() + (hktOffset + localOffset) * 60 * 1000);
  return hktTime.toISOString().replace('T', ' ').substring(0, 19) + ' HKT';
}

// Wrap a tool function to prepend HKT time
function withTimePrefix(toolFn) {
  return async function(params) {
    const prefix = `[Local time: ${hktNow()}]`;
    try {
      const result = await toolFn.call(this, params);
      // If result is an object or array, we can't just prepend string; attach a meta field
      if (typeof result === 'string') {
        return `${prefix}\n${result}`;
      } else {
        // Attach a _meta field with the timestamp
        if (result && typeof result === 'object') {
          result._meta = result._meta || {};
          result._meta.local_time = hktNow();
        }
        // Also log to console for visibility
        console.log(prefix);
        return result;
      }
    } catch (err) {
      console.log(prefix);
      throw err;
    }
  };
}

// Export
module.exports = {
  tools: {
    add_channel: withTimePrefix(addChannel),
    remove_channel: withTimePrefix(removeChannel),
    list_channels: withTimePrefix(listChannels),
    get_next_broadcast: withTimePrefix(getNextBroadcast),
    check_upcoming_broadcasts: withTimePrefix(checkUpcomingBroadcasts),
    get_live_broadcast: withTimePrefix(getLiveBroadcast),
    // expose resolver for external use
    resolve_channel_id: withTimePrefix(async (params) => {
      const { channel_id } = params || {};
      if (!channel_id) return { error: 'channel_id required' };
      const youtube = getYouTubeClient();
      const res = await resolveChannelId(channel_id, youtube);
      return res;
    }),
    check_full_status: withTimePrefix(checkFullStatus),
    check_live_status: withTimePrefix(checkLiveStatus)
  }
};
