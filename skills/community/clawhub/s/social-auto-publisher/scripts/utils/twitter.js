/**
 * Twitter API v2 Publishing Module
 * Requires environment variables: TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
 */

const TWITTER_API_BASE = 'https://api.twitter.com/2';
const MAX_TWEET_LENGTH = 280;

/**
 * Format tweet content
 */
function formatContent(content) {
  let text = content.title ? `${content.title}\n${content.body}` : content.body;
  if (text.length > MAX_TWEET_LENGTH) {
    text = text.slice(0, MAX_TWEET_LENGTH - 3) + '...';
  }
  const hashtags = (content.tags || [])
    .map(t => `#${t.replace(/[^a-zA-Z0-9\u4e00-\u9fff]/g, '')}`)
    .join(' ');
  const fullText = `${text} ${hashtags}`.trim();
  return fullText.slice(0, MAX_TWEET_LENGTH);
}

/**
 * Build a tweet thread (split long content into multiple tweets)
 */
function buildThread(content) {
  const body = content.body || '';
  const title = content.title || '';
  const tags = (content.tags || [])
    .map(t => `#${t.replace(/[^a-zA-Z0-9\u4e00-\u9fff]/g, '')}`)
    .join(' ');

  const baseText = title ? `${title}\n\n${body}` : body;
  const tagSuffix = `\n\n${tags}`;
  const availableForContent = MAX_TWEET_LENGTH - tagSuffix.length;

  if (baseText.length <= MAX_TWEET_LENGTH) {
    return [{ text: `${baseText}${tags ? tagSuffix : ''}`.trim().slice(0, MAX_TWEET_LENGTH) }];
  }

  // Split long content
  const tweets = [];
  let remaining = baseText;
  let index = 1;

  while (remaining.length > 0) {
    const maxLen = index === 1 ? MAX_TWEET_LENGTH : availableForContent;
    if (remaining.length <= maxLen) {
      tweets.push({
        text: index === 1 ? remaining.slice(0, MAX_TWEET_LENGTH) : `${remaining}${tagSuffix}`,
      });
      break;
    }
    // Find a break point within maxLen
    let cut = remaining.lastIndexOf('\n', maxLen);
    if (cut < maxLen / 2) cut = remaining.lastIndexOf('.', maxLen);
    if (cut < maxLen / 2) cut = maxLen;

    tweets.push({ text: remaining.slice(0, cut).trim() });
    remaining = remaining.slice(cut).trim();
    index++;
  }

  return tweets;
}

module.exports = { formatContent, buildThread, MAX_TWEET_LENGTH };