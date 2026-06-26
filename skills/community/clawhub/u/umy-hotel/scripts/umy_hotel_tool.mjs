#!/usr/bin/env node
/**
 * Umy Hotel MCP Tool CLI
 *
 * Connect to Umy MCP server via HTTP and call hotel search tools.
 * Uses only Node.js built-in APIs (fetch) — zero external dependencies.
 *
 * Usage:
 *   node scripts/umy_hotel_tool.mjs search --location "31.2359,121.4912" --check-in "2026-03-05" --check-out "2026-03-06" --query "上海外滩"
 *   node scripts/umy_hotel_tool.mjs detail --hotel-id 15084192
 */

const API_BASE = "https://api.umy.com/v1";
const API_KEY = process.env.UMY_API_KEY || "umyf1a1e67eae96d612c0d5a09e2d9cdf4f";

function showHelp() {
  console.log(`
Umy Hotel Tool CLI

Usage:
  node scripts/umy_hotel_tool.mjs <command> [options]

Commands:
  search    Search for hotels
  detail    Get hotel details by ID

Search Options:
  --location <lat,lng>    Location coordinates (required)
  --check-in <YYYY-MM-DD> Check-in date (required)
  --check-out <YYYY-MM-DD> Check-out date (required)
  --query <string>        Search keyword (optional)
  --radius <km>           Search radius in km (default: 5)
  --currency <code>       Currency code (default: CNY)

Detail Options:
  --hotel-id <id>         Hotel ID (required)

Examples:
  node scripts/umy_hotel_tool.mjs search --location "31.2359,121.4912" --check-in "2026-03-05" --check-out "2026-03-06" --query "上海外滩"
  node scripts/umy_hotel_tool.mjs detail --hotel-id 15084192
`);
}

async function searchHotelsAPI(params, timeoutMs = 30000) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(`${API_BASE}/hotel/search`, {
      method: "POST",
      headers: {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        location: params.location,
        check_in_date: params.checkIn,
        check_out_date: params.checkOut,
        query: params.query || "",
        radius: parseFloat(params.radius) || 5,
        currency: params.currency || "CNY"
      }),
      signal: controller.signal,
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`HTTP ${response.status}: ${text}`);
    }

    return await response.json();
  } finally {
    clearTimeout(timeout);
  }
}

async function getHotelDetailAPI(hotelId, timeoutMs = 30000) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(`${API_BASE}/hotel/detail`, {
      method: "POST",
      headers: {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        hotel_id: hotelId
      }),
      signal: controller.signal,
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`HTTP ${response.status}: ${text}`);
    }

    return await response.json();
  } finally {
    clearTimeout(timeout);
  }
}

function addBookingLink(hotel) {
  // Add umy booking link based on hotel ID
  const hotelId = hotel.id || hotel.hotel_id;
  return {
    ...hotel,
    booking_url: hotelId ? `https://umy.com/hotel/${hotelId}` : null,
    booking_link: hotelId ? `https://umy.com/hotel/${hotelId}` : null
  };
}

function processHotels(hotels) {
  return hotels.map(hotel => {
    const processed = addBookingLink(hotel);
    // Also add booking links to nested structures if present
    if (processed.price) {
      processed.price.booking_url = processed.booking_url;
      processed.price.booking_link = processed.booking_link;
    }
    return processed;
  });
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    showHelp();
    process.exit(0);
  }

  const command = args[0];

  try {
    if (command === "search") {
      const params = {};
      for (let i = 1; i < args.length; i++) {
        if (args[i] === "--location" && args[i + 1]) {
          params.location = args[++i];
        } else if (args[i] === "--check-in" && args[i + 1]) {
          params.checkIn = args[++i];
        } else if (args[i] === "--check-out" && args[i + 1]) {
          params.checkOut = args[++i];
        } else if (args[i] === "--query" && args[i + 1]) {
          params.query = args[++i];
        } else if (args[i] === "--radius" && args[i + 1]) {
          params.radius = args[++i];
        } else if (args[i] === "--currency" && args[i + 1]) {
          params.currency = args[++i];
        }
      }

      if (!params.location || !params.checkIn || !params.checkOut) {
        console.error("Error: --location, --check-in, and --check-out are required");
        process.exit(1);
      }

      const result = await searchHotelsAPI(params);

      // Add booking links to all hotels
      if (result.hotels) {
        result.hotels = processHotels(result.hotels);
      }

      console.log(JSON.stringify(result, null, 2));

    } else if (command === "detail") {
      let hotelId = null;
      for (let i = 1; i < args.length; i++) {
        if (args[i] === "--hotel-id" && args[i + 1]) {
          hotelId = args[++i];
        }
      }

      if (!hotelId) {
        console.error("Error: --hotel-id is required");
        process.exit(1);
      }

      const result = await getHotelDetailAPI(hotelId);

      // Add booking link
      if (result.hotel) {
        result.hotel = addBookingLink(result.hotel);
      }

      console.log(JSON.stringify(result, null, 2));

    } else {
      console.error(`Unknown command: ${command}`);
      showHelp();
      process.exit(1);
    }
  } catch (error) {
    console.error("Error:", error.message);
    process.exit(1);
  }
}

main();