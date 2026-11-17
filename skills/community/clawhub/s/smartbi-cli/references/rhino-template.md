# MQL 取数 — Rhino 1.7R2 脚本模板

本文件是 `scenarios/schedule-task.md`（S1 定时计划任务）共享的 Rhino JS 代码模板，也可用于 Part 1 通用流程中的即时数据查询场景。

`<...>` 占位符由 agent 根据用户问句和已核实契约填入。本模板只在任务实际需要服务端脚本时使用，普通外部取数走数据查询路径，不创建计划或任务。

## 完整模板

```js
// === <任务名称> ===
// 运行时自动注入: logger, context, connector

var print = (typeof logger !== "undefined")
    ? function(m) { logger.info(String(m)); }
    : function(m) { java.lang.System.out.println(String(m)); };

// BASE_URL：优先从环境变量 SMARTBI_SDK_BASE_URL 获取，不存在时使用占位值
var BASE_URL = java.lang.System.getenv("SMARTBI_SDK_BASE_URL") || "<SDK_API_BASE_URL>";
var newline = String.fromCharCode(10);

// ===== Token 获取 =====
// 优先级：环境变量 <TOKEN_ENV_NAME> > RMI generateTempToken > context/占位值
// connector 已用当前用户身份登录，可通过 RMI 调用 UserService 生成临时令牌。
// generateTempToken：临时令牌，自动命名无重复，存于 session，执行结束即释放。
var TOKEN = java.lang.System.getenv("<TOKEN_ENV_NAME>");
if (TOKEN) {
    print("Token from env <TOKEN_ENV_NAME>");
} else {
    try {
        var expireTime = java.lang.System.currentTimeMillis() + 30 * 60 * 1000;
        var tokenResult = connector.remoteInvoke("UserService", "generateTempToken", [expireTime]);
        TOKEN = tokenResult.getResult().toString();
        print("Token generated via generateTempToken");
    } catch (e) {
        print("Token generation failed: " + e);
        TOKEN = null;
    }
    if (!TOKEN) {
        TOKEN = context.get("API_TOKEN") || "<TOKEN>";
    }
}
var MODEL_ID = "<MODEL_ID>";

// ===== HTTP POST (Java 桥接) =====
function httpPostJson(url, token, body) {
    var c = new java.net.URL(url).openConnection();
    c.setRequestMethod("POST");
    c.setDoOutput(true); c.setDoInput(true);
    c.setRequestProperty("Content-Type", "application/json; charset=utf-8");
    c.setRequestProperty("Authorization", "Bearer " + token);
    c.setConnectTimeout(30000); c.setReadTimeout(120000);
    var w = new java.io.OutputStreamWriter(c.getOutputStream(), "UTF-8");
    w.write(body); w.flush(); w.close();
    var status = c.getResponseCode();
    var s = status == 200 ? c.getInputStream() : c.getErrorStream();
    if (!s) { c.disconnect(); return { code: status, body: "" }; }
    var r = new java.io.BufferedReader(new java.io.InputStreamReader(s, "UTF-8"));
    var sb = new java.lang.StringBuilder(); var l;
    while ((l = r.readLine()) != null) sb.append(l);
    r.close(); c.disconnect();
    return { code: status, body: sb.toString() };
}

// ===== MQL 查询 =====
// 仅用于已确认 dataTable 可覆盖每批结果的接口；预览/文件接口需按契约生成独立下载流程。
// scope=all 时批量取齐，scope=topn 时 limit 是用户明确的结果上限。
function queryData(dims, metrics, opt) {
    opt = opt || {};
    if (opt.inlineCompleteVerified !== true) {
        throw new Error("尚未确认 dataTable 批次完整性，不能据此交付或推送");
    }
    var limit = Number(opt.limit);
    var maxPages = Number(opt.maxPages);
    if (!(limit > 0) || Math.floor(limit) !== limit ||
        !(maxPages > 0) || Math.floor(maxPages) !== maxPages) {
        throw new Error("limit 和 maxPages 必须是正整数");
    }
    if (opt.scope !== "all" && opt.scope !== "topn") {
        throw new Error("必须明确 all 或用户指定的 topn 范围");
    }
    if (!opt.sort || !opt.sort.length) {
        throw new Error("需要按模型粒度确认的稳定排序；TopN 按目标指标排序");
    }
    var offset = opt.offset == null ? 0 : Number(opt.offset);
    if (offset !== 0) throw new Error("本完整交付模板从 offset=0 开始");
    var allRows = [], headers = null, headerSignature = null, seenPages = {};
    for (var page = 0; page < maxPages; page++) {
        var mql = { dims: dims, metrics: metrics, sort: opt.sort,
            limit: new java.lang.Integer(limit), offset: new java.lang.Integer(page * limit) };
        if (opt.from) mql.from = opt.from;
        if (opt.dimFilter) mql.dimFilter = opt.dimFilter;
        if (opt.metricFilter) mql.metricFilter = opt.metricFilter;
        var payload = { req: { modelId: MODEL_ID, modelType: "<MODEL_TYPE>",
            showDataTable: true, mql: mql, params: opt.params || [] } };
        var body = Packages.smartbi.net.sf.json.JSONObject.fromObject(payload).toString();
        var resp = httpPostJson(BASE_URL + "/api/v1/datamodel/datamodel/query-data-by-mql", TOKEN, body);
        if (resp.code !== 200) throw new Error("MQL HTTP " + resp.code);
        var obj = Packages.smartbi.net.sf.json.JSONObject.fromObject(resp.body);
        if (!obj.optBoolean("success", false)) {
            throw new Error("MQL 业务失败，停止当前任务；核对权限、字段或服务端日志，不自动切换文件查询");
        }
        var result = obj.optJSONObject("result");
        var dt = result && result.optJSONObject("dataTable");
        var rows = dt && dt.optJSONArray("data");
        var cols = dt && dt.optJSONArray("headers");
        if (!rows || !cols || rows.size() > limit) {
            throw new Error("批次数据缺失或超出请求行数，禁止交付部分结果");
        }
        var currentHeaders = [];
        for (var h = 0; h < cols.size(); h++) currentHeaders.push(cols.getString(h));
        if (headerSignature !== null && headerSignature !== String(cols.toString())) {
            throw new Error("分页字段发生变化，禁止拼接");
        }
        headers = currentHeaders;
        headerSignature = String(cols.toString());
        var signature = rows.toString();
        if (rows.size() && seenPages[signature]) throw new Error("检测到重复页，无法证明完整性");
        seenPages[signature] = true;
        for (var i = 0; i < rows.size(); i++) {
            var row = rows.getJSONArray(i), values = [];
            if (row.size() !== headers.length) throw new Error("行列宽度不一致");
            for (var j = 0; j < row.size(); j++) values.push(row.get(j));
            allRows.push(values);
        }
        if (opt.scope === "topn" || rows.size() < limit) {
            return Packages.smartbi.net.sf.json.JSONObject.fromObject({
                rowCount: allRows.length, s3Url: "", dataTable: { headers: headers, data: allRows }
            });
        }
    }
    throw new Error("达到本任务执行批数预算但未取齐，已取 " + allRows.length + " 行；禁止作为成功结果推送");
}

// ===== dataTable → HTML 表格 =====
function buildTableHtml(dt) {
    var html = "<table border='1' cellpadding='4' cellspacing='0'>";
    html += "<tr style='background-color:#f0f0f0'>";
    var headers = dt.optJSONArray("headers");
    if (headers) {
        for (var i = 0; i < headers.size(); i++) {
            html += "<th>" + headers.getString(i) + "</th>";
        }
    }
    html += "</tr>";
    var rows = dt.optJSONArray("data");
    if (rows) {
        for (var r = 0; r < rows.size(); r++) {
            html += "<tr>";
            var row = rows.getJSONArray(r);
            for (var c = 0; c < row.size(); c++) {
                html += "<td>" + row.getString(c) + "</td>";
            }
            html += "</tr>";
        }
    }
    html += "</table>";
    return html;
}

// ===== Push API 通用发送（辅助函数，独立于渠道） =====
// var PUSH_URL = BASE_URL + "/api/v1/push/push/send-message";  // sdk-server
// var PROGRESS_URL = BASE_URL + "/api/v1/push/push/get-send-progress";
//
// function pushMessage(channelType, content, contentType, recipients, config) {
//     var payload = {
//         sendMessageRequest: {
//             channelType: channelType,
//             content: content,
//             contentType: contentType || "MARKDOWN",
//             title: "<任务名称>"
//         }
//     };
//     if (recipients && recipients.length > 0) {
//         payload.sendMessageRequest.recipients = recipients;
//     }
//     if (config) {
//         payload.sendMessageRequest.config = config;
//     }
//     var body = Packages.smartbi.net.sf.json.JSONObject.fromObject(payload).toString();
//     var resp = httpPostJson(PUSH_URL, TOKEN, body);
//     print("Push [" + channelType + "] HTTP " + resp.code + ": " + resp.body);
//     if (resp.code == 200) {
//         var respObj = Packages.smartbi.net.sf.json.JSONObject.fromObject(resp.body);
//         var result = respObj.optJSONObject("result");
//         if (result) {
//             var platformTaskId = result.optString("platformTaskId", "");
//             if (platformTaskId) {
//                 print("  -> platformTaskId=" + platformTaskId);
//                 return platformTaskId;
//             }
//         }
//     }
//     return null;
// }
//
// // 可选：查询某次推送的最终状态
// function queryPushProgress(platformTaskId) {
//     var payload = { platformTaskId: platformTaskId };
//     var body = Packages.smartbi.net.sf.json.JSONObject.fromObject(payload).toString();
//     var resp = httpPostJson(PROGRESS_URL, TOKEN, body);
//     print("Push progress [" + platformTaskId + "] HTTP " + resp.code + ": " + resp.body);
//     return resp.code == 200;
// }

// ===== 主流程 =====
try {
    print("开始: <任务名称>");

    var result = queryData(
        [<DIMS>],        // 示例: "业务机构名称", "年月"
        [<METRICS>],     // 示例: "贷款余额", "不良率"
        {
            // dimFilter: "<SQL过滤>",   // 示例: "贷款余额 > 200000"
            sort: [["<SORT_FIELD>", "DESC"]],
            limit: <QUERY_LIMIT>,
            maxPages: <MAX_PAGES>,
            scope: "<QUERY_SCOPE>",
            inlineCompleteVerified: <INLINE_COMPLETE_VERIFIED>
        }
    );

    if (result) {
        var rowCount = result.optInt("rowCount", 0);
        var dt = result.optJSONObject("dataTable");
        var html = "<h3><任务名称></h3>" + newline + buildTableHtml(dt);
        // 此处 rowCount 是本模板已拼接的交付行数；接口原始 rowCount 不保证等于本页行数。
        var markdown = "### <任务名称>\n\n" + "- 已校验结果行数: " + rowCount;
        context.put("resultTitle", "<任务名称>");
        context.put("resultContent", html);
        context.put("resultIsHtml", true);
        print("完成, deliveredRows=" + rowCount);

        // ===== 推送（可选，仅当用户要求推送时生成此段） =====
        // 多渠道路由规则：
        //   - 邮件 → sendToMail Routine（代码简洁，依赖系统 SMTP 配置）
        //   - 企微/钉钉/飞书（群机器人）→ pushMessage() + Markdown
        //   - 系统消息 → pushMessage() + Markdown
        //   - 企微/钉钉（企业应用）→ pushMessage() + agentId / toUsers
        // 各渠道独立 try-catch，互不影响。Agent 按用户意图启用对应渠道。
        // pushMessage() 返回 platformTaskId（可用于 queryPushProgress 查询最终状态）。
        //
        // var pushResults = [];  // 收集 platformTaskId 供日志查看
        //
        // // --- 1. 邮件（sendToMail 内置 Routine）---
        // // RoutineExecutor：isXxx()/getXxx() → 属性名按 Java Bean 规范（isHTMLText → HTMLText）
        // execute("sendToMail", {
        //     taskName: "<任务名称>",
        //     sendSetting: {
        //         mailList: "<收件邮箱>",     // 多个用";"分隔
        //         title: "<任务名称>",
        //         text: html,                 // 邮件用 HTML 格式
        //         HTMLText: true,             // isHTMLText() → HTMLText
        //         doZip: false,
        //         doUnzip: false,
        //         picInMail: false,
        //         ccMailList: "",
        //         bccMailList: ""
        //     },
        //     files: [],
        //     paramValueMap: {}
        // });
        //
        // // --- 2. 企业微信群机器人（无需扩展） ---
        // pushMessage("WECHAT_WORK", markdown, "MARKDOWN", [],
        //     { webhookUrl: "<企微群机器人webhook地址>" });
        //
        // // --- 3. 钉钉群机器人（无需扩展） ---
        // pushMessage("DINGTALK", markdown, "MARKDOWN", [],
        //     { webhookUrl: "<钉钉群机器人webhook地址>" });
        //
        // // --- 4. 飞书群机器人（无需扩展） ---
        // pushMessage("FEISHU", markdown, "MARKDOWN", [],
        //     { webhookUrl: "<飞书群机器人webhook地址>" });
        //
        // // --- 5. 企业微信企业应用（依赖 WeiXinExt 扩展） ---
        // pushMessage("WECHAT_WORK", markdown, "MARKDOWN", [],
        //     { agentId: "<企微应用agentId>", toUsers: "<userid1|userid2>" });
        //
        // // --- 6. 钉钉工作通知（依赖 DingdingExt 扩展） ---
        // pushMessage("DINGTALK", markdown, "MARKDOWN", [],
        //     { toUsers: "<钉钉userid1,钉钉userid2>" });
        //
        // // --- 7. 系统消息 ---
        // pushMessage("MESSAGE", markdown, "MARKDOWN",
        //     ["<SmartBI用户ID>"], {});
    }
} catch (e) { logger.error("异常: " + (e.message || e)); throw e; }
```

