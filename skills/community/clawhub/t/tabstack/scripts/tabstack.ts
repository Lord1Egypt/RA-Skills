#!/usr/bin/env npx tsx
/**
 * tabstack.ts — CLI wrapper for the Tabstack API (SDK v2)
 *
 * SDK v2 method signatures (all take options objects):
 *   client.extract.markdown({ url, metadata?, nocache?, geo_target? })
 *   client.extract.json({ url, json_schema?, nocache?, geo_target? })
 *   client.generate.json({ url, json_schema, instructions, nocache?, geo_target? })
 *   client.agent.automate({ task, url?, guardrails?, data?, maxIterations?, geo_target? })
 *   client.agent.research({ query, mode?, geo_target? })
 *
 * Usage:
 *   npx tsx tabstack.ts extract-markdown <url> [--metadata] [--nocache] [--geo CC]
 *   npx tsx tabstack.ts extract-json <url> [json_schema|@file] [--nocache] [--geo CC]
 *   npx tsx tabstack.ts generate <url> <json_schema|@file> <instructions> [--nocache] [--geo CC]
 *   npx tsx tabstack.ts automate <task> [--url <url>] [--max-iterations N] [--geo CC] [--guardrails "..."] [--data '{...}'|@file]
 *   npx tsx tabstack.ts research <query> [--mode fast|balanced] [--geo CC]
 *
 * Requires: TABSTACK_API_KEY env var
 */

import { readFileSync } from "fs";
import Tabstack from "@tabstack/sdk";

const apiKey = process.env.TABSTACK_API_KEY;
if (!apiKey) {
  console.error("ERROR: TABSTACK_API_KEY environment variable is not set.");
  process.exit(1);
}

const client = new Tabstack({ apiKey });

// ---------------------------------------------------------------------------
// Shared: parse --geo flag into geo_target option
// ---------------------------------------------------------------------------
function parseGeo(flags: Record<string, string | boolean>): object | undefined {
  const geo = flags.geo;
  if (typeof geo === "string") return { country: geo.toUpperCase() };
  return undefined;
}

