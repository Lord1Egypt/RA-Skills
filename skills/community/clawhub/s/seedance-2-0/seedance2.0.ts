#!/usr/bin/env bun

/**
 * Seedance 2.0 AI视频生成技能
 *
 * 功能：
 * 1. 输出申请开通指南
 * 2. 调用API生成视频
 * 3. 下载生成结果
 */

import { parseArgs } from 'util';
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);

// 加载环境变量
import dotenv from 'dotenv';
dotenv.config({ path: path.join(__dirname, '.env') });

// 默认提示词模板配置
export const PROMPT_TEMPLATES = {
  "promo": "产品宣传促销视频，吸引人的视觉效果，清晰的产品展示，购买呼吁，适合社交媒体分享",
  "event": "活动预告短视频，倒计时展示，活动信息清晰，激发观众兴趣参与，节奏轻快",
  "vlog": "日常生活vlog片段，自然流畅，真实风格，适合竖屏观看",
  "education": "知识科普短视频，清晰讲解，图文并茂，生动有趣，便于理解",
  "marketing": "营销短视频，产品卖点突出，行动召唤明确，高转化率"
};

// 模型配置
export const MODEL_CONFIGS = {
  "pro": "doubao-seedance-2-0-260128",
  "fast": "doubao-seedance-1-0-fast",
  "lite": "doubao-seedance-1-0-lite"
};

export interface SeedanceOptions {
  prompt: string;
  model?: keyof typeof MODEL_CONFIGS;
  duration?: number; // 5, 10, 15 (seconds)
  ratio?: "9:16" | "16:9" | "1:1";
  generateAudio?: boolean;
  watermark?: boolean;
  outputPath?: string;
  referenceImages?: string[];
  referenceVideos?: string[];
  referenceAudios?: string[];
}

export function getApiConfig() {
  const apiKey = process.env.ARK_API_KEY;
  // ARK endpoint for Seedance
  const baseUrl = process.env.ARK_BASE_URL || "https://ark.cn-beijing.volces.com/api/v3";

  if (!apiKey) {
    throw new Error("ARK_API_KEY environment variable is required");
  }

  return { apiKey, baseUrl };
}

export function getModelId(model: keyof typeof MODEL_CONFIGS): string {
  return MODEL_CONFIGS[model] || MODEL_CONFIGS.pro;
}

export function getPromptFromTemplate(templateName: string, customPrompt?: string): string {
  const basePrompt = PROMPT_TEMPLATES[templateName as keyof typeof PROMPT_TEMPLATES] || "";
  if (customPrompt) {
    return `${basePrompt} ${customPrompt}`;
  }
  return basePrompt;
}

