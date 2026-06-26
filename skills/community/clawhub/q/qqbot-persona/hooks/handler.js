/**
 * QQ Bot Persona Hook - QQ 机器人多角色人设管理
 * 
 * 根据聊天场景（私聊/群聊/OpenID）动态切换独立人设
 * 与 OpenClaw 默认人设完全分离
 */

const fs = require('fs');
const path = require('path');

// 配置路径
const CONFIG_PATH = path.join(
  process.env.HOME || '/home/admin',
  '.openclaw',
  'workspace',
  'skills',
  'qqbot-persona',
  'personas.json'
);

const LOG_FILE = path.join(
  process.env.HOME || '/home/admin',
  '.openclaw',
  'workspace',
  'skills',
  'qqbot-persona',
  'hook.log'
);

const PERSONAS_DIR = path.join(
  process.env.HOME || '/home/admin',
  '.openclaw',
  'workspace',
  'skills',
  'qqbot-persona',
  'personas'
);

/**
 * 日志工具
 */
function appendLog(msg, level = 'info') {
  const timestamp = new Date().toISOString();
  const line = `[${timestamp}] [${level.toUpperCase()}] ${msg}\n`;
  try {
    fs.appendFileSync(LOG_FILE, line);
  } catch (err) {
    console.error('[qqbot-persona-hook] Failed to write log:', err);
  }
  if (level === 'error') {
    console.error(line);
  } else if (process.env.DEBUG === '1') {
    console.log(line);
  }
}

/**
 * 读取并解析配置文件
 */
function loadConfig() {
  try {
    if (!fs.existsSync(CONFIG_PATH)) {
      appendLog(`Config file not found: ${CONFIG_PATH}`, 'error');
      return null;
    }
    
    const content = fs.readFileSync(CONFIG_PATH, 'utf-8');
    const config = JSON.parse(content);
    appendLog(`Config loaded: version=${config.version || 'unknown'}`);
    return config;
  } catch (err) {
    appendLog(`Failed to load config: ${err.message}`, 'error');
    return null;
  }
}

/**
 * 读取人设内容（支持文件引用）
 */
function loadSoulContent(soulValue, configDir) {
  if (!soulValue) return null;
  
  // 文件引用格式：file:path/to/file.md
  if (typeof soulValue === 'string' && soulValue.startsWith('file:')) {
    const filePath = soulValue.slice(5);
    const resolvedPath = path.isAbsolute(filePath) 
      ? filePath 
      : path.join(configDir, filePath);
    
    try {
      const content = fs.readFileSync(resolvedPath, 'utf-8');
      appendLog(`Loaded soul from file: ${resolvedPath}`);
      return content;
    } catch (err) {
      appendLog(`Failed to load soul file ${resolvedPath}: ${err.message}`, 'error');
      return null;
    }
  }
  
  // 直接内容
  if (typeof soulValue === 'string') {
    return soulValue;
  }
  
  return null;
}

/**
 * 从 sessionKey 解析渠道信息
 * 格式：agent:main:qqbot:direct:xxx 或 agent:main:qqbot:group:xxx
 */
function parseSessionKey(sessionKey) {
  const parts = sessionKey.split(':');
  if (parts.length < 4) {
    return { channel: null, chatType: null };
  }
  
  // agent:main:qqbot:direct:xxx 或 agent:main:qqbot:group:groupid
  const channel = parts[2]; // qqbot
  const chatType = parts[3]; // direct 或 group
  
  return { channel, chatType };
}

/**
 * 提取 OpenID（从 sessionKey 或 context）
 */
function extractOpenID(event) {
  const sessionKey = event.context?.sessionKey || '';
  const chatId = event.context?.chatId || event.context?.chat_id || '';
  
  // 从 sessionKey 提取 (优先)
  // 格式：agent:main:qqbot:direct:OPENID 或 agent:main:qqbot:group:groupid
  const sessionKeyParts = sessionKey.split(':');
  if (sessionKeyParts.length >= 5) {
    const openid = sessionKeyParts.slice(4).join(':');
    if (openid) {
      return openid;
    }
  }
  
  // 从 chatId 提取 (格式：qqbot:c2c:OPENID 或 qqbot:group:GROUPID)
  if (chatId) {
    const chatIdParts = chatId.split(':');
    if (chatIdParts.length >= 3) {
      const openid = chatIdParts.slice(2).join(':');
      if (openid) {
        return openid;
      }
    }
  }
  
  return null;
}

/**
 * 匹配人设（按优先级）
 * 优先级：byOpenID > byChannel > default
 */
