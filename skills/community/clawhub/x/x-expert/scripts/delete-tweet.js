#!/usr/bin/env node

/**
 * X Publisher - Delete a tweet
 * Usage: node delete-tweet.js "tweet_id"
 */

const { TwitterApi } = require('twitter-api-v2');

async function deleteTweet(tweetId) {
  const apiKey = process.env.X_API_KEY;
  const apiSecret = process.env.X_API_SECRET;
  const accessToken = process.env.X_ACCESS_TOKEN;
  const accessSecret = process.env.X_ACCESS_TOKEN_SECRET;

  if (!apiKey || !apiSecret || !accessToken || !accessSecret) {
    console.error('Error: Missing required environment variables.');
    process.exit(1);
  }

  if (!tweetId) {
    console.error('Usage: node delete-tweet.js "tweet_id"');
    process.exit(1);
  }

  const client = new TwitterApi({
    appKey: apiKey,
    appSecret: apiSecret,
    accessToken: accessToken,
    accessSecret: accessSecret,
  });

  try {
    await client.v2.deleteTweet(tweetId);
    console.log('Tweet deleted successfully!');
    console.log('Deleted Tweet ID:', tweetId);
  } catch (error) {
    console.error('Error deleting tweet:', error.message);
    process.exit(1);
  }
}

const tweetId = process.argv[2];
deleteTweet(tweetId);
