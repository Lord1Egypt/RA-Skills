/**
 * Skill: X/Twitter Lead Generation
 * Template: lead-gen-x-twitter
 * 
 * Monitor keywords, score X prospects, generate DM sequences,
 * draft threads, and track engagement metrics.
 * Uses Brave Search API (site:x.com) to find keyword mentions — no X API credentials needed.
 */
import https from 'https';

/**
 * Generate an engagement-first DM outreach sequence for an X prospect
 * @param {object} prospect - X prospect details
 */
export async function generateXOutreach(prospect) {
  try {
    if (!prospect || !prospect.handle) {
      throw new Error('Prospect X handle is required');
    }

    const { handle, name, bio, recentTweet, followerCount, icpMatch } = prospect;
    const displayName = name || handle;

    const sequence = [
      {
        phase: 'warm-up',
        days: '1-3',
        actions: [
          { type: 'like', description: `Like 3-5 recent tweets from @${handle}` },
          { type: 'reply', description: `Reply to their tweet: "${recentTweet?.slice(0, 50) || '[their best recent tweet]'}..." with a genuine, insightful take` },
          { type: 'quote-tweet', description: `Quote-tweet one of their posts adding your own insight or data point` },
        ],
        goal: 'Get on their radar — NO DMs yet',
      },
      {
        phase: 'dm-1',
        day: 'Day 4',
        type: 'curiosity-dm',
        template: `Hey ${displayName}, been enjoying your takes on ${bio ? bio.split(' ').slice(0, 5).join(' ') : '[their topic]'}. Quick Q — how are you currently handling [pain point]? Curious what's working for you.`,
        maxLength: 280,
        tip: 'Ask a genuine question — make it about THEM, not you',
      },
      {
        phase: 'dm-2',
        day: 'Day 6',
        type: 'value-dm',
        template: `Btw, we built something that does exactly [solution]. Not pitching — just thought you'd find it interesting given your work on [topic]. Here's a [free resource/demo]: [link]`,
        maxLength: 280,
        tip: 'Lead with free value — resource, tool, guide. No hard sell.',
      },
      {
        phase: 'dm-3',
        day: 'Day 7',
        type: 'soft-close',
        template: `Hey ${displayName}, a few ${bio?.includes('founder') ? 'founders' : 'folks'} like you have been loving [specific feature]. Want me to set up a quick walkthrough? No pressure either way 🙌`,
        maxLength: 280,
        tip: 'Only send if they engaged with DM 1 or 2. Otherwise, keep warming.',
        condition: 'ONLY if replied to DM 1 or DM 2',
      },
    ];

    return {
      success: true,
      data: {
        prospect: { handle, name, bio: bio?.slice(0, 100), followerCount },
        icpMatch,
        sequence,
        timestamp: new Date().toISOString(),
      },
      summary: `🐦 Generated X outreach sequence for @${handle} (${displayName})`,
    };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Score an X/Twitter prospect based on engagement signals and ICP fit
 * @param {object} prospect - X prospect data
 */
export function scoreXProspect(prospect) {
  let score = 0;
  const reasons = [];

  // Engagement signals
  if (prospect.repliedToYou) {
    score += 25;
    reasons.push('Replied to your tweet/thread');
  }

  if (prospect.likedMultiple && prospect.likedMultiple >= 3) {
    score += 15;
    reasons.push(`Liked ${prospect.likedMultiple}+ of your tweets`);
  }

  if (prospect.followedBack) {
    score += 20;
    reasons.push('Followed you back');
  }

  // ICP fit
  if (prospect.bioMatchesICP) {
    score += 20;
    reasons.push('Bio matches ICP keywords');
  }

  if (prospect.followerCount >= 1000) {
    score += 10;
    reasons.push(`${prospect.followerCount.toLocaleString()} followers (has influence)`);
  }

  // DM engagement
  if (prospect.repliedToDM) {
    score += 30;
    reasons.push('Replied to DM');
  }

  if (prospect.clickedLink) {
    score += 35;
    reasons.push('Clicked link in DM');
  }

  // Intent signals
  if (prospect.postedPainPoint) {
    score += 25;
    reasons.push('Posted about a problem you solve');
  }

  if (prospect.engagedWithCompetitor) {
    score += 15;
    reasons.push('Engaged with competitor content');
  }

  let tier;
  if (score >= 70) tier = '🔥 HOT';
  else if (score >= 40) tier = '🟡 WARM';
  else tier = '🔵 COLD';

  return {
    score,
    maxScore: 195,
    tier,
    reasons,
    nextAction:
      score >= 70
        ? 'Move to DM Phase 2 immediately'
        : score >= 40
          ? 'Continue engagement-first warming (likes + replies)'
          : 'Add to thread/content nurture list',
    summary: `${tier} X Prospect: @${prospect.handle || 'unknown'} — Score: ${score}/195`,
  };
}

/**
 * Generate a lead-magnet thread for X/Twitter
 * @param {object} config - Thread configuration
 */
export function generateThread(config) {
  const { topic, hook, steps, socialProof, cta, leadMagnet } = config;

  if (!topic || !hook) {
    return { success: false, error: 'Topic and hook are required' };
  }

  const tweets = [];

  // Tweet 1 — Hook
  tweets.push({
    position: 1,
    type: 'hook',
    content: `${hook}\n\n🧵 Thread:`,
    tip: 'Contrarian take, surprising stat, or bold claim. Must stop the scroll.',
    charCount: hook.length + 11,
  });

  // Tweets 2-N — Value steps
  const valueSteps = steps || [
    'Step 1: [First actionable insight]',
    'Step 2: [Framework or process]',
    'Step 3: [Common mistake to avoid]',
    'Step 4: [Advanced tip]',
    'Step 5: [Real numbers or screenshot]',
  ];

  valueSteps.forEach((step, i) => {
    tweets.push({
      position: i + 2,
      type: 'value',
      content: step,
      tip: '1 idea per tweet. Use line breaks. Numbers > words.',
      charCount: step.length,
    });
  });

  // Social proof tweet
  if (socialProof) {
    tweets.push({
      position: tweets.length + 1,
      type: 'social-proof',
      content: `This is exactly how ${socialProof}`,
      charCount: socialProof.length + 22,
    });
  }

  // CTA tweet
  tweets.push({
    position: tweets.length + 1,
    type: 'cta',
    content: cta || `Want the full playbook?\n\n${leadMagnet ? `Grab it here → ${leadMagnet}` : 'Drop a 🔥 and I\'ll DM it to you'}\n\nFollow @[handle] for more threads like this.`,
    tip: 'Soft CTA. Offer free value. Ask for follow + RT.',
  });

  return {
    success: true,
    data: {
      topic,
      tweetCount: tweets.length,
      tweets,
      estimatedReadTime: `${Math.ceil(tweets.length * 0.5)} min`,
      bestPostingTimes: ['8:00 AM', '12:00 PM', '5:30 PM'],
    },
    summary: `🧵 Generated ${tweets.length}-tweet thread on "${topic}"`,
  };
}

/**
 * Analyze keyword matches from X monitoring
 * @param {object} tweet - Tweet data from monitoring
 */
export function analyzeKeywordMatch(tweet) {
  const { text, author, authorBio, authorFollowers, keyword, timestamp } = tweet;

  if (!text || !keyword) {
    return { success: false, error: 'Tweet text and matched keyword are required' };
  }

  // Determine intent level
  const highIntentPhrases = ['need a tool', 'looking for', 'any recommendations', 'switching from', 'alternative to', 'frustrated with', 'hate using'];
  const mediumIntentPhrases = ['thinking about', 'considering', 'has anyone tried', 'what do you use', 'opinions on'];
  
  let intentLevel = 'low';
  const lowerText = text.toLowerCase();
  
  if (highIntentPhrases.some(p => lowerText.includes(p))) {
    intentLevel = 'high';
  } else if (mediumIntentPhrases.some(p => lowerText.includes(p))) {
    intentLevel = 'medium';
  }

  // Suggest action
  let suggestedAction;
  if (intentLevel === 'high') {
    suggestedAction = {
      type: 'reply-with-value',
      template: `Great question! I've been working on exactly this. Here's what I've found works: [insight]. We actually built [product] to solve this — happy to share more if useful.`,
      urgency: 'Reply within 1 hour for best engagement',
    };
  } else if (intentLevel === 'medium') {
    suggestedAction = {
      type: 'reply-helpful',
      template: `Interesting thread! A few things to consider: [genuine advice]. I've seen [data point] work well for this. DM me if you want more details.`,
      urgency: 'Reply within 4 hours',
    };
  } else {
    suggestedAction = {
      type: 'monitor',
      template: null,
      urgency: 'Add to watch list — engage with their content this week',
    };
  }

  return {
    success: true,
    data: {
      tweet: { text: text.slice(0, 280), author, authorFollowers },
      matchedKeyword: keyword,
      intentLevel,
      suggestedAction,
      icpSignals: {
        bioMatch: authorBio ? 'Check bio against ICP keywords' : 'No bio available',
        influence: authorFollowers >= 1000 ? 'High' : authorFollowers >= 200 ? 'Medium' : 'Low',
      },
    },
    summary: `🎯 ${intentLevel.toUpperCase()} intent match: @${author || 'unknown'} — keyword: "${keyword}"`,
  };
}

// =============================================
// BRAVE SEARCH HELPER
// =============================================

/**
 * Search X/Twitter via Brave Search API (site:x.com)
 * @param {string} keyword - Search query
 * @param {number} count - Number of results (max 20)
 */
export function searchXViaBrave(keyword, count = 10) {
  return new Promise((resolve, reject) => {
    const apiKey = process.env.BRAVE_API_KEY;
    if (!apiKey) {
      return resolve({ success: false, error: 'BRAVE_API_KEY not set. Add it in your agent deploy settings.' });
    }

    const query = encodeURIComponent(`site:x.com ${keyword}`);
    const options = {
      hostname: 'api.search.brave.com',
      path: `/res/v1/web/search?q=${query}&count=${count}`,
      headers: {
        'Accept': 'application/json',
        'X-Subscription-Token': apiKey,
      },
    };

    const req = https.get(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const results = (json.web?.results || []).map(r => ({
            url: r.url,
            title: r.title,
            description: r.description,
            // Extract handle from x.com URL: x.com/handle/status/...
            handle: r.url.match(/x\.com\/([^/]+)/)?.[1] || null,
          }));

          const scored = results.map(r => {
            const text = `${r.title} ${r.description}`;
            const analysis = analyzeKeywordMatch({ text, author: r.handle, keyword });
            return { ...r, intentLevel: analysis.data?.intentLevel || 'low', suggestedAction: analysis.data?.suggestedAction };
          }).sort((a, b) => {
            const rank = { high: 3, medium: 2, low: 1 };
            return (rank[b.intentLevel] || 0) - (rank[a.intentLevel] || 0);
          });

          resolve({
            success: true,
            keyword,
            count: scored.length,
            results: scored,
            summary: `🔍 Found ${scored.length} X posts for "${keyword}" — ${scored.filter(r => r.intentLevel === 'high').length} high-intent`,
          });
        } catch (e) {
          resolve({ success: false, error: `Parse error: ${e.message}` });
        }
      });
    });

    req.on('error', e => resolve({ success: false, error: e.message }));
    req.end();
  });
}

