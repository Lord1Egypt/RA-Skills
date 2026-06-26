const BASE_URL = "https://proxy.reivo.dev";

class ProxyClient {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseUrl = BASE_URL;
  }

  _headers() {
    return {
      Authorization: `Bearer ${this.apiKey}`,
      "Content-Type": "application/json",
    };
  }

  async checkHealth() {
    const res = await fetch(`${this.baseUrl}/health`, {
      headers: this._headers(),
    });
    if (!res.ok) {
      throw new Error(`Health check failed: ${res.status} ${res.statusText}`);
    }
    return await res.json();
  }
}

module.exports = { ProxyClient, BASE_URL };
