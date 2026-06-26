#!/usr/bin/env node

/**
 * video-to-text - 免费视频转文字 API 工具
 * 使用免费的 Whisper API 将视频/音频转为文字
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

// 配置
const CONFIG = {
  // 首选免费 API (MyShell)
  primaryApi: 'https://api.myshell.ai/v1/audio/transcriptions',
  // 备用 API (OpenAI，需要Key时可配置)
  backupApi: 'https://api.openai.com/v1/audio/transcriptions',
  maxFileSize: 25 * 1024 * 1024, // 25MB
};

/**
 * 下载文件到临时目录
 */
async function downloadFile(url) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    
    console.log(`📥 正在下载文件: ${url}`);
    
    protocol.get(url, (response) => {
      // 检查 Content-Length
      const contentLength = parseInt(response.headers['content-length'] || '0', 10);
      if (contentLength > CONFIG.maxFileSize) {
        reject(new Error(`文件太大: ${(contentLength / 1024 / 1024).toFixed(2)}MB，最大支持 ${CONFIG.maxFileSize / 1024 / 1024}MB`));
        return;
      }

      const tmpDir = os.tmpdir();
      const ext = path.extname(url.split('?')[0]) || '.tmp';
      const tempFile = path.join(tmpDir, `video-to-text-${Date.now()}${ext}`);
      const fileStream = fs.createWriteStream(tempFile);

      let downloaded = 0;
      response.on('data', (chunk) => {
        downloaded += chunk.length;
        if (contentLength) {
          const percent = ((downloaded / contentLength) * 100).toFixed(1);
          process.stdout.write(`\r📥 下载进度: ${percent}%`);
        }
      });

      response.pipe(fileStream);

      fileStream.on('finish', () => {
        console.log(`\n✅ 文件已保存到: ${tempFile}`);
        resolve(tempFile);
      });

      fileStream.on('error', (err) => {
        fs.unlink(tempFile, () => {});
        reject(err);
      });
    }).on('error', reject);
  });
}

/**
 * 使用 MyShell API 转写
 */
async function transcribeWithMyShell(filePath, language = 'zh') {
  const boundary = '----FormBoundary' + Date.now();
  
  const filename = path.basename(filePath);
  const fileContent = fs.readFileSync(filePath);

  const header = Buffer.from(
    `--${boundary}\r\n` +
    `Content-Disposition: form-data; name="file"; filename="${filename}"\r\n` +
    `Content-Type: audio/mpeg\r\n\r\n`
  );
  const footer = Buffer.from(`\r\n--${boundary}\r\n--${boundary}--\r\n`);
  
  const languagePart = Buffer.from(
    `--${boundary}\r\n` +
    `Content-Disposition: form-data; name="language"\r\n\r\n` +
    `${language}\r\n`
  );
  
  const modelPart = Buffer.from(
    `--${boundary}\r\n` +
    `Content-Disposition: form-data; name="model"\r\n\r\n` +
    `whisper-1\r\n`
  );

  const body = Buffer.concat([header, fileContent, languagePart, modelPart, footer]);

  return new Promise((resolve, reject) => {
    const url = new URL(CONFIG.primaryApi);
    
    const options = {
      hostname: url.hostname,
      port: url.port || 443,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': body.length,
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.text) {
            resolve(result.text);
          } else if (result.error) {
            reject(new Error(result.error.message || result.error));
          } else {
            reject(new Error(`API返回异常: ${data}`));
          }
        } catch (e) {
          resolve(data); // 有些API直接返回文本
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  
  // 解析参数
  let url = null;
  let language = 'zh';
  let outputFormat = 'text';
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--url' && args[i + 1]) {
      url = args[i + 1];
      i++;
    } else if (args[i] === '--language' && args[i + 1]) {
      language = args[i + 1];
      i++;
    } else if (args[i] === '--format' && args[i + 1]) {
      outputFormat = args[i + 1];
      i++;
    } else if (!url && args[i].startsWith('http')) {
      url = args[i];
    }
  }

  if (!url) {
    console.error('❌ 请提供视频/音频文件的URL');
    console.log('用法: video-to-text <url> [--language zh] [--format text|srt]');
    console.log('示例: video-to-text https://example.com/audio.mp3 --language zh');
    process.exit(1);
  }

  try {
    console.log('🎬 开始视频转文字处理...');
    console.log(`📎 输入文件: ${url}`);
    console.log(`🌐 语言: ${language}`);
    console.log(`📝 输出格式: ${outputFormat}`);
    
    // 下载文件
    const filePath = await downloadFile(url);
    
    // 转写
    console.log('🔄 正在识别语音...');
    const text = await transcribeWithMyShell(filePath, language);
    
    // 清理临时文件
    fs.unlink(filePath, () => {});
    
    // 输出结果
    if (outputFormat === 'srt') {
      // 转换为 SRT 格式
      const srt = convertToSRT(text);
      console.log('\n📄 字幕内容 (SRT格式):\n');
      console.log(srt);
    } else {
      console.log('\n📄 转写结果:\n');
      console.log(text);
    }
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    
    // 如果首选API失败，提示备用方案
    if (error.message.includes('401') || error.message.includes('403')) {
      console.log('\n💡 提示: 主要API可能需要认证，尝试使用备用方案或配置OpenAI API Key');
    }
    process.exit(1);
  }
}

/**
 * 将纯文本转换为 SRT 字幕格式
 */
function convertToSRT(text) {
  // 简单按句分割，每句约10-15字为一条字幕
  const sentences = text.split(/[。！？\n]/).filter(s => s.trim());
  let srtContent = '';
  let startTime = 0;
  
  sentences.forEach((sentence, index) => {
    const trimmed = sentence.trim();
    if (!trimmed) return;
    
    // 每条字幕约3秒（根据字数调整）
    const duration = Math.max(2, Math.ceil(trimmed.length / 5));
    const endTime = startTime + duration;
    
    srtContent += `${index + 1}\n`;
    srtContent += `${formatSRTTime(startTime)} --> ${formatSRTTime(endTime)}\n`;
    srtContent += `${trimmed}\n\n`;
    
    startTime = endTime;
  });
  
  return srtContent;
}

/**
 * 格式化 SRT 时间
 */
function formatSRTTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')},000`;
}

// 导出供外部调用
module.exports = { transcribe: main };

// 直接运行
if (require.main === module) {
  main();
}