// =============================================
// CLI ENTRY POINT
// =============================================
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
if (path.resolve(process.argv[1]) === path.resolve(__filename)) {
  const [,, cmd, ...rest] = process.argv;

  const parseArgs = (args) => {
    const result = { _: [] };
    for (let i = 0; i < args.length; i++) {
      if (args[i].startsWith('--')) {
        const key = args[i].slice(2);
        result[key] = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
      } else {
        result._.push(args[i]);
      }
    }
    return result;
  };

  (async () => {
    switch (cmd) {
      case 'search': {
        const keyword = rest.join(' ');
        if (!keyword) { console.error('Usage: search <keyword>'); process.exit(1); }
        const result = await searchXViaBrave(keyword);
        if (!result.success) { console.error(result.error); process.exit(1); }
        console.log(`\n${result.summary}\n`);
        result.results.forEach((r, i) => {
          const icon = r.intentLevel === 'high' ? '🔴' : r.intentLevel === 'medium' ? '🟡' : '⚪';
          console.log(`${icon} ${i + 1}. @${r.handle || 'unknown'}`);
          console.log(`   ${r.title}`);
          console.log(`   ${r.description?.slice(0, 120) || ''}`);
          console.log(`   ${r.url}\n`);
        });
        break;
      }
      case 'score': {
        const args = parseArgs(rest);
        const result = scoreXProspect({
          handle: args.handle,
          bioMatchesICP: !!args.bio,
          followerCount: parseInt(args.followers || '0'),
          postedPainPoint: !!(args.tweet && ['frustrated', 'looking for', 'need', 'alternative'].some(p => args.tweet.toLowerCase().includes(p))),
        });
        console.log(result.summary);
        console.log('Reasons:', result.reasons.join(', '));
        console.log('Next action:', result.nextAction);
        break;
      }
      case 'dm-sequence': {
        const args = parseArgs(rest);
        if (!args.handle) { console.error('Usage: dm-sequence --handle "@username" [--name "Name"]'); process.exit(1); }
        const result = await generateXOutreach({ handle: args.handle, name: args.name });
        if (!result.success) { console.error(result.error); process.exit(1); }
        console.log(`\n${result.summary}\n`);
        result.data.sequence.forEach(step => {
          console.log(`--- ${step.phase} (${step.day || step.days}) ---`);
          if (step.template) console.log(step.template);
          if (step.actions) step.actions.forEach(a => console.log(`  • ${a.description}`));
          console.log();
        });
        break;
      }
      default:
        console.log('Commands: search <keyword>, score --handle "@x", dm-sequence --handle "@x" --name "Name"');
    }
  })();
}
