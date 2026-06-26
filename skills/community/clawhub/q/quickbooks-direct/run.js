#!/usr/bin/env node

/**
 * QuickBooks API Skill for OpenClaw
 * 
 * This skill provides comprehensive QuickBooks Online API integration
 * Supports: OAuth2, Invoices, Customers, Items, Payments, Reports, and more
 * 
 * Usage: node run.js <tool_name> <json_params>
 * Example: node run.js qb_create_customer '{"DisplayName":"John Doe"}'
 */

import axios from 'axios';
import { promises as fs } from 'fs';
import path from 'path';
import express from 'express';
import open from 'open';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

// ES module equivalents for __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Configuration
const CONFIG_FILE = path.join(__dirname, 'config.json');
const QB_AUTH_URL = 'https://appcenter.intuit.com/connect/oauth2';
const QB_TOKEN_URL = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer';
const QB_REFRESH_URL = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer';

// QuickBooks API Client
class QuickBooksClient {
  constructor() {
    this.config = null;
    this.accessToken = null;
    this.refreshToken = null;
    this.realmId = null;
    this.tokenExpiry = null;
  }

  async loadConfig() {
    try {
      const data = await fs.readFile(CONFIG_FILE, 'utf8');
      this.config = JSON.parse(data);
      this.accessToken = this.config.access_token;
      this.refreshToken = this.config.refresh_token;
      this.realmId = this.config.realm_id;
      this.tokenExpiry = this.config.token_expiry;
      
      // Set API base URL based on environment
      const apiEnv = this.config.api_environment || 'sandbox';
      this.apiBase = apiEnv === 'production'
        ? 'https://quickbooks.api.intuit.com/v3/company'
        : 'https://sandbox-quickbooks.api.intuit.com/v3/company';
      
      return true;
    } catch (error) {
      return false;
    }
  }

  async saveConfig() {
    const config = {
      client_id: this.config.client_id,
      client_secret: this.config.client_secret,
      redirect_uri: this.config.redirect_uri,
      api_environment: this.config.api_environment || 'sandbox',
      access_token: this.accessToken,
      refresh_token: this.refreshToken,
      realm_id: this.realmId,
      token_expiry: this.tokenExpiry,
    };
    await fs.writeFile(CONFIG_FILE, JSON.stringify(config, null, 2));
  }

  async refreshAccessToken() {
    if (Date.now() < this.tokenExpiry - 300000) {
      return; // Token still valid for at least 5 minutes
    }

    const auth = Buffer.from(
      `${this.config.client_id}:${this.config.client_secret}`
    ).toString('base64');

    const response = await axios.post(
      QB_REFRESH_URL,
      new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: this.refreshToken,
      }),
      {
        headers: {
          Authorization: `Basic ${auth}`,
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );

    this.accessToken = response.data.access_token;
    this.refreshToken = response.data.refresh_token;
    this.tokenExpiry = Date.now() + response.data.expires_in * 1000;
    await this.saveConfig();
  }

