/**
 * Multimodal Base - 统一多模态管道
 * 整合图像、语音、文本的统一处理
 */

import ImageProcessor from './image-processor.js';
import SpeechRecognizer from './speech-recognizer.js';
import SpeechSynthesizer from './speech-synthesizer.js';
import { EventEmitter } from 'events';

/**
 * 多模态消息格式
 */
export class MultimodalMessage {
  constructor(data) {
    this.id = data.id || `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    this.timestamp = data.timestamp || Date.now();
    this.role = data.role || 'user'; // 'user' | 'assistant'
    this.content = data.content || {};
    this.metadata = data.metadata || {};
  }

  /**
   * 获取所有模态类型
   */
  getModalities() {
    const modalities = [];
    if (this.content.text) modalities.push('text');
    if (this.content.image) modalities.push('image');
    if (this.content.audio) modalities.push('audio');
    return modalities;
  }

  /**
   * 转换为纯文本表示
   */
  toText() {
    let text = '';
    
    if (this.content.text) {
      text += this.content.text;
    }
    
    if (this.content.image?.description) {
      text += `\n[图像: ${this.content.image.description}]`;
    }
    
    if (this.content.audio?.transcript) {
      text += `\n[语音: ${this.content.audio.transcript}]`;
    }
    
    return text.trim();
  }
}

/**
 * 多模态管道类
 */
export class MultimodalPipeline extends EventEmitter {
  /**
   * @param {Object} config
   * @param {Object} config.image - 图像处理配置
   * @param {Object} config.speech - 语音识别配置
   * @param {Object} config.tts - 语音合成配置
   */
  constructor(config = {}) {
    super();
    
    // 初始化各模块
    this.imageProcessor = new ImageProcessor(config.image);
    this.speechRecognizer = new SpeechRecognizer(config.speech);
    this.speechSynthesizer = new SpeechSynthesizer(config.tts);
    
    // 消息历史
    this.history = [];
    this.maxHistory = config.maxHistory || 100;
  }

  /**
   * 处理输入（统一入口）
   * @param {Object} input - 输入数据
   * @returns {Promise<MultimodalMessage>} - 处理后的消息
   */
  async processInput(input) {
    this.emit('processing', { type: 'input', input });

    const message = new MultimodalMessage({
      role: 'user',
      content: {},
      metadata: {
        rawInput: input,
        processedAt: Date.now()
      }
    });

    try {
      // 根据输入类型处理
      if (input.type === 'text') {
        message.content.text = input.content;
      }
      
      else if (input.type === 'image') {
        // 处理图像
        const imageResult = await this.imageProcessor.understand(
          input.path,
          input.prompt || '描述这张图片的内容'
        );
        
        message.content.image = {
          path: input.path,
          description: imageResult.description,
          tokens: imageResult.tokens
        };
        
        // 同时生成文本表示
        message.content.text = `[图像: ${imageResult.description}]`;
      }
      
      else if (input.type === 'audio') {
        // 处理语音
        const audioResult = await this.speechRecognizer.recognize(input.path);
        
        message.content.audio = {
          path: input.path,
          transcript: audioResult.text,
          confidence: audioResult.confidence,
          language: audioResult.language
        };
        
        message.content.text = audioResult.text;
      }
      
      else if (input.type === 'multimodal') {
        // 处理多模态输入
        if (input.text) {
          message.content.text = input.text;
        }
        
        if (input.image) {
          const imageResult = await this.imageProcessor.understand(input.image);
          message.content.image = {
            path: input.image,
            description: imageResult.description
          };
        }
        
        if (input.audio) {
          const audioResult = await this.speechRecognizer.recognize(input.audio);
          message.content.audio = {
            path: input.audio,
            transcript: audioResult.text
          };
        }
      }

      // 保存到历史
      this.addToHistory(message);
      
      this.emit('processed', { message });
      return message;

    } catch (error) {
      this.emit('error', { type: 'input', error });
      throw error;
    }
  }

  /**
   * 生成输出（支持语音）
   * @param {string} text - 要输出的文本
   * @param {Object} options - 选项
   * @returns {Promise<MultimodalMessage>} - 输出消息
   */
  async generateOutput(text, options = {}) {
    this.emit('generating', { text, options });

    const message = new MultimodalMessage({
      role: 'assistant',
      content: { text },
      metadata: {
        generatedAt: Date.now()
      }
    });

    try {
      // 如果需要语音输出
      if (options.speak) {
        const ttsResult = await this.speechSynthesizer.synthesize(text, {
          voice: options.voice,
          rate: options.rate,
          pitch: options.pitch
        });
        
        message.content.audio = {
          path: ttsResult.audioPath,
          voice: ttsResult.voice,
          duration: ttsResult.duration
        };
      }

      // 保存到历史
      this.addToHistory(message);
      
      this.emit('generated', { message });
      return message;

    } catch (error) {
      this.emit('error', { type: 'output', error });
      throw error;
    }
  }

  /**
   * 添加到历史
   */
  addToHistory(message) {
    this.history.push(message);
    
    // 限制历史长度
    if (this.history.length > this.maxHistory) {
      this.history = this.history.slice(-this.maxHistory);
    }
  }

  /**
   * 获取历史消息
   */
  getHistory(options = {}) {
    let history = this.history;
    
    // 按角色过滤
    if (options.role) {
      history = history.filter(m => m.role === options.role);
    }
    
    // 按模态过滤
    if (options.modality) {
      history = history.filter(m => m.getModalities().includes(options.modality));
    }
    
    // 限制数量
    if (options.limit) {
      history = history.slice(-options.limit);
    }
    
    return history;
  }

  /**
   * 清空历史
   */
  clearHistory() {
    this.history = [];
    this.emit('history-cleared');
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const stats = {
      totalMessages: this.history.length,
      byRole: {},
      byModality: {}
    };

    for (const message of this.history) {
      // 按角色统计
      stats.byRole[message.role] = (stats.byRole[message.role] || 0) + 1;
      
      // 按模态统计
      for (const modality of message.getModalities()) {
        stats.byModality[modality] = (stats.byModality[modality] || 0) + 1;
      }
    }

    return stats;
  }

  /**
   * 批量处理
   */
  async batchProcess(inputs) {
    const results = [];
    
    for (const input of inputs) {
      try {
        const result = await this.processInput(input);
        results.push({ input, success: true, result });
      } catch (error) {
        results.push({ input, success: false, error: error.message });
      }
    }

    return results;
  }

  /**
   * 导出对话
   */
  exportConversation(format = 'json') {
    if (format === 'json') {
      return JSON.stringify(this.history, null, 2);
    }
    
    if (format === 'text') {
      return this.history.map(m => {
        const role = m.role === 'user' ? '用户' : '助手';
        return `${role}: ${m.toText()}`;
      }).join('\n\n');
    }
    
    throw new Error(`Unsupported format: ${format}`);
  }
}

export default MultimodalPipeline;
