# Redacta MCP server

An [MCP](https://modelcontextprotocol.io) server that pseudonymises patient
identifiers and PII in text — and restores them. Gives any MCP client (Claude
Desktop, Cursor, etc.) three tools:

- **`redact`** — replace identifiers with labelled tokens (`[NHS_NUMBER_1]`,
  `[PATIENT_NAME_1]`, …). Returns the redacted text, a report, a `token_map`
  (token → original, for re-identification), and a self-check.
- **`reinstate`** — reverse a redaction using a token map, to put real values
  back into output generated from redacted text.
- **`self_check`** — re-scan redacted text for anything that still looks like an
  identifier.

Everything runs locally in the server process: **no network calls, no storage.**
Same engine as the [Redacta skill](https://clawhub.ai/nickjlamb/redacta) and the
Redacta for Miro app.

## Detection

Deterministic patterns with checksum validation — NHS numbers (Modulus-11), UK
National Insurance numbers, dates of birth (keyword-anchored; appointment dates
preserved), UK postcodes, US SSNs/ZIPs, hospital/MRN numbers, emails, phones —
plus general PII (URLs, IPs, Luhn-validated cards, IBANs, account numbers, UK
vehicle regs) and keyword-anchored patient/relative/carer names (clinician names
preserved by design). Names in free prose are not caught; review the output.

## Use with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "redacta": {
      "command": "npx",
      "args": ["-y", "redacta-mcp"]
    }
  }
}
```

Restart Claude Desktop. Then: *"Redact this letter before I share it"* → the
`redact` tool runs; *"put the real details back using this token map"* →
`reinstate`.

## Local development

```bash
npm install
npm run build
npm test          # engine tests (vitest)
npm start         # run the server on stdio
```

## Publishing

To npm (powers the `npx redacta-mcp` install above):

```bash
npm publish
```

Then list it on the MCP registries for discovery:

- **Official MCP registry** — <https://registry.modelcontextprotocol.io>
- **Smithery** — `smithery mcp publish`
- **Glama** — auto-indexes published npm MCP servers; verify the listing
- **mcp.so / PulseMCP** — community submission
- **awesome-mcp-servers** — open a PR adding the entry

## Limits

Deterministic + keyword-anchored detection only — not a guarantee, and not a
substitute for formal data-protection processes. Always review the result, and
treat the `token_map` as the key that reverses the redaction: store it with the
same care as the original data.

## License

MIT-0. Built by [PharmaTools.AI](https://www.pharmatools.ai/redacta).
