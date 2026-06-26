#!/usr/bin/env node

// 修复版：使用S3分块上传视频文件
const { 
  S3Client, 
  CreateMultipartUploadCommand,
  UploadPartCommand, 
  CompleteMultipartUploadCommand,
  AbortMultipartUploadCommand
} = require('@aws-sdk/client-s3');
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

class FixedS3Uploader {
  constructor(configFile = '/home/node/.openclaw/workspace/.r2-upload.yml') {
    this.configFile = configFile;
    this.loadConfig();
  }
  
  loadConfig() {
    if (!fs.existsSync(this.configFile)) {
      throw new Error(`配置文件不存在: ${this.configFile}`);
    }
    
    const config = yaml.load(fs.readFileSync(this.configFile, 'utf8'));
    const bucketConfig = config.buckets[config.default];
    
    this.client = new S3Client({
      endpoint: bucketConfig.endpoint,
      credentials: {
        accessKeyId: bucketConfig.access_key_id,
        secretAccessKey: bucketConfig.secret_access_key
      },
      region: bucketConfig.region,
      forcePathStyle: true,
    });
    
    this.bucketConfig = bucketConfig;
  }
  
  async uploadVideo(videoPath, customKey = null, options = {}) {
    console.log('🎬 修复版：上传视频到 S3（使用分块上传）\n');
    
    // 检查文件
    if (!fs.existsSync(videoPath)) {
      throw new Error(`视频文件不存在: ${videoPath}`);
    }
    
    const stats = fs.statSync(videoPath);
    const fileSizeMB = stats.size / 1024 / 1024;
    const fileName = path.basename(videoPath);
    const fileExt = path.extname(videoPath).toLowerCase();
    
    console.log('📋 文件信息:');
    console.log('文件名:', fileName);
    console.log('大小:', fileSizeMB.toFixed(2), 'MB');
    console.log('类型:', fileExt);
    
    // 确定内容类型
    let contentType = 'application/octet-stream';
    if (fileExt === '.mp4') contentType = 'video/mp4';
    else if (fileExt === '.webm') contentType = 'video/webm';
    else if (fileExt === '.avi') contentType = 'video/x-msvideo';
    else if (fileExt === '.mov') contentType = 'video/quicktime';
    
    // 生成文件键
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const fileKey = customKey || `videos/${timestamp}-${fileName}`;
    
    console.log('\n📤 上传配置:');
    console.log('存储桶:', this.bucketConfig.bucket_name);
    console.log('S3路径:', fileKey);
    console.log('方法: S3分块上传');
    
    // 根据文件大小选择方法
    const method = fileSizeMB > 50 ? 'multipart' : 'simple';
    console.log('选择方法:', method === 'multipart' ? '分块上传' : '简单PUT');
    
    if (method === 'multipart') {
      return await this.uploadMultipart(videoPath, fileKey, contentType, stats, options);
    } else {
      return await this.uploadSimple(videoPath, fileKey, contentType, stats, options);
    }
  }
  
