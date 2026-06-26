// Volcengine Doubao STT/TTS integration for xiaozhiclaw
// https://www.volcengine.com/docs/6561/142162

import https from 'https';

// Load environment variables from .env file
import 'dotenv/config';

export interface DoubaoConfig {
  appId: string;
  accessToken: string;
  cluster: string;
  apiHost: string;
  voiceType?: string;
}

export const DEFAULT_DOUBAO_CONFIG: DoubaoConfig = {
  appId: process.env.DOUBAO_APP_ID || '',
  accessToken: process.env.DOUBAO_ACCESS_TOKEN || '',
  cluster: process.env.DOUBAO_CLUSTER || 'volcano_tts',
  apiHost: 'openspeech.bytedance.com',
  voiceType: process.env.DOUBAO_VOICE_TYPE || 'zh_female_tianmei_moon_bigtts',
};

export class DoubaoService {
  private config: DoubaoConfig;

  constructor(config: DoubaoConfig = DEFAULT_DOUBAO_CONFIG) {
    this.config = config;
  }

  /**
   * Speech-to-Text: Convert audio (PCM/WAV) to text
   * API: https://www.volcengine.com/docs/6561/142162
   */
  async speechToText(audioData: Buffer, sampleRate: number = 16000): Promise<string> {
    const params = {
      app: {
        appid: this.config.appId,
        cluster: this.config.cluster,
      },
      user: {
        uid: 'xiaozhiclaw-user',
      },
      audio: {
        format: 'wav',
        rate: sampleRate,
        language: 'zh-CN',
        bits: 16,
        channel: 1,
      },
    };

    const result = await this.sendRequest('/api/v1/asr', params, audioData);
    return result.result?.text || '';
  }

  /**
   * Text-to-Speech: Convert text to audio (PCM)
   * API: https://www.volcengine.com/docs/6561/142164
   */
  async textToSpeech(text: string, speaker: string = 'zh_female_tianmei_moon_bigtts'): Promise<Buffer> {
    const params = {
      app: {
        appid: this.config.appId,
        cluster: this.config.cluster,
      },
      user: {
        uid: 'xiaozhiclaw-user',
      },
      audio: {
        format: 'wav',
        rate: 24000,
        bits: 16,
        channel: 1,
      },
      request: {
        reqid: this.generateReqId(),
        text: text,
        text_type: 'plain',
        operation: 'query',
        with_frontend: 1,
        frontend_type: 'unitTson',
      },
      tts: {
        voice_type: speaker,
        encoding: 'raw',
        speed_ratio: 1.0,
        volume_ratio: 1.0,
        pitch_ratio: 1.0,
      },
    };

    const result = await this.sendRequest('/api/v1/tts', params);
    return Buffer.from(result.data || '', 'base64');
  }

  private async sendRequest(
    path: string,
    params: any,
    audioData?: Buffer
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      const options = {
        hostname: this.config.apiHost,
        port: 443,
        path: path,
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.config.accessToken}`,
          'Content-Type': 'application/json',
        },
      };

      const req = https.request(options, (res) => {
        let body = '';
        res.on('data', (chunk) => body += chunk);
        res.on('end', () => {
          try {
            const result = JSON.parse(body);
            if (result.code !== 0 && result.code !== undefined) {
              reject(new Error(`Doubao API error: ${result.message || result.code}`));
            } else {
              resolve(result);
            }
          } catch (error) {
            reject(new Error(`Failed to parse response: ${error}`));
          }
        });
      });

      req.on('error', reject);
      req.write(JSON.stringify(params));
      if (audioData) {
        req.write(audioData);
      }
      req.end();
    });
  }

  private generateReqId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

export function createDoubaoService(config?: DoubaoConfig): DoubaoService {
  return new DoubaoService(config);
}
