#!/usr/bin/env node

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { x402Client, wrapFetchWithPayment } from '@x402/fetch';
import { registerExactEvmScheme } from '@x402/evm/exact/client';
import { toClientEvmSigner } from '@x402/evm';
import { privateKeyToAccount } from 'viem/accounts';
import { createPublicClient, http } from 'viem';
import { base } from 'viem/chains';
import { z } from 'zod';
import { chromium } from 'playwright';
import { loadCredentials, saveCredentials, clearCredentials, CREDS_PATH } from './auth.js';
import 'dotenv/config';

// ── Config ────────────────────────────────────────────────────────────────────

const API_BASE = process.env.API_BASE ?? 'https://x402.twit.sh';
const privateKey = process.env.WALLET_PRIVATE_KEY as `0x${string}` | undefined;

if (!privateKey) {
  process.stderr.write('Error: WALLET_PRIVATE_KEY environment variable is required.\n');
  process.stderr.write('Fund a wallet with a few USDC on Base and set its private key.\n');
  process.exit(1);
}

// ── x402 payment client ───────────────────────────────────────────────────────

const account = privateKeyToAccount(privateKey);
const publicClient = createPublicClient({ chain: base, transport: http() });
const signer = toClientEvmSigner(account, publicClient);
const client = new x402Client();
registerExactEvmScheme(client, { signer });
const fetchWithPayment = wrapFetchWithPayment(fetch, client);

async function call(path: string): Promise<unknown> {
  const res = await fetchWithPayment(`${API_BASE}${path}`);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json();
}

// ── MCP server ────────────────────────────────────────────────────────────────

const server = new McpServer({
  name: 'twit-mcp',
  version: '1.0.0',
  description: 'Real-time X/Twitter data via x402 micropayments. Pay per request in USDC on Base. No API keys required.',
});

// ── Users ─────────────────────────────────────────────────────────────────────

