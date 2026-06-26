#!/usr/bin/env node

/**
 * Understand Image Skill
 * Uses Minimax Coding Plan VLM API to analyze images
 * 
 * Usage:
 *   node understand.cjs "prompt" "image_url_or_path"
 *   node understand.cjs "描述这张图片" "https://example.com/image.jpg"
 *   node understand.cjs "这张图片有什么" "/path/to/local/image.png"
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

const args = process.argv.slice(2);
if (args.length < 2) {
  console.error("Usage: understand.cjs <prompt> <image_url_or_path>");
  console.error("Example: node understand.cjs \"描述这张图片\" \"https://example.com/image.jpg\"");
  process.exit(1);
}

const prompt = args[0];
let imageSource = args[1];

async function processImageUrl(imageUrl) {
  // If already in base64 data URL format, pass through
  if (imageUrl.startsWith("data:")) {
    return imageUrl;
  }
  
  // Handle local file paths
  if (!imageUrl.startsWith("http://") && !imageUrl.startsWith("https://")) {
    // Resolve relative paths
    let resolvedPath = imageUrl;
    if (!path.isAbsolute(imageUrl)) {
      resolvedPath = path.resolve(process.cwd(), imageUrl);
    }
    
    if (!fs.existsSync(resolvedPath)) {
      throw new Error(`Local image file does not exist: ${resolvedPath}`);
    }
    
    const ext = path.extname(resolvedPath).toLowerCase();
    const mimeTypes = {
      ".jpg": "image/jpeg",
      ".jpeg": "image/jpeg",
      ".png": "image/png",
      ".gif": "image/gif",
      ".webp": "image/webp"
    };
    const mimeType = mimeTypes[ext] || "image/jpeg";
    
    const imageBuffer = fs.readFileSync(resolvedPath);
    const base64 = imageBuffer.toString("base64");
    return `data:${mimeType};base64,${base64}`;
  }
  
  // Handle HTTP/HTTPS URLs - download and convert to base64
  console.error(`Downloading image from ${imageUrl}...`);
  
  try {
    const response = await fetch(imageUrl);
    
    if (!response.ok) {
      throw new Error(`Failed to download image: ${response.status} ${response.statusText}`);
    }
    
    const buffer = await response.arrayBuffer();
    const base64 = Buffer.from(buffer).toString("base64");
    
    // Detect content type
    const contentType = response.headers.get("content-type") || "image/jpeg";
    let format = "jpeg";
    if (contentType.includes("png")) format = "png";
    else if (contentType.includes("webp")) format = "webp";
    else if (contentType.includes("gif")) format = "gif";
    
    return `data:image/${format};base64,${base64}`;
  } catch (err) {
    throw new Error(`Failed to download image: ${err.message}`);
  }
}

async function understandImage() {
  // Process image to base64 data URL
  const processedImageUrl = await processImageUrl(imageSource);
  
  const url = `${API_HOST}/v1/coding_plan/vlm`;
  
  const body = {
    prompt: prompt,
    image_url: processedImageUrl
  };
  
  console.error(`Calling Minimax VLM API...`);
  console.error(`Prompt: ${prompt}`);
  
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${API_KEY}`,
      "MM-API-Source": "Minimax-Skill"
    },
    body: JSON.stringify(body)
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
  
  // Output the result
  const content = data.content;
  if (content) {
    console.log(content);
  } else {
    console.error("No content returned from API");
    process.exit(1);
  }
}

understandImage().catch(err => {
  console.error("Error:", err.message);
  process.exit(1);
});