  async uploadMultipart(videoPath, fileKey, contentType, stats, options) {
    console.log('\n🔧 使用S3分块上传...');
    
    const partSize = options.partSize || 50 * 1024 * 1024; // 默认50MB
    const maxRetries = options.maxRetries || 3;
    
    console.log('分块大小:', partSize / 1024 / 1024, 'MB');
    
    let uploadId = null;
    let partETags = [];
    
    try {
      // 1. 初始化分块上传
      console.log('1. 初始化分块上传...');
      const createResponse = await this.client.send(new CreateMultipartUploadCommand({
        Bucket: this.bucketConfig.bucket_name,
        Key: fileKey,
        ContentType: contentType,
        Metadata: options.metadata || {
          uploadedBy: 'fixed-s3-uploader',
          uploadTime: new Date().toISOString(),
          method: 'multipart'
        }
      }));
      
      uploadId = createResponse.UploadId;
      console.log('上传ID:', uploadId.substring(0, 50) + '...');
      
      // 2. 计算分块
      const partCount = Math.ceil(stats.size / partSize);
      console.log(`总块数: ${partCount}`);
      
      // 3. 上传各个分块
      console.log('2. 上传分块...');
      
      for (let partNumber = 1; partNumber <= partCount; partNumber++) {
        const start = (partNumber - 1) * partSize;
        const end = Math.min(start + partSize, stats.size);
        const chunkSize = end - start;
        
        console.log(`   分块 ${partNumber}/${partCount} (${chunkSize / 1024 / 1024} MB)...`);
        
        // 读取分块
        const chunkBuffer = Buffer.alloc(chunkSize);
        const fd = fs.openSync(videoPath, 'r');
        fs.readSync(fd, chunkBuffer, 0, chunkSize, start);
        fs.closeSync(fd);
        
        // 上传分块（带重试）
        let retryCount = 0;
        let uploaded = false;
        
        while (!uploaded && retryCount < maxRetries) {
          try {
            const uploadPartResponse = await this.client.send(new UploadPartCommand({
              Bucket: this.bucketConfig.bucket_name,
              Key: fileKey,
              UploadId: uploadId,
              PartNumber: partNumber,
              Body: chunkBuffer,
              ContentLength: chunkSize,
            }));
            
            partETags.push({
              PartNumber: partNumber,
              ETag: uploadPartResponse.ETag
            });
            
            console.log(`     ✅ 分块 ${partNumber} 完成`);
            uploaded = true;
            
          } catch (error) {
            retryCount++;
            if (retryCount >= maxRetries) {
              console.log(`     ❌ 分块 ${partNumber} 失败: ${error.message}`);
              throw error;
            }
            console.log(`     ⚠️  分块 ${partNumber} 重试 ${retryCount}/${maxRetries}`);
            await new Promise(resolve => setTimeout(resolve, 1000 * retryCount));
          }
        }
      }
      
      // 4. 完成分块上传
      console.log('3. 完成分块上传...');
      
      // 按PartNumber排序
      partETags.sort((a, b) => a.PartNumber - b.PartNumber);
      
      const completeResponse = await this.client.send(new CompleteMultipartUploadCommand({
        Bucket: this.bucketConfig.bucket_name,
        Key: fileKey,
        UploadId: uploadId,
        MultipartUpload: {
          Parts: partETags
        }
      }));
      
      console.log('\n✅ 分块上传成功！');
      console.log('ETag:', completeResponse.ETag);
      
      const fileUrl = `${this.bucketConfig.endpoint}/${this.bucketConfig.bucket_name}/${fileKey}`;
      
      return {
        success: true,
        url: fileUrl,
        key: fileKey,
        size: stats.size,
        etag: completeResponse.ETag,
        method: 'multipart',
        partCount: partCount,
        duration: null // 由调用者计算
      };
      
    } catch (error) {
      console.error('\n❌ 分块上传失败:', error.message);
      
      // 如果上传失败，尝试中止上传
      if (uploadId) {
        try {
          console.log('尝试中止未完成的上传...');
          await this.client.send(new AbortMultipartUploadCommand({
            Bucket: this.bucketConfig.bucket_name,
            Key: fileKey,
            UploadId: uploadId
          }));
          console.log('已中止上传');
        } catch (abortError) {
          console.log('中止上传失败:', abortError.message);
        }
      }
      
      throw error;
    }
  }
  
  async uploadSimple(videoPath, fileKey, contentType, stats, options) {
    console.log('\n🔧 使用简单PUT上传（小文件）...');
    
    try {
      // 读取文件
      console.log('读取文件...');
      const fileBuffer = fs.readFileSync(videoPath);
      
      // 上传
      const { PutObjectCommand } = require('@aws-sdk/client-s3');
      const uploadCommand = new PutObjectCommand({
        Bucket: this.bucketConfig.bucket_name,
        Key: fileKey,
        Body: fileBuffer,
        ContentType: contentType,
        ContentLength: stats.size,
        Metadata: options.metadata || {
          uploadedBy: 'fixed-s3-uploader',
          uploadTime: new Date().toISOString(),
          method: 'simple'
        }
      });
      
      console.log('上传中...');
      const result = await this.client.send(uploadCommand);
      
      const fileUrl = `${this.bucketConfig.endpoint}/${this.bucketConfig.bucket_name}/${fileKey}`;
      
      return {
        success: true,
        url: fileUrl,
        key: fileKey,
        size: stats.size,
        etag: result.ETag,
        method: 'simple',
        partCount: 1
      };
      
    } catch (error) {
      console.error('❌ 简单上传失败:', error.message);
      throw error;
    }
  }
  
