# Configuration Guide

## Tencent Cloud API Credentials Configuration

Before using TencentCloud-HotSearch-skill, you need to configure the credentials for Tencent Cloud Online Search API (SearchPro). The API uses **SecretId** and **SecretKey** for authentication.

**API Information:**
- **Endpoint Domain**: wsa.tencentcloudapi.com
- **API Version**: 2025-05-08
- **API Name**: SearchPro

## Obtaining Tencent Cloud API Credentials

### Step 1: Register/Login to Tencent Cloud Account

1. Visit [Tencent Cloud Official Website](https://cloud.tencent.com/)
2. Click "Register" or "Login" in the top right corner
3. If you're a new user, complete the registration process
4. Log in to your Tencent Cloud account

### Step 2: Activate Online Search Service

1. After logging in, visit [Tencent Cloud Console](https://console.cloud.tencent.com/)
2. Enter "Online Search" in the search box
3. Click to enter the "Online Search" product page
4. Click the "Activate Now" button
5. Read and agree to the service agreement
6. Complete the activation process

### Step 3: Obtain API Credentials

#### Get SecretId and SecretKey

1. Visit [Tencent Cloud Access Management Console](https://console.cloud.tencent.com/cam/capi)
2. Click the "Create Key" button
3. The system will generate a pair of credentials:
   - **SecretId**: Key ID (format: AKIDxxxxxxxxxxxxxxxx)
   - **SecretKey**: Key (format: xxxxxxxxxxxxxxxx)
4. **Important**: Please save these two credentials immediately, SecretKey is only displayed once!

#### Obtain via Online Search Product

1. Enter [Online Search Console](https://console.cloud.tencent.com/ais)
2. Select "API Key Management" in the left navigation bar
3. Click "Create Key"
4. Copy the generated SecretId and SecretKey

## Configuration File

### config.json Structure

```json
{
  "secret_id": "YOUR_TENCENT_CLOUD_SECRET_ID",
  "secret_key": "YOUR_TENCENT_CLOUD_SECRET_KEY",
  "output_dir": "./output"
}
```

### Configuration Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| secret_id | string | Yes | Tencent Cloud API SecretId |
| secret_key | string | Yes | Tencent Cloud API SecretKey |
| output_dir | string | No | Default output directory, defaults to ./output |

## Configuration Steps

### 1. Create Configuration File

If the `config.json` file does not exist, copy it from the example file:

```bash
cp config.example.json config.json
```

### 2. Edit Configuration File

Open `config.json` with a text editor and fill in your API credentials:

```json
{
  "secret_id": "AKIDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "secret_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "output_dir": "./output"
}
```

**Important Notes:**
- Ensure the JSON format is correct, no extra commas
- SecretId and SecretKey must be enclosed in quotes
- Do not add comments in the configuration file (JSON does not support comments)
- `output_dir` specifies the default output directory, uses `./output` if not specified

## Security Recommendations

### 1. API Credentials Protection

- ⚠️ **DO NOT** commit `config.json` to version control (Git)
- ⚠️ Use `.gitignore` to ignore `config.json` (already configured)
- ⚠️ Rotate API keys regularly
- ⚠️ Use different keys for different environments
- ⚠️ Follow least privilege principle when configuring API keys
- ⚠️ Rotate/delete keys after testing

### 2. Output Directory Safety

- ⚠️ Do not set output directory to sensitive system paths
- ⚠️ Recommended to use dedicated temporary directory or sandbox environment
- ⚠️ Program will automatically create output directory but prevents directory traversal attacks
- ⚠️ Output path must be within the configured output_dir directory

### 3. Runtime Environment

- ⚠️ Recommended to run in isolated environment (container or sandbox)
- ⚠️ Use temporary API keys with minimal permissions for testing
- ⚠️ All API requests are encrypted via HTTPS
- ⚠️ Only accesses official Tencent Cloud API endpoint (wsa.tencentcloudapi.com)

### 4. Configuration File Permissions

On Linux/macOS systems, set file access permissions:

```bash
chmod 600 config.json
```

This ensures only the file owner can read and modify the configuration file.

## Verify Configuration

After configuration is complete, you can verify the configuration by running a test command:

```bash
python scripts/tencent_hotsearch.py test -l 1 --print
```

If the configuration is correct, you should see search results. If errors occur, please check:

1. Whether SecretId and SecretKey are correctly filled
2. Whether the network connection is normal
3. Whether the Tencent Cloud account has activated the Online Search service
4. Whether the API key has sufficient permissions

## Output Directory Configuration

You can configure the default output directory in `config.json`:

```json
{
  "secret_id": "AKIDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "secret_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "output_dir": "/path/to/your/search_results"
}
```

The following path formats are supported:
- **Relative paths**: `./output`, `../results`, `search_output`
- **Absolute paths**: `/path/to/your/search_results`, `C:\Users\yourname\Documents\search_results`

If `output_dir` is not specified, `./output` is used by default.

## Frequently Asked Questions

### Q1: Where can I view SecretId and SecretKey?

A: Visit [Tencent Cloud Access Management Console](https://console.cloud.tencent.com/cam/capi), click "Create Key" to obtain. Note that SecretKey is only displayed once, please save it properly.

### Q2: What if I forgot to save SecretKey?

A: You can delete the old key and create a new one. Visit [Access Management Console](https://console.cloud.tencent.com/cam/capi), delete the old key and create a new one.

### Q3: API call fails with authentication error?

A: Please check:
- Whether SecretId and SecretKey are correctly copied (note no extra spaces)
- Whether SecretId starts with AKID
- Whether the account has sufficient balance or free quota
- Whether the account has activated the Online Search service

### Q4: How to view API call count and charges?

A: Visit [Tencent Cloud Expense Center](https://console.cloud.tencent.com/expense/bill) to view detailed call records and charge information.

### Q5: What is the free quota?

A: Tencent Cloud Online Search API provides a certain amount of free calls. Please refer to the official documentation for the specific quota. After exceeding the free quota, you will be charged based on actual usage.

### Q6: How to improve API call speed?

A:
- Optimize network connection
- Use CDN acceleration
- Set concurrent requests reasonably

### Q7: What happens if the output directory does not exist?

A: The program will automatically create the output directory (including all parent directories), no manual creation required.

### Q8: Can I specify both output path and output format?

A: Yes. Use the `-o` parameter to specify the output path and the `-f` parameter to specify the output format. For example:

```bash
python scripts/tencent_hotsearch.py "AI" -o results.json -f json
```

## Related Links

- [Tencent Cloud Online Search Product Page](https://cloud.tencent.com/product/ais)
- [Tencent Cloud Online Search API Documentation](https://cloud.tencent.com/document/product/1139/46888)
- [Tencent Cloud Access Management Console](https://console.cloud.tencent.com/cam/capi)
- [Tencent Cloud Online Search Console](https://console.cloud.tencent.com/ais)
- [Tencent Cloud Expense Center](https://console.cloud.tencent.com/expense/bill)

## Technical Support

If you encounter issues during configuration:

1. Check [Tencent Cloud Documentation Center](https://cloud.tencent.com/document/product)
2. Submit a ticket via [Ticket System](https://console.cloud.tencent.com/workorder)
3. Contact Tencent Cloud technical support

---

**Last Updated**: 2024
