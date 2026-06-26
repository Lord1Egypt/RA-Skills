---
name: umeng-app-analysis
description: 友盟+ App 数据分析工具，通过友盟 Open API 查询移动应用统计数据。支持全部应用统计（App列表、数量、汇总数据）和单个应用详细分析（活跃/新增用户、启动次数、留存率、使用时长、渠道/版本维度、自定义事件及参数分析）。当用户需要查询友盟App统计数据、分析应用指标、获取用户行为数据时使用。认证信息从环境变量 UMENG_API_KEY 和 UMENG_API_SECURITY 读取。
---

# 友盟+ App 分析

## 环境变量要求

| 变量名 | 用途 |
|---|---|
| `UMENG_API_KEY` | 接口鉴权 key（无默认值） |
| `UMENG_API_SECURITY` | 接口鉴权密钥（无默认值） |

```bash
pip install requests
```

## 执行方式

所有 API 通过 `scripts/umeng.py` 调用，输出 JSON：

```bash
# 将 SKILL_DIR 替换为 skill 的实际安装路径
SKILL_DIR=/path/to/umeng-app-analysis
python3 $SKILL_DIR/scripts/umeng.py <command> [参数]
```

**输出约定**：成功返回 JSON 对象；失败 exit 1，并输出 `{"error": "..."}` 结构。

## 快速上手

```bash
# 全部 App 汇总
python3 umeng.py get-all-app-data

# 单个 App 昨日数据
python3 umeng.py get-yesterday-data --appkey 123456

# 新增用户时间段统计
python3 umeng.py get-new-users --appkey 123456 --start-date 2024-01-01 --end-date 2024-01-31
```

完整命令列表见 [references/commands.md](references/commands.md)。

## Gotchas

- **`--appkey` 是整数**，不能加引号传字符串，否则签名校验失败
- **`get-app-list` 需要 access_token**，其他接口不需要；忘传会导致接口报权限错误
- **`--channels` / `--versions` 是逗号分隔字符串**（如 `"渠道A,渠道B"`），由 API 侧解析，不是数组
- **`--event-id` 和 `--event-name` 是不同参数**：`get-event-param-list` 用 `--event-id`（数字），其他事件接口用 `--event-name`（字符串）
- **`--period-type` 在渠道/版本过滤接口中是必填**，在基础指标接口中是可选
- 游戏账号接口（`get-new-accounts` / `get-active-accounts`）**仅对游戏类型 App 有效**
