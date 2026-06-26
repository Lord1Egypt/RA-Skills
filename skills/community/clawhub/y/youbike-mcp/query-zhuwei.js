import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

async function runQuery() {
  const transport = new StdioClientTransport({
    command: "node",
    args: ["src/index.js"]
  });

  const client = new Client(
    { name: "query-client", version: "1.0.0" },
    { capabilities: {} }
  );

  try {
    await client.connect(transport);
    const result = await client.callTool({
      name: "get_nearby_stations",
      arguments: {
        city: "桃園市",
        latitude: 25.116855,
        longitude: 121.24415,
        limit: 5
      }
    });

    console.log(result.content[0].text);
  } catch (error) {
    console.error("Error:", error.message);
  }
}

runQuery();
