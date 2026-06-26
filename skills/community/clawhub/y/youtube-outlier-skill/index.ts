import { google } from 'googleapis';
import { Client as DiscordClient, TextChannel } from 'discord.js';
import { getYoutubeOutlierVideos, extractVideoMetadata } from './youtubeUtils'; // <-- implement these helpers
import dotenv from 'dotenv';

dotenv.config({ path: __dirname + '/.env' });

// Environment vars
const SHEET_ID = process.env.GOOGLE_SHEET_ID;
const SHEET_RANGE = process.env.GOOGLE_SHEET_RANGE || 'Sheet1!A1';
const DISCORD_TOKEN = process.env.DISCORD_BOT_TOKEN;
const DISCORD_CHANNEL_ID = process.env.DISCORD_CHANNEL_ID;

// ============ Google Sheets Setup
const getSheets = () => {
  const auth = new google.auth.GoogleAuth({
    credentials: JSON.parse(process.env.GOOGLE_SHEETS_CREDENTIALS_JSON || '{}'),
    scopes: ['https://www.googleapis.com/auth/spreadsheets'],
  });
  return google.sheets({ version: 'v4', auth });
};

// ============ Discord Setup
const getDiscordClient = async () => {
  const client = new DiscordClient({ intents: [] });
  await client.login(DISCORD_TOKEN);
  return client;
};

// ============ Main Handler
export async function handler({ niche }: { niche: string }) {
  const DRY_RUN = false;
  // 1. Find outlier YouTube videos for given niche(s)
  const videos = await getYoutubeOutlierVideos(niche);
  if (!videos.length) return 'No outlier videos found.';

  // 2. Extract metadata & enrich
  const enriched = await Promise.all(videos.map(extractVideoMetadata));

  const rows = enriched.map(v => [
    niche,
    v.title,
    v.thumbnail,
    v.mainIdea,
    v.transcriptPoints,
    v.tags.join(','),
    v.hashtags.join(',')
  ]);
  
  // === DRY-RUN BLOCK ===
  if (DRY_RUN) {
    console.log('DRY RUN: Video Rows:', rows);
    console.log('DRY RUN: Would post summary to Discord:', rows.map(r => `${r[1]} | ${r[3]} | ${r[2]}`).join('\n'));
    return `DRY RUN: ${rows.length} videos found. No data written.`;
  }
  // === END DRY-RUN BLOCK ===

  // 3. Write to Google Sheet
  const sheets = getSheets();
  await sheets.spreadsheets.values.append({
    spreadsheetId: SHEET_ID,
    range: SHEET_RANGE,
    valueInputOption: 'RAW',
    requestBody: { values: rows }
  });

  // 4. Post summary to Discord
  const discord = await getDiscordClient();
  const channel = await discord.channels.fetch(DISCORD_CHANNEL_ID!);
  if (channel && channel.isTextBased()) {
    let msg = '**YouTube Outlier Trend Report: ' + niche + '**\n';
    msg += 'Title | Main Idea | Thumbnail URL\n';
    msg += rows.map(r => `${r[1]} | ${r[3]} | ${r[2]}`).join('\n');
    (channel as TextChannel).send(msg);
  }

  return `Job complete. ${rows.length} videos saved and reported.`;
}

// ---- You should implement getYoutubeOutlierVideos and extractVideoMetadata in a youtubeUtils.ts file ----
// - getYoutubeOutlierVideos(niche: string): Promise<YouTubeVideo[]> -- finds trending/outlier videos for the niche
// - extractVideoMetadata(video): Promise<EnrichedVideo> -- gets transcripts, main points, tags, hashtags
// Also consider using youtube-api-skill if available for easier calls.

// --- BOOTSTRAP FOR CLI ---
if (require.main === module) {
  // Grab niche argument from CLI (--niche="topic")
  const argNiche = process.argv.find(arg => arg.startsWith('--niche='));
  const niche = argNiche ? argNiche.split('=')[1] : '';
  console.log('[YTOUTLIER] CLI bootstrap running with niche:', niche);
  handler({ niche }).then(result => {
    console.log('RESULT:', result);
    process.exit(0);
  }).catch(err => {
    console.error('ERROR:', err);
    process.exit(1);
  });
}
