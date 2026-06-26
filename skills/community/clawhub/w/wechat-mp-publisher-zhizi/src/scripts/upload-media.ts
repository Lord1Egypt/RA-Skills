#!/usr/bin/env node
/**
 * CLI 脚本: 上传素材到微信服务器
 */

import { createWeChatMPClient, MediaType } from '../index';

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
  if (!params.file) {
    console.log('用法: node upload-media.js --file "文件路径" [--type image|thumb|voice|video]');
    process.exit(1);
  }

  try {
    const client = createWeChatMPClient();
    
    const type: MediaType = params.type || 'image';
    console.log(`📤 正在上传素材 (${type})...`);
    
    const result = await client.media.uploadMedia(params.file, type);
    
    console.log('✅ 上传成功！');
    console.log(`📄 Media ID: ${result.media_id}`);
    console.log(`📊 Type: ${result.type}`);
    console.log(`🕐 Created At: ${new Date(result.created_at * 1000).toLocaleString()}`);
  } catch (error: any) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

main();
