#!/usr/bin/env node
/**
 * Redacta MCP server.
 *
 * Exposes the Redacta engine over the Model Context Protocol so any MCP client
 * (Claude Desktop, Cursor, etc.) can pseudonymise patient identifiers / PII in
 * text, re-identify it from a token map, and self-check redacted output.
 *
 * Everything runs locally in this process — no network calls, no storage.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { Redactor, isValidTokenMap, reinstate, selfCheck } from "@pharmatools/redacta";

const server = new McpServer({ name: "redacta", version: "1.2.0" });

const jsonResult = (data: unknown) => ({
  content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }],
});

server.registerTool(
  "redact",
  {
    title: "Redact / pseudonymise text",
    description:
      "Replace patient identifiers and PII in text with labelled tokens " +
      "([NHS_NUMBER_1], [PATIENT_NAME_1], ...) so it can be safely shared or " +
      "processed. Deterministic patterns plus keyword-anchored names. Returns " +
      "the redacted text, a report of what was replaced, and a token_map " +
      "(token -> original) for later re-identification. The token_map is the " +
      "key that reverses the redaction — handle it with care.",
    inputSchema: {
      text: z.string().describe("The text to redact."),
      categories: z
        .array(z.enum(["clinical", "general", "safeharbor"]))
        .optional()
        .describe(
          "Which pattern sets to apply. Defaults to clinical + general. " +
            "'clinical' = NHS/NI/DOB/MRN/postcode/SSN/ZIP/email/phone/names; " +
            "'general' = URLs, IPs, payment cards, IBANs, account numbers, " +
            "vehicle regs; 'safeharbor' = strictest, HIPAA Safe Harbor — implies " +
            "clinical + general and also removes ALL dates (not just DOB), ages, " +
            "fax, licence, device-serial, VIN and health-plan numbers."
        ),
    },
  },
  async ({ text, categories }) => {
    const cats = categories && categories.length ? categories : (["clinical", "general"] as const);
    const redactor = new Redactor([...cats]);
    const { text: redacted } = redactor.redactText(text);
    const residual = selfCheck(redacted);
    return jsonResult({
      redacted_text: redacted,
      report: redactor.report,
      token_map: redactor.tokenMap,
      self_check: residual,
    });
  }
);

server.registerTool(
  "reinstate",
  {
    title: "Re-identify (restore originals)",
    description:
      "Reverse a redaction: replace tokens with their original values using a " +
      "token map from an earlier redact call. Use this to put real data back " +
      "into output generated from redacted text.",
    inputSchema: {
      text: z.string().describe("Text containing Redacta tokens to restore."),
      token_map: z
        .record(z.string())
        .describe('Token map, e.g. {"[NHS_NUMBER_1]": "943 476 5919"}.'),
    },
  },
  async ({ text, token_map }) => {
    if (!isValidTokenMap(token_map)) {
      return {
        isError: true,
        content: [
          {
            type: "text" as const,
            text: "Invalid token map. Expected an object of [TOKEN] -> original-value entries.",
          },
        ],
      };
    }
    const { text: restored, changed } = reinstate(text, token_map);
    return jsonResult({ text: restored, changed });
  }
);

server.registerTool(
  "self_check",
  {
    title: "Self-check for residual identifiers",
    description:
      "Scan already-redacted text for anything that still looks like an " +
      "identifier (long numbers, emails, postcodes, URLs). A second pair of " +
      "eyes, not a guarantee. Returns a list of possible leftovers to review.",
    inputSchema: {
      text: z.string().describe("Redacted text to re-scan."),
    },
  },
  async ({ text }) => jsonResult({ findings: selfCheck(text) })
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  // stderr so we don't corrupt the stdio JSON-RPC channel
  console.error("Redacta MCP server running on stdio");
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
