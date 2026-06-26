/**
 * OpenClaw Skill for SocialRails
 *
 * Provides chat-based social media management through the SocialRails Public API.
 * Commands: schedule-post, show-analytics, generate-caption, list-posts, list-accounts
 */

const fs = require('fs');
const path = require('path');

function loadConfig() {
  const configPath = path.join(
    process.env.HOME || process.env.USERPROFILE || '~',
    '.openclaw',
    'openclaw.json'
  );

  try {
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    return config.skills?.socialrails || {};
  } catch {
    return {};
  }
}

async function apiRequest(method, endpoint, body = null) {
  const config = loadConfig();
  const apiKey = config.apiKey;
  const baseUrl = config.baseUrl || 'https://socialrails.com/api/v1';

  if (!apiKey) {
    return { error: 'SocialRails API key not configured. Run: openclaw config socialrails apiKey <your-key>' };
  }

  const options = {
    method,
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const url = `${baseUrl}${endpoint}`;

  try {
    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
      return { error: data.error?.message || `API error: ${response.status}` };
    }

    return data;
  } catch (err) {
    return { error: `Request failed: ${err.message}` };
  }
}

// --- Command Handlers ---

async function schedulePost(params) {
  const { content, platform, scheduled_for } = params;

  if (!content) return { error: 'Missing required parameter: content' };
  if (!platform) return { error: 'Missing required parameter: platform' };

  const body = { content, platform };
  if (scheduled_for) body.scheduled_for = scheduled_for;

  const result = await apiRequest('POST', '/posts', body);

  if (result.error) return result;

  const post = result.data;
  return {
    message: post.status === 'scheduled'
      ? `Post scheduled for ${post.scheduled_for} on ${post.platform}.`
      : `Post saved as draft on ${post.platform}.`,
    post_id: post.id,
  };
}

async function showAnalytics(params) {
  const { period = '7d', platform } = params;

  let endpoint = `/analytics?period=${period}`;
  if (platform) endpoint += `&platform=${platform}`;

  const result = await apiRequest('GET', endpoint);

  if (result.error) return result;

  const analytics = result.data;
  let summary = `Analytics for the last ${analytics.period}:\n`;
  summary += `Total posts published: ${analytics.total_posts}\n`;

  if (analytics.by_platform && analytics.by_platform.length > 0) {
    summary += '\nBy platform:\n';
    for (const p of analytics.by_platform) {
      summary += `  ${p.platform}: ${p.posts_published} posts\n`;
    }
  }

  return { message: summary };
}

async function generateCaption(params) {
  const { prompt, platform, tone } = params;

  if (!prompt) return { error: 'Missing required parameter: prompt' };

  const body = { prompt };
  if (platform) body.platform = platform;
  if (tone) body.tone = tone;

  const result = await apiRequest('POST', '/ai/generate', body);

  if (result.error) return result;

  return {
    message: `Generated content:\n\n${result.data.content}`,
    content: result.data.content,
  };
}

async function listPosts(params) {
  const { status, limit = 10 } = params;

  let endpoint = `/posts?limit=${limit}`;
  if (status) endpoint += `&status=${status}`;

  const result = await apiRequest('GET', endpoint);

  if (result.error) return result;

  if (!result.data || result.data.length === 0) {
    return { message: 'No posts found.' };
  }

  let summary = `Found ${result.pagination?.total || result.data.length} posts:\n\n`;
  for (const post of result.data) {
    const statusIcon = post.status === 'posted' ? 'v' : post.status === 'scheduled' ? '>' : '-';
    const text = typeof post.content === 'object' ? (post.content.all || JSON.stringify(post.content)) : String(post.content);
    const preview = text.length > 60 ? text.substring(0, 60) + '...' : text;
    summary += `[${statusIcon}] ${post.platform} | ${preview}\n`;
  }

  return { message: summary };
}

async function listAccounts() {
  const result = await apiRequest('GET', '/accounts');

  if (result.error) return result;

  if (!result.data || result.data.length === 0) {
    return { message: 'No connected accounts found.' };
  }

  let summary = 'Connected accounts:\n\n';
  for (const account of result.data) {
    summary += `  ${account.provider}: ${account.name}\n`;
  }

  return { message: summary };
}

// --- Exports ---

module.exports = {
  commands: {
    'schedule-post': schedulePost,
    'show-analytics': showAnalytics,
    'generate-caption': generateCaption,
    'list-posts': listPosts,
    'list-accounts': listAccounts,
  },
};
