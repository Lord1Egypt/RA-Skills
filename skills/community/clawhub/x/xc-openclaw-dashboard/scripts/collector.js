/**
 * OpenClaw Dashboard - 数据采集器 v2
 * 从 openclaw status 命令获取真实数据
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 默认配置
const DEFAULT_CONFIG = {
  maxSessions: 50,
  sessionTimeoutHours: 24,
  tokenLimit: 200000  // Context 上限
};

/**
 * 通过 openclaw status 命令获取数据
 */
function getOpenClawStatus() {
  try {
    const output = execSync('openclaw status', {
      encoding: 'utf-8',
      timeout: 10000,
      windowsHide: true
    });
    return output;
  } catch (err) {
    return err.stdout || '';
  }
}

/**
 * 解析 openclaw status 输出
 */
function parseStatusOutput(output) {
  const lines = output.split('\n');
  
  const sessions = [];
  
  for (const line of lines) {
    // 直接匹配包含 agent: 的行
    if (line.includes('| agent:')) {
      // 提取 key
      const keyMatch = line.match(/\| ([^|]+)\|/);
      const key = keyMatch ? keyMatch[1].trim() : '';
      
      // 提取 kind
      const kindMatch = line.match(/\| (direct|group|cron) \|/);
      const kind = kindMatch ? kindMatch[1] : 'unknown';
      
      // 提取 age
      const ageMatch = line.match(/\| (\d+\w+ ago|just now)  \|/);
      const age = ageMatch ? ageMatch[1] : '';
      
      // 提取 token 信息
      const tokenMatch = line.match(/(\d+)k\/(\d+)k\s*\((\d+)%\)/);
      let tokens = 0;
      let percentage = 0;
      if (tokenMatch) {
        tokens = parseInt(tokenMatch[1]) * 1000;
        percentage = parseInt(tokenMatch[3]);
      }
      
      // 检测是否是 unknown
      if (line.includes('unknown/')) {
        tokens = 0;
        percentage = 0;
      }
      
      if (key) {
        sessions.push({
          key,
          kind,
          age,
          model: 'MiniMax-M2.5-highspeed',
          tokens,
          percentage
        });
      }
    }
  }
  
  return sessions;
}

/**
 * 获取完整仪表盘数据
 */
async function collectDashboardData(config = {}) {
  const tokenLimit = config.tokenLimit || DEFAULT_CONFIG.tokenLimit;
  
  // 获取 openclaw status
  const statusOutput = getOpenClawStatus();
  const sessions = parseStatusOutput(statusOutput);
  
  // 计算总 token（所有 session 的总和）
  const totalTokens = sessions.reduce((sum, s) => sum + s.tokens, 0);
  
  // 获取系统信息
  const nodeName = process.env.COMPUTERNAME || 'Unknown';
  
  return {
    timestamp: new Date().toISOString(),
    model: 'MiniMax-M2.5-highspeed',
    node: nodeName,
    channel: 'feishu',
    os: `${process.platform} ${process.arch}`,
    runtime: 'OpenClaw v3.13',
    tokenLimit: tokenLimit,
    tokens: {
      total: totalTokens,
      formatted: {
        total: formatNumber(totalTokens),
        limit: formatNumber(tokenLimit)
      }
    },
    sessions: sessions.slice(0, config.maxSessions || 20),
    sessionCount: sessions.length,
    uptime: formatUptime(process.uptime())
  };
}

/**
 * 格式化数字
 */
function formatNumber(num) {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
  if (num >= 1000) return Math.round(num / 1000) + 'K';
  return num.toString();
}

/**
 * 格式化运行时长
 */
function formatUptime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  if (hours > 0) return `${hours}h ${minutes}m`;
  return `${minutes}m`;
}

/**
 * 构建飞书卡片消息体
 */