## 占位符说明

| 占位符 | 来源 | 说明 |
|--------|------|------|
| `<任务名称>` | 自动生成 | 如 "每日贷款质量分析" |
| `<SDK_API_BASE_URL>` | 兜底 | SDK API 根地址：直连 SmartBI 为配置 baseUrl 加 `/sdk`；sdk-server 使用其根地址。以当前契约核对，环境变量必须指向同一根地址 |
| `<TOKEN>` | 兜底 | 优先从环境变量 `<TOKEN_ENV_NAME>` 获取，不存在时通过 `generateTempToken` 生成临时令牌（30 分钟有效） |
| `<TOKEN_ENV_NAME>` | 运行环境配置 | 按任务执行环境实际提供的凭证变量填写，不固定开发环境变量 |
| `<MODEL_TYPE>` | 当前模型元数据 | 不固定为某一种模型类型 |
| `<MODEL_ID>` | 数据模型 ID | 通过问句检索或用户提供 |
| `<DIMS>` | 问句提取（**MUST 来自 getDataModelTrees 返回的 label**） | 如 `"订单日期"`, `"产品类别"`。禁止编造不存在的字段名，否则触发 "没有找到层次字段: xxx" 500 错误 |
| `<METRICS>` | 问句提取（**MUST 来自 getDataModelTrees 返回的 label**） | 如 `"销售额"`, `"订单量"`。禁止编造 |
| `<QUERY_LIMIT>` | 问句与规模 | all 模式批量大小；topn 模式为用户明确的 N，不固定100行作为全量 |
| `<MAX_PAGES>` | 任务运行预算 | 正整数；达到预算仍未取齐时任务失败，不交付部分结果 |
| `<QUERY_SCOPE>` | 用户范围 | all 或 topn；不能为避免分页擅自改成topn |
| `<INLINE_COMPLETE_VERIFIED>` | 当前接口契约及验证 | 仅确认dataTable覆盖批次结果后填true；预览或仅文件模式另生成已验证下载流程，不盲设true |
| `<SORT_FIELD>` | 问句与模型粒度 | TopN 按目标指标；分页需唯一稳定排序，必要时扩展sort为多个已核实字段，不默认只按金额排序 |
| `dimFilter` | 问句中的过滤条件 | 如 `"贷款余额 > 200000"`（SQL 语法，字符串用单引号，内部单引号双写 `'it''s'`） |

