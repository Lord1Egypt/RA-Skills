import { command } from '@clawjs/common';

export default {
  name: 'sefaria-mcp-guidance',
  version: '1.0.0',
  description: 'Guidance for using the Sefaria API MCP and example usage patterns',
  author: 'Sefaria Developer <dev@sefaria.org>',
  license: 'MIT',
  tools: [
    {
      name: 'connect',
      description: 'Start the Sefaria API MCP server',
      command: async (context) => {
        const { port = 8080 } = context?.params || {};
        return command('node', ['dist/index.js'], {
          env: {
            PORT: port
          }
        })
      }
    },
    {
      name: 'use',
      description: 'Show example usage patterns for Sefaria MCP tools',
      command: async (context) => {
        return `Example usage patterns:
\n\n1. Get text by reference:
\n   {\n     \"name\": \"get_text\",\n     \"arguments\": { \"tref\": \"Genesis 1:1\" }\n   }
\n\n2. Search texts:
\n   {\n     \"name\": \"search\",\n     \"arguments\": { \"q\": \"love\", \"limit\": 5 }\n   }
\n\n3. Parse references:
\n   {\n     \"name\": \"find_refs\",\n     \"arguments\": { \"text\": \"As it says in Shabbat 31a about lighting candles\" }\n   }
\n\n4. Get today's readings:
\n   {\n     \"name\": \"get_calendars\"\n   }
\n\n5. Explore related content:
\n   {\n     \"name\": \"get_related\",\n     \"arguments\": { \"tref\": \"Genesis 1:1\" }\n   }`
      }
    }
  ]
};
