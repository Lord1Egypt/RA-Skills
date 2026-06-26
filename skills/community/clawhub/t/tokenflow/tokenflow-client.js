/**
 * TokenFlow Client
 * Reference implementation for agent skill integration
 *
 * Usage: import { TokenFlowClient } from './tokenflow-client.js'
 */

import { loadConfig, saveConfig, getFiletypeBehavior } from './config.js';

export class TokenFlowClient {
  constructor(apiKey, baseUrl = 'https://tokenflow.fly.dev') {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  /**
   * Convert a file to structured text
   * @param {File|Blob} file - The file to convert
   * @param {Object} options - Conversion options
   * @param {string} options.sheets - For XLSX: 'all' or comma-separated sheet names
   * @param {string} options.outputFormat - 'html' or 'markdown' (default: 'markdown')
   * @returns {Promise<string|Object>} Text content or multi-sheet results
   */
  async convert(file, options = {}) {
    const formData = new FormData();
    formData.append('file', file);

    if (options.sheets) {
      formData.append('sheets', options.sheets);
    }

    const outputFormat = options.outputFormat || 'markdown';
    formData.append('output_format', outputFormat);

    const response = await fetch(`${this.baseUrl}/convert`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
      },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`TokenFlow conversion failed: ${response.status} ${error}`);
    }

    const contentType = response.headers.get('content-type') || '';

    if (contentType.includes('application/json')) {
      return await response.json();
    }

