import Database from 'better-sqlite3';
import * as path from 'path';
import * as os from 'os';
import * as fs from 'fs';

// 数据存储目录
const DATA_DIR = path.join(os.homedir(), '.waimai-merchant');
const DB_PATH = path.join(DATA_DIR, 'merchant.db');

// 确保数据目录存在
function ensureDataDir(): void {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
}

// 数据库连接实例
let db: Database.Database | null = null;

// 获取数据库连接
export function getDatabase(): Database.Database {
  if (!db) {
    ensureDataDir();
    db = new Database(DB_PATH);
    db.pragma('journal_mode = WAL');
    initializeTables();
  }
  return db;
}

// 初始化数据表
function initializeTables(): void {
  if (!db) return;

  // 商家表
  db.exec(`
    CREATE TABLE IF NOT EXISTS merchants (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      phone TEXT NOT NULL UNIQUE,
      email TEXT,
      address TEXT NOT NULL,
      business_license TEXT,
      contact_person TEXT,
      status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'suspended')),
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // 商品表
  db.exec(`
    CREATE TABLE IF NOT EXISTS products (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      merchant_id INTEGER NOT NULL,
      name TEXT NOT NULL,
      description TEXT,
      price REAL NOT NULL CHECK (price >= 0),
      original_price REAL CHECK (original_price >= 0),
      image_url TEXT,
      category TEXT,
      delivery_time INTEGER DEFAULT 30,
      stock INTEGER DEFAULT 0 CHECK (stock >= 0),
      status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'sold_out')),
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (merchant_id) REFERENCES merchants(id) ON DELETE CASCADE
    )
  `);

  // 创建索引
  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_products_merchant ON products(merchant_id);
    CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);
    CREATE INDEX IF NOT EXISTS idx_merchants_phone ON merchants(phone);
    CREATE INDEX IF NOT EXISTS idx_merchants_status ON merchants(status);
  `);
}

// 关闭数据库连接
export function closeDatabase(): void {
  if (db) {
    db.close();
    db = null;
  }
}

// 获取数据目录路径
export function getDataDir(): string {
  return DATA_DIR;
}

// 导出类型定义
export interface Merchant {
  id: number;
  name: string;
  phone: string;
  email?: string;
  address: string;
  business_license?: string;
  contact_person?: string;
  status: 'pending' | 'approved' | 'rejected' | 'suspended';
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: number;
  merchant_id: number;
  name: string;
  description?: string;
  price: number;
  original_price?: number;
  image_url?: string;
  category?: string;
  delivery_time: number;
  stock: number;
  status: 'active' | 'inactive' | 'sold_out';
  created_at: string;
  updated_at: string;
}
