/**
 * Weibo API Publishing Module
 * Publish via the Weibo Open Platform API or Cookie method
 */

const WEIBO_API_BASE = 'https://api.weibo.com/2';

/**
 * Format Weibo content (140 character limit)
 */
function formatContent(content) {
  const maxLen = 140;
  let text = content.title ? `${content.title}\n\n${content.body}` : content.body;
  if (text.length > maxLen) {
    text = text.slice(0, maxLen - 3) + '...';
  }
  // Append tags
  const tags = (content.tags || []).map(t => `#${t.replace(/^#/, '')}#`).join(' ');
  const fullText = `${text} ${tags}`.trim();
  return fullText.slice(0, maxLen);
}

/**
 * Publish Weibo via API
 */
async function publishViaApi(content, credentials) {
  const { appKey, accessToken } = credentials;
  const status = formatContent(content);

  const params = new URLSearchParams({
    access_token: accessToken,
    status,
  });

  // If there is an image
  if (content.imageUrl) {
    params.append('pic', content.imageUrl);
  }

  const url = `${WEIBO_API_BASE}/statuses/update.json?${params}`;
  // The actual request is handled by the caller
  return { method: 'POST', url, params: { status, image: content.imageUrl || null } };
}

/**
 * Publish Weibo via Cookie method (browser emulation)
 */
function buildBrowserCommands(content) {
  const status = formatContent(content);
  return [
    { step: 1, action: 'navigate', command: 'browser navigate https://weibo.com' },
    { step: 2, action: 'screenshot', command: 'browser screenshot', description: 'Check login status' },
    { step: 3, action: 'click', command: 'browser act ref=<weibo-post-input> kind=click' },
    { step: 4, action: 'type', command: `browser act ref=<weibo-content-input-area> kind=type text="${status}"` },
    { step: 5, action: 'click', command: 'browser act ref=<publish-button> kind=click' },
  ];
}

module.exports = { formatContent, publishViaApi, buildBrowserCommands };