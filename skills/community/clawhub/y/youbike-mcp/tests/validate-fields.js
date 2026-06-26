import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

async function runValidation() {
  console.log("🔍 Starting Multi-City Field Validation...");

  const transport = new StdioClientTransport({
    command: "node",
    args: ["src/index.js"]
  });

  const client = new Client(
    { name: "validation-client", version: "1.0.0" },
    { capabilities: {} }
  );

  const requiredFields = [
    "station_name", "city", "area", "address", 
    "available_rent", "available_return", "ebike", "total", 
    "latitude", "longitude", "update_time"
  ];

  try {
    await client.connect(transport);
    
    const cities = ["台北市", "新北市", "桃園市"];
    
    for (const city of cities) {
      console.log(`\nTesting ${city}...`);
      const result = await client.callTool({
        name: "get_nearby_stations",
        arguments: {
          city: city,
          latitude: city === "台北市" ? 25.033 : (city === "新北市" ? 25.012 : 24.993),
          longitude: city === "台北市" ? 121.543 : (city === "新北市" ? 121.465 : 121.301),
          limit: 1
        }
      });

      const stations = JSON.parse(result.content[0].text);
      if (stations.length === 0) {
        console.log(`⚠️ No stations found for ${city}`);
        continue;
      }

      const s = stations[0];
      let missing = [];
      requiredFields.forEach(f => {
        if (s[f] === undefined || s[f] === null || s[f] === "") {
          missing.push(f);
        }
      });

      if (missing.length === 0) {
        console.log(`✅ ${city} validation PASSED`);
        console.log(`   Sample: ${s.station_name} (${s.available_rent}/${s.total})`);
      } else {
        console.log(`❌ ${city} validation FAILED. Missing fields: ${missing.join(", ")}`);
        console.log(`   Raw Data Sample: ${JSON.stringify(s)}`);
      }
    }

  } catch (error) {
    console.error("Error:", error.message);
  }
}

runValidation();
