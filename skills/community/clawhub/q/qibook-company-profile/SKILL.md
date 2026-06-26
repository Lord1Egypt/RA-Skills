---
name: qibook-company-profile
version: 1.0.2
description: >
  企业工商信息与人员关联查询（查企业查老板）。
  Use when: 用户需要查企业、查公司、查老板、查股东、查高管、查法人、查对外投资、查人员任职、工商信息、主体识别等。
argument-hint: [企业名称/人员姓名/省份]
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - Read
  - Bash
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["QIBOOK_ACCESS_KEY", "QIBOOK_BASE_URL"],
        "bins": ["python3"]
      }
    }
  }
---

# 查企业查老板

基于企百科 API，快速查询企业工商信息和人员关联信息，将结果转为中文 Markdown 后回答用户。

先理解用户想查什么（企业还是人、要哪些信息），再选择正确的查询路径，不要随意升级查询范围。

**不适合深度企业分析（企业画像、信用评估、竞争力分析），这类需求应引导使用 qibook-company-wiki-deepresearch skill。**

***

## 前提条件

### 1. 获取 API 凭证

访问 https://skill.qibook.com 注册账号并获取 QIBOOK_ACCESS_KEY 和 QIBOOK_BASE_URL。

### 2. 配置环境变量

```bash
export QIBOOK_ACCESS_KEY=your_access_key
export QIBOOK_BASE_URL=your_base_url
```

调用前先校验这两个环境变量是否存在，缺失则提示用户设置。

***

## When to use

用户不说"工商"、"照面"这些术语也要触发。以下口语都属于本 skill 范围：

- 帮我查一下华为 / 美团的全称是什么 / XX 是哪家公司
- XX 的法人是谁 / 注册资本多少 / 什么时候成立的
- XX 的股东有哪些 / 高管是谁 / 对外投资 / 谁是大股东
- XX 是谁开的 / 这家公司老板是谁
- 查一下张三 / 张三名下有几家公司 / 张三在 XX 公司担任什么
- 查张三在北京的情况

**口语理解优先**：
- "查一下 XX 公司" → 主体识别，返回全称 + 信用代码
- "XX 的老板" / "谁开的" → 查法人代表
- "XX 名下有几家公司" → 查人员关联企业统计
- "XX 的股东" → 查股东及出资信息

***

## 功能路由

**重要：根据用户意图选择正确的功能，不要随意升级查询范围。**

### 1. 主体识别

**触发：** 用户给了企业简称/别名想知道全称，或只提到公司名没要求具体信息。

```bash
python3 -m scripts.combined_query --entmark "华为"
```

**只返回企业全称 + 统一社会信用代码，不要额外展开。**

### 2. 查企业详细信息

**触发：** 用户明确要查照面/股东/高管/对外投资等具体信息。

```bash
python3 -m scripts.combined_query --entmark "天津测试有限公司"
```

**用户没指定模块 → 默认只返回照面，提示"还可以进一步查看股东、高管、对外投资"。**

### 3. 查人

**仅人名** → 人员统计汇总：

```bash
python3 -m scripts.combined_query --name "张三"
```

**人名+省份** → 该省份下的统计：

```bash
python3 -m scripts.combined_query --name "张三" --province "天津"
```

**人名+企业** → 担任法人、高管、投资详情：

```bash
python3 -m scripts.combined_query --entmark "天津测试有限公司" --name "张三"
```

### 路由判断

```
用户提问
  ├── 只提到公司名/简称，没要求具体信息 → 功能1（主体识别）
  ├── 明确要查照面/股东/高管/对外投资   → 功能2（查企业）
  ├── 提到人名，没提公司               → 功能3（查人汇总）
  ├── 提到人名+省份                    → 功能3（查人+省份）
  └── 提到人名+公司                    → 功能3（查人+企业详情）
```

***

## 回答规范

1. 使用脚本返回的中文 Markdown 作为数据来源，不要暴露英文字段
2. 数组数据（股东、高管等）用表格展示
3. 空值字段脚本已自动过滤，无需额外处理
4. 某模块数据为空 → 告知"暂无该项信息"
5. 金额字段保留两位小数
6. 查询为空时区分原因（名称不对 / 权限不足 / 网络异常），不要统一说"查询失败"

***

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `scripts/base.py` | API 认证、调用、字段映射(英→中)、空值过滤、Markdown 格式化 |
| `scripts/combined_query.py` | 三个功能的 fetch 函数，根据入参自动判断场景，返回 Markdown 字符串 |
| `scripts/__init__.py` | 统一入口，导出 fetch / fetch_entity_id / fetch_enterprise / fetch_person_summary / fetch_person_detail |