  async request(method, endpoint, data = null) {
    if (!this.accessToken) {
      throw new Error('Not authenticated. Please run qb_authenticate first.');
    }

    await this.refreshAccessToken();

    const url = `${this.apiBase}/${this.realmId}/${endpoint}`;
    const config = {
      method,
      url,
      headers: {
        Authorization: `Bearer ${this.accessToken}`,
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      params: {
        minorversion: 65
      }
    };

    if (data) {
      config.data = data;
    }

    try {
      const response = await axios(config);
      return response.data;
    } catch (error) {
      if (error.response) {
        console.error('API Error:', JSON.stringify({
          status: error.response.status,
          statusText: error.response.statusText,
          url: url,
          fault: error.response.data?.fault
        }, null, 2));
      }
      throw error;
    }
  }

  async authenticate(clientId, clientSecret) {
    this.config = {
      client_id: clientId,
      client_secret: clientSecret,
      redirect_uri: 'http://localhost:3001/callback',
    };

    const authUrl = `${QB_AUTH_URL}?` +
      `client_id=${clientId}&` +
      `redirect_uri=${encodeURIComponent(this.config.redirect_uri)}&` +
      `response_type=code&` +
      `scope=com.intuit.quickbooks.accounting&` +
      `state=randomstate`;

    return new Promise((resolve, reject) => {
      const app = express();
      const server = app.listen(3001);

      app.get('/callback', async (req, res) => {
        try {
          const code = req.query.code;
          const realmId = req.query.realmId;

          const auth = Buffer.from(`${clientId}:${clientSecret}`).toString('base64');
          const tokenResponse = await axios.post(
            QB_TOKEN_URL,
            new URLSearchParams({
              grant_type: 'authorization_code',
              code: code,
              redirect_uri: this.config.redirect_uri,
            }),
            {
              headers: {
                Authorization: `Basic ${auth}`,
                'Content-Type': 'application/x-www-form-urlencoded',
              },
            }
          );

          this.accessToken = tokenResponse.data.access_token;
          this.refreshToken = tokenResponse.data.refresh_token;
          this.realmId = realmId;
          this.tokenExpiry = Date.now() + tokenResponse.data.expires_in * 1000;

          await this.saveConfig();

          res.send('<h1>Authentication successful!</h1><p>You can close this window.</p>');
          server.close();
          resolve({ success: true, realm_id: realmId });
        } catch (error) {
          server.close();
          reject(error);
        }
      });

      open(authUrl);
    });
  }

  // API Methods
  async getCompanyInfo() {
    return await this.request('GET', 'companyinfo/' + this.realmId);
  }

  async createCustomer(data) {
    return await this.request('POST', 'customer', data);
  }

  async createVendor(data) {
    return await this.request('POST', 'vendor', data);
  }

  async createItem(data) {
    return await this.request('POST', 'item', data);
  }

  async createInvoice(data) {
    return await this.request('POST', 'invoice', data);
  }

  async createPayment(data) {
    return await this.request('POST', 'payment', data);
  }

  async createBill(data) {
    return await this.request('POST', 'bill', data);
  }

  async createEstimate(data) {
    return await this.request('POST', 'estimate', data);
  }

  async createPurchaseOrder(data) {
    return await this.request('POST', 'purchaseorder', data);
  }

  async createSalesReceipt(data) {
    return await this.request('POST', 'salesreceipt', data);
  }

  async query(query) {
    const encoded = encodeURIComponent(query);
    return await this.request('GET', `query?query=${encoded}`);
  }

  async getReport(reportName, params = {}) {
    const queryString = Object.entries(params)
      .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
      .join('&');
    return await this.request('GET', `reports/${reportName}?${queryString}`);
  }

  async sendInvoice(invoiceId, email) {
    return await this.request('POST', `invoice/${invoiceId}/send?sendTo=${encodeURIComponent(email)}`);
  }

  async updateInvoice(id, data) {
    return await this.request('POST', 'invoice', { ...data, Id: id });
  }

  async updateCustomer(id, data) {
    return await this.request('POST', 'customer', { ...data, Id: id });
  }

  async updateItem(id, data) {
    return await this.request('POST', 'item', { ...data, Id: id });
  }
}

// Tool Handlers
const tools = {
  async qb_authenticate(params) {
    const client = new QuickBooksClient();
    const result = await client.authenticate(params.client_id, params.client_secret);
    return result;
  },

  async qb_get_company_info(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.getCompanyInfo();
  },

  async qb_create_customer(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.createCustomer(params);
  },

  async qb_query_customers(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    const query = params.query || 'SELECT * FROM Customer MAXRESULTS 100';
    return await client.query(query);
  },

  async qb_create_vendor(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.createVendor(params);
  },

  async qb_create_item(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.createItem(params);
  },

  async qb_query_items(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    const query = params.query || 'SELECT * FROM Item MAXRESULTS 100';
    return await client.query(query);
  },

  async qb_create_invoice(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.createInvoice(params);
  },

  async qb_query_invoices(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    const query = params.query || 'SELECT * FROM Invoice MAXRESULTS 100';
    return await client.query(query);
  },

  async qb_send_invoice(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.sendInvoice(params.invoice_id, params.email);
  },

  async qb_update_invoice(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.updateInvoice(params.id, params.data);
  },

  async qb_create_payment(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.createPayment(params);
  },

  async qb_query_payments(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    const query = params.query || 'SELECT * FROM Payment MAXRESULTS 100';
    return await client.query(query);
  },

  async qb_create_bill(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.createBill(params);
  },

  async qb_query_bills(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    const query = params.query || 'SELECT * FROM Bill MAXRESULTS 100';
    return await client.query(query);
  },

  async qb_create_estimate(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.createEstimate(params);
  },

  async qb_create_purchase_order(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.createPurchaseOrder(params);
  },

  async qb_create_sales_receipt(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.createSalesReceipt(params);
  },

  async qb_query(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.query(params.query);
  },

  async qb_query_accounts(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    const query = params.query || 'SELECT * FROM Account MAXRESULTS 100';
    return await client.query(query);
  },

  async qb_get_profit_loss(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.getReport('ProfitAndLoss', params);
  },

  async qb_get_balance_sheet(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.getReport('BalanceSheet', params);
  },

  async qb_get_cash_flow(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.getReport('CashFlow', params);
  },

  async qb_get_aged_receivables(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.getReport('AgedReceivables', params);
  },

  async qb_get_aged_payables(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.getReport('AgedPayables', params);
  },

  async qb_update_customer(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.updateCustomer(params.id, params.data);
  },

  async qb_update_item(params) {
    const client = new QuickBooksClient();
    await client.loadConfig();
    return await client.updateItem(params.id, params.data);
  },
};

// Main CLI Handler
async function main() {
  try {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
      console.log(JSON.stringify({
        error: 'Usage: node run.js <tool_name> <json_params>',
        example: 'node run.js qb_get_company_info "{}"'
      }, null, 2));
      process.exit(1);
    }

    const toolName = args[0];
    const params = args[1] ? JSON.parse(args[1]) : {};

    if (!tools[toolName]) {
      console.log(JSON.stringify({
        error: `Unknown tool: ${toolName}`,
        available_tools: Object.keys(tools)
      }, null, 2));
      process.exit(1);
    }

    const result = await tools[toolName](params);
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
  } catch (error) {
    console.log(JSON.stringify({
      error: error.message,
      stack: error.stack
    }, null, 2));
    process.exit(1);
  }
}

main();
