#!/usr/bin/env node
/**
 * Instagram Post via instagrapi (Python)
 * Posts photos, reels, carousels, and stories to Instagram
 * 
 * Requires: pip3 install instagrapi pillow
 * Auth: Set IG_USERNAME and IG_PASSWORD env vars, or pass --username/--password
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Parse args
const args = process.argv.slice(2);
let action = 'photo'; // photo, reel, story, carousel
let caption = '';
let mediaFiles = [];
let username = process.env.IG_USERNAME || '';
let password = process.env.IG_PASSWORD || '';
let sessionFile = path.join(process.env.HOME || '', '.openclaw', 'ig_session.json');

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--action' && args[i + 1]) { action = args[i + 1]; i++; }
  else if (args[i] === '--caption' && args[i + 1]) { caption = args[i + 1]; i++; }
  else if (args[i] === '--media' && args[i + 1]) { mediaFiles.push(args[i + 1]); i++; }
  else if (args[i] === '--username' && args[i + 1]) { username = args[i + 1]; i++; }
  else if (args[i] === '--password' && args[i + 1]) { password = args[i + 1]; i++; }
  else if (args[i] === '--session' && args[i + 1]) { sessionFile = args[i + 1]; i++; }
  else if (!args[i].startsWith('--')) { mediaFiles.push(args[i]); }
}

if (mediaFiles.length === 0) {
  console.error(`Usage: instagram-post.js [--action photo|reel|story|carousel] [--caption "text"] [--username x] [--password x] <media_file(s)>`);
  console.error(`\nActions:`);
  console.error(`  photo     - Post a single photo (default)`);
  console.error(`  reel      - Post a video reel`);
  console.error(`  story     - Post a story (photo or video)`);
  console.error(`  carousel  - Post multiple photos as carousel`);
  console.error(`\nEnv vars: IG_USERNAME, IG_PASSWORD`);
  process.exit(1);
}

if (!username || !password) {
  console.error('❌ Instagram credentials required.');
  console.error('   Set IG_USERNAME and IG_PASSWORD env vars');
  console.error('   Or use --username and --password flags');
  process.exit(1);
}

// Validate media files exist
for (const f of mediaFiles) {
  if (!fs.existsSync(f)) {
    console.error(`❌ File not found: ${f}`);
    process.exit(1);
  }
}

// Build Python script
const escapePy = (s) => s.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/\n/g, '\\n');
const mediaListPy = mediaFiles.map(f => `'${escapePy(path.resolve(f))}'`).join(', ');

const pyScript = `
import json, os, sys
from pathlib import Path
from instagrapi import Client

cl = Client()
session_file = '${escapePy(sessionFile)}'

# Try loading session
if os.path.exists(session_file):
    try:
        cl.load_settings(session_file)
        cl.login('${escapePy(username)}', '${escapePy(password)}')
        cl.get_timeline_feed()  # test session
        print("✅ Logged in via saved session")
    except Exception as e:
        print(f"⚠️ Session expired, re-logging: {e}")
        cl = Client()
        cl.login('${escapePy(username)}', '${escapePy(password)}')
        cl.dump_settings(session_file)
else:
    cl.login('${escapePy(username)}', '${escapePy(password)}')
    cl.dump_settings(session_file)
    print("✅ Logged in fresh, session saved")

caption = '''${escapePy(caption)}'''
media_files = [${mediaListPy}]
action = '${action}'

try:
    if action == 'photo':
        result = cl.photo_upload(media_files[0], caption)
        print(f"📸 Photo posted! https://instagram.com/p/{result.code}")
    elif action == 'reel':
        result = cl.clip_upload(media_files[0], caption)
        print(f"🎬 Reel posted! https://instagram.com/reel/{result.code}")
    elif action == 'story':
        ext = Path(media_files[0]).suffix.lower()
        if ext in ['.mp4', '.mov']:
            result = cl.video_upload_to_story(media_files[0], caption)
        else:
            result = cl.photo_upload_to_story(media_files[0], caption)
        print(f"📖 Story posted!")
    elif action == 'carousel':
        result = cl.album_upload(media_files, caption)
        print(f"🎠 Carousel posted! https://instagram.com/p/{result.code}")
    else:
        print(f"❌ Unknown action: {action}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Post failed: {e}")
    sys.exit(1)
`;

console.log(`📤 Posting ${action} to Instagram...`);

try {
  const result = execSync(`python3 -c '${pyScript.replace(/'/g, "'\"'\"'")}'`, {
    encoding: 'utf8',
    timeout: 120000,
    stdio: ['pipe', 'pipe', 'pipe'],
  });
  console.log(result);
} catch (e) {
  console.error('❌ Failed:', e.stderr || e.message);
  process.exit(1);
}
