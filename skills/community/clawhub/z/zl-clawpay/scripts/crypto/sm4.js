'use strict';

/**
 * SM4 加密算法（ECB 模式）— 基于 sm-crypto 库实现
 * 
 * 迁移记录：v2.0.0 从自实现迁移至 sm-crypto，经对照测试验证加解密结果完全一致。
 * 自实现代码已移除，sm-crypto 同时提供 SM2/SM3/SM4，减少维护负担。
 */

const { sm4 } = require('sm-crypto');

/**
 * SM4 ECB 加密
 * @param {string} key - 密钥 hex（32位，16字节）
 * @param {string} plaintext - 明文
 * @returns {string} 密文 hex
 */
function encryptECB(key, plaintext) {
  return sm4.encrypt(plaintext, key, {
    inputEncoding: 'utf8',
    outputEncoding: 'hex',
    mode: 'ecb'
  });
}

/**
 * SM4 ECB 解密
 * @param {string} key - 密钥 hex（32位，16字节）
 * @param {string} ciphertextHex - 密文 hex
 * @returns {string} 明文
 */
function decryptECB(key, ciphertextHex) {
  return sm4.decrypt(ciphertextHex, key, {
    inputEncoding: 'hex',
    outputEncoding: 'utf8',
    mode: 'ecb'
  });
}

/**
 * 生成随机 SM4 密钥（16字节 = 32位 hex）
 * @returns {string} 密钥 hex
 */
function generateKey() {
  const bytes = require('crypto').randomBytes(16);
  return bytes.toString('hex');
}

module.exports = { encryptECB, decryptECB, generateKey };
