/**
 * Multimodal Base - 语音识别模块
 * 基于 Whisper 实现语音转文字
 */

import { EventEmitter } from 'events';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs/promises';
import axios from 'axios';
import FormData from 'form-data';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * 语音识别器类
 */
export class SpeechRecognizer extends EventEmitter {
  /**
   * @param {Object} config
   * @param {string} config.mode - 模式：'local' | 'api'
   * @param {string} config.modelPath - Whisper 模型路径（本地模式）
   * @param {string} config.openaiApiKey - OpenAI API Key（API 模式）
   * @param {string} config.language - 语言（默认：zh）
   */
  constructor(config = {}) {
    super();
    this.mode = config.mode || 'api'; // 默认使用 API，更准确
    this.modelPath = config.modelPath || path.join(__dirname, '../models/ggml-base.bin');
    this.apiKey = config.openaiApiKey || process.env.OPENAI_API_KEY;
    this.language = config.language || 'zh';
    this.whisperPath = config.whisperPath || 'whisper'; // whisper.cpp 可执行文件
  }

  /**
   * 识别音频文件
   * @param {string} audioPath - 音频文件路径
   * @returns {Promise<Object>} - 识别结果
   */
  async recognize(audioPath) {
    this.emit('processing', { path: audioPath });

    try {
      let result;
      
      if (this.mode === 'local') {
        result = await this.recognizeLocal(audioPath);
      } else {
        result = await this.recognizeAPI(audioPath);
      }

      this.emit('completed', { path: audioPath, result });
      return result;

    } catch (error) {
      this.emit('error', { path: audioPath, error });
      throw new Error(`Speech recognition failed: ${error.message}`);
    }
  }

  /**
   * 本地识别（使用 whisper.cpp）
   */
  async recognizeLocal(audioPath) {
    return new Promise((resolve, reject) => {
      const args = [
        '-m', this.modelPath,
        '-f', audioPath,
        '-l', this.language,
        '--output-json',
        '--output-file', '-' // 输出到 stdout
      ];

      const whisper = spawn(this.whisperPath, args);
      let output = '';
      let errorOutput = '';

      whisper.stdout.on('data', (data) => {
        output += data.toString();
      });

      whisper.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      whisper.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(`Whisper exited with code ${code}: ${errorOutput}`));
          return;
        }

        try {
          // 解析输出
          const lines = output.split('\n').filter(line => line.trim());
          const text = lines.join(' ');
          
          resolve({
            text: text,
            language: this.language,
            mode: 'local',
            path: audioPath
          });
        } catch (e) {
          reject(new Error(`Failed to parse whisper output: ${e.message}`));
        }
      });
    });
  }

  /**
   * API 识别（使用 OpenAI Whisper API）
   */
  async recognizeAPI(audioPath) {
    const formData = new FormData();
    formData.append('file', await fs.readFile(audioPath), path.basename(audioPath));
    formData.append('model', 'whisper-1');
    formData.append('language', this.language);
    formData.append('response_format', 'verbose_json');

    const response = await axios.post(
      'https://api.openai.com/v1/audio/transcriptions',
      formData,
      {
        headers: {
          ...formData.getHeaders(),
          'Authorization': `Bearer ${this.apiKey}`
        },
        timeout: 60000,
        maxBodyLength: Infinity,
        maxContentLength: Infinity
      }
    );

    const data = response.data;
    
    return {
      text: data.text,
      language: data.language,
      confidence: data.segments?.[0]?.avg_logprob || 0,
      segments: data.segments?.map(s => ({
        start: s.start,
        end: s.end,
        text: s.text,
        confidence: s.avg_logprob
      })) || [],
      mode: 'api',
      path: audioPath
    };
  }

  /**
   * 实时流式识别（实验性）
   * @param {ReadableStream} audioStream - 音频流
   * @returns {Promise<Object>} - 识别结果
   */
  async recognizeStream(audioStream) {
    // 将流保存为临时文件
    const tmpPath = path.join(__dirname, `../tmp/stream_${Date.now()}.wav`);
    
    try {
      await fs.mkdir(path.dirname(tmpPath), { recursive: true });
      
      const chunks = [];
      for await (const chunk of audioStream) {
        chunks.push(chunk);
      }
      
      const buffer = Buffer.concat(chunks);
      await fs.writeFile(tmpPath, buffer);
      
      // 识别临时文件
      const result = await this.recognize(tmpPath);
      
      // 清理临时文件
      await fs.unlink(tmpPath).catch(() => {});
      
      return result;
      
    } catch (error) {
      // 清理临时文件
      await fs.unlink(tmpPath).catch(() => {});
      throw error;
    }
  }

  /**
   * 批量识别
   * @param {Array<string>} audioPaths - 音频路径数组
   * @returns {Promise<Array>} - 结果数组
   */
  async batchRecognize(audioPaths) {
    const results = [];
    
    for (const audioPath of audioPaths) {
      try {
        const result = await this.recognize(audioPath);
        results.push({ path: audioPath, success: true, result });
      } catch (error) {
        results.push({ path: audioPath, success: false, error: error.message });
      }
    }

    return results;
  }

  /**
   * 检查模型文件是否存在
   */
  async checkModel() {
    if (this.mode !== 'local') return true;
    
    try {
      await fs.access(this.modelPath);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * 下载模型
   */
  async downloadModel() {
    if (this.mode !== 'local') return;
    
    const modelUrl = 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin';
    
    console.log(`Downloading Whisper model to ${this.modelPath}...`);
    
    const response = await axios({
      method: 'GET',
      url: modelUrl,
      responseType: 'stream'
    });

    await fs.mkdir(path.dirname(this.modelPath), { recursive: true });
    
    const writer = (await import('fs')).createWriteStream(this.modelPath);
    response.data.pipe(writer);

    return new Promise((resolve, reject) => {
      writer.on('finish', resolve);
      writer.on('error', reject);
    });
  }

  /**
   * 验证音频文件
   */
  async validateAudio(audioPath) {
    try {
      const stats = await fs.stat(audioPath);
      if (!stats.isFile()) {
        throw new Error('Path is not a file');
      }

      // 检查文件大小（最大 25MB - OpenAI 限制）
      if (stats.size > 25 * 1024 * 1024) {
        throw new Error('Audio too large (max 25MB)');
      }

      return true;
    } catch (error) {
      throw new Error(`Audio validation failed: ${error.message}`);
    }
  }
}

export default SpeechRecognizer;
