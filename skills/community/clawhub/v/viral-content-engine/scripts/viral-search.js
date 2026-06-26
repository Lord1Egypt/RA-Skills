#!/usr/bin/env node
/**
 * Viral Content Search — finds trending/high-engagement content on X and Instagram
 * 
 * X/Twitter: Uses bird CLI with --json, filters and sorts by engagement
 * Instagram: Uses Brave Search with viral/popular modifiers
 * 
 * Usage:
 *   node viral-search.js "query" [options]
 * 
 * Options:
 *   --platform x|instagram|both    (default: both)
 *   --min-likes N                  Min likes to include (X only, default: 50)
 *   --min-retweets N               Min retweets (X only, default: 10)
 *   --sort engagement|recent       (default: engagement)
 *   --limit N                      Results per platform (default: 10)
 *   --trending                     Find what's trending right now (X only)
 *   --days N                       Only show content from last N days (default: 7)
 */

const { execSync } = require('child_process');
const path = require('path');

// Parse args
const args = process.argv.slice(2);
let query = '';
let platform = 'both';
let minLikes = 50;
let minRetweets = 10;
let sort = 'engagement';
let limit = 10;
let trending = false;
let days = 7;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--platform' && args[i + 1]) { platform = args[i + 1]; i++; }
  else if (args[i] === '--min-likes' && args[i + 1]) { minLikes = parseInt(args[i + 1]); i++; }
  else if (args[i] === '--min-retweets' && args[i + 1]) { minRetweets = parseInt(args[i + 1]); i++; }
  else if (args[i] === '--sort' && args[i + 1]) { sort = args[i + 1]; i++; }
  else if (args[i] === '--limit' && args[i + 1]) { limit = parseInt(args[i + 1]); i++; }
  else if (args[i] === '--trending') { trending = true; }
  else if (args[i] === '--days' && args[i + 1]) { days = parseInt(args[i + 1]); i++; }
  else if (!args[i].startsWith('--')) { query += (query ? ' ' : '') + args[i]; }
}

if (!query && !trending) {
  console.error('Usage: viral-search.js "query" [--platform x|instagram|both] [--min-likes 50] [--min-retweets 10] [--sort engagement|recent] [--limit 10] [--trending] [--days 7]');
  process.exit(1);
}

// ==================== X/TWITTER SEARCH ====================
function searchX(query, limit, minLikes, minRetweets, sort, days) {
  console.log(`\n🐦 X/Twitter — searching "${query}" (min ${minLikes} likes, ${minRetweets} RTs)\n`);
  
  try {
    // Use bird's advanced search operators for better results
    // min_faves and min_retweets are X search operators
    let searchQuery = query;
    if (minLikes >= 100) {
      searchQuery += ` min_faves:${minLikes}`;
    }
    if (minRetweets >= 50) {
      searchQuery += ` min_retweets:${minRetweets}`;
    }
    
    // Fetch more than needed so we can filter
    const fetchCount = Math.min(limit * 3, 40);
    const raw = execSync(`bird search "${searchQuery.replace(/"/g, '\\"')}" -n ${fetchCount} --json`, {
      encoding: 'utf8',
      timeout: 30000,
      stdio: ['pipe', 'pipe', 'pipe'],
    });

    let tweets = JSON.parse(raw);
    
    // Filter by date
    const cutoff = Date.now() - (days * 24 * 60 * 60 * 1000);
    tweets = tweets.filter(t => {
      const created = new Date(t.createdAt).getTime();
      return created >= cutoff;
    });

    // Filter by engagement
    tweets = tweets.filter(t => {
      return (t.likeCount || 0) >= minLikes || (t.retweetCount || 0) >= minRetweets;
    });

    // Sort
    if (sort === 'engagement') {
      tweets.sort((a, b) => {
        const scoreA = (a.likeCount || 0) * 1 + (a.retweetCount || 0) * 3 + (a.replyCount || 0) * 2;
        const scoreB = (b.likeCount || 0) * 1 + (b.retweetCount || 0) * 3 + (b.replyCount || 0) * 2;
        return scoreB - scoreA;
      });
    }

    // Trim to limit
    tweets = tweets.slice(0, limit);

    if (tweets.length === 0) {
      console.log(`  No viral tweets found. Try lowering --min-likes or --min-retweets.\n`);
      return;
    }

    tweets.forEach((t, i) => {
      const engagement = `❤️ ${t.likeCount || 0} | 🔄 ${t.retweetCount || 0} | 💬 ${t.replyCount || 0}`;
      const score = (t.likeCount || 0) + (t.retweetCount || 0) * 3 + (t.replyCount || 0) * 2;
      const date = new Date(t.createdAt).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
      
      console.log(`${i + 1}. @${t.author?.username || 'unknown'} (${date}) — Score: ${score}`);
      console.log(`   ${engagement}`);
      console.log(`   ${t.text?.substring(0, 200).replace(/\n/g, ' ')}`);
      console.log(`   🔗 https://x.com/${t.author?.username}/status/${t.id}`);
      console.log();
    });

    console.log(`--- ${tweets.length} viral tweets found ---\n`);
  } catch (e) {
    console.error(`  ❌ X search failed: ${e.message}\n`);
  }
}

