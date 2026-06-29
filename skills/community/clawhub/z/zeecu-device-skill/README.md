# zeecu-device-skill

极酷电动车车辆信息查询 Skill — 让 AI Agent 查询用户绑定的车辆列表与实时数据。

## 快速开始

### 1. 获取 API Key

在品牌 App 中点击"获取 AI 助手接入密钥"，获取以 `sk_live_` 开头的 API Key。

### 2. 配置 API Key

三种方式任选其一：

**方式 A：环境变量（推荐）**

```bash
export API_KEY=sk_live_xxx
python3 scripts/query.py --device-tuid T123456789
```

**方式 B：命令行参数**

```bash
python3 scripts/query.py --api-key sk_live_xxx --device-tuid T123456789
```

**方式 C：配置文件**

复制 `config.example.json` 为 `config.json` 并填入 Key：

```bash
cp config.example.json config.json
# 编辑 config.json，填入 apiKey
python3 scripts/query.py --device-tuid T123456789
```

### 3. 查询车辆

```bash
# 自动选择唯一车辆
python3 scripts/query.py

# 按车辆名称模糊匹配
python3 scripts/query.py --device-name "我的小电驴"

# 按 TUID 精确查询
python3 scripts/query.py --device-tuid T123456789
```

## 依赖

- Python 3.7+（无第三方依赖，仅使用标准库）

## 文件说明


| 文件                        | 说明                                      |
| --------------------------- | ----------------------------------------- |
| `SKILL.md`                  | Agent 指令文档，声明 Skill 能力与使用方式 |
| `scripts/query.py` | Python 查询脚本                           |
| `references/api-spec.md`    | API 规格文档                              |
| `config.example.json`       | 配置样例                                  |