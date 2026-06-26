# YouTube to S3 Uploader

A complete workflow for downloading YouTube videos and storing them in your own S3-compatible storage.

## What This Skill Does

1. **Downloads YouTube videos** using yt-dlp
2. **Uploads to your S3 storage** (Cloudflare R2, AWS S3, MinIO, etc.)
3. **Generates access URLs** for sharing
4. **Automatically cleans up** local files
5. **Tracks progress** with detailed logging

## Why Use This?

- **Own your data**: Videos stored in YOUR S3, not on YouTube's servers
- **Privacy control**: No third-party tracking of your watched videos
- **Permanent storage**: Videos won't disappear if YouTube removes them
- **Fast access**: CDN-accelerated through Cloudflare or AWS CloudFront
- **Cost effective**: Store videos cheaply with Cloudflare R2 (no egress fees)

## Quick Start

### 1. Install

```bash
clawhub install youtube-s3-uploader
```

### 2. Configure

Create `~/.youtube-s3-uploader.yml`:

```yaml
default: my-videos

buckets:
  my-videos:
    endpoint: https://your-s3-endpoint.com
    access_key_id: YOUR_ACCESS_KEY
    secret_access_key: YOUR_SECRET_KEY
    bucket_name: my-videos
    region: auto
```

### 3. Use

```bash
# Download and upload a YouTube video
youtube-s3-upload https://youtu.be/VIDEO_ID

# Test your S3 connection
youtube-s3-upload test

# Show configuration
youtube-s3-upload config
```

## Supported S3 Providers

- ✅ **Cloudflare R2** (recommended - no egress fees)
- ✅ **AWS S3**
- ✅ **MinIO** (self-hosted)
- ✅ **Backblaze B2**
- ✅ **Google Cloud Storage**
- ✅ **Any S3-compatible service**

## Use Cases

### Personal Media Archive
```bash
# Archive your favorite YouTube videos
youtube-s3-upload https://youtu.be/favorite-video-1
youtube-s3-upload https://youtu.be/favorite-video-2
```

### Content Backup
```bash
# Backup important tutorial videos
youtube-s3-upload https://youtu.be/important-tutorial --path tutorials/programming/
```

### Team Collaboration
```bash
# Share videos with team (generate presigned URLs)
youtube-s3-upload https://youtu.be/team-meeting --path team/meetings/
```

## Advanced Features

### Custom S3 Paths
```bash
# Organize by date and category
youtube-s3-upload https://youtu.be/VIDEO_ID --path videos/2026/march/education/
```

### Multiple Buckets
```bash
# Use different buckets for different purposes
youtube-s3-upload https://youtu.be/VIDEO_ID --bucket personal
youtube-s3-upload https://youtu.be/VIDEO_ID --bucket work
```

### Debug Mode
```bash
# See detailed logs for troubleshooting
youtube-s3-upload https://youtu.be/VIDEO_ID --debug
```

## Security Features

- **Encrypted uploads**: All data encrypted in transit (HTTPS)
- **Secure credentials**: Stored locally in your config file
- **Access control**: Fine-grained bucket policies supported
- **Audit logging**: All uploads logged with timestamps
- **No external APIs**: Everything runs locally

## Performance

- **Parallel processing**: Download and metadata extraction happen concurrently
- **Resumable uploads**: Large files upload in chunks
- **Progress tracking**: Real-time speed and ETA display
- **Memory efficient**: Streams files without loading entire video into memory

## Requirements

- Node.js 18 or higher
- yt-dlp installed (auto-detected or installs automatically)
- S3-compatible storage account
- 100MB free disk space for temporary files

## Installation Notes

The skill will:
1. Check for yt-dlp installation
2. Offer to install it if missing
3. Validate S3 credentials
4. Test connection to your storage

## Troubleshooting

### Common Issues

**"yt-dlp not found"**
```bash
# Install yt-dlp manually
pip install yt-dlp
# or
brew install yt-dlp
```

**"Invalid S3 credentials"**
- Check your Access Key ID and Secret Access Key
- Verify bucket exists and you have write permissions
- Test with: `youtube-s3-upload test`

**"Upload too slow"**
- Check your internet connection
- Consider using Cloudflare R2 for better performance
- Large files (>100MB) may take longer

### Getting Help

1. Check debug logs: `youtube-s3-upload --debug`
2. Test connection: `youtube-s3-upload test`
3. Review config: `youtube-s3-upload config`

## Development

This skill is open source and welcomes contributions:

- Report issues on GitHub
- Submit pull requests
- Suggest new features
- Improve documentation

## License

MIT-0 - Free to use, modify, and redistribute. No attribution required.

## Credits

Created by 西米露 (Simeilu) - Making personal media storage simple and secure.