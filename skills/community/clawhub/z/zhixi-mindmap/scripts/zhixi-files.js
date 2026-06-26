/**
 * 知犀思维导图 - 云文件操作
 */

const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.dirname(__dirname);

function getApiToken() {
  if (process.env.ZHIXI_API_KEY) {
    return process.env.ZHIXI_API_KEY.trim();
  }
  const tokenPath = path.join(SKILL_DIR, 'token');
  if (fs.existsSync(tokenPath)) {
    const token = fs.readFileSync(tokenPath, 'utf8').trim();
    if (token) return token;
  }
  throw new Error(`请配置 API Token:\n  方式1: export ZHIXI_API_KEY=your_token\n  方式2: echo "your_token" > ${tokenPath}`);
}

const CONFIG = {
  appId: '80001001',
  get authorization() {
    return getApiToken();
  },
  get userAgent() {
    return `OpenClaw node/${process.versions.node}`;
  },
  baseUrl: 'https://www.zhixi.com/api'
};

class ZhixiClient {
  constructor() {
    this.headers = {
      'Accept-language': 'zh-CN,zh;q=0.9',
      'AppID': CONFIG.appId,
      'User-Agent': CONFIG.userAgent,
      'X-Api-Key': CONFIG.authorization
    };
  }

  async getFiles(pid = "") {
    const api = `${CONFIG.baseUrl}/v1/file/index?pid=${pid || ""}`;
    const result = await this._fetch(api);
    if (result.code !== 0) return result;
    return this._formatFiles(result);
  }

  async getContent(fileId) {
    const api = `${CONFIG.baseUrl}/v1/file/details?file_guid=${fileId}`;
    const result = await this._fetch(api);
    if (result.code !== 0) return result;
    // console.debug(result.data?.content_url);
    const response = await fetch(result.data?.content_url);
    return response.json();
  }


  async search(keyword) {
    const api = `${CONFIG.baseUrl}/v1/file/index?title=${encodeURIComponent(keyword)}`;
    const result = await this._fetch(api);
    if (result.code !== 0) return result;
    return this._formatFiles(result);
  }

  async importMarkdown(content, filename, dirId = 0) {
    const formData = new FormData();
    formData.append('file', new Blob([content], { type: 'text/markdown' }), filename);
    formData.append('dirId', dirId.toString());

    const response = await fetch(`${CONFIG.baseUrl}/import/mind`, {
      method: 'POST',
      headers: this.headers,
      body: formData
    });
    const result = response.json();

    if (result.code === 2001) return {
      code: 2001,
      message: "请访问 https://www.zhixi.com/pricing?from=openclaw 开通会员解锁限制"
    };
    return result.code === 0 ? {
      file_guid: result.fileId,
    } : result;
  }

  async _fetch(url) {
    const response = await fetch(url, {
      headers: { ...this.headers, 'Content-Type': 'application/json' }
    });
    return response.json();
  }

  _formatFiles(result) {
    const data = result.data?.data || [];
    return data.map(f => ({
      title: f.title,
      file_guid: f.file_guid,
      id: f.id,
      type: f.item_type === 2 ? 'folder' : 'file'
    }));
  }
}

function walk(tree, cb, depth = 1) {
  let children = tree.children;
  if (!Array.isArray(children)) {
    children = tree.children?.normal || [];
    if (tree.children?.summary) children.concat(tree.children.summary);
  }
  cb(depth, tree.data);
  for (const node of children) {
    walk(node, cb, depth + 1);
  }
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks);
}

async function main() {
  const args = process.argv.slice(2);
  const client = new ZhixiClient();

  if (args[0] === 'search') {
    if (!args[1]) {
      console.log('用法: node zhixi-files.js search <关键字>');
      process.exit(1);
    }
    const files = await client.search(args[1]);
    // console.debug(`搜索: "${args[1]}" (${files.length} 个结果)`);
    console.log(JSON.stringify(files, null, 2));
    return;
  }

  if (args[0] === 'content') {
    if (!args[1]) {
      console.log('用法: node zhixi-files.js content <fileId>');
      process.exit(1);
    }
    const result = await client.getContent(args[1]);
    if (result.contents || result.root) {
      walk(result.root || result.contents[0].root, (depth, data) => {
        let marker = "#".repeat(depth);
        if (depth > 4) marker = "  ".repeat(depth - 4) + "-";
        else if (depth > 1) marker = "\n" + marker;

        if (data.text) console.log(`${marker} ${data.text}`);
      });
    } else {
      console.log(result);
    }
    return;
  }

  if (args[0] === 'import') {
    let content, filename;

    const inputFile = args[1] || '-';
    if (inputFile !== '-') {
      try {
        content = await fs.promises.readFile(inputFile);
        filename = inputFile.split('/').pop();
      } catch (e) {
        console.error(`文件不存在: ${inputFile}`);
        process.exit(1);
      }
    } else {
      content = await readStdin();
      filename = 'mindmap.md';
    }

    const dirId = args.includes('--dir') ? args[args.indexOf('--dir') + 1] || 0 : 0;
    // console.debug(`导入: ${filename} → 目录ID ${dirId}`);

    const result = await client.importMarkdown(content, filename, dirId);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (['help', '--help', '-h'].includes(args[0])) {
    console.log(`用法:
  node zhixi-files.js [dirId]            获取文件列表
  node zhixi-files.js content <fileId>   获取文件内容
  node zhixi-files.js search <关键字>    搜索
  node zhixi-files.js import <file> [--dir <id>]   导入Markdown`);
    return;
  }

  const files = await client.getFiles(args[0]);
  console.log(JSON.stringify(files, null, 2));
}

main().catch(e => console.error('错误:', e.message));
