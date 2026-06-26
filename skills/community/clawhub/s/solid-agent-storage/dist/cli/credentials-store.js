import { randomBytes, createCipheriv, createDecipheriv, pbkdf2Sync } from 'node:crypto';
import { mkdirSync, writeFileSync, readFileSync, readdirSync, chmodSync, existsSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';
const ALGORITHM = 'aes-256-gcm';
const KEY_LENGTH = 32;
const PBKDF2_ITERATIONS = 100_000;
const SALT_LENGTH = 32;
const IV_LENGTH = 16;
let encryptionKey = null;
function getStoreDir() {
    return join(homedir(), '.interition', 'agents');
}
function deriveKey(passphrase, salt) {
    return pbkdf2Sync(passphrase, salt, PBKDF2_ITERATIONS, KEY_LENGTH, 'sha256');
}
export function initStore(passphrase) {
    // Derive a key from passphrase with a fixed salt for session use.
    // Each file has its own random salt for actual encryption.
    // We store the passphrase-derived material to re-derive per-file keys.
    // Actually, we just hold the passphrase and derive per-file.
    // Simpler: hold passphrase in closure. But we need it in module scope.
    // Store passphrase hash as the "session key" indicator.
    encryptionKey = Buffer.from(passphrase, 'utf-8');
}
export function isStoreInitialised() {
    return encryptionKey !== null;
}
function getPassphrase() {
    if (!encryptionKey) {
        throw new Error('Credentials store not initialised. Call initStore(passphrase) first.');
    }
    return encryptionKey;
}
function encrypt(data, passphrase) {
    const salt = randomBytes(SALT_LENGTH);
    const key = deriveKey(passphrase.toString('utf-8'), salt);
    const iv = randomBytes(IV_LENGTH);
    const cipher = createCipheriv(ALGORITHM, key, iv);
    const encrypted = Buffer.concat([cipher.update(data, 'utf-8'), cipher.final()]);
    const tag = cipher.getAuthTag();
    return {
        salt: salt.toString('base64'),
        iv: iv.toString('base64'),
        tag: tag.toString('base64'),
        data: encrypted.toString('base64'),
    };
}
function decrypt(payload, passphrase) {
    const salt = Buffer.from(payload.salt, 'base64');
    const key = deriveKey(passphrase.toString('utf-8'), salt);
    const iv = Buffer.from(payload.iv, 'base64');
    const tag = Buffer.from(payload.tag, 'base64');
    const data = Buffer.from(payload.data, 'base64');
    const decipher = createDecipheriv(ALGORITHM, key, iv);
    decipher.setAuthTag(tag);
    try {
        const decrypted = Buffer.concat([decipher.update(data), decipher.final()]);
        return decrypted.toString('utf-8');
    }
    catch {
        throw new Error('Invalid passphrase — cannot decrypt credentials');
    }
}
export function saveCredentials(name, credentials) {
    const passphrase = getPassphrase();
    const agentDir = join(getStoreDir(), name);
    mkdirSync(agentDir, { recursive: true });
    const payload = encrypt(JSON.stringify(credentials), passphrase);
    const filePath = join(agentDir, 'credentials.enc');
    writeFileSync(filePath, JSON.stringify(payload, null, 2), 'utf-8');
    // Defence in depth: restrict file permissions (owner only)
    try {
        chmodSync(filePath, 0o600);
    }
    catch {
        // chmod may fail on some platforms (e.g., Windows) — non-fatal
    }
}
export function loadCredentials(name) {
    const passphrase = getPassphrase();
    const filePath = join(getStoreDir(), name, 'credentials.enc');
    if (!existsSync(filePath)) {
        throw new Error(`No credentials found for agent "${name}". Run provision first.`);
    }
    const raw = readFileSync(filePath, 'utf-8');
    const payload = JSON.parse(raw);
    const decrypted = decrypt(payload, passphrase);
    return JSON.parse(decrypted);
}
export function deleteAgentCredentials(name) {
    const agentDir = join(getStoreDir(), name);
    if (existsSync(agentDir)) {
        rmSync(agentDir, { recursive: true, force: true });
    }
}
export function listAgents() {
    const dir = getStoreDir();
    if (!existsSync(dir))
        return [];
    return readdirSync(dir, { withFileTypes: true })
        .filter((d) => d.isDirectory())
        .map((d) => d.name);
}
//# sourceMappingURL=credentials-store.js.map