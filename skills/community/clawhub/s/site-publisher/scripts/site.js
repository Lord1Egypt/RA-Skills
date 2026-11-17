#!/usr/bin/env node
/**
 * site.js — Module wrapper for site-publisher skill
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const mimeTypes = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

/**
 * Serve a static site directory via HTTP.
 * @param {number} port - Port number
 * @param {string} dir - Directory to serve
 * @returns {Promise<http.Server>}
 */
function serveSite(port, dir) {
  const PORT = port || 3000;
  const DIR = path.resolve(dir || process.cwd());

  const server = http.createServer((req, res) => {
    let filePath = path.join(DIR, req.url === '/' ? 'index.html' : req.url);
    const ext = path.extname(filePath).toLowerCase();
    const contentType = mimeTypes[ext] || 'application/octet-stream';

    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404);
        res.end('Not found');
        return;
      }
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(data);
    });
  });

  return new Promise((resolve, reject) => {
    server.listen(PORT, () => {
      console.log(`Serving ${DIR} at http://localhost:${PORT}`);
      resolve(server);
    });
    server.on('error', reject);
  });
}

/**
 * Package a static site into a tar.gz archive.
 * @param {string} dir - Directory to package
 * @param {string} output - Output file path
 */
function packageSite(dir, output) {
  const DIR = path.resolve(dir || process.cwd());
  const OUTPUT = output || path.join(DIR, 'site-package.tar.gz');

  if (!fs.existsSync(DIR)) {
    throw new Error(`Directory not found: ${DIR}`);
  }

  try {
    execSync(`tar -czf ${JSON.stringify(OUTPUT)} -C ${JSON.stringify(DIR)} .`, { encoding: 'utf8', stdio: 'pipe' });
    console.log(`Packaged ${DIR} => ${OUTPUT}`);
    return OUTPUT;
  } catch (e) {
    throw new Error(`Packaging failed: ${e.message}`);
  }
}

// CLI mode
if (require.main === module) {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (cmd === 'serve' || cmd === '--serve') {
    const port = parseInt(args[1]) || 3000;
    const dir = args[2] || process.cwd();
    serveSite(port, dir).catch(err => {
      console.error('Serve failed:', err.message);
      process.exit(1);
    });
  } else if (cmd === 'package' || cmd === '--package') {
    const dir = args[1] || process.cwd();
    const output = args[2];
    try {
      packageSite(dir, output);
    } catch (e) {
      console.error('Package failed:', e.message);
      process.exit(1);
    }
  } else {
    console.log('Usage: site-publisher <serve|package> [options]');
    console.log('  serve <port> <dir>    Serve static site (default port 3000)');
    console.log('  package <dir> <out>   Package site into tar.gz');
    process.exit(0);
  }
}

module.exports = { serveSite, packageSite };
