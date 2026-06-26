/**
 * Skill: Reddit Lead Generation & Community Engagement
 * Template: lead-gen-reddit
 *
 * Find buying-intent posts on Reddit via Brave Search (site:reddit.com) —
 * no Reddit OAuth credentials needed. Score prospects, generate value-first
 * comments, draft content posts, and track karma + lead attribution.
 *
 * Required env vars:
 *   BRAVE_API_KEY  — Brave Search API key (free tier: 2,000 queries/month)
 *                    Sign up at: api.search.brave.com
 */
import https from 'https';

/**
 * Analyze a Reddit post for lead generation opportunity
 * @param {object} post - Reddit post data
 */
export function analyzeRedditPost(post) {
  const { title, body, subreddit, author, upvotes, commentCount, flair } = post;

  if (!title) {
    return { success: false, error: 'Post title is required' };
  }

  const fullText = `${title} ${body || ''}`.toLowerCase();

  // Intent detection
  const highIntent = [
    'what tool', 'which tool', 'looking for', 'need help with',
    'any recommendations', 'best way to', 'alternative to',
    'switching from', 'frustrated with', 'hate using',
    'has anyone tried', 'worth paying for',
  ];
  const mediumIntent = [
    'thinking about', 'considering', 'opinions on', 'what do you use',
    'how do you handle', 'workflow for', 'setup for',
  ];

  let intentLevel = 'low';
  let matchedPhrase = null;

  for (const phrase of highIntent) {
    if (fullText.includes(phrase)) {
      intentLevel = 'high';
      matchedPhrase = phrase;
      break;
    }
  }
  if (intentLevel === 'low') {
    for (const phrase of mediumIntent) {
      if (fullText.includes(phrase)) {
        intentLevel = 'medium';
        matchedPhrase = phrase;
        break;
      }
    }
  }

  // Engagement potential
  const isNew = (upvotes || 0) < 10 && (commentCount || 0) < 5;
  const isTrending = (upvotes || 0) >= 50;

  let responseUrgency;
  if (intentLevel === 'high' && isNew) {
    responseUrgency = '🔴 Respond within 1 hour (high-intent, low competition)';
  } else if (intentLevel === 'high') {
    responseUrgency = '🟡 Respond within 4 hours (high-intent, competitive)';
  } else if (intentLevel === 'medium') {
    responseUrgency = '🟢 Respond within 12 hours';
  } else {
    responseUrgency = '⚪ Monitor — respond only if you have genuine value to add';
  }

  return {
    success: true,
    data: {
      post: { title, subreddit, author, upvotes, commentCount },
      analysis: {
        intentLevel,
        matchedPhrase,
        isNew,
        isTrending,
        responseUrgency,
      },
      suggestedApproach: intentLevel === 'high'
        ? 'Lead with 2-3 paragraphs of genuine help → mention alternatives → naturally include your product (with disclosure)'
        : intentLevel === 'medium'
          ? 'Share personal experience or data → be helpful → only mention product if directly relevant'
          : 'Provide helpful comment → build karma → no product mention',
    },
    summary: `📊 r/${subreddit || 'unknown'}: ${intentLevel.toUpperCase()} intent — "${matchedPhrase || 'no keyword match'}"`,
  };
}

/**
 * Generate a value-first comment for a Reddit post
 * @param {object} config - Comment configuration
 */
export function generateRedditComment(config) {
  const { postTitle, postBody, subreddit, authorPainPoint, includeProductMention, productName, productDescription } = config;

  if (!postTitle) {
    return { success: false, error: 'Post title is required' };
  }

  const sections = [];

  // Section 1: Empathy / relate to the problem
  sections.push({
    part: 'opener',
    content: `[Empathize with the poster's situation — reference their specific problem]\n\nExample: "I dealt with this exact issue when I was [relevant experience]. Here's what worked for me:"`,
    tip: 'Show you understand their pain BEFORE offering solutions',
  });

  // Section 2: Genuine advice (2-3 paragraphs)
  sections.push({
    part: 'value',
    content: `[2-3 paragraphs of actionable advice]\n\n1. [First recommendation with reasoning]\n2. [Second recommendation — can include competitors/alternatives]\n3. [Third tip — something non-obvious that shows expertise]`,
    tip: 'This should be useful even if the reader never uses your product',
  });

  // Section 3: Product mention (only if flagged)
  if (includeProductMention && productName) {
    sections.push({
      part: 'product-mention',
      content: `Another option worth looking at is ${productName} — ${productDescription || '[what it does specifically for their use case]'}. Full disclosure: I work on this, so I'm biased, but happy to answer any questions about it or the other tools I mentioned.`,
      tip: 'Always disclose. Always list alternatives too. Never make it ONLY about your product.',
    });
  }

  // Section 4: Closing
  sections.push({
    part: 'closing',
    content: `Happy to go deeper on any of this — I've been doing [relevant thing] for [X time] so feel free to ask follow-ups.`,
    tip: 'Invite conversation. Redditors love people who stick around in the thread.',
  });

  return {
    success: true,
    data: {
      targetPost: postTitle,
      subreddit,
      sections,
      includesProductMention: !!includeProductMention,
      estimatedLength: includeProductMention ? '200-300 words' : '150-250 words',
    },
    summary: `💬 Generated comment structure for r/${subreddit || 'unknown'} ${includeProductMention ? '(with product mention)' : '(value-only)'}`,
  };
}

