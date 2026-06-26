/**
 * 测试发布图文功能
 */

import { publishContent } from './src/xhs-tools.js';

async function test() {
  console.log('🧪 测试发布图文功能...\n');

  const result = await publishContent({
    title: "今日美食分享",
    content: "今天做了一道超好吃的红烧肉，分享给大家～\n\n食材：五花肉 500g、冰糖、生抽、老抽、料酒、葱姜\n\n步骤：\n1. 五花肉切块，冷水下锅焯水\n2. 锅中放油，加冰糖炒糖色\n3. 放入肉块翻炒上色\n4. 加生抽、老抽、料酒调味\n5. 加水没过肉块，小火炖 1 小时\n6. 大火收汁即可\n\n#美食 #红烧肉 #家常菜",
    images: [
      "https://picsum.photos/800/600?random=1",
      "https://picsum.photos/800/600?random=2"
    ],
    tags: ["美食", "红烧肉", "家常菜"]
  });

  console.log('📝 发布结果：');
  console.log(JSON.stringify(result, null, 2));
}

test().catch(console.error);
