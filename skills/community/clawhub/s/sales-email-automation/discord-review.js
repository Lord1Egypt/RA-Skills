#!/usr/bin/env node

/**
 * Discord 审阅流程模块
 * 将生成的回复草稿推送到 Discord 频道供审批
 * 支持：✅发送 / ✏️编辑 / ❌丢弃
 * 
 * 使用 Discord Bot API + Embed 格式 + 交互按钮
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');

// 配置
const CONFIG_PATH = path.join(__dirname, 'config', 'discord-config.json');
const DRAFTS_DIR = path.join(__dirname, 'drafts');
const ENV_PATH = path.join(__dirname, '..', '..', '.env');

// 加载 Discord Bot Token
function loadDiscordToken() {
  if (fs.existsSync(ENV_PATH)) {
    const envContent = fs.readFileSync(ENV_PATH, 'utf8');
    const match = envContent.match(/^DISCORD_BOT_TOKEN=(.+)$/m);
    if (match) {
      return match[1].trim();
    }
  }
  return process.env.DISCORD_BOT_TOKEN;
}

// 加载配置
function loadConfig() {
  if (fs.existsSync(CONFIG_PATH)) {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  }
  // 创建默认配置
  const defaultConfig = {
    channel_id: '',
    guild_id: '',
    review_channel: 'email-review',
    timeout_minutes: 30
  };
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(defaultConfig, null, 2), 'utf8');
  console.log('⚠️ 配置文件不存在，已创建默认配置，请编辑:', CONFIG_PATH);
  return defaultConfig;
}

// Discord API 请求
function discordRequest(endpoint, method = 'GET', body = null, token) {
  return new Promise((resolve, reject) => {
    const url = `https://discord.com/api/v10/${endpoint}`;
    const options = {
      method,
      headers: {
        'Authorization': `Bot ${token}`,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(url, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(data ? JSON.parse(data) : {});
        } else {
          reject(new Error(`Discord API ${res.statusCode}: ${data}`));
        }
      });
    });

    req.on('error', reject);
    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}

/**
 * 构建 Discord Embed 消息
 */
function buildEmbed(draft) {
  const isEscalate = draft.escalate || (draft.intent === 'complaint');
  const color = isEscalate ? 0xFF0000 : 0x0099FF;
  const titlePrefix = isEscalate ? '⚠️ ' : '';
  
  const embed = {
    title: `${titlePrefix}📧 [EMAIL REVIEW] ${draft.subject || 'No Subject'}`,
    color,
    fields: [
      {
        name: '📮 From',
        value: draft.from || 'Unknown',
        inline: true
      },
      {
        name: '🎯 Intent',
        value: `${draft.intent || 'unknown'} (${draft.confidence?.toFixed(2) || 'N/A'})`,
        inline: true
      },
      {
        name: '⏰ Generated',
        value: new Date(draft.created_at || Date.now()).toLocaleString('zh-CN'),
        inline: true
      }
    ],
    description: '```' + (draft.reply || draft.content || 'No content') + '```',
    footer: {
      text: `Draft ID: ${draft.draft_id || 'N/A'} | Timeout: 30 min`
    },
    timestamp: new Date().toISOString()
  };

  // 添加 escalation 警告字段
  if (isEscalate) {
    embed.fields.push({
      name: '⚠️ Escalation',
      value: 'This is a complaint/escalation case requiring human approval.',
      inline: false
    });
  }

  return embed;
}

/**
 * 构建交互按钮组件
 */
function buildActionComponents(draftId) {
  return {
    components: [
      {
        type: 1, // Action Row
        components: [
          {
            type: 2, // Button
            style: 3, // Success (green)
            label: '✅ Send',
            custom_id: `send_${draftId}`
          },
          {
            type: 2, // Button
            style: 1, // Primary (blue)
            label: '✏️ Edit',
            custom_id: `edit_${draftId}`,
            disabled: true // 当前版本仅记录意图
          },
          {
            type: 2, // Button
            style: 4, // Danger (red)
            label: '❌ Discard',
            custom_id: `discard_${draftId}`
          }
        ]
      }
    ]
  };
}

/**
 * 更新草稿状态
 */
