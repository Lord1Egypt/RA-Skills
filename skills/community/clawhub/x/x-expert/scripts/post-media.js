#!/usr/bin/env node

/**
 * X Publisher - Post a tweet with media
 * Usage: node post-media.js "Your tweet text" "/path/to/image.jpg"
 */

const { TwitterApi } = require('twitter-api-v2');
const fs = require('fs');
const path = require('path');

async function postTweetWithMedia(text, mediaPath) {
  const apiKey = process.env.X_API_KEY;
  const apiSecret = process.env.X_API_SECRET;
  const accessToken = process.env.X_ACCESS_TOKEN;
  const accessSecret = process.env.X_ACCESS_TOKEN_SECRET;

  if (!apiKey || !apiSecret || !accessToken || !accessSecret) {
    console.error('Error: Missing required environment variables.');
    process.exit(1);
  }

  // Check if media file exists
  if (!fs.existsSync(mediaPath)) {
    console.error(`Error: Media file not found: ${mediaPath}`);
    process.exit(1);
  }

  const client = new TwitterApi({
    appKey: apiKey,
    appSecret: apiSecret,
    accessToken: accessToken,
    accessSecret: accessSecret,
  });

  try {
    // Upload media first
    console.log('Uploading media...');
    const mediaId = await client.v1.uploadMedia(mediaPath);
    console.log('Media uploaded, ID:', mediaId);

    // Post tweet with media
    const tweet = await client.v2.tweet({
      text: text,
      media: { media_ids: [mediaId] },
    });

    console.log('Tweet posted successfully!');
    console.log('Tweet ID:', tweet.data.id);
    console.log('Tweet URL:', `https://twitter.com/user/status/${tweet.data.id}`);
    return tweet.data;
  } catch (error) {
    console.error('Error posting tweet with media:', error.message);
    process.exit(1);
  }
}

const text = process.argv[2];
const mediaPath = process.argv[3];

if (!text || !mediaPath) {
  console.error('Usage: node post-media.js "Your tweet text" "/path/to/image.jpg"');
  process.exit(1);
}

postTweetWithMedia(text, mediaPath);
