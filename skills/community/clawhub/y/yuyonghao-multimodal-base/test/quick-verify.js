/**
 * Multimodal Base - 快速验证
 * 验证各模块基本功能
 */

import ImageProcessor from '../src/image-processor.js';
import SpeechSynthesizer from '../src/speech-synthesizer.js';
import { MultimodalPipeline } from '../src/multimodal-pipeline.js';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs/promises';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

console.log('🧪 Multimodal Base Quick Verification\n');

async function verifyImageProcessor() {
  console.log('📷 Testing ImageProcessor...');
  
  const processor = new ImageProcessor({
    openaiApiKey: process.env.OPENAI_API_KEY || 'test-key'
  });
  
  // 测试 MIME 类型检测
  const mimeType = processor.getMimeType('test.jpg');
  console.assert(mimeType === 'image/jpeg', 'JPEG MIME type should be correct');
  
  const mimeType2 = processor.getMimeType('test.png');
  console.assert(mimeType2 === 'image/png', 'PNG MIME type should be correct');
  
  console.log('✅ ImageProcessor basic tests passed\n');
}

async function verifySpeechSynthesizer() {
  console.log('🔊 Testing SpeechSynthesizer...');
  
  const tts = new SpeechSynthesizer({
    outputDir: path.join(__dirname, '../test-output')
  });
  
  // 测试音色列表
  const voices = tts.getVoices();
  console.assert(voices.length > 0, 'Should have voices');
  console.assert(voices.some(v => v.id === 'zh-CN-XiaoxiaoNeural'), 'Should have Chinese voice');
  
  // 测试推荐音色
  const recommended = tts.getRecommendedVoice('zh-CN', 'Female');
  console.assert(recommended.length > 0, 'Should have recommended voices');
  
  // 测试 SSML 生成
  const ssml = tts.generateSSML('你好', { voice: 'zh-CN-XiaoxiaoNeural' });
  console.assert(ssml.includes('<speak'), 'SSML should be valid');
  console.assert(ssml.includes('你好'), 'SSML should contain text');
  
  console.log('✅ SpeechSynthesizer basic tests passed\n');
}

async function verifyMultimodalPipeline() {
  console.log('🔄 Testing MultimodalPipeline...');
  
  const pipeline = new MultimodalPipeline({
    maxHistory: 10
  });
  
  // 测试文本输入
  const textMessage = await pipeline.processInput({
    type: 'text',
    content: '你好'
  });
  
  console.assert(textMessage.content.text === '你好', 'Text content should match');
  console.assert(textMessage.role === 'user', 'Role should be user');
  
  // 测试历史记录
  const history = pipeline.getHistory();
  console.assert(history.length === 1, 'Should have 1 message in history');
  
  // 测试统计
  const stats = pipeline.getStats();
  console.assert(stats.totalMessages === 1, 'Stats should show 1 message');
  console.assert(stats.byRole.user === 1, 'Stats should show 1 user message');
  
  // 测试清空历史
  pipeline.clearHistory();
  console.assert(pipeline.history.length === 0, 'History should be cleared');
  
  console.log('✅ MultimodalPipeline basic tests passed\n');
}

async function verifyMultimodalMessage() {
  console.log('💬 Testing MultimodalMessage...');
  
  const { MultimodalMessage } = await import('../src/multimodal-pipeline.js');
  
  // 测试纯文本消息
  const textMsg = new MultimodalMessage({
    role: 'user',
    content: { text: '你好' }
  });
  
  console.assert(textMsg.getModalities().includes('text'), 'Should have text modality');
  console.assert(textMsg.toText() === '你好', 'Text conversion should work');
  
  // 测试图像消息
  const imageMsg = new MultimodalMessage({
    role: 'user',
    content: {
      text: '请看这张图',
      image: { path: './photo.jpg', description: '一只猫' }
    }
  });
  
  console.assert(imageMsg.getModalities().includes('image'), 'Should have image modality');
  console.assert(imageMsg.toText().includes('一只猫'), 'Should include image description');
  
  console.log('✅ MultimodalMessage basic tests passed\n');
}

async function main() {
  try {
    await verifyImageProcessor();
    await verifySpeechSynthesizer();
    await verifyMultimodalPipeline();
    await verifyMultimodalMessage();
    
    console.log('='.repeat(50));
    console.log('✅ All verifications passed!');
    console.log('='.repeat(50));
    console.log('\n📊 Summary:');
    console.log('- ImageProcessor: Basic functions working');
    console.log('- SpeechSynthesizer: Voices and SSML working');
    console.log('- MultimodalPipeline: Message processing working');
    console.log('- MultimodalMessage: Format conversion working');
    
    process.exit(0);
  } catch (e) {
    console.error('❌ Verification failed:', e);
    process.exit(1);
  }
}

main();
