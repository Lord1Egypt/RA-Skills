'use strict';

const crypto = require('crypto');
const { McpServer } = require('@modelcontextprotocol/sdk/server/mcp.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { z } = require('zod');

// ─── 环境变量校验（启动时快速失败）───────────────────────────────────────────

const GROUP_KEY = process.env.TRUTU_GROUP_KEY;
const GROUP_SECRET = process.env.TRUTU_GROUP_SECRET;

if (!GROUP_KEY || !GROUP_SECRET) {
  console.error(
    '[trutu-photo-verify] 启动失败：缺少必要的环境变量。\n' +
    '  请设置以下环境变量后重新启动：\n' +
    '    TRUTU_GROUP_KEY     — 您的 GroupKey 标识符\n' +
    '    TRUTU_GROUP_SECRET  — 您的 HMAC 签名密钥\n' +
    '  可参考项目根目录的 .env.example 文件。'
  );
  process.exit(1);
}

// ─── API 端点 ────────────────────────────────────────────────────────────────

const API_BASE = 'https://openapi.xhey.top';
const ENDPOINT_CREATE = `${API_BASE}/v2/truth_build/create`;
const ENDPOINT_QUERY  = `${API_BASE}/v2/truth_build/query`;

// ─── HMAC-SHA256 两阶段签名 ──────────────────────────────────────────────────

/**
 * 计算 HMAC-SHA256 签名，返回 Base64 字符串
 */
function sign(secret, data) {
  return crypto.createHmac('sha256', secret).update(data, 'utf8').digest('base64');
}

/**
 * 构建请求 Headers（包含两阶段签名）
 * Stage 1: dataSign = Base64(HMAC-SHA256(groupSecret, bodyStr))
 * Stage 2: Signature = Base64(HMAC-SHA256(groupSecret, `groupKey=...&sign=...&timestamp=...`))
 */
function buildHeaders(bodyStr) {
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const dataSign = sign(GROUP_SECRET, bodyStr);
  const signPayload = `groupKey=${GROUP_KEY}&sign=${dataSign}&timestamp=${timestamp}`;
  const signature = sign(GROUP_SECRET, signPayload);

  return {
    'Content-Type': 'application/json',
    'GroupKey': GROUP_KEY,
    'Timestamp': timestamp,
    'Signature': signature,
  };
}

// ─── HTTP 工具函数 ───────────────────────────────────────────────────────────

/**
 * 向指定端点发送 POST 请求，返回解析后的 JSON
 * 对 HTTP 4xx/5xx 及 API 错误码抛出结构化错误
 */
async function httpPost(url, body) {
  const bodyStr = JSON.stringify(body);
  const headers = buildHeaders(bodyStr);

  let response;
  try {
    response = await fetch(url, {
      method: 'POST',
      headers,
      body: bodyStr,
    });
  } catch (err) {
    throw new Error(`网络请求失败：${err.message}`);
  }

  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error(`API 返回了非 JSON 响应（HTTP ${response.status}）`);
  }

  // HTTP 层错误处理
  if (response.status === 401) {
    throw new Error('鉴权失败（HTTP 401）：GroupKey 或 Signature 无效，请检查您的 TRUTU_GROUP_KEY 和 TRUTU_GROUP_SECRET。');
  }
  if (!response.ok) {
    throw new Error(`API 请求失败（HTTP ${response.status}）：${JSON.stringify(data)}`);
  }

  // 业务层错误处理
  const code = data.code ?? data.errorCode;
  if (code === 4007) {
    throw new Error('凭证无效（错误码 4007）：GroupKey 不存在或已过期，请联系 xhey.top 获取有效凭证。');
  }
  if (code !== undefined && code !== 200 && code !== 0) {
    throw new Error(`API 业务错误（code=${code}）：${data.message ?? data.msg ?? JSON.stringify(data)}`);
  }

  return data;
}

// ─── API 封装 ────────────────────────────────────────────────────────────────

/**
 * 创建验真任务，返回 { taskID }
 */
