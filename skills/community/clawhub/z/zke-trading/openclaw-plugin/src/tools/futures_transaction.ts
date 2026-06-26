import { runMainJson } from "../python.js";
import type { PluginConfig, ToolSpec } from "../types.js";

export function createFuturesTransactionTools(config?: PluginConfig): ToolSpec[] {
  return [
    {
      name: "zke_get_futures_transaction_history",
      description: "Get ZKE futures transaction history (experimental endpoint)",
      inputSchema: {
        type: "object",
        properties: {
          begin_time: {
            type: "string",
            description: "Prefer 13-digit millisecond timestamp"
          },
          end_time: {
            type: "string",
            description: "Prefer 13-digit millisecond timestamp"
          },
          symbol: {
            type: "string",
            description: "Prefer BTC-USDT style for this endpoint"
          },
          page: { type: "integer", default: 1 },
          limit: { type: "integer", default: 200 },
          asset_type: { type: "integer" },
          lang_key: { type: "string" },
          tx_type: { type: "string" }
        },
        required: ["begin_time", "end_time", "symbol"],
        additionalProperties: false
      },
      execute: async ({
        begin_time,
        end_time,
        symbol,
        page = 1,
        limit = 200,
        asset_type,
        lang_key,
        tx_type
      }) => {
        const args = [
          "futures-transaction-history",
          String(begin_time),
          String(end_time),
          String(symbol),
          String(page),
          String(limit)
        ];

        if (asset_type !== undefined && asset_type !== null) {
          args.push(String(asset_type));
          args.push(lang_key ? String(lang_key) : "");
          args.push(tx_type ? String(tx_type) : "");
        } else if (lang_key) {
          args.push("");
          args.push(String(lang_key));
          args.push(tx_type ? String(tx_type) : "");
        } else if (tx_type) {
          args.push("");
          args.push("");
          args.push(String(tx_type));
        }

        // 加上 --json 尾巴
        args.push("--json");

        return await runMainJson(args, config);
      }
    }
  ];
}
