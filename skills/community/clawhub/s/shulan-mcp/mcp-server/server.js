#!/usr/bin/env node
/**
 * 数懒 MCP Server：把数据中台 REST API 包装为 MCP 工具，
 * 供 Claude Code / Cursor / ChatGPT 等客户端调用。
 *
 * 环境变量：
 *   SHULAN_API_KEY   必填，API Key（在网页「对外开放接入」页生成）
 *   SHULAN_BASE_URL  默认 http://127.0.0.1:8790
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const BASE = process.env.SHULAN_BASE_URL || "http://127.0.0.1:8790";
const KEY = process.env.SHULAN_API_KEY || "";

async function call(path, options = {}) {
  const headers = { "Content-Type": "application/json" };
  if (KEY) headers.Authorization = `Bearer ${KEY}`;
  const res = await fetch(`${BASE}${path}`, { ...options, headers });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
  return data;
}

const server = new McpServer({
  name: "shulan-data",
  version: "0.1.0",
});

server.tool("shulan_health", "检查数懒数据中台服务状态", {}, async () => {
  const d = await call("/v1/health");
  return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
});

server.tool(
  "shulan_create_task",
  "创建一次数据调研任务（自动扣费，多退少不补），返回任务ID",
  {
    question: z.string().describe("调研问题，如：广州新开茶餐厅探店博主精选与开业引流方案"),
    taskType: z.enum(["one_off", "subscription"]).optional().describe("任务类型"),
    dataSources: z.array(z.string()).optional().describe("数据源名称列表"),
    cost: z.number().optional().describe("预估点数（可选）"),
    frequency: z.enum(["每天", "每周", "每月"]).optional(),
  },
  async ({ question, taskType, dataSources, cost, frequency }) => {
    const d = await call("/v1/tasks", {
      method: "POST",
      body: JSON.stringify({ question, taskType, dataSources, cost, frequency }),
    });
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  }
);

server.tool(
  "shulan_get_task",
  "查询任务状态与报告（status: queued/running/done/failed）",
  { task_id: z.string() },
  async ({ task_id }) => {
    const d = await call(`/v1/tasks/${task_id}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  }
);

server.tool("shulan_market", "获取交付物市场列表", {}, async () => {
  const d = await call("/v1/market");
  const items = (d.items || []).map((i) => ({ id: i.id, title: i.title, price: i.price, sales: i.sales, category: i.categoryName }));
  return { content: [{ type: "text", text: JSON.stringify(items, null, 2) }] };
});

server.tool(
  "shulan_get_report",
  "获取报告详情（含 HTML/MD 链接与结构化数据）",
  { report_id: z.string() },
  async ({ report_id }) => {
    const d = await call(`/v1/reports/${report_id}`);
    return { content: [{ type: "text", text: JSON.stringify(d, null, 2) }] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