/**
 * Score a Reddit user as a potential lead
 * @param {object} prospect - Reddit user data
 */
export function scoreRedditProspect(prospect) {
  let score = 0;
  const reasons = [];

  // High-intent signals
  if (prospect.askedForRecommendations) {
    score += 30;
    reasons.push('Asked for product recommendations');
  }

  if (prospect.complainedAboutCompetitor) {
    score += 25;
    reasons.push('Complained about a competitor');
  }

  // Engagement with you
  if (prospect.repliedToYourComment) {
    score += 35;
    reasons.push('Replied to your comment asking for details');
  }

  if (prospect.dmedYou) {
    score += 40;
    reasons.push('DMed you after your comment');
  }

  if (prospect.upvotedProductMention) {
    score += 15;
    reasons.push('Upvoted your product mention');
  }

  // Activity signals
  if (prospect.activeInTargetSubreddits) {
    score += 10;
    reasons.push('Active in target subreddits');
  }

  if (prospect.isMod) {
    score += 20;
    reasons.push('Moderator of a target subreddit (high influence)');
  }

  // Language signals
  if (prospect.usedBuyingLanguage) {
    score += 25;
    reasons.push('Used "looking for" / "need" / "willing to pay" language');
  }

  // Influence
  if (prospect.karma >= 10000) {
    score += 10;
    reasons.push('High-karma user (potential advocate)');
  }

  let tier;
  if (score >= 70) tier = '🔥 HOT';
  else if (score >= 40) tier = '🟡 WARM';
  else tier = '🔵 COLD';

  return {
    score,
    maxScore: 210,
    tier,
    reasons,
    nextAction:
      score >= 70
        ? 'Reply with detailed help + natural product mention. DM only if they invited it.'
        : score >= 40
          ? 'Comment helpfully, monitor for future interactions'
          : 'Note for content targeting, build karma in their subreddits',
    summary: `${tier} Reddit Prospect: u/${prospect.username || 'unknown'} — Score: ${score}/210`,
  };
}

/**
 * Generate a content post for Reddit (case study, resource, AMA)
 * @param {object} config - Post configuration
 */
