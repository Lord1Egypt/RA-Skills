#!/usr/bin/env node

/**
 * 云效 MCP 客户端 CLI - 面向 AI agent
 *
 * 用法:
 *   yunxiao [--url <url>] [--debug] list                     # Markdown 表格：工具名 + 描述
 *   yunxiao [--url <url>] [--debug] schema <tool>             # JSON：单个工具的完整定义（含 inputSchema）
 *   yunxiao [--url <url>] [--debug] call <tool> [json_args]   # JSON：工具调用结果
 *   yunxiao [--url <url>] [--debug] call <tool> --stdin        # 从 stdin 读取 JSON 参数
 *
 * 输出约定:
 *   list   → stdout Markdown 表格（省 token）
 *   schema → stdout JSON（按需获取单个工具参数定义）
 *   call   → stdout JSON（业务数据）
 *   --debug → stderr 显示连接/请求日志
 *
 * 退出码:
 *   0 = 成功
 *   1 = 工具调用失败 / 参数错误
 *   2 = 连接失败
 */

import { createClient } from './client.mjs';

function outputJson(data) {
  console.log(JSON.stringify(data, null, 2));
}

function outputError(message) {
  console.log(JSON.stringify({ error: message }));
}

function outputToolsTable(tools) {
  const lines = [];
  lines.push('| Tool | Description |');
  lines.push('|------|-------------|');
  for (const tool of tools) {
    // collapse multiline descriptions to single line, strip markdown noise
    let desc = tool.description
      .split('\n')[0]             // keep only the first line
      .replace(/\|/g, '\\|')     // escape pipes
      .replace(/[*_`#]/g, '')    // strip markdown formatting chars
      .trim();
    if (desc.length > 120) {
      desc = desc.slice(0, 117) + '...';
    }
    lines.push(`| ${tool.name} | ${desc} |`);
  }
  console.log(lines.join('\n'));
}

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk) => { data += chunk; });
    process.stdin.on('end', () => resolve(data.trim()));
    process.stdin.on('error', reject);
  });
}

function parseArgs(argv) {
  const args = argv.slice(2);
  let url = 'http://localhost:3000';
  let useStdin = false;
  let debug = false;
  const positional = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--url' && i + 1 < args.length) {
      url = args[++i];
    } else if (args[i] === '--stdin') {
      useStdin = true;
    } else if (args[i] === '--debug' || args[i] === '-d') {
      debug = true;
    } else if (args[i] === '--help' || args[i] === '-h') {
      printUsage();
      process.exit(0);
    } else {
      positional.push(args[i]);
    }
  }

  const command = positional[0] || null;
  const toolName = positional[1] || null;
  const toolArgs = positional[2] || null;

  return { url, command, toolName, toolArgs, useStdin, debug };
}

function printUsage() {
  console.error(`Usage:
  yunxiao [--url <url>] [--debug] list
  yunxiao [--url <url>] [--debug] schema <tool>
  yunxiao [--url <url>] [--debug] call <tool> [json_args]
  yunxiao [--url <url>] [--debug] call <tool> --stdin

Commands:
  list            List all tools (Markdown table)
  schema <tool>   Show tool definition with inputSchema (JSON)
  call <tool>     Call a tool and return result (JSON)

Options:
  --url <url>   MCP Server address (default: http://localhost:3000)
  --stdin       Read tool arguments from stdin (JSON)
  --debug, -d   Show debug logs (stderr)
  -h, --help    Show this help

Exit codes:
  0  Success
  1  Tool call failed / invalid arguments
  2  Connection failed`);
}

async function main() {
  const { url, command, toolName, toolArgs, useStdin, debug } = parseArgs(process.argv);

  if (!command) {
    printUsage();
    process.exit(1);
  }

  // 连接客户端
  let client;
  try {
    client = await createClient(url, { debug });
  } catch (e) {
    outputError(`connection failed: ${e.message}`);
    process.exit(2);
  }

  if (!client.tools.length) {
    outputError('no tools available, check if MCP Server is running');
    await client.close();
    process.exit(2);
  }

  try {
    if (command === 'list') {
      outputToolsTable(client.listTools());

    } else if (command === 'schema') {
      if (!toolName) {
        outputError('missing tool name. Usage: yunxiao schema <tool>');
        process.exit(1);
      }
      const tool = client.tools.find((t) => t.name === toolName);
      if (!tool) {
        outputError(`tool not found: ${toolName}`);
        process.exit(1);
      }
      outputJson(tool);

    } else if (command === 'call') {
      if (!toolName) {
        outputError('missing tool name. Usage: yunxiao call <tool> [json_args]');
        process.exit(1);
      }

      let args = {};
      if (useStdin) {
        const raw = await readStdin();
        if (raw) {
          try {
            args = JSON.parse(raw);
          } catch {
            outputError(`invalid JSON from stdin: ${raw.slice(0, 200)}`);
            process.exit(1);
          }
        }
      } else if (toolArgs) {
        try {
          args = JSON.parse(toolArgs);
        } catch {
          outputError(`invalid JSON argument: ${toolArgs.slice(0, 200)}`);
          process.exit(1);
        }
      }

      const result = await client.callTool(toolName, args);
      if (result === null) {
        outputError(`tool call failed: ${toolName}`);
        process.exit(1);
      }
      outputJson(result);

    } else {
      outputError(`unknown command: ${command}. Use 'list', 'schema', or 'call'.`);
      process.exit(1);
    }
  } finally {
    await client.close();
  }
}

main().catch((e) => {
  outputError(`unexpected error: ${e.message}`);
  process.exit(1);
});
