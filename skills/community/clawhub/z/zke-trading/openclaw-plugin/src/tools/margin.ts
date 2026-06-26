import { runMainJson } from "../python.js";
import type { PluginConfig, ToolSpec } from "../types.js";

export function createMarginTools(config?: PluginConfig): ToolSpec[] {
  return [
    {
      name: "zke_create_margin_order",
      description: "Create a ZKE margin order",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          side: { type: "string", enum: ["BUY", "SELL"] },
          order_type: { type: "string", enum: ["LIMIT", "MARKET"] },
          volume: { type: "string" },
          price: { type: "string" }
        },
        required: ["symbol", "side", "order_type", "volume"],
        additionalProperties: false
      },
      execute: async ({ symbol, side, order_type, volume, price = "" }) => {
        const args = [
          "margin-create-order",
          String(symbol),
          String(side),
          String(order_type),
          String(volume)
        ];
        if (String(order_type).toUpperCase() === "LIMIT") {
          args.push(String(price));
        }
        args.push("--json");
        return await runMainJson(args, config);
      }
    },
    {
      name: "zke_get_margin_order",
      description: "Query a ZKE margin order by order id",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          order_id: { type: "string" }
        },
        required: ["symbol", "order_id"],
        additionalProperties: false
      },
      execute: async ({ symbol, order_id }) => {
        return await runMainJson(
          ["margin-order", String(symbol), String(order_id), "--json"],
          config
        );
      }
    },
    {
      name: "zke_cancel_margin_order",
      description: "Cancel a ZKE margin order by order id",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          order_id: { type: "string" }
        },
        required: ["symbol", "order_id"],
        additionalProperties: false
      },
      execute: async ({ symbol, order_id }) => {
        return await runMainJson(
          ["margin-cancel-order", String(symbol), String(order_id), "--json"],
          config
        );
      }
    },
    {
      name: "zke_get_margin_open_orders",
      description: "Get current ZKE margin open orders",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          limit: { type: "integer", default: 100 }
        },
        required: ["symbol"],
        additionalProperties: false
      },
      execute: async ({ symbol, limit = 100 }) => {
        return await runMainJson(
          ["margin-open-orders", String(symbol), String(limit), "--json"],
          config
        );
      }
    },
    {
      name: "zke_get_margin_my_trades",
      description: "Get ZKE margin trade history",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          limit: { type: "integer", default: 100 }
        },
        required: ["symbol"],
        additionalProperties: false
      },
      execute: async ({ symbol, limit = 100 }) => {
        return await runMainJson(
          ["margin-my-trades", String(symbol), String(limit), "--json"],
          config
        );
      }
    }
  ];
}
