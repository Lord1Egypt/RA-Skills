/**
 * WeCom Group Notification Skill for OpenClaw
 * 
 * Function: Send notifications to group chats via WeCom robot Webhook
 * Supports: text, images (Markdown format), and Markdown rich text
 * 
 * Usage:
 * 1. Call in OpenClaw: openclaw skill qywx-notify send --webhook <url> --content <text> [--image <url>]
 * 2. Call in code: await skill.send({webhook: url, content: text, image: url})
 * 
 * Configuration example (openclaw.yaml):
 * skills:
 *   qywx-notify:
 *     enabled: true
 *     defaultWebhook: "your-webhook-url"
 *     timeout: 10000
 */

const axios = require('axios');

class QywxNotifySkill {
  constructor(config = {}) {
    this.name = 'qywx-notify';
    this.label = 'WeCom Group Notification';
    this.version = '1.0.0';
    
    // Configuration
    this.config = {
      enabled: config.enabled !== false,
      defaultWebhook: config.defaultWebhook || '',
      timeout: config.timeout || 10000,
      retryCount: config.retryCount || 3,
      retryDelay: config.retryDelay || 1000,
      ...config
    };
    
    // HTTP client
    this.httpClient = axios.create({
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'OpenClaw-Qywx-Notify/1.0.0'
      }
    });
    
