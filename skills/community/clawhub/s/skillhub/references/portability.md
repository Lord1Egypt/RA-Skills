# 可移植性与 REST 回退

## 连接方式

| Agent 能力 | 使用方式 |
| --- | --- |
| 支持远程 Streamable HTTP MCP | 配置 `https://mro-api.iwilley.com/v1/mcp`，调用 MCP 的来源发现、匹配、详情和批量工具。 |
| 不能注册 MCP，但可运行 Python 3 | 使用 `scripts/mro_api_client.py` 调用 REST。脚本只依赖 Python 标准库。 |
| 既不能调用网络 MCP，也不能执行脚本 | 说明无法读取实时商品数据；可帮助整理询价，但不能声称已完成在线匹配。 |

无论采用哪种方式，都必须先在 [MRO API 平台](https://mro-api.iwilley.com/) 注册并创建自己的 API Key。服务端按账号授权限制可查询的数据源。

## REST 回退脚本

将密钥仅保存在运行环境：

```bash
export MRO_API_KEY='your-api-key'
# 可选；默认已经是生产服务地址
export MRO_API_BASE_URL='https://mro-api.iwilley.com'
```

单条匹配请求保存在 JSON 文件后执行：

```bash
python3 scripts/mro_api_client.py match --input request.json
```

读取指定商品：

```bash
python3 scripts/mro_api_client.py get-product --source xiyu --source-id 123
```

多条互不依赖的请求可以做本地并发处理，默认每批最多 10 条；只有纯摘要请求可放宽至 20 条：

```bash
python3 scripts/mro_api_client.py batch --input inquiries.json --workers 4
```

`batch` 是客户端对单条 REST 接口的并发封装，不替代 MCP 的 `batch_match_inquiries`。有 MCP 能力时，优先使用服务端批量工具；同一行依赖前一步分类或属性结果时，仍需分阶段请求。

脚本从文件或标准输入读取 JSON，避免把询价内容和密钥拼接进命令行。错误会输出 JSON，返回码为非零；不得将密钥写入询价表、日志、代码或最终交付文件。

脚本始终验证 HTTPS 证书，绝不添加跳过证书校验的参数。它会优先使用已安装的 `certifi` CA 包；没有该包时使用 Python 系统证书库。如果本机 Python 提示证书验证失败，应修复该 Python 的 CA 证书安装后重试。

### 私有清单与来源发现

先运行 `python scripts/mro_api_client.py sources` 获取免费来源元数据（`data.privateProductCount`）。存在私有商品时，请求 JSON 使用 `"sources":["mine"]`；仅零结果行才按 Skill 流程查询公共来源，错误不当作零结果。查询私有商品同样扣积分。
