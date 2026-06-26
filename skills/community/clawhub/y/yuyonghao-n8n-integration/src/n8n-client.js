/**
 * n8n Integration - n8n API Client
 * Interacts with n8n API to trigger workflows and manage executions
 */

const https = require('https');
const http = require('http');
const url = require('url');

class N8nClient {
  constructor(options = {}) {
    this.baseUrl = options.baseUrl || process.env.N8N_BASE_URL || 'http://localhost:5678';
    this.apiKey = options.apiKey || process.env.N8N_API_KEY;
    this.timeout = options.timeout || 30000;
  }

  /**
   * Make HTTP request to n8n API
   */
  request(method, path, data = null) {
    return new Promise((resolve, reject) => {
      const parsedUrl = new url.URL(`${this.baseUrl}${path}`);
      const isHttps = parsedUrl.protocol === 'https:';
      const lib = isHttps ? https : http;

      const options = {
        hostname: parsedUrl.hostname,
        port: parsedUrl.port || (isHttps ? 443 : 80),
        path: parsedUrl.pathname + parsedUrl.search,
        method,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      };

      // Add API key
      if (this.apiKey) {
        options.headers['X-N8N-API-KEY'] = this.apiKey;
      }

      const req = lib.request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(body);
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve(parsed);
            } else {
              reject(new Error(`API error: ${res.statusCode} - ${parsed.message || body}`));
            }
          } catch (error) {
            reject(new Error(`Parse error: ${error.message}`));
          }
        });
      });

      req.on('error', reject);
      req.setTimeout(this.timeout, () => {
        req.destroy(new Error('Request timeout'));
      });

      if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        req.write(JSON.stringify(data));
      }

      req.end();
    });
  }

  /**
   * Trigger a workflow by webhook
   */
  async triggerWorkflow(workflowId, data = {}) {
    return await this.request('POST', `/webhook/${workflowId}`, data);
  }

  /**
   * Get workflow executions
   */
  async getExecutions(workflowId, options = {}) {
    const params = new url.URLSearchParams();
    if (options.limit) params.append('limit', options.limit);
    if (options.offset) params.append('offset', options.offset);
    
    const query = params.toString();
    return await this.request('GET', `/executions?workflowId=${workflowId}${query ? '&' + query : ''}`);
  }

  /**
   * Get execution details
   */
  async getExecution(executionId) {
    return await this.request('GET', `/executions/${executionId}`);
  }

  /**
   * List all workflows
   */
  async listWorkflows() {
    return await this.request('GET', '/workflows');
  }

  /**
   * Get workflow by ID
   */
  async getWorkflow(workflowId) {
    return await this.request('GET', `/workflows/${workflowId}`);
  }

  /**
   * Create or update workflow
   */
  async saveWorkflow(workflow) {
    if (workflow.id) {
      return await this.request('PUT', `/workflows/${workflow.id}`, workflow);
    } else {
      return await this.request('POST', '/workflows', workflow);
    }
  }

  /**
   * Delete workflow
   */
  async deleteWorkflow(workflowId) {
    return await this.request('DELETE', `/workflows/${workflowId}`);
  }

  /**
   * Get credentials
   */
  async listCredentials() {
    return await this.request('GET', '/credentials');
  }

  /**
   * Test connection
   */
  async testConnection() {
    try {
      await this.listWorkflows();
      return {
        success: true,
        message: 'Connected to n8n successfully',
        baseUrl: this.baseUrl
      };
    } catch (error) {
      return {
        success: false,
        message: error.message,
        baseUrl: this.baseUrl
      };
    }
  }
}

module.exports = { N8nClient };