### 推送占位符（按渠道）

| 渠道 | 方式 | 占位符 | 内容格式 | 依赖扩展 |
|------|------|--------|---------|---------|
| 邮件 | `sendToMail` | 收件邮箱地址 | HTML（`html` 变量） | — |
| 企微群机器人 | `pushMessage("WECHAT_WORK", ...)` | `webhookUrl` | MARKDOWN | — |
| 钉钉群机器人 | `pushMessage("DINGTALK", ...)` | `webhookUrl` | MARKDOWN | — |
| 飞书群机器人 | `pushMessage("FEISHU", ...)` | `webhookUrl` | MARKDOWN | — |
| 企微企业应用 | `pushMessage("WECHAT_WORK", ...)` | `agentId` + `toUsers`（`\|` 分隔） | MARKDOWN | WeiXinExt |
| 钉钉工作通知 | `pushMessage("DINGTALK", ...)` | `toUsers`（逗号分隔） | MARKDOWN | DingdingExt |
| 系统消息 | `pushMessage("MESSAGE", ...)` | SmartBI 用户 ID | MARKDOWN | — |

## 脚本注入方式

模板代码写入 `.js` 文件后，**使用 `scripts/inject-script.mjs` 工具**自动完成 JSON 转义并注入请求体。
详见 `scenarios/schedule-task.md`「script 字段处理」章节。

