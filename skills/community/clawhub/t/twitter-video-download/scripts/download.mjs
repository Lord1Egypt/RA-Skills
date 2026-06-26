#!/usr/bin/env node

/**
 * Twitter Video Downloader
 * Downloads videos from Twitter/X posts using yt-dlp
 * 
 * Security: Uses array form for spawn (no shell injection risk)
 */

import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Resolve base directory (parent of scripts folder)
const baseDir = path.resolve(__dirname, '..');

/**
 * Parse command line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  let url = '';
  let output = process.cwd();
  let filename = '';
  let quality = 'best';

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    // URL detection
    if (arg.startsWith('http://') || arg.startsWith('https://')) {
      url = arg;
    } else if ((arg === '-o' || arg === '--output') && args[i + 1]) {
      output = args[++i];
    } else if ((arg === '-f' || arg === '--filename') && args[i + 1]) {
      filename = args[++i];
    } else if ((arg === '-q' || arg === '--quality') && args[i + 1]) {
      quality = args[++i];
    }
  }

  return { url, output, filename, quality };
}

/**
 * Validate URL is a valid Twitter/X URL
 */
function validateUrl(url) {
  try {
    const urlObj = new URL(url);
    const hostname = urlObj.hostname.toLowerCase();
    return hostname === 'twitter.com' || hostname === 'x.com' || hostname === 'www.twitter.com' || hostname === 'www.x.com';
  } catch {
    return false;
  }
}

/**
 * Sanitize filename to prevent path traversal
 */
function sanitizeFilename(filename) {
  // Remove any path separators or dangerous characters
  return filename.replace(/[<>:"/\\|?*]/g, '_');
}

/**
 * Main download function
 */
async function download() {
  const { url, output, filename, quality } = parseArgs();

  // Validate URL parameter
  if (!url) {
    console.error('Error: Please provide a Twitter/X URL');
    console.log('Usage: node download.mjs <twitter_url> [--output <dir>] [--filename <name>] [--quality <quality>]');
    console.log('Example: node download.mjs "https://x.com/user/status/123456789" --output "./downloads"');
    process.exit(1);
  }

  // Validate URL format
  if (!validateUrl(url)) {
    console.error('Error: Please provide a valid Twitter or X URL (twitter.com or x.com)');
    process.exit(1);
  }

  // Sanitize output path
  const safeOutput = path.resolve(output);
  
  // Ensure output directory exists
  if (!fs.existsSync(safeOutput)) {
    fs.mkdirSync(safeOutput, { recursive: true });
  }

  // Build output filename template
  const sanitizedFilename = filename ? sanitizeFilename(filename) : '%(title)s';
  const outputTemplate = path.join(safeOutput, `${sanitizedFilename}.%(ext)s`);
  
  // Build yt-dlp arguments (array form - safe, no shell injection)
  const ydlArgs = [
    '-f', `${quality}[ext=mp4]/best`,
    '--output', outputTemplate,
    '--no-warnings',
    '--socket-timeout', '30',
    '--no-check-certificate'  // Only if needed for proxy
  ];

  // Add proxy if set (environment variable)
  const proxy = process.env.PROXY_URL;
  if (proxy) {
    // Validate proxy URL format
    if (proxy.startsWith('http://') || proxy.startsWith('https://') || proxy.startsWith('socks5://')) {
      ydlArgs.push('--proxy', proxy);
      console.log(`Using proxy: ${proxy}`);
    } else {
      console.warn('Warning: PROXY_URL should start with http://, https:// or socks5://');
    }
  }

  console.log(`Downloading: ${url}`);
  console.log(`Output: ${safeOutput}`);
  if (filename) console.log(`Filename: ${filename}`);

  // Execute yt-dlp with array arguments (SECURE - no shell=true)
  return new Promise((resolve, reject) => {
    const ytDlp = spawn('yt-dlp', [...ydlArgs, url], {
      stdio: 'inherit',
      shell: false  // SECURITY: Explicitly disabled shell execution
    });

    ytDlp.on('close', (code) => {
      if (code === 0) {
        console.log('✅ Download complete!');
        
        // List recently downloaded files
        try {
          const files = fs.readdirSync(safeOutput);
          const videoFiles = files
            .filter(f => f.endsWith('.mp4') || f.endsWith('.webm') || f.endsWith('.mkv'))
            .map(f => ({
              name: f,
              path: path.join(safeOutput, f),
              mtime: fs.statSync(path.join(safeOutput, f)).mtime
            }))
            .sort((a, b) => b.mtime - a.mtime);
          
          if (videoFiles.length > 0) {
            const latestFile = videoFiles[0];
            console.log(`📁 Saved to: ${latestFile.path}`);
          }
        } catch (err) {
          // Ignore file listing errors
        }
        
        resolve();
      } else {
        console.error(`❌ Download failed with code ${code}`);
        reject(new Error(`yt-dlp exited with code ${code}`));
      }
    });

    ytDlp.on('error', (err) => {
      if (err.code === 'ENOENT') {
        console.error('❌ Error: yt-dlp not found');
        console.log('Please install yt-dlp first: pip install yt-dlp');
      } else {
        console.error('❌ Error running yt-dlp:', err.message);
      }
      reject(err);
    });
  });
}

// Run with error handling
download()
  .catch(err => {
    console.error('Fatal error:', err.message);
    process.exit(1);
  });
