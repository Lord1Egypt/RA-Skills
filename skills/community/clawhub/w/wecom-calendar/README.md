# 📅 WeCom Calendar - 企业微信日历管理

企业微信日程管理工具，支持创建、查询、更新、删除日程。

## ✅ 功能特性

- ✅ 创建日程（一次性/重复/全天）
- ✅ 查询日程列表和详情
- ✅ 更新日程信息
- ✅ 取消日程
- ✅ 添加/删除参与者
- ✅ 重复日程（每日/每周/每月/每年）
- ✅ 提醒设置（多个提醒时间）
- ✅ 时区支持

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /root/.openclaw/workspace/skills/wecom-calendar
npm install
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
WECOM_CORP_ID=ww6dddd750e5f1d37a
WECOM_AGENT_ID=1000004
WECOM_AGENT_SECRET=xxx
```

### 3. 企业微信后台配置

1. 登录 https://work.weixin.qq.com/
2. 协作 → 日程 → 可调用接口的应用 → 添加你的应用
3. 应用管理 → 你的应用 → 企业可信 IP → 添加服务器 IP

### 4. 使用示例

```bash
# 创建日程
node calendar.mjs add --summary "会议" --start 1773462000 --end 1773471600

# 创建重复日程（每周六）
node calendar.mjs add --summary "英语课" --start 1773462000 --end 1773471600 --repeat 1 --repeat-type 1 --repeat-day-of-week 6

# 获取日程列表
node calendar.mjs list --cal_id "wcH5NrPwAA..."

# 更新日程（添加参与者）
node calendar.mjs update --schedule_id "xxx" --attendees "user1,user2"

# 取消日程
node calendar.mjs cancel --schedule_id "xxx"
```

## 📖 完整文档

查看 [SKILL.md](./SKILL.md) 获取完整使用说明和 API 文档。

## 🎯 实际案例

### 创建团队周例会

```bash
node calendar.mjs add \
  --summary "团队周例会" \
  --start 1773462000 \
  --end 1773471600 \
  --repeat 1 \
  --repeat-type 1 \
  --repeat-day-of-week 1 \
  --remind 1 \
  --remind-before 900
```

### 创建月度汇报

```bash
node calendar.mjs add \
  --summary "月度汇报" \
  --start 1775376000 \
  --end 1775383200 \
  --repeat 1 \
  --repeat-type 2 \
  --repeat-day-of-month 1
```

## 📦 文件结构

```
wecom-calendar/
├── calendar.mjs      # 主程序
├── package.json      # 依赖配置
├── SKILL.md          # 完整文档
├── README.md         # 快速入门
├── .env.example      # 配置示例
└── clawhub.yaml      # ClawHub 配置
```

## 🔗 相关链接

- [GitHub](https://github.com/davinwang/wecom-calendar)
- [企业微信 API 文档](https://developer.work.weixin.qq.com/document/path/93703)

---

**版本**: 1.0.0  
**作者**: OpenClaw Workspace  
**许可**: MIT
