#!/usr/bin/env node
/**
 * CLI 脚本: 发布微信公众号文章
 */

import { createWeChatMPClient } from '../index';

async function main() {
  const args = process.argv.slice(2);
  
  // 解析参数
  const params: any = {};
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace(/^--/, '');
    const value = args[i + 1];
    if (key && value !== undefined) {
      params[key] = value;
    }
  }

  // 检查必需参数
  if (!params.title || !params.content || !params.cover) {
    console.log('用法: node publish.js --title "文章标题" --content "正文内容" --cover "封面图路径" [--author "作者"] [--publish]');
    process.exit(1);
  }

  try {
    const client = createWeChatMPClient();
    
    console.log('📤 正在上传封面图片...');
    const coverMediaId = await client.media.uploadCoverImage(params.cover);
    console.log(`✅ 封面上传成功: ${coverMediaId}`);

    console.log('\n📝 正在创建文章...');
    const options = {
      title: params.title,
      content: params.content,
      coverMediaId: coverMediaId,
      author: params.author || client.config.default_author,
      showCoverPic: true
    };

    if (params.publish) {
      const result = await client.article.publishArticle(options);
      console.log('✅ 文章创建成功并提交发布！');
      console.log(`📄 Media ID: ${result.mediaId}`);
      console.log(`🚀 Publish ID: ${result.publishId}`);
    } else {
      const mediaId = await client.article.createSingleDraft(options);
      console.log('✅ 草稿创建成功！');
      console.log(`📄 Media ID: ${mediaId}`);
    }
  } catch (error: any) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

main();
