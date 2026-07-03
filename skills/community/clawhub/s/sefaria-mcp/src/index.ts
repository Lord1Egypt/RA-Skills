#!/usr/bin/env node
/**
 * Sefaria MCP Server
 * Provides access to Jewish texts via Model Context Protocol
 * 
 * Tools:
 * - get_text: Get text by reference (Genesis 1:1, Berakhot 2a)
 * - search: Search across all Jewish texts
 * - get_links: Get commentaries and cross-references
 * - get_parsha: Get this week's Torah portion
 * - get_calendars: Get today's learning schedule
 * - get_book_info: Get metadata about a book
 * - get_related: Get related topics and source sheets
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";

import {
  getText,
  search,
  getLinks,
  getParsha,
  getCalendars,
  getBookInfo,
  getRelated,
} from "./sefaria-api.js";

// Tool definitions
const TOOLS: Tool[] = [
  {
    name: "get_text",
    description: `Get Jewish text by reference. Supports Torah, Talmud, Mishnah, Midrash, and commentaries.

Reference formats:
- Torah: "Genesis 1:1", "Exodus 20:1-10", "Deuteronomy 6:4-9"
- Talmud: "Berakhot 2a", "Shabbat 31a", "Bava Metzia 59b"
- Mishnah: "Mishnah Avot 1:1", "Mishnah Berakhot 1:1"
- Midrash: "Genesis Rabbah 1:1", "Tanchuma Bereshit 1"
- Commentaries: "Rashi on Genesis 1:1"

Returns Hebrew and English text with metadata.`,
    inputSchema: {
      type: "object",
      properties: {
        ref: {
          type: "string",
          description: "Sefaria reference (e.g., 'Genesis 1:1', 'Berakhot 2a')",
        },
        with_context: {
          type: "boolean",
          description: "Include surrounding context (default: false)",
          default: false,
        },
      },
      required: ["ref"],
    },
  },
  {
    name: "search",
    description: `Full-text search across all Jewish texts in Sefaria's library.
Searches Torah, Talmud, Midrash, Halacha, and more.
Supports English and Hebrew queries.

Examples: "love your neighbor", "tikkun olam", "ואהבת לרעך כמוך"`,
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Search query (English or Hebrew)",
        },
        limit: {
          type: "number",
          description: "Max results to return (default: 10, max: 50)",
          default: 10,
        },
        book: {
          type: "string",
          description: "Filter to specific book (e.g., 'Genesis', 'Berakhot')",
        },
      },
      required: ["query"],
    },
  },
  {
    name: "get_links",
    description: `Get all texts linked to a reference - commentaries (Rashi, Ramban, Ibn Ezra), cross-references, and related sources.

Essential for deep Torah study and finding multiple perspectives on a verse.`,
    inputSchema: {
      type: "object",
      properties: {
        ref: {
          type: "string",
          description: "Sefaria reference to find links for",
        },
      },
      required: ["ref"],
    },
  },
  {
    name: "get_parsha",
    description: "Get this week's Torah portion (Parashat Hashavua) with Hebrew and English names.",
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
  {
    name: "get_calendars",
    description: `Get today's Jewish learning schedule including:
- Daf Yomi (daily Talmud page)
- Parashat Hashavua (weekly Torah portion)
- Haftarah
- Daily Mishnah, Rambam, and more`,
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
  {
    name: "get_book_info",
    description: "Get metadata about a Jewish text - structure, categories, and length.",
    inputSchema: {
      type: "object",
      properties: {
        title: {
          type: "string",
          description: "Book title (e.g., 'Genesis', 'Berakhot', 'Mishneh Torah')",
        },
      },
      required: ["title"],
    },
  },
  {
    name: "get_related",
    description: "Get related topics and community source sheets for a reference.",
    inputSchema: {
      type: "object",
      properties: {
        ref: {
          type: "string",
          description: "Sefaria reference",
        },
      },
      required: ["ref"],
    },
  },
];

// Create MCP server
const server = new Server(
  {
    name: "sefaria-mcp-server",
    version: "1.0.1",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Handle list tools request
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools: TOOLS };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "get_text": {
        const ref = String(args?.ref || "");
        const withContext = Boolean(args?.with_context);
        
        if (!ref) {
          return {
            content: [{ type: "text", text: "Error: 'ref' parameter is required" }],
            isError: true,
          };
        }
        
        const result = await getText(ref, withContext);
        
        if (result.error) {
          return {
            content: [{ type: "text", text: `Error: ${result.error}` }],
            isError: true,
          };
        }
        
        const output = [
          `## ${result.ref}`,
          "",
          result.book ? `**Book:** ${result.book}` : "",
          result.categories.length ? `**Categories:** ${result.categories.join(" > ")}` : "",
          "",
          "### Hebrew",
          result.hebrew || "(No Hebrew text available)",
          "",
          "### English",
          result.english || "(No English translation available)",
        ].filter(Boolean).join("\n");
        
        return { content: [{ type: "text", text: output }] };
      }

      case "search": {
        const query = String(args?.query || "");
        const limit = Math.min(Number(args?.limit) || 10, 50);
        const book = args?.book ? String(args.book) : undefined;
        
        if (!query) {
          return {
            content: [{ type: "text", text: "Error: 'query' parameter is required" }],
            isError: true,
          };
        }
        
        const result = await search(query, limit, book ? { book } : undefined);
        
        if (result.error) {
          return {
            content: [{ type: "text", text: `Error: ${result.error}` }],
            isError: true,
          };
        }
        
        if (result.hits.length === 0) {
          return {
            content: [{ type: "text", text: `No results found for "${query}"` }],
          };
        }
        
        const output = [
          `## Search Results for "${query}"`,
          `Found ${result.total} results (showing ${result.hits.length})`,
          "",
          ...result.hits.map((hit, i) => [
            `### ${i + 1}. ${hit.ref}`,
            `*${hit.category}*`,
            hit.snippet ? `> ${hit.snippet}` : "",
            "",
          ].filter(Boolean).join("\n")),
        ].join("\n");
        
        return { content: [{ type: "text", text: output }] };
      }

      case "get_links": {
        const ref = String(args?.ref || "");
        
        if (!ref) {
          return {
            content: [{ type: "text", text: "Error: 'ref' parameter is required" }],
            isError: true,
          };
        }
        
        const result = await getLinks(ref);
        
        if (result.error) {
          return {
            content: [{ type: "text", text: `Error: ${result.error}` }],
            isError: true,
          };
        }
        
        const output = [
          `## Linked Texts for ${result.ref}`,
          `Found ${result.links.length} links`,
          "",
          ...Object.entries(result.byCategory).map(([category, links]) => [
            `### ${category}`,
            ...links.slice(0, 5).map(link => 
              `- **${link.ref}**: ${link.text || "(text available in full view)"}`
            ),
            "",
          ].join("\n")),
        ].join("\n");
        
        return { content: [{ type: "text", text: output }] };
      }

      case "get_parsha": {
        const result = await getParsha();
        
        if (result.error) {
          return {
            content: [{ type: "text", text: `Error: ${result.error}` }],
            isError: true,
          };
        }
        
        const output = [
          "## This Week's Parsha",
          "",
          `**${result.name}**`,
          result.hebrew ? `**Hebrew:** ${result.hebrew}` : "",
          "",
          `Use \`get_text("${result.ref}")\` to read the full portion.`,
        ].filter(Boolean).join("\n");
        
        return { content: [{ type: "text", text: output }] };
      }

      case "get_calendars": {
        const result = await getCalendars();
        
        if (result.error) {
          return {
            content: [{ type: "text", text: `Error: ${result.error}` }],
            isError: true,
          };
        }
        
        const output = [
          "## Today's Learning Schedule",
          "",
          ...result.items.map(item => 
            `- **${item.name}:** ${item.ref}${item.hebrew ? ` (${item.hebrew})` : ""}`
          ),
        ].join("\n");
        
        return { content: [{ type: "text", text: output }] };
      }

      case "get_book_info": {
        const title = String(args?.title || "");
        
        if (!title) {
          return {
            content: [{ type: "text", text: "Error: 'title' parameter is required" }],
            isError: true,
          };
        }
        
        const result = await getBookInfo(title);
        
        if (result.error) {
          return {
            content: [{ type: "text", text: `Error: ${result.error}` }],
            isError: true,
          };
        }
        
        const output = [
          `## ${result.title}`,
          result.heTitle ? `**Hebrew:** ${result.heTitle}` : "",
          result.categories.length ? `**Categories:** ${result.categories.join(" > ")}` : "",
          result.structure ? `**Structure:** ${result.structure}` : "",
          result.length ? `**Length:** ${result.length} sections` : "",
        ].filter(Boolean).join("\n");
        
        return { content: [{ type: "text", text: output }] };
      }

      case "get_related": {
        const ref = String(args?.ref || "");
        
        if (!ref) {
          return {
            content: [{ type: "text", text: "Error: 'ref' parameter is required" }],
            isError: true,
          };
        }
        
        const result = await getRelated(ref);
        
        if (result.error) {
          return {
            content: [{ type: "text", text: `Error: ${result.error}` }],
            isError: true,
          };
        }
        
        const output = [
          `## Related Content for ${result.ref}`,
          "",
          result.topics.length ? `### Topics\n${result.topics.map(t => `- ${t}`).join("\n")}` : "",
          "",
          result.sheets.length 
            ? `### Community Source Sheets\n${result.sheets.map(s => `- [${s.title}](https://www.sefaria.org/sheets/${s.id})`).join("\n")}` 
            : "",
        ].filter(Boolean).join("\n");
        
        return { content: [{ type: "text", text: output }] };
      }

      default:
        return {
          content: [{ type: "text", text: `Unknown tool: ${name}` }],
          isError: true,
        };
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error instanceof Error ? error.message : String(error)}`,
        },
      ],
      isError: true,
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Sefaria MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
