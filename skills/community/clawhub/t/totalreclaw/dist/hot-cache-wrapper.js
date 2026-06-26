/**
 * Hot cache wrapper for the plugin.
 *
 * Self-contained XChaCha20-Poly1305 encrypted cache (same implementation as
 * client/src/cache/hot-cache.ts but without cross-package import).
 */
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
const MAX_HOT_FACTS = 30;
const IV_LENGTH = 12;
const TAG_LENGTH = 16;
export class PluginHotCache {
    cachePath;
    hotFacts = [];
    factCount = 0;
    lastSyncedBlock = 0;
    smartAccountAddress = '';
    lastUpdatedAt = 0;
    lastQueryEmbedding = null;
    key;
    constructor(cachePath, hexKey) {
        this.cachePath = cachePath;
        this.key = Buffer.from(hexKey, 'hex');
    }
    getHotFacts() { return [...this.hotFacts]; }
    getFactCount() { return this.factCount; }
    getLastSyncedBlock() { return this.lastSyncedBlock; }
    getSmartAccountAddress() { return this.smartAccountAddress; }
    getLastUpdatedAt() { return this.lastUpdatedAt; }
    getLastQueryEmbedding() { return this.lastQueryEmbedding ? [...this.lastQueryEmbedding] : null; }
    setHotFacts(facts) {
        const sorted = [...facts].sort((a, b) => b.importance - a.importance);
        this.hotFacts = sorted.slice(0, MAX_HOT_FACTS);
        this.lastUpdatedAt = Date.now();
    }
    setFactCount(count) { this.factCount = count; }
    setLastSyncedBlock(block) { this.lastSyncedBlock = block; }
    setSmartAccountAddress(addr) { this.smartAccountAddress = addr; }
    setLastUpdatedAt(ts) { this.lastUpdatedAt = ts; }
    setLastQueryEmbedding(embedding) { this.lastQueryEmbedding = embedding ? [...embedding] : null; }
    /**
     * Check if the cache is fresh (within TTL).
     * @param ttlMs TTL in milliseconds (default: 5 minutes)
     */
    isFresh(ttlMs = 300_000) {
        if (this.lastUpdatedAt === 0)
            return false;
        return (Date.now() - this.lastUpdatedAt) < ttlMs;
    }
    flush() {
        const payload = {
            hotFacts: this.hotFacts,
            factCount: this.factCount,
            lastSyncedBlock: this.lastSyncedBlock,
            smartAccountAddress: this.smartAccountAddress,
            lastUpdatedAt: this.lastUpdatedAt,
            lastQueryEmbedding: this.lastQueryEmbedding,
        };
        const plaintext = Buffer.from(JSON.stringify(payload), 'utf-8');
        const iv = crypto.randomBytes(IV_LENGTH);
        const cipher = crypto.createCipheriv('aes-256-gcm', this.key, iv);
        const encrypted = Buffer.concat([cipher.update(plaintext), cipher.final()]);
        const tag = cipher.getAuthTag();
        const output = Buffer.concat([iv, tag, encrypted]);
        const dir = path.dirname(this.cachePath);
        if (!fs.existsSync(dir))
            fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(this.cachePath, output);
    }
    load() {
        if (!fs.existsSync(this.cachePath))
            return;
        try {
            const data = fs.readFileSync(this.cachePath);
            if (data.length < IV_LENGTH + TAG_LENGTH)
                return;
            const iv = data.subarray(0, IV_LENGTH);
            const tag = data.subarray(IV_LENGTH, IV_LENGTH + TAG_LENGTH);
            const ciphertext = data.subarray(IV_LENGTH + TAG_LENGTH);
            const decipher = crypto.createDecipheriv('aes-256-gcm', this.key, iv);
            decipher.setAuthTag(tag);
            const decrypted = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
            const payload = JSON.parse(decrypted.toString('utf-8'));
            this.hotFacts = payload.hotFacts || [];
            this.factCount = payload.factCount || 0;
            this.lastSyncedBlock = payload.lastSyncedBlock || 0;
            this.smartAccountAddress = payload.smartAccountAddress || '';
            this.lastUpdatedAt = payload.lastUpdatedAt || 0;
            this.lastQueryEmbedding = payload.lastQueryEmbedding || null;
        }
        catch {
            this.hotFacts = [];
            this.factCount = 0;
            this.lastSyncedBlock = 0;
            this.smartAccountAddress = '';
            this.lastUpdatedAt = 0;
            this.lastQueryEmbedding = null;
        }
    }
}
