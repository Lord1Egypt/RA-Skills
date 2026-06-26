#!/usr/bin/env node
/**
 * youtube-transcript skill
 * Uses yt-dlp to fetch subtitles, then cleans and outputs plain text.
 * Usage: node transcript.js <youtube-url-or-id> [lang]
 */

const { execSync, spawnSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

function extractVideoId(input) {
  const patterns = [
    /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})/,
    /^([a-zA-Z0-9_-]{11})$/,
  ];
  for (const p of patterns) {
    const m = input.match(p);
    if (m) return m[1];
  }
  return null;
}

function cleanVtt(vttContent) {
  const lines = vttContent.split('\n');
  const seen = new Set();
  const result = [];

  for (const line of lines) {
    // Skip headers, timestamps, empty lines
    if (!line.trim()) continue;
    if (line.startsWith('WEBVTT') || line.startsWith('Kind:') || line.startsWith('Language:')) continue;
    if (/^\d{2}:\d{2}:\d{2}/.test(line)) continue;  // timestamps
    if (/^\d{2}:\d{2}\.\d{3}/.test(line)) continue;  // short timestamps

    // Strip HTML tags
    const cleaned = line
      .replace(/<[^>]+>/g, '')
      .replace(/&amp;/g, '&')
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .trim();

    if (!cleaned) continue;

    // Deduplicate (auto-captions repeat lines)
    if (!seen.has(cleaned)) {
      seen.add(cleaned);
      result.push(cleaned);
    }
  }

  return result.join(' ');
}

function getYtDlpPath() {
  try {
    return execSync('which yt-dlp', { encoding: 'utf8' }).trim();
  } catch {
    // Try common paths
    const paths = ['/opt/homebrew/bin/yt-dlp', '/usr/local/bin/yt-dlp', '/usr/bin/yt-dlp'];
    for (const p of paths) {
      if (fs.existsSync(p)) return p;
    }
    throw new Error('yt-dlp not found. Install with: brew install yt-dlp');
  }
}

async function getTranscript(videoId, lang = 'pt') {
  const ytdlp = getYtDlpPath();
  const tmpDir = os.tmpdir();
  const outBase = path.join(tmpDir, `yt_${videoId}_${Date.now()}`);
  const url = `https://www.youtube.com/watch?v=${videoId}`;

  // Try requested lang first, then 'en'
  for (const tryLang of [lang, 'en']) {
    const outFile = `${outBase}.${tryLang}.vtt`;

    const result = spawnSync(ytdlp, [
      '--write-auto-sub',
      '--skip-download',
      '--sub-lang', tryLang,
      '--sub-format', 'vtt',
      '-o', outBase,
      '--quiet',
      '--no-warnings',
      url,
    ], { encoding: 'utf8', timeout: 30000 });

    if (fs.existsSync(outFile)) {
      const vtt = fs.readFileSync(outFile, 'utf8');
      fs.unlinkSync(outFile);
      return {
        language: tryLang,
        text: cleanVtt(vtt),
      };
    }
  }

  // Cleanup any leftover files
  try {
    const files = fs.readdirSync(tmpDir).filter(f => f.startsWith(`yt_${videoId}`));
    files.forEach(f => fs.unlinkSync(path.join(tmpDir, f)));
  } catch {}

  throw new Error('No transcript available for this video in the requested language.');
}

async function main() {
  const input = process.argv[2];
  const lang = process.argv[3] || 'pt';

  if (!input) {
    console.error('Usage: node transcript.js <youtube-url-or-id> [lang]');
    console.error('Example: node transcript.js https://www.youtube.com/watch?v=abc123 en');
    process.exit(1);
  }

  const videoId = extractVideoId(input);
  if (!videoId) {
    console.error('Error: Invalid YouTube URL or video ID.');
    process.exit(1);
  }

  try {
    const result = await getTranscript(videoId, lang);
    process.stdout.write(`[Language: ${result.language}]\n\n`);
    process.stdout.write(result.text + '\n');
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

main();
