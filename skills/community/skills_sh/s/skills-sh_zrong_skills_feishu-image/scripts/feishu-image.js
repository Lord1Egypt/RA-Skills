/**
 * Feishu Image Sender
 * Send images via Feishu (Lark) API
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

class FeishuImageError extends Error {
  constructor(message, code, details = {}) {
    super(message);
    this.name = 'FeishuImageError';
    this.code = code;
    this.details = details;
  }
}

class FeishuImage {
  constructor(config = {}) {
    this.appId = config.appId || process.env.FEISHU_APP_ID;
    this.appSecret = config.appSecret || process.env.FEISHU_APP_SECRET;
    this.baseUrl = config.baseUrl || 'https://open.feishu.cn/open-apis';
    this.tokenCache = null;
    this.tokenExpiry = null;
  }

  /**
   * Make an HTTP request
   */
  async _request(url, options = {}) {
    return new Promise((resolve, reject) => {
      const parsedUrl = new URL(url);
      const requestOptions = {
        hostname: parsedUrl.hostname,
        port: parsedUrl.port || 443,
        path: parsedUrl.pathname + parsedUrl.search,
        method: options.method || 'GET',
        headers: options.headers || {}
      };

      const req = https.request(requestOptions, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            resolve({ statusCode: res.statusCode, data: json });
          } catch (e) {
            resolve({ statusCode: res.statusCode, data });
          }
        });
      });

      req.on('error', reject);

      if (options.body) {
        req.write(options.body);
      }

      req.end();
    });
  }

  /**
   * Get tenant access token
   */
  async getTenantToken() {
    // Check cache
    if (this.tokenCache && this.tokenExpiry && Date.now() < this.tokenExpiry) {
      return this.tokenCache;
    }

    if (!this.appId || !this.appSecret) {
      throw new FeishuImageError(
        'Missing credentials. Set FEISHU_APP_ID and FEISHU_APP_SECRET environment variables.',
        'MISSING_CREDENTIALS'
      );
    }

    const url = `${this.baseUrl}/auth/v3/tenant_access_token/internal`;
    const response = await this._request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        app_id: this.appId,
        app_secret: this.appSecret
      })
    });

    if (response.data.code !== 0) {
      throw new FeishuImageError(
        `Authentication failed: ${response.data.msg}`,
        'AUTH_FAILED',
        { code: response.data.code }
      );
    }

    this.tokenCache = response.data.tenant_access_token;
    // Token expires in 2 hours, cache for 1.5 hours to be safe
    this.tokenExpiry = Date.now() + (1.5 * 60 * 60 * 1000);

    return this.tokenCache;
  }

  /**
   * Upload image to Feishu
   */
  async uploadImage(imagePath) {
    if (!fs.existsSync(imagePath)) {
      throw new FeishuImageError(
        `Image file not found: ${imagePath}`,
        'FILE_NOT_FOUND'
      );
    }

    const token = await this.getTenantToken();
    const imageData = fs.readFileSync(imagePath);
    const boundary = '----FeishuFormBoundary' + Date.now();

    // Build multipart form data
    const formData = Buffer.concat([
      Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="image_type"\r\n\r\nmessage\r\n`),
      Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="image"; filename="${path.basename(imagePath)}"\r\nContent-Type: image/png\r\n\r\n`),
      imageData,
      Buffer.from(`\r\n--${boundary}--\r\n`)
    ]);

    const url = `${this.baseUrl}/im/v1/images`;
    const response = await this._request(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': `multipart/form-data; boundary=${boundary}`
      },
      body: formData
    });

    if (response.data.code !== 0) {
      throw new FeishuImageError(
        `Upload failed: ${response.data.msg}`,
        'UPLOAD_FAILED',
        { code: response.data.code }
      );
    }

    return response.data.data.image_key;
  }

  /**
   * Send image message
   */
  async sendImage(options) {
    const {
      imagePath,
      receiveId,
      receiveType = 'user',
      text
    } = options;

    if (!imagePath || !receiveId) {
      throw new FeishuImageError(
        'Missing required parameters: imagePath and receiveId',
        'MISSING_PARAMS'
      );
    }

    // Upload image first
    const imageKey = await this.uploadImage(imagePath);
    const token = await this.getTenantToken();

    // Determine receive_id_type
    const idType = receiveType === 'chat' ? 'chat_id' : 'open_id';

    // Build message content
    const content = JSON.stringify({ image_key: imageKey });

    // If there's text, send as post message with image and text
    if (text) {
      const url = `${this.baseUrl}/im/v1/messages?receive_id_type=${idType}`;
      const response = await this._request(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          receive_id: receiveId,
          msg_type: 'post',
          content: JSON.stringify({
            zh_cn: {
              title: text,
              content: [
                [{ tag: 'img', image_key: imageKey }]
              ]
            }
          })
        })
      });

      if (response.data.code !== 0) {
        throw new FeishuImageError(
          `Send failed: ${response.data.msg}`,
          'SEND_FAILED',
          { code: response.data.code }
        );
      }

      return response.data.data.message_id;
    }

    // Send image-only message
    const url = `${this.baseUrl}/im/v1/messages?receive_id_type=${idType}`;
    const response = await this._request(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        receive_id: receiveId,
        msg_type: 'image',
        content: content
      })
    });
    if (response.data.code !== 0) {
      throw new FeishuImageError(
        `Send failed: ${response.data.msg}`,
        'SEND_FAILED',
        { code: response.data.code }
      );
    }

    return response.data.data.message_id;
  }
}

module.exports = { FeishuImage, FeishuImageError };
