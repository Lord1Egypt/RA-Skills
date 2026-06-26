import express from 'express';
import axios from 'axios';
import { parseString } from 'xml2js';
import crypto from 'crypto';
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

const {
  CORP_ID,
  AGENT_ID,
  AGENT_SECRET,
  WEBHOOK_TOKEN,
  OPENCLAW_TOKEN,
  OPENCLAW_BASE_URL = 'http://localhost:18789',
  CLAUDE_MODEL = 'claude-haiku-4-5',
  LOG_LEVEL = 'INFO',
} = process.env;

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const port = 8090;
const logsDir = path.join(__dirname, 'logs');

// 验证必需的环境变量
const required = ['CORP_ID', 'AGENT_ID', 'AGENT_SECRET', 'WEBHOOK_TOKEN', 'OPENCLAW_TOKEN'];
for (const v of required) {
  if (!process.env[v]) {
    console.error(`❌ 缺少必需的环境变量: ${v}`);
    process.exit(1);
  }
}

// 创建日志目录
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
}

// 日志函数
function log(level, msg) {
  const timestamp = new Date().toISOString();
  const logEntry = `[${timestamp}] [${level}] ${msg}`;
  
  if (['INFO', 'WARN', 'ERROR'].includes(level)) {
    console.log(logEntry);
    fs.appendFileSync(path.join(logsDir, 'wecom-adapter.log'), logEntry + '\n');
  }
}

// CORS + 解析
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'HEAD,GET,POST,DELETE,PATCH,OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') return res.sendStatus(204);
  next();
});

app.use(express.text({ type: ['application/xml', 'text/xml', 'text/plain', '*/*'] }));
app.use(express.json());

// ========== 健康检查 ==========
app.get('/health', (req, res) => {
  res.json({ ok: true, timestamp: new Date().toISOString() });
});

// ========== 企业微信 GET 验证 ==========
app.get('/webhook', (req, res) => {
  // ⚠️ 企业微信使用 msg_signature，不是 signature！
  const { msg_signature, timestamp, nonce, echostr } = req.query;
  
  log('INFO', `📩 GET /webhook 请求 - msg_signature=${msg_signature}, timestamp=${timestamp}, nonce=${nonce}, echostr=${echostr}`);
  
  if (!msg_signature || !timestamp || !nonce) {
    log('WARN', '❌ 缺少必需的查询参数');
    return res.status(400).send('Missing parameters');
  }
  
  // 企业微信加密模式：sort([token, timestamp, nonce, echostr])，然后 SHA1
  const arr = [WEBHOOK_TOKEN, timestamp, nonce, echostr].sort();
  const tmpStr = arr.join('');
  const sha1 = crypto.createHash('sha1').update(tmpStr).digest('hex');
  
  log('INFO', `签名验证：计算=${sha1}，收到=${msg_signature}`);
  
  if (sha1 === msg_signature) {
    log('INFO', '✅ 企业微信签名验证通过，开始解密 echostr...');
    
    try {
      // 解密 echostr（企业微信加密模式）
      const aesKey = Buffer.from(AGENT_SECRET + '=', 'base64');
      const iv = aesKey.slice(0, 16);
      
      const encryptedBuffer = Buffer.from(echostr, 'base64');
      const decipher = crypto.createDecipheriv('aes-256-cbc', aesKey, iv);
      decipher.setAutoPadding(false);
      
      let decrypted = Buffer.concat([decipher.update(encryptedBuffer), decipher.final()]);
      
      // 去除 PKCS#7 填充
      const pad = decrypted[decrypted.length - 1];
      if (pad > 0 && pad <= 32) {
        decrypted = decrypted.slice(0, decrypted.length - pad);
      }
      
      // 企业微信格式：16字节随机串 + 4字节消息长度(网络字节序) + 消息内容 + CorpID
      const msgLen = decrypted.readUInt32BE(16);
      const msg = decrypted.slice(20, 20 + msgLen).toString('utf8');
      const corpId = decrypted.slice(20 + msgLen).toString('utf8');
      
      log('INFO', `✅ 解密成功：msg=${msg}, corpId=${corpId}`);
      
      return res.status(200).send(msg);
    } catch (err) {
      log('ERROR', `❌ 解密 echostr 失败: ${err.message}`);
      return res.status(500).send('Decrypt error');
    }
  }
  
  log('WARN', `❌ 签名验证失败：计算=${sha1}, 收到=${msg_signature}`);
  return res.status(403).send('Forbidden');
});

