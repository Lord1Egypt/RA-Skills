/**
 * 测试发布视频功能
 */

import { publishWithVideo } from './src/xhs-tools.js';

async function test() {
  console.log('🧪 测试发布视频功能...\n');

  const result = await publishWithVideo({
    title: "Vlog 日常分享",
    content: "今天去公园散步啦，天气真的超好～\n\n分享一些生活碎片 🌿\n\n#日常 #Vlog #生活记录",
    video: "D:/Videos/daily_vlog.mp4",  // 替换为实际视频路径
    tags: ["日常", "Vlog", "生活记录"]
  });

  console.log('📝 发布结果：');
  console.log(JSON.stringify(result, null, 2));
}

test().catch(console.error);