**MUST 使用 inject-script 工具**，禁止手动 JSON.stringify 或手写转义。工具会自动处理换行、引号、反斜杠等转义字符。

### 如需在脚本中使用特殊字符

当需要在 HTML 输出中包含换行时，使用 `String.fromCharCode(10)` 代替字面量 `\n`，
避免 Rhino 引擎在解析某些上下文时将 JavaScript 中的 `\n` 误判。

## 注意事项

- **查询与交付**：模板仅用于已验证可完整分页的内联结果。业务失败直接使任务失败，不自动改成文件请求；文件模式须单独按当前契约实现下载、识别、完整性校验后才交付，不把 s3Url 当作已交付文件。
- **分页边界**：all 模式固定页长与唯一稳定排序，满批继续、短批结束；TopN按用户明确N停止。重复页、字段或行数异常、超过任务批数预算均抛错，禁止执行后续成功推送。无法维持稳定数据快照时仍须披露完整性限制。
- **验证范围**：本模板的查询逻辑有本地替身回归；Java JSON桥接、Rhino运行时、调度失败状态及推送须在获授权的目标环境另行验证，不据此声称端到端通过。
- sdk-server 路径为 `/api/v1/datamodel/datamodel/query-data-by-mql`（双 datamodel）
- 字段名用 label（展示名），不是内部 name；先用 `getDataModelTrees` 确认（参考 Step 2）
- 跨来源维度与指标能否组合，以当前模型关联和口径为准；异常重复或汇总放大时停止交付该结论
- **push API 路径**：
  - 以目标环境 `describe push.sendMessage` 为准；已核实 SDK 路径为 `/api/v1/push/push/send-message`。
  - SmartBI 的 SDK 根地址是配置 baseUrl 加 `/sdk`，sdk-server 则使用配置根地址；不因 serverType 改写 operation 的路径段。
- **邮件推送优先用 sendToMail Routine**：须按 `SendToMail.Input` 接口提供 `taskName`/`sendSetting`/`files`/`paramValueMap` 四个属性，`sendSetting` 内须含 `IMailSetting` 全部字段（`mailList`/`title`/`text`/`HTMLText`/`doZip`/`doUnzip`/`picInMail`/`ccMailList`/`bccMailList`）。RoutineExecutor 按 Java Bean 规范转换属性名（`isHTMLText()` → 属性 `HTMLText`）。详见模板中注释掉的示例代码
- `dimFilter` SQL 字符串值用单引号括起，内部单引号双写转义
