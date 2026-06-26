/**
 * 讯飞 TTS 核心模块
 */
const crypto = require('crypto');
const fs = require('fs');
const ws = require('ws');
const config = require('./tts-config');

class XunfeiTTS {
  constructor(options = {}) {
    this.appId = options.appId || config.xunfei.appId;
    this.apiKey = options.apiKey || config.xunfei.apiKey;
    this.apiSecret = options.apiSecret || config.xunfei.apiSecret;
    this.voice = options.voice || config.xunfei.defaultVoice;
    this.timeout = options.timeout || config.xunfei.timeout;
    this.audioConfig = config.xunfei.audio;
  }

  async synthesize(text, outputPath) {
    return new Promise((resolve, reject) => {
      const timeoutId = setTimeout(() => {
        this.wsClient?.close();
        reject(new Error('TTS timeout'));
      }, this.timeout);

      const host = config.xunfei.host;
      const path = config.xunfei.path;
      const dateStr = new Date().toUTCString();

      const signatureOrigin = `host: ${host}\ndate: ${dateStr}\nGET ${path} HTTP/1.1`;
      const signature = crypto.createHmac('sha256', this.apiSecret)
        .update(signatureOrigin, 'utf8')
        .digest('base64');

      const authorizationOrigin = `api_key="${this.apiKey}", algorithm="hmac-sha256", headers="host date request-line", signature="${signature}"`;
      const authorization = Buffer.from(authorizationOrigin, 'utf8').toString('base64');

      const wsUrl = `wss://${host}${path}?authorization=${encodeURIComponent(authorization)}&date=${encodeURIComponent(dateStr)}&host=${host}`;

      this.wsClient = new ws.WebSocket(wsUrl, {
        headers: { 'Sec-WebSocket-Protocol': 'chat' }
      });

      const audioBuffer = [];

      this.wsClient.on('open', () => {
        this.wsClient.send(JSON.stringify({
          common: { app_id: this.appId },
          business: {
            aue: this.audioConfig.aue,
            auf: this.audioConfig.auf,
            vcn: this.voice,
            tte: this.audioConfig.tte
          },
          data: {
            text: Buffer.from(text).toString('base64'),
            status: 2
          }
        }));
      });

      this.wsClient.on('message', (data) => {
        const res = JSON.parse(data.toString());

        if (res.code !== 0) {
          clearTimeout(timeoutId);
          this.wsClient.close();
          reject(new Error(`TTS error: ${res.desc || res.message}`));
          return;
        }

        if (res.data?.audio) {
          audioBuffer.push(Buffer.from(res.data.audio, 'base64'));
        }

        if (res.data?.status === 2) {
          clearTimeout(timeoutId);
          const pcmAudio = Buffer.concat(audioBuffer);

          if (outputPath) {
            const pcmPath = outputPath.replace(/\.(mp3|opus)$/, '.pcm');
            fs.writeFileSync(pcmPath, pcmAudio);

            const { execSync } = require('child_process');

            if (outputPath.endsWith('.mp3')) {
              execSync(`ffmpeg -y -f s16le -ar 16000 -ac 1 -i ${pcmPath} -ar ${this.audioConfig.outputSampleRate} -ac 1 ${outputPath} 2>/dev/null`);
            } else if (outputPath.endsWith('.opus')) {
              execSync(`ffmpeg -y -f s16le -ar 16000 -ac 1 -i ${pcmPath} -c:a libopus -b:a ${this.audioConfig.outputBitrate} -ar ${this.audioConfig.outputSampleRate} -ac 1 ${outputPath} 2>/dev/null`);
            }

            fs.unlinkSync(pcmPath);
          }

          this.wsClient.close();
          resolve(pcmAudio);
        }
      });

      this.wsClient.on('error', (err) => {
        clearTimeout(timeoutId);
        this.wsClient?.close();
        reject(err);
      });
    });
  }
}

module.exports = { XunfeiTTS, config };
