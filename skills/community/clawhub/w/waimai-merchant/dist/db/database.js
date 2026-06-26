"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getDatabase = getDatabase;
exports.closeDatabase = closeDatabase;
exports.getDataDir = getDataDir;
const better_sqlite3_1 = __importDefault(require("better-sqlite3"));
const path = __importStar(require("path"));
const os = __importStar(require("os"));
const fs = __importStar(require("fs"));
// 数据存储目录
const DATA_DIR = path.join(os.homedir(), '.waimai-merchant');
const DB_PATH = path.join(DATA_DIR, 'merchant.db');
// 确保数据目录存在
function ensureDataDir() {
    if (!fs.existsSync(DATA_DIR)) {
        fs.mkdirSync(DATA_DIR, { recursive: true });
    }
}
// 数据库连接实例
let db = null;
// 获取数据库连接
function getDatabase() {
    if (!db) {
        ensureDataDir();
        db = new better_sqlite3_1.default(DB_PATH);
        db.pragma('journal_mode = WAL');
        initializeTables();
    }
    return db;
}
// 初始化数据表
function initializeTables() {
    if (!db)
        return;
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
function closeDatabase() {
    if (db) {
        db.close();
        db = null;
    }
}
// 获取数据目录路径
function getDataDir() {
    return DATA_DIR;
}
//# sourceMappingURL=database.js.map