function updateDraftStatus(draftId, status, additionalData = {}) {
  const draftPath = path.join(DRAFTS_DIR, `${draftId}.json`);
  if (!fs.existsSync(draftPath)) {
    console.log(`⚠️ 草稿文件不存在：${draftPath}`);
    return false;
  }

  const draft = JSON.parse(fs.readFileSync(draftPath, 'utf8'));
  draft.status = status;
  draft.updated_at = new Date().toISOString();
  Object.assign(draft, additionalData);

  fs.writeFileSync(draftPath, JSON.stringify(draft, null, 2), 'utf8');
  console.log(`✅ 草稿状态已更新：${draftId} → ${status}`);
  return true;
}

/**
 * 发送邮件（调用 SMTP）
 */
async function sendEmail(draft) {
  const smtpPath = path.join(__dirname, 'scripts', 'smtp.js');
  
  return new Promise((resolve, reject) => {
    const args = [
      'send',
      '--to', draft.to || draft.original_from,
      '--subject', draft.subject || 'Re: ' + (draft.original_subject || 'Your Inquiry'),
      '--html',
      '--body', draft.reply || draft.content
    ];

    // 添加附件（如果有）
    if (draft.attachments && draft.attachments.length > 0) {
      args.push('--attach', draft.attachments.join(','));
    }

    console.log(`📤 发送邮件：${args.join(' ')}`);
    
    execFile('node', [smtpPath, ...args], { 
      env: process.env,
      cwd: __dirname
    }, (error, stdout, stderr) => {
      if (error) {
        reject(new Error(`SMTP 发送失败：${stderr || error.message}`));
      } else {
        resolve({ stdout, stderr });
      }
    });
  });
}

/**
 * 发送草稿到 Discord 审阅
 * @param {Object} draft - generateReply() 的返回值
 */
async function sendForReview(draft) {
  console.log(`\n📤 发送草稿到 Discord 审阅...`);
  
  const token = loadDiscordToken();
  if (!token) {
    throw new Error('DISCORD_BOT_TOKEN 未配置');
  }

  const config = loadConfig();
  const channelId = config.channel_id;
  
  if (!channelId) {
    throw new Error('Discord channel_id 未配置，请编辑 config/discord-config.json');
  }

  // 构建 Embed 和按钮
  const embed = buildEmbed(draft);
  const components = buildActionComponents(draft.draft_id);

  const messagePayload = {
    embeds: [embed],
    components: [components]
  };

  try {
    // 发送消息到 Discord
    const result = await discordRequest(
      `channels/${channelId}/messages`,
      'POST',
      messagePayload,
      token
    );

    console.log(`✅ 审阅消息已发送到 Discord: ${result.id}`);

    // 记录审阅请求
    const reviewRecord = {
      review_id: `review-${Date.now()}`,
      draft_id: draft.draft_id,
      discord_message_id: result.id,
      channel_id: channelId,
      sent_at: new Date().toISOString(),
      status: 'pending',
      timeout_at: new Date(Date.now() + config.timeout_minutes * 60 * 1000).toISOString()
    };

    // 保存审阅记录
    const reviewsDir = path.join(__dirname, 'reviews-pending');
    if (!fs.existsSync(reviewsDir)) {
      fs.mkdirSync(reviewsDir, { recursive: true });
    }
    const reviewPath = path.join(reviewsDir, `${reviewRecord.review_id}.json`);
    fs.writeFileSync(reviewPath, JSON.stringify(reviewRecord, null, 2), 'utf8');

    // 启动超时定时器
    setupTimeout(reviewRecord, token, channelId);

    return {
      success: true,
      review_id: reviewRecord.review_id,
      discord_message_id: result.id,
      channel: channelId,
      status: 'pending_approval'
    };
  } catch (err) {
    console.error(`❌ Discord 发送失败：${err.message}`);
    
    // 降级：保存到本地
    return saveReviewRequestLocally(draft);
  }
}

/**
 * 设置超时处理
 */