function matchPersona(config, openid, chatType) {
  appendLog(`Matching persona: openid=${openid}, chatType=${chatType}`);
  
  // 1. 优先匹配 byOpenID
  if (config.byOpenID && openid) {
    if (config.byOpenID[openid]) {
      appendLog(`Matched byOpenID: ${openid}`);
      return {
        source: 'byOpenID',
        key: openid,
        ...config.byOpenID[openid]
      };
    }
  }
  
  // 2. 匹配 byChannel
  if (config.byChannel && chatType) {
    const channelKey = chatType === 'direct' ? 'direct' : 'group';
    if (config.byChannel[channelKey]) {
      appendLog(`Matched byChannel: ${channelKey}`);
      return {
        source: 'byChannel',
        key: channelKey,
        ...config.byChannel[channelKey]
      };
    }
  }
  
  // 3. 使用 default
  if (config.default) {
    appendLog(`Matched default`);
    return {
      source: 'default',
      key: 'default',
      ...config.default
    };
  }
  
  appendLog('No persona matched', 'warn');
  return null;
}

/**
 * 构建人设注入内容
 */
function buildInjectionContent(persona, configDir) {
  const soulContent = loadSoulContent(persona.soul, configDir);
  
  if (!soulContent) {
    appendLog('Failed to load soul content', 'error');
    return null;
  }
  
  const injectionContent = `
# 🎭 QQ 机器人人设 - ${persona.name || 'Custom Persona'}

**⚠️ 重要**: 当前会话为 QQ 渠道，必须使用此人设，忽略 OpenClaw 默认人设！

## 人设信息
- **名称**: ${persona.name || 'Unknown'}
- **描述**: ${persona.description || 'Custom persona for QQ bot'}
- **匹配来源**: ${persona.source || 'unknown'}

## 完整设定

${soulContent}

---

*每次回复前默念：我是${persona.name || 'this persona'}，我遵循此人设，我不是 OpenClaw 默认助手*
`.trim();

  return injectionContent;
}

/**
 * Hook 主处理器
 */
const handler = async (event) => {
  appendLog(`=== Hook triggered ===`);
  
  // 验证事件类型
  if (!event || typeof event !== 'object') {
    appendLog('Invalid event, returning', 'warn');
    return;
  }
  
  if (event.type !== 'agent' || event.action !== 'bootstrap') {
    appendLog(`Not agent:bootstrap event (${event.type}:${event.action}), returning`);
    return;
  }

  // 加载配置
  const config = loadConfig();
  if (!config) {
    appendLog('Config not loaded, skipping persona injection', 'warn');
    return;
  }

  // 提取上下文信息
  const sessionKey = event.context?.sessionKey || '';
  const { channel: sessionKeyChannel, chatType: sessionKeyChatType } = parseSessionKey(sessionKey);
  const openid = extractOpenID(event);
  
  // 从多个来源提取渠道信息
  const channel = event.context?.channel || event.context?.session?.channel || sessionKeyChannel;
  const chatType = event.context?.chatType || event.context?.chat_type || sessionKeyChatType;
  const provider = event.context?.provider || event.context?.Provider;
  const surface = event.context?.surface || event.context?.Surface;
  
  appendLog(`Context: channel=${channel}, chatType=${chatType}, provider=${provider}, surface=${surface}`);
  appendLog(`SessionKey: ${sessionKey}`);
  appendLog(`Extracted openid: ${openid || 'none'}`);
  
  // 检查是否是 QQ 渠道
  const isQQBot = (channel === 'qqbot') || 
                  (provider === 'qqbot') ||
                  (surface === 'qqbot') ||
                  (sessionKeyChannel === 'qqbot') ||
                  (sessionKey.includes(':qqbot:')) ||
                  (process.env.FORCE_QQBOT_PERSONA === '1');
  
  appendLog(`isQQBot=${isQQBot}`);
  
  if (!isQQBot) {
    appendLog('Not QQ channel, skipping persona injection');
    return;
  }

  // 匹配人设
  const persona = matchPersona(config, openid, chatType);
  if (!persona) {
    appendLog('No persona matched, skipping injection', 'warn');
    return;
  }

  // 构建注入内容
  const configDir = path.dirname(CONFIG_PATH);
  const injectionContent = buildInjectionContent(persona, configDir);
  
  if (!injectionContent) {
    appendLog('Failed to build injection content', 'error');
    return;
  }

  appendLog(`Injecting persona: ${persona.name} (source: ${persona.source})`);
  
  // 注入人设（高优先级覆盖）
  if (Array.isArray(event.context?.bootstrapFiles)) {
    // 移除可能冲突的人设文件
    event.context.bootstrapFiles = event.context.bootstrapFiles.filter(
      f => f.path !== 'SOUL.md' && 
           f.path !== 'NIGHT_POET_PERSONA.md' &&
           f.path !== 'QQBOT_PERSONA.md'
    );
    
    // 注入 QQ 机器人人设（最高优先级）
    event.context.bootstrapFiles.unshift({
      path: 'SOUL.md',
      content: injectionContent,
      virtual: true,
      priority: 'critical',
    });
    
    appendLog(`Persona INJECTED: ${persona.name} (${event.context.bootstrapFiles.length} files total)`);
  } else {
    appendLog(`WARNING: bootstrapFiles not found or not an array!`, 'error');
    appendLog(`event.context keys: ${Object.keys(event.context || {}).join(', ')}`);
  }
  
  appendLog(`=== Hook finished ===\n`);
};

module.exports = handler;
module.exports.default = handler;