// ==================== INSTAGRAM SEARCH ====================
function searchInstagram(query, limit) {
  console.log(`\n📸 Instagram — searching "${query}" (viral/popular)\n`);
  
  const scriptDir = path.dirname(process.argv[1]);
  
  try {
    // Use viral modifiers in Brave search
    const viralQueries = [
      `site:instagram.com "${query}" viral popular`,
      `site:instagram.com "${query}" trending`,
    ];
    
    const raw = execSync(
      `node "${path.join(scriptDir, 'instagram-search.js')}" "${query} viral popular trending" --limit ${limit}`,
      { encoding: 'utf8', timeout: 15000, stdio: ['pipe', 'pipe', 'pipe'] }
    );
    
    console.log(raw);
  } catch (e) {
    // Fallback to regular search with popular modifier
    try {
      const raw = execSync(
        `node "${path.join(scriptDir, 'instagram-search.js')}" "${query} popular" --limit ${limit}`,
        { encoding: 'utf8', timeout: 15000, stdio: ['pipe', 'pipe', 'pipe'] }
      );
      console.log(raw);
    } catch (e2) {
      console.error(`  ❌ Instagram search failed: ${e2.message}\n`);
    }
  }
}

// ==================== TRENDING MODE ====================
function searchTrending() {
  console.log(`\n🔥 TRENDING on X right now\n`);
  
  // Search for high-engagement recent content across crypto/defi/ai
  const trendQueries = [
    'crypto min_faves:1000',
    'DeFi min_faves:500',
    'AI trading min_faves:500',
  ];
  
  let allTweets = [];
  
  for (const q of trendQueries) {
    try {
      const raw = execSync(`bird search "${q}" -n 5 --json`, {
        encoding: 'utf8', timeout: 20000, stdio: ['pipe', 'pipe', 'pipe'],
      });
      const tweets = JSON.parse(raw);
      allTweets = allTweets.concat(tweets);
    } catch (e) {}
  }
  
  // Dedupe by ID
  const seen = new Set();
  allTweets = allTweets.filter(t => {
    if (seen.has(t.id)) return false;
    seen.add(t.id);
    return true;
  });
  
  // Sort by engagement
  allTweets.sort((a, b) => {
    const scoreA = (a.likeCount || 0) + (a.retweetCount || 0) * 3;
    const scoreB = (b.likeCount || 0) + (b.retweetCount || 0) * 3;
    return scoreB - scoreA;
  });
  
  allTweets.slice(0, 10).forEach((t, i) => {
    const engagement = `❤️ ${t.likeCount || 0} | 🔄 ${t.retweetCount || 0} | 💬 ${t.replyCount || 0}`;
    console.log(`${i + 1}. @${t.author?.username || '?'} — ${engagement}`);
    console.log(`   ${t.text?.substring(0, 200).replace(/\n/g, ' ')}`);
    console.log(`   🔗 https://x.com/${t.author?.username}/status/${t.id}\n`);
  });
}

// ==================== RUN ====================
if (trending) {
  searchTrending();
}

if (query) {
  if (platform === 'x' || platform === 'both') {
    searchX(query, limit, minLikes, minRetweets, sort, days);
  }
  if (platform === 'instagram' || platform === 'both') {
    searchInstagram(query, limit);
  }
}