    this.log(`Skill initialized with config: ${JSON.stringify(this.config, null, 2)}`);
  }
  
  /**
   * Send notification to WeCom group
   * @param {Object} params - Parameter object
   * @param {string} params.webhook - WeCom robot Webhook URL
   * @param {string} params.content - Notification content (supports Markdown)
   * @param {string} [params.image] - Image URL (optional)
   * @param {string} [params.title] - Message title (optional)
   * @param {string} [params.msgtype] - Message type: text|markdown (default: text)
   * @param {boolean} [params.mentionAll] - Whether to @all (default: false)
   * @param {Array} [params.mentionedList] - List of user IDs to @mention
   * @param {Array} [params.mentionedMobileList] - List of user mobile numbers to @mention
   * @returns {Promise<Object>} Send result
   */
  async send(params = {}) {
    try {
      // Parameter validation
      const validated = this._validateParams(params);
      
      // Build request data
      const requestData = this._buildRequestData(validated);
      
      // Send request
      const result = await this._sendRequest(validated.webhook, requestData);
      
      this.log(`Notification sent successfully: ${validated.content.substring(0, 50)}...`);
      return {
        success: true,
        message: 'Notification sent successfully',
        data: result.data,
        request: {
          webhook: this._maskWebhook(validated.webhook),
          content: validated.content,
          image: validated.image
        }
      };
      
    } catch (error) {
      this.error('Failed to send notification:', error.message);
      return {
        success: false,
        message: `Send failed: ${error.message}`,
        error: error.response?.data || error.message,
        request: params
      };
    }
  }
  
  /**
   * validate parameters
   * @private
   */
  _validateParams(params) {
    const webhook = params.webhook || this.config.defaultWebhook;
    if (!webhook) {
      throw new Error('Missing Webhook URL. Please provide the webhook parameter or configure defaultWebhook.');
    }
    
    if (!params.content || params.content.trim() === '') {
      throw new Error('Notification content cannot be empty.');
    }
    
    // Validate Webhook URL format
    if (!this._isValidUrl(webhook)) {
      throw new Error(`Invalid Webhook URL: ${webhook}`);
    }
    
    return {
      webhook: webhook.trim(),
      content: params.content.trim(),
      image: params.image ? params.image.trim() : null,
      title: params.title ? params.title.trim() : null,
      msgtype: params.msgtype || 'text',
      mentionAll: params.mentionAll || false,
      mentionedList: params.mentionedList || [],
      mentionedMobileList: params.mentionedMobileList || []
    };
  }
  
  /**
   * build request data based on message type and content
   * @private
   */
  _buildRequestData(params) {
    const { content, image, title, msgtype, mentionAll, mentionedList, mentionedMobileList } = params;
    
    let messageContent = content;
    
    // If image is provided, append to content
    if (image) {
      messageContent += `\n\n![image](${image})`;
    }
    
    // Build base message
    const baseMessage = {
      msgtype: msgtype
    };
    
    // Build different message structures based on message type
    if (msgtype === 'markdown') {
      baseMessage.markdown = {
        content: messageContent
      };
      
      // If title is provided, prepend to markdown
      if (title) {
        baseMessage.markdown.content = `# ${title}\n\n${messageContent}`;
      }
    } else {
      // Default text type
      baseMessage.text = {
        content: messageContent,
        mentioned_list: mentionAll ? ['@all'] : mentionedList,
        mentioned_mobile_list: mentionedMobileList
      };
    }
    
    return baseMessage;
  }
  
  /**
   * send request with retry logic
   * @private
   */
  async _sendRequest(webhook, data, retry = 0) {
    try {
      this.log(`Sending request to: ${this._maskWebhook(webhook)}`);
      this.log(`Request data: ${JSON.stringify(data, null, 2)}`);
      
      const response = await this.httpClient.post(webhook, data);
      
      // Check WeCom response error codes (supports two formats)
      if (response.data) {
        // Format 1: {"success":true,"message":"Message received","data":{}}
        if (response.data.success === false) {
          const errorMsg = `WeCom API error: ${response.data.message || 'Unknown error'}`;
          throw new Error(errorMsg);
        }
        // Format 2: {"errcode":0,"errmsg":"ok"}
        else if (response.data.errcode !== undefined && response.data.errcode !== 0) {
          const errorMsg = `WeCom API error: ${response.data.errmsg || 'Unknown error'} (code: ${response.data.errcode})`;
          throw new Error(errorMsg);
        }
        // Format 3: No success field and no errcode field (default success)
      }
      
      return response;
      
    } catch (error) {
      // Retry logic
      if (retry < this.config.retryCount) {
        const delay = this.config.retryDelay * Math.pow(2, retry);
        this.log(`Request failed, retrying in ${delay}ms (${retry + 1}/${this.config.retryCount}): ${error.message}`);
        
        await this._sleep(delay);
        return this._sendRequest(webhook, data, retry + 1);
      }
      
      throw error;
    }
  }
  
  /**
   * vialidate URL format
   * @private
   */
  _isValidUrl(url) {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  }
  
  /**
   * Mask sensitive information in the Webhook URL
   * @private
   */
  _maskWebhook(url) {
    try {
      const urlObj = new URL(url);
      const pathParts = urlObj.pathname.split('/');
      
      // Mask bot token
      if (pathParts.length > 0) {
        const lastPart = pathParts[pathParts.length - 1];
        if (lastPart.length > 8) {
          pathParts[pathParts.length - 1] = lastPart.substring(0, 8) + '...';
        }
      }
      
      urlObj.pathname = pathParts.join('/');
      return urlObj.toString();
    } catch {
      return 'invalid-url';
    }
  }
  
  /**
   * Sleep utility
   * @private
   */
  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  /**
   * Log utility
   * @private
   */
  log(...args) {
    console.log(`[QywxNotifySkill]`, ...args);
  }
  
  /**
   * Error log utility
   * @private
   */
  error(...args) {
    console.error(`[QywxNotifySkill]`, ...args);
  }
  
  /**
   * Skill command handler
   * Supports OpenClaw CLI invocation
   */
  async handleCommand(command, args = {}) {
    switch (command) {
      case 'send':
        return await this.send(args);
        
      case 'test':
        return await this._testConnection(args);
        
      case 'config':
        return {
          success: true,
          config: this.config,
          maskedWebhook: this.config.defaultWebhook ? this._maskWebhook(this.config.defaultWebhook) : null
        };
        
      default:
        return {
          success: false,
          message: `Unknown command: ${command}`,
          availableCommands: ['send', 'test', 'config']
        };
    }
  }
  
  /**
   * Test connection by sending a test message
   * @private
   */
  async _testConnection(params = {}) {
    const webhook = params.webhook || this.config.defaultWebhook;
    
    if (!webhook) {
      return {
        success: false,
        message: 'Please provide a Webhook URL or configure defaultWebhook.'
      };
    }
    
    try {
      // Send test message
      const testContent = `Test notification - ${new Date().toLocaleString()}\n\nThis is a test message from OpenClaw.`;
      
      const result = await this.send({
        webhook: webhook,
        content: testContent,
        title: 'OpenClaw Test Notification'
      });
      
      return {
        success: true,
        message: 'Connection test successful',
        webhook: this._maskWebhook(webhook),
        testResult: result
      };
      
    } catch (error) {
      return {
        success: false,
        message: 'Connection test failed',
        webhook: this._maskWebhook(webhook),
        error: error.message
      };
    }
  }
  
  /**
   * Get skill information for OpenClaw
   */
  getInfo() {
    return {
      name: this.name,
      label: this.label,
      version: this.version,
      description: 'WeCom Group Notification Skill - Send notifications to WeCom group chats via Webhook',
      capabilities: ['text', 'images', 'markdown', 'notifications'],
      config: {
        hasDefaultWebhook: !!this.config.defaultWebhook,
        timeout: this.config.timeout,
        retryCount: this.config.retryCount
      },
      usage: {
        command: 'openclaw skill qywx-notify send --webhook <url> --content <text> [--image <url>]',
        example: 'openclaw skill qywx-notify send --webhook "https://..." --content "Hello World" --image "https://example.com/image.jpg"'
      }
    };
  }
}

module.exports = QywxNotifySkill;