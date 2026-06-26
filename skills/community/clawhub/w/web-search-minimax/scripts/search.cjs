#!/usr/bin/env node

/**
 * Web Search Skill
 * Uses Minimax Coding Plan Search API to perform web searches
 * 
 * Usage:
 *   node search.cjs "search query"
 *   node search.cjs "今天天气怎么样"
 *   node search.cjs "Python 教程"
 */

const fs = require("fs");
const path = require("path");

// Read API key from environment variable
const API_KEY = process.env.MINIMAX_API_KEY;
if (!API_KEY) {
  console.error("Error: MINIMAX_API_KEY environment variable not set");
  console.error("Please set it with: export MINIMAX_API_KEY=\"your-api-key\"");
  process.exit(1);
}
const API_HOST = "https://api.minimaxi.com";
const ENDPOINT = "/v1/coding_plan/search";

const args = process.argv.slice(2);
if (args.length < 1) {
  console.error("Usage: search.cjs <query>");
  console.error("Example: node search.cjs \"今天天气怎么样\"");
  process.exit(1);
}

const query = args.join(" ");

async function webSearch() {
  const url = `${API_HOST}${ENDPOINT}`;
  
  console.error(`Searching for: ${query}`);
  
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${API_KEY}`,
      "MM-API-Source": "Minimax-Skill"
    },
    body: JSON.stringify({ q: query })
  });
  
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API request failed (${response.status}): ${errorText}`);
  }
  
  const data = await response.json();
  
  // Check for API-level errors
  const baseResp = data.base_resp || {};
  if (baseResp.status_code !== 0) {
    throw new Error(`API error (${baseResp.status_code}): ${baseResp.status_msg}`);
  }
  
  // Parse and format the results
  const results = data.organic || [];
  const relatedSearches = data.related_searches || [];
  
  if (results.length === 0) {
    console.log("No search results found.");
    return;
  }
  
  // Output formatted results
  console.log("=== 搜索结果 ===\n");
  
  results.forEach((item, index) => {
    console.log(`${index + 1}. ${item.title}`);
    console.log(`   链接: ${item.link}`);
    if (item.snippet) {
      console.log(`   摘要: ${item.snippet}`);
    }
    if (item.date) {
      console.log(`   日期: ${item.date}`);
    }
    console.log("");
  });
  
  if (relatedSearches.length > 0) {
    console.log("=== 相关搜索 ===");
    relatedSearches.forEach(item => {
      console.log(`• ${item}`);
    });
  }
}

webSearch().catch(err => {
  console.error("Error:", err.message);
  process.exit(1);
});
