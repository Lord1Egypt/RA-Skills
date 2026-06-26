#!/usr/bin/env node

/**
 * Reach MCP Server — exposes Reach primitives as MCP tools
 * for direct use from Claude Code.
 *
 * Protocol: JSON-RPC over stdio (MCP standard)
 *
 * Tools exposed:
 *   web_fetch      — Fetch content from URL (HTTP or browser)
 *   web_act        — Interact with web page (click, type, submit)
 *   web_authenticate — Login to a service
 *   web_sign       — Sign a message or transaction
 *   web_see        — Screenshot + accessibility tree extraction
 *   web_email      — Send email via Resend
 */

import dotenv from 'dotenv';
dotenv.config();

import { fetch } from './primitives/fetch.js';
import { act } from './primitives/act.js';
import { authenticate } from './primitives/authenticate.js';
import { sign } from './primitives/sign.js';
import { see } from './primitives/see.js';
import { sendEmail } from './primitives/email.js';
import pool from './browser.js';

const SERVER_NAME = 'reach';
const SERVER_VERSION = '0.1.0';

// Tool definitions
const TOOLS = [
  {
    name: 'web_fetch',
    description: 'Fetch content from a URL. Tries HTTP first, falls back to browser for JS-rendered sites. Returns markdown, HTML, JSON, or screenshot.',
    inputSchema: {
      type: 'object',
      properties: {
        url: { type: 'string', description: 'URL to fetch' },
        format: { type: 'string', enum: ['markdown', 'html', 'json', 'screenshot'], description: 'Output format (default: markdown)' },
        javascript: { type: 'boolean', description: 'Force browser rendering (default: false)' },
        session: { type: 'string', description: 'Session/cookie domain to use for authenticated fetches' },
      },
      required: ['url'],
    },
  },
  {
    name: 'web_act',
    description: 'Interact with a web page — click elements, type text, submit forms, select options, scroll.',
    inputSchema: {
      type: 'object',
      properties: {
        url: { type: 'string', description: 'URL to interact with' },
        action: { type: 'string', enum: ['click', 'type', 'submit', 'select', 'scroll'], description: 'Action to perform' },
        selector: { type: 'string', description: 'CSS selector for the target element' },
        text: { type: 'string', description: 'Text to match (for click) or type (for type)' },
        data: { type: 'object', description: 'Form data object for submit action' },
        session: { type: 'string', description: 'Session domain for authenticated interactions' },
      },
      required: ['url', 'action'],
    },
  },
  {
    name: 'web_authenticate',
    description: 'Authenticate with a web service. Supports cookie reuse, browser-based login, and API key auth.',
    inputSchema: {
      type: 'object',
      properties: {
        service: { type: 'string', description: 'Service name (e.g., cantina, upwork)' },
        method: { type: 'string', enum: ['cookie', 'login', 'apikey'], description: 'Auth method' },
        url: { type: 'string', description: 'Login page URL (for login method)' },
        email: { type: 'string', description: 'Email/username (for login method)' },
        password: { type: 'string', description: 'Password (for login method)' },
        apiKey: { type: 'string', description: 'API key (for apikey method)' },
        headerName: { type: 'string', description: 'Header name for API key (default: Authorization)' },
      },
      required: ['service', 'method'],
    },
  },
  {
    name: 'web_sign',
    description: 'Sign a message, transaction, or EIP-712 typed data with the configured wallet.',
    inputSchema: {
      type: 'object',
      properties: {
        payload: { description: 'Message string, transaction object, or typed data object' },
        type: { type: 'string', enum: ['message', 'transaction', 'typed'], description: 'Sign type (default: message)' },
      },
      required: ['payload'],
    },
  },
  {
    name: 'web_see',
    description: 'Take a screenshot and extract accessibility tree + interactive elements from a web page. Returns structured page data for visual reasoning.',
    inputSchema: {
      type: 'object',
      properties: {
        url: { type: 'string', description: 'URL to capture' },
        question: { type: 'string', description: 'Optional context about what to look for' },
      },
      required: ['url'],
    },
  },
  {
    name: 'web_email',
    description: 'Send an email via Resend API from ollie@exoagent.xyz. Supports plain text and HTML.',
    inputSchema: {
      type: 'object',
      properties: {
        to: { type: 'string', description: 'Recipient email address' },
        subject: { type: 'string', description: 'Email subject' },
        body: { type: 'string', description: 'Email body (plain text or HTML)' },
        html: { type: 'boolean', description: 'Treat body as HTML (default: auto-detect)' },
        replyTo: { type: 'string', description: 'Reply-to address' },
      },
      required: ['to', 'subject', 'body'],
    },
  },
];