export function generateRedditPost(config) {
  const { type, subreddit, topic, data, productName } = config;

  if (!type || !topic) {
    return { success: false, error: 'Post type and topic are required' };
  }

  const templates = {
    'case-study': {
      titleFormat: `How I ${topic} — breakdown & real numbers inside`,
      structure: [
        { section: 'TL;DR', content: '2-3 sentence summary with the key result' },
        { section: 'Background', content: 'What was the situation/problem (2 paragraphs)' },
        { section: 'What I tried', content: 'Previous approaches that failed and why' },
        { section: 'What worked', content: 'The approach/process that got results (this is the meat — 3-4 paragraphs)' },
        { section: 'Numbers', content: 'Actual metrics, screenshots, data (Redditors love numbers)' },
        { section: 'Lessons learned', content: '3-5 takeaways others can apply' },
        { section: 'Tools used', content: `List of tools (including ${productName || 'yours'} naturally among others). Always include free alternatives.` },
        { section: 'Questions', content: '"Happy to answer any questions about the process. AMA in the comments."' },
      ],
    },
    'resource': {
      titleFormat: `[Free] ${topic} — no signup required`,
      structure: [
        { section: 'What it is', content: 'Clear description of the resource' },
        { section: 'Who it\'s for', content: 'Specific audience (the more specific, the more upvotes)' },
        { section: 'Direct link', content: 'No landing page, no email gate — direct access' },
        { section: 'Why I made it', content: 'Personal story / motivation' },
        { section: 'Feedback welcome', content: '"Made this based on [experience]. Would love feedback on what to add."' },
      ],
    },
    'ama': {
      titleFormat: `I'm [role] who ${topic}. AMA`,
      structure: [
        { section: 'Intro', content: 'Who you are, credentials, what you\'ve done (keep humble)' },
        { section: 'Context', content: 'What you\'re working on now and why you\'re doing this AMA' },
        { section: 'Proof', content: 'Link to verify identity (website, LinkedIn, etc.)' },
        { section: 'Topics', content: '"Happy to talk about: [topic 1], [topic 2], [topic 3]"' },
        { section: 'Time', content: '"I\'ll be answering for the next [X hours]. Let\'s go!"' },
      ],
    },
  };

  const template = templates[type];
  if (!template) {
    return { success: false, error: `Unknown post type: ${type}. Use: case-study, resource, ama` };
  }

  return {
    success: true,
    data: {
      type,
      subreddit,
      suggestedTitle: template.titleFormat,
      structure: template.structure,
      bestPostingTimes: {
        weekday: '9-11 AM EST (before lunch)',
        weekend: '10 AM - 12 PM EST',
        avoid: 'Friday evening, Saturday night',
      },
      tips: [
        'Check subreddit rules before posting — some require specific flairs or formats',
        'Reply to EVERY comment in the first 2 hours (boosts visibility)',
        'If post gets traction, edit to add a "EDIT: answering common questions" section',
        'Cross-post to related subreddits (but wait 24 hours)',
      ],
    },
    summary: `📝 Generated ${type} post template for r/${subreddit || '[subreddit]'}: "${template.titleFormat}"`,
  };
}

// =============================================
// BRAVE SEARCH HELPER
// =============================================

/**
 * Search Reddit via Brave Search API (site:reddit.com) — no Reddit credentials needed
 * @param {string} keyword - Search query
 * @param {string} subreddit - Optional subreddit to scope the search (e.g. 'startups')
 * @param {number} count - Number of results (max 20)
 */
