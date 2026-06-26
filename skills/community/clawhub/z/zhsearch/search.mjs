#!/usr/bin/env node

import os from "node:os";
import fs from "node:fs";
import path from "node:path";
import { program } from "commander";
import { charge, getBalance, getPaymentLink } from "./lib/billing.mjs";
import { searchBaidu } from "./lib/baidu.mjs";
import { searchZhihu } from "./lib/zhihu.mjs";
import { searchWechat } from "./lib/wechat.mjs";
import { mergeResults, formatForAgent } from "./lib/merge.mjs";

function resolveCallerId() {
  if (process.env.OPENCLAW_CALLER_ID) return process.env.OPENCLAW_CALLER_ID;
  if (process.env.OPENCLAW_AGENT_ID) return process.env.OPENCLAW_AGENT_ID;

  const candidates = [
    path.join(os.homedir(), ".openclaw", "identity", "device.json"),
    process.env.OPENCLAW_STATE_DIR
      ? path.join(process.env.OPENCLAW_STATE_DIR, "identity", "device.json")
      : null,
  ].filter(Boolean);

  for (const fp of candidates) {
    try {
      const data = JSON.parse(fs.readFileSync(fp, "utf8"));
      if (data.deviceId) return data.deviceId;
    } catch { /* ignore */ }
  }

  return `${os.hostname()}-${os.userInfo().username}`;
}

const VALID_SOURCES = ["baidu", "zhihu", "wechat"];

const searchFns = {
  baidu: searchBaidu,
  zhihu: searchZhihu,
  wechat: searchWechat,
};

program
  .name("zhsearch")
  .description("Chinese search enhancement - Baidu, Zhihu, WeChat articles")
  .argument("<query>", "Search keywords")
  .option("-s, --sources <sources>", "Comma-separated sources: baidu,zhihu,wechat", "baidu,zhihu,wechat")
  .option("-n, --limit <count>", "Results per source", "5")
  .option("--no-billing", "Skip billing (for local testing only)")
  .action(async (query, opts) => {
    const sources = opts.sources
      .split(",")
      .map((s) => s.trim().toLowerCase())
      .filter((s) => VALID_SOURCES.includes(s));

    if (sources.length === 0) {
      console.error(JSON.stringify({ error: `Invalid sources. Valid: ${VALID_SOURCES.join(", ")}` }));
      process.exit(1);
    }

    const limit = Math.min(Math.max(parseInt(opts.limit, 10) || 5, 1), 20);

    if (opts.billing !== false) {
      const callerId = resolveCallerId();
      const bill = await charge(callerId);
      if (!bill.success) {
        const output = {
          error: "Payment required",
          query,
          balance: bill.balance,
        };
        if (bill.payment_url) {
          output.payment_url = bill.payment_url;
          output.message = `Insufficient balance. Please top up: ${bill.payment_url}`;
        } else {
          const link = await getPaymentLink(callerId);
          if (link.success && link.payment_url) {
            output.payment_url = link.payment_url;
            output.message = `Insufficient balance. Please top up (min 8 USDT): ${link.payment_url}`;
          } else {
            output.message = bill.error || "Charge failed. Please try again later.";
          }
        }
        console.log(JSON.stringify(output, null, 2));
        process.exit(0);
      }
    }

    const sourceResults = {};
    const errors = {};

    const tasks = sources.map(async (src) => {
      try {
        sourceResults[src] = await searchFns[src](query, limit);
      } catch (err) {
        errors[src] = err.message;
        sourceResults[src] = [];
      }
    });

    await Promise.all(tasks);

    const merged = mergeResults(sourceResults);
    const output = formatForAgent(merged, query);

    if (Object.keys(errors).length > 0) {
      const parsed = JSON.parse(output);
      parsed.errors = errors;
      console.log(JSON.stringify(parsed, null, 2));
    } else {
      console.log(output);
    }
  });

program.parse();
