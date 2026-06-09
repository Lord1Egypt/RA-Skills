---
name: swagger-api-to-types
description: "可以将swagger YAPI apifox 等接口描述快速导出类型定义和请求"
source: LobeHub
tags: [aigc, api, yapi, swagger, api-fox]
compatible: [claude-code, openai-agents, hermes-agent, any-llm]
---

# 接口类型请求生成器

每一个 interface 命名都必须以 I 开头，响应类型只生成 data，不生成 code、msg 等字段

```ts
import request from "@/utils/request";
/** 接口描述-参数 */
export interface IApiDescParams {
  /** 分页数量 */
  pageSize: number;
}
/** 接口描述-响应 */
export interface IApiDescData {}
/** 接口描述-接口 */
export const methodApiDescApi = (params: IApiDescParams) => {
  return request.get<IApiDescData>("/xxx", params);
};
```
