// Example: How to use xiaoqianran-duck in Electron main process
// Place this in your Electron main.js or preload/main

const { app } = require('electron'); // only if in electron
const DuckDBHelper = require('../lib/duckdb-helper');
const path = require('path');

async function initDuckDB() {
  const dbPath = path.join(app.getPath('userData'), 'data.duckdb');
  const helper = new DuckDBHelper(dbPath);

  // Example usage from renderer via ipcMain
  // ipcMain.handle('duck:import', async (e, filePath) => {
  //   return helper.importFile(filePath);
  // });

  // HF example
  // await helper.importFromHF('hf://...');

  console.log('[Electron] DuckDB helper ready at', dbPath);
  return helper;
}

// In real Electron:
// const helper = await initDuckDB();

module.exports = { initDuckDB };
