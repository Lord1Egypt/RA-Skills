// QQ Bot 语音识别集成示例
// 将此代码添加到 gateway.ts 的附件处理逻辑中

import * as fs from 'fs';
import { exec } from 'node:child_process';
import * as os from 'node:os';

/**
 * 处理 QQ 语音消息
 * @param localPath - 语音文件本地路径 (.amr)
 * @returns Promise<string | null> - 识别的文字或 null
 */
async function processQQVoice(localPath: string): Promise<string | null> {
  const log = console; // 替换为实际日志对象
  
  try {
    log.info(`🎤 开始处理 QQ 语音：${localPath}`);
    
    // 1. 去掉第一个字节 (0x02)
    const data = fs.readFileSync(localPath);
    const fixedPath = localPath + '.fixed';
    fs.writeFileSync(fixedPath, data.slice(1));
    log.info(`✅ 已去掉文件头`);
    
    // 2. silk-v3-decoder 解码
    const decoderPath = process.env.SILK_DECODER_PATH || '/tmp/silk-v3-decoder';
    const outputMp3 = localPath + '.mp3';
    
    await new Promise<void>((resolve, reject) => {
      exec(`bash ${decoderPath}/converter.sh ${fixedPath} mp3`, (err, stdout, stderr) => {
        if (err) {
          log.error(`❌ 解码失败：${stderr}`);
          reject(err);
        } else {
          log.info(`✅ 解码完成`);
          resolve();
        }
      });
    });
    
    // 3. Whisper 识别文字
    const model = process.env.WHISPER_MODEL || 'base';
    const language = process.env.WHISPER_LANGUAGE || 'zh';
    
    const transcript = await new Promise<string>((resolve, reject) => {
      exec(
        `whisper --model ${model} --language ${language} ${outputMp3} --output_dir ${os.tmpdir()} --verbose False`,
        (err, stdout, stderr) => {
          if (err) {
            log.error(`❌ 识别失败：${stderr}`);
            reject(err);
          } else {
            const txtPath = outputMp3 + '.txt';
            fs.readFile(txtPath, 'utf-8', (err, data) => {
              if (err) reject(err);
              else resolve(data.trim());
            });
          }
        }
      );
    });
    
    // 4. 清理临时文件
    try {
      fs.unlinkSync(fixedPath);
      fs.unlinkSync(outputMp3);
      fs.unlinkSync(outputMp3 + '.txt');
    } catch (e) {
      log.warn(`⚠️ 清理临时文件失败：${e}`);
    }
    
    log.info(`✅ 语音识别完成：${transcript}`);
    return transcript;
    
  } catch (err: any) {
    log.error(`❌ 语音处理失败：${err.message}`);
    return null;
  }
}

/**
 * 在 gateway.ts 中的使用示例
 * 
 * 找到附件处理部分，添加：
 */
/*
if (event.attachments?.length) {
  const audioTranscripts: string[] = [];
  
  for (const att of event.attachments) {
    const localPath = await downloadFile(att.url, downloadDir, att.filename);
    
    if (localPath) {
      if (att.content_type?.startsWith("image/")) {
        // 图片处理逻辑...
      } else if (localPath.endsWith(".amr")) {
        // ============ QQ 语音处理 ============
        const transcript = await processQQVoice(localPath);
        
        if (transcript) {
          audioTranscripts.push(`\n🎤 **语音消息**：${transcript}\n`);
        }
      } else {
        // 其他附件...
      }
    }
  }
  
  // 组合附件信息
  if (audioTranscripts.length > 0) {
    attachmentInfo += "\n" + audioTranscripts.join("\n");
  }
}
*/

export { processQQVoice };