export async function generateVideo(options: SeedanceOptions): Promise<string> {
  const { apiKey, baseUrl } = getApiConfig();
  const modelId = getModelId(options.model || "pro");

  const ratio = options.ratio || "9:16";
  const duration = options.duration || 5;
  const generateAudio = options.generateAudio !== undefined ? options.generateAudio : true;
  const watermark = options.watermark !== undefined ? options.watermark : false;

  // Build content array
  const content = [
    {
      type: "text",
      text: options.prompt
    }
  ];

  // Add reference images if provided
  if (options.referenceImages && options.referenceImages.length > 0) {
    for (const url of options.referenceImages) {
      content.push({
        type: "image_url",
        image_url: { url },
        role: "reference_image"
      });
    }
  }

  // Add reference videos if provided
  if (options.referenceVideos && options.referenceVideos.length > 0) {
    for (const url of options.referenceVideos) {
      content.push({
        type: "video_url",
        video_url: { url },
        role: "reference_video"
      });
    }
  }

  // Add reference audios if provided
  if (options.referenceAudios && options.referenceAudios.length > 0) {
    for (const url of options.referenceAudios) {
      content.push({
        type: "audio_url",
        audio_url: { url },
        role: "reference_audio"
      });
    }
  }

  const requestBody = {
    model: modelId,
    content: content,
    generate_audio: generateAudio,
    ratio: ratio,
    duration: duration,
    watermark: watermark
  };

  console.log("Starting video generation with parameters:");
  console.log(JSON.stringify(requestBody, null, 2));

  const endpoint = `${baseUrl}/contents/generations/tasks`;
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`
    },
    body: JSON.stringify(requestBody)
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`API request failed: ${response.status} - ${error}`);
  }

  const data = await response.json();
  const taskId = data.id;

  console.log(`Generation started: ${taskId}`);
  console.log("Waiting for completion...");

  // Poll for completion
  let result = null;
  for (let i = 0; i < 60; i++) { // 最长等待10分钟
    await new Promise(resolve => setTimeout(resolve, 10000)); // 每10秒检查一次

    const statusResponse = await fetch(`${baseUrl}/contents/generations/tasks/${taskId}`, {
      headers: {
        "Authorization": `Bearer ${apiKey}`
      }
    });

    if (!statusResponse.ok) {
      console.warn(`Status check failed: ${statusResponse.status}, retrying...`);
      continue;
    }

    const statusData = await statusResponse.json();

    if (statusData.status === "completed") {
      result = statusData;
      break;
    } else if (statusData.status === "failed") {
      throw new Error(`Generation failed: ${statusData.error || "unknown error"}`);
    } else {
      console.log(`Current status: ${statusData.status}, continuing to wait...`);
    }
  }

  if (!result) {
    throw new Error("Generation timed out after 10 minutes");
  }

  const videoUrl = result.content[0].video_url;
  console.log(`Generation completed! Video URL: ${videoUrl}`);

  // Download the video if output path is specified
  if (options.outputPath) {
    console.log(`Downloading video to ${options.outputPath}...`);
    const videoResponse = await fetch(videoUrl);
    if (!videoResponse.ok) {
      throw new Error(`Failed to download video: ${videoResponse.status}`);
    }
    const videoBuffer = Buffer.from(await videoResponse.arrayBuffer());
    fs.writeFileSync(options.outputPath, videoBuffer);
    console.log(`Video saved to: ${options.outputPath}`);
  }

  return videoUrl;
}

// 输出申请指南
export function printApplicationGuide() {
  console.log(`
=============================================
 Seedance 2.0 企业用户邀测 & 高级功能开白申请指南
=============================================

前置条件：
  • 需要企业实名认证（未实名无法申请）
  • 需要通过合作伙伴邀请链接关联

申请步骤：
  1. 通过邀请链接注册/登录火山引擎合作伙伴平台
  2. 提交申请后，请提供：公司名称 + 客户账号ID 给渠道联系人
  3. 渠道联系人协助内部申请开白
  4. 留资通过后，在官网签署协议并下单购买
  5. 开通完成后即可使用API

邀请链接：
https://partner.volcengine.com/partners/auth/confirm?inviteToken=Z804VS6L0OUHUALB0UA450PEUPSJ4TYN4LA4JPO6F652OBSUUKI94FYKM5FL5YC2&partnerType=101&partnerName=%E6%99%BA%E7%BB%B4%E7%95%8C%EF%BC%88%E6%88%90%E9%83%BD%EF%BC%89%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&InvitationSource=1&ActivityCode=Seedance2.0

手机扫码快速申请：
  二维码文件：${__dirname}/qrcode.png

权益差异：
  • 普通用户：基本功能可用，低优排队，默认并发限制
  • 保底客户：高优排队，可提升并发，支持自定义人像库、真人人像、版权IP等高级功能

申请高级功能：
  • 完成基础申请后，联系渠道联系人核对权益
  • 签署合约盖章，走内部流程
  • 开通高阶客户转售售后群

合规审核禁止内容：
  • 涉黄、涉恐、涉敏
  • 侵权版权IP、公众人物、版权音乐
  • 未开白真人人脸

文档链接：
https://fcndvyb6ssj0.feishu.cn/wiki/Y5gMwATc1i6A3BkpDGZc84axn4b

=============================================
  `);
}

// CLI main
async function main() {
  const { values } = parseArgs({
    args: Bun.argv,
    options: {
      'guide': { type: 'boolean', short: 'g' },
      'prompt': { type: 'string', short: 'p' },
      'model': { type: 'string', short: 'm', default: 'pro' },
      'duration': { type: 'string', short: 'd', default: '5' },
      'ratio': { type: 'string', short: 'r', default: '9:16' },
      'no-audio': { type: 'boolean' },
      'watermark': { type: 'boolean' },
      'template': { type: 'string', short: 't' },
      'output': { type: 'string', short: 'o' },
      'ref-image': { type: 'string', multiple: true },
      'ref-video': { type: 'string', multiple: true },
      'ref-audio': { type: 'string', multiple: true },
    },
    allowPositionals: true
  });

  if (values.guide) {
    printApplicationGuide();
    process.exit(0);
  }

  if (!values.prompt && !values.template) {
    console.error("Error: either --prompt or --template is required");
    console.log("Usage:");
    console.log("  bun run seedance2.0.ts --guide                # Show application guide");
    console.log("  bun run seedance2.0.ts --prompt \"...\"          # Generate video with custom prompt");
    console.log("  bun run seedance2.0.ts --template promo        # Use template prompt");
    console.log("  bun run seedance2.0.ts --prompt \"...\" --ref-image https://... # With reference image");
    console.log("  bun run seedance2.0.ts --prompt \"...\" --duration 11 --ratio 16:9 # Custom duration");
    process.exit(1);
  }

  let prompt = values.prompt || "";
  if (values.template && PROMPT_TEMPLATES[values.template as keyof typeof PROMPT_TEMPLATES]) {
    prompt = getPromptFromTemplate(values.template, prompt);
  }

  const options: SeedanceOptions = {
    prompt,
    model: (values.model as any) || "pro",
    duration: parseInt(values.duration || "5"),
    ratio: (values.ratio as any) || "9:16",
    generateAudio: !values['no-audio'],
    watermark: values.watermark || false,
    outputPath: values.output || `seedance-${Date.now()}.mp4`,
    referenceImages: values['ref-image'] || [],
    referenceVideos: values['ref-video'] || [],
    referenceAudios: values['ref-audio'] || [],
  };

  try {
    const videoUrl = await generateVideo(options);
    console.log("\n✅ Generation completed successfully!");
    console.log(`Video URL: ${videoUrl}`);
    if (options.outputPath) {
      console.log(`File saved to: ${options.outputPath}`);
    }
  } catch (error) {
    console.error("❌ Error:", (error as Error).message);
    process.exit(1);
  }
}

// Run if called directly
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
if (process.argv[1] === __filename) {
  main();
}
