import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { TokenSet } from 'xero-node';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export interface StoredTokens {
  tokenSet: TokenSet;
  activeTenantId?: string;
  updatedAt: string;
}

export class TokenStore {
  private tokenPath: string;

  constructor(tokenPath?: string) {
    this.tokenPath = tokenPath || path.join(__dirname, '../../data/tokens.json');
  }

  save(tokenSet: TokenSet, activeTenantId?: string): void {
    const data: StoredTokens = {
      tokenSet,
      activeTenantId,
      updatedAt: new Date().toISOString(),
    };

    const dir = path.dirname(this.tokenPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(this.tokenPath, JSON.stringify(data, null, 2), 'utf-8');
  }

  load(): StoredTokens | null {
    if (!fs.existsSync(this.tokenPath)) {
      return null;
    }

    try {
      const data = fs.readFileSync(this.tokenPath, 'utf-8');
      return JSON.parse(data) as StoredTokens;
    } catch {
      return null;
    }
  }

  hasTokens(): boolean {
    return this.load() !== null;
  }

  getTokenSet(): TokenSet | null {
    const data = this.load();
    return data?.tokenSet || null;
  }

  getActiveTenantId(): string | null {
    const data = this.load();
    return data?.activeTenantId || null;
  }

  setActiveTenantId(tenantId: string): void {
    const data = this.load();
    if (data) {
      this.save(data.tokenSet, tenantId);
    }
  }

  isTokenExpired(): boolean {
    const tokenSet = this.getTokenSet();
    if (!tokenSet || !tokenSet.expires_at) {
      return true;
    }

    const expiresAt = tokenSet.expires_at * 1000;
    const bufferMs = 60000;
    return Date.now() > expiresAt - bufferMs;
  }

  clear(): void {
    if (fs.existsSync(this.tokenPath)) {
      fs.unlinkSync(this.tokenPath);
    }
  }

  getTokenInfo(): { isValid: boolean; expiresAt?: Date; expiresIn?: string } {
    const tokenSet = this.getTokenSet();
    if (!tokenSet || !tokenSet.expires_at) {
      return { isValid: false };
    }

    const expiresAt = new Date(tokenSet.expires_at * 1000);
    const now = new Date();
    const diffMs = expiresAt.getTime() - now.getTime();

    if (diffMs <= 0) {
      return { isValid: false, expiresAt };
    }

    const diffMins = Math.floor(diffMs / 60000);
    const diffSecs = Math.floor((diffMs % 60000) / 1000);

    return {
      isValid: true,
      expiresAt,
      expiresIn: `${diffMins}m ${diffSecs}s`,
    };
  }
}

export const tokenStore = new TokenStore();
