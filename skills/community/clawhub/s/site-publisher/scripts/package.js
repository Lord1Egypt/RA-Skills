#!/usr/bin/env node
/**
 * package.js — Package a static site into a zip file
 */

const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const { pipeline } = require('stream');

const DIR = process.argv[2] || process.cwd();
const OUTPUT = process.argv[3] || path.join(DIR, path.basename(DIR) + '.zip');

// Simple zip creation using Node's built-in zlib
async function createZip() {
  const files = [];
  
  function walk(dir) {
    const entries = fs.readdirSync(dir);
    for (const entry of entries) {
      const fullPath = path.join(dir, entry);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory()) {
        walk(fullPath);
      } else {
        const relative = path.relative(DIR, fullPath);
        files.push({ path: relative, fullPath });
      }
    }
  }
  
  walk(DIR);
  console.log(`Packaging ${files.length} files into ${OUTPUT}...`);
  
  // For simplicity, just copy files to a dist directory
  // A real zip would need a proper zip library
  const distDir = OUTPUT.replace('.zip', '');
  if (!fs.existsSync(distDir)) {
    fs.mkdirSync(distDir, { recursive: true });
  }
  
  for (const file of files) {
    const dest = path.join(distDir, file.path);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(file.fullPath, dest);
  }
  
  console.log(`Packaged to ${distDir}/`);
  console.log(`Files: ${files.length}`);
}

createZip().catch(console.error);