export function searchRedditViaBrave(keyword, subreddit = null, count = 10) {
  return new Promise((resolve) => {
    const apiKey = process.env.BRAVE_API_KEY;
    if (!apiKey) {
      return resolve({ success: false, error: 'BRAVE_API_KEY not set. Add it in your agent deploy settings.' });
    }

    const base = subreddit
      ? `site:reddit.com/r/${subreddit} ${keyword}`
      : `site:reddit.com ${keyword}`;
    const query = encodeURIComponent(base);

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
          const results = (json.web?.results || []).map(r => {
            // Extract subreddit and post slug from URL: reddit.com/r/<sub>/comments/<id>/<slug>
            const subMatch = r.url.match(/reddit\.com\/r\/([^/]+)/);
            const isComment = r.url.includes('/comments/');
            return {
              url: r.url,
              title: r.title,
              snippet: r.description,
              subreddit: subMatch?.[1] || null,
              isComment,
            };
          });

          const scored = results.map(r => {
            const text = `${r.title} ${r.snippet || ''}`;
            const analysis = analyzeRedditPost({ title: r.title, body: r.snippet, subreddit: r.subreddit });
            return { ...r, intentLevel: analysis.data?.analysis?.intentLevel || 'low', responseUrgency: analysis.data?.analysis?.responseUrgency };
          }).sort((a, b) => {
            const rank = { high: 3, medium: 2, low: 1 };
            return (rank[b.intentLevel] || 0) - (rank[a.intentLevel] || 0);
          });

          resolve({
            success: true,
            keyword,
            subreddit: subreddit || 'all',
            count: scored.length,
            results: scored,
            summary: `🔍 Found ${scored.length} Reddit posts for "${keyword}" — ${scored.filter(r => r.intentLevel === 'high').length} high-intent`,
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

/**
 * Track karma and engagement metrics for a Reddit account
 * @param {object} metrics - Current Reddit metrics
 */
export function trackRedditMetrics(metrics) {
  const {
    commentsThisWeek = 0,
    karmaEarned = 0,
    postsCreated = 0,
    postUpvotes = 0,
    productMentions = 0,
    dmsSent = 0,
    dmReplies = 0,
    inboundInquiries = 0,
    signUps = 0,
  } = metrics;

  const targets = {
    commentsThisWeek: { target: 30, unit: 'comments' },
    karmaEarned: { target: 200, unit: 'karma' },
    postsCreated: { target: 2, unit: 'posts' },
    postUpvotes: { target: 50, unit: 'avg upvotes' },
    productMentions: { target: 4, unit: 'mentions' },
    dmsSent: { target: 7, unit: 'DMs' },
    dmReplies: { target: 3, unit: 'replies' },
    inboundInquiries: { target: 10, unit: 'inquiries' },
    signUps: { target: 5, unit: 'sign-ups' },
  };

  const report = Object.entries(targets).map(([key, { target, unit }]) => {
    const actual = metrics[key] || 0;
    const percentage = Math.round((actual / target) * 100);
    const status = percentage >= 100 ? '✅' : percentage >= 60 ? '🟡' : '🔴';
    return { metric: key, actual, target, percentage, status, unit };
  });

  const overallHealth = report.filter(r => r.percentage >= 100).length;
  let grade;
  if (overallHealth >= 7) grade = 'A — Excellent Reddit lead gen performance';
  else if (overallHealth >= 5) grade = 'B — Good, but room to improve';
  else if (overallHealth >= 3) grade = 'C — Needs more engagement';
  else grade = 'D — Ramp up activity significantly';

  return {
    success: true,
    data: {
      report,
      grade,
      dmReplyRate: dmsSent > 0 ? `${Math.round((dmReplies / dmsSent) * 100)}%` : 'N/A',
      mentionToSignupRate: productMentions > 0 ? `${Math.round((signUps / productMentions) * 100)}%` : 'N/A',
    },
    summary: `📊 Reddit Weekly: Grade ${grade.charAt(0)} | ${karmaEarned} karma | ${inboundInquiries} inquiries | ${signUps} sign-ups`,
  };
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
        const args = parseArgs(rest);
        const keyword = args._.join(' ') || args.keyword;
        if (!keyword) { console.error('Usage: search <keyword> [--subreddit startups]'); process.exit(1); }
        const result = await searchRedditViaBrave(keyword, args.subreddit || null);
        if (!result.success) { console.error(result.error); process.exit(1); }
        console.log(`\n${result.summary}\n`);
        result.results.forEach((r, i) => {
          const icon = r.intentLevel === 'high' ? '🔴' : r.intentLevel === 'medium' ? '🟡' : '⚪';
          console.log(`${icon} ${i + 1}. r/${r.subreddit || 'unknown'}`);
          console.log(`   ${r.title}`);
          console.log(`   ${r.snippet?.slice(0, 120) || ''}`);
          console.log(`   ${r.url}\n`);
        });
        break;
      }
      case 'score': {
        const args = parseArgs(rest);
        const result = scoreRedditProspect({
          username: args.username,
          askedForRecommendations: !!(args.post && ['looking for', 'recommend', 'best tool'].some(p => args.post.toLowerCase().includes(p))),
          usedBuyingLanguage: !!(args.post && ['willing to pay', 'need', 'looking for'].some(p => args.post.toLowerCase().includes(p))),
          karma: parseInt(args.karma || '0'),
          activeInTargetSubreddits: !!args.active,
        });
        console.log(result.summary);
        console.log('Reasons:', result.reasons.join(', ') || 'none');
        console.log('Next action:', result.nextAction);
        break;
      }
      case 'comment': {
        const args = parseArgs(rest);
        if (!args.title) { console.error('Usage: comment --title "Post title" --subreddit startups [--product "MyProduct"] [--mention]'); process.exit(1); }
        const result = generateRedditComment({
          postTitle: args.title,
          subreddit: args.subreddit,
          includeProductMention: !!args.mention,
          productName: args.product,
          productDescription: args.description,
        });
        if (!result.success) { console.error(result.error); process.exit(1); }
        console.log(`\n${result.summary}\n`);
        result.data.sections.forEach(s => {
          console.log(`--- ${s.part.toUpperCase()} ---`);
          console.log(s.content);
          if (s.tip) console.log(`💡 Tip: ${s.tip}`);
          console.log();
        });
        break;
      }
      default:
        console.log('Commands:');
        console.log('  search <keyword> [--subreddit <sub>]   Find high-intent Reddit posts via Brave');
        console.log('  score --username u/handle --post "..." Score a Reddit prospect');
        console.log('  comment --title "Post" --subreddit <s>  Generate a value-first comment structure');
    }
  })();
}
