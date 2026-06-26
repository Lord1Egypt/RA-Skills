/**
 * Skill: Product Hunt Launch Tracker
 * Publisher: @modelfitai
 *
 * Track upvotes, rank, and comments on your Product Hunt launch in real-time.
 * Run this skill hourly during your launch day to get live updates.
 *
 * Commands:
 *   check <url>   — Get current upvotes, rank, and comments
 *   trend <url>   — Get current stats + trend vs last check
 *
 * Example:
 *   node track-upvotes.js check https://www.producthunt.com/posts/your-product
 *   node track-upvotes.js trend https://www.producthunt.com/posts/your-product
 *
 * No API key required.
 */

export async function trackUpvotes(productUrl) {
  try {
    if (!productUrl || !productUrl.includes('producthunt.com')) {
      throw new Error('Invalid Product Hunt URL');
    }

    const response = await fetch(productUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw/1.0)'
      }
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch PH page: ${response.status}`);
    }

    const html = await response.text();

    // Extract upvote count from page
    const upvoteMatch = html.match(/data-test="vote-button"[^>]*>(\d+)/);
    const upvotes = upvoteMatch ? parseInt(upvoteMatch[1], 10) : null;

    // Extract rank if on homepage
    const rankMatch = html.match(/#(\d+)\s+Product of the Day/i);
    const rank = rankMatch ? parseInt(rankMatch[1], 10) : null;

    // Extract comment count
    const commentMatch = html.match(/(\d+)\s+comments?/i);
    const comments = commentMatch ? parseInt(commentMatch[1], 10) : null;

    return {
      success: true,
      data: {
        upvotes,
        rank,
        comments,
        url: productUrl,
        timestamp: new Date().toISOString()
      },
      summary: `📊 PH Update: ${upvotes ?? '?'} upvotes | ${comments ?? '?'} comments | Rank: ${rank ?? 'N/A'}`
    };

  } catch (error) {
    return {
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Track upvotes over time and detect trends
 */
const history = [];

export async function trackUpvoteTrend(productUrl) {
  const current = await trackUpvotes(productUrl);

  if (current.success) {
    history.push(current.data);

    // Keep last 24 entries (24 hours if hourly)
    if (history.length > 24) history.shift();

    const trend = history.length >= 2
      ? current.data.upvotes - history[history.length - 2].upvotes
      : 0;

    const trendEmoji = trend > 10 ? '🚀' : trend > 0 ? '📈' : trend === 0 ? '➡️' : '📉';

    return {
      ...current,
      trend: {
        change: trend,
        emoji: trendEmoji,
        hourlyAvg: Math.round(
          (current.data.upvotes - (history[0]?.upvotes || current.data.upvotes)) / Math.max(history.length - 1, 1)
        ),
        dataPoints: history.length
      },
      summary: `${current.summary} | ${trendEmoji} ${trend >= 0 ? '+' : ''}${trend}/hr`
    };
  }

  return current;
}

// ─── CLI Entrypoint ────────────────────────────────────────────────────────────
import { fileURLToPath } from 'url';
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const [,, cmd, url] = process.argv;

  if (!cmd || !url) {
    console.log('Usage:');
    console.log('  node track-upvotes.js check <producthunt-url>');
    console.log('  node track-upvotes.js trend <producthunt-url>');
    console.log('');
    console.log('Example:');
    console.log('  node track-upvotes.js check https://www.producthunt.com/posts/modelfitai');
    process.exit(0);
  }

  (async () => {
    switch (cmd) {
      case 'check': {
        const result = await trackUpvotes(url);
        if (!result.success) { console.error('Error:', result.error); process.exit(1); }
        console.log(result.summary);
        console.log(`  Upvotes : ${result.data.upvotes ?? 'N/A'}`);
        console.log(`  Rank    : ${result.data.rank ? '#' + result.data.rank : 'Not ranked today'}`);
        console.log(`  Comments: ${result.data.comments ?? 'N/A'}`);
        console.log(`  Checked : ${result.data.timestamp}`);
        break;
      }
      case 'trend': {
        const result = await trackUpvoteTrend(url);
        if (!result.success) { console.error('Error:', result.error); process.exit(1); }
        console.log(result.summary);
        if (result.trend) {
          console.log(`  Change    : ${result.trend.change >= 0 ? '+' : ''}${result.trend.change} since last check`);
          console.log(`  Hourly avg: ${result.trend.hourlyAvg}/hr`);
          console.log(`  Data points: ${result.trend.dataPoints}`);
        }
        break;
      }
      default:
        console.error(`Unknown command: ${cmd}`);
        console.log('Commands: check, trend');
        process.exit(1);
    }
  })();
}
