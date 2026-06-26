# MQL 取数 — Rhino 1.7R2 脚本模板

本文件是 `scenarios/schedule-task.md`（S1 定时计划任务）共享的 Rhino JS 代码模板，也可用于 Part 1 通用流程中的即时数据查询场景。

`<...>` 占位符由 agent 根据用户问句填入。

## 完整模板

```js
// === <任务名称> ===
// 运行时自动注入: logger, context, connector

var print = (typeof logger !== "undefined")
    ? function(m) { logger.info(String(m)); }
    : function(m) { java.lang.System.out.println(String(m)); };

// BASE_URL：优先从环境变量 SMARTBI_SDK_BASE_URL 获取，不存在时使用占位值
var BASE_URL = java.lang.System.getenv("SMARTBI_SDK_BASE_URL") || "<SMARTBI_BASE_URL>";
var newline = String.fromCharCode(10);

// ===== Token 获取 =====
// 优先级：环境变量 SMARTBI_TOKEN_DEV > RMI generateTempToken > context/占位值
// connector 已用当前用户身份登录，可通过 RMI 调用 UserService 生成临时令牌。
// generateTempToken：临时令牌，自动命名无重复，存于 session，执行结束即释放。
var TOKEN = java.lang.System.getenv("SMARTBI_TOKEN_DEV");
if (TOKEN) {
    print("Token from env SMARTBI_TOKEN_DEV");
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
    var s = c.getResponseCode() == 200 ? c.getInputStream() : c.getErrorStream();
    var r = new java.io.BufferedReader(new java.io.InputStreamReader(s, "UTF-8"));
    var sb = new java.lang.StringBuilder(); var l;
    while ((l = r.readLine()) != null) sb.append(l);
    r.close(); c.disconnect();
    return { code: c.getResponseCode(), body: sb.toString() };
}

// ===== MQL 查询 =====
// 优先 showDataTable:true 获取二维表数据以渲染邮件正文表格；
// 若服务端报错（旧版本 bug 或模型不兼容）则降级为 false，仅显示 rowCount + s3Url。
function queryData(dims, metrics, opt) {
    opt = opt || {};
    var mql = { dims: dims, metrics: metrics };
    if (opt.dimFilter)    mql.dimFilter    = opt.dimFilter;
    if (opt.metricFilter) mql.metricFilter = opt.metricFilter;
    if (opt.sort)          mql.sort         = opt.sort;
    // Rhino 中 JS Number 为 double，序列化 JSON 时带 .0（如 5.0）；
    // 转为 java.lang.Integer 确保输出整数（5）
    if (opt.limit)         mql.limit         = new java.lang.Integer(opt.limit);
    if (opt.offset)        mql.offset        = new java.lang.Integer(opt.offset);
    var bodyPayload = {
        req: { modelId: MODEL_ID, modelType: "AUGMENTED_DATASET", showDataTable: true, mql: mql }
    };
    var body = Packages.smartbi.net.sf.json.JSONObject.fromObject(bodyPayload).toString();
    var url = BASE_URL + "/api/v1/datamodel/datamodel/query-data-by-mql";
    var resp = httpPostJson(url, TOKEN, body);
    if (resp.code != 200) { logger.error("MQL HTTP " + resp.code + ": " + resp.body); return null; }
    var dObj = Packages.smartbi.net.sf.json.JSONObject.fromObject(resp.body);
    if (dObj.optBoolean("success", false)) {
        return dObj.opt("result");
    }
    // 降级：旧版本或部分模型不支持 showDataTable=true，改用 false 重试
    print("showDataTable=true failed, retrying with false");
    bodyPayload.req.showDataTable = false;
    body = Packages.smartbi.net.sf.json.JSONObject.fromObject(bodyPayload).toString();
    resp = httpPostJson(url, TOKEN, body);
    if (resp.code != 200) { logger.error("MQL retry HTTP " + resp.code + ": " + resp.body); return null; }
    dObj = Packages.smartbi.net.sf.json.JSONObject.fromObject(resp.body);
    return dObj.optBoolean("success", false) ? dObj.opt("result") : (logger.error("MQL retry: " + resp.body), null);
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
            limit: 100
        }
    );

    if (result) {
        var rowCount = result.optInt("rowCount", 0);
        var s3Url = result.optString("s3Url", "");
        var dt = result.opt("dataTable");
        var html = "<h3><任务名称></h3>" + newline;
        if (dt) {
            // showDataTable:true 成功，渲染数据表格
            html += buildTableHtml(dt);
        } else {
            // 降级为 showDataTable:false，仅显示摘要
            html += "<p>总行数: " + rowCount + "</p>" + newline
                + "<p>数据文件: " + s3Url + "</p>";
        }
        // 聊天渠道用 Markdown（企微/钉钉/飞书群机器人不支持 HTML，MESSAGE 推荐 Markdown）
        var markdown = "### <任务名称>\n\n"
            + "- 总行数: " + rowCount + "\n"
            + "- 数据文件: " + s3Url;
        context.put("resultTitle", "<任务名称>");
        context.put("resultContent", html);
        context.put("resultIsHtml", true);
        print("完成, rowCount=" + result.rowCount);

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
        //     ["<Smartbi用户ID>"], {});
    }
} catch (e) { logger.error("异常: " + (e.message || e)); }
```

