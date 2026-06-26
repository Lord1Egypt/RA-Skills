#!/usr/bin/env node
import { readFileSync } from "node:fs";
import path from "node:path";
import { getSupportedActions, runOpenClawSkill, validateOpenClawSkillRequest, type OpenClawSkillRequest } from "./index";

function readStdin(): Promise<string> {
  return new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => {
      data += chunk;
    });
    process.stdin.on("end", () => resolve(data));
    process.stdin.on("error", reject);
  });
}

interface CliArgs {
  input?: string;
  file?: string;
  action?: string;
  payload?: string;
  payloadFile?: string;
  help?: boolean;
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {};

  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];
    if (current === "--input") args.input = argv[index + 1];
    if (current === "--file") args.file = argv[index + 1];
    if (current === "--action") args.action = argv[index + 1];
    if (current === "--payload") args.payload = argv[index + 1];
    if (current === "--payload-file") args.payloadFile = argv[index + 1];
    if (current === "--help" || current === "-h") args.help = true;
  }

  return args;
}

function printHelp(): void {
  const scriptName = path.basename(process.argv[1] ?? "openclaw.js");
  process.stdout.write(
    [
      `Usage: node dist/${scriptName} [options]`,
      "",
      "Options:",
      "  --input <json>         Full request JSON string",
      "  --file <path>          Full request JSON file",
      `  --action <name>        Action name: ${getSupportedActions().join(" | ")}`,
      "  --payload <json>       Payload JSON string for the selected action",
      "  --payload-file <path>  Payload JSON file for the selected action",
      "  --help, -h             Show help",
      "",
      "Examples:",
      "  node dist/openclaw.js --input '{\"action\":\"script\",\"payload\":{\"topic\":\"测试主题\"}}'",
      "  node dist/openclaw.js --action script --payload '{\"topic\":\"测试主题\"}'",
    ].join("\n"),
  );
}

async function resolveRequest(): Promise<OpenClawSkillRequest> {
  const { input, file, action, payload, payloadFile, help } = parseArgs(process.argv.slice(2));

  if (help) {
    printHelp();
    process.exit(0);
  }

  if (input) {
    return validateOpenClawSkillRequest(JSON.parse(input));
  }

  if (file) {
    return validateOpenClawSkillRequest(JSON.parse(readFileSync(file, "utf8")));
  }

  if (action && (payload || payloadFile)) {
    const resolvedPayload = payload
      ? JSON.parse(payload)
      : JSON.parse(readFileSync(payloadFile as string, "utf8"));

    return validateOpenClawSkillRequest({
      action,
      payload: resolvedPayload,
    });
  }

  const stdin = await readStdin();
  if (!stdin.trim()) {
    throw new Error("Missing skill input. Provide --input, --file, --action with --payload/--payload-file, or JSON via stdin.");
  }

  return validateOpenClawSkillRequest(JSON.parse(stdin));
}

async function main(): Promise<void> {
  const request = await resolveRequest();
  const result = await runOpenClawSkill(request);
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

if (require.main === module) {
  main().catch((error: unknown) => {
    const message = error instanceof Error ? error.message : String(error);
    process.stderr.write(`${message}\n`);
    process.exitCode = 1;
  });
}
