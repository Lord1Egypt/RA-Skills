/**
 * Multimodal Base 测试套件
 */

import { MultimodalPipeline, MultimodalMessage } from '../src/multimodal-pipeline.js';
import ImageProcessor from '../src/image-processor.js';
import SpeechSynthesizer from '../src/speech-synthesizer.js';

// 测试配置
const testConfig = {
  image: {
    openaiApiKey: process.env.OPENAI_API_KEY || 'test-key'
  },
  speech: {
    mode: 'api',
    openaiApiKey: process.env.OPENAI_API_KEY || 'test-key'
  },
  tts: {
    outputDir: './test-output'
  }
};

// 测试运行器
class TestRunner {
  constructor() {
    this.tests = [];
    this.passed = 0;
    this.failed = 0;
  }

  test(name, fn) {
    this.tests.push({ name, fn });
  }

  async run() {
    console.log('🧪 Multimodal Base Test Suite Starting...\n');
    
    for (const { name, fn } of this.tests) {
      try {
        await fn();
        console.log(`✓ ${name}`);
        this.passed++;
      } catch (error) {
        console.log(`✗ ${name}`);
        console.log(`  Error: ${error.message}`);
        this.failed++;
      }
    }
    
    console.log(`\n📊 Results: ${this.passed} passed, ${this.failed} failed`);
    return this.failed === 0;
  }
}

const runner = new TestRunner();

// === MultimodalMessage Tests ===
runner.test('MultimodalMessage - should create message', async () => {
  const msg = new MultimodalMessage({
    role: 'user',
    content: { text: 'Hello' }
  });
  if (!msg.id || !msg.timestamp) throw new Error('Message should have id and timestamp');
  if (msg.content.text !== 'Hello') throw new Error('Content mismatch');
});

runner.test('MultimodalMessage - should detect text modality', async () => {
  const msg = new MultimodalMessage({
    content: { text: 'Hello' }
  });
  const modalities = msg.getModalities();
  if (!modalities.includes('text')) throw new Error('Should detect text modality');
});

runner.test('MultimodalMessage - should detect image modality', async () => {
  const msg = new MultimodalMessage({
    content: { image: { path: './test.jpg' } }
  });
  const modalities = msg.getModalities();
  if (!modalities.includes('image')) throw new Error('Should detect image modality');
});

runner.test('MultimodalMessage - should detect audio modality', async () => {
  const msg = new MultimodalMessage({
    content: { audio: { path: './test.wav' } }
  });
  const modalities = msg.getModalities();
  if (!modalities.includes('audio')) throw new Error('Should detect audio modality');
});

runner.test('MultimodalMessage - should convert to text', async () => {
  const msg = new MultimodalMessage({
    content: { 
      text: 'Hello',
      image: { description: 'A cat' }
    }
  });
  const text = msg.toText();
  if (!text.includes('Hello')) throw new Error('Should include text content');
  if (!text.includes('A cat')) throw new Error('Should include image description');
});

// === MultimodalPipeline Tests ===
runner.test('MultimodalPipeline - should initialize', async () => {
  const pipeline = new MultimodalPipeline(testConfig);
  if (!pipeline) throw new Error('Failed to initialize');
});

runner.test('MultimodalPipeline - should process text input', async () => {
  const pipeline = new MultimodalPipeline(testConfig);
  const result = await pipeline.processInput({
    type: 'text',
    content: 'Hello world'
  });
  if (!result.content.text) throw new Error('Should process text input');
});

// === ImageProcessor Tests ===
runner.test('ImageProcessor - should initialize', async () => {
  const processor = new ImageProcessor(testConfig.image);
  if (!processor) throw new Error('Failed to initialize');
});

// === SpeechSynthesizer Tests ===
runner.test('SpeechSynthesizer - should initialize', async () => {
  const tts = new SpeechSynthesizer(testConfig.tts);
  if (!tts) throw new Error('Failed to initialize');
});

runner.test('SpeechSynthesizer - should list voices', async () => {
  const tts = new SpeechSynthesizer(testConfig.tts);
  const voices = tts.getVoices();
  if (!voices || voices.length === 0) throw new Error('Should return voices');
  if (!voices.some(v => v.id.includes('zh-CN'))) throw new Error('Should include Chinese voices');
});

// 运行测试
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
