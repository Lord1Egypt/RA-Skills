#!/usr/bin/env node

const API_BASE = process.env.MBM_API_BASE || "https://api.makebestmusic.com";
const API_KEY = process.env.apiKey;

if (!API_KEY) {
  console.error(JSON.stringify({ code: -1, message: "Missing apiKey - please fill in the apiKey field in skill settings" }));
  process.exit(1);
}

const prompt = process.argv[2];
const instrumental = process.argv[3] === "true";

if (!prompt) {
  console.error(JSON.stringify({ code: -1, message: "Missing music description parameter" }));
  console.error("Usage: node generate.js <prompt> [instrumental(true/false)]");
  process.exit(1);
}

async function generate() {
  try {
    const res = await fetch(`${API_BASE}/api/skill/generate_music`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${API_KEY}`,
      },
      body: JSON.stringify({
        model: "Fi",
        custom: true,
        instrumental: instrumental,
        prompt: prompt,
        title: "",
        style: "",
        advance: {
          vocal_gender: "",
          ai_lyrics: true
        }
      }),
    });

    const data = await res.json();
    
    if (data.music_ids && data.music_ids.length > 0) {
      console.log(JSON.stringify({
        success: true,
        music_ids: data.music_ids,
        status: data.status,
        message: "Music generation started! I'll check back in 30 seconds..."
      }, null, 2));
    } else {
      console.log(JSON.stringify({
        success: false,
        message: data.message || "Generation failed"
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

generate();
