#!/bin/bash
# Lovart 图片下载器（绕过 SSL 问题）
# 用法：./download_image.sh <IMAGE_URL> <OUTPUT_PATH>
#
# ⚠️ Lovart 的 a.lovart.ai 域名 SSL 证书与 curl/Python 不兼容
# 必须用 Node.js 下载

if [ $# -lt 2 ]; then
    echo "用法: ./download_image.sh <IMAGE_URL> <OUTPUT_PATH>"
    echo ""
    echo "示例:"
    echo "  ./download_image.sh 'https://a.lovart.ai/artifacts/agent/xxx.png' ./output/cover.png"
    echo ""
    echo "💡 提示: URL 中去掉 ?x-oss-process=... 参数可获取原始高质量图片"
    exit 1
fi

URL="$1"
OUTPUT="$2"

# 去掉 OSS 处理参数（获取原图）
CLEAN_URL=$(echo "$URL" | sed 's/\?x-oss-process=.*//')

echo "📥 下载图片..."
echo "   URL: $CLEAN_URL"
echo "   输出: $OUTPUT"

# 确保输出目录存在
mkdir -p "$(dirname "$OUTPUT")"

NODE_TLS_REJECT_UNAUTHORIZED=0 node -e "
const https = require('https');
const http = require('http');
const fs = require('fs');
const url = '$CLEAN_URL';
const mod = url.startsWith('https') ? https : http;
mod.get(url, {rejectUnauthorized: false}, res => {
  if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
    console.log('↪️  重定向到:', res.headers.location);
    return;
  }
  const chunks = [];
  res.on('data', c => chunks.push(c));
  res.on('end', () => {
    const buf = Buffer.concat(chunks);
    fs.writeFileSync('$OUTPUT', buf);
    console.log('✅ 下载完成:', (buf.length / 1024).toFixed(1), 'KB');
  });
}).on('error', e => {
  console.error('❌ Node.js 下载失败:', e.message);
  console.error('');
  console.error('💡 如果所有本地 SSL 客户端都失败（EPROTO / tlsv1 alert / WRONG_VERSION_NUMBER），');
  console.error('   请使用浏览器内 fetch + base64 分块提取方案（方法 C）。');
  console.error('   详见 references/lovart-operation.md 的 Phase 4 方法 C。');
  process.exit(1);
});
"
