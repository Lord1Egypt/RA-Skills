// youtubeUtils.ts -- YouTube search and enrichment helpers for youtube-outlier-skill
import axios from 'axios';
import { Anthropic } from '@anthropic-ai/sdk'; // Switching to Anthropic Claude for NLP

/** TYPES **/
export interface YoutubeVideo {
  id: string;
  title: string;
  description: string;
  thumbnail: string;
  viewCount: number;
  publishedAt: string;
  channelId: string;
  channelTitle: string;
}

export interface EnrichedVideo extends YoutubeVideo {
  mainIdea: string;
  transcriptPoints: string;
  tags: string[];
  hashtags: string[];
}

const API_KEY = process.env.YOUTUBE_API_KEY || '';
const CLAUDE_API_KEY = process.env.ANTHROPIC_API_KEY || '';
const anthropic = CLAUDE_API_KEY ? new Anthropic({ apiKey: CLAUDE_API_KEY }) : null;

/** Uses YouTube Data API v3 to search videos matching the niche, filtered by date. */
export async function getYoutubeOutlierVideos(niche: string): Promise<YoutubeVideo[]> {
  // 1. Search for most viewed videos in the past month for the niche
  const searchUrl =
    `https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=25&q=${encodeURIComponent(niche)}` +
    `&publishedAfter=${getLastMonthISO()}&key=${API_KEY}`;
  const searchRes = await axios.get(searchUrl);
  const videoIds = searchRes.data.items.map((item: any) => item.id.videoId).join(',');

  // 2. Fetch video stats (views, published date)
  const detailsUrl = `https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=${videoIds}&key=${API_KEY}`;
  const detailsRes = await axios.get(detailsUrl);
  const videos: YoutubeVideo[] = detailsRes.data.items.map((item: any) => ({
    id: item.id,
    title: item.snippet.title,
    description: item.snippet.description,
    thumbnail: item.snippet.thumbnails?.high?.url || '',
    viewCount: Number(item.statistics.viewCount || 0),
    publishedAt: item.snippet.publishedAt,
    channelId: item.snippet.channelId,
    channelTitle: item.snippet.channelTitle,
  }));

  // 3. Find outliers (top 20% by view count)
  const sorted = [...videos].sort((a, b) => b.viewCount - a.viewCount);
  const cutoff = Math.floor(sorted.length * 0.2) || 1;
  return sorted.slice(0, cutoff);
}

function getLastMonthISO() {
  const d = new Date();
  d.setMonth(d.getMonth() - 1);
  return d.toISOString();
}

export async function extractVideoMetadata(video: YoutubeVideo): Promise<EnrichedVideo> {
  // 1. (Optional) Get transcript using YouTube API or a third-party service
  let transcript = '';
  // transcript = await fetchTranscript(video.id); // implement as needed

  // 2. Use Anthropic Claude to summarize main idea and points
  let mainIdea = 'N/A';
  let transcriptPoints = 'N/A';
  if (anthropic) {
    const prompt =
      `Analyze the following YouTube video information and return the main idea and a list of main points.\n` +
      `Title: ${video.title}\n` +
      `Description: ${video.description}\n` +
      `Transcript: ${transcript}`;
    const completion = await anthropic.messages.create({
      model: 'claude-3-haiku-20240307', // You can use 'claude-3-sonnet-20240229' or 'claude-3-opus-20240229' if you have access
      max_tokens: 400,
      messages: [
        { role: 'user', content: prompt }
      ]
    });
    const summary = completion.content[0]?.text || '';
    mainIdea = summary.split('\n')[0] || '';
    transcriptPoints = summary.split('\n').slice(1).join('\n');
  }

  // 3. Extract tags and hashtags from description or YouTube API if available
  const tags = extractTags(video.description);
  const hashtags = extractHashtags(video.description);

  return {
    ...video,
    mainIdea,
    transcriptPoints,
    tags,
    hashtags,
  };
}

function extractTags(desc: string): string[] {
  // Simple placeholder for demo; YouTube API provides tags but not always surface
  return (desc.match(/#\w+/g) || []).map(s => s.replace('#', ''));
}

function extractHashtags(desc: string): string[] {
  // For now, reusing extractTags for hashtags; refine as needed
  return (desc.match(/#\w+/g) || []).map(s => s.replace('#', ''));
}
