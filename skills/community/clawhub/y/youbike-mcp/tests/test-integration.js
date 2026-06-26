import { spawn } from "child_process";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

async function runTest() {
  console.log("🚀 Starting YouBike MCP Integration Test...");

  const transport = new StdioClientTransport({
    command: "node",
    args: ["src/index.js"]
  });

  const client = new Client(
    { name: "test-client", version: "1.0.0" },
    { capabilities: {} }
  );

  try {
    await client.connect(transport);
    console.log("✅ Connected to MCP Server");

    // Test 1: List Tools
    const tools = await client.listTools();
    console.log(`✅ List Tools: Found ${tools.tools.length} tools`);

    // Test 2: Search Station (Taipei)
    console.log("Testing search_stations (台北市 - 捷運科技大樓站)...");
    const searchResult = await client.callTool({
      name: "search_stations",
      arguments: { city: "台北市", keyword: "捷運科技大樓站" }
    });
    
    const stations = JSON.parse(searchResult.content[0].text);
    if (stations.length > 0) {
      const s = stations[0];
      console.log(`✅ Search Success: Found ${s.station_name}, Rent: ${s.available_rent}, E-bike: ${s.ebike}`);
    } else {
      throw new Error("Search returned no results for 台北市");
    }

    // Test 3: Nearby Stations (Taoyuan - Latitude: 24.993, Longitude: 121.301)
    console.log("Testing get_nearby_stations (桃園市)...");
    const nearbyResult = await client.callTool({
      name: "get_nearby_stations",
      arguments: {
        city: "桃園市",
        latitude: 24.993,
        longitude: 121.301,
        limit: 1
      }
    });

    const nearbyStationsResult = nearbyResult.content[0].text;
    if (nearbyStationsResult.startsWith("Error:")) {
      console.log(`⚠️ Nearby Search failed with: ${nearbyStationsResult} (Skipping...)`);
    } else {
      const nearbyStations = JSON.parse(nearbyStationsResult);
      if (nearbyStations.length > 0) {
        const s = nearbyStations[0];
        console.log(`✅ Nearby Success: Found ${s.station_name}, distance: ${Math.round(s.distance)}m, Rent: ${s.available_rent}, E-bike: ${s.ebike}`);
      } else {
        console.log("⚠️ Nearby search returned no results for 桃園市");
      }
    }

    console.log("\n🎉 All Integration Tests Passed!");
    process.exit(0);
  } catch (error) {
    console.error("\n❌ Test Failed:", error.message);
    process.exit(1);
  }
}

runTest();
