# AMap 地点搜索适配器

服务端地点搜索。它调用高德 Web 服务 API v5 的固定 HTTPS POI 文本搜索端点，并将可用 POI 映射为 UI 可直接使用的统一结果：

```js
{
  id, label, address, latitude, longitude,
  coordinateSystem: "GCJ-02", source: "amap"
}
```

高德返回的坐标是 GCJ-02；不要把它当作 WGS-84 或 BD-09 混用。没有完整 ID、名称、地址或经纬度的提供方记录会被丢弃，普通字符串不会被伪装为已解析地点。

## 服务端配置

申请 Web 服务 API Key 后，只在服务器密钥存储或进程环境中配置：

```sh
AMAP_WEB_SERVICE_KEY=server_only_key
```

不要使用 `VITE_`、`NEXT_PUBLIC_`、`EXPO_PUBLIC_` 等会进入客户端包的变量。不要把 Key、原始上游 URL、查询文本或上游错误直接返回给浏览器。

```js
import { createAMapPlaceService } from "./amap-place-service.mjs";

// `key` 可省略：服务会读取仅服务端的 AMAP_WEB_SERVICE_KEY。
const places = createAMapPlaceService({
  key: process.env.AMAP_WEB_SERVICE_KEY,
  timeoutMs: 5_000,
});

const results = await places.search({ query: "中国国家博物馆", city: "北京市" });
```

`city` 会传为 `region` 并使用 `city_limit=true`，而不是只当作展示文案。请求可传 `AbortSignal`；默认五秒超时。错误是稳定的安全分类：`INVALID_REQUEST`、`CONFIGURATION`、`ABORTED`、`TIMEOUT` 或 `UNAVAILABLE`，不包含密钥或查询。

## 同源路由示例

`route-handler.mjs` 是最小的 framework-neutral server adapter。应用需要自己提供真实的身份验证、授权、频率限制，以及框架的 CSRF/会话策略；示例不会假装这些已完成。

```js
import { createAMapPlaceService } from "./amap-place-service.mjs";
import { createPlaceSearchHandler } from "./route-handler.mjs";

export const POST = createPlaceSearchHandler({
  placeService: createAMapPlaceService({ key: process.env.AMAP_WEB_SERVICE_KEY }),
  origin: process.env.APP_ORIGIN,
  authenticate: async (request) => Boolean(await requireSignedInUser(request)),
  rateLimit: async (request) => await allowUserPlaceSearch(request),
});
```

将该处理器挂在同源 `POST /api/place-search`。前端只发送 `{ query, city?, limit? }` 给自己的域名，不直接请求 AMap。客户端的输入框应有短暂防抖、加载态、取消旧请求、键盘选择、空结果和错误状态；确认地点后保存这里返回的完整对象，而不是只保存显示文字。

官方接口文档：[搜索 POI 2.0](https://lbs.amap.com/api/webservice/guide/api-advanced/newpoisearch)。
