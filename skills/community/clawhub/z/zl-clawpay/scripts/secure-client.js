'use strict';

const axios = require('axios');
const { GmStrategy } = require('./crypto/gm-strategy');
const config = require('./config');

class SecureClient {
  constructor(apiKey, memory) {
    this.apiKey = apiKey;
    this.memory = memory;
    this.baseUrl = config.getApiUrl();
    this.strategy = null;

    if (apiKey) {
      this.strategy = this._initStrategy();
    }
  }

  _initStrategy() {
    const serverPublicKey = config.getServerPublicKey();
    if (!this.apiKey) throw new Error('api_key not set');
    if (!serverPublicKey) throw new Error('Server public key not configured');
    return new GmStrategy(this.apiKey, serverPublicKey, this.memory);
  }

  async secureRequest(method, endpoint, interfaceId, body, seqId, appIdOverride, extraFields) {
    if (!this.strategy) throw new Error('Strategy not initialized');

    const reqBody = this.strategy.buildRequestBody(body || {}, interfaceId, seqId, appIdOverride, extraFields);
    const headers = this.strategy.buildRequestHeaders(endpoint, interfaceId);

    const url = `${this.baseUrl.replace(/\/$/, '')}/${endpoint.replace(/^\//, '')}`;

    const response = await axios({
      method: method.toUpperCase(),
      url,
      data: reqBody,
      headers,
      timeout: 30000,
      validateStatus: () => true
    });

    if (response.status !== 200) {
      const errMsg = response.data
        ? (typeof response.data === 'string' ? response.data : JSON.stringify(response.data))
        : response.statusText;
      throw new Error(`HTTP ${response.status}: ${errMsg}`);
    }

    return this.strategy.processResponse(response.data);
  }
}

module.exports = { SecureClient };
