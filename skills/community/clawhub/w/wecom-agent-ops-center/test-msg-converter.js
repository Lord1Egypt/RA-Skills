#!/usr/bin/env node
/**
 * 测试 msg-converter.js 的云端 API 调用
 */

// 注入环境变量（模拟 config.yaml 配置）
process.env.CONVERTER_API_BASE = 'https://www.hermesai.ltd';
process.env.CONVERTER_API_KEY  = '你的API密钥';

const { wecomToStandard, standardToWecomReply, standardToWecomCard } = require('./msg-converter.js');

// 测试用例 1：文本消息
async function testText() {
  console.log('=== 测试1：文本消息 toStandard ===');
  const frame = {
    headers: { req_id: 'T1' },
    body: {
      msgid: 'M001',
      msgtype: 'text',
      chattype: 'single',
      from: { userid: 'user1', name: '张三' },
      text: { content: '你好，我是张三' },
    },
  };

  try {
    const result = await wecomToStandard(frame);
    console.log('✅ toStandard 成功：');
    console.log(JSON.stringify(result, null, 2));
  } catch (e) {
    console.error('❌ toStandard 失败：', e.message);
  }
}

// 测试用例 2：回复转企微格式
async function testReply() {
  console.log('\n=== 测试2：回复 toWecom ===');
  const reply = {
    content: '你好张三！我是 AI 助手，有什么可以帮你？',
    msg_type: 'markdown',
  };

  try {
    const result = await standardToWecomReply(reply);
    console.log('✅ toWecom 成功：');
    console.log(JSON.stringify(result, null, 2));
  } catch (e) {
    console.error('❌ toWecom 失败：', e.message);
  }
}

// 运行测试
(async () => {
  await testText();
  await testReply();
  console.log('\n✅ 测试完成');
})();
