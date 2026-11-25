# ToEstate via mcporter

## 確認 Bifrost 路徑

先用現成設定；此流程不修改 MCP 設定。下列以 mcporter 0.17.1 驗證。不要使用 `mcporter config get` 傾印 headers 或分享完整設定。若別台主機 alias 不同，只從已配置且已確認為 Bifrost 的候選選擇；不能只憑工具名稱相信任意伺服器。

```bash
mcporter config list --source local --json | jq -r '.servers[]?.name'
bifrost_server=bifrost
schema=$(mcporter list "$bifrost_server" --schema --json \
  --no-oauth --timeout 7000 --exit-code) || exit 1
jq -r '.tools[]? | select(.name | startswith("ToEstate-")) | .name' <<<"$schema"
jq -e --arg name 'ToEstate-get_area_statistics' \
  '.tools[]? | select(.name == $name) | {name, description, inputSchema}' <<<"$schema"
```

下一次換工具時，從同一份 `schema` 依精確名稱取該工具的 `description`、`inputSchema`；有需要才看 `outputSchema`。注意 JSON Schema 可能只給 string 或 nullable 型別，真正接受的列舉、單位和互斥條件常在 tool description；欄位不在 required 也可能有「二選一」的語意必填。

## 呼叫與解包


oauth 不在此流程中啟動。資料查詢用 `--args` 傳 JSON，保留陣列、布林、數字和有前導零的地號字串。動態值用 `jq --arg`／`--argjson` 組 JSON，禁止 `eval` 或把輸入拼進 shell 程式。以下 helper 用 Bash；`bifrost_server` 是上一步驗過的 alias：

```bash
te() {
  local tool=$1 args=$2 raw
  if raw=$(mcporter call "${bifrost_server:-bifrost}.ToEstate-$tool" \
    --args "$args" --no-oauth --timeout 12000 --output json); then
    jq -e '
      if .isError == true then error([.content[]?.text] | join("; "))
      else (.structuredContent // .)
        | if type == "object" and has("result") then .result else . end
        | if type == "string" then fromjson else . end
        | if type == "object" then
            if .isError == true or (.error != null and .error != false and .error != "")
            then error((.error // .message // "ToEstate returned an error") | tostring)
            else . end
          else error("Expected a ToEstate data object") end
      end
    ' <<<"$raw"
  else
    jq -r '[.content[]?.text] | join("; ") | select(length>0)' <<<"$raw" >&2 || true
    return 1
  fi
}

te search '{"query":"板橋","limit":3}' | jq '.items[] | {kind,title,href}'
te get_area_statistics '{"county":"臺北市","town":"大安區"}' \
  | jq '{items,sources}'
```

開啟 Bash 的 `set -o pipefail`，避免後段 jq 遮住呼叫錯誤。工具曾回傳 `{"result":"{...}"}`；只解已辨識的包裝，不把原樣的 MCP `content` 錯當資料。如果未來包裝不同，先看不含敏感資料的欄位結構和實際 MCP 錯誤，再調整。即使輸出為合法物件，仍需檢查 `items`、`summary`、`coverage`、`need`、`warnings` 等業務欄位。

## 失敗怎麼判讀

| 現象 | 行動 |
| --- | --- |
| Bifrost alias 未設定 | 報告這台沒有配置；不要復原編輯器匯入或自行加直連。 |
| Gateway 清單可讀，但沒所需工具 | 回報 Bifrost 工具暴露缺口；找已暴露且能正確回答的工具，或看公開頁面。 |
| 閘道呼叫回 timeout、429、初始化 4xx | 收斂為少量、優先逐次查；有 Retry-After 就遵守。若是偶發，僅針對必要的讀取做有界單次重試。若回 401/403 或持續失敗，停止反覆呼叫，不改認證、端點或 HTTP 傳輸。 |
| Schema／業務輸入錯 | 讀訊息後核對 JSON 型別、列舉、名稱、ID 組合與日期，不以同一輸入盲重試。 |
| 空清單、資料不足、覆蓋缺口 | 如實分開；同意後才放寬關鍵條件，或改公開來源並說清楚口徑不同。 |

Bifrost 曾對部分工具呼叫回 `failed to establish ephemeral MCP connection`，並附 `initialize POST` 的 4xx。這只是閘道回報的握手錯誤，不能從訊息推斷直連確實使用 legacy SSE（官方教學標明 Streamable HTTP），也不能推斷是資料不存在。必要時以 [官方 MCP 教學](https://toestate.tw/mcp-guide) 和 [官方資料入口](https://toestate.tw/llms.txt) 找相關公開頁面；切換方法後不得把網站數字說成自己用 MCP 取得。

## 2026-11-18 抽測紀錄

- Schema：Bifrost 讀出 55 個 `ToEstate-*` 工具；工具清單在 [索引](tool-catalog.md)。
- 已收到資料：`search`（板橋）、`get_area_statistics`（大安區）、`get_market_pulse`、`search_transactions`（大安區買賣）、`check_rent`（大安區，整層兩房）、`get_foreclosures`（臺北市待拍）、`search_projects`（板橋區；初測握手失敗，稍後單筆重測回傳 1 筆及 `sources`）。這些結果不保證未來每次呼叫都成功。
- `compare_areas`、`list_land_sections`、`get_nearby_transactions` 的初次抽查遇到閘道握手錯誤；未列為已跑通。其餘未逐一呼叫，皆屬 schema 已盤點。
