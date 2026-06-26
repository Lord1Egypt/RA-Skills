/**
 * A股 API Client
 *
 * 安全说明（Security Notice）
 * ─────────────────────────────────────────────────────────────────
 * 此脚本仅做两件事：
 *   1. 从本地 .env 文件或环境变量中读取 ASTOCK_API_KEY
 *   2. 将该 Key 作为 HTTP Header 发送至 https://api.aipmedia.cn
 *
 * 不会读取任何其他文件，不会上传本地文件内容，
 * 不会将 .env 文件内容发送至任何地址。
 * Key 仅用于 API 认证，不做任何记录或持久化。
 * ─────────────────────────────────────────────────────────────────
 *
 * 使用方式：
 *   npx tsx api-client.ts <endpoint> [params_json]
 *
 * 示例：
 *   npx tsx api-client.ts /api/stock/sse_summary
 *   npx tsx api-client.ts /api/stock/individual_info_em '{"symbol":"600519"}'
 *
 * apiKey 读取优先级：
 *   1. 项目根目录 .env 文件中的 ASTOCK_API_KEY
 *   2. 环境变量 ASTOCK_API_KEY
 *   3. 以上均无 → 提示用户配置后退出，不做任何网络请求
 */

import * as fs from "fs";
import * as path from "path";

const BASE_URL = "https://api.aipmedia.cn";

// ─── 读取 apiKey（仅读 ASTOCK_API_KEY，不读取其他内容）──────────
function loadApiKey(): string | null {
  // 1. 尝试读取 .env 文件（仅解析 ASTOCK_API_KEY 行，忽略其他所有内容）
  const searchDirs = [process.cwd(), path.resolve(process.cwd(), "..")];
  for (const dir of searchDirs) {
    const envPath = path.join(dir, ".env");
    if (fs.existsSync(envPath)) {
      const lines = fs.readFileSync(envPath, "utf-8").split("\n");
      for (const line of lines) {
        // 只处理 ASTOCK_API_KEY 这一行，其余行直接跳过
        const match = line.match(/^ASTOCK_API_KEY\s*=\s*(.+)$/);
        if (match) return match[1].trim().replace(/^["']|["']$/g, "");
      }
    }
  }
  // 2. 尝试环境变量
  if (process.env.ASTOCK_API_KEY) return process.env.ASTOCK_API_KEY;
  return null;
}

// ─── 提示缺少 apiKey（不发起任何网络请求）──────────────────────
function promptMissingKey(): never {
  console.error(`
❌ 未找到 ASTOCK_API_KEY。

配置方法（请勿在聊天窗口中粘贴 API Key）：

  方式一（推荐）：在项目根目录创建 .env 文件：
    echo "ASTOCK_API_KEY=你的apiKey" >> .env

  方式二：设置环境变量：
    export ASTOCK_API_KEY=你的apiKey

  获取 API Key：https://aipmedia.cn/ → 登录 → 个人中心
`);
  process.exit(1);
}

// ─── 核心请求（Key 仅用于 Authorization Header，不上传其他数据）──
async function fetchStock(
  endpoint: string,
  params: Record<string, string> = {}
): Promise<void> {
  // 先检查 Key，无 Key 时直接退出，不发任何请求
  const apiKey = loadApiKey();
  if (!apiKey) promptMissingKey();

  const url = new URL(`${BASE_URL}${endpoint}`);
  for (const [k, v] of Object.entries(params)) {
    url.searchParams.set(k, v);
  }

  // 仅发送：API Key Header + 查询参数。不附带任何本地文件内容。
  const resp = await fetch(url.toString(), {
    method: "GET",
    headers: {
      apiKey: apiKey!,   // 仅此一个 Header 携带 Key
      lng: "zh",
    },
  });

  if (!resp.ok) {
    console.error(`❌ HTTP 错误: ${resp.status} ${resp.statusText}`);
    process.exit(1);
  }

  const json = (await resp.json()) as {
    code: number;
    message: string;
    data: unknown;
  };

  if (json.code !== 200 && json.code !== 0) {
    console.error(`❌ 接口错误 [${json.code}]: ${json.message}`);
    process.exit(1);
  }

  // 仅输出 data 字段，不输出包含 Key 的任何内容
  console.log(JSON.stringify(json.data, null, 2));
}

// ─── CLI 入口 ─────────────────────────────────────────────────────
const [, , endpoint, paramsArg] = process.argv;

if (!endpoint) {
  console.error("用法: npx tsx api-client.ts <endpoint> [params_json]");
  process.exit(1);
}

const params: Record<string, string> = paramsArg ? JSON.parse(paramsArg) : {};

fetchStock(endpoint, params).catch((err) => {
  console.error("❌ 请求失败:", err.message);
  process.exit(1);
});
