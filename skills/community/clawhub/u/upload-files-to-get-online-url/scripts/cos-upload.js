#!/usr/bin/env node
/**
 * 腾讯云 COS 文件上传脚本
 * Usage: node cos-upload.js <file-path> [options]
 */

const COS = require('cos-nodejs-sdk-v5');
const fs = require('fs');
const path = require('path');

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const filePath = args[0];
  
  const options = {
    secretId: process.env.TENCENT_SECRET_ID,
    secretKey: process.env.TENCENT_SECRET_KEY,
    bucket: process.env.TENCENT_COS_BUCKET,
    region: process.env.TENCENT_COS_REGION,
    cosPath: process.env.TENCENT_COS_PATH || 'uploads/'
  };

  // 解析可选参数
  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--secret-id' && args[i + 1]) options.secretId = args[++i];
    else if (arg === '--secret-key' && args[i + 1]) options.secretKey = args[++i];
    else if (arg === '--bucket' && args[i + 1]) options.bucket = args[++i];
    else if (arg === '--region' && args[i + 1]) options.region = args[++i];
    else if (arg === '--path' && args[i + 1]) options.cosPath = args[++i];
  }

  return { filePath, options };
}

// 验证配置
function validateConfig(options) {
  const required = ['secretId', 'secretKey', 'bucket', 'region'];
  const missing = required.filter(key => !options[key]);
  
  if (missing.length > 0) {
    console.error('❌ 缺少必需的配置项:', missing.join(', '));
    console.error('\\n请通过以下方式之一提供配置:');
    console.error('1. 环境变量: TENCENT_SECRET_ID, TENCENT_SECRET_KEY, TENCENT_COS_BUCKET, TENCENT_COS_REGION');
    console.error('2. 命令行参数: --secret-id, --secret-key, --bucket, --region');
    process.exit(1);
  }
}

// 主函数
async function uploadToCOS(filePath, options) {
  // 检查文件
  if (!filePath) {
    console.error('❌ 请提供要上传的文件路径');
    console.error('Usage: node cos-upload.js <file-path> [options]');
    process.exit(1);
  }

  if (!fs.existsSync(filePath)) {
    console.error(`❌ 文件不存在: ${filePath}`);
    process.exit(1);
  }

  // 验证配置
  validateConfig(options);

  // 确保路径以/结尾
  if (!options.cosPath.endsWith('/')) {
    options.cosPath += '/';
  }

  // 初始化 COS
  const cos = new COS({
    SecretId: options.secretId,
    SecretKey: options.secretKey
  });

  // 生成文件名
  const ext = path.extname(filePath);
  const timestamp = Date.now();
  const randomStr = Math.random().toString(36).substring(2, 8);
  const fileName = `upload_${timestamp}_${randomStr}${ext}`;
  const cosKey = options.cosPath + fileName;

  console.log('📤 开始上传...');
  console.log(`文件: ${path.basename(filePath)}`);
  console.log(`大小: ${(fs.statSync(filePath).size / 1024).toFixed(2)} KB`);
  console.log(`目标: ${cosKey}`);

  try {
    // 上传文件
    const uploadResult = await new Promise((resolve, reject) => {
      cos.uploadFile({
        Bucket: options.bucket,
        Region: options.region,
        Key: cosKey,
        FilePath: filePath,
        SliceSize: 1024 * 1024 * 5 // 5MB分块
      }, (err, data) => {
        if (err) reject(err);
        else resolve(data);
      });
    });

    // 构建访问URL
    const accessUrl = `https://${options.bucket}.cos.${options.region}.myqcloud.com/${cosKey}`;

    // 生成预签名URL（24小时有效期）
    let signedUrl = null;
    try {
      signedUrl = await new Promise((resolve, reject) => {
        cos.getObjectUrl({
          Bucket: options.bucket,
          Region: options.region,
          Key: cosKey,
          Sign: true,
          Expires: 86400
        }, (err, data) => {
          if (err) resolve(null);
          else resolve(data.Url);
        });
      });
    } catch (e) {
      // 忽略预签名错误
    }

    // 输出结果
    console.log('\\n✅ 上传成功!');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`📁 文件名: ${fileName}`);
    console.log(`📍 COS Key: ${cosKey}`);
    console.log(`📦 ETag: ${uploadResult.ETag}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('\\n🔗 直接访问URL:');
    console.log(accessUrl);
    
    if (signedUrl) {
      console.log('\\n🔐 预签名URL (24小时有效):');
      console.log(signedUrl);
    }
    
    console.log('\\n💡 提示: 如果存储桶是私有的，请使用预签名URL访问');

    return {
      success: true,
      fileName,
      cosKey,
      url: accessUrl,
      signedUrl,
      etag: uploadResult.ETag
    };

  } catch (error) {
    console.error('\\n❌ 上传失败:', error.message);
    if (error.statusCode === 403) {
      console.error('\\n可能是以下原因:');
      console.error('- SecretId/SecretKey 不正确');
      console.error('- 密钥没有 COS 访问权限');
      console.error('- 存储桶不存在或无权限');
    }
    process.exit(1);
  }
}

// 执行
const { filePath, options } = parseArgs();
uploadToCOS(filePath, options);