  async verifyUpload(url, expectedSize) {
    console.log(`\n🔍 验证上传: ${url}`);
    
    return new Promise((resolve) => {
      const { exec } = require('child_process');
      exec(`curl -I "${url}" 2>/dev/null | head -8`, (error, stdout) => {
        if (error) {
          resolve({ verified: false, error: error.message });
          return;
        }
        
        console.log('HTTP响应:');
        console.log(stdout.trim());
        
        if (stdout.includes('200')) {
          console.log('✅ 文件可访问');
          
          // 检查大小
          const contentLength = stdout.match(/content-length:\s*(\d+)/i);
          if (contentLength) {
            const serverSize = parseInt(contentLength[1]);
            console.log(`服务器大小: ${(serverSize / 1024 / 1024).toFixed(2)} MB`);
            console.log(`大小匹配: ${serverSize === expectedSize ? '✅' : '❌'}`);
          }
          
          resolve({ verified: true, response: stdout });
        } else {
          console.log('❌ 文件不可访问');
          resolve({ verified: false, response: stdout });
        }
      });
    });
  }
}

// 命令行接口
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('🎬 修复版视频上传工具');
    console.log('使用方法:');
    console.log('  node fixed-upload-video-to-s3.js <视频文件路径> [S3路径]');
    console.log('\n选项:');
    console.log('  --part-size <MB>    分块大小（默认50MB）');
    console.log('  --simple            强制使用简单PUT方法');
    console.log('\n示例:');
    console.log('  node fixed-upload-video-to-s3.js video.mp4');
    console.log('  node fixed-upload-video-to-s3.js video.mp4 videos/my-video.mp4');
    console.log('  node fixed-upload-video-to-s3.js video.mp4 --part-size 20');
    console.log('  node fixed-upload-video-to-s3.js small.mp4 --simple');
    process.exit(1);
  }
  
  const videoPath = args[0];
  let customKey = null;
  let partSize = 50 * 1024 * 1024;
  let forceSimple = false;
  
  // 解析参数
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--part-size' && args[i + 1]) {
      partSize = parseInt(args[i + 1]) * 1024 * 1024;
      i++;
    } else if (args[i] === '--simple') {
      forceSimple = true;
    } else if (!args[i].startsWith('--') && !customKey) {
      customKey = args[i];
    }
  }
  
  try {
    const uploader = new FixedS3Uploader();
    
    const startTime = Date.now();
    
    const result = await uploader.uploadVideo(videoPath, customKey, {
      partSize: forceSimple ? undefined : partSize,
      metadata: {
        uploadedBy: 'youtube-s3-uploader-fixed',
        timestamp: new Date().toISOString()
      }
    });
    
    const duration = (Date.now() - startTime) / 1000;
    
    if (result.success) {
      console.log('\n🎉 上传成功！');
      console.log('耗时:', duration.toFixed(2), '秒');
      console.log('速度:', (result.size / 1024 / 1024 / duration).toFixed(2), 'MB/秒');
      console.log('方法:', result.method);
      console.log('分块数:', result.partCount);
      console.log('URL:', result.url);
      
      // 验证
      await uploader.verifyUpload(result.url, result.size);
      
    } else {
      console.log('\n❌ 上传失败');
      console.log('错误:', result.error);
    }
    
  } catch (error) {
    console.error('\n❌ 上传过程错误:', error.message);
    process.exit(1);
  }
}

// 运行
if (require.main === module) {
  main().catch(error => {
    console.error('主程序错误:', error);
    process.exit(1);
  });
}

module.exports = FixedS3Uploader;