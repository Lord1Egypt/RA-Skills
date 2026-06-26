#!/usr/bin/env node

/**
 * X Publisher - Post a single tweet
 * Usage: node post-tweet.js "Your tweet content"
 */

const { TwitterApi } = require('twitter-api-v2');

async function postTweet(content) {
  // Check environment variables
  const apiKey = process.env.X_API_KEY;
  const apiSecret = process.env.X_API_SECRET;
  const accessToken = process.env.X_ACCESS_TOKEN;
  const accessSecret = process.env.X_ACCESS_TOKEN_SECRET;

  if (!apiKey || !apiSecret || !accessToken || !accessSecret) {
    console.error('Error: Missing required environment variables.');
    console.error('Please set: X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET');
    process.exit(1);
  }

  const client = new TwitterApi({
    appKey: apiKey,
    appSecret: apiSecret,
    accessToken: accessToken,
    accessSecret: accessSecret,
  });

  try {
    const tweet = await client.v2.tweet(content);
    console.log('Tweet posted successfully!');
    console.log('Tweet ID:', tweet.data.id);
    console.log('Tweet URL:', `https://twitter.com/user/status/${tweet.data.id}`);
    return tweet.data;
  } catch (error) {
    console.error('Error posting tweet:', error.message);
    if (error.data) {
      console.error('Error details:', JSON.stringify(error.data, null, 2));
    }
    process.exit(1);
  }
}

// Get content from command line argument
const content = process.argv[2];
if (!content) {
  console.error('Usage: node post-tweet.js "Your tweet content"');
  process.exit(1);
}

postTweet(content);
