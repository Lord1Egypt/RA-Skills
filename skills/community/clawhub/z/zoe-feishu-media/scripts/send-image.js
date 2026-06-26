import { uploadImageFeishu, sendImageFeishu } from "../../../feishu/src/media.js";

/**
 * @param {object} params
 * @param {string} params.imagePath - 本地图片路径
 * @param {string} params.chatId - 飞书群ID或个人ID
 * @param {object} params.cfg - OpenClaw配置
 */
export async function sendImageToFeishu({ imagePath, chatId, cfg }) {
  // 1. 上传图片到飞书
  const { imageKey } = await uploadImageFeishu({
    cfg,
    image: imagePath,
    imageType: "message",
  });

  // 2. 发送图片
  const result = await sendImageFeishu({
    cfg,
    to: chatId,
    imageKey,
  });

  return result;
}
