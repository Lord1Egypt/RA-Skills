# 新氧青春诊所工具集 Soyoung Clinic Tools 🏥

新氧青春诊所工具集，包含预约、项目查询百科、医生信息及医生排班查询等能力 | Soyoung clinic tools

OpenClaw skill for the Soyoung (soyoung) clinic chain: appointment booking, store lookup, doctor info, schedules, project knowledge and pricing. Keywords: Soyoung, soyoung, clinic, appointment, doctor, schedule, medical aesthetic.

## 关键安全模型

- API Key 只能由主人在私聊中发送和配置，绝不能发到多人群聊中。
- Key、主人绑定、位置、审批单按 workspace 隔离，保存在 `~/.openclaw/state/soyoung-clinic-tools/workspaces/<workspace_key>/`。
- 高风险预约动作 `appointment_query/create/update/cancel`：
  - 主人本人可直接执行
  - 非主人私聊发起会被拒绝
  - 非主人群聊发起必须先 `@主人`，再由主人用 `确认 #审批单号` 或 `拒绝 #审批单号` 处理

## 组件

| 类型 | 名称 | 说明 |
|------|------|------|
| Setup | `setup/apikey` | 绑定主人、配置/替换/删除 API Key、管理主人位置 |
| Skill | `skills/appointment` | 门店查询、预约切片、预约审批与执行 |
| Skill | `skills/project` | 项目知识与商品价格查询 |
| Skill | `skills/doctor` | 医生信息与排班查询 |

## 常见说法

### API Key / 主人绑定

```text
配置新氧 API Key 为 xxx
我的新氧 API Key 配置了吗
当前新氧主人是谁
删除新氧 API Key
```

### 门店 / 预约

```text
附近有新氧门店吗
查下北京有哪些新氧
明天下午还有新氧面诊号吗
帮我预约新氧
查询我的预约
@主人 帮我取消预约 12345
确认 #A1B2C3
```

### 项目 / 价格

```text
什么是童颜水光
热玛吉疼不疼
痤疮怎么办
玻尿酸多少钱
超声炮价格
```

### 医生 / 排班

```text
北京保利店有哪些医生
唐碧莹医生这周哪天坐诊
新氧今天谁在班
新氧医生排班
```

## 对接要求

所有脚本调用都应透传当前消息上下文：

```text
--workspace-key
--chat-type
--chat-id
--sender-open-id
[--sender-name]
[--mention-open-id ...]
```

飞书侧建议统一转换为：

- 私聊：`direct`
- 群聊：`group`

## 运行依赖

- 必需：`python3`（3.8+）、`bash`
- `main.sh` 为各脚本的入口兼容壳，自动委托给 `main.py`；无 python3 时报错退出

## 安装 Hook

```bash
clawdhub install soyoung-clinic-tools && openclaw hooks install ~/.openclaw/skills/soyoung-clinic-tools/hooks/openclaw
```

Hook 会在 `agent:bootstrap` 时注入触发规则，让 agent 优先调用本 skill，并把 API Key 私聊限制和审批规则作为最高优先级执行。

## OpenClaw 识别依据

OpenClaw 是否能稳定识别这个 skill，主要看这几处：

- `SKILL.md`：技能集说明与入口信息
- `skills/appointment/SKILL.md`
- `skills/project/SKILL.md`
- `skills/doctor/SKILL.md`
- `setup/apikey/SKILL.md`
- `hooks/openclaw/handler.ts`：bootstrap 时注入最高优先级规则

`README.md` 和 `使用说明.md` 主要服务人类阅读，不是 OpenClaw 路由命中的核心依据。只要上述规则文件还完整、触发词和执行规则还在，识别精度不会因为 README 变短而明显下降。

为了让 OpenClaw 更稳地命中，我已经把真正的识别增强放在了规则文件里：

- `setup/apikey/SKILL.md`：补了更多 API Key、主人、位置类说法
- `skills/appointment/SKILL.md`：补了更多门店、预约、审批口令和自然语言说法
- `skills/project/SKILL.md`：补了更多项目、价格、适应症词
- `skills/doctor/SKILL.md`：补了医生、排班、门店医生查询说法
- `hooks/openclaw/handler.ts`：补了路由优先级和说法示例，bootstrap 时直接注入

## 目录结构

```text
soyoung-clinic-tools/
├── hooks/openclaw/
├── lib/
├── setup/apikey/
└── skills/
    ├── appointment/
    ├── doctor/
    └── project/
```

详细用法见 `使用说明.md`，版本变更见 `CHANGELOG.md`。

**版本**: 2.2.2
**最后更新**: 2026-04-03