function buildFeishuCard(data) {
  // 按 token 使用量排序显示
  const topSessions = data.sessions
    .sort((a, b) => b.tokens - a.tokens)
    .slice(0, 8);

  let sessionList = topSessions.map(s => {
    const tokensStr = s.tokens >= 1000 
      ? Math.round(s.tokens / 1000) + 'K' 
      : s.tokens.toString();
    const key = s.key.includes(':') 
      ? s.key.split(':').slice(1, 3).join('/') 
      : s.key;
    return `• \`${key}\` (${s.kind}): ${tokensStr} tokens`;
  }).join('\n');

  if (data.sessionCount > 8) {
    sessionList += `\n• ... 还有 ${data.sessionCount - 8} 个 session`;
  }

  const elements = [
    {
      tag: 'div',
      text: { 
        tag: 'lark_md', 
        content: `**📊 Token 使用情况**\n\n总消耗: **${data.tokens.formatted.total}** tokens\n会话数: ${data.sessionCount} 个活跃\nContext 上限: ${data.tokens.formatted.limit}/session` 
      }
    },
    { tag: 'hr' },
    {
      tag: 'div',
      text: { 
        tag: 'lark_md', 
        content: `**📚 活跃 Sessions**\n\n${sessionList}` 
      }
    },
    { tag: 'hr' },
    {
      tag: 'div',
      text: { 
        tag: 'lark_md', 
        content: `**🖥️ 系统信息**\n\n• 节点: \`${data.node}\`\n• Channel: \`${data.channel}\`\n• Agent 数: \`${getAgentCount(data.sessions)}\`\n• 模型: \`${data.model}\`` 
      }
    },
    { tag: 'hr' },
    {
      tag: 'div',
      text: { 
        tag: 'lark_md', 
        content: `⏰ ${new Date().toLocaleString('zh-CN')}` 
      }
    }
  ];

  return {
    msg_type: 'interactive',
    card: {
      config: { wide_screen_mode: true },
      header: {
        title: { tag: 'plain_text', content: '🤖 OpenClaw 多 Agent 状态' },
        template: 'blue'
      },
      elements
    }
  };
}

/**
 * 获取 Agent 数量
 */
function getAgentCount(sessions) {
  const agents = new Set();
  sessions.forEach(s => {
    const parts = s.key.split(':');
    if (parts[1]) agents.add(parts[1]);
  });
  return agents.size;
}

/**
 * 获取简要状态文本
 */
function getStatusText(data) {
  return `🤖 **OpenClaw 状态**

📊 Token 总消耗: ${data.tokens.formatted.total} tokens
📚 活跃 Sessions: ${data.sessionCount} 个
🖥️ 模型: ${data.model}
⏱️ 更新于 ${new Date().toLocaleTimeString('zh-CN')}`;
}

/**
 * 获取 Session 列表文本
 */
function getSessionsText(data) {
  let text = `📚 **活跃 Sessions (${data.sessionCount})**\n\n`;
  
  data.sessions
    .sort((a, b) => b.tokens - a.tokens)
    .forEach((s, i) => {
      const key = s.key.includes(':') 
        ? s.key.split(':').slice(1, 3).join('/') 
        : s.key;
      const tokensStr = s.tokens >= 1000 
        ? Math.round(s.tokens / 1000) + 'K' 
        : s.tokens.toString();
      
      text += `${i + 1}. **${key}**\n`;
      text += `   ├ 类型: ${s.kind}\n`;
      text += `   ├ Age: ${s.age}\n`;
      text += `   └ Tokens: ${tokensStr}\n\n`;
    });
  
  return text;
}

// 导出模块
module.exports = {
  collectDashboardData,
  buildFeishuCard,
  getStatusText,
  getSessionsText,
  getOpenClawStatus,
  parseStatusOutput
};

// 命令行测试
if (require.main === module) {
  (async () => {
    try {
      const data = await collectDashboardData();
      console.log(JSON.stringify(data, null, 2));
    } catch (err) {
      console.error('采集失败:', err.message);
      process.exit(1);
    }
  })();
}
