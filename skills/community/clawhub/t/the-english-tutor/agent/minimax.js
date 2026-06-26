/**
 * MiniMax API · TTS 语音合成 + Token Plan 检查
 * TTS文档: https://platform.minimaxi.com/docs/api-reference/speech-t2a-http
 */

const crypto = require('crypto');
const fs = require('fs');
const https = require('https');
const os = require('os');
const path = require('path');

// ===== Token Plan 剩余次数查询 =====
// 返回 { remain: number } — remain=0 表示本区间额度用完
async function checkTokenPlanRemain(apiKey) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'www.minimaxi.com',
      path: '/v1/token_plan/remains',
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
    };
    const req = https.request(options, (res) => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        try {
          const data = JSON.parse(Buffer.concat(chunks).toString());
          const models = data.model_remains || [];

          // speech-2.8-hd 的区间限额 4000次，优先级最高
          const speechModel = models.find(m => m.model_name === 'speech-hd');
          if (speechModel) {
            const used = speechModel.current_interval_usage_count || 0;
            const total = speechModel.current_interval_total_count || 0;
            const remain = Math.max(0, total - used);
            resolve({ remain });
            return;
          }

          // fallback: 取任意模型首个
          const first = models[0];
          if (first) {
            const used = first.current_interval_usage_count || 0;
            const total = first.current_interval_total_count || 0;
            resolve({ remain: Math.max(0, total - used) });
          } else {
            resolve({ remain: 0 });
          }
        } catch (e) {
          reject(e);
        }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

// ===== TTS =====
class MinimaxTTS {
  constructor(config) {
    const { MINIMAX_API_KEY: apiKey, TTS_MODEL: model, TTS_SPEED: speed, TTS_VOICE_ID: voiceId } = config;
    this.apiKey = apiKey;
    // 有 API Key 时使用推荐值；无 Key 时静默跳过（synthesize 会抛错）
    this.model = model || (apiKey ? 'speech-2.8-hd' : null);
    this.speed = speed;
    this.voiceId = voiceId || (apiKey ? 'male-qn-qingse' : null);
  }

  /**
   * 检查剩余次数，不足则抛异常
   */
  async _checkQuota() {
    try {
      const { remain } = await checkTokenPlanRemain(this.apiKey);
      if (remain <= 0) {
        throw new Error('TOKEN_EXHAUSTED');
      }
      return remain;
    } catch (e) {
      if (e.message === 'TOKEN_EXHAUSTED') throw e;
      console.warn('[TTS] 额度查询失败，继续尝试:', e.message);
    }
  }

  /**
   * 同步 TTS 合成
   * @param {string} text - 要合成的文本
   * @returns {Promise<{url: string, localPath: string}>}
   */
  async synthesize(text) {
    // 无 API Key：静默跳过
    if (!this.apiKey) {
      throw new Error('MINIMAX_API_KEY_NOT_CONFIGURED');
    }
    await this._checkQuota(); // 先检查余量

    const payload = {
      model: this.model,
      text,
      stream: false,
      voice_setting: {
        voice_id: this.voiceId,
        speed: this.speed,
        vol: 1,
        pitch: 0,
      },
      audio_setting: {
        sample_rate: 32000,
        bitrate: 128000,
        format: 'mp3',
        channel: 1,
      },
    };

    const result = await this._request('/v1/t2a_v2', payload);
    return this._parseResponse(result, text);
  }

  async _request(path, payload) {
    return new Promise((resolve, reject) => {
      const body = JSON.stringify(payload);
      const options = {
        hostname: 'api.minimaxi.com',
        path,
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body),
        },
      };

      const req = https.request(options, (res) => {
        const chunks = [];
        res.on('data', c => chunks.push(c));
        res.on('end', () => resolve(Buffer.concat(chunks).toString()));
      });
      req.on('error', reject);
      req.write(body);
      req.end();
    });
  }

  _parseResponse(raw, text) {
    try {
      const data = JSON.parse(raw);
      if (data.base_resp?.status_code !== 0) {
        throw new Error(`TTS API error [${data.base_resp?.status_code}]: ${data.base_resp?.status_msg}`);
      }
      const hexAudio = data.data?.audio;
      if (!hexAudio) return { url: '', localPath: '' };

      const buf = Buffer.from(hexAudio, 'hex');
      const hash = crypto.createHash('sha256').update(text).digest('hex').slice(0, 8);
      const tmpPath = path.join(os.tmpdir(), `tts_${Date.now()}_${hash}.mp3`);
      fs.writeFileSync(tmpPath, buf);
      return { url: `file://${tmpPath}`, localPath: tmpPath };
    } catch (e) {
      console.error('[TTS] 解析失败:', e.message, '| raw:', raw.slice(0, 200));
      throw e; // 重新抛出，让 synthesize() 的调用方能捕获配额错误
    }
  }
}

// ===== Chat (Anthropic 兼容) =====
class MiniMaxAPI {
  constructor(config) {
    this.apiKey = config.MINIMAX_API_KEY;
    this.model = config.LLM_MODEL || 'MiniMax-M2.7';
  }

  async chat(systemPrompt, messages, temperature = 0.65) {
    if (!this.apiKey) {
      throw new Error('MINIMAX_API_KEY_NOT_CONFIGURED');
    }
    return new Promise((resolve, reject) => {
      const body = JSON.stringify({
        model: this.model,
        max_tokens: 512,
        temperature,
        system: systemPrompt,
        messages,
      });

      const options = {
        hostname: 'api.minimaxi.com',
        path: '/v1/text/chatcompletion_v2',
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body),
        },
      };

      const req = https.request(options, (res) => {
        const chunks = [];
        res.on('data', c => chunks.push(c));
        res.on('end', () => {
          try {
            const data = JSON.parse(Buffer.concat(chunks).toString());
            resolve(data.choices?.[0]?.text || data.choices?.[0]?.message?.content || '');
          } catch (e) {
            reject(e);
          }
        });
      });
      req.on('error', reject);
      req.write(body);
      req.end();
    });
  }
}

module.exports = { MinimaxTTS, MiniMaxAPI, checkTokenPlanRemain };
