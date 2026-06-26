import { runMainJson } from "../python.js";
import type { PluginConfig, ToolSpec } from "../types.js";

export function createFuturesControlTools(config?: PluginConfig): ToolSpec[] {
  return [
    {
      name: "zke_edit_futures_position_mode",
      description: "Edit ZKE futures position mode",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          position_model: { type: "integer" }
        },
        required: ["symbol", "position_model"],
        additionalProperties: false
      },
      execute: async ({ symbol, position_model }) => {
        return await runMainJson(
          ["futures-edit-position-mode", String(symbol), String(position_model), "--json"],
          config
        );
      }
    },
    {
      name: "zke_edit_futures_margin_mode",
      description: "Edit ZKE futures margin mode",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          margin_model: { type: "integer" }
        },
        required: ["symbol", "margin_model"],
        additionalProperties: false
      },
      execute: async ({ symbol, margin_model }) => {
        return await runMainJson(
          ["futures-edit-margin-mode", String(symbol), String(margin_model), "--json"],
          config
        );
      }
    },
    {
      name: "zke_adjust_futures_position_margin",
      description: "Adjust ZKE futures position margin",
      inputSchema: {
        type: "object",
        properties: {
          position_id: { type: "integer" },
          amount: { type: "string" }
        },
        required: ["position_id", "amount"],
        additionalProperties: false
      },
      execute: async ({ position_id, amount }) => {
        return await runMainJson(
          ["futures-edit-position-margin", String(position_id), String(amount), "--json"],
          config
        );
      }
    },
    {
      name: "zke_edit_futures_leverage",
      description: "Edit ZKE futures leverage",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          now_level: { type: "integer" }
        },
        required: ["symbol", "now_level"],
        additionalProperties: false
      },
      execute: async ({ symbol, now_level }) => {
        return await runMainJson(
          ["futures-edit-leverage", String(symbol), String(now_level), "--json"],
          config
        );
      }
    }
  ];
}
