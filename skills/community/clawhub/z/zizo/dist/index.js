#!/usr/bin/env node
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ 692:
/***/ ((module) => {

"use strict";
module.exports = require("https");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __nccwpck_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		var threw = true;
/******/ 		try {
/******/ 			__webpack_modules__[moduleId](module, module.exports, __nccwpck_require__);
/******/ 			threw = false;
/******/ 		} finally {
/******/ 			if(threw) delete __webpack_module_cache__[moduleId];
/******/ 		}
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat */
/******/ 	
/******/ 	if (typeof __nccwpck_require__ !== 'undefined') __nccwpck_require__.ab = __dirname + "/";
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};

const https = __nccwpck_require__(692);

const DEFAULT_CONFIG = {
  server: 'https://zizo.pro',
  token: '',
  defaults: {
    limit: 20,
    scope: 'public'
  }
};

// 获取配置，只从环境变量和默认值获取
function getConfig() {
  return {
    server: process.env.ZIZO_SERVER || DEFAULT_CONFIG.server,
    token: process.env.ZIZO_TOKEN || DEFAULT_CONFIG.token,
    defaults: {
      limit: parseInt(process.env.ZIZO_LIMIT) || DEFAULT_CONFIG.defaults.limit,
      scope: process.env.ZIZO_SCOPE || DEFAULT_CONFIG.defaults.scope
    }
  };
}

// MCP 调用
function callMCP(method, params) {
  return new Promise((resolve, reject) => {
    const config = getConfig();

    if (!config.token) {
      reject(new Error('Token not configured. Set ZIZO_TOKEN environment variable\nYou can get your token from: https://zizo.pro/#/?settings=token'));
      return;
    }

    const url = new URL(`${config.server}/mcp`);
    // 强制使用 HTTPS
    if (url.protocol !== 'https:') {
      reject(new Error('Server URL must use HTTPS protocol'));
      return;
    }
    const client = https;

    const body = JSON.stringify({
      jsonrpc: '2.0',
      id: Date.now(),
      method: method,
      params: params
    });

    const options = {
      hostname: url.hostname,
      port: url.port || 443,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
        'Authorization': `Bearer ${config.token}`
      }
    };

    const req = client.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.error) {
            reject(new Error(result.error.message || JSON.stringify(result.error)));
          } else {
            resolve(result.result);
          }
        } catch (e) {
          reject(new Error(`Invalid response: ${data}`));
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// 格式化输出
function formatOutput(results, type) {
  if (!results || results.length === 0) {
    console.log('No results found.');
    return;
  }

  results.forEach((item, index) => {
    console.log(`\n[${index + 1}] ${item.title || item.name || 'Untitled'}`);
    console.log(`    ID: ${item.id}`);

    if (type === 'images') {
      console.log(`    URL: ${item.url || item.thumbnail_url || item.thumbnail || ''}`);
      if (item.width && item.height) {
        console.log(`    Size: ${item.width}x${item.height}`);
      }
    } else if (type === 'boards') {
      console.log(`    Images: ${item.image_count || item.count || 0}`);
      if (item.description) {
        console.log(`    Desc: ${item.description.substring(0, 100)}...`);
      }
    }
  });
  console.log(`\nTotal: ${results.length} results`);
}

// 显示配置
function showConfig() {
  const config = getConfig();
  console.log('Configuration:');
  console.log(`  Server: ${process.env.ZIZO_SERVER ? `${config.server} (from ZIZO_SERVER)` : `${config.server} (default)`}`);
  console.log(`  Token: ${config.token ? '***' + config.token.slice(-4) + ` (from ZIZO_TOKEN)` : '(not set)'}`);
  console.log(`  Defaults:`);
  console.log(`    limit: ${process.env.ZIZO_LIMIT ? `${config.defaults.limit} (from ZIZO_LIMIT)` : `${config.defaults.limit} (default)`}`);
  console.log(`    scope: ${process.env.ZIZO_SCOPE ? `${config.defaults.scope} (from ZIZO_SCOPE)` : `${config.defaults.scope} (default)`}`);
  console.log(`\nNote: Configuration is only read from environment variables.`);
}

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('Usage: zizo <command> [options]');
    console.log('Commands:');
    console.log('  search images <query> [--limit <number>] [--scope <scope>]');
    console.log('  search boards <query> [--limit <number>]');
    console.log('  config show');
    console.log('  version');
    process.exit(0);
  }

  const command = args[0];
  
  if (command === 'version') {
    console.log('zizo v1.0.0');
    process.exit(0);
  }

  if (command === 'config' && args[1] === 'show') {
    showConfig();
    process.exit(0);
  }

  if (command === 'search') {
    const subCommand = args[1];
    const query = args[2];
    
    if (!subCommand || !query) {
      console.log('Usage: zizo search <images|boards> <query> [options]');
      process.exit(1);
    }

    let limit = 10;
    let scope = 'public';

    // 解析选项
    for (let i = 3; i < args.length; i++) {
      if (args[i] === '--limit' && i + 1 < args.length) {
        limit = parseInt(args[i + 1]);
        i++;
      } else if (args[i] === '--scope' && i + 1 < args.length) {
        scope = args[i + 1];
        i++;
      }
    }

    return {
      type: subCommand,
      query: query,
      limit: limit,
      scope: scope
    };
  }

  console.log('Unknown command:', command);
  process.exit(1);
}

// 主函数
async function main() {
  try {
    const args = parseArgs();
    
    if (args.type === 'images') {
      console.log(`Searching images for "${args.query}" (limit: ${args.limit}, scope: ${args.scope})...`);
      
      const result = await callMCP('tools/call', {
        name: 'search_images_by_text',
        arguments: {
          query: args.query,
          limit: args.limit,
          scope: args.scope
        }
      });

      // 解析 MCP 响应
      let content = result?.content;
      if (Array.isArray(content)) {
        // 找到 JSON 数据
        for (const item of content) {
          if (item.type === 'text' && item.text.startsWith('[')) {
            const data = JSON.parse(item.text);
            formatOutput(data, 'images');
            process.exit(0);
          }
        }
        // 如果没有 JSON，显示文本结果
        console.log(content.map(c => c.text).join('\n'));
      } else if (result?.images) {
        formatOutput(result.images, 'images');
      } else {
        formatOutput(result, 'images');
      }
    } else if (args.type === 'boards') {
      console.log(`Searching boards for "${args.query}" (limit: ${args.limit})...`);
      
      const result = await callMCP('tools/call', {
        name: 'search_boards',
        arguments: {
          query: args.query,
          limit: args.limit
        }
      });

      // 解析 MCP 响应
      let content = result?.content;
      if (Array.isArray(content) && content[0]?.text) {
        const data = JSON.parse(content[0].text);
        formatOutput(data.boards || data, 'boards');
      } else if (result?.boards) {
        formatOutput(result.boards, 'boards');
      } else {
        formatOutput(result, 'boards');
      }
    }
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

// 运行主函数
main();
module.exports = __webpack_exports__;
/******/ })()
;