#!/usr/bin/env node

const API_BASE = process.env.MBM_API_BASE || "https://api.makebestmusic.com";
const API_KEY = process.env.apiKey;

if (!API_KEY) {
  console.error(JSON.stringify({ code: -1, message: "Missing apiKey - please fill in the apiKey field in skill settings" }));
  process.exit(1);
}

const musicIds = process.argv[2];
if (!musicIds) {
  console.error(JSON.stringify({ code: -1, message: "Missing music_ids parameter" }));
  console.error("Usage: node query.js '<music_id1> <music_id2> ...'");
  process.exit(1);
}

// Split by space or comma
const ids = musicIds.split(/[\s,]+/).filter(id => id.trim());
const musicIdsParam = ids.map(id => `music_ids=${encodeURIComponent(id)}`).join('&');

async function query() {
  try {
    const res = await fetch(`${API_BASE}/api/skill/music_status?${musicIdsParam}`, {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    });

    const data = await res.json();
    
    if (!Array.isArray(data)) {
      console.log(JSON.stringify({
        success: false,
        message: "Invalid response from server"
      }, null, 2));
      return;
    }
    
    // Check if all completed
    const allCompleted = data.every(item => item.status === "completed");
    const anyFailed = data.some(item => item.status === "failed");
    
    if (allCompleted) {
      console.log(JSON.stringify({
        success: true,
        status: "completed",
        results: data,
        message: "Your song is ready!"
      }, null, 2));
    } else if (anyFailed) {
      console.log(JSON.stringify({
        success: false,
        status: "failed",
        results: data,
        message: "Generation failed. Try a different description!"
      }, null, 2));
    } else {
      console.log(JSON.stringify({
        success: true,
        status: "processing",
        results: data,
        message: "Still generating... Please check again in 30 seconds."
      }, null, 2));
    }
  } catch (err) {
    console.error(JSON.stringify({ 
      success: false, 
      message: `Request failed: ${err.message}` 
    }));
    process.exit(1);
  }
}

query();
