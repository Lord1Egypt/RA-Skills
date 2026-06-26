import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { ethers } from 'ethers';
import type { NetworkName } from './provider.js';

export interface WalletMeta {
  address: string;
  name: string;
  network: NetworkName;
  createdAt: string;
}

export class QFCKeystore {
  private storeDir: string;
  private keystoreDir: string;
  private metaPath: string;

  constructor(storeDir?: string) {
    this.storeDir = storeDir ?? path.join(os.homedir(), '.openclaw', 'qfc-wallets');
    this.keystoreDir = path.join(this.storeDir, 'keystore');
    this.metaPath = path.join(this.storeDir, 'meta.json');
  }

  private ensureDir(): void {
    fs.mkdirSync(this.keystoreDir, { recursive: true });
  }

  private readMeta(): WalletMeta[] {
    if (!fs.existsSync(this.metaPath)) return [];
    const raw = fs.readFileSync(this.metaPath, 'utf-8');
    return JSON.parse(raw) as WalletMeta[];
  }

  private writeMeta(meta: WalletMeta[]): void {
    this.ensureDir();
    fs.writeFileSync(this.metaPath, JSON.stringify(meta, null, 2), 'utf-8');
    fs.chmodSync(this.metaPath, 0o600);
  }

  async saveWallet(
    wallet: ethers.Wallet,
    password: string,
    opts?: { name?: string; network?: NetworkName },
  ): Promise<string> {
    this.ensureDir();

    const address = wallet.address.toLowerCase();
    const keystorePath = path.join(this.keystoreDir, `${address}.json`);

    const json = await wallet.encrypt(password);
    fs.writeFileSync(keystorePath, json, 'utf-8');
    fs.chmodSync(keystorePath, 0o600);

    const meta = this.readMeta();
    const existing = meta.findIndex((m) => m.address === address);
    const entry: WalletMeta = {
      address,
      name: opts?.name ?? 'default',
      network: opts?.network ?? 'testnet',
      createdAt: new Date().toISOString(),
    };

    if (existing >= 0) {
      meta[existing] = entry;
    } else {
      meta.push(entry);
    }
    this.writeMeta(meta);

    return keystorePath;
  }

  async loadWallet(address: string, password: string): Promise<ethers.Wallet> {
    const normalised = address.toLowerCase();
    const keystorePath = path.join(this.keystoreDir, `${normalised}.json`);

    if (!fs.existsSync(keystorePath)) {
      throw new Error(`No keystore found for ${address}`);
    }

    const json = fs.readFileSync(keystorePath, 'utf-8');
    return ethers.Wallet.fromEncryptedJson(json, password) as Promise<ethers.Wallet>;
  }

  listWallets(): WalletMeta[] {
    return this.readMeta();
  }

  removeWallet(address: string): boolean {
    const normalised = address.toLowerCase();
    const keystorePath = path.join(this.keystoreDir, `${normalised}.json`);

    const meta = this.readMeta();
    const filtered = meta.filter((m) => m.address !== normalised);
    if (filtered.length === meta.length) return false;

    this.writeMeta(filtered);
    if (fs.existsSync(keystorePath)) {
      fs.unlinkSync(keystorePath);
    }
    return true;
  }

  getKeystoreJson(address: string): string | null {
    const normalised = address.toLowerCase();
    const keystorePath = path.join(this.keystoreDir, `${normalised}.json`);

    if (!fs.existsSync(keystorePath)) return null;
    const raw = fs.readFileSync(keystorePath, 'utf-8');
    const parsed = JSON.parse(raw);
    if (parsed.Crypto && !parsed.crypto) {
      parsed.crypto = parsed.Crypto;
      delete parsed.Crypto;
    }
    return JSON.stringify(parsed);
  }
}
