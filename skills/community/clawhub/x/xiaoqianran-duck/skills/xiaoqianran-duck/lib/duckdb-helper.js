const duckdb = require('@duckdb/node-api');
const path = require('path');
const fs = require('fs');

class DuckDBHelper {
  constructor(dbPath = 'data.duckdb') {
    this.dbPath = path.resolve(dbPath);
    this.conn = null;
    this.instance = null;
  }

  async connect() {
    if (this.conn) return this.conn;
    this.instance = await duckdb.DuckDBInstance.create(this.dbPath);
    this.conn = await this.instance.connect();
    return this.conn;
  }

  async close() {
    if (this.conn) {
      // DuckDB node-api may not have explicit close, but we can drop ref
      this.conn = null;
      this.instance = null;
    }
  }

  async loadHttpfs() {
    const conn = await this.connect();
    await conn.run('INSTALL httpfs; LOAD httpfs;');
  }

  /**
   * Set Hugging Face token for accessing gated/private datasets.
   * Creates a DuckDB secret.
   */
  async setHFTtoken(token) {
    const conn = await this.connect();
    await this.loadHttpfs();
    // Use parameterized if possible, but for secret we interpolate carefully
    // In production, prefer env or secure storage.
    const safeToken = String(token).replace(/'/g, '');
    await conn.run(`CREATE OR REPLACE SECRET hf_token (TYPE HUGGINGFACE, TOKEN '${safeToken}');`);
    return true;
  }

  /**
   * Try to load HF token from environment or .env
   */
  async autoLoadHFToken() {
    let token = process.env.HF_TOKEN || process.env.HUGGINGFACE_TOKEN;
    if (!token) {
      // Try .env file in project
      const envPath = path.join(path.dirname(this.dbPath), '.env');
      if (fs.existsSync(envPath)) {
        const envContent = fs.readFileSync(envPath, 'utf8');
        const match = envContent.match(/HF_TOKEN=([^\s]+)/);
        if (match) token = match[1];
      }
    }
    if (token) {
      await this.setHFTtoken(token);
      return true;
    }
    return false;
  }

  async loadExcel() {
    const conn = await this.connect();
    await conn.run('INSTALL excel; LOAD excel;');
  }

  async ensureExtensions() {
    await this.loadHttpfs();
    await this.loadExcel();
  }

  /**
   * Import a local file into a table.
   * Supports: .csv, .tsv, .json, .parquet, .xlsx
   */
  async importFile(filePath, tableName = null, options = {}) {
    const conn = await this.connect();
    const ext = path.extname(filePath).toLowerCase().replace('.', '');
    const absPath = path.resolve(filePath);
    
    if (!fs.existsSync(absPath)) {
      throw new Error(`File not found: ${absPath}`);
    }

    if (!tableName) {
      tableName = path.basename(filePath, path.extname(filePath))
        .replace(/[^a-zA-Z0-9_]/g, '_');
    }

    await this.ensureExtensions();

    let query;
    switch (ext) {
      case 'csv':
      case 'tsv':
        const delim = ext === 'tsv' ? '\t' : ',';
        query = `CREATE OR REPLACE TABLE ${tableName} AS SELECT * FROM read_csv_auto('${absPath}', delim='${delim}')`;
        break;
      case 'json':
      case 'jsonl':
        query = `CREATE OR REPLACE TABLE ${tableName} AS SELECT * FROM read_json_auto('${absPath}')`;
        break;
      case 'parquet':
        query = `CREATE OR REPLACE TABLE ${tableName} AS SELECT * FROM '${absPath}'`;
        break;
      case 'xlsx':
      case 'xls':
        query = `CREATE OR REPLACE TABLE ${tableName} AS SELECT * FROM read_xlsx('${absPath}')`;
        break;
      default:
        throw new Error(`Unsupported file extension: .${ext}. Supported: csv, tsv, json, parquet, xlsx`);
    }

    await conn.run(query);
    
    const countRes = await conn.run(`SELECT COUNT(*) as cnt FROM ${tableName}`);
    const rows = await countRes.getRows();
    const count = Number(rows[0][0]);

    return {
      tableName,
      rowCount: count,
      file: absPath,
      format: ext
    };
  }

  /**
   * Query Hugging Face dataset directly (uses hf:// protocol)
   */
  async importFromHF(hfPath, tableName = null, options = { autoToken: true }) {
    const conn = await this.connect();
    await this.loadHttpfs();

    if (options.autoToken) {
      await this.autoLoadHFToken();
    }

    if (!tableName) {
      // Derive table name from path
      tableName = hfPath.replace(/[^a-zA-Z0-9_]/g, '_').slice(0, 50);
    }

    // Support @~parquet for better performance on many HF datasets
    const query = `CREATE OR REPLACE TABLE ${tableName} AS SELECT * FROM '${hfPath}'`;

    await conn.run(query);

    const countRes = await conn.run(`SELECT COUNT(*) as cnt FROM ${tableName}`);
    const rows = await countRes.getRows();
    const count = Number(rows[0][0]);

    return {
      tableName,
      rowCount: count,
      source: hfPath,
      format: 'hf'
    };
  }

  async query(sql) {
    const conn = await this.connect();
    const result = await conn.run(sql);
    const rows = await result.getRows();
    // Also get column names if possible
    // For simplicity return rows; enhance later
    return rows;
  }

  async listTables() {
    const conn = await this.connect();
    const res = await conn.run("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main' ORDER BY table_name");
    const rows = await res.getRows();
    return rows.map(r => r[0]);
  }

  async getTableInfo(tableName) {
    const conn = await this.connect();
    const res = await conn.run(`DESCRIBE ${tableName}`);
    return await res.getRows();
  }

  async exportTable(tableName, outputPath, format = 'parquet') {
    const conn = await this.connect();
    const absPath = path.resolve(outputPath);
    
    let query;
    switch (format.toLowerCase()) {
      case 'parquet':
        query = `COPY (SELECT * FROM ${tableName}) TO '${absPath}' (FORMAT PARQUET)`;
        break;
      case 'csv':
        query = `COPY (SELECT * FROM ${tableName}) TO '${absPath}' (FORMAT CSV, HEADER)`;
        break;
      case 'json':
        query = `COPY (SELECT * FROM ${tableName}) TO '${absPath}' (FORMAT JSON)`;
        break;
      default:
        throw new Error('Supported export formats: parquet, csv, json');
    }

    await conn.run(query);
    return absPath;
  }
}

module.exports = DuckDBHelper;