async function setupTimeout(reviewRecord, token, channelId) {
  const timeoutMs = 30 * 60 * 1000; // 30 分钟
  
  setTimeout(async () => {
    const reviewPath = path.join(__dirname, 'reviews-pending', `${reviewRecord.review_id}.json`);
    if (!fs.existsSync(reviewPath)) {
      return; // 已处理
    }

    const review = JSON.parse(fs.readFileSync(reviewPath, 'utf8'));
    if (review.status !== 'pending') {
      return; // 已处理
    }

    // 更新状态为 timeout
    review.status = 'timeout';
    review.completed_at = new Date().toISOString();
    fs.writeFileSync(reviewPath, JSON.stringify(review, null, 2), 'utf8');

    // 更新草稿状态
    updateDraftStatus(review.draft_id, 'timeout');

    // 更新 Discord 消息
    try {
      await discordRequest(
        `channels/${channelId}/messages/${review.discord_message_id}`,
        'PATCH',
        {
          embeds: [{
            title: '⏰ Timed Out',
            description: 'No action taken within 30 minutes.',
            color: 0xFFA500
          }],
          components: [] // 移除按钮
        },
        token
      );
      console.log(`⏰ 审阅超时：${review.review_id}`);
    } catch (err) {
      console.error(`⚠️ 更新超时消息失败：${err.message}`);
    }
  }, timeoutMs);
}

/**
 * 降级方案：保存到本地审阅队列
 */
function saveReviewRequestLocally(draft) {
  const reviewDir = path.join(__dirname, 'reviews-pending');
  if (!fs.existsSync(reviewDir)) {
    fs.mkdirSync(reviewDir, { recursive: true });
  }

  const reviewId = `review-${Date.now()}`;
  const reviewFile = path.join(reviewDir, `${reviewId}.json`);

  const reviewData = {
    review_id: reviewId,
    draft_id: draft.draft_id,
    created_at: new Date().toISOString(),
    status: 'pending_local',
    channel: 'local_file',
    email: {
      subject: draft.subject,
      from: draft.from,
      intent: draft.intent
    },
    draft: {
      content: draft.reply || draft.content,
      wordCount: draft.wordCount
    },
    actions: {
      approve: `node discord-review.js approve ${reviewId}`,
      reject: `node discord-review.js reject ${reviewId}`
    }
  };

  fs.writeFileSync(reviewFile, JSON.stringify(reviewData, null, 2), 'utf8');
  console.log(`💾 审阅请求已保存到：${reviewFile}`);

  return {
    success: true,
    review_id: reviewId,
    channel: 'local_file',
    status: 'pending_approval',
    filePath: reviewFile
  };
}

/**
 * 处理审阅动作（被外部调用）
 */
async function processReviewAction(reviewId, action, token, channelId, messageId) {
  const reviewPath = path.join(__dirname, 'reviews-pending', `${reviewId}.json`);
  
  if (!fs.existsSync(reviewPath)) {
    throw new Error(`Review ${reviewId} not found`);
  }

  const review = JSON.parse(fs.readFileSync(reviewPath, 'utf8'));
  const draftId = review.draft_id;

  switch (action) {
    case 'send':
    case 'approve':
      console.log(`✅ 审阅通过，准备发送...`);
      
      // 读取草稿
      const draftPath = path.join(DRAFTS_DIR, `${draftId}.json`);
      const draft = JSON.parse(fs.readFileSync(draftPath, 'utf8'));
      
      // 发送邮件
      await sendEmail(draft);
      
      // 更新状态
      updateDraftStatus(draftId, 'sent', { sent_at: new Date().toISOString() });
      review.status = 'completed';
      review.action = 'sent';
      break;

    case 'discard':
    case 'reject':
      console.log(`❌ 草稿已丢弃`);
      updateDraftStatus(draftId, 'discarded', { discarded_at: new Date().toISOString() });
      review.status = 'completed';
      review.action = 'discarded';
      break;

    case 'edit':
      console.log(`✏️ 编辑请求（当前版本仅记录）`);
      review.status = 'edit_requested';
      break;

    default:
      throw new Error(`Unknown action: ${action}`);
  }

  review.completed_at = new Date().toISOString();
  fs.writeFileSync(reviewPath, JSON.stringify(review, null, 2), 'utf8');

  // 更新 Discord 消息
  if (messageId && channelId && token) {
    try {
      const embed = {
        title: action === 'send' ? '✅ Sent' : '❌ Discarded',
        description: action === 'send' ? 'Email has been sent.' : 'Draft has been discarded.',
        color: action === 'send' ? 0x00FF00 : 0xFF0000
      };
      
      await discordRequest(
        `channels/${channelId}/messages/${messageId}`,
        'PATCH',
        {
          embeds: [embed],
          components: []
        },
        token
      );
    } catch (err) {
      console.error(`⚠️ 更新 Discord 消息失败：${err.message}`);
    }
  }

  return review;
}

