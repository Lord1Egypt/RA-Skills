#!/usr/bin/env node

/**
 * Universal Video to S3 Uploader - CLI Entry Point
 * 
 * This is the main entry point for the CLI commands.
 * It routes to the appropriate script based on the command name.
 */

const path = require('path');
const fs = require('fs');

// Get the command name (youtube-s3-upload or video-s3-upload)
const commandName = path.basename(process.argv[1]);

// Show help if no arguments
if (process.argv.length < 3) {
  showHelp(commandName);
  process.exit(1);
}

const videoUrl = process.argv[2];

// Check for help flags
if (videoUrl === '--help' || videoUrl === '-h') {
  showHelp(commandName);
  process.exit(0);
}

// Check for version flag
if (videoUrl === '--version' || videoUrl === '-v') {
  const packageJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json'), 'utf8'));
  console.log(`${packageJson.name} v${packageJson.version}`);
  console.log(packageJson.description);
  process.exit(0);
}

// Route to the appropriate script
if (commandName === 'youtube-s3-upload') {
  // Use the YouTube-specific script
  console.log('🎬 YouTube to S3 Uploader');
  console.log('='.repeat(50));
  require('./scripts/youtube-to-s3.js');
  
} else if (commandName === 'video-s3-upload') {
  // Use the universal video script
  console.log('🌐 Universal Video to S3 Uploader');
  console.log('='.repeat(50));
  require('./scripts/video-to-s3-universal.js');
  
} else {
  console.error(`❌ Unknown command: ${commandName}`);
  console.log('Available commands:');
  console.log('  youtube-s3-upload - Download YouTube videos');
  console.log('  video-s3-upload   - Download videos from any platform');
  process.exit(1);
}

function showHelp(commandName) {
  const packageJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json'), 'utf8'));
  
  console.log('='.repeat(70));
  
  if (commandName === 'youtube-s3-upload') {
    console.log('🎬 YouTube to S3 Uploader');
    console.log('='.repeat(70));
    console.log('Download YouTube videos and upload them to S3-compatible storage');
    console.log('');
    console.log('Usage:');
    console.log(`  ${commandName} <YouTube URL>`);
    console.log('');
    console.log('Examples:');
    console.log(`  ${commandName} https://youtu.be/VIDEO_ID`);
    console.log(`  ${commandName} https://www.youtube.com/watch?v=VIDEO_ID`);
    
  } else if (commandName === 'video-s3-upload') {
    console.log('🌐 Universal Video to S3 Uploader');
    console.log('='.repeat(70));
    console.log('Download videos from multiple platforms and upload to S3');
    console.log('');
    console.log('Supported platforms:');
    console.log('  • YouTube (youtube.com, youtu.be)');
    console.log('  • Twitter/X (x.com, twitter.com)');
    console.log('  • TikTok (tiktok.com)');
    console.log('  • 抖音 (douyin.com)');
    console.log('  • B站 (bilibili.com)');
    console.log('  • Instagram (instagram.com)');
    console.log('  • Facebook (facebook.com)');
    console.log('  • Twitch (twitch.tv)');
    console.log('  • And 1000+ more sites supported by yt-dlp');
    console.log('');
    console.log('Usage:');
    console.log(`  ${commandName} <视频URL>`);
    console.log('');
    console.log('Examples:');
    console.log(`  ${commandName} https://youtu.be/VIDEO_ID`);
    console.log(`  ${commandName} https://x.com/user/status/1234567890`);
    console.log(`  ${commandName} https://www.tiktok.com/@user/video/1234567890`);
    
  } else {
    console.log('Universal Video to S3 Uploader');
    console.log('='.repeat(70));
    console.log('Available commands:');
    console.log('  youtube-s3-upload - Download YouTube videos');
    console.log('  video-s3-upload   - Download videos from any platform');
  }
  
  console.log('');
  console.log('Options:');
  console.log('  --help, -h     Show this help message');
  console.log('  --version, -v  Show version information');
  console.log('');
  console.log(`Version: ${packageJson.version}`);
  console.log('='.repeat(70));
}

// Pass the URL to the script
// The scripts will access process.argv[2] directly