    return await response.text();
  }

  /**
   * Preview XLSX sheet names without converting
   * @param {File|Blob} file - XLSX file
   * @returns {Promise<{filename: string, sheets: string[]}>}
   */
  async preview(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/convert/preview`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Preview failed: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Check API health and features
   * @returns {Promise<Object>}
   */
  async health() {
    const response = await fetch(`${this.baseUrl}/health`);
    return await response.json();
  }

  /**
   * Get current usage statistics
   * @returns {Promise<Object>}
   */
  async usage() {
    const response = await fetch(`${this.baseUrl}/usage`, {
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Usage check failed: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Get billing summary (read-only, no session creation)
   * @returns {Promise<{tier: string, status: string, quota_used: number, quota_limit: number, remaining: number, current_period_end: string|null, reset_date: string}>}
   */
  async billingSummary() {
    const response = await fetch(`${this.baseUrl}/billing/summary`, {
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Billing summary failed: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Convert a URL to structured text
   * @param {string} url - The URL to convert
   * @returns {Promise<{markdown: string, output_tokens: number}>}
   */
  async convertUrl(url) {
    const response = await fetch(`${this.baseUrl}/convert/url`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`URL conversion failed: ${response.status} ${error}`);
    }

    return await response.json();
  }

  /**
   * Sign up with email/password (CLI auth)
   * @param {string} email
   * @param {string} password
   * @returns {Promise<{api_key: string, user_id: string, email: string}>}
   */
  async signup(email, password) {
    const response = await fetch(`${this.baseUrl}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(`Signup failed: ${data.detail || response.statusText}`);
    }
    this.apiKey = data.api_key;
    saveConfig({ apiKey: data.api_key });
    return data;
  }

  /**
   * Sign in with email/password (CLI auth)
   * @param {string} email
   * @param {string} password
   * @returns {Promise<{api_key: string, user_id: string, email: string}>}
   */
  async signin(email, password) {
    const response = await fetch(`${this.baseUrl}/auth/signin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(`Signin failed: ${data.detail || response.statusText}`);
    }
    this.apiKey = data.api_key;
    saveConfig({ apiKey: data.api_key });
    return data;
  }

  /**
   * Check current quota usage
   * @returns {Promise<{quota_used: number, quota_limit: number, tier: string}>}
   */
  async checkQuota() {
    return this.usage();
  }

  /**
   * Check if file type is supported
   * @param {string} filename - Filename with extension
   * @returns {boolean}
   */
  isSupported(filename) {
    const ext = filename.split('.').pop()?.toLowerCase();
    const supported = [
      'pdf', 'docx', 'xlsx', 'pptx', 'html', 'htm',
      'csv', 'json', 'xml', 'txt', 'md',
      'wav', 'mp3', 'ogg', 'flac', 'm4a',
      'zip'
    ];
    return supported.includes(ext);
  }
}

/**
 * Agent-side file processing with user preferences
 */
export class TokenFlowAgent {
  constructor(client, preferences = {}) {
    this.client = client;

    // Auto-load saved preferences if none explicitly provided
    const saved = Object.keys(preferences).length === 0 ? loadConfig() : {};

    this.prefs = {
      outputFormat: preferences.outputFormat || saved.outputFormat || 'markdown',
      maxRetries: parseInt(preferences.maxRetries) || saved.maxRetries || 1,
      fallbackBehavior: preferences.fallbackBehavior || saved.fallbackBehavior || 'use_file',
      ...preferences
    };
  }

  /**
   * Process a file attachment based on user preferences
   * @param {File} file - The attached file
   * @param {boolean} explicitRequest - Whether user explicitly asked to convert
   * @returns {Promise<{content: string, source: string, success: boolean, shouldAsk?: boolean}>}
   */
  async processFile(file, explicitRequest = false) {
    // Check if supported
    if (!this.client.isSupported(file.name)) {
      return { content: null, source: 'original', success: true };
    }

    // Check filetype behavior
    const behavior = getFiletypeBehavior(file.name);

    if (behavior.action === 'skip') {
      return { content: null, source: 'original', success: true };
    }

    if (behavior.askEachTime && !explicitRequest) {
      return { content: null, source: 'original', success: true, shouldAsk: true };
    }

    // XLSX sheet handling
    let sheets = null;
    const ext = file.name.split('.').pop()?.toLowerCase();
    if (ext === 'xlsx' || ext === 'xls') {
      try {
        const preview = await this.client.preview(file);
        if (preview.sheets && preview.sheets.length > 1) {
          sheets = 'all';
        }
      } catch (e) {
        // Preview failed, proceed without sheets
      }
    }

    // Attempt conversion with retries
    let lastError = null;
    for (let attempt = 0; attempt <= this.prefs.maxRetries; attempt++) {
      try {
        const result = await this.client.convert(file, {
          sheets,
          outputFormat: this.prefs.outputFormat,
        });

        // Extract content from response
        let content = '';
        if (typeof result === 'string') {
          content = result;
        } else if (result.markdown) {
          content = result.markdown;
        } else if (result.html) {
          content = result.html;
        } else if (Array.isArray(result.markdown)) {
          content = result.markdown.map(r => `## ${r.sheet_name}\n\n${r.markdown}`).join('\n\n---\n\n');
        }

        if (!content || content.trim().length === 0) {
          throw new Error('Empty conversion result');
        }

        return { content, source: 'tokenflow', success: true };
      } catch (error) {
        lastError = error;
        if (attempt < this.prefs.maxRetries) {
          await new Promise(r => setTimeout(r, 1000));
        }
      }
    }

    // All retries exhausted
    if (this.prefs.fallbackBehavior === 'fail') {
      throw new Error(`TokenFlow conversion failed after ${this.prefs.maxRetries + 1} attempts: ${lastError.message}`);
    }

    // Check for quota exceeded
    const isQuotaError = lastError.message && (
      lastError.message.includes('quota') ||
      lastError.message.includes('429') ||
      lastError.message.includes('rate limit')
    );

    // Fallback: use original file
    return {
      content: null,
      source: 'original',
      success: false,
      error: lastError.message,
      quotaExceeded: isQuotaError,
      upgradeUrl: isQuotaError ? 'https://tokenflow.fly.dev' : undefined,
    };
  }
}

export default TokenFlowClient;