// ---------------------------------------------------------------------------
// Shared: parse a JSON argument that may be inline JSON or @filepath
// ---------------------------------------------------------------------------
function parseJsonArg(arg: string, label: string): object {
  let raw = arg;
  if (arg.startsWith("@")) {
    const filePath = arg.slice(1);
    try {
      raw = readFileSync(filePath, "utf-8");
    } catch (e) {
      console.error(`ERROR: could not read ${label} file "${filePath}": ${e}`);
      process.exit(1);
    }
  }
  try {
    return JSON.parse(raw);
  } catch (e) {
    console.error(`ERROR: ${label} is not valid JSON: ${e}`);
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------
// extract-markdown
// ---------------------------------------------------------------------------
async function extractMarkdown(
  url: string,
  metadata: boolean,
  nocache: boolean,
  geo_target?: object
): Promise<void> {
  const body: any = { url };
  if (metadata) body.metadata = true;
  if (nocache) body.nocache = true;
  if (geo_target) body.geo_target = geo_target;

  const result = await client.extract.markdown(body);
  if (metadata && (result as any).metadata) {
    console.log("--- metadata ---");
    console.log(JSON.stringify((result as any).metadata, null, 2));
    console.log("--- content ---");
  }
  process.stdout.write((result as any).content ?? String(result));
}

// ---------------------------------------------------------------------------
// extract-json
// ---------------------------------------------------------------------------
async function extractJson(
  url: string,
  schemaArg?: string,
  nocache?: boolean,
  geo_target?: object
): Promise<void> {
  const body: any = { url };
  if (schemaArg) {
    body.json_schema = parseJsonArg(schemaArg, "json_schema");
  }
  if (nocache) body.nocache = true;
  if (geo_target) body.geo_target = geo_target;

  const result = await client.extract.json(body);
  console.log(JSON.stringify(result, null, 2));
}

// ---------------------------------------------------------------------------
// generate
// ---------------------------------------------------------------------------
async function generate(
  url: string,
  schemaArg: string,
  instructions: string,
  nocache: boolean,
  geo_target?: object
): Promise<void> {
  const json_schema = parseJsonArg(schemaArg, "json_schema");
  const body: any = { url, json_schema, instructions };
  if (nocache) body.nocache = true;
  if (geo_target) body.geo_target = geo_target;

  const result = await client.generate.json(body);
  console.log(JSON.stringify(result, null, 2));
}

// ---------------------------------------------------------------------------
// automate
// Returns an SSE stream. We iterate over events and print progress,
// then output the final answer.
// ---------------------------------------------------------------------------
async function automate(
  task: string,
  url?: string,
  maxIterations?: number,
  geo_target?: object,
  guardrails?: string,
  data?: object
): Promise<void> {
  const body: any = { task };
  if (url) body.url = url;
  if (maxIterations) body.maxIterations = maxIterations;
  if (geo_target) body.geo_target = geo_target;
  if (guardrails) body.guardrails = guardrails;
  if (data) body.data = data;

  const stream = await client.agent.automate(body);

  let finalAnswer: string | undefined;

  for await (const event of stream as any) {
    const eventType = event.event ?? event.type;
    const eventData = event.data ?? event;

    const get = (key: string) => {
      if (eventData && typeof eventData.get === "function") return eventData.get(key);
      if (eventData && typeof eventData === "object") return eventData[key];
      return undefined;
    };

    // SDK yields plain data objects without event type wrapper —
    // detect completion by checking for finalAnswer/report fields.
    const answer = get("finalAnswer") ?? get("report");
    if (answer) {
      finalAnswer = answer;
    } else if (get("reason")) {
      console.error(`[aborted] ${get("reason")}`);
    } else if (get("action")) {
      console.error(`[action] ${get("action")}`);
    } else {
      const msg = get("message");
      if (msg) console.error(`[automate] ${msg}`);
    }
  }

  if (finalAnswer) {
    process.stdout.write(finalAnswer);
  } else {
    console.error("ERROR: automate stream ended without a final answer.");
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------
// research
// New in SDK v2 — AI-powered web research with streaming progress.
// ---------------------------------------------------------------------------
async function research(
  query: string,
  mode?: string,
  geo_target?: object
): Promise<void> {
  const body: any = { query };
  if (mode) body.mode = mode;
  if (geo_target) body.geo_target = geo_target;

  const stream = await client.agent.research(body);

  let finalAnswer: string | undefined;

  for await (const event of stream as any) {
    const eventType = event.event ?? event.type;
    const eventData = event.data ?? event;

    const get = (key: string) => {
      if (eventData && typeof eventData.get === "function") return eventData.get(key);
      if (eventData && typeof eventData === "object") return eventData[key];
      return undefined;
    };

    // SDK yields plain data objects without event type wrapper —
    // detect completion by checking for report/finalAnswer/answer fields.
    const report = get("report") ?? get("finalAnswer") ?? get("answer");
    if (report) {
      finalAnswer = report;
    } else if (get("reason")) {
      console.error(`[aborted] ${get("reason")}`);
    } else {
      // Progress event
      const msg = get("message");
      if (msg) console.error(`[research] ${msg}`);
    }
  }

  if (finalAnswer) {
    process.stdout.write(finalAnswer);
  } else {
    console.error("ERROR: research stream ended without a final answer.");
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------
// Error handling
// ---------------------------------------------------------------------------
function handleError(error: unknown): never {
  const msg = error instanceof Error ? error.message : String(error);
  console.error(`ERROR: ${msg}`);
  process.exit(1);
}

// ---------------------------------------------------------------------------
// CLI dispatch
// ---------------------------------------------------------------------------
function parseFlags(args: string[]): {
  positional: string[];
  flags: Record<string, string | boolean>;
} {
  const positional: string[] = [];
  const flags: Record<string, string | boolean> = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--")) {
      const key = args[i].slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith("--")) {
        flags[key] = next;
        i++;
      } else {
        flags[key] = true;
      }
    } else {
      positional.push(args[i]);
    }
  }
  return { positional, flags };
}

async function main(): Promise<void> {
  const [command, ...rest] = process.argv.slice(2);
  const { positional, flags } = parseFlags(rest);
  const geo_target = parseGeo(flags);

  switch (command) {
    case "extract-markdown": {
      const [url] = positional;
      if (!url) {
        console.error("Usage: tabstack.ts extract-markdown <url> [--metadata] [--nocache] [--geo CC]");
        process.exit(1);
      }
      await extractMarkdown(url, !!flags.metadata, !!flags.nocache, geo_target).catch(handleError);
      break;
    }

    case "extract-json": {
      const [url, schema] = positional;
      if (!url) {
        console.error("Usage: tabstack.ts extract-json <url> [json_schema] [--nocache] [--geo CC]");
        process.exit(1);
      }
      await extractJson(url, schema, !!flags.nocache, geo_target).catch(handleError);
      break;
    }

    case "generate": {
      const [url, schema, ...instrParts] = positional;
      const instructions = instrParts.join(" ");
      if (!url || !schema || !instructions) {
        console.error("Usage: tabstack.ts generate <url> <json_schema> <instructions> [--nocache] [--geo CC]");
        process.exit(1);
      }
      await generate(url, schema, instructions, !!flags.nocache, geo_target).catch(handleError);
      break;
    }

    case "automate": {
      const task = positional.join(" ");
      if (!task) {
        console.error("Usage: tabstack.ts automate <task> [--url <url>] [--max-iterations N] [--geo CC] [--guardrails \"...\"] [--data '{...}']");
        process.exit(1);
      }
      const url = flags.url as string | undefined;
      const maxIter = flags["max-iterations"]
        ? parseInt(flags["max-iterations"] as string, 10)
        : undefined;
      const guardrails = flags.guardrails as string | undefined;
      let data: object | undefined;
      if (typeof flags.data === "string") {
        data = parseJsonArg(flags.data, "--data");
      }
      await automate(task, url, maxIter, geo_target, guardrails, data).catch(handleError);
      break;
    }

    case "research": {
      const query = positional.join(" ");
      if (!query) {
        console.error("Usage: tabstack.ts research <query> [--mode fast|balanced] [--geo CC]");
        process.exit(1);
      }
      const mode = flags.mode as string | undefined;
      await research(query, mode, geo_target).catch(handleError);
      break;
    }

    default:
      console.error(`Unknown command: ${command ?? "(none)"}`);
      console.error("Commands: extract-markdown | extract-json | generate | automate | research");
      process.exit(1);
  }
}

main();
