#!/usr/bin/env node

/**
 * X Publisher - Post a thread (tweet chain)
 * Usage: node post-thread.js "First tweet" "Second tweet" "Third tweet"
 */

const { TwitterApi } = require('twitter-api-v2');

async function postThread(tweets) {
  const apiKey = process.env.X_API_KEY;
  const apiSecret = process.env.X_API_SECRET;
  const accessToken = process.env.X_ACCESS_TOKEN;
  const accessSecret = process.env.X_ACCESS_TOKEN_SECRET;

  if (!apiKey || !apiSecret || !accessToken || !accessSecret) {
    console.error('Error: Missing required environment variables.');
    process.exit(1);
  }

  const client = new TwitterApi({
    appKey: apiKey,
    appSecret: apiSecret,
    accessToken: accessToken,
    accessSecret: accessSecret,
  });

  try {
    const tweetIds = [];

    for (let i = 0; i < tweets.length; i++) {
      const isLast = i === tweets.length - 1;
      const replyTo = i > 0 ? tweetIds[i - 1] : undefined;

      const tweet = await client.v2.tweet({
        text: tweets[i],
        ...(replyTo && { reply: { in_reply_to_tweet_id: replyTo } }),
      });

      tweetIds.push(tweet.data.id);
      console.log(`Tweet ${i + 1}/${tweets.length} posted:`, tweet.data.id);
    }

    console.log('\nThread posted successfully!');
    console.log('Thread URL:', `https://twitter.com/user/status/${tweetIds[0]}`);
    return tweetIds;
  } catch (error) {
    console.error('Error posting thread:', error.message);
    process.exit(1);
  }
}

// Get tweets from command line arguments
const tweets = process.argv.slice(2);
if (tweets.length === 0) {
  console.error('Usage: node post-thread.js "First tweet" "Second tweet" "Third tweet"');
  console.error('Or pass as JSON: node post-thread.js \'["Tweet 1", "Tweet 2", "Tweet 3"]\'');
  process.exit(1);
}

// Handle JSON array input
let tweetList;
try {
  tweetList = JSON.parse(tweets[0]);
  if (!Array.isArray(tweetList)) throw new Error('Not an array');
} catch {
  tweetList = tweets;
}

postThread(tweetList);
