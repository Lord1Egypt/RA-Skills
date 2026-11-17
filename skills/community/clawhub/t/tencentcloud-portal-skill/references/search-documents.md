# portal SearchDocuments — 接口参考

按关键词搜索腾讯云官网文档。

- 产品/接口：`portal` / `SearchDocuments`（版本 `2023-04-13`）
- 频率限制：默认 5 次/秒；地域可选
- 实时签名核对：`tccli portal SearchDocuments help`

## 命令

```bash
tccli portal SearchDocuments --cli-unfold-argument \
  --Query '绑定安全组' --Page 1 --PageSize 5 --ProductName '云服务器'
```

## 入参

| 参数 | 必填 | 说明 |
|------|------|------|
| `--Query` | 是 | 搜索关键词/短语 |
| `--Page` | 是 | 页码，`[1, 99]` |
| `--PageSize` | 是 | 每页条数，`[1, 20]` |
| `--ProductName` | 否 | 限定产品（自由文本，如 `云服务器`）；不填则跨全产品 |

## 出参

- `Total`：匹配总数（跨全部分页）
- `Documents[]`：当前页文档，每条含 `Url` / `Title` / `ProductName` / `Snippet`
- `RequestId`：请求 ID

```json
{
  "Total": 15,
  "Documents": [
    {
      "Url": "https://cloud.tencent.com/document/product/213/31282",
      "Title": "绑定安全组",
      "ProductName": "云服务器",
      "Snippet": "本接口 (AssociateSecurityGroups) 用于绑定安全组到指定实例..."
    }
  ],
  "RequestId": "708b5a25-b649-423f-baea-039815794fed"
}
```

## 呈现与分页

- 先报 `Total`，再逐条列出 `Title` / `ProductName` / `Snippet` / `Url`（URL 放代码块，见 SKILL.md「渠道输出兼容性」）。
- `Total > PageSize` 时提示还有更多并询问是否翻页；翻页保持其它参数不变、递增 `--Page`，`Page * PageSize >= Total` 时停止。
- 只呈现返回内容，绝不臆造；失败时反馈错误与 `RequestId`。

## 提示

- 明确针对某产品时用 `--ProductName` 收窄，宽泛搜索时去掉。
- `Total` 为 0 时换同义词 / 更短短语，或去掉 `--ProductName`。
- `PageSize`/`Page` 超范围返回 `InvalidParameterValue`。
