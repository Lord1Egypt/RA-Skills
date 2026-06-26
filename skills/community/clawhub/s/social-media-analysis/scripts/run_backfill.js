#!/usr/bin/env node
/**
 * social-media-analysis 的 Clawhub 自动执行入口：
 * 依次运行两个回填脚本：
 * 1) backfill-content-analysis-by-source.js（非新浪微博渠道）
 * 2) backfill-weibo-content-analysis.js（新浪微博渠道）
 */

const { spawn } = require("child_process");
const path = require("path");

function runNode(scriptFile) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [scriptFile], {
      stdio: "inherit",
      env: process.env,
    });
    child.on("error", reject);
    child.on("exit", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`script_failed=${path.basename(scriptFile)} exit_code=${code}`));
    });
  });
}

async function main() {
  const smoke = ["1", "true", "yes"].includes(
    String(process.env.RUN_SMOKE_TEST || "").trim().toLowerCase()
  );

  if (smoke) {
    const tests = [
      {
        script: "backfill-content-analysis-by-source.js",
        env: { TEST_CHANNEL: "抖音APP", TEST_URL: "https://www.douyin.com/share/video/7621027680988917926" },
      },
      {
        script: "backfill-content-analysis-by-source.js",
        env: { TEST_CHANNEL: "快手APP", TEST_URL: "https://www.kuaishou.com/short-video/3xuyqtb4mxdy4jc" },
      },
      {
        script: "backfill-content-analysis-by-source.js",
        env: { TEST_CHANNEL: "小红书APP", TEST_URL: "https://www.xiaohongshu.com/explore/69c3530f00000000220255d4" },
      },
      {
        script: "backfill-content-analysis-by-source.js",
        env: { TEST_CHANNEL: "酷安APP", TEST_URL: "https://www.coolapk.com/feed/70874324?s=OWNjZGIzYzYwZzY5YzM1NTRlega1603" },
      },
      {
        script: "backfill-content-analysis-by-source.js",
        env: { TEST_CHANNEL: "今日头条", TEST_URL: "http://www.toutiao.com/item/1860602228145289" },
      },
      {
        script: "backfill-weibo-content-analysis.js",
        env: { TEST_SOURCE_CHANNEL: "新浪微博", TEST_URL: "https://weibo.com/3047053367/QxHoSdUEx" },
      },
    ];

    const dir = __dirname;
    for (const t of tests) {
      const scriptFile = path.join(dir, t.script);
      const childEnv = { ...process.env, ...t.env };
      await new Promise((resolve, reject) => {
        const child = require("child_process").spawn(process.execPath, [scriptFile], {
          stdio: "inherit",
          env: childEnv,
        });
        child.on("error", reject);
        child.on("exit", (code) => {
          if (code === 0) resolve();
          else reject(new Error(`smoke_failed=${t.script} exit_code=${code}`));
        });
      });
    }
    return;
  }

  const dir = __dirname;
  const multi = path.join(dir, "backfill-content-analysis-by-source.js");
  const weibo = path.join(dir, "backfill-weibo-content-analysis.js");

  await runNode(multi);
  await runNode(weibo);
}

main().catch((e) => {
  console.error(String(e && e.message ? e.message : e));
  process.exit(1);
});

