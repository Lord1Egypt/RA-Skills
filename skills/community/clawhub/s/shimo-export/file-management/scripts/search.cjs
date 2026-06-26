/**
 * 石墨文档搜索脚本
 *
 * 按关键词搜索石墨文档中的文件。
 *
 * 使用方法:
 *   node search.cjs --keyword <关键词> [options]
 *   node search.cjs --type <类型>               (无关键词，仅按类型筛选)
 *
 * 选项:
 *   --keyword KW  - 搜索关键词（可选，不传则返回该类型的所有文件）
 *   --size N      - 返回结果数量 (默认 15)
 *   --type TYPE   - 按文件类型筛选: newdoc, modoc, mosheet, presentation, mindmap
 *   --full-text   - 全文搜索 (默认仅搜索文件名)
 *
 * 环境变量:
 *   SHIMO_COOKIE - shimo_sid 的值 (优先使用)
 *   或者使用配置文件 config/env.json
 *
 * 输出:
 *   JSON 数组到 stdout
 *
 * Exit codes:
 *   0 - 搜索成功
 *   1 - 搜索失败
 */

// --- Configuration ---

const SEARCH_API = 'https://shimo.im/lizard-api/search_v2/files';

const HEADERS = {
  'Referer': 'https://shimo.im/desktop',
  'Accept': 'application/nd.shimo.v2+json, text/plain, */*',
  'X-Requested-With': 'SOS 2.0',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
};

// --- Helpers ---

function loadCookie() {
  return process.env.SHIMO_COOKIE || null;
}

function getHeaders(cookie) {
  return {
    ...HEADERS,
    'Cookie': `shimo_sid=${cookie}`,
    'Content-Type': 'application/json',
  };
}

function outputResult(result) {
  console.log(JSON.stringify(result, null, 2));
}

function parseArgs(args) {
  const result = { keyword: null, size: 15, fileType: '', fullText: false };

  let i = 0;
  while (i < args.length) {
    if (args[i] === '--keyword' && i + 1 < args.length) {
      result.keyword = args[i + 1];
      i += 2;
    } else if (args[i] === '--size' && i + 1 < args.length) {
      result.size = parseInt(args[i + 1], 10) || 15;
      i += 2;
    } else if (args[i] === '--type' && i + 1 < args.length) {
      result.fileType = args[i + 1];
      i += 2;
    } else if (args[i] === '--full-text') {
      result.fullText = true;
      i += 1;
    } else if (!args[i].startsWith('--') && !result.keyword) {
      // 兼容旧的位置参数用法
      result.keyword = args[i];
      i += 1;
    } else {
      i += 1;
    }
  }

  return result;
}

// --- Main ---

async function main() {
  const args = process.argv.slice(2);
  const opts = parseArgs(args);

  if (!opts.keyword && !opts.fileType) {
    process.stderr.write('用法: node search.cjs --keyword <关键词> [--size N] [--type TYPE] [--full-text]\n');
    process.stderr.write('      node search.cjs --type <类型> [--size N]\n');
    process.stderr.write('\n');
    process.stderr.write('选项:\n');
    process.stderr.write('  --keyword KW   搜索关键词\n');
    process.stderr.write('  --size N       返回结果数量 (默认 15)\n');
    process.stderr.write('  --type TYPE    文件类型筛选: newdoc, modoc, mosheet, presentation, mindmap\n');
    process.stderr.write('  --full-text    全文搜索 (默认仅搜索文件名)\n');
    process.exit(1);
  }

  const cookie = loadCookie();
  if (!cookie) {
    outputResult({ error: '未找到石墨凭证。请先运行 browser-login.cjs 或设置 SHIMO_COOKIE 环境变量。' });
    process.exit(1);
  }

  const headers = getHeaders(cookie);

  const body = {
    keyword: opts.keyword || ' ',
    fileType: opts.fileType,
    category: '',
    createdBy: '',
    createdAtBegin: '',
    createdAtEnd: '',
    searchFields: opts.fullText ? '' : 'name',
    desktop: false,
    spaceGuids: [],
    size: opts.size,
    params: '',
  };

  try {
    const response = await fetch(SEARCH_API, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
    });

    if (response.status === 401) {
      outputResult({ error: '凭证已过期，请重新登录。' });
      process.exit(1);
    }

    if (!response.ok) {
      outputResult({ error: `搜索失败: HTTP ${response.status} ${response.statusText}` });
      process.exit(1);
    }

    const data = await response.json();
    const results = (data.results || []).map(r => {
      const s = r.source || {};
      const ancestors = s.ancestors || [];
      const folderPath = ancestors.map(a => a.name).join('/');

      return {
        guid: s.guid,
        name: s.name,
        type: s.type,
        path: folderPath || '',
      };
    });

    outputResult(results);

  } catch (error) {
    outputResult({ error: error.message });
    process.exit(1);
  }
}

main().catch(error => {
  outputResult({ error: error.message });
  process.exit(1);
});
