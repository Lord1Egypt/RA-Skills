'use strict';

const sm2 = require('./sm2');
const sm4 = require('./sm4');

const DEFAULT_TRX_DEVICE_INFO = {
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

/**
 * GM 安全策略 — 与 Java AbstractController 加解密逻辑对应
 */
class GmStrategy {
  /**
   * @param {string} apiKey - api_key 即 SM2 私钥
   * @param {string} serverPublicKey - 服务端 SM2 公钥
   * @param {object} memory - Memory 实例
   */
  constructor(apiKey, serverPublicKey, memory) {
    this.apiKey = apiKey;
    this.clientPrivateKey = apiKey;
    this.serverPublicKey = serverPublicKey;
    this.memory = memory;
    this.version = '1.0';
  }

  _resolveAppId() {
    if (this.memory) {
      const subWalletId = this.memory.recallWallet();
      if (subWalletId) return subWalletId;
    }
    return this.apiKey;
  }

  _generateSeqId() {
    return String(Date.now() * 1000000 + Math.floor(Math.random() * 1000000));
  }

  _timestamp() {
    const d = new Date();
    const pad = n => String(n).padStart(2, '0');
    return `${d.getFullYear()}${pad(d.getMonth()+1)}${pad(d.getDate())}${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
  }

  _buildCommonFields(seqId, interfaceId) {
    return {
      appId: this._resolveAppId(),
      version: this.version,
      seqId: seqId,
      timeStamp: this._timestamp(),
      interfaceId: interfaceId
    };
  }

  buildRequestHeaders(endpoint, interfaceId) {
    return {
      'Content-Type': 'application/json; charset=utf-8',
      'X-Encryption-Type': 'SM2/SM4',
      'X-Interface-Id': interfaceId
    };
  }

  buildRequestBody(body, interfaceId, seqId, appIdOverride, extraFields) {
    if (!body) body = {};
    if (!seqId) seqId = this._generateSeqId();
    if (!interfaceId) throw new Error('interfaceId required');

    const headerFields = this._buildCommonFields(seqId, interfaceId);
    if (appIdOverride) {
      headerFields.appId = appIdOverride;
    }

    // 交易设备信息（放在加密数据外层，服务端需要）
    // 优先使用 extraFields 中传入的 trxDevcInf
    const trxDevcInf = (extraFields && extraFields.trxDevcInf) || body.trxDevcInf || DEFAULT_TRX_DEVICE_INFO;
    const trxDevcInfStr = typeof trxDevcInf === 'string' ? trxDevcInf : JSON.stringify(trxDevcInf);

    const sm4Key = sm4.generateKey();

    const encryptedData = sm4.encryptECB(sm4Key, JSON.stringify(body));
    const encryptedSm4Key = sm2.encrypt(this.serverPublicKey, sm4Key);

    const signDict = {
      appId: headerFields.appId,
      version: headerFields.version,
      seqId: headerFields.seqId,
      timeStamp: headerFields.timeStamp,
      interfaceId: headerFields.interfaceId,
      secret: encryptedSm4Key,
      data: encryptedData
    };
    const signContent = this._orderedStringify(signDict) + sm4Key;
    const signature = sm2.sign(this.clientPrivateKey, signContent);

    return {
      ...headerFields,
      secret: encryptedSm4Key,
      data: encryptedData,
      sign: signature,
      trxDevcInf: trxDevcInfStr
    };
  }

  _orderedStringify(obj) {
    const keys = Object.keys(obj).sort();
    const pairs = keys.map(k => `"${k}":${JSON.stringify(obj[k])}`);
    return '{' + pairs.join(',') + '}';
  }

  processResponse(responseData) {
    const serverSign = responseData.sign || '';
    let secret = responseData.secret || '';
    const encryptedData = responseData.data || '';

    // 检测未加密响应（data 是明文 JSON，不是 hex 密文）
    const isPlainJson = encryptedData && (encryptedData.startsWith('{') || encryptedData.startsWith('['));
    if (isPlainJson) {
      try { return JSON.parse(encryptedData); } catch (_) { return { data: encryptedData }; }
    }

    // 处理 04 前缀
    if (secret.startsWith('04')) {
      secret = secret.slice(2);
    }

    const sm4Key = sm2.decrypt(this.clientPrivateKey, secret);

    const verifyDict = { ...responseData };
    delete verifyDict.sign;
    delete verifyDict.trxDevcInf;
    delete verifyDict.sessionToken;
    Object.keys(verifyDict).forEach(k => {
      if (verifyDict[k] === null || verifyDict[k] === undefined) delete verifyDict[k];
    });
    const sortedKeys = Object.keys(verifyDict).sort();
    const verifyJson = '{' + sortedKeys.map(k => `"${k}":${JSON.stringify(verifyDict[k])}`).join(',') + '}';
    const verifyContent = verifyJson + sm4Key;

    if (serverSign) {
      const isValid = sm2.verify(this.serverPublicKey, verifyContent, serverSign);
      if (!isValid) throw new Error('Server signature verification failed');
    }

    if (encryptedData) {
      const decrypted = sm4.decryptECB(sm4Key, encryptedData);
      try { return JSON.parse(decrypted); } catch (_) { return { data: decrypted }; }
    }

    return responseData;
  }
}

module.exports = { GmStrategy };
