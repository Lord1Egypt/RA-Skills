# 王聚财面皮铺 AI Skill

> 西安首家芥末蒜香酿皮，擀面皮人气榜TOP

## 店铺信息

| 项目 | 内容 |
|------|------|
| 店名 | 王聚财面皮铺 |
| 地址 | 西安市凤城6路ee新城南门底商 |
| 商圈 | 张家堡商圈，西安北站附近 |
| 电话 | 19537080416 |
| 营业时间 | 9:00 - 21:00 |
| 人均 | 12-13元 |
| 评分 | 大众点评4.6-4.7分 |

## 特色菜品

- **芥末蒜香酿皮**（8元）- 招牌特色，西安首家
- **经典擀面皮**（8元）- 劲道有嚼劲，辣椒香而不辣
- **辣肠夹馍**（9元）- 经典搭配

## Skill 功能

### V1版本（当前）

| 工具 | 功能 |
|------|------|
| `get_restaurant_info` | 餐厅基本信息（地址、营业时间、电话） |
| `get_menu` | 菜单与特色菜介绍 |
| `get_delivery_info` | 外卖配送信息（美团/饿了么） |
| `get_reservation_info` | 堂食预约信息 |
| `get_wifi_info` | 到店 Wi-Fi 指引（公开版不返回密码） |
| `get_order_entry` | 公开下单入口（AI 可直接提供链接，也可提示到店扫码） |

## 发布安全说明

- 公开发布版本**不包含店内 Wi-Fi 密码**
- 公开发布版本**不包含门店扫码点单二维码图片**
- 公开发布版本**保留二维码对应的公开下单链接**，方便 AI 直接读取
- 本地调试服务默认只监听 `127.0.0.1`，避免无意暴露到局域网
- MCP 响应已按 JSON-RPC 方式封装，便于接入 ClawHub 等平台

### V2版本（计划）

- 外卖平台跳转链接

### V3版本（计划）

- 在线下单
- 微信支付

## 安装方式

### 方式一：告诉 AI 助手

```
帮我安装王聚财面皮铺 Skill，仓库地址：https://github.com/maggotnian-cell/wangjucai-liangpi-skill
```

### 方式二：手动克隆

```bash
git clone https://github.com/maggotnian-cell/wangjucai-liangpi-skill.git \
  ~/.hermes/skills/mcp/wangjucai-liangpi
```

## 本地测试

```bash
cd ~/.hermes/skills/mcp/wangjucai-liangpi
python mcp_server.py
```

默认监听 `127.0.0.1:8080`。然后访问：
- GET http://127.0.0.1:8080/ 查看健康状态
- POST http://127.0.0.1:8080/ 进行 MCP 协议调用

示例：

```bash
curl -X POST http://127.0.0.1:8080/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

获取公开下单入口示例：

```bash
curl -X POST http://127.0.0.1:8080/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_order_entry"}}'
```

如需对外监听，请显式设置：

```bash
MCP_HOST=0.0.0.0 python mcp_server.py
```

## 部署到腾讯云 CloudBase

推荐走“GitHub 仓库部署”路线，项目已经包含 `Dockerfile`。

简要步骤：

1. 先把当前项目推到 GitHub 仓库
2. 在 CloudBase 云托管里选择“通过 Git 仓库部署”
3. 选择当前仓库和 `main` 分支
4. 端口填写 `8080`
5. 部署完成后拿到公网域名
6. 把真实公网地址写回 `skill.json` 的 `mcp_server.url`

详细步骤请看 [DEPLOY_CLOUDBASE.md](./DEPLOY_CLOUDBASE.md)。

## MCP 接入配置

```json
{
  "mcpServers": {
    "wangjucai-liangpi": {
      "type": "streamable-http",
      "url": "https://wangjucai-liangpi-246135-8-1421953131.sh.run.tcloudbase.com"
    }
  }
}
```

## 项目结构

```text
wangjucai-liangpi/
├── .gitignore        # Git 忽略规则
├── .dockerignore     # Docker 构建忽略规则
├── Dockerfile        # CloudBase 云托管部署文件
├── DEPLOY_CLOUDBASE.md # CloudBase 部署说明
├── LICENSE           # MIT 许可证
├── SKILL.md          # Agent 指令文档
├── skill.json        # 机器可读配置
├── mcp_server.py     # MCP 服务器实现
├── PUBLISHING.md     # 发布前检查清单
├── README.md         # 本文件
└── tests/            # 基础兼容性测试
```

## 发布说明

发布前请先查看 [PUBLISHING.md](./PUBLISHING.md)。

## 关联项目

**西安AI搞钱联盟** - 以王聚财面皮铺为据点，打造西安AI创业者线下聚会+线上组织。

## License

MIT
