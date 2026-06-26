import fs from 'fs';
import path from 'path';
import { createWorker } from 'tesseract.js';
import ort from 'onnxruntime-node';
import axios from 'axios';

// 读取配置
const config = JSON.parse(fs.readFileSync('./config.json', 'utf8'));

/* ---------- OCR ---------- */
async function ocrImage(imagePath) {
  const worker = await createWorker({
    logger: () => {}
  });
  await worker.load();
  await worker.loadLanguage(config.tesseractLang);
  await worker.initialize(config.tesseractLang);
  const { data: { text } } = await worker.recognize(imagePath);
  await worker.terminate();
  return text.trim();
}

/* ---------- YOLO 检测 ---------- */
async function detectObjects(imagePath) {
  const session = await ort.InferenceSession.create(config.yoloModelPath);
  const imageBuffer = fs.readFileSync(imagePath);
  const tensor = ort.Tensor.fromImage(imageBuffer, { channels: 3, mean: [0,0,0], std: [255,255,255] });
  const feeds = { images: tensor };
  const results = await session.run(feeds);
  // 简单返回占位结果（实际项目请做 NMS、类别映射）
  const dummy = results['output0'].data.slice(0, 5);
  return dummy.map((v, i) => `对象${i + 1}`);
}

/* ---------- 翻译（Google 免费网页） ---------- */
async function translateIfEnglish(text) {
  const isEnglish = /^[\x00-\x7F]*$/.test(text);
  if (!isEnglish) return text;
  const resp = await axios.get('https://translate.googleapis.com/translate_a/single', {
    params: {
      client: 'gtx',
      sl: 'en',
      tl: 'zh-CN',
      dt: 't',
      q: text
    }
  });
  return resp.data[0].map(item => item[0]).join('');
}

/* ---------- 主入口 ---------- */
export async function run(context) {
  const { imagePath, source, feishu } = context;
  if (!fs.existsSync(imagePath)) throw new Error(`图片不存在：${imagePath}`);

  const rawText = await ocrImage(imagePath);
  const translated = await translateIfEnglish(rawText);
  const objects = await detectObjects(imagePath);

  const result = [
    '--- 图片识别结果 ---',
    `📝 文字识别：\n${translated}`,
    `🔎 物体/场景检测：\n${objects.join(', ')}`,
    '--- End ---'
  ].join('\n\n');

  if (source?.startsWith('feishu')) {
    const { client } = feishu;
    if (source === 'feishu-msg') {
      await client.message.update({ message_id: feishu.messageId, text: result });
    } else if (source === 'feishu-doc') {
      await client.doc.edit({ doc_token: feishu.docToken, content: `\n${result}` });
    }
  } else {
    const outPath = `${imagePath}.txt`;
    fs.writeFileSync(outPath, result, 'utf8');
    return { outPath };
  }

  return { result };
}