// ============ 测试模式 ============
function runTest() {
  console.log('🧪 运行测试模式（不实际发送）\n');

  // 模拟草稿
  const testDraft = {
    draft_id: `DRAFT-${Date.now()}-TEST`,
    subject: 'Re: Product Inquiry - HDMI Cable',
    from: 'customer@example.com',
    intent: 'inquiry',
    confidence: 0.92,
    escalate: false,
    reply: `Dear Customer,

Thank you for your inquiry about our HDMI cables.

We offer a wide range of HDMI solutions including:
- HDMI 2.1 (8K@60Hz, 4K@120Hz)
- HDMI 2.0 (4K@60Hz)
- Standard HDMI (1080p)

Please let us know your specific requirements (length, quantity, connector type) so we can provide an accurate quotation.

Best regards,
Farreach Electronic Team`,
    wordCount: 67,
    created_at: new Date().toISOString()
  };

  console.log('📋 模拟草稿数据:');
  console.log(JSON.stringify(testDraft, null, 2));

  // 构建 Embed
  const embed = buildEmbed(testDraft);
  console.log('\n📦 Discord Embed 结构:');
  console.log(JSON.stringify(embed, null, 2));

  // 构建按钮
  const components = buildActionComponents(testDraft.draft_id);
  console.log('\n🔘 按钮组件:');
  console.log(JSON.stringify(components, null, 2));

  // 检查配置
  console.log('\n⚙️ 配置检查:');
  const config = loadConfig();
  console.log(`  - 配置文件：${CONFIG_PATH}`);
  console.log(`  - Channel ID: ${config.channel_id || '(未配置)'}`);
  console.log(`  - Timeout: ${config.timeout_minutes} 分钟`);

  // 检查 Token
  const token = loadDiscordToken();
  console.log(`  - Token: ${token ? '✓ 已配置' : '✗ 未配置'}`);

  console.log('\n✅ 测试完成 - 模块结构正确');
}

// ============ CLI 入口 ============
async function main() {
  const args = process.argv.slice(2);
  
  if (args[0] === 'test') {
    runTest();
    return;
  }

  if (args[0] === 'approve' || args[0] === 'send') {
    const reviewId = args[1];
    if (!reviewId) {
      console.error('❌ 用法：node discord-review.js approve <review_id>');
      process.exit(1);
    }
    // 本地审批模式
    const token = loadDiscordToken();
    const config = loadConfig();
    await processReviewAction(reviewId, 'send', token, config.channel_id, null);
    console.log('✅ 审批完成');
    return;
  }

  if (args[0] === 'reject' || args[0] === 'discard') {
    const reviewId = args[1];
    if (!reviewId) {
      console.error('❌ 用法：node discord-review.js discard <review_id>');
      process.exit(1);
    }
    const token = loadDiscordToken();
    const config = loadConfig();
    await processReviewAction(reviewId, 'discard', token, config.channel_id, null);
    console.log('✅ 已丢弃草稿');
    return;
  }

  console.log('Discord Review Module');
  console.log('用法:');
  console.log('  node discord-review.js test     - 运行测试');
  console.log('  node discord-review.js approve <review_id>  - 审批通过');
  console.log('  node discord-review.js discard <review_id>  - 丢弃草稿');
  console.log('\n在代码中调用:');
  console.log('  const { sendForReview } = require("./discord-review.js");');
  console.log('  await sendForReview(draft);');
}

// 导出
module.exports = {
  sendForReview,
  processReviewAction,
  buildEmbed,
  buildActionComponents,
  updateDraftStatus,
  loadConfig,
  loadDiscordToken
};

// 直接运行时执行 main
if (require.main === module) {
  main().catch(err => {
    console.error('❌ 错误:', err.message);
    process.exit(1);
  });
}
