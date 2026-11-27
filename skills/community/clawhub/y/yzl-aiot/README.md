# YZL-AIoT（平台入口）

> 云智联 AIoT 平台 `aiot.yzlkj.com` 的**总入口**技能：判断方向、装对技能、说清平台边界。
> 它本身不提供接入代码；北向见 `yzl-aiot-north`，南向见 `yzl-aiot-south`，开放平台见 `yzl-open-api`。

**当前版本：v2.0.0**（由 1.x 拆分而来）

## 平台边界

| 你的需求 | 用哪个技能 | 入口 / 协议 |
|---|---|---|
| 后端 / 看板 / Webhook / 历史与告警 | `yzl-aiot-north` | `aiot.yzlkj.com` REST、北向 MQTT、Bridge |
| MCU / 4G 模组固件接入 | `yzl-aiot-south` | TCP 41032 / UDP 40501 / MQTT 1883 |
| 开放平台 API Key 取数 / 开关水阀 | `yzl-open-api` | `open.yzlkj.com` Open API v2 |
| 不确定 | **本技能** | 负责分流 |

## 安装

```bash
clawhub install yzl-aiot          # 本入口
clawhub install yzl-aiot-north    # 北向
clawhub install yzl-aiot-south    # 南向
clawhub install yzl-open-api      # 开放平台（按需）
```

## 加载规则

| 用户说 | 实际加载 |
|---|---|
| 「加载 yzl-aiot」 | 本技能 + `yzl-aiot-north` + `yzl-aiot-south` |
| 「加载 yzl-aiot 北向」 | 只加载 `yzl-aiot-north` |
| 「加载 yzl-aiot 南向」 | 只加载 `yzl-aiot-south` |
| 提到液位 / 温湿度 / 水阀 / open.yzlkj.com | 用 `yzl-open-api` |

## 快速使用

```bash
python tool.py status        # 环境与同族技能安装情况（不需要 API Key）
python tool.py migrate       # 开放平台迁移引导（不需要 API Key）
python tool.py check-update  # 检查 yzl-aiot 版本
```

## 限频（只针对北向 REST）

**用户配额 = 基础配额 + 设备数 × 每台追加**（例：基础 60 + 100 台 × 10 = 1060 次/秒）；
**写接口（POST / PUT / DELETE）按 3 倍配额计**；超限 429。配额数据由接口返回，查询配额本身也受限速约束。
南向设备链路不走这条配额；开放平台的按接口限速与「封 IP」只属于 `yzl-open-api`。

## 从 1.x 升级

- 1.x 的 `tool.py` 命令（`all` / `send` / `history` …）作为**兼容层**保留到 **3.0.0**，只对接 `open.yzlkj.com`；
- `python tool.py migrate` 给出迁移步骤；3.0.0 起移除兼容层。

## 仓库

| 平台 | 地址 |
|------|------|
| 🐙 GitHub | https://github.com/yzlkj/yzl-aiot |
| 🏠 Gitee | https://gitee.com/yzl-aiot/yzl-aiot |
| 📦 ClawHub | `yzl-aiot` |

## 联系

- 电话：089836692518/18689850608
- 邮箱：yzlkj@yzlkj.com
- 官网：www.yzlkj.com
