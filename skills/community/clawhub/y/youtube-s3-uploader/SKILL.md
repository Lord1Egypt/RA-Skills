---
name: Universal Video to S3 Uploader
description: Download videos from YouTube, Twitter/X, TikTok, Douyin, Bilibili and upload to S3-compatible storage. Universal video downloader with smart quality selection and audio merging.
summary: A universal video downloader that supports multiple platforms (YouTube, Twitter/X, TikTok, Douyin, Bilibili, etc.) and uploads to your own S3-compatible storage. Features platform detection, intelligent quality selection, readable filenames, reliable audio merging, and S3 Multipart Upload for large files.
metadata: {"clawdbot":{"emoji":"🌐→☁️","os":["linux","darwin"]}, "version": "3.0.1"}
---

# Universal Video to S3 Uploader v3.0.1

A universal video downloader that supports multiple platforms and uploads to S3-compatible storage.

## 🚀 Version 3.0.1 - Filename Optimization

### What's New:
- **✅ Clean Filenames**: Removes all punctuation marks, emojis, and special characters from filenames
- **✅ Better Unicode Support**: Proper handling of Chinese punctuation and emojis
- **✅ Platform Detection**: Automatic detection of video platform (YouTube, Twitter/X, TikTok, etc.)
- **✅ Universal Support**: Works with 1000+ websites via yt-dlp

### Breaking Changes:
- **❌ NOT backward compatible**: v3.x is a complete rewrite from v2.x
- **❌ New API**: Universal `video-to-s3-universal.js` script
- **❌ Platform Detection**: Automatically detects video platform

### Why v3.0.1?
v3.0.1 improves filename handling:
1. **Clean filenames** - Removes all punctuation and emojis
2. **Better S3 compatibility** - Avoids issues with special characters
3. **Improved readability** - Clean, readable filenames without clutter

### What's New:
- **✅ S3 Multipart Upload for All Files**: v2.0.0 uses S3 multipart upload for all file sizes
- **✅ Memory Optimization**: Chunked reading to avoid memory overflow
- **✅ Error Recovery**: Automatic retry mechanism for failed uploads
- **✅ Smart Chunk Sizing**: Automatically adjusts chunk size based on file size
- **✅ Performance Improvements**: Better progress tracking and speed calculation
- **✅ Fixed Help System**: Proper help information display

### Breaking Changes:
- **❌ NOT backward compatible**: v2.0.0 is a complete rewrite
- **❌ Old scripts removed**: All v1.x scripts have been replaced
- **❌ New API**: Uses S3 multipart upload for all files, not just large ones

### Why v2.0.0?
v2.0.0 fixes critical issues in v1.x:
1. **Fixed help system** - Proper `--help` display
2. **Consistent API** - Always uses multipart upload
3. **Better error handling** - Improved error messages
4. **Cleaner codebase** - Removed compatibility layers

## Features

- **One-command workflow**: Download YouTube video → Upload to S3 → Get access URL
- **S3-compatible**: Works with Cloudflare R2, AWS S3, MinIO, and any S3-compatible storage
- **Automatic cleanup**: Removes local files after successful upload
- **Progress tracking**: Real-time upload progress and speed calculation
- **Secure by default**: Uses your own S3 credentials, no external dependencies
- **Flexible configuration**: Multiple bucket support, custom paths, metadata
- **Smart upload method**: Automatically uses S3 Multipart Upload for large files (>50MB)
- **Memory efficient**: Chunked reading to avoid memory overflow
- **Error recovery**: Retry mechanism for failed uploads

## Prerequisites

1. **S3-compatible storage** (Cloudflare R2, AWS S3, MinIO, etc.)
2. **S3 credentials** (Access Key ID and Secret Access Key)
3. **Bucket created** with appropriate permissions

## Quick Start

### 1. Install the skill

```bash
clawhub install youtube-s3-uploader
```

### 2. Configure your S3 storage

Create `~/.youtube-s3-uploader.yml`:

```yaml
# Default bucket to use
default: my-videos

# Bucket configurations
buckets:
  my-videos:
    endpoint: https://your-s3-endpoint.com
    access_key_id: YOUR_ACCESS_KEY_ID
    secret_access_key: YOUR_SECRET_ACCESS_KEY
    bucket_name: my-videos
    region: auto  # Use "auto" for Cloudflare R2, or specific region for AWS S3
    # Optional: Custom public URL (e.g., CDN domain)
    # public_url: https://cdn.yourdomain.com
```

### 3. Download and upload a YouTube video

```bash
youtube-s3-upload https://youtu.be/VIDEO_ID
```

## Configuration Details

### Cloudflare R2 Example

```yaml
buckets:
  r2-storage:
    endpoint: https://ACCOUNT_ID.r2.cloudflarestorage.com
    access_key_id: YOUR_R2_ACCESS_KEY_ID
    secret_access_key: YOUR_R2_SECRET_ACCESS_KEY
    bucket_name: video-storage
    region: auto
```

### AWS S3 Example

