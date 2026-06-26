---
name: smart-hotel-search
description: 智能酒店搜索 - 处理非标准酒店需求（如"安静酒店"、"宠物友好"、"无边泳池"等），结合小红书内容发现和飞猪预订对接。Use when: (1) 用户搜索酒店但需求无法用标准筛选表达（如"适合带老人的酒店"、"隔音好的酒店"）(2) 用户提到场景化需求（如"带狗住哪"、"网红打卡酒店"）(3) 需要从用户真实评价中找酒店推荐。不适用于：标准酒店搜索（目的地+日期+价格），这种情况直接使用flyai。
---

# Smart Hotel Search

用"内容平台理解需求 + 交易平台对接供给"的组合，承接任意非标准酒店搜索诉求。

## Prerequisites

**必须先检查并安装所需工具，确保闭环可用。**

### 快速检查

```bash
# 检查工具是否已安装
which opencli && echo "✅ opencli 已安装" || echo "❌ opencli 未安装"
which flyai && echo "✅ flyai 已安装" || echo "❌ flyai 未安装"
```

如果两个工具都已安装，跳过安装步骤，直接进入 Workflow。

### 安装指南

如果任一工具未安装，详见 **[references/installation.md](references/installation.md)** 获取完整安装步骤：

- **flyai**: `npm i -g @fly-ai/flyai-cli`
- **opencli**: Chrome + Playwright MCP Bridge插件 + 登录小红书

### 环境就绪确认

继续前，确认以下条件满足：

- ✅ `opencli` 命令可用
- ✅ `flyai` 命令可用
- ✅ Chrome 已登录小红书

如果任一条件不满足，先阅读 [installation.md](references/installation.md) 完成安装再继续。

## Workflow

**触发条件：** 用户需求是自然语言、非结构化的，标准搜索接口无法承接。

```
用户需求（自然语言）
    ↓
语义理解层 - opencli xiaohongshu search
    ↓
内容发现 → AI 提取酒店名
    ↓
供给对接层 - flyai search-hotel
    ↓
输出：测评 + 价格 + 链接
```

### Step 1: 内容发现

使用 `opencli xiaohongshu search` 在小红书搜索用户真实测评：

```bash
opencli xiaohongshu search "三亚带狗住酒店推荐"
opencli xiaohongshu search "无边泳池酒店 网红打卡"
opencli xiaohongshu search "适合带老人的酒店 安静"
```

从搜索结果中提取：
- 酒店名称
- 用户真实评价（环境、设施、服务）
- 实际体验（图片、视频）

### Step 2: AI提取酒店名

从小红书搜索结果中识别候选酒店：

- 提取酒店名称（注意区分民宿、公寓、酒店）
- 收集用户评价关键词
- 过滤广告内容、推广贴

### Step 3: 飞猪搜索

对每个候选酒店，使用 `flyai search-hotel` 获取可预订信息：

```bash
flyai search-hotel --key-words "三亚某度假酒店" --check-in "2024-01-15" --check-out "2024-01-17"
```

获取：
- 实时价格
- 房型信息
- 预订链接
- 用户评分

### Step 4: 综合输出

返回给用户：

1. **小红书真实测评**（1-2条精华内容）
2. **飞猪预订信息**（价格、链接）
3. **综合推荐结论**（为什么推荐）

## 失败处理

| 情况 | 处理方式 |
|------|---------|
| 小红书搜不到相关内容 | 扩大搜索范围，或提示"暂无相关内容，建议换个说法试试" |
| 提取的酒店名在飞猪搜不到 | 提示"该酒店可能不在飞猪，建议联系酒店直接预订" |
| 内容平台评价不客观 | 标注来源，提示"信息来自用户分享，建议入住前与酒店确认" |
| 用户需求太模糊 | 引导用户补充关键信息（目的地、时间、预算等） |

## Examples

详见 [references/examples.md](references/examples.md) 获取完整输入输出示例。

## Tips

- **语义理解优先**：先理解用户真实需求，再选择合适的关键词搜索小红书
- **多角度搜索**：一个需求可能需要多次搜索（如"宠物友好"可搜"带狗住"、"宠物入住"、"狗狗友好"）
- **信息交叉验证**：小红书评价 + 飞猪评分 = 更可靠的推荐
- **标注来源**：让用户知道信息来自真实用户分享，而非官方宣传