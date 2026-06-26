'use strict';

const sm2 = require('sm-crypto').sm2;

const CIPHER_MODE = 0;

/**
 * SM2 加密（C1C2C3 模式，与 Java BouncyCastle 一致）
 * @param {string} publicKey - 公钥 hex
 * @param {string} plaintext - 明文
 * @returns {string} 密文 hex（04前缀 + C1C2C3）
 */
function encrypt(publicKey, plaintext) {
  // sm-crypto 生成的密文C1部分不包含04前缀
  // 但 Java BouncyCastle 期望C1有04前缀（非压缩格式标识）
  // 参考后端代码：if(cipherData.length() <= 256) { cipherData = "04".concat(cipherData); }
  const ciphertext = sm2.doEncrypt(plaintext, publicKey, CIPHER_MODE);
  // 如果密文不以04开头，添加04前缀
  if (!ciphertext.startsWith('04')) {
    return '04' + ciphertext;
  }
  return ciphertext;
}

/**
 * SM2 解密（C1C2C3 模式）
 * @param {string} privateKey - 私钥 hex (64 chars)
 * @param {string} ciphertext - 密文 hex（可能带04前缀）
 * @returns {string} 明文
 */
function decrypt(privateKey, ciphertext) {
  // sm-crypto 的 doDecrypt 不期望04前缀
  // 如果密文以04开头，去掉它
  let cipher = ciphertext;
  if (cipher.startsWith('04')) {
    cipher = cipher.slice(2);
  }
  return sm2.doDecrypt(cipher, privateKey, CIPHER_MODE);
}

/**
 * SM2 签名（DER 格式，与 Java BouncyCastle 一致）
 * @param {string} privateKey - 私钥 hex (64 chars)
 * @param {string} data - 待签名数据
 * @returns {string} DER 签名 hex
 */
function sign(privateKey, data) {
  return sm2.doSignature(data, privateKey, {
    der: true,
    hash: true,
    publicKey: ''
  });
}

/**
 * SM2 验签（DER 格式）
 * @param {string} publicKey - 公钥 hex
 * @param {string} data - 原始数据
 * @param {string} signatureHex - DER 签名 hex
 * @returns {boolean}
 */
function verify(publicKey, data, signatureHex) {
  return sm2.doVerifySignature(data, signatureHex, publicKey, {
    der: true,
    hash: true
  });
}

/**
 * 从私钥推导公钥
 * @param {string} privateKey - 私钥 hex (64 chars)
 * @returns {string} 公钥 hex（04前缀 + 128 chars）
 */
function derivePublicKey(privateKey) {
  return sm2.getPublicKeyFromPrivateKey(privateKey);
}

module.exports = { encrypt, decrypt, sign, verify, derivePublicKey };