server.tool(
  'get_user_by_username',
  'Retrieve a Twitter/X user profile by username. Returns id, name, bio, follower count, verified status, and more.',
  {
    username: z.string().describe('Twitter/X username without the @ symbol (e.g. "elonmusk")'),
  },
  async ({ username }) => {
    const data = await call(`/users/by/username?username=${encodeURIComponent(username)}`);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'get_user_by_id',
  'Retrieve a Twitter/X user profile by their numeric ID.',
  {
    id: z.string().describe('Numeric Twitter/X user ID (e.g. "44196397")'),
  },
  async ({ id }) => {
    const data = await call(`/users/by/id?id=${id}`);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'search_users',
  'Search for Twitter/X users by keyword. Returns up to 20 users per page. Use next_token to paginate.',
  {
    query: z.string().describe('Search query (e.g. "bitcoin developer")'),
    next_token: z.string().optional().describe('Pagination cursor from a previous response meta.next_token'),
  },
  async ({ query, next_token }) => {
    let path = `/users/search?query=${encodeURIComponent(query)}`;
    if (next_token) path += `&next_token=${encodeURIComponent(next_token)}`;
    const data = await call(path);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'get_user_followers',
  'Retrieve the followers of a Twitter/X user. Returns ~50 users per page. Use next_token to paginate.',
  {
    id: z.string().describe('Numeric Twitter/X user ID'),
    next_token: z.string().optional().describe('Pagination cursor from a previous response meta.next_token'),
  },
  async ({ id, next_token }) => {
    let path = `/users/followers?id=${id}`;
    if (next_token) path += `&next_token=${encodeURIComponent(next_token)}`;
    const data = await call(path);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'get_user_following',
  'Retrieve the accounts a Twitter/X user follows. Returns ~50 users per page. Use next_token to paginate.',
  {
    id: z.string().describe('Numeric Twitter/X user ID'),
    next_token: z.string().optional().describe('Pagination cursor from a previous response meta.next_token'),
  },
  async ({ id, next_token }) => {
    let path = `/users/following?id=${id}`;
    if (next_token) path += `&next_token=${encodeURIComponent(next_token)}`;
    const data = await call(path);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'get_users',
  'Retrieve multiple Twitter/X user profiles in a single request (max 50 IDs).',
  {
    ids: z.string().describe('Comma-separated numeric Twitter/X user IDs (max 50, e.g. "44196397,12,783214")'),
  },
  async ({ ids }) => {
    const data = await call(`/users?ids=${encodeURIComponent(ids)}`);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Tweets ────────────────────────────────────────────────────────────────────

server.tool(
  'get_tweet_by_id',
  'Retrieve a single tweet/post by its ID. Includes author info, text, metrics, and metadata.',
  {
    id: z.string().describe('Numeric tweet ID (e.g. "1110302988")'),
  },
  async ({ id }) => {
    const data = await call(`/tweets/by/id?id=${id}`);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'get_article_by_id',
  'Retrieve the full content of an X Article by the tweet ID of the post that hosts it. Returns article title, preview text, cover image, publish date, and full article_content as Markdown (headings, bold, italic, lists, images). Not available in the official X API.',
  {
    id: z.string().describe('Numeric tweet ID of the X Article post (e.g. "2010751592346030461")'),
  },
  async ({ id }) => {
    const data = await call(`/articles/by/id?id=${id}`);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'get_user_tweets',
  "Retrieve a user's recent tweets/posts. Returns ~20 tweets per page. Use next_token to paginate.",
  {
    username: z.string().describe('Twitter/X username without the @ symbol'),
    next_token: z.string().optional().describe('Pagination cursor from a previous response meta.next_token'),
  },
  async ({ username, next_token }) => {
    let path = `/tweets/user?username=${encodeURIComponent(username)}`;
    if (next_token) path += `&next_token=${encodeURIComponent(next_token)}`;
    const data = await call(path);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'search_tweets',
  'Search the full Twitter/X archive with advanced filters. Returns ~20 tweets per page. At least one filter is required.',
  {
    words:      z.string().optional().describe('All of these words must appear in the tweet'),
    phrase:     z.string().optional().describe('This exact phrase must appear'),
    anyWords:   z.string().optional().describe('Any of these words (space-separated)'),
    noneWords:  z.string().optional().describe('None of these words (space-separated)'),
    hashtags:   z.string().optional().describe('These hashtags (without #, space-separated)'),
    from:       z.string().optional().describe('Tweets from this username (without @)'),
    to:         z.string().optional().describe('Tweets replying to this username (without @)'),
    mentioning: z.string().optional().describe('Tweets mentioning this username (without @)'),
    minReplies: z.number().optional().describe('Minimum reply count'),
    minLikes:   z.number().optional().describe('Minimum like count'),
    minReposts: z.number().optional().describe('Minimum retweet count'),
    since:      z.string().optional().describe('Start date inclusive (YYYY-MM-DD)'),
    until:      z.string().optional().describe('End date exclusive (YYYY-MM-DD)'),
    next_token: z.string().optional().describe('Pagination cursor from a previous response meta.next_token'),
  },
  async (params) => {
    const qs = Object.entries(params)
      .filter(([, v]) => v !== undefined)
      .map(([k, v]) => `${k}=${encodeURIComponent(String(v))}`)
      .join('&');
    const data = await call(`/tweets/search?${qs}`);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'get_tweets',
  'Retrieve multiple tweets/posts by their IDs in a single request (max 50 IDs).',
  {
    ids: z.string().describe('Comma-separated tweet IDs (max 50, e.g. "1110302988,1234567890")'),
  },
  async ({ ids }) => {
    const data = await call(`/tweets?ids=${encodeURIComponent(ids)}`);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Communities ───────────────────────────────────────────────────────────────

server.tool(
  'get_community_by_id',
  'Retrieve details of an X Community by its numeric ID. Returns name, description, member count, join policy, topic, rules, banner image, and admin/creator profiles. Not available in the official X API.',
  {
    id: z.string().describe('Numeric community ID (e.g. "1506789406203695107")'),
  },
  async ({ id }) => {
    const data = await call(`/communities/by/id?id=${id}`);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'get_community_posts',
  'Retrieve latest posts from an X Community. Returns ~20 tweets per page with author profiles. Use next_token to paginate. Not available in the official X API.',
  {
    id: z.string().describe('Numeric community ID'),
    next_token: z.string().optional().describe('Pagination cursor from a previous response meta.next_token'),
  },
  async ({ id, next_token }) => {
    let path = `/communities/posts?id=${id}`;
    if (next_token) path += `&next_token=${encodeURIComponent(next_token)}`;
    const data = await call(path);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'get_community_members',
  'Retrieve members of an X Community. Returns 10–20 user profiles per page with community role (Admin, Moderator, Member). Use next_token to paginate. Not available in the official X API.',
  {
    id: z.string().describe('Numeric community ID'),
    next_token: z.string().optional().describe('Pagination cursor from a previous response meta.next_token'),
  },
  async ({ id, next_token }) => {
    let path = `/communities/members?id=${id}`;
    if (next_token) path += `&next_token=${encodeURIComponent(next_token)}`;
    const data = await call(path);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Tweet engagement ──────────────────────────────────────────────────────────

server.tool(
  'get_tweet_replies',
  'Retrieve replies to a tweet. Returns ~30 reply tweets per page with author profiles. Use next_token to paginate.',
  {
    id: z.string().describe('Numeric tweet ID'),
    next_token: z.string().optional().describe('Pagination cursor from a previous response meta.next_token'),
  },
  async ({ id, next_token }) => {
    let path = `/tweets/replies?id=${id}`;
    if (next_token) path += `&next_token=${encodeURIComponent(next_token)}`;
    const data = await call(path);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'get_tweet_quote_tweets',
  'Retrieve tweets that quote a specific tweet. Returns ~20 quote tweets per page with author profiles. Use next_token to paginate.',
  {
    id: z.string().describe('Numeric tweet ID'),
    next_token: z.string().optional().describe('Pagination cursor from a previous response meta.next_token'),
  },
  async ({ id, next_token }) => {
    let path = `/tweets/quote_tweets?id=${id}`;
    if (next_token) path += `&next_token=${encodeURIComponent(next_token)}`;
    const data = await call(path);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'get_tweet_retweeted_by',
  'Retrieve users who reposted a specific tweet. Returns ~20 user profiles per page. Use next_token to paginate.',
  {
    id: z.string().describe('Numeric tweet ID'),
    next_token: z.string().optional().describe('Pagination cursor from a previous response meta.next_token'),
  },
  async ({ id, next_token }) => {
    let path = `/tweets/retweeted_by?id=${id}`;
    if (next_token) path += `&next_token=${encodeURIComponent(next_token)}`;
    const data = await call(path);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Lists ─────────────────────────────────────────────────────────────────────

server.tool(
  'get_list_by_id',
  'Retrieve details of a specific Twitter/X List by its numeric ID. Returns name, description, mode, member count, subscriber count, creation date, banner image, and owner profile.',
  {
    id: z.string().describe('Numeric Twitter/X List ID'),
  },
  async ({ id }) => {
    const data = await call(`/lists/by/id?id=${id}`);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'get_list_members',
  'Retrieve members of a Twitter/X List. Returns up to 100 user profiles per page. Use next_token to paginate.',
  {
    id: z.string().describe('Numeric Twitter/X List ID'),
    next_token: z.string().optional().describe('Pagination cursor from a previous response meta.next_token'),
  },
  async ({ id, next_token }) => {
    let path = `/lists/members?id=${id}`;
    if (next_token) path += `&next_token=${encodeURIComponent(next_token)}`;
    const data = await call(path);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'get_list_followers',
  'Retrieve users who follow a specific Twitter/X List. Returns up to 20 user profiles per page. Use next_token to paginate.',
  {
    id: z.string().describe('Numeric Twitter/X List ID'),
    next_token: z.string().optional().describe('Pagination cursor from a previous response meta.next_token'),
  },
  async ({ id, next_token }) => {
    let path = `/lists/followers?id=${id}`;
    if (next_token) path += `&next_token=${encodeURIComponent(next_token)}`;
    const data = await call(path);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

server.tool(
  'get_list_tweets',
  'Retrieve the latest tweets from a Twitter/X List. Returns ~100 tweets per page with author profiles. Use next_token to paginate.',
  {
    id: z.string().describe('Numeric Twitter/X List ID'),
    next_token: z.string().optional().describe('Pagination cursor from a previous response meta.next_token'),
  },
  async ({ id, next_token }) => {
    let path = `/lists/tweets?id=${id}`;
    if (next_token) path += `&next_token=${encodeURIComponent(next_token)}`;
    const data = await call(path);
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Post tweet ────────────────────────────────────────────────────────────────

server.tool(
  'post_tweet',
  'Post a new tweet/post as the authenticated Twitter/X user, or reply to an existing tweet. Requires Twitter credentials — use connect_twitter first if not already connected.',
  {
    text: z.string().max(280).describe('The content of the tweet (max 280 characters)'),
    in_reply_to_tweet_id: z.string().optional().describe('Numeric tweet ID to reply to (optional)'),
    quote_tweet_id: z.string().optional().describe('Numeric tweet ID to quote (optional)'),
  },
  async ({ text, in_reply_to_tweet_id, quote_tweet_id }) => {
    const creds = loadCredentials();
    if (!creds?.authToken || !creds?.ct0) {
      return {
        content: [{
          type: 'text' as const,
          text: 'No Twitter account connected. Use connect_twitter to authenticate first.',
        }],
      };
    }

    const res = await fetchWithPayment(`${API_BASE}/tweets`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text,
        auth_token: creds.authToken,
        ct0: creds.ct0,
        ...(in_reply_to_tweet_id && { in_reply_to_tweet_id }),
        ...(quote_tweet_id && { quote_tweet_id }),
      }),
    });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`API error ${res.status}: ${err}`);
    }

    const data = await res.json();
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Retweet ───────────────────────────────────────────────────────────────────

server.tool(
  'retweet',
  'Repost (retweet) a tweet by its ID as the authenticated Twitter/X user. Requires Twitter credentials — use connect_twitter first if not already connected.',
  {
    id: z.string().describe('Numeric tweet ID to retweet'),
  },
  async ({ id }) => {
    const creds = loadCredentials();
    if (!creds?.authToken || !creds?.ct0) {
      return {
        content: [{
          type: 'text' as const,
          text: 'No Twitter account connected. Use connect_twitter to authenticate first.',
        }],
      };
    }

    const params = new URLSearchParams({ id, auth_token: creds.authToken, ct0: creds.ct0 });
    const res = await fetchWithPayment(`${API_BASE}/tweets/retweet?${params}`, { method: 'POST' });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`API error ${res.status}: ${err}`);
    }

    const data = await res.json();
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Like tweet ────────────────────────────────────────────────────────────────

server.tool(
  'like_tweet',
  'Like a tweet by its ID as the authenticated Twitter/X user. Requires Twitter credentials — use connect_twitter first if not already connected.',
  {
    id: z.string().describe('Numeric tweet ID to like'),
  },
  async ({ id }) => {
    const creds = loadCredentials();
    if (!creds?.authToken || !creds?.ct0) {
      return {
        content: [{
          type: 'text' as const,
          text: 'No Twitter account connected. Use connect_twitter to authenticate first.',
        }],
      };
    }

    const params = new URLSearchParams({ id, auth_token: creds.authToken, ct0: creds.ct0 });
    const res = await fetchWithPayment(`${API_BASE}/tweets/like?${params}`, { method: 'POST' });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`API error ${res.status}: ${err}`);
    }

    const data = await res.json();
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Follow user ───────────────────────────────────────────────────────────────

server.tool(
  'follow_user',
  'Follow a Twitter/X user by their ID or username as the authenticated user. Pass either id or username — one is required. Requires Twitter credentials — use connect_twitter first if not already connected.',
  {
    id: z.string().optional().describe('Numeric Twitter/X user ID to follow'),
    username: z.string().optional().describe('Screen name to follow (without @)'),
  },
  async ({ id, username }) => {
    const creds = loadCredentials();
    if (!creds?.authToken || !creds?.ct0) {
      return {
        content: [{
          type: 'text' as const,
          text: 'No Twitter account connected. Use connect_twitter to authenticate first.',
        }],
      };
    }

    if (!id && !username) {
      return { content: [{ type: 'text' as const, text: 'Error: provide either id or username' }] };
    }

    const queryParams: Record<string, string> = { auth_token: creds.authToken, ct0: creds.ct0 };
    if (id) queryParams.id = id;
    else queryParams.username = username!;

    const params = new URLSearchParams(queryParams);
    const res = await fetchWithPayment(`${API_BASE}/users/following?${params}`, { method: 'POST' });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`API error ${res.status}: ${err}`);
    }

    const data = await res.json();
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Unfollow user ─────────────────────────────────────────────────────────────

server.tool(
  'unfollow_user',
  'Unfollow a Twitter/X user by their ID or username as the authenticated user. Pass either id or username — one is required. Requires Twitter credentials — use connect_twitter first if not already connected.',
  {
    id: z.string().optional().describe('Numeric Twitter/X user ID to unfollow'),
    username: z.string().optional().describe('Screen name to unfollow (without @)'),
  },
  async ({ id, username }) => {
    const creds = loadCredentials();
    if (!creds?.authToken || !creds?.ct0) {
      return {
        content: [{
          type: 'text' as const,
          text: 'No Twitter account connected. Use connect_twitter to authenticate first.',
        }],
      };
    }

    if (!id && !username) {
      return { content: [{ type: 'text' as const, text: 'Error: provide either id or username' }] };
    }

    const queryParams: Record<string, string> = { auth_token: creds.authToken, ct0: creds.ct0 };
    if (id) queryParams.id = id;
    else queryParams.username = username!;

    const params = new URLSearchParams(queryParams);
    const res = await fetchWithPayment(`${API_BASE}/users/following?${params}`, { method: 'DELETE' });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`API error ${res.status}: ${err}`);
    }

    const data = await res.json();
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Bookmark tweet ────────────────────────────────────────────────────────────

server.tool(
  'bookmark_tweet',
  'Add a tweet to the authenticated user\'s bookmarks by its ID. Requires Twitter credentials — use connect_twitter first if not already connected.',
  {
    id: z.string().describe('Numeric tweet ID to bookmark'),
  },
  async ({ id }) => {
    const creds = loadCredentials();
    if (!creds?.authToken || !creds?.ct0) {
      return {
        content: [{
          type: 'text' as const,
          text: 'No Twitter account connected. Use connect_twitter to authenticate first.',
        }],
      };
    }

    const params = new URLSearchParams({ id, auth_token: creds.authToken, ct0: creds.ct0 });
    const res = await fetchWithPayment(`${API_BASE}/tweets/bookmark?${params}`, { method: 'POST' });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`API error ${res.status}: ${err}`);
    }

    const data = await res.json();
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Remove bookmark ────────────────────────────────────────────────────────────

server.tool(
  'unbookmark_tweet',
  'Remove a tweet from the authenticated user\'s bookmarks by its ID. Requires Twitter credentials — use connect_twitter first if not already connected.',
  {
    id: z.string().describe('Numeric tweet ID to remove from bookmarks'),
  },
  async ({ id }) => {
    const creds = loadCredentials();
    if (!creds?.authToken || !creds?.ct0) {
      return {
        content: [{
          type: 'text' as const,
          text: 'No Twitter account connected. Use connect_twitter to authenticate first.',
        }],
      };
    }

    const params = new URLSearchParams({ id, auth_token: creds.authToken, ct0: creds.ct0 });
    const res = await fetchWithPayment(`${API_BASE}/tweets/bookmark?${params}`, { method: 'DELETE' });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`API error ${res.status}: ${err}`);
    }

    const data = await res.json();
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Unlike tweet ──────────────────────────────────────────────────────────────

server.tool(
  'unlike_tweet',
  'Remove a like (unlike) from a tweet by its ID as the authenticated Twitter/X user. Requires Twitter credentials — use connect_twitter first if not already connected.',
  {
    id: z.string().describe('Numeric tweet ID to unlike'),
  },
  async ({ id }) => {
    const creds = loadCredentials();
    if (!creds?.authToken || !creds?.ct0) {
      return {
        content: [{
          type: 'text' as const,
          text: 'No Twitter account connected. Use connect_twitter to authenticate first.',
        }],
      };
    }

    const params = new URLSearchParams({ id, auth_token: creds.authToken, ct0: creds.ct0 });
    const res = await fetchWithPayment(`${API_BASE}/tweets/like?${params}`, { method: 'DELETE' });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`API error ${res.status}: ${err}`);
    }

    const data = await res.json();
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Unretweet ─────────────────────────────────────────────────────────────────

server.tool(
  'unretweet',
  'Remove a retweet (unrepost) by tweet ID as the authenticated Twitter/X user. Requires Twitter credentials — use connect_twitter first if not already connected.',
  {
    id: z.string().describe('Numeric tweet ID to unretweet'),
  },
  async ({ id }) => {
    const creds = loadCredentials();
    if (!creds?.authToken || !creds?.ct0) {
      return {
        content: [{
          type: 'text' as const,
          text: 'No Twitter account connected. Use connect_twitter to authenticate first.',
        }],
      };
    }

    const params = new URLSearchParams({ id, auth_token: creds.authToken, ct0: creds.ct0 });
    const res = await fetchWithPayment(`${API_BASE}/tweets/retweet?${params}`, { method: 'DELETE' });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`API error ${res.status}: ${err}`);
    }

    const data = await res.json();
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Delete tweet ──────────────────────────────────────────────────────────────

server.tool(
  'delete_tweet',
  'Delete a tweet/post by its ID. Only works for tweets owned by the authenticated user. Requires Twitter credentials — use connect_twitter first if not already connected.',
  {
    id: z.string().describe('Numeric tweet ID to delete'),
  },
  async ({ id }) => {
    const creds = loadCredentials();
    if (!creds?.authToken || !creds?.ct0) {
      return {
        content: [{
          type: 'text' as const,
          text: 'No Twitter account connected. Use connect_twitter to authenticate first.',
        }],
      };
    }

    const params = new URLSearchParams({ id, auth_token: creds.authToken, ct0: creds.ct0 });
    const res = await fetchWithPayment(`${API_BASE}/tweets?${params}`, { method: 'DELETE' });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`API error ${res.status}: ${err}`);
    }

    const data = await res.json();
    return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
  },
);

// ── Twitter auth ──────────────────────────────────────────────────────────────

server.tool(
  'connect_twitter',
  'Connect your Twitter/X account by opening a browser window. Logs in via x.com and stores session cookies locally for posting tweets. Credentials are saved to ~/.twit-mcp-credentials.json.',
  {},
  async () => {
    const browser = await chromium.launch({
      headless: false,
      channel: 'chrome',
      args: ['--disable-blink-features=AutomationControlled'],
    });
    const context = await browser.newContext();
    await context.addInitScript(() => {
      Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    });
    const page = await context.newPage();

    await page.goto('https://x.com');

    // Poll for auth_token + ct0 cookies (up to 3 minutes)
    let creds: { authToken: string; ct0: string; username?: string } | null = null;

    for (let i = 0; i < 180; i++) {
      const cookies = await context.cookies('https://x.com');
      const authToken = cookies.find((c) => c.name === 'auth_token');
      const ct0 = cookies.find((c) => c.name === 'ct0');

      if (authToken && ct0) {
        // Try to get username from page
        let username: string | undefined;
        try {
          const handle = await page.$eval(
            'a[data-testid="AppTabBar_Profile_Link"]',
            (el) => el.getAttribute('href')
          );
          username = handle?.replace('/', '') ?? undefined;
        } catch {
          // username is optional
        }

        creds = { authToken: authToken.value, ct0: ct0.value, username };
        break;
      }

      await page.waitForTimeout(1000);
    }

    await browser.close();

    if (!creds) {
      throw new Error('Timed out waiting for login (3 minutes). Please try again.');
    }

    saveCredentials(creds);

    const who = creds.username ? `@${creds.username}` : 'your account';
    return {
      content: [{
        type: 'text' as const,
        text: `Connected ${who} successfully. Credentials saved to ~/.twit-mcp-credentials.json — ready to use immediately.`,
      }],
    };
  },
);

server.tool(
  'disconnect_twitter',
  'Disconnect your Twitter/X account by clearing stored session credentials.',
  {},
  async () => {
    const existing = loadCredentials();
    if (!existing?.authToken) {
      return { content: [{ type: 'text' as const, text: 'No Twitter account connected.' }] };
    }
    clearCredentials();
    return { content: [{ type: 'text' as const, text: 'Disconnected. Credentials cleared from ~/.twit-mcp-credentials.json.' }] };
  },
);

server.tool(
  'twitter_account_status',
  'Check whether a Twitter/X account is currently connected.',
  {},
  async () => {
    const creds = loadCredentials();
    if (!creds?.authToken) {
      return { content: [{ type: 'text' as const, text: 'No Twitter account connected. Use connect_twitter to connect.' }] };
    }
    const who = creds.username ? `@${creds.username}` : 'an account';
    return { content: [{ type: 'text' as const, text: `Connected as ${who}.` }] };
  },
);

// ── Start ─────────────────────────────────────────────────────────────────────

const transport = new StdioServerTransport();
await server.connect(transport);
