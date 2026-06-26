# US3 CLI Configuration Guide

## Overview

This document explains how to install and configure us3cli (filemgr) for uploading files to UCloud US3 (UFile) object storage.

## Installation

### Download us3cli

**Official sources:**
- GitHub Releases: https://github.com/ucloud/us3cli/releases
- Official Documentation: https://docs.ucloud.cn/ufile/tools/us3cli/prepare

**Select the correct binary for your platform:**
- macOS: `filemgr-darwin` or `filemgr-mac`
- Linux: `filemgr-linux`
- Windows: `filemgr-windows.exe`

**Installation steps (macOS/Linux):**
```bash
# Download the binary (replace URL with latest version)
curl -L https://github.com/ucloud/us3cli/releases/download/vX.X.X/filemgr-darwin -o filemgr

# Make it executable
chmod +x filemgr

# Move to PATH (optional)
sudo mv filemgr /usr/local/bin/filemgr
```

**Verify installation:**
```bash
filemgr --help
```

## Configuration

### Required Credentials

You need the following from your UCloud account:

1. **Public Key** (API 公钥) - YOUR_PUBLIC_KEY_HERE
2. **Private Key** (API 私钥) - YOUR_PRIVATE_KEY_HERE
3. **Bucket Name** - your-bucket-name
4. **Endpoint** - cn-sh2.ufileos.com

### How to Get Credentials

You need to obtain your own credentials from UCloud console. See the section above for how to get them.

### Configure us3cli

Run the interactive configuration command:

```bash
filemgr-config --action putconfig
```

You will be prompted to enter:
- **Public Key**: Your API public key
- **Private Key**: Your API private key
- **Bucket Name**: Your bucket name
- **Endpoint**: Region endpoint (e.g., cn-bj.ufileos.com)
- **File Host**: Leave empty or press Enter

**Example configuration session:**
```
Please input your public key: TOKEN_xxxxx-xxxx-xxxx
Please input your private key: xxxxx-xxxx-xxxx-xxxx
Please input your bucket name: my-bucket
Please input your bucket endpoint: cn-bj.ufileos.com
Please input your file host (optional): [Press Enter]
```

The configuration is saved to `~/.us3cliconfig`

### View Current Configuration

```bash
filemgr-config --action getconfig
```

## Common Endpoints by Region

- **北京 Beijing**: `cn-bj.ufileos.com`
- **上海 Shanghai**: `cn-sh2.ufileos.com`
- **广州 Guangzhou**: `cn-gd.ufileos.com`
- **香港 Hong Kong**: `hk.ufileos.com`
- **新加坡 Singapore**: `sg.ufileos.com`
- **美国 US**: `us-ca.ufileos.com`

## Testing the Setup

Test by uploading a file:

```bash
filemgr --action put --bucket your-bucket --key test.txt --file /path/to/test.txt
```

Successful upload will show:
```
Put file test.txt success!!
```

## Download URL Format

After upload, files are accessible at:
```
https://{bucket}.{endpoint}/{filename}
```

Example:
```
https://my-bucket.cn-bj.ufileos.com/document.pdf
```

## Security Best Practices

- ⚠️ Never commit `.us3cliconfig` to version control
- Keep API keys secure and private
- Use `.gitignore` to exclude config files
- Rotate API keys periodically
- Use separate buckets for different environments (dev/prod)
- For public sharing, set bucket permissions to public-read

## Troubleshooting

**"filemgr: command not found"**
- Ensure the binary is executable: `chmod +x filemgr`
- Ensure it's in your PATH or use full path: `/path/to/filemgr`

**"Config file not found"**
- Run: `filemgr-config --action putconfig` to create configuration

**Upload fails with authentication error**
- Verify your API keys are correct
- Check if keys are still active in UCloud console
- Ensure bucket name and endpoint match your configuration
