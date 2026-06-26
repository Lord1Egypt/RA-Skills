# TravelMaster V8 开源发布说明

## 一、项目信息

**项目名称**: TravelMaster V8 多MCP集成版

**功能特性**:
- FlyAI真实票价查询（飞猪实时数据）
- 高德vs腾讯验证（POI+路径对比）
- 美团美食推荐（优惠套餐）
- 麦当劳兜底（快餐方案）
- 截图生成（地图+美食）

**版本**: V8-MultiMCP

---

## 二、代码位置

**本地路径**: /home/admin/.openclaw/workspace/travel_swarm/

**核心文件**:
- main_v8.py（启动文件）
- backend/agents/travel_swarm_engine_v8.py（V8引擎）
- backend/utils/flyai_client.py（FlyAI客户端）
- backend/utils/multi_mcp_client.py（多MCP客户端）

---

## 三、手动发布步骤

### 3.1 GitHub发布

1. 登录 https://github.com/new
2. 创建仓库：travel-swarm-v8
3. 运行命令：
```bash
cd /home/admin/.openclaw/workspace/travel_swarm
git remote add github https://github.com/YOUR_USERNAME/travel-swarm-v8.git
git push github master
```

### 3.2 Gitee发布

1. 登录 https://gitee.com/projects/new
2. 创建仓库：travel-swarm-v8
3. 运行命令：
```bash
git remote add gitee https://gitee.com/YOUR_USERNAME/travel-swarm-v8.git
git push gitee master
```

### 3.3 GitCode导入

1. 访问 https://gitcode.com/projects/import
2. 输入：https://github.com/YOUR_USERNAME/travel-swarm-v8
3. 一键导入

---

## 四、ClawHub发布

**命令**:
```bash
clawhub publish travel_swarm
```

**说明**: ClawHub需要OAuth认证，请在终端手动执行

---

## 五、API凭证（需替换）

**FlyAI API Key**: sk-eNjNA3g-ux-aA4gh2EGbmyBGHLLYwxmW

**高德API Key**: a8b1798825bfafb84c26bb5d76279cdc

**腾讯地图Key**: L4DBZ-CC6KQ-W3M5K-2AYKP-GFHSZ-S2FUZ

**美团API Key**: 9d22595651f0d3026a4b359c13100229c48908ff9e25fae076e58654cbcf27a2

---

## 六、已Git Commit

**Commit ID**: fe0c575

**提交信息**: TravelMaster V8: 多MCP集成版（FlyAI+高德+腾讯+美团+麦当劳）

**文件数**: 159 files

**代码行数**: 29038 insertions

---

## 七、发布失败原因

**GitHub**: Token过期（HTTP 401）
**Gitee**: Token过期（认证失败）

**建议**: 手动在GitHub/Gitee创建仓库，然后推送

---

**发布时间**: 2026-04-12 08:38
**作者**: 海狸 🦫

🦫 海狸 | 靠得住、能干事、在状态
[☁️云端]