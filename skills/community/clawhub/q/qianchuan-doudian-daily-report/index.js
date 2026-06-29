#!/usr/bin/env node
const { scrape } = require('./scraper');
const { makeReports } = require('./report');
const { writeRowsToFeishu } = require('./feishu');
const fs = require('fs');
const path = require('path');

const CONFIG_PATH = path.resolve(process.cwd(), 'config.json');
const DEFAULT_CONFIG = path.resolve(process.cwd(), 'config.example.json');

if (!fs.existsSync(CONFIG_PATH)) {
  console.error('未找到 config.json。请复制 config.example.json -> config.json，并填写目标表格配置。');
  process.exit(1);
}

(async () => {
  const config = require(CONFIG_PATH);
  try {
    console.log('开始抓取流程...');
    const rows = await scrape(config);
    console.log(`抓取完成，得到 ${rows.length} 条可见账户记录。`);

    if (config.generateReports === true) {
      console.log('开始生成本地报表...');
      const outputs = makeReports(rows, config);
      console.log('报表生成完毕：', outputs);
    } else {
      console.log('已跳过本地 CSV/Markdown 报表生成。若确需本地留档，请在 config.json 中显式设置 generateReports=true。');
    }

    const feishuResult = await writeRowsToFeishu(rows, config);
    if (feishuResult.skipped) {
      console.log(`飞书写入已跳过：${feishuResult.reason}`);
    } else {
      console.log(`飞书写入完成：sheetId=${feishuResult.sheetId}，写入 ${feishuResult.rowsWritten} 行。`);
    }

    console.log('全部完成。');
  } catch (err) {
    console.error('运行出错：', err);
    process.exit(2);
  }
})();
