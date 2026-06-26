#!/usr/bin/env node

/**
 * Thought Leader Content Collector
 * Collects podcasts, interviews, and videos from YouTube, Apple Podcasts, and Spotify
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Configuration
const CONFIG_PATH = path.join(__dirname, '..', 'config.json');
const OUTPUT_DIR = path.join(__dirname, '..', 'daily-logs');

/**
 * Search YouTube for content
 * Note: Requires YouTube Data API key for production use
 * This is a placeholder implementation
 */
async function searchYouTube(query, days) {
  console.log(`[YouTube] Searching for: ${query} (last ${days} days)`);
  
  // Placeholder - in production, use YouTube Data API v3
  // const apiKey = process.env.YOUTUBE_API_KEY;
  // const url = `https://www.googleapis.com/youtube/v3/search?q=${encodeURIComponent(query)}&type=video&order=date&maxResults=10&key=${apiKey}`;
  
  return {
    platform: 'YouTube',
    query: query,
    results: [] // API results would go here
  };
}

/**
 * Search Apple Podcasts
 * Uses iTunes Search API (no key required)
 */
async function searchApplePodcasts(query, days) {
  console.log(`[Apple Podcasts] Searching for: ${query}`);
  
  return new Promise((resolve) => {
    const url = `https://itunes.apple.com/search?term=${encodeURIComponent(query)}&entity=podcast&limit=10`;
    
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve({
            platform: 'Apple Podcasts',
            query: query,
            results: json.results?.map(item => ({
              title: item.trackName,
              link: item.trackViewUrl,
              publishDate: item.releaseDate,
              summary: item.description || item.trackName,
              author: item.artistName
            })) || []
          });
        } catch (e) {
          resolve({ platform: 'Apple Podcasts', query: query, results: [] });
        }
      });
    }).on('error', () => {
      resolve({ platform: 'Apple Podcasts', query: query, results: [] });
    });
  });
}

/**
 * Search Spotify Podcasts
 * Note: Requires Spotify API authentication for production use
 */
async function searchSpotify(query, days) {
  console.log(`[Spotify] Searching for: ${query}`);
  
  // Placeholder - in production, use Spotify Web API
  // Requires OAuth2 authentication
  return {
    platform: 'Spotify',
    query: query,
    results: [] // API results would go here
  };
}

/**
 * Extract key points from content summary
 */
function extractKeyPoints(summary) {
  if (!summary) return [];
  
  // Simple extraction - in production, use NLP/LLM
  const sentences = summary.split(/[.!?]+/).filter(s => s.trim().length > 20);
  return sentences.slice(0, 3).map(s => s.trim() + '.');
}

/**
 * Main collection function
 */
async function collectContent(thoughtLeader, days) {
  const results = {
    name: thoughtLeader.name,
    keywords: thoughtLeader.keywords,
    content: []
  };
  
  for (const keyword of thoughtLeader.keywords.slice(0, 2)) {
    if (thoughtLeader.platforms.includes('youtube')) {
      const ytResults = await searchYouTube(keyword, days);
      results.content.push(...ytResults.results);
    }
    
    if (thoughtLeader.platforms.includes('apple-podcasts')) {
      const apResults = await searchApplePodcasts(keyword, days);
      results.content.push(...apResults.results);
    }
    
    if (thoughtLeader.platforms.includes('spotify')) {
      const spResults = await searchSpotify(keyword, days);
      results.content.push(...spResults.results);
    }
  }
  
  return results;
}

/**
 * Analyze common themes across thought leaders
 */
