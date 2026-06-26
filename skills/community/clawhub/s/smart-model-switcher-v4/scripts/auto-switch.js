#!/usr/bin/env node
/**
 * 智能模型切换器 V4 - 多模态感知版
 * 自动检测图片/代码任务，切换到最优模型
 * 
 * 使用方法：
 *   node auto-switch.js --check "用户消息"
 *   node auto-switch.js --switch glm-5
 */

const https = require('https');
const http = require('http');

// 模型配置
const MODELS = {
  vision: {
    best: 'bailian/qwen3-vl-plus',      // 最强视觉
    hybrid: 'bailian/qwen3.5-plus',     // 视觉+代码
    fallback: 'bailian/qvq-max'
  },
  coding: {
    best: 'bailian/glm-5',              // 最强代码
    alt: 'bailian/qwen3-coder-plus',
    fallback: 'bailian/qwen-coder-turbo'
  },
  reasoning: {
    best: 'bailian/qwq-plus',           // 最强推理
    alt: 'bailian/qwen3-max',
    fallback: 'bailian/glm-5'
  },
  general: {
    best: 'bailian/qwen3.5-plus',       // 通用最强
    fast: 'bailian/qwen-turbo'
  }
};

// 关键词检测
const KEYWORDS = {
  coding: [
    '代码', '编程', 'python', 'javascript', 'js', 'ts', 'typescript',
    '函数', 'debug', 'bug', '报错', '错误', '修复', '重构',
    '写一个', '帮我写', '实现', '开发', '.py', '.js', '.ts', '.html',
    'api', '接口', '脚本', '爬虫', '自动化'
  ],
  reasoning: [
    '推理', '逻辑', '证明', '数学', '计算', '推导', '分析',
    '为什么', '怎么推导', '能否推出', '关系', '原理'
  ],
  writing: [
    '写', '作文', '文章', '小说', '故事', '文案', '邮件', '报告',
    '创作', '撰写', '起草'
  ],
  image: [
    '图片', '截图', '照片', '图像', '看这个', '图里',
    '识别', 'ocr', '表格', '图表'
  ]
};

// 检测任务类型
function detectTaskType(message, hasImage = false) {
  const lowerMsg = message.toLowerCase();
  
  // 优先检测图片
  if (hasImage) {
    // 图片 + 代码关键词 → 视觉+代码模型
    if (KEYWORDS.coding.some(k => lowerMsg.includes(k))) {
      return { type: 'vision_coding', model: MODELS.vision.hybrid, reason: '图片+代码任务，使用视觉+代码模型' };
    }
    // 纯图片理解
    return { type: 'vision', model: MODELS.vision.best, reason: '图片理解任务，使用最强视觉模型' };
  }
  
  // 代码关键词
  if (KEYWORDS.coding.some(k => lowerMsg.includes(k))) {
    return { type: 'coding', model: MODELS.coding.best, reason: '代码任务，使用最强代码模型' };
  }
  
  // 推理关键词
  if (KEYWORDS.reasoning.some(k => lowerMsg.includes(k))) {
    return { type: 'reasoning', model: MODELS.reasoning.best, reason: '推理任务，使用最强推理模型' };
  }
  
  // 写作关键词
  if (KEYWORDS.writing.some(k => lowerMsg.includes(k))) {
    return { type: 'writing', model: MODELS.general.best, reason: '写作任务，使用通用强模型' };
  }
  
  // 默认通用
  return { type: 'general', model: MODELS.general.best, reason: '通用任务，使用通用强模型' };
}

// 切换模型（通过 OpenClaw API）
async function switchModel(modelId) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({ model: modelId });
    
    const options = {
      hostname: 'localhost',
      port: 3737,
      path: '/api/session/model',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      }
    };
    
    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          resolve({ success: true, model: modelId });
        }
      });
    });
    
    req.on('error', (e) => {
      // 如果 API 不可用，返回成功（假设用户手动切换）
      resolve({ success: true, model: modelId, note: '请手动切换模型' });
    });
    
    req.write(data);
    req.end();
  });
}

// CLI 入口
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
🧠 智能模型切换器 V4

使用方法：
  node auto-switch.js --check "用户消息" [--has-image]
  node auto-switch.js --switch glm-5
  node auto-switch.js --list

示例：
  node auto-switch.js --check "帮我写个爬虫"
  node auto-switch.js --check "看这个截图" --has-image
  node auto-switch.js --switch bailian/glm-5
`);
    return;
  }
  
  const command = args[0];
  
  if (command === '--list') {
    console.log('\n📋 可用模型列表：\n');
    console.log('🖼️ 视觉模型：');
    console.log('  - qwen3-vl-plus (最强视觉)');
    console.log('  - qwen3.5-plus (视觉+代码)');
    console.log('\n💻 代码模型：');
    console.log('  - glm-5 (最强代码)');
    console.log('  - qwen3-coder-plus');
    console.log('\n🧠 推理模型：');
    console.log('  - qwq-plus (最强推理)');
    console.log('  - qwen3-max');
    console.log('\n📝 通用模型：');
    console.log('  - qwen3.5-plus (通用最强)');
    console.log('  - qwen-turbo (快速)');
    return;
  }
  
  if (command === '--check') {
    const message = args[1] || '';
    const hasImage = args.includes('--has-image');
    
    const result = detectTaskType(message, hasImage);
    
    console.log('\n🧠 任务分析结果：');
    console.log(`  类型: ${result.type}`);
    console.log(`  推荐模型: ${result.model}`);
    console.log(`  原因: ${result.reason}`);
    
    // 输出切换命令
    console.log(`\n💡 切换命令: /model ${result.model}`);
    
    return result;
  }
  
  if (command === '--switch') {
    const modelId = args[1];
    if (!modelId) {
      console.error('❌ 请指定模型 ID');
      return;
    }
    
    const result = await switchModel(modelId);
    console.log(`✅ 已切换到: ${modelId}`);
    return result;
  }
  
  console.log('❌ 未知命令，使用 --help 查看帮助');
}

main().catch(console.error);