/**
 * crypto-local.js — AES-256-GCM machine-derived encryption
 *
 * Derives an encryption key from /etc/machine-id + username so the encrypted
 * file is only decryptable on this machine as this user. Zero external deps.
 *
 * File format (binary):
 *   [4 bytes magic "OCVT"][1 byte version=1][32 bytes PBKDF2 salt]
 *   [12 bytes GCM IV][16 bytes GCM auth tag][N bytes ciphertext]
 */

"use strict";

const crypto = require("node:crypto");
const fs = require("node:fs");
const os = require("node:os");

const MAGIC = Buffer.from("OCVT");
const VERSION = 1;
const SALT_LEN = 32;
const IV_LEN = 12;
const TAG_LEN = 16;
const KEY_LEN = 32;
const PBKDF2_ITERATIONS = 600_000;
const PBKDF2_DIGEST = "sha512";
const APP_SALT = "openclaw-supabase-v1";

/**
 * Read /etc/machine-id (Linux) or equivalent.
 * Falls back to hostname if not available.
 */
function getMachineId() {
  try {
    return fs.readFileSync("/etc/machine-id", "utf8").trim();
  } catch {
    try {
      return fs.readFileSync("/var/lib/dbus/machine-id", "utf8").trim();
    } catch {
      return os.hostname();
    }
  }
}

/**
 * Derive a 32-byte AES key from machine identity.
 * @param {Buffer} salt - Random 32-byte salt stored in the encrypted file header.
 */
function deriveKey(salt) {
  const machineId = getMachineId();
  const username = os.userInfo().username;
  const password = `${machineId}:${username}:${APP_SALT}`;
  return crypto.pbkdf2Sync(password, salt, PBKDF2_ITERATIONS, KEY_LEN, PBKDF2_DIGEST);
}

/**
 * Encrypt a UTF-8 string.
 * @param {string} plaintext
 * @returns {Buffer} Encrypted blob ready for writing to disk.
 */
function encrypt(plaintext) {
  const salt = crypto.randomBytes(SALT_LEN);
  const iv = crypto.randomBytes(IV_LEN);
  const key = deriveKey(salt);

  const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
  const ciphertext = Buffer.concat([
    cipher.update(Buffer.from(plaintext, "utf8")),
    cipher.final(),
  ]);
  const tag = cipher.getAuthTag();

  return Buffer.concat([
    MAGIC,
    Buffer.from([VERSION]),
    salt,
    iv,
    tag,
    ciphertext,
  ]);
}

/**
 * Decrypt a blob produced by encrypt().
 * @param {Buffer} blob
 * @returns {string} Decrypted UTF-8 string.
 */
function decrypt(blob) {
  if (!Buffer.isBuffer(blob)) blob = Buffer.from(blob);

  // Validate header
  if (blob.length < MAGIC.length + 1 + SALT_LEN + IV_LEN + TAG_LEN) {
    throw new Error("crypto-local: invalid encrypted blob (too short)");
  }
  const magic = blob.subarray(0, 4);
  if (!magic.equals(MAGIC)) {
    throw new Error("crypto-local: invalid magic bytes — not an OCVT file");
  }
  const version = blob[4];
  if (version !== VERSION) {
    throw new Error(`crypto-local: unsupported version ${version}`);
  }

  let offset = 5;
  const salt = blob.subarray(offset, offset + SALT_LEN); offset += SALT_LEN;
  const iv   = blob.subarray(offset, offset + IV_LEN);   offset += IV_LEN;
  const tag  = blob.subarray(offset, offset + TAG_LEN);  offset += TAG_LEN;
  const ciphertext = blob.subarray(offset);

  const key = deriveKey(salt);
  const decipher = crypto.createDecipheriv("aes-256-gcm", key, iv);
  decipher.setAuthTag(tag);

  try {
    const plaintext = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
    return plaintext.toString("utf8");
  } catch {
    throw new Error(
      "crypto-local: decryption failed — wrong machine/user or file corrupted"
    );
  }
}

module.exports = { encrypt, decrypt, deriveKey };
