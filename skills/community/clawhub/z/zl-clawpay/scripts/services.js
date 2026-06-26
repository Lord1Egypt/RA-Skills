'use strict';

const { SecureClient } = require('./secure-client');

const LOG_LEVELS = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3
};

function getLogLevel() {
  const constants = require('./constants');
  const level = process.env[constants.ENV_LOG_LEVEL] || 'info';
  return LOG_LEVELS[level.toLowerCase()] ?? LOG_LEVELS.info;
}

function log(level, message, data) {
  const currentLevel = getLogLevel();
  const targetLevel = LOG_LEVELS[level.toLowerCase()] ?? LOG_LEVELS.info;

  if (targetLevel < currentLevel) return;

  const timestamp = new Date().toISOString();
  const prefix = `[${timestamp}] [${level.toUpperCase()}]`;

  if (data !== undefined) {
    console.log(`${prefix} ${message}`, data);
  } else {
    console.log(`${prefix} ${message}`);
  }
}

function maskApiKey(apiKey) {
  if (!apiKey || apiKey.length < 8) return '***';
  return `${apiKey.slice(0, 4)}***${apiKey.slice(-4)}`;
}

function maskSubWalletId(subWalletId) {
  if (!subWalletId || subWalletId.length < 8) return '***';
  return `${subWalletId.slice(0, 4)}***${subWalletId.slice(-4)}`;
}

class WalletService {
  constructor(memory) {
    this.memory = memory;
  }

  clearLocalCredentials() {
    this.memory.forgetWallet();
    this.memory.forgetApiKey();
  }

  async bindSubWallet(apiKey, body) {
    const client = new SecureClient(apiKey, this.memory);
    const reqBody = {
      apiKey: body.apiKey,
      subWalletName: body.subWalletName
    };
    return client.secureRequest('POST', '/post/claw/bind-sub-wallet', 'C00003', reqBody, null, body.subWalletId);
  }

  queryWallet() {
    const sid = this.memory.recallWallet();
    if (sid) {
      return { resCode: 'S010000', resMsg: '已绑定', subWalletId: sid, bindStatus: '已绑定' };
    }
    return { resCode: 'S010000', resMsg: '未绑定', subWalletId: null, bindStatus: '未绑定' };
  }

  unbindWallet() {
    const sid = this.memory.recallWallet();
    if (!sid) {
      return { resCode: 'F010001', resMsg: '未绑定子钱包', unbindStatus: '解绑失败' };
    }
    this.clearLocalCredentials();
    return { resCode: 'S010000', resMsg: '解绑成功，本地凭据已清除', subWalletId: sid, unbindStatus: '已解绑' };
  }

  async revokeBinding(apiKey, body) {
    const client = new SecureClient(apiKey, this.memory);
    const reqBody = {
      subWalletName: body.subWalletName
    };
    const result = await client.secureRequest('POST', '/post/pay-claw/unbind-sub-wallet', 'C00011', reqBody);

    if (result.resCode === 'S010000') {
      this.clearLocalCredentials();
    }
    return result;
  }
}

class PaymentService {
  constructor(memory) {
    this.memory = memory;
  }

  _validateAmount(amount) {
    if (!amount) {
      throw new Error('Missing amount parameter');
    }
    try {
      const amountInt = parseInt(parseFloat(amount));
      if (amountInt <= 0) {
        throw new Error('Amount must be positive integer (fen/分)');
      }
      if (amountInt !== parseFloat(amount)) {
        throw new Error('Amount must be integer (fen/分), decimal not allowed');
      }
      return amountInt;
    } catch (e) {
      if (e.message.includes('Amount') || e.message.includes('Missing')) {
        throw e;
      }
      throw new Error('Amount must be integer (fen/分)');
    }
  }

  async initiatePayment(apiKey, body) {
    const amount = body.amount;
    const merApiKey = body.merApiKey;
    const seqId = body.seqId;
    const orderDetail = body.orderDetail || '';
    const confirm = body.confirm;

    const amountInt = this._validateAmount(amount);

    if (!merApiKey) {
      throw new Error('Missing merApiKey parameter');
    }

    if (!seqId) {
      throw new Error('Missing seqId parameter (merchant transaction ID, required)');
    }

    const subWalletId = this.memory.recallWallet();

    const reqBody = {
      amount: amountInt,
      merApiKey: merApiKey
    };
    if (subWalletId) {
      reqBody.subWalletId = subWalletId;
    }
    if (orderDetail) {
      reqBody.orderDetail = orderDetail;
    }

    const trxDevcInf = body.trxDevcInf || {
      ip: '127.0.0.1',
      terminal: '3',
      mac: '00:00:00:00:00:00',
      deviceID: 'skill-server-001',
      deviceType: '4',
      imei: '',
      imsi: '',
      wifiMac: '',
      gps: ''
    };

    const extraFields = {
      seqId: seqId,
      trxDevcInf: JSON.stringify(trxDevcInf)
    };

    const client = new SecureClient(apiKey, this.memory);
    return client.secureRequest('POST', '/post/pay-claw/payment', 'C00009', reqBody, seqId, null, extraFields);
  }
}

