import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";
import axios from "axios";

const API_CONFIG = {
  taipei: "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json",
  new_taipei: "https://data.ntpc.gov.tw/api/datasets/010e5b15-3823-4b20-b401-b1cf000550c5/json?size=2000",
  taoyuan: "https://opendata.tycg.gov.tw/api/v1/dataset.api_access?rid=08274d61-edbe-419d-8fcc-7a643831283d&format=json&limit=2000"
};

const server = new Server(
  {
    name: "youbike-mcp",
    version: "1.0.2",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

async function fetchStations(city) {
  const url = city === "台北市" ? API_CONFIG.taipei : (city === "新北市" ? API_CONFIG.new_taipei : API_CONFIG.taoyuan);
  const response = await axios.get(url);
  
  return response.data;
}

function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371e3;
  const φ1 = (lat1 * Math.PI) / 180;
  const φ2 = (lat2 * Math.PI) / 180;
  const Δφ = ((lat2 - lat1) * Math.PI) / 180;
  const Δλ = ((lon2 - lon1) * Math.PI) / 180;

  const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
    Math.cos(φ1) * Math.cos(φ2) *
    Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  return R * c;
}

function formatUpdateTime(timeStr) {
  if (!timeStr) return "";
  const cleanStr = timeStr.replace(/[- :T]/g, "");
  if (cleanStr.length >= 14) {
    const y = cleanStr.substring(0, 4);
    const m = cleanStr.substring(4, 6);
    const d = cleanStr.substring(6, 8);
    const h = cleanStr.substring(8, 10);
    const min = cleanStr.substring(10, 12);
    const s = cleanStr.substring(12, 14);
    return `${y}-${m}-${d} ${h}:${min}:${s}`;
  }
  return timeStr;
}

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_nearby_stations",
        description: "根據經緯度搜尋最近的 YouBike 站點",
        inputSchema: {
          type: "object",
          properties: {
            city: { type: "string", enum: ["台北市", "新北市", "桃園市"], description: "縣市名稱" },
            latitude: { type: "number", description: "緯度" },
            longitude: { type: "number", description: "經度" },
            limit: { type: "number", description: "返回站點數量" }
          },
          required: ["city", "latitude", "longitude", "limit"],
        },
      },
      {
        name: "search_stations",
        description: "根據關鍵字搜尋 YouBike 站點",
        inputSchema: {
          type: "object",
          properties: {
            city: { type: "string", enum: ["台北市", "新北市", "桃園市"], description: "縣市名稱" },
            keyword: { type: "string", description: "關鍵字 (如: 捷運永寧站)" }
          },
          required: ["city", "keyword"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === "get_nearby_stations") {
      const { city, latitude, longitude, limit } = args;
      const rawStations = await fetchStations(city);
      
      const stations = rawStations.map(s => {
        const sLat = s.lat || s.latitude;
        const sLng = s.lng || s.longitude;
        if (sLat === undefined || sLng === undefined) {
          return null;
        }

        const availableRent = parseInt(s.sbi || s.available_rent_bikes || s.sbi_quantity || 0);
        const availableReturn = parseInt(s.bemp || s.available_return_bikes || 0);
        const total = parseInt(s.tot || s.total_bikes || s.tot_quantity || 0);
        
        let eBike = 0;
        if (s.eyb_quantity !== undefined) {
          eBike = parseInt(s.eyb_quantity);
        } else if (s.sbi_detail) {
          try {
            const detail = typeof s.sbi_detail === 'string' ? JSON.parse(s.sbi_detail) : s.sbi_detail;
            eBike = parseInt(detail.eyb || 0);
          } catch (e) {}
        }
        
        return {
          station_name: s.sna,
          city: city,
          area: s.sarea,
          address: s.ar,
          available_rent: availableRent,
          available_return: availableReturn,
          ebike: eBike,
          total: total,
          latitude: parseFloat(sLat),
          longitude: parseFloat(sLng),
          update_time: formatUpdateTime(s.mday || s.srcUpdateTime),
          distance: calculateDistance(latitude, longitude, parseFloat(sLat), parseFloat(sLng))
        };
      }).filter(s => s !== null).sort((a, b) => a.distance - b.distance).slice(0, limit);

      return {
        content: [{ type: "text", text: JSON.stringify(stations, null, 2) }],
      };
    }

    if (name === "search_stations") {
      const { city, keyword } = args;
      const rawStations = await fetchStations(city);
      
      const stations = rawStations
        .filter(s => s.sna.includes(keyword))
        .map(s => {
          const availableRent = parseInt(s.sbi || s.available_rent_bikes || s.sbi_quantity || 0);
          const availableReturn = parseInt(s.bemp || s.available_return_bikes || 0);
          const total = parseInt(s.tot || s.total_bikes || s.tot_quantity || 0);

          let eBike = 0;
          if (s.eyb_quantity !== undefined) {
            eBike = parseInt(s.eyb_quantity);
          } else if (s.sbi_detail) {
            try {
              const detail = typeof s.sbi_detail === 'string' ? JSON.parse(s.sbi_detail) : s.sbi_detail;
              eBike = parseInt(detail.eyb || 0);
            } catch (e) {}
          }

          return {
            station_name: s.sna,
            city: city,
            area: s.sarea,
            address: s.ar,
            available_rent: availableRent,
            available_return: availableReturn,
            ebike: eBike,
            total: total,
            latitude: parseFloat(s.lat || s.latitude),
            longitude: parseFloat(s.lng || s.longitude),
            update_time: formatUpdateTime(s.mday || s.srcUpdateTime)
          };
        });

      return {
        content: [{ type: "text", text: JSON.stringify(stations, null, 2) }],
      };
    }
  } catch (error) {
    return {
      content: [{ type: "text", text: `Error: ${error.message}` }],
      isError: true,
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
