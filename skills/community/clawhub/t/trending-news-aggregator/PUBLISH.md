# Trending News Aggregator 发布指南

## 文件清单

```
Smart News Aggregator/
├── README.md           # 项目说明
├── SKILL.md            # Skill核心定义
├── package.json        # NPM配置
├── LICENSE             # MIT协议
├── CHANGELOG.md        # 更新日志
├── config.yaml         # 默认配置
├── .gitignore          # Git忽略
└── PUBLISH.md          # 本文件
```

## 发布步骤

### 1. 创建GitHub仓库

在GitHub创建 `trending-news-aggregator` 仓库

### 2. 初始化并推送

```bash
cd "C:\Users\fiddl\Desktop\Smart News Aggregator"
git init
git add .
git commit -m "Initial release v1.0.0"
git branch -M main
git remote add origin https://github.com/yourusername/trending-news-aggregator.git
git push -u origin main
```

### 3. 发布到NPM

```bash
npm login
npm publish --access public
```

### 4. 发布到ClawHub

```bash
npm i -g clawdhub
clawdhub login
clawdhub publish ./ \
  --slug trending-news-aggregator \
  --name "Trending News Aggregator" \
  --version 1.0.0 \
  --changelog "Initial release"
```

## 用户使用方式

### 安装
```bash
clawdhub install trending-news-aggregator
```

### 配置
1. 复制 `config.yaml` 到OpenClaw配置目录
2. 设置推送渠道
3. 启用定时任务

### 使用
```
获取今日热点新闻
```

## 隐私安全说明

本Skill：
- ✅ 不收集用户个人信息
- ✅ 不存储浏览历史
- ✅ 仅使用公开网络搜索
- ✅ 所有配置存储在用户本地
- ✅ 无外部数据上报
