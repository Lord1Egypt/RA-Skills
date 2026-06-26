/**
 * E2E 模拟测试 - 不依赖企微连接，验证完整数据流
 *
 * 测试链路：
 *   模拟企微回调帧 → msg-converter → agent-bridge → test-agent (HTTP) → 回复验证
 *
 * 启动：node e2e-test.js
 */

const { spawn } = require('child_process');
const http = require('http');
const path = require('path');
const { wecomToStandard, standardToWecomReply } = require('./msg-converter');
const { AgentBridge } = require('./agent-bridge');

// ============================================================
// 模拟企微回调帧
// ============================================================
const MOCK_WECOM_FRAME = {
  cmd: 'aibot_msg_callback',
  headers: { req_id: 'REQ_TEST_E2E_001' },
  body: {
    msgid: 'MSG_TEST_001',
    aibotid: '你的BotID',
    chatid: 'CHAT_TEST_001',
    chattype: 'single',
    from: { userid: 'test_user_001' },
    msgtype: 'text',
    text: { content: '你好，请帮我查询订单1288的状态' },
  },
};

// ============================================================
// 验证结果
// ============================================================
let passed = 0;
let failed = 0;

function assert(condition, msg) {
  if (condition) {
    console.log(`  ✅ ${msg}`);
    passed++;
  } else {
    console.log(`  ❌ ${msg}`);
    failed++;
  }
}

// ============================================================
// 主测试
// ============================================================

async function runTests() {
  console.log('='.repeat(50));
  console.log('  E2E 模拟测试 - 企微 Agent Connector');
  console.log('='.repeat(50));
  console.log('');

  // ----------------------------------------------------------
  // 1. 启动测试 Agent
  // ----------------------------------------------------------
  console.log('📡 启动测试 Agent...');
  const agentProcess = spawn('node', [path.join(__dirname, 'test-agent.js')], {
    stdio: ['pipe', 'pipe', 'pipe'],
    env: { ...process.env, TEST_AGENT_PORT: '3001' },
  });

  // 等待 Agent 启动
  await new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('Agent 启动超时')), 5000);
    agentProcess.stdout.on('data', (data) => {
      if (data.toString().includes('已启动')) {
        clearTimeout(timeout);
        setTimeout(resolve, 500); // 额外等 500ms 确保 ready
      }
    });
    agentProcess.stderr.on('data', (data) => {
      console.log(`  [Agent stderr] ${data.toString().trim()}`);
    });
  });
  console.log('  ✅ 测试 Agent 已启动 (port 3001)\n');

  // ----------------------------------------------------------
  // 2. 测试 msg-converter：企微帧 → 标准化 JSON
  // ----------------------------------------------------------
  console.log('🔄 测试 1: msg-converter（企微帧 → 标准化 JSON）');

  const standardMsg = wecomToStandard(MOCK_WECOM_FRAME);
  console.log(`  标准化消息: ${JSON.stringify(standardMsg, null, 2)}`);

  assert(standardMsg.msg_id === 'MSG_TEST_001', 'msg_id 正确');
  assert(standardMsg.req_id === 'REQ_TEST_E2E_001', 'req_id 正确');
  assert(standardMsg.from.user_id === 'test_user_001', 'user_id 正确');
  assert(standardMsg.from.chat_type === 'single', 'chat_type 正确');
  assert(standardMsg.content === '你好，请帮我查询订单1288的状态', 'content 正确');
  assert(standardMsg.channel === 'wecom', 'channel 正确');
  console.log('');

  // ----------------------------------------------------------
  // 3. 测试 agent-bridge：转发到测试 Agent
  // ----------------------------------------------------------
  console.log('🌉 测试 2: agent-bridge（HTTP 转发 → Agent → 回复）');

  const bridge = new AgentBridge({
    endpoint: 'http://localhost:3001/chat',
    timeout: 10,
    retry: 2,
  });

  const reply = await bridge.forward(standardMsg);

  assert(reply !== null, 'Agent 有回复');
  assert(reply.reply_to === 'MSG_TEST_001', 'reply_to 正确');
  assert(reply.content && reply.content.includes('测试Agent'), '回复内容包含标识');
  assert(reply.content && reply.content.includes('订单1288'), '回复内容包含原消息');
  console.log(`  回复内容: ${reply ? reply.content.slice(0, 100) : 'null'}...`);
  console.log('');

  // ----------------------------------------------------------
  // 4. 测试 standardToWecomReply：回复 → 企微格式
  // ----------------------------------------------------------
  console.log('📤 测试 3: standardToWecomReply（标准化 → 企微回复体）');

  const markdownReply = standardToWecomReply(reply, 'markdown');
  console.log(`  markdown 回复体: ${JSON.stringify(markdownReply)}`);

  assert(markdownReply.msgtype === 'markdown', 'msgtype = markdown');
  assert(markdownReply.markdown && markdownReply.markdown.content, '有 markdown.content');

  const textReply = standardToWecomReply({ content: '纯文本测试' }, 'text');
  assert(textReply.msgtype === 'text', 'msgtype = text');
  assert(textReply.text && textReply.text.content === '纯文本测试', 'text.content 正确');

  console.log('');

  // ----------------------------------------------------------
  // 5. 测试 Agent 不可达场景
  // ----------------------------------------------------------
  console.log('🔌 测试 4: Agent 不可达（应返回 null）');

  const badBridge = new AgentBridge({
    endpoint: 'http://localhost:19999/chat',
    timeout: 2,
    retry: 1,
  });

  const noReply = await badBridge.forward(standardMsg);
  assert(noReply === null, '不可达 Agent 返回 null');
  console.log('');

  // ----------------------------------------------------------
  // 6. 测试多种消息类型
  // ----------------------------------------------------------
  console.log('📨 测试 5: 多种消息类型转换');

  // 图文混排
  const mixedFrame = {
    cmd: 'aibot_msg_callback',
    headers: { req_id: 'REQ_MIXED' },
    body: {
      msgid: 'MSG_MIXED',
      chatid: 'CHAT_001',
      chattype: 'group',
      from: { userid: 'user_001' },
      msgtype: 'mixed',
      mixed: {
        msg_item: [
          { msgtype: 'text', text: { content: '帮我看看这个' } },
          { msgtype: 'image', image: { url: 'http://...' } },
          { msgtype: 'text', text: { content: '价格对吗？' } },
        ],
      },
    },
  };
  const mixedStd = wecomToStandard(mixedFrame);
  assert(mixedStd.content === '帮我看看这个 价格对吗？', '图文混排内容提取正确');
  assert(mixedStd.from.chat_type === 'group', '群聊类型识别');

  // 语音消息
  const voiceFrame = {
    cmd: 'aibot_msg_callback',
    headers: { req_id: 'REQ_VOICE' },
    body: {
      msgid: 'MSG_VOICE',
      chatid: 'CHAT_001',
      chattype: 'single',
      from: { userid: 'user_001' },
      msgtype: 'voice',
      voice: { content: '语音转文字结果' },
    },
  };
  const voiceStd = wecomToStandard(voiceFrame);
  assert(voiceStd.content === '语音转文字结果', '语音消息内容提取');

  console.log('');

  // ----------------------------------------------------------
  // 结果汇总
  // ----------------------------------------------------------
  console.log('='.repeat(50));
  console.log(`  测试结果: ✅ ${passed} 通过  ❌ ${failed} 失败`);
  console.log('='.repeat(50));

  // 清理
  agentProcess.kill();

  if (failed > 0) {
    process.exit(1);
  }
}

runTests().catch(err => {
  console.error('💥 测试异常:', err);
  process.exit(1);
});
