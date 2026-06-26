/**
 * QQ Bot Gateway 语音识别集成示例 v2.0
 * 
 * 此示例展示如何在 gateway.ts 中集成语音自动识别功能
 * 版本：2.0.0
 * 日期：2026-03-01
 */

import * as fs from 'node:fs';
import * as path from 'node:path';
import { exec } from 'node:child_process';
import { promisify } from 'node:util';

const execPromise = promisify(exec);

/**
 * 处理 QQ 语音消息
 * @param localPath 语音文件本地路径 (.amr)
 * @param downloadDir 下载目录
 * @param log 日志对象
 */
async function processQQVoice(
  localPath: string,
  downloadDir: string,
  log?: { info: (msg: string) => void; error: (msg: string) => void }
): Promise<string | null> {
  const ext = path.extname(localPath).toLowerCase();
  
  // 检查是否为语音文件
  if (ext !== '.amr' && ext !== '.silk') {
    return null;
  }
  
  log?.info(`🎤 检测到语音消息：${localPath}`);
  
  try {
    // 1. 去掉第一个字节 (0x02)
    const data = fs.readFileSync(localPath);
    const fixedPath = localPath + ".fixed";
    fs.writeFileSync(fixedPath, data.slice(1));
    
    // 2. silk-v3-decoder 解码为 PCM
    const decoderPath = "/tmp/silk-v3-decoder";
    const pcmPath = localPath + ".pcm";
    
    await execPromise(`${decoderPath}/silk/decoder ${fixedPath} ${pcmPath}`);
    
    // 3. PCM 转 WAV (16kHz)
    const wavPath = localPath + ".wav";
    await execPromise(
      `ffmpeg -y -f s16le -ar 24000 -ac 1 -i ${pcmPath} -ar 16000 ${wavPath} 2>/dev/null`
    );
    
    // 4. Whisper 识别 (medium 模型)
    log?.info(`🤖 正在识别语音...`);
    await execPromise(
      `whisper --model medium --language zh ${wavPath} --output_dir ${downloadDir} --verbose False`
    );
    
    // 5. 读取识别结果（检查多个可能的路径）
    let transcript = "";
    const possibleTxtPaths = [
      localPath + ".txt",         // .amr.txt ✅ (Whisper 实际输出)
      wavPath + ".txt",           // .wav.txt
      downloadDir + "/" + path.basename(localPath) + ".txt"
    ];
    
    for (const txtPath of possibleTxtPaths) {
      if (fs.existsSync(txtPath)) {
        transcript = fs.readFileSync(txtPath, 'utf-8').trim();
        log?.info(`📝 读取识别结果：${txtPath}`);
        break;
      }
    }
    
    // 6. 返回识别结果（带确认提示）
    if (transcript) {
      log?.info(`✅ 识别成功：${transcript}`);
      return transcript;
    } else {
      log?.error(`❌ 识别结果为空`);
      return null;
    }
    
  } catch (err: any) {
    log?.error(`❌ 语音处理失败：${err.message}`);
    throw err;
  } finally {
    // 7. 清理临时文件
    try {
      const fixedPath = localPath + ".fixed";
      const pcmPath = localPath + ".pcm";
      const wavPath = localPath + ".wav";
      const txtPath = localPath + ".txt";
      
      [fixedPath, pcmPath, wavPath, txtPath].forEach(p => {
        if (fs.existsSync(p)) fs.unlinkSync(p);
      });
    } catch (e) {}
  }
}

/**
 * 在 gateway.ts 中的使用示例
 */
async function integrateInGateway() {
  // 模拟 gateway.ts 中的附件处理循环
  const attachments = [
    {
      url: "https://example.com/voice.amr",
      filename: "voice.amr",
      content_type: "audio/amr"
    }
  ];
  
  const downloadDir = "/root/clawd/downloads";
  const audioTranscripts: string[] = [];
  
  for (const att of attachments) {
    // 下载文件（示例中跳过）
    const localPath = `${downloadDir}/${att.filename}`;
    
    // 处理语音消息
    const ext = path.extname(localPath).toLowerCase();
    const mimeType = att.content_type?.toLowerCase() || '';
    
    if (ext === '.amr' || mimeType.includes('amr')) {
      const transcript = await processQQVoice(localPath, downloadDir, {
        info: (msg) => console.log(`[INFO] ${msg}`),
        error: (msg) => console.error(`[ERROR] ${msg}`)
      });
      
      if (transcript) {
        // 添加到消息内容（带确认提示）
        audioTranscripts.push(
          `\n\n🎤 **语音消息识别结果**：${transcript}\n\n_请确认是否正确，我将按此执行_`
        );
      }
    }
  }
  
  // 输出结果
  console.log("\n=== 识别结果 ===");
  console.log(audioTranscripts.join("\n"));
}

// 运行示例
if (require.main === module) {
  integrateInGateway().catch(console.error);
}

export { processQQVoice };
