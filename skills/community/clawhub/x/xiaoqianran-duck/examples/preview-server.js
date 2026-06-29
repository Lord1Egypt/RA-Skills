// Simple HTTP preview server for xiaoqianran-duck
// Run: node examples/preview-server.js
// Then open http://localhost:3000

const http = require('http');
const DuckDBHelper = require('../lib/duckdb-helper');
const path = require('path');
const { URL } = require('url');

const helper = new DuckDBHelper(path.join(__dirname, '..', 'data.duckdb'));
const PORT = 3000;

async function startServer() {
  await helper.connect();
  console.log('DuckDB connected for preview server');

  const server = http.createServer(async (req, res) => {
    const parsedUrl = new URL(req.url, `http://localhost:${PORT}`);
    res.setHeader('Content-Type', 'text/html; charset=utf-8');

    if (parsedUrl.pathname === '/') {
      const tables = await helper.listTables();
      let html = `<h1>xiaoqianran-duck Preview</h1>`;
      html += `<p>DB: ${helper.dbPath}</p>`;
      html += `<h2>Tables</h2><ul>`;
      for (const t of tables) {
        html += `<li><a href="/table?name=${t}">${t}</a></li>`;
      }
      html += `</ul>`;
      html += `<h2>Run Query</h2>`;
      html += `<form action="/query" method="get"><input name="sql" size="80" value="SELECT * FROM sample LIMIT 5"><button>Run</button></form>`;
      res.end(html);
    } else if (parsedUrl.pathname === '/table') {
      const name = parsedUrl.searchParams.get('name');
      if (!name) { res.end('No table'); return; }
      const info = await helper.getTableInfo(name);
      const rows = await helper.query(`SELECT * FROM ${name} LIMIT 20`);
      let html = `<h1>Table: ${name}</h1>`;
      html += `<pre>${JSON.stringify(info, null, 2)}</pre>`;
      html += `<h3>Sample rows (20)</h3><pre>${JSON.stringify(rows, null, 2)}</pre>`;
      html += `<a href="/">Back</a>`;
      res.end(html);
    } else if (parsedUrl.pathname === '/query') {
      const sql = parsedUrl.searchParams.get('sql') || 'SELECT 1';
      try {
        const rows = await helper.query(sql);
        res.end(`<h1>Query Result</h1><pre>${JSON.stringify(rows, null, 2)}</pre><a href="/">Back</a>`);
      } catch (e) {
        res.end(`<h1>Error</h1><pre>${e.message}</pre><a href="/">Back</a>`);
      }
    } else {
      res.statusCode = 404;
      res.end('Not found');
    }
  });

  server.listen(PORT, () => {
    console.log(`Preview server running at http://localhost:${PORT}`);
    console.log('Use the CLI or examples to populate data.duckdb first.');
  });
}

startServer().catch(console.error);
