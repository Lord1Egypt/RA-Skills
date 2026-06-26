/**
 * Multimodal Base - 语音合成模块
 * 基于 Edge TTS 实现文字转语音
 */

import { EventEmitter } from 'events';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs/promises';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * 语音合成器类
 */
export class SpeechSynthesizer extends EventEmitter {
  /**
   * @param {Object} config
   * @param {string} config.outputDir - 输出目录
   * @param {string} config.defaultVoice - 默认音色
   */
  constructor(config = {}) {
    super();
    this.outputDir = config.outputDir || path.join(__dirname, '../output');
    this.defaultVoice = config.defaultVoice || 'zh-CN-XiaoxiaoNeural';
    
    // 可用音色列表
    this.voices = {
      // 中文女声
      'zh-CN-XiaoxiaoNeural': { name: '晓晓', gender: 'Female', locale: 'zh-CN' },
      'zh-CN-XiaoyiNeural': { name: '晓伊', gender: 'Female', locale: 'zh-CN' },
      // 中文男声
      'zh-CN-YunjianNeural': { name: '云健', gender: 'Male', locale: 'zh-CN' },
      'zh-CN-YunxiNeural': { name: '云希', gender: 'Male', locale: 'zh-CN' },
      // 英文
      'en-US-AriaNeural': { name: 'Aria', gender: 'Female', locale: 'en-US' },
      'en-US-GuyNeural': { name: 'Guy', gender: 'Male', locale: 'en-US' },
      // 日文
      'ja-JP-NanamiNeural': { name: '七海', gender: 'Female', locale: 'ja-JP' },
      // 韩文
      'ko-KR-SunHiNeural': { name: '善熙', gender: 'Female', locale: 'ko-KR' }
    };
  }

  /**
   * 合成语音
   * @param {string} text - 要合成的文本
   * @param {Object} options - 选项
   * @returns {Promise<Object>} - 合成结果
   */
  async synthesize(text, options = {}) {
    this.emit('synthesizing', { text });

    try {
      const voice = options.voice || this.defaultVoice;
      const rate = options.rate || 1.0;
      const pitch = options.pitch || 0;
      const volume = options.volume || 100;

      // 生成输出文件名
      const outputFile = path.join(
        this.outputDir,
        `tts_${Date.now()}_${Math.random().toString(36).substr(2, 9)}.mp3`
      );

      // 确保输出目录存在
      await fs.mkdir(this.outputDir, { recursive: true });

      // 使用 edge-tts 命令行工具
      const args = [
        '--voice', voice,
        '--rate', `${(rate - 1) * 100}%`,
        '--pitch', `${pitch}Hz`,
        '--volume', `${volume}%`,
        '--text', text,
        '--write-media', outputFile
      ];

      await this.runEdgeTTS(args);

      const result = {
        text: text,
        audioPath: outputFile,
        voice: voice,
        voiceInfo: this.voices[voice],
        rate: rate,
        pitch: pitch,
        duration: await this.getAudioDuration(outputFile)
      };

      this.emit('completed', { result });
      return result;

    } catch (error) {
      this.emit('error', { error });
      throw new Error(`Speech synthesis failed: ${error.message}`);
    }
  }

  /**
   * 使用 SSML 合成（高级控制）
   * @param {string} ssml - SSML 文本
   * @param {Object} options - 选项
   * @returns {Promise<Object>} - 合成结果
   */
  async synthesizeSSML(ssml, options = {}) {
    this.emit('synthesizing', { ssml });

    try {
      const voice = options.voice || this.defaultVoice;
      const outputFile = path.join(
        this.outputDir,
        `tts_ssml_${Date.now()}.mp3`
      );

      await fs.mkdir(this.outputDir, { recursive: true });

      // 将 SSML 保存为临时文件
      const ssmlFile = path.join(this.outputDir, `tmp_${Date.now()}.ssml`);
      await fs.writeFile(ssmlFile, ssml, 'utf-8');

      // 使用 edge-tts
      const args = [
        '--voice', voice,
        '--file', ssmlFile,
        '--write-media', outputFile
      ];

      await this.runEdgeTTS(args);

      // 清理临时文件
      await fs.unlink(ssmlFile).catch(() => {});

      const result = {
        ssml: ssml,
        audioPath: outputFile,
        voice: voice,
        duration: await this.getAudioDuration(outputFile)
      };

      this.emit('completed', { result });
      return result;

    } catch (error) {
      this.emit('error', { error });
      throw new Error(`SSML synthesis failed: ${error.message}`);
    }
  }