// Handle incoming JSON-RPC messages over stdio
let buffer = '';

process.stdin.setEncoding('utf-8');
process.stdin.on('data', (chunk) => {
  buffer += chunk;
  processBuffer();
});

function processBuffer() {
  // MCP uses Content-Length header framing
  while (true) {
    const headerEnd = buffer.indexOf('\r\n\r\n');
    if (headerEnd === -1) break;

    const header = buffer.substring(0, headerEnd);
    const contentLengthMatch = header.match(/Content-Length: (\d+)/i);
    if (!contentLengthMatch) {
      // Skip malformed header
      buffer = buffer.substring(headerEnd + 4);
      continue;
    }

    const contentLength = parseInt(contentLengthMatch[1], 10);
    const bodyStart = headerEnd + 4;

    if (buffer.length < bodyStart + contentLength) break; // Incomplete body

    const body = buffer.substring(bodyStart, bodyStart + contentLength);
    buffer = buffer.substring(bodyStart + contentLength);

    try {
      const message = JSON.parse(body);
      handleMessage(message);
    } catch (e) {
      sendError(null, -32700, `Parse error: ${e.message}`);
    }
  }
}

function sendResponse(id, result) {
  const response = JSON.stringify({ jsonrpc: '2.0', id, result });
  const header = `Content-Length: ${Buffer.byteLength(response)}\r\n\r\n`;
  process.stdout.write(header + response);
}

function sendError(id, code, message) {
  const response = JSON.stringify({ jsonrpc: '2.0', id, error: { code, message } });
  const header = `Content-Length: ${Buffer.byteLength(response)}\r\n\r\n`;
  process.stdout.write(header + response);
}

async function handleMessage(message) {
  const { id, method, params } = message;

  try {
    switch (method) {
      case 'initialize':
        sendResponse(id, {
          protocolVersion: '2024-11-05',
          capabilities: { tools: {} },
          serverInfo: { name: SERVER_NAME, version: SERVER_VERSION },
        });
        break;

      case 'initialized':
        // Notification — no response needed
        break;

      case 'tools/list':
        sendResponse(id, { tools: TOOLS });
        break;

      case 'tools/call':
        await handleToolCall(id, params);
        break;

      case 'shutdown':
        await pool.close();
        sendResponse(id, null);
        break;

      default:
        sendError(id, -32601, `Method not found: ${method}`);
    }
  } catch (e) {
    sendError(id, -32603, `Internal error: ${e.message}`);
  }
}

async function handleToolCall(id, params) {
  const { name, arguments: args } = params;

  try {
    let result;

    switch (name) {
      case 'web_fetch': {
        result = await fetch(args.url, {
          format: args.format,
          javascript: args.javascript,
          session: args.session,
        });
        break;
      }

      case 'web_act': {
        result = await act(args.url, args.action, {
          selector: args.selector,
          text: args.text,
          data: args.data,
          session: args.session,
        });
        break;
      }

      case 'web_authenticate': {
        result = await authenticate(args.service, args.method, {
          url: args.url,
          email: args.email,
          password: args.password,
          apiKey: args.apiKey,
          headerName: args.headerName,
        });
        break;
      }

      case 'web_sign': {
        result = await sign(args.payload, { type: args.type });
        break;
      }

      case 'web_see': {
        result = await see(args.url, args.question);
        break;
      }

      case 'web_email': {
        result = await sendEmail(args.to, args.subject, args.body, {
          html: args.html,
          replyTo: args.replyTo,
        });
        break;
      }

      default:
        sendError(id, -32602, `Unknown tool: ${name}`);
        return;
    }

    // Format result as MCP tool response
    const content = typeof result === 'string'
      ? [{ type: 'text', text: result }]
      : [{ type: 'text', text: JSON.stringify(result, null, 2) }];

    sendResponse(id, { content });
  } catch (e) {
    sendResponse(id, {
      content: [{ type: 'text', text: `Error: ${e.message}` }],
      isError: true,
    });
  }
}

// Graceful shutdown
process.on('SIGINT', async () => {
  await pool.close();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  await pool.close();
  process.exit(0);
});

// Log to stderr (MCP convention — stdout is for protocol)
console.log = (...args) => process.stderr.write(args.join(' ') + '\n');
console.error = (...args) => process.stderr.write(args.join(' ') + '\n');

process.stderr.write(`[reach-mcp] Server started — ${TOOLS.length} tools available\n`);