```yaml
buckets:
  aws-s3:
    endpoint: https://s3.us-east-1.amazonaws.com
    access_key_id: YOUR_AWS_ACCESS_KEY_ID
    secret_access_key: YOUR_AWS_SECRET_ACCESS_KEY
    bucket_name: my-video-bucket
    region: us-east-1
```

### MinIO / Self-hosted Example

```yaml
buckets:
  minio:
    endpoint: http://localhost:9000
    access_key_id: minioadmin
    secret_access_key: minioadmin
    bucket_name: uploads
    region: us-east-1
```

## Usage

### Basic usage

```bash
# Download and upload a YouTube video (original method)
youtube-s3-upload https://youtu.be/8uZGlzWA4oo

# Download and upload using FIXED method (recommended for large files)
npm run youtube-to-s3-fixed -- https://youtu.be/8uZGlzWA4oo

# Specify custom S3 path
youtube-s3-upload https://youtu.be/VIDEO_ID --path videos/2026/march/my-video.mp4

# Use specific bucket (from config)
youtube-s3-upload https://youtu.be/VIDEO_ID --bucket backup-bucket

# Keep local file after upload (for debugging)
youtube-s3-upload https://youtu.be/VIDEO_ID --keep-local
```

### Upload existing video file

```bash
# Upload a local video file to S3
upload-to-s3 /path/to/video.mp4

# With custom S3 path
upload-to-s3 /path/to/video.mp4 --path archived/videos/special.mp4
```

### Test S3 connection

```bash
# Test S3 connection and bucket access
test-s3-connection

# Test specific bucket
test-s3-connection --bucket my-bucket
```

## Output

After successful processing, you'll get:

```
🎉 Processing Complete!

📊 Results:
Video Title: What Made the Turtle Cry!? Vedal's First Interaction with Neuro 3D
Original Size: 41.22 MB
Upload Time: 11.12 seconds
Average Speed: 3.71 MB/s

🔗 S3 Access URL:
https://s3.yourdomain.com/bucket-name/videos/2026-03-25/video-title.mp4

📁 S3 Path:
bucket-name/videos/2026-03-25/video-title.mp4

💡 Tip: This URL may require authentication. Use presigned URLs for temporary access.
```

## Advanced Features

### Presigned URLs

Generate temporary access URLs (default: 1 hour):

```bash
generate-presigned-url videos/2026/march/my-video.mp4

# Custom expiration (e.g., 24 hours)
generate-presigned-url videos/2026/march/my-video.mp4 --expires 24h
```

### List uploaded videos

```bash
# List recent uploads
list-s3-uploads

# List from specific bucket
list-s3-uploads --bucket my-bucket

# List with details
list-s3-uploads --detailed
```

### Delete files from S3

```bash
# Delete a file
delete-from-s3 videos/old-video.mp4

# Delete with confirmation
delete-from-s3 videos/old-video.mp4 --confirm
```

## Environment Variables

- `YOUTUBE_S3_CONFIG`: Path to config file (default: `~/.youtube-s3-uploader.yml`)
- `YOUTUBE_S3_DEFAULT_BUCKET`: Override default bucket
- `YOUTUBE_S3_KEEP_LOCAL`: Keep local files (default: `false`)
- `YOUTUBE_S3_DEBUG`: Enable debug logging

## Security Best Practices

1. **Use IAM roles** when possible instead of long-term credentials
2. **Set short expiration** for presigned URLs (minutes, not days)
3. **Enable bucket versioning** for accidental deletion protection
4. **Configure lifecycle rules** to automatically delete old files
5. **Use bucket policies** to restrict access by IP or referrer

## Troubleshooting

### Common Issues

1. **"Invalid credentials"**: Check your Access Key ID and Secret Access Key
2. **"Bucket does not exist"**: Create the bucket in your S3 provider's dashboard
3. **"Access denied"**: Verify bucket policies and IAM permissions
4. **"SSL certificate error"**: For self-signed certificates, use HTTP or add certificate exception
5. **"Upload timeout"**: Large files may need multipart upload - use the fixed version
6. **"Memory overflow"**: Use the fixed version with chunked reading
7. **"Large file upload fails"**: Use `youtube-to-s3-fixed.js` for files >50MB

### Fixed Version for Large Files

For large video files (>50MB), use the fixed version that implements S3 Multipart Upload:

```bash
# Using npm script
npm run youtube-to-s3-fixed -- https://youtu.be/VIDEO_ID

# Direct script execution
node scripts/youtube-to-s3-fixed.js https://youtu.be/VIDEO_ID

# Upload existing large file
node scripts/fixed-upload-video-to-s3.js /path/to/large-video.mp4
```

The fixed version:
- Uses S3 Multipart Upload for files >50MB
- Implements chunked reading to avoid memory overflow
- Includes retry mechanism for failed uploads
- Shows real-time progress and speed
- Automatically selects best method based on file size

### Debug Mode

Enable debug logging to see detailed information:

```bash
YOUTUBE_S3_DEBUG=true youtube-s3-upload https://youtu.be/VIDEO_ID
```

## License

MIT-0 - Free to use, modify, and redistribute. No attribution required.

## Credits

Created by 西米露 (Simeilu) - A complete YouTube to S3 workflow for personal media storage.