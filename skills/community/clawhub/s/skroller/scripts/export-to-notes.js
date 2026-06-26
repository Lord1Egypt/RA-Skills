#!/usr/bin/env node
/**
 * Export to Note Apps - Unified Exporter
 * 
 * Exports skroller data to multiple note applications:
 * - Bear (macOS)
 * - Obsidian (cross-platform)
 * - Notion (cross-platform)
 * - Apple Notes (macOS/iOS)
 * - Evernote (cross-platform)
 * - OneNote (cross-platform)
 * - Google Keep (web)
 * 
 * ⚖️ COMPLIANCE NOTICE:
 * - Only export data you have legal right to store
 * - Anonymize personal data per GDPR/CCPA
 * - Honor deletion requests (GDPR Art. 17)
 * - Limit retention to necessary periods
 * - Do not export sensitive personal data
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Parse command line arguments
function parseArgs(args) {
  const parsed = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const value = args[i + 1];
      if (key === 'limit') {
        parsed[key] = parseInt(value || '10');
      } else if (key === 'dryRun') {
        parsed[key] = value === 'true' || value === undefined;
      } else {
        parsed[key] = value;
      }
      i++;
    }
  }
  return parsed;
}

// Load configuration
function loadConfig() {
  const configPath = path.join(process.cwd(), '.skroller-config.json');
  if (fs.existsSync(configPath)) {
    return JSON.parse(fs.readFileSync(configPath, 'utf8'));
  }
  return { export: {} };
}

// Extract engagement from post
function extractEngagement(post) {
  const engagement = post.likes || post.votes || post.points || post.claps || post.saves || '0';
  return parseInt(engagement.replace(/[^0-9]/g, '')) || 0;
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

// Get author breakdown
function getAuthorBreakdown(posts) {
  const authors = {};
  posts.forEach(p => {
    const author = p.author || 'Unknown';
    authors[author] = (authors[author] || 0) + 1;
  });
  
  return Object.entries(authors)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);
}

// Calculate average engagement
function getAverageEngagement(posts) {
  const sum = posts.reduce((s, p) => s + extractEngagement(p), 0);
  return posts.length > 0 ? Math.round(sum / posts.length) : 0;
}

// Format content for note apps
function formatContent(data, limit = 10) {
  const { platform, query, collectedAt, posts } = data;
  
  const sorted = [...posts].sort((a, b) => extractEngagement(b) - extractEngagement(a));
  const topPosts = sorted.slice(0, limit);
  const keywords = extractKeywords(posts.map(p => p.text || '').join(''));
  const authors = getAuthorBreakdown(posts);
  const avgEngagement = getAverageEngagement(posts);
  
  return {
    title: `${platform.toUpperCase()} Research: "${query}"`,
    collected: new Date(collectedAt).toLocaleString(),
    postCount: posts.length,
    topPosts,
    keywords,
    authors,
    avgEngagement,
    raw: data
  };
}

// Bear Export (macOS)
function exportToBear(content, options) {
  const { title, tags, dryRun } = options;
  
  let markdown = `# ${content.title}\n\n`;
  markdown += `**Collected:** ${content.collected}\n`;
  markdown += `**Posts:** ${content.postCount}\n\n`;
  markdown += `---\n\n`;
  
  content.topPosts.forEach((p, i) => {
    markdown += `## ${i + 1}. ${p.author || 'Unknown'}\n\n`;
    markdown += `${p.text || ''}\n\n`;
    markdown += `**Engagement:** ${extractEngagement(p)} | `;
    markdown += `[View](${p.url || '#'})\n\n`;
    markdown += `---\n\n`;
  });
  
  if (dryRun) {
    console.log('[DRY RUN] Bear export:');
    console.log(`  Title: ${title}`);
    console.log(`  Tags: ${tags?.split(',').join(', ') || 'skroller, research'}`);
    console.log(`  Preview: ${markdown.slice(0, 150)}...`);
    return;
  }
  
  try {
    execSync('which grizzly', { stdio: 'ignore' });
  } catch (e) {
    throw new Error('grizzly CLI not found. Install: go install github.com/tylerwince/grizzly/cmd/grizzly@latest');
  }
  
  const tagList = tags?.split(',') || ['skroller', 'research'];
  const tagArgs = tagList.map(t => `--tag "${t}"`).join(' ');
  const escaped = markdown.replace(/"/g, '\\"').replace(/\$/g, '\\$');
  const command = `echo "${escaped}" | grizzly create --title "${title}" ${tagArgs}`;
  
  execSync(command, { stdio: 'inherit' });
  console.log(`✓ Created Bear note: "${title}"`);
}

// Obsidian Export
function exportToObsidian(content, options) {
  const { vault, folder, filename } = options;
  
  if (!vault) throw new Error('Obsidian vault path required (--vault <path>)');
  if (!fs.existsSync(vault)) throw new Error(`Vault not found: ${vault}`);
  
  let markdown = `---\n`;
  markdown += `title: "${content.title}"\n`;
  markdown += `platform: ${content.raw.platform}\n`;
  markdown += `query: "${content.raw.query}"\n`;
  markdown += `collected: ${content.raw.collectedAt}\n`;
  markdown += `posts: ${content.postCount}\n`;
  markdown += `tags: [skroller, ${content.raw.platform}, research]\n`;
  markdown += `created: ${new Date().toISOString()}\n`;
  markdown += `---\n\n`;
  
  markdown += `# ${content.title}\n\n`;
  markdown += `**Collected:** ${content.collected}\n`;
  markdown += `**Posts:** ${content.postCount}\n\n`;
  markdown += `---\n\n`;
  
  markdown += `## 🔥 Top Posts\n\n`;
  content.topPosts.forEach((p, i) => {
    markdown += `### ${i + 1}. ${p.author || 'Unknown'}\n\n`;
    markdown += `${p.text || ''}\n\n`;
    markdown += `**Engagement:** ${extractEngagement(p)} | `;
    markdown += `[[${p.url}|View]]\n\n`;
    markdown += `---\n\n`;
  });
  
  markdown += `## 🏷️ Key Themes\n\n`;
  content.keywords.forEach(k => markdown += `- [[${k}]]\n`);
  markdown += '\n';
  
  markdown += `## 👥 Top Contributors\n\n`;
  content.authors.forEach(([author, count]) => markdown += `- ${author}: ${count}\n`);
  markdown += '\n';
  
  markdown += `## 📊 Stats\n\n`;
  markdown += `- **Avg engagement:** ${content.avgEngagement}\n`;
  markdown += `- **Total posts:** ${content.postCount}\n`;
  markdown += `- **Unique authors:** ${content.authors.length}\n`;
  
  const folderPath = path.join(vault, folder || 'Skroller');
  if (!fs.existsSync(folderPath)) fs.mkdirSync(folderPath, { recursive: true });
  
  const baseName = filename || `${content.raw.platform}-${content.raw.query.replace(/\s+/g, '-')}-${Date.now()}.md`;
  const filePath = path.join(folderPath, baseName);
  
  fs.writeFileSync(filePath, markdown);
  console.log(`✓ Created Obsidian note: ${baseName}`);
  console.log(`  Location: ${path.relative(vault, filePath)}`);
}

// Notion Export
async function exportToNotion(content, options) {
  const { apiKey, databaseId, dryRun } = options;
  const notionKey = apiKey || process.env.NOTION_API_KEY;
  
  if (!notionKey) throw new Error('Notion API key required (--api-key or NOTION_API_KEY env)');
  
  if (dryRun) {
    console.log('[DRY RUN] Notion export:');
    console.log(`  Title: ${content.title}`);
    console.log(`  Database: ${databaseId || 'default'}`);
    return;
  }
  
  const properties = {
    title: { title: [{ text: { content: content.title } }] },
    Platform: { select: { name: content.raw.platform } },
    Posts: { number: content.postCount },
    Tags: { multi_select: [{ name: 'skroller' }, { name: 'research' }] }
  };
  
  const parent = databaseId ? { database_id: databaseId } : { page_id: 'parent-page-id' };
  
  try {
    const response = await fetch('https://api.notion.com/v1/pages', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${notionKey}`,
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
      },
      body: JSON.stringify({ parent, properties })
    });
    
    if (!response.ok) throw new Error(`Notion API failed: ${response.status}`);
    
    const result = await response.json();
    console.log(`✓ Created Notion page: ${content.title}`);
    console.log(`  URL: ${result.url}`);
  } catch (e) {
    throw new Error(`Notion API failed: ${e.message}`);
  }
}

// Apple Notes Export
function exportToAppleNotes(content, options) {
  const { folder, dryRun } = options;
  
  let body = `${content.title}\\n\\n`;
  body += `Collected: ${content.collected}\\n`;
  body += `Posts: ${content.postCount}\\n\\n`;
  body += `---\\n\\n`;
  
  content.topPosts.forEach((p, i) => {
    body += `${i + 1}. ${p.author || 'Unknown'}\\n`;
    body += `${p.text || ''}\\n`;
    body += `Engagement: ${extractEngagement(p)}\\n`;
    body += `URL: ${p.url || 'N/A'}\\n\\n`;
  });
  
  if (dryRun) {
    console.log('[DRY RUN] Apple Notes export:');
    console.log(`  Title: ${content.title}`);
    console.log(`  Folder: ${folder || 'Notes'}`);
    return;
  }
  
  const script = `tell application "Notes"
    activate
    set noteFolder to "${folder || 'Notes'}"
    try
      set targetFolder to folder noteFolder
    on error
      set targetFolder to folder "Notes"
    end try
    set newNote to make new note at targetFolder with properties {body:"${body}"}
    set name of newNote to "${content.title}"
  end tell`;
  
  try {
    execSync(`osascript -e '${script}'`, { stdio: 'inherit' });
    console.log(`✓ Created Apple Note: "${content.title}"`);
  } catch (e) {
    throw new Error('Apple Notes export failed. Ensure Notes app is installed.');
  }
}

// Evernote Export
function exportToEvernote(content, options) {
  const { output, dryRun } = options;
  
  let enex = `<?xml version="1.0" encoding="UTF-8"?>\n`;
  enex += `<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">\n`;
  enex += `<en-export export-date="${new Date().toISOString()}">\n`;
  enex += `  <note>\n`;
  enex += `    <title>${content.title}</title>\n`;
  enex += `    <created>${new Date().toISOString()}</created>\n`;
  enex += `    <note-content><![CDATA[\n`;
  enex += `      <h1>${content.title}</h1>\n`;
  enex += `      <p>Collected: ${content.collected}</p>\n`;
  enex += `      <p>Posts: ${content.postCount}</p>\n`;
  enex += `      <hr/>\n`;
  
  content.topPosts.forEach((p, i) => {
    enex += `      <h2>${i + 1}. ${p.author || 'Unknown'}</h2>\n`;
    enex += `      <p>${p.text || ''}</p>\n`;
    enex += `      <p>Engagement: ${extractEngagement(p)}</p>\n`;
    enex += `      <p>URL: <a href="${p.url || '#'}">View</a></p>\n`;
  });
  
  enex += `    ]]></note-content>\n`;
  enex += `    <tag>skroller</tag>\n`;
  enex += `    <tag>research</tag>\n`;
  enex += `  </note>\n`;
  enex += `</en-export>`;
  
  const outputPath = output || `evernote-${Date.now()}.enex`;
  
  if (dryRun) {
    console.log('[DRY RUN] Evernote export:');
    console.log(`  Output: ${outputPath}`);
    return;
  }
  
  fs.writeFileSync(outputPath, enex);
  console.log(`✓ Created Evernote export: ${outputPath}`);
  console.log('  Import via Evernote: File → Import → ENEX file');
}

// OneNote Export
async function exportToOneNote(content, options) {
  const { accessToken, sectionId, dryRun } = options;
  const token = accessToken || process.env.MS_GRAPH_TOKEN;
  
  if (!token) throw new Error('Microsoft Graph token required (--access-token or MS_GRAPH_TOKEN env)');
  
  if (dryRun) {
    console.log('[DRY RUN] OneNote export:');
    console.log(`  Section: ${sectionId || 'default'}`);
    console.log(`  Title: ${content.title}`);
    return;
  }
  
  const pageContent = `<!DOCTYPE html><html><head><title>${content.title}</title></head><body>
    <h1>${content.title}</h1>
    <p><strong>Collected:</strong> ${content.collected}</p>
    <p><strong>Posts:</strong> ${content.postCount}</p>
    <hr/>
    ${content.topPosts.map((p, i) => `
      <h2>${i + 1}. ${p.author || 'Unknown'}</h2>
      <p>${p.text || ''}</p>
      <p><strong>Engagement:</strong> ${extractEngagement(p)}</p>
      <p><a href="${p.url || '#'}">View post</a></p>
      <hr/>
    `).join('')}
  </body></html>`;
  
  const endpoint = sectionId 
    ? `https://graph.microsoft.com/v1.0/me/onenote/sections/${sectionId}/pages`
    : 'https://graph.microsoft.com/v1.0/me/onenote/pages';
  
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/xhtml+xml'
      },
      body: pageContent
    });
    
    if (!response.ok) throw new Error(`OneNote failed: ${response.status}`);
    
    const result = await response.json();
    console.log(`✓ Created OneNote page: ${content.title}`);
    console.log(`  Links: ${result.links?.oneNoteClientUrl?.href || result.id}`);
  } catch (e) {
    throw new Error(`OneNote export failed: ${e.message}`);
  }
}

// Google Keep Export
function exportToGoogleKeep(content, options) {
  const { output, dryRun } = options;
  
  let html = `<!DOCTYPE html>\n<html>\n<head><title>${content.title}</title></head>\n<body>\n`;
  html += `<h1>${content.title}</h1>\n`;
  html += `<p>Collected: ${content.collected}</p>\n`;
  html += `<p>Posts: ${content.postCount}</p>\n`;
  html += `<hr/>\n`;
  
  content.topPosts.forEach((p, i) => {
    html += `<h3>${i + 1}. ${p.author || 'Unknown'}</h3>\n`;
    html += `<p>${p.text || ''}</p>\n`;
    html += `<p><small>Engagement: ${extractEngagement(p)}</small></p>\n`;
    html += `<p><a href="${p.url || '#'}">View</a></p>\n`;
    html += `<hr/>\n`;
  });
  
  html += `</body>\n</html>`;
  
  const outputPath = output || `keep-${Date.now()}.html`;
  
  if (dryRun) {
    console.log('[DRY RUN] Google Keep export:');
    console.log(`  Output: ${outputPath}`);
    console.log('  Note: Manual import required (no public write API)');
    return;
  }
  
  fs.writeFileSync(outputPath, html);
  console.log(`✓ Created Google Keep export: ${outputPath}`);
  console.log('  Import via: https://keep.google.com (copy/paste content)');
}

// ============================================================================
// Roam Research Export (via Markdown import)
// ============================================================================

function exportToRoam(content, options) {
  const { output, dryRun } = options;
  
  // Roam uses Markdown with block references
  let md = `# ${content.title}\n\n`;
  md += `**Collected:** ${content.collected}\n`;
  md += `**Posts:** ${content.postCount}\n\n`;
  md += `---\n\n`;
  
  content.topPosts.forEach((p, i) => {
    md += `- ## ${i + 1}. ${p.author || 'Unknown'}\n`;
    md += `  - ${p.text || ''}\n`;
    md += `  - **Engagement:** ${extractEngagement(p)}\n`;
    md += `  - [${p.url || '#'} View]\n`;
    md += `\n`;
  });
  
  md += `---\n\n`;
  md += `## Key Themes\n\n`;
  content.keywords.forEach(k => {
    md += `- [[${k}]]\n`;
  });
  
  const outputPath = output || `roam-${Date.now()}.md`;
  
  if (dryRun) {
    console.log('[DRY RUN] Roam Research export:');
    console.log(`  Output: ${outputPath}`);
    console.log('  Import: Drag into Roam or use Import menu');
    return;
  }
  
  fs.writeFileSync(outputPath, md);
  console.log(`✓ Created Roam Research export: ${outputPath}`);
  console.log('  Import: Drag MDL file into Roam or use File → Import');
}

// ============================================================================
// Logseq Export (via Markdown for journals/pages)
// ============================================================================

function exportToLogseq(content, options) {
  const { vault, page, dryRun } = options;
  
  if (!vault) {
    throw new Error('Logseq vault path required (--vault <path>)');
  }
  
  if (!fs.existsSync(vault)) {
    throw new Error(`Vault not found: ${vault}`);
  }
  
  let md = `---\n`;
  md += `title: ${content.title}\n`;
  md += `platform: ${content.raw.platform}\n`;
  md += `collected: ${content.raw.collectedAt}\n`;
  md += `tags: [skroller, ${content.raw.platform}, research]\n`;
  md += `---\n\n`;
  
  md += `# ${content.title}\n\n`;
  md += `**Collected:** ${content.collected}\n`;
  md += `**Posts:** ${content.postCount}\n\n`;
  md += `---\n\n`;
  
  content.topPosts.forEach((p, i) => {
    md += `## ${i + 1}. ${p.author || 'Unknown'}\n\n`;
    md += `${p.text || ''}\n\n`;
    md += `**Engagement:** ${extractEngagement(p)} | [View](${p.url || '#'})\n\n`;
    md += `---\n\n`;
  });
  
  md += `## Key Themes\n\n`;
  content.keywords.forEach(k => {
    md += `- [[${k}]]\n`;
  });
  
  const pagesDir = path.join(vault, 'pages');
  if (!fs.existsSync(pagesDir)) fs.mkdirSync(pagesDir, { recursive: true });
  
  const pageName = page || `${content.raw.platform}-${content.raw.query.replace(/\s+/g, '-')}`;
  const filePath = path.join(pagesDir, `${pageName}.md`);
  
  if (dryRun) {
    console.log('[DRY RUN] Logseq export:');
    console.log(`  Page: ${pageName}`);
    console.log(`  Location: ${filePath}`);
    return;
  }
  
  fs.writeFileSync(filePath, md);
  console.log(`✓ Created Logseq page: ${pageName}.md`);
  console.log(`  Location: ${path.relative(vault, filePath)}`);
}

// ============================================================================
// Anytype Export (via Markdown import)
// ============================================================================

function exportToAnytype(content, options) {
  const { output, dryRun } = options;
  
  // Anytype supports Markdown import with object types
  let md = `# ${content.title}\n\n`;
  md += `**Type:** Research\n`;
  md += `**Collected:** ${content.collected}\n`;
  md += `**Posts:** ${content.postCount}\n`;
  md += `**Tags:** skroller, ${content.raw.platform}, research\n\n`;
  md += `---\n\n`;
  
  content.topPosts.forEach((p, i) => {
    md += `## ${i + 1}. ${p.author || 'Unknown'}\n\n`;
    md += `${p.text || ''}\n\n`;
    md += `**Engagement:** ${extractEngagement(p)}\n`;
    md += `**Source:** [${p.url || '#'}]\n\n`;
    md += `---\n\n`;
  });
  
  md += `## Key Themes\n\n`;
  content.keywords.forEach(k => {
    md += `- ${k}\n`;
  });
  
  const outputPath = output || `anytype-${Date.now()}.md`;
  
  if (dryRun) {
    console.log('[DRY RUN] Anytype export:');
    console.log(`  Output: ${outputPath}`);
    console.log('  Import: Use Anytype Import feature');
    return;
  }
  
  fs.writeFileSync(outputPath, md);
  console.log(`✓ Created Anytype export: ${outputPath}`);
  console.log('  Import: Open Anytype → Import → Select MDL file');
}

// Main export router
async function main() {
  const args = parseArgs(process.argv.slice(2));
  
  const input = args.input;
  if (!input || !fs.existsSync(input)) {
    console.error('Error: --input <file> required (JSON from skroller.js)');
    process.exit(1);
  }
  
  const app = args.app?.toLowerCase();
  if (!app) {
    console.error('Error: --app <name> required');
    console.error('Available: bear, obsidian, notion, apple-notes, evernote, one-note, keep');
    process.exit(1);
  }
  
  const config = loadConfig();
  const data = JSON.parse(fs.readFileSync(input, 'utf8'));
  const content = formatContent(data, args.limit || 10);
  
  const dryRun = args.dryRun === true;
  
  console.log(`Exporting to ${app}...`);
  console.log(`Input: ${input}`);
  console.log(`Posts: ${content.postCount}`);
  
  const options = {
    dryRun,
    title: args.title || content.title,
    tags: args.tags,
    vault: args.vault || config.export?.vault,
    folder: args.folder || config.export?.folder,
    filename: args.filename,
    apiKey: args.apiKey || process.env.NOTION_API_KEY,
    databaseId: args.databaseId || config.export?.notionDatabaseId,
    accessToken: args.accessToken || process.env.MS_GRAPH_TOKEN,
    output: args.output,
    limit: args.limit
  };
  
  try {
    switch (app) {
      case 'bear': exportToBear(content, options); break;
      case 'obsidian': exportToObsidian(content, options); break;
      case 'notion': await exportToNotion(content, options); break;
      case 'apple-notes':
      case 'apple': exportToAppleNotes(content, options); break;
      case 'evernote': exportToEvernote(content, options); break;
      case 'one-note':
      case 'onenote': await exportToOneNote(content, options); break;
      case 'keep':
      case 'google-keep': exportToGoogleKeep(content, options); break;
      case 'roam':
      case 'roam-research': exportToRoam(content, options); break;
      case 'logseq': exportToLogseq(content, options); break;
      case 'anytype': exportToAnytype(content, options); break;
      default:
        console.error(`Unknown app: ${app}`);
        console.error('Available: bear, obsidian, notion, apple-notes, evernote, one-note, keep, roam, logseq, anytype');
        process.exit(1);
    }
  } catch (e) {
    console.error(`Export failed: ${e.message}`);
    process.exit(1);
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