  /**
   * 运行 edge-tts 命令
   */
  async runEdgeTTS(args) {
    return new Promise((resolve, reject) => {
      const edgeTTS = spawn('edge-tts', args);
      let errorOutput = '';

      edgeTTS.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      edgeTTS.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(`edge-tts exited with code ${code}: ${errorOutput}`));
        } else {
          resolve();
        }
      });

      edgeTTS.on('error', (err) => {
        reject(new Error(`Failed to start edge-tts: ${err.message}`));
      });
    });
  }

  /**
   * 批量合成
   * @param {Array<string>} texts - 文本数组
   * @param {Object} options - 选项
   * @returns {Promise<Array>} - 结果数组
   */
  async batchSynthesize(texts, options = {}) {
    const results = [];
    
    for (const text of texts) {
      try {
        const result = await this.synthesize(text, options);
        results.push({ text, success: true, result });
      } catch (error) {
        results.push({ text, success: false, error: error.message });
      }
    }

    return results;
  }

  /**
   * 获取音频时长（秒）
   */
  async getAudioDuration(audioPath) {
    try {
      // 使用 ffprobe 获取时长
      return new Promise((resolve, reject) => {
        const ffprobe = spawn('ffprobe', [
          '-v', 'error',
          '-show_entries', 'format=duration',
          '-of', 'default=noprint_wrappers=1:nokey=1',
          audioPath
        ]);

        let output = '';
        ffprobe.stdout.on('data', (data) => {
          output += data.toString();
        });

        ffprobe.on('close', (code) => {
          if (code === 0) {
            resolve(parseFloat(output.trim()));
          } else {
            resolve(0); // 无法获取时长时返回 0
          }
        });
      });
    } catch {
      return 0;
    }
  }

  /**
   * 获取可用音色列表
   */
  getVoices() {
    return Object.entries(this.voices).map(([id, info]) => ({
      id,
      ...info
    }));
  }

  /**
   * 获取推荐音色
   * @param {string} locale - 语言区域
   * @param {string} gender - 性别
   */
  getRecommendedVoice(locale = 'zh-CN', gender = 'Female') {
    return Object.entries(this.voices)
      .filter(([id, info]) => info.locale === locale && info.gender === gender)
      .map(([id, info]) => ({ id, ...info }));
  }

  /**
   * 生成简单 SSML
   */
  generateSSML(text, options = {}) {
    const rate = options.rate ? `rate="${(options.rate - 1) * 100}%"` : '';
    const pitch = options.pitch ? `pitch="${options.pitch}Hz"` : '';
    
    return `<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
  <voice name="${options.voice || this.defaultVoice}">
    <prosody ${rate} ${pitch}>
      ${text}
    </prosody>
  </voice>
</speak>`;
  }

  /**
   * 清理输出目录
   */
  async cleanup(maxAge = 24 * 60 * 60 * 1000) {
    try {
      const files = await fs.readdir(this.outputDir);
      const now = Date.now();

      for (const file of files) {
        const filePath = path.join(this.outputDir, file);
        const stats = await fs.stat(filePath);
        
        if (now - stats.mtime.getTime() > maxAge) {
          await fs.unlink(filePath);
        }
      }
    } catch (error) {
      console.warn('Cleanup failed:', error);
    }
  }
}

export default SpeechSynthesizer;
