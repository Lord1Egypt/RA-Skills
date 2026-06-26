#!/usr/bin/env node
/**
 * Web Automation Helper
 * Chrome CDP连接和基本操作
 */

const http = require('http');

// 获取Chrome WebSocket URL
function getChromeWSUrl() {
  return new Promise((resolve, reject) => {
    http.get('http://localhost:9222/json/version', (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.webSocketDebuggerUrl);
        } catch (e) {
          reject(new Error('Failed to parse Chrome debug info'));
        }
      });
    }).on('error', reject);
  });
}

async function main() {
  const args = process.argv.slice(2);
  const urlArg = args.find(a => a.startsWith('--url='));
  const url = urlArg ? urlArg.split('=')[1] : 'https://example.com';

  console.log('Web Automation Helper');
  console.log('====================');
  console.log('URL:', url);
  console.log('Chrome must be running with --remote-debugging-port=9222');
  
  try {
    const wsUrl = await getChromeWSUrl();
    console.log('WS URL:', wsUrl);
    console.log('Status: Connected');
  } catch (e) {
    console.log('Error:', e.message);
    console.log('Make sure Chrome is running with: chrome.exe --remote-debugging-port=9222');
  }
}

main();
