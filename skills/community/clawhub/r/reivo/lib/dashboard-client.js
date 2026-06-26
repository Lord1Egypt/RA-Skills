const DASHBOARD_API = "https://app.reivo.dev/api/v1";

class DashboardClient {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseUrl = DASHBOARD_API;
  }

  _headers() {
    return {
      Authorization: `Bearer ${this.apiKey}`,
      "Content-Type": "application/json",
    };
  }

  async get(path) {
    const res = await fetch(`${this.baseUrl}${path}`, {
      headers: this._headers(),
    });
    if (!res.ok) {
      throw new Error(`API error: ${res.status} ${res.statusText}`);
    }
    return await res.json();
  }

  async post(path, body) {
    const res = await fetch(`${this.baseUrl}${path}`, {
      method: "POST",
      headers: this._headers(),
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`API error: ${res.status} ${text}`);
    }
    return await res.json();
  }
}

module.exports = { DashboardClient, DASHBOARD_API };