## 占位符说明

| 占位符 | 来源 | 说明 |
|--------|------|------|
| `<任务名称>` | 自动生成 | 如 "每日贷款质量分析" |
| `<SMARTBI_BASE_URL>` | 兜底 | Smartbi 服务地址（优先从环境变量 `SMARTBI_SDK_BASE_URL` 获取） |
| `<TOKEN>` | 兜底 | 优先从环境变量 `SMARTBI_TOKEN_DEV` 获取，不存在时通过 `generateTempToken` 生成临时令牌（30 分钟有效） |
| `<MODEL_ID>` | 数据模型 ID | 通过问句检索或用户提供 |
| `<DIMS>` | 问句提取（**MUST 来自 getDataModelTrees 返回的 label**） | 如 `"订单日期"`, `"产品类别"`。禁止编造不存在的字段名，否则触发 "没有找到层次字段: xxx" 500 错误 |
| `<METRICS>` | 问句提取（**MUST 来自 getDataModelTrees 返回的 label**） | 如 `"销售额"`, `"订单量"`。禁止编造 |
| `<SORT_FIELD>` | 默认取第一个 `<METRICS>` label | 排序字段，必须是 dims 或 metrics 中的 label |
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
| 系统消息 | `pushMessage("MESSAGE", ...)` | Smartbi 用户 ID | MARKDOWN | — |

## 脚本注入方式

模板代码写入 `.js` 文件后，**使用 `scripts/inject-script.mjs` 工具**自动完成 JSON 转义并注入请求体。
详见 `scenarios/schedule-task.md`「script 字段处理」章节。

**MUST 使用 inject-script 工具**，禁止手动 JSON.stringify 或手写转义。工具会自动处理换行、引号、反斜杠等转义字符。

### 如需在脚本中使用特殊字符

当需要在 HTML 输出中包含换行时，使用 `String.fromCharCode(10)` 代替字面量 `\n`，
避免 Rhino 引擎在解析某些上下文时将 JavaScript 中的 `\n` 误判。

## 注意事项

- **`showDataTable` 降级策略**：模板默认 `true` 优先获取二维表数据渲染邮件表格；若服务端返回错误（旧版本 bug），`queryData()` 自动降级为 `false` 重试，仅显示 `rowCount` + `s3Url`。Agent 无需手动调整此值
- sdk-server 路径为 `/api/v1/datamodel/datamodel/query-data-by-mql`（双 datamodel）
- 字段名用 label（展示名），不是内部 name；先用 `getDataModelTrees` 确认（参考 Step 2）
- 核心指标（资本充足率等）不可与业务维度（机构名称等）跨表混用
- **push API 路径**：
  - `serverType=sdk-server`：`/api/v1/push/push/send-message`（双 push）
  - `serverType=smartbi`（直连）：`/api/v1/push/send-message`（单 push）
  - 在脚本中建议先确定 BASE_URL 对应的 serverType 再拼路径
- **邮件推送优先用 sendToMail Routine**：须按 `SendToMail.Input` 接口提供 `taskName`/`sendSetting`/`files`/`paramValueMap` 四个属性，`sendSetting` 内须含 `IMailSetting` 全部字段（`mailList`/`title`/`text`/`HTMLText`/`doZip`/`doUnzip`/`picInMail`/`ccMailList`/`bccMailList`）。RoutineExecutor 按 Java Bean 规范转换属性名（`isHTMLText()` → 属性 `HTMLText`）。详见模板中注释掉的示例代码
- `dimFilter` SQL 字符串值用单引号括起，内部单引号双写转义