class QueryService {
  constructor(memory) {
    this.memory = memory;
  }

  async queryOrder(apiKey, body) {
    const orgSeqId = body.orgSeqId;
    if (!orgSeqId) {
      throw new Error('Missing orgSeqId parameter');
    }

    const subWalletId = this.memory.recallWallet();
    if (!subWalletId) {
      throw new Error('subWalletId not found. Bind wallet first via C00003.');
    }

    const merApiKey = body.merApiKey;

    const reqBody = {
      subWalletId: subWalletId,
      orgSeqId: orgSeqId
    };
    if (merApiKey) {
      reqBody.merApiKey = merApiKey;
    }

    const client = new SecureClient(apiKey, this.memory);
    return client.secureRequest('POST', '/post/claw/query-pay-status', 'C00005', reqBody);
  }

  async queryTransactions(apiKey, body) {
    const subWalletId = this.memory.recallWallet();
    if (!subWalletId) {
      throw new Error('subWalletId not found. Bind wallet first via C00003.');
    }

    const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const startDate = body.startDate || today;
    const endDate = body.endDate || today;

    const reqBody = {
      subWalletId: subWalletId,
      startDate: startDate,
      endDate: endDate
    };

    const client = new SecureClient(apiKey, this.memory);
    return client.secureRequest('POST', '/post/claw/query-receipt-list', 'C00007', reqBody);
  }
}

class SkillOrchestrator {
  constructor(memory) {
    this.memory = memory;
    this._wallet = new WalletService(memory);
    this._payment = new PaymentService(memory);
    this._query = new QueryService(memory);
  }

  _requireApiKey() {
    const apiKey = this.memory.recallApiKey();
    if (!apiKey) throw new Error('apiKey not set. Bind wallet first via C00003.');
    return apiKey;
  }

  _attachSubWalletId(body) {
    const subWalletId = this.memory.recallWallet();
    if (subWalletId) {
      body.subWalletId = subWalletId;
    }
  }

  async bindSubWallet(body) {
    const apiKey = body.apiKey;
    if (!apiKey) throw new Error('--apiKey is required for C00003');
    if (!body.subWalletName) throw new Error('--subWalletName is required for C00003');

    log('debug', 'Using apiKey (masked):', maskApiKey(apiKey));
    log('debug', 'Using subWalletId (masked):', maskSubWalletId(body.subWalletId));

    const result = await this._wallet.bindSubWallet(apiKey, body);

    if (result.resCode === 'S010000') {
      this.memory.rememberApiKey(apiKey);
      let resData = result.resData;
      if (typeof resData === 'string') {
        try { resData = JSON.parse(resData); } catch (_) {}
      }
      if (resData && resData.subWalletId) {
        this.memory.rememberWallet(resData.subWalletId);
      }
    }

    log('info', 'C00003 Response:', result);
    return result;
  }

  queryWallet() {
    return this._wallet.queryWallet();
  }

  unbindWallet() {
    return this._wallet.unbindWallet();
  }

  async initiatePayment(body) {
    const apiKey = this._requireApiKey();
    this._attachSubWalletId(body);
    return this._payment.initiatePayment(apiKey, body);
  }

  async queryOrder(body) {
    const apiKey = this._requireApiKey();
    this._attachSubWalletId(body);
    return this._query.queryOrder(apiKey, body);
  }

  async queryTransactions(body) {
    const apiKey = this._requireApiKey();
    return this._query.queryTransactions(apiKey, body);
  }

  async revokeBinding(body) {
    const apiKey = this._requireApiKey();
    if (!body.subWalletName) {
      throw new Error('--subWalletName is required for C00011');
    }
    return this._wallet.revokeBinding(apiKey, body);
  }

}

module.exports = { WalletService, PaymentService, QueryService, SkillOrchestrator };
