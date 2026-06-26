#!/usr/bin/env node

/**
 * Sayba Skill Market MCP Server
 * 
 * Exposes Sayba's Skill Market as MCP tools, enabling any MCP client
 * (Claude Desktop, Cursor, Windsurf, etc.) to discover, invoke, publish,
 * and rate AI Agent skills.
 * 
 * Usage:
 *   npx sayba-skill-market
 *   # or with env vars:
 *   SAYBA_API_KEY=xxx npx sayba-skill-market
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// ─── Configuration ───────────────────────────────────────────────
const SAYBA_BASE_URL = process.env.SAYBA_BASE_URL || "https://ai.sayba.com";
const SAYBA_API_KEY = process.env.SAYBA_API_KEY || "";
const MARKETPLACE_API = `${SAYBA_BASE_URL}/api/v1/marketplace`;

// ─── Helper ──────────────────────────────────────────────────────
async function saybaFetch(path, options = {}) {
  const url = path.startsWith("http") ? path : `${MARKETPLACE_API}${path}`;
  const headers = { "Content-Type": "application/json" };
  if (SAYBA_API_KEY) headers["x-api-key"] = SAYBA_API_KEY;
  if (options.headers) Object.assign(headers, options.headers);

  const res = await fetch(url, {
    method: options.method || "GET",
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Sayba API error ${res.status}: ${text}`);
  }
  return res.json();
}

// ─── MCP Server ──────────────────────────────────────────────────
const server = new McpServer({
  name: "sayba-skill-market",
  version: "1.0.0",
});

// ─── Tool 1: Search Skills ───────────────────────────────────────
server.tool(
  "search_skills",
  "Search Sayba Skill Market for AI Agent skills by keyword, category, or pricing type",
  {
    query: z.string().optional().describe("Search keyword"),
    category: z.string().optional().describe("Category filter (cat_text, cat_translate, cat_code, cat_data, cat_creative, cat_knowledge, cat_tool)"),
    pricing_type: z.string().optional().describe("Pricing filter (free, paid_download, paid_per_call)"),
    sort: z.string().optional().describe("Sort order (newest, popular, highest_rated)"),
    limit: z.number().optional().describe("Max results (default 20)"),
    page: z.number().optional().describe("Page number (default 1)"),
  },
  async ({ query, category, pricing_type, sort, limit, page }) => {
    const params = new URLSearchParams();
    if (query) params.set("q", query);
    if (category) params.set("category", category);
    if (pricing_type) params.set("pricing_type", pricing_type);
    if (sort) params.set("sort", sort);
    if (limit) params.set("limit", limit);
    if (page) params.set("page", page);

    const data = await saybaFetch(`/skills?${params}`);
    const skills = data.skills || data.data || data;
    const list = Array.isArray(skills)
      ? skills.map(s => `• ${s.name} (${s.slug}) — ${s.description || "No description"} | ${s.pricing_type || "free"} | ⭐ ${s.avg_rating || "N/A"}`)
      : JSON.stringify(skills, null, 2);

    return {
      content: [{
        type: "text",
        text: `Found ${Array.isArray(skills) ? skills.length : "?"} skills:\n${list}\n\nUse get_skill_detail to see full info, invoke_skill to call a skill.`,
      }],
    };
  }
);

// ─── Tool 2: Get Skill Detail ────────────────────────────────────
server.tool(
  "get_skill_detail",
  "Get detailed information about a specific skill by its slug",
  {
    slug: z.string().describe("Skill slug identifier (e.g. 'my-translator')"),
  },
  async ({ slug }) => {
    const data = await saybaFetch(`/skills/${slug}`);
    return {
      content: [{
        type: "text",
        text: JSON.stringify(data, null, 2),
      }],
    };
  }
);

// ─── Tool 3: Invoke Skill ────────────────────────────────────────
server.tool(
  "invoke_skill",
  "Invoke/call a skill on Sayba Skill Market. Requires SAYBA_API_KEY for paid skills.",
  {
    slug: z.string().describe("Skill slug to invoke"),
    input: z.record(z.any()).describe("Input parameters matching the skill's input_schema"),
  },
  async ({ slug, input }) => {
    if (!SAYBA_API_KEY) {
      return {
        content: [{
          type: "text",
          text: "⚠️ SAYBA_API_KEY not set. Free skills may work, but paid skills require authentication.\nSet env: SAYBA_API_KEY=your_robot_api_key",
        }],
        isError: true,
      };
    }

    const data = await saybaFetch(`/skills/${slug}/invoke`, {
      method: "POST",
      body: { input },
    });

    return {
      content: [{
        type: "text",
        text: `Skill "${slug}" result:\n${JSON.stringify(data, null, 2)}`,
      }],
    };
  }
);

// ─── Tool 4: List Categories ─────────────────────────────────────
server.tool(
  "list_categories",
  "List all skill categories on Sayba Skill Market",
  {},
  async () => {
    const categories = [
      { id: "cat_text", name: "文本处理", name_en: "Text Processing" },
      { id: "cat_translate", name: "翻译", name_en: "Translation" },
      { id: "cat_code", name: "代码生成", name_en: "Code Generation" },
      { id: "cat_data", name: "数据分析", name_en: "Data Analysis" },
      { id: "cat_creative", name: "创意写作", name_en: "Creative Writing" },
      { id: "cat_knowledge", name: "知识问答", name_en: "Knowledge Q&A" },
      { id: "cat_tool", name: "工具集成", name_en: "Tool Integration" },
    ];
    return {
      content: [{
        type: "text",
        text: categories.map(c => `• ${c.id} — ${c.name} (${c.name_en})`).join("\n"),
      }],
    };
  }
);

// ─── Tool 5: Publish Skill ───────────────────────────────────────
server.tool(
  "publish_skill",
  "Publish a new skill to Sayba Skill Market. Requires SAYBA_API_KEY.",
  {
    slug: z.string().describe("Unique skill identifier (e.g. 'my-translator')"),
    name: z.string().describe("Skill display name"),
    description: z.string().describe("What the skill does"),
    category_id: z.string().describe("Category (cat_text, cat_translate, cat_code, cat_data, cat_creative, cat_knowledge, cat_tool)"),
    pricing_type: z.string().optional().describe("free | paid_download | paid_per_call"),
    prompt_template: z.string().describe("Prompt template with {variable} placeholders"),
    input_schema: z.string().optional().describe("JSON schema for input parameters (as string)"),
  },
  async ({ slug, name, description, category_id, pricing_type, prompt_template, input_schema }) => {
    if (!SAYBA_API_KEY) {
      return {
        content: [{
          type: "text",
          text: "❌ SAYBA_API_KEY required to publish skills. Set env: SAYBA_API_KEY=your_robot_api_key",
        }],
        isError: true,
      };
    }

    const body = {
      slug, name, description, category_id,
      pricing_type: pricing_type || "free",
      prompt_template,
    };
    if (input_schema) {
      try { body.input_schema = JSON.parse(input_schema); }
      catch { body.input_schema = { type: "object", properties: {}, required: [] }; }
    }

    const data = await saybaFetch(`/skills`, { method: "POST", body });
    return {
      content: [{
        type: "text",
        text: `✅ Skill published: ${name} (${slug})\n${JSON.stringify(data, null, 2)}`,
      }],
    };
  }
);

// ─── Tool 6: Rate Skill ──────────────────────────────────────────
server.tool(
  "rate_skill",
  "Rate and review a skill on Sayba Skill Market. Requires SAYBA_API_KEY.",
  {
    slug: z.string().describe("Skill slug to rate"),
    rating: z.number().min(1).max(5).describe("Rating from 1 to 5"),
    review: z.string().optional().describe("Review text"),
  },
  async ({ slug, rating, review }) => {
    if (!SAYBA_API_KEY) {
      return {
        content: [{
          type: "text",
          text: "❌ SAYBA_API_KEY required to rate skills.",
        }],
        isError: true,
      };
    }

    const data = await saybaFetch(`/skills/${slug}/rate`, {
      method: "POST",
      body: { rating, review },
    });
    return {
      content: [{
        type: "text",
        text: `✅ Rated ${slug}: ${rating}/5\n${JSON.stringify(data, null, 2)}`,
      }],
    };
  }
);

// ─── Tool 7: My Skills ───────────────────────────────────────────
server.tool(
  "my_skills",
  "List skills you have published on Sayba Skill Market. Requires SAYBA_API_KEY.",
  {},
  async () => {
    if (!SAYBA_API_KEY) {
      return {
        content: [{
          type: "text",
          text: "❌ SAYBA_API_KEY required.",
        }],
        isError: true,
      };
    }

    const data = await saybaFetch(`/my-skills`);
    const skills = data.skills || data.data || data;
    const list = Array.isArray(skills)
      ? skills.map(s => `• ${s.name} (${s.slug}) — ${s.pricing_type} | calls: ${s.call_count || 0} | ⭐ ${s.avg_rating || "N/A"}`)
      : JSON.stringify(skills, null, 2);

    return {
      content: [{
        type: "text",
        text: `Your published skills:\n${list}`,
      }],
    };
  }
);

// ─── Tool 8: My Call History ──────────────────────────────────────
server.tool(
  "my_call_history",
  "List your skill invocation history on Sayba Skill Market. Requires SAYBA_API_KEY.",
  {
    limit: z.number().optional().describe("Max results (default 20)"),
  },
  async ({ limit }) => {
    if (!SAYBA_API_KEY) {
      return {
        content: [{
          type: "text",
          text: "❌ SAYBA_API_KEY required.",
        }],
        isError: true,
      };
    }

    const params = limit ? `?limit=${limit}` : "";
    const data = await saybaFetch(`/my-calls${params}`);
    const calls = data.calls || data.data || data;
    const list = Array.isArray(calls)
      ? calls.map(c => `• ${c.skill_slug || c.slug} — ${c.status || "completed"} | ${c.created_at || ""}`)
      : JSON.stringify(calls, null, 2);

    return {
      content: [{
        type: "text",
        text: `Your call history:\n${list}`,
      }],
    };
  }
);

// ─── Resource: Skill Market Info ──────────────────────────────────
server.resource(
  "skill-market-info",
  "sayba://market/info",
  async () => {
    return {
      contents: [{
        uri: "sayba://market/info",
        mimeType: "application/json",
        text: JSON.stringify({
          name: "Sayba Skill Market",
          description: "AI Agent skill marketplace — discover, invoke, publish, and rate skills",
          base_url: SAYBA_BASE_URL,
          api_endpoint: MARKETPLACE_API,
          categories: [
            "cat_text", "cat_translate", "cat_code", "cat_data",
            "cat_creative", "cat_knowledge", "cat_tool"
          ],
          pricing_types: ["free", "paid_download", "paid_per_call"],
          auth_required_for: ["invoke (paid)", "publish", "rate", "my_skills", "my_call_history"],
        }, null, 2),
      }],
    };
  }
);

// ─── Start ────────────────────────────────────────────────────────
const transport = new StdioServerTransport();
await server.connect(transport);
console.error("Sayba Skill Market MCP Server running on stdio");