// ========== 企业微信 POST 消息 ==========
app.post('/webhook', async (req, res) => {
  try {
    // 1️⃣ 解析 XML 获取 Encrypt 字段
    const { msg_signature, timestamp, nonce } = req.query;
    const rawXml = req.body;
    
    if (!rawXml) {
      log('WARN', '❌ 消息体为空');
      return res.status(200).send('success');
    }
    
    log('INFO', `📩 POST /webhook - msg_signature=${msg_signature}, body长度=${rawXml.length}`);
    
    // 从 XML 中提取 Encrypt 字段
    const encryptMatch = rawXml.match(/<Encrypt><!\[CDATA\[(.*?)\]\]><\/Encrypt>/);
    if (!encryptMatch) {
      log('WARN', '❌ 无法提取 Encrypt 字段');
      return res.status(200).send('success');
    }
    const encrypt = encryptMatch[1];
    
    // 2️⃣ 验证签名：sort([token, timestamp, nonce, encrypt]) → SHA1
    if (msg_signature && timestamp && nonce) {
      const arr = [WEBHOOK_TOKEN, timestamp, nonce, encrypt].sort();
      const tmpStr = arr.join('');
      const sha1 = crypto.createHash('sha1').update(tmpStr).digest('hex');
      
      if (sha1 !== msg_signature) {
        log('WARN', `❌ POST 签名验证失败：计算=${sha1}, 收到=${msg_signature}`);
        return res.status(200).send('success');
      }
      log('INFO', '✅ POST 签名验证成功');
    }

    // 3️⃣ 解密消息
    const decryptedXml = decryptWeComMessage(encrypt, AGENT_SECRET);
    
    // 3️⃣ 解析 XML
    const result = await parseXMLPromise(decryptedXml);
    const msg = result.xml || {};
    const fromUser = msg.FromUserName?.[0] || 'unknown';
    const content = msg.Content?.[0] || msg.Text?.[0] || '';
    const msgType = msg.MsgType?.[0] || 'unknown';

    log('INFO', `📨 收到消息 from=${fromUser} type=${msgType} content=${content.substring(0, 50)}`);

    // 4️⃣ 仅处理文本消息
    if (msgType !== 'text' || !content.trim()) {
      log('INFO', `⏭️ 跳过非文本消息`);
      return res.status(200).send('success');
    }

    // 5️⃣ 立即回复 success（企业微信要求 5 秒内响应）
    res.status(200).send('success');

    // 6️⃣ 异步调用 OpenClaw 并通过企业微信 API 发送回复
    (async () => {
      try {
        log('INFO', `🤖 调用 OpenClaw...`);
        const claudeReply = await callOpenClaw(content);
        
        // 通过企业微信 API 主动发送消息
        const accessToken = await getAccessToken();
        await axios.post(
          `https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=${accessToken}`,
          {
            touser: fromUser,
            msgtype: 'text',
            agentid: parseInt(AGENT_ID),
            text: { content: claudeReply },
          }
        );
        log('INFO', `✅ 回复已发送 to=${fromUser}`);
      } catch (err) {
        log('ERROR', `❌ 异步回复失败: ${err.message}`);
      }
    })();
  } catch (err) {
    log('ERROR', `❌ Webhook 处理失败: ${err.message}`);
    res.status(200).json({ errcode: 0 }); // 返回 200 防止企业微信重试
  }
});

// ========== 辅助函数 ==========

// 解密企业微信消息（标准企业微信加密格式）
function decryptWeComMessage(encryptedMsg, encodingAESKey) {
  try {
    const aesKey = Buffer.from(encodingAESKey + '=', 'base64');
    const iv = aesKey.slice(0, 16);
    
    const encryptedBuffer = Buffer.from(encryptedMsg, 'base64');
    const decipher = crypto.createDecipheriv('aes-256-cbc', aesKey, iv);
    decipher.setAutoPadding(false);
    
    let decrypted = Buffer.concat([decipher.update(encryptedBuffer), decipher.final()]);
    
    // 去除 PKCS#7 填充
    const pad = decrypted[decrypted.length - 1];
    if (pad > 0 && pad <= 32) {
      decrypted = decrypted.slice(0, decrypted.length - pad);
    }
    
    // 企业微信格式：16字节随机串 + 4字节消息长度(网络字节序) + 消息内容 + CorpID
    const msgLen = decrypted.readUInt32BE(16);
    const xmlContent = decrypted.slice(20, 20 + msgLen).toString('utf8');
    
    log('INFO', `✅ 消息解密成功，长度=${msgLen}`);
    return xmlContent;
  } catch (err) {
    log('ERROR', `❌ 消息解密失败: ${err.message}`);
    throw err;
  }
}

// 解析 XML
function parseXMLPromise(xml) {
  return new Promise((resolve, reject) => {
    parseString(xml, (err, result) => {
      if (err) reject(err);
      else resolve(result);
    });
  });
}

// 获取企业微信 access_token（带缓存）
let cachedToken = { token: '', expiresAt: 0 };
async function getAccessToken() {
  if (cachedToken.token && Date.now() < cachedToken.expiresAt) {
    return cachedToken.token;
  }
  const res = await axios.get(
    `https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=${CORP_ID}&corpsecret=${process.env.APP_SECRET || AGENT_SECRET}`
  );
  if (res.data.errcode !== 0) {
    throw new Error(`获取 access_token 失败: ${res.data.errmsg}`);
  }
  cachedToken = {
    token: res.data.access_token,
    expiresAt: Date.now() + (res.data.expires_in - 300) * 1000,
  };
  log('INFO', `✅ 获取 access_token 成功`);
  return cachedToken.token;
}

// 调用 OpenClaw API
async function callOpenClaw(userMessage) {
  try {
    const response = await axios.post(
      `${OPENCLAW_BASE_URL}/v1/chat/completions`,
      {
        model: CLAUDE_MODEL,
        messages: [{ role: 'user', content: userMessage }],
        max_tokens: 500,
      },
      {
        headers: {
          'Authorization': `Bearer ${OPENCLAW_TOKEN}`,
          'Content-Type': 'application/json',
        },
        timeout: 30000, // 30 秒超时（企业微信会异步等待）
      }
    );

    const reply = response.data.choices?.[0]?.message?.content || '抱歉，我还没学会回答这个。';
    log('INFO', `✅ OpenClaw 回复: ${reply.substring(0, 50)}`);
    return reply;
  } catch (err) {
    log('ERROR', `❌ OpenClaw 调用失败: ${err.message}`);
    return '服务暂时不可用，请稍后重试。';
  }
}

// 启动服务
app.listen(port, () => {
  log('INFO', `🚀 WeCom 适配器启动成功，监听 :${port}`);
  log('INFO', `📝 日志位置: ${logsDir}/wecom-adapter.log`);
  log('INFO', `🤖 使用模型: ${CLAUDE_MODEL}`);
});

process.on('unhandledRejection', (err) => {
  log('ERROR', `未捕获的错误: ${err.message}`);
});
