#!/usr/bin/env node
/**
 * Feed Digest Generator
 * 
 * Creates summary digests from collected social media posts.
 * Generates markdown summaries with key themes, top posts, and insights.
 * 
 * ⚖️ COMPLIANCE NOTICE:
 * - Only process data you have legal right to store
 * - Anonymize personal data in digests
 * - Do not retain personal data longer than necessary
 * - Comply with GDPR/CCPA retention requirements
 */

const fs = require('fs');
const path = require('path');

// Parse command line arguments
function parseArgs(args) {
  const parsed = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const value = args[i + 1];
      parsed[key] = value;
      i++;
    }
  }
  return parsed;
}

// Extract keywords from text
function extractKeywords(text) {
  const stopwords = new Set([
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
    'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought', 'used',
    'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between',
    'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
    'why', 'how', 'all', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
    'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
    'just', 'and', 'but', 'if', 'or', 'because', 'until', 'while', 'although',
    'though', 'after', 'before', 'when', 'whenever', 'where', 'wherever', 'whether',
    'which', 'whichever', 'who', 'whoever', 'whom', 'whomever', 'whose', 'what',
    'whatever', 'whichever', 'that', 'whatever'
  ]);
  
  const words = text.toLowerCase().replace(/[^\w\s]/g, '').split(/\s+/);
  const freq = {};
  
  words.forEach(w => {
    if (w.length > 3 && !stopwords.has(w)) {
      freq[w] = (freq[w] || 0) + 1;
    }
  });
  
  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([word]) => word);
}

// Extract engagement from post
function extractEngagement(post) {
  const engagement = post.likes || post.votes || post.points || '0';
  return parseInt(engagement.replace(/[^0-9]/g, '')) || 0;
}

// Generate digest content
function generateDigest(data) {
  const { platform, query, collectedAt, posts } = data;
  
  let digest = `# ${platform.toUpperCase()} Digest: "${query}"\n\n`;
  digest += `**Generated:** ${new Date(collectedAt).toLocaleString()}\n`;
  digest += `**Posts analyzed:** ${posts.length}\n\n`;
  
  // Top posts by engagement
  const sorted = [...posts].sort((a, b) => {
    return extractEngagement(b) - extractEngagement(a);
  });
  
  digest += `## 🔥 Top Posts\n\n`;
  sorted.slice(0, 5).forEach((p, i) => {
    digest += `### ${i + 1}. ${p.author || 'Unknown'} (${extractEngagement(p)} engagement)\n`;
    digest += `${p.text || ''}\n\n`;
    digest += `[View](${p.url || '#'})\n\n`;
  });
  
  // Key themes
  const allText = posts.map(p => p.text || '').join(' ');
  const keywords = extractKeywords(allText);
  
  digest += `## 🏷️ Key Themes\n\n`;
  digest += keywords.map(k => `- ${k}`).join('\n') + '\n\n';
  
  // Author breakdown
  const authors = {};
  posts.forEach(p => {
    const author = p.author || 'Unknown';
    authors[author] = (authors[author] || 0) + 1;
  });
  
  digest += `## 👥 Top Contributors\n\n`;
  Object.entries(authors)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .forEach(([author, count]) => {
      digest += `- ${author}: ${count} posts\n`;
    });
  digest += '\n';
  
  // Time distribution
  const hours = {};
  posts.forEach(p => {
    if (p.timestamp) {
      const hour = new Date(p.timestamp).getHours();
      hours[hour] = (hours[hour] || 0) + 1;
    }
  });
  
  const peakHour = Object.entries(hours).sort((a, b) => b[1] - a[1])[0];
  if (peakHour) {
    digest += `## 📈 Activity Timeline\n\n`;
    digest += `**Peak activity:** ${peakHour[0]}:00 (${peakHour[1]} posts)\n\n`;
  }
  
  // Quick stats
  const avgEngagement = posts.reduce((sum, p) => {
    return sum + extractEngagement(p);
  }, 0) / posts.length;
  
  digest += `## 📊 Quick Stats\n\n`;
  digest += `- **Average engagement:** ${Math.round(avgEngagement)}\n`;
  digest += `- **Total posts:** ${posts.length}\n`;
  digest += `- **Unique authors:** ${Object.keys(authors).length}\n`;
  
  return digest;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  
  const input = args.input;
  if (!input) {
    console.error('Error: --input <file> required (JSON from skroller.js)');
    process.exit(1);
  }
  
  if (!fs.existsSync(input)) {
    console.error(`Error: Input file not found: ${input}`);
    process.exit(1);
  }
  
  const output = args.output || `digest-${Date.now()}.md`;
  
  console.log(`Generating digest from ${input}...`);
  
  const data = JSON.parse(fs.readFileSync(input, 'utf8'));
  const digest = generateDigest(data);
  
  fs.writeFileSync(output, digest);
  
  console.log(`Digest saved to: ${output}`);
  console.log(`Analyzed ${data.posts.length} posts`);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