function analyzeCommonThemes(allResults, threshold) {
  const themeMap = new Map();
  
  allResults.forEach(result => {
    result.content.forEach(item => {
      const summary = (item.summary || '').toLowerCase();
      const keywords = ['AI', 'machine learning', 'product', 'growth', 'performance', 'leadership', 'innovation', 'technology', 'strategy', 'development'];
      
      keywords.forEach(keyword => {
        if (summary.includes(keyword.toLowerCase())) {
          const count = themeMap.get(keyword) || { count: 0, leaders: new Set() };
          count.count++;
          count.leaders.add(result.name);
          themeMap.set(keyword, count);
        }
      });
    });
  });
  
  const commonThemes = [];
  themeMap.forEach((data, theme) => {
    if (data.leaders.size >= threshold) {
      commonThemes.push({
        theme: theme,
        leaderCount: data.leaders.size,
        leaders: Array.from(data.leaders)
      });
    }
  });
  
  return commonThemes.sort((a, b) => b.leaderCount - a.leaderCount);
}

/**
 * Generate Markdown report
 */
function generateMarkdownReport(allResults, commonThemes, timeRange) {
  const date = new Date().toISOString().split('T')[0];
  
  let md = `# Thought Leader Daily Report\n\n`;
  md += `**Date:** ${date}\n`;
  md += `**Time Range:** Last ${timeRange} days\n\n`;
  md += `---\n\n`;
  
  // Common Themes Section
  if (commonThemes.length > 0) {
    md += `## 🔍 Common Themes\n\n`;
    md += `Themes mentioned by ${commonThemes[0].leaderCount}+ thought leaders:\n\n`;
    commonThemes.forEach(theme => {
      md += `- **${theme.theme}** - Mentioned by: ${theme.leaders.join(', ')}\n`;
    });
    md += `\n---\n\n`;
  }
  
  // Individual Results
  allResults.forEach(result => {
    md += `## 👤 ${result.name}\n\n`;
    
    if (result.content.length === 0) {
      md += `_No new content found in the last ${timeRange} days._\n\n`;
    } else {
      result.content.forEach((item, idx) => {
        md += `### ${item.title || 'Untitled'}\n\n`;
        md += `- **Platform:** ${item.platform}\n`;
        md += `- **Published:** ${item.publishDate ? new Date(item.publishDate).toLocaleDateString() : 'Unknown'}\n`;
        md += `- **Link:** ${item.link || 'N/A'}\n`;
        md += `- **Summary:** ${item.summary || 'No summary available'}\n`;
        
        const keyPoints = extractKeyPoints(item.summary);
        if (keyPoints.length > 0) {
          md += `- **Key Points:**\n`;
          keyPoints.forEach(point => {
            md += `  - ${point}\n`;
          });
        }
        md += `\n`;
      });
    }
    
    md += `---\n\n`;
  });
  
  md += `_Generated by Thought Leader Tracker_\n`;
  
  return md;
}

/**
 * Main execution
 */
async function main() {
  const args = process.argv.slice(2);
  const timeRange = args.includes('30') ? 30 : 7; // Default to 7 days
  
  console.log(`\n🚀 Thought Leader Content Collector`);
  console.log(`Time range: Last ${timeRange} days\n`);
  
  // Load configuration
  const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  
  // Collect content for each thought leader
  const allResults = [];
  for (const leader of config.thoughtLeaders) {
    console.log(`\n📍 Collecting for: ${leader.name}`);
    const result = await collectContent(leader, timeRange);
    allResults.push(result);
    console.log(`   Found ${result.content.length} items`);
  }
  
  // Analyze common themes
  console.log('\n🔍 Analyzing common themes...');
  const commonThemes = analyzeCommonThemes(allResults, config.commonThemesThreshold);
  console.log(`   Found ${commonThemes.length} common themes`);
  
  // Generate report
  console.log('\n📝 Generating report...');
  const report = generateMarkdownReport(allResults, commonThemes, timeRange);
  
  // Save report
  const date = new Date().toISOString().split('T')[0];
  const filename = `daily-report-${date}-${timeRange}d.md`;
  const outputPath = path.join(OUTPUT_DIR, filename);
  
  fs.writeFileSync(outputPath, report, 'utf8');
  console.log(`\n✅ Report saved to: ${outputPath}\n`);
}

main().catch(console.error);
