#!/usr/bin/env node

/**
 * YouTube to S3 Uploader - Main CLI
 * 
 * Usage: youtube-s3-upload <YouTube URL> [options]
 */

import { program } from 'commander';
import { downloadAndUpload } from './core.js';
import { testConnection } from './s3-client.js';
import { loadConfig } from './config.js';

program
  .name('youtube-s3-upload')
  .description('Download YouTube videos and upload to S3 storage')
  .version('1.0.0')
  .argument('<url>', 'YouTube video URL')
  .option('-b, --bucket <name>', 'S3 bucket name (from config)')
  .option('-p, --path <path>', 'Custom S3 path (e.g., videos/2026/march/my-video.mp4)')
  .option('-k, --keep-local', 'Keep local file after upload', false)
  .option('-d, --debug', 'Enable debug logging', false)
  .action(async (url, options) => {
    try {
      console.log('🎬 YouTube to S3 Uploader\n');
      
      const config = loadConfig();
      const bucketName = options.bucket || config.default;
      
      console.log(`📋 Configuration:`);
      console.log(`  YouTube URL: ${url}`);
      console.log(`  S3 Bucket: ${bucketName}`);
      if (options.path) console.log(`  S3 Path: ${options.path}`);
      
      const result = await downloadAndUpload(url, {
        bucket: bucketName,
        customPath: options.path,
        keepLocal: options.keepLocal,
        debug: options.debug
      });
      
      if (result.success) {
        console.log('\n🎉 Processing Complete!\n');
        console.log('📊 Results:');
        console.log(`  Video Title: ${result.videoInfo.title}`);
        console.log(`  Original Size: ${(result.size / 1024 / 1024).toFixed(2)} MB`);
        console.log(`  Upload Time: ${result.uploadTime.toFixed(2)} seconds`);
        console.log(`  Average Speed: ${(result.size / 1024 / 1024 / result.uploadTime).toFixed(2)} MB/s\n`);
        console.log('🔗 S3 Access URL:');
        console.log(`  ${result.url}\n`);
        console.log('📁 S3 Path:');
        console.log(`  ${result.bucket}/${result.s3Key}\n`);
        console.log('💡 Tip: This URL may require authentication. Use presigned URLs for temporary access.');
      } else {
        console.error('❌ Processing failed:', result.error);
        process.exit(1);
      }
    } catch (error) {
      console.error('❌ Error:', error.message);
      if (options.debug) console.error(error.stack);
      process.exit(1);
    }
  });

program
  .command('test')
  .description('Test S3 connection')
  .option('-b, --bucket <name>', 'Test specific bucket')
  .action(async (options) => {
    try {
      console.log('🔍 Testing S3 Connection...\n');
      const result = await testConnection(options.bucket);
      
      if (result.success) {
        console.log('✅ S3 Connection Test Successful!\n');
        console.log('📋 Connection Details:');
        console.log(`  Endpoint: ${result.endpoint}`);
        console.log(`  Bucket: ${result.bucket}`);
        console.log(`  Region: ${result.region}`);
        console.log(`  Available Buckets: ${result.availableBuckets.join(', ')}`);
        
        if (result.objects && result.objects.length > 0) {
          console.log(`\n📁 Objects in bucket (first 5):`);
          result.objects.slice(0, 5).forEach(obj => {
            console.log(`  - ${obj.Key} (${obj.Size} bytes)`);
          });
        } else {
          console.log('\n📁 Bucket is empty');
        }
      } else {
        console.error('❌ S3 Connection Test Failed:', result.error);
        process.exit(1);
      }
    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

program
  .command('config')
  .description('Show current configuration')
  .action(() => {
    try {
      const config = loadConfig();
      console.log('📋 Current Configuration:\n');
      console.log(`Default bucket: ${config.default}`);
      console.log('\nConfigured buckets:');
      Object.entries(config.buckets).forEach(([name, bucketConfig]) => {
        console.log(`\n  ${name}:`);
        console.log(`    Endpoint: ${bucketConfig.endpoint}`);
        console.log(`    Bucket: ${bucketConfig.bucket_name}`);
        console.log(`    Region: ${bucketConfig.region}`);
        console.log(`    Access Key: ${bucketConfig.access_key_id ? '***' + bucketConfig.access_key_id.slice(-4) : 'not set'}`);
      });
    } catch (error) {
      console.error('❌ Error loading config:', error.message);
      process.exit(1);
    }
  });

program.parse();