async function createTask(photoUrlList) {
  const result = await httpPost(ENDPOINT_CREATE, { photoUrlList });
  // 实际响应结构: { data: { data: [{ taskID }] } }
  const taskID = result.data?.data?.[0]?.taskID ?? result.data?.taskID ?? result.taskID;
  if (!taskID) {
    throw new Error(`创建任务成功但未返回 taskID，原始响应：${JSON.stringify(result)}`);
  }
  return taskID;
}

/**
 * 查询任务结果
 */
async function queryTask(taskID) {
  const result = await httpPost(ENDPOINT_QUERY, { taskID });
  // 实际响应结构: { data: { taskStatus, list: [...] } }
  return result.data ?? result;
}

// ─── 轮询逻辑 ────────────────────────────────────────────────────────────────

const TASK_STATUS = {
  PENDING:    1,
  PROCESSING: 2,
  COMPLETE:   5,
  CANCELLED:  6,
};

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 轮询直到任务完成（taskStatus=5），最多重试 maxRetries 次
 */
async function pollUntilComplete(taskID, maxRetries = 10, delayMs = 2000) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    const result = await queryTask(taskID);
    const status = result.taskStatus;

    if (status === TASK_STATUS.COMPLETE) {
      return result;
    }
    if (status === TASK_STATUS.CANCELLED) {
      throw new Error(`任务 ${taskID} 已被服务器取消。`);
    }
    if (status === TASK_STATUS.PENDING || status === TASK_STATUS.PROCESSING) {
      if (attempt < maxRetries) {
        await sleep(delayMs);
        continue;
      }
    }

    if (attempt === maxRetries) {
      throw new Error(`等待验真结果超时（已轮询 ${maxRetries} 次，间隔 ${delayMs}ms），taskID=${taskID}。`);
    }

    throw new Error(`未知的 taskStatus=${status}，taskID=${taskID}。`);
  }
}

// ─── 照片状态解析 ────────────────────────────────────────────────────────────

const PHOTO_STATUS_MAP = {
  0:      { verdict: '通过',  message: '照片验证通过，水印有效，未检测到篡改。' },
  '-1':   { verdict: '错误',  message: '分辨率过低，无法进行有效验真分析。' },
  '-1001':{ verdict: '错误',  message: '网络连接出错或照片损坏，请检查照片文件后重试。' },
  '-1002':{ verdict: '错误',  message: '程序内部出错，请稍后重试或联系技术支持。' },
  '-1003':{ verdict: '错误',  message: '未知错误，请联系技术支持。' },
  '-2300':{ verdict: '未通过', message: 'OCR 启动错误，无法识别照片水印信息。' },
  '-2301':{ verdict: '未通过', message: '照片无防伪码，不支持验真。仅支持带水印和防伪码的今日水印照片。' },
  '-2302':{ verdict: '未通过', message: 'OCR 识别错误，无法解析照片中的水印内容。' },
  '-2303':{ verdict: '未通过', message: '防伪码长度错误，水印信息可能已损坏或被篡改。' },
  '-2305':{ verdict: '未通过', message: '非今日水印相机拍摄，或照片无水印。' },
  '-2306':{ verdict: '错误',   message: '照片 URL 无法访问，请确认链接有效且可公开访问。' },
  '-2307':{ verdict: '错误',   message: '照片格式不支持，请使用 JPG/PNG 格式。' },
  '-2308':{ verdict: '错误',   message: '照片分辨率过低，无法进行有效验真分析。' },
};

function buildPhotoResult(photo) {
  const statusKey = String(photo.status);
  const known = PHOTO_STATUS_MAP[statusKey];

  let verdict, message;
  if (known) {
    verdict = known.verdict;
    message = known.message;
  } else if (photo.status < 0) {
    verdict = '未通过';
    message = `验真未通过（错误码 ${photo.status}）。`;
  } else {
    verdict = '未知';
    message = `未知状态码 ${photo.status}，请联系技术支持。`;
  }

  const result = {
    photoUrl: photo.photoUrl,
    status: photo.status,
    verdict,
    message,
  };

  // 仅在真实照片有元数据时附加
  if (photo.status === 0 && (photo.lat || photo.photoTime || photo.photoAddress)) {
    result.metadata = {
      lat: photo.lat ?? null,
      lng: photo.lng ?? null,
      photoTime: photo.photoTime ?? null,
      photoAddress: photo.photoAddress ?? null,
    };
  } else {
    result.metadata = null;
  }

  return result;
}

// ─── MCP Server ──────────────────────────────────────────────────────────────

const server = new McpServer(
  { name: 'trutu-photo-verify', version: '1.0.0' },
  {
    instructions:
      '当用户提供照片 URL、询问照片真假、怀疑现场造假、' +
      '或要求核验地理位置/时间戳真实性时，必须调用 verify_photo_authenticity 工具。' +
      '对于验真失败的照片，必须以严厉且专业的语气向用户明确警示风险。',
  }
);

server.registerTool(
  'verify_photo_authenticity',
  {
    description:
      '对今日水印相机拍摄的照片进行真实性核验。' +
      '检测 GPS 位置伪造、时间戳篡改和水印造假。' +
      '返回每张照片的验真判定（真实/非真实/错误）及拍摄地点、时间等元数据。' +
      '当用户上传水印照片 URL、询问照片是否真实、询问拍摄地点或时间是否被篡改、' +
      '或明确要求验真时，必须调用此工具。',
    inputSchema: {
      photo_urls: z
        .array(z.string().url({ message: '每个元素必须是合法的 URL' }))
        .min(1, { message: '至少提供 1 张照片 URL' })
        .max(10, { message: '每次最多提交 10 张照片' })
        .describe('待验真的照片 URL 数组（1–10 条）。URL 必须可公开访问。'),
      wait_for_result: z
        .boolean()
        .default(true)
        .describe(
          '是否等待验真结果（默认 true）。' +
          'true：轮询直到完成，返回完整结果；' +
          'false：提交后立即返回 taskID，可稍后手动查询。'
        ),
    },
    annotations: {
      readOnlyHint: true,
      openWorldHint: true,
    },
  },
  async ({ photo_urls, wait_for_result }) => {
    let taskID;

    // Step 1: 创建任务
    try {
      taskID = await createTask(photo_urls);
    } catch (err) {
      return {
        isError: true,
        content: [{ type: 'text', text: `[验真] 创建任务失败：${err.message}` }],
      };
    }

    // Step 2: 如果不等待，直接返回 taskID
    if (!wait_for_result) {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({ taskID, status: 'submitted', message: '任务已提交，请稍后查询结果。' }, null, 2),
        }],
      };
    }

    // Step 3: 轮询直到完成
    let taskResult;
    try {
      taskResult = await pollUntilComplete(taskID);
    } catch (err) {
      return {
        isError: true,
        content: [{ type: 'text', text: `[验真] 查询任务失败：${err.message}` }],
      };
    }

    // Step 4: 构建结构化输出
    // 实际响应结构: { taskStatus, list: [...] }
    const photos = Array.isArray(taskResult.list) ? taskResult.list : [];
    const photoResults = photos.map(buildPhotoResult);

    const authentic = photoResults.filter(p => p.verdict === '通过').length;
    const failed    = photoResults.filter(p => p.verdict === '未通过').length;
    const error     = photoResults.filter(p => p.verdict === '错误').length;

    const output = {
      taskID,
      taskStatus: taskResult.taskStatus,
      summary: {
        total: photoResults.length,
        通过: authentic,
        未通过: failed,
        错误: error,
      },
      photos: photoResults,
    };

    return {
      content: [{ type: 'text', text: JSON.stringify(output, null, 2) }],
    };
  }
);

// ─── 启动 ────────────────────────────────────────────────────────────────────

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(err => {
  console.error('[trutu-photo-verify] 服务器异常退出：', err);
  process.exit(1);
});
