// AES-GCM + PBKDF2 encryption — adapted from your working implementation
// Uses Web Crypto API (available globally in Node 22)
import { webcrypto as crypto } from "crypto"
import { MASTER_ENCRYPTED, MASTER_ENCRYPTION_PASSWORD_CRYPTO, MASTER_SALT } from "./environment.ts"

const ALGORITHM = "AES-GCM"
const KEY_LENGTH = 256
const IV_LENGTH = 12 // 96 bits for GCM

// Derive a CryptoKey from a password using PBKDF2
export const deriveKeyFromPassword = async (
  password: string,
  salt?: Uint8Array
): Promise<{ key: CryptoKey; salt: Uint8Array }> => {
  const encoder = new TextEncoder()

  const keyMaterial = await crypto.subtle.importKey(
    "raw",
    encoder.encode(password),
    { name: "PBKDF2" },
    false,
    ["deriveBits", "deriveKey"]
  )

  const saltArray = salt ?? crypto.getRandomValues(new Uint8Array(16))

  const key = await crypto.subtle.deriveKey(
    {
      name: "PBKDF2",
      salt: saltArray,
      iterations: 100_000,
      hash: "SHA-256",
    },
    keyMaterial,
    { name: ALGORITHM, length: KEY_LENGTH },
    false,
    ["encrypt", "decrypt"]
  )

  return { key, salt: saltArray }
}

// Encrypt a plaintext string → base64 (IV prepended)
export const encrypt = async (plaintext: string, key: CryptoKey): Promise<string> => {
  const encoder = new TextEncoder()
  const data = encoder.encode(plaintext)
  const iv = crypto.getRandomValues(new Uint8Array(IV_LENGTH))

  const encrypted = await crypto.subtle.encrypt({ name: ALGORITHM, iv }, key, data)

  const combined = new Uint8Array(iv.length + encrypted.byteLength)
  combined.set(iv)
  combined.set(new Uint8Array(encrypted), iv.length)

  return btoa(String.fromCharCode(...combined))
}

// Decrypt a base64 string (IV prepended) → plaintext
export const decrypt = async (encryptedBase64: string, key: CryptoKey): Promise<string> => {
  const combined = new Uint8Array(
    atob(encryptedBase64)
      .split("")
      .map(c => c.charCodeAt(0))
  )

  const iv = combined.slice(0, IV_LENGTH)
  const encrypted = combined.slice(IV_LENGTH).buffer

  const decrypted = await crypto.subtle.decrypt({ name: ALGORITHM, iv }, key, encrypted)
  return new TextDecoder().decode(decrypted)
}

// Encrypt with a password — returns encrypted payload + salt (both base64)
export const encryptWithPassword = async (
  plaintext: string,
  password: string
): Promise<{ encrypted: string; salt: string }> => {
  const { key, salt } = await deriveKeyFromPassword(password)
  const encrypted = await encrypt(plaintext, key)
  const saltBase64 = btoa(String.fromCharCode(...salt))
  return { encrypted, salt: saltBase64 }
}

// Decrypt with a password + salt (both base64)
export const decryptWithPassword = async (
  encrypted: string,
  password: string,
  saltBase64: string
): Promise<string> => {
  const salt = new Uint8Array(
    atob(saltBase64)
      .split("")
      .map(c => c.charCodeAt(0))
  )
  const { key } = await deriveKeyFromPassword(password, salt)
  return decrypt(encrypted, key)
}

// Decrypt the master key from env vars (two-layer: password → master key)
export const getMasterKey = async (): Promise<string> =>
  decryptWithPassword(
    MASTER_ENCRYPTED(),
    MASTER_ENCRYPTION_PASSWORD_CRYPTO(),
    MASTER_SALT()
  )
