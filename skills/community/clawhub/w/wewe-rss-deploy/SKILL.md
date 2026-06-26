# SKILL.md - 部署 WeWe RSS 微信公众号 RSS 服务

## 触发条件
当 WeWe RSS 服务未运行（端口 4000 无响应），或用户要求部署 WeWe RSS 项目时激活。

## 功能概述
部署 WeWe RSS 服务，通过微信读书获取微信公众号文章，生成 RSS 订阅源。

## 前置条件
- Node.js >= 16
- pnpm 已安装
- Python 3.x

## 项目信息
- GitHub：https://github.com/cooderl/wewe-rss
- 安装后路径：`~/.openclaw/workspace/wewe-rss-main`

---

## 部署步骤

### Step 1：克隆项目

```bash
# 克隆到 workspace
git clone https://github.com/cooderl/wewe-rss.git ~/.openclaw/workspace/wewe-rss-main
```

如果 Git 克隆失败，使用 curl 下载压缩包：
```bash
# 下载
curl -L "https://github.com/cooderl/wewe-rss/archive/refs/heads/main.zip" -o /tmp/wewe-rss.zip

# 解压（自动生成 wewe-rss-main 目录）
unzip -o /tmp/wewe-rss.zip -d ~/.openclaw/workspace/

# 清理
rm /tmp/wewe-rss.zip
```

### Step 2：安装依赖

```bash
cd ~/.openclaw/workspace/wewe-rss-main
pnpm install
```

### Step 3：配置 SQLite 数据库

**切换 Prisma schema（项目默认是 MySQL，需要改为 SQLite）：**

```bash
# 进入 server 目录
cd ~/.openclaw/workspace/wewe-rss-main/apps/server

# 检查当前 prisma 目录
ls prisma/

# 删除 MySQL schema（如果存在）
rm -rf prisma/

# 重命名 SQLite schema
mv prisma-sqlite prisma
```

**创建数据目录：**
```bash
mkdir -p ~/.openclaw/workspace/wewe-rss-main/apps/server/data
mkdir -p ~/.openclaw/workspace/wewe-rss-main/apps/data
```

### Step 4：配置环境变量

创建配置文件 `~/.openclaw/workspace/wewe-rss-main/apps/server/.env`：

```env
HOST=0.0.0.0
PORT=4000

# 使用 SQLite
DATABASE_URL="file:../data/wewe-rss.db"
DATABASE_TYPE="sqlite"

# 访问授权码（自定义，建议设置复杂密码）
AUTH_CODE=your-secret-code-here

# 自动提取全文内容
FEED_MODE="fulltext"

# 服务地址
SERVER_ORIGIN_URL=http://localhost:4000

# 定时更新 Cron（每天 5:35 和 17:35 更新）
CRON_EXPRESSION="35 5,17 * * *"

# 微信读书转发服务（公共可用）
PLATFORM_URL="https://weread.111965.xyz"

# 关闭 HTML 清理（保留完整内容）
ENABLE_CLEAN_HTML=false

# 更新延迟（秒）
UPDATE_DELAY_TIME=60

# 每分钟最大请求数
MAX_REQUEST_PER_MINUTE=60
```

### Step 5：初始化数据库

```bash
cd ~/.openclaw/workspace/wewe-rss-main/apps/server

# 设置环境变量
export DATABASE_URL="file:../data/wewe-rss.db"
export DATABASE_TYPE="sqlite"

# 生成 Prisma Client
npx prisma generate

# 初始化数据库
npx prisma migrate deploy
```

### Step 6：构建项目

```bash
cd ~/.openclaw/workspace/wewe-rss-main
pnpm run -r build
```

如果构建时出现 MySQL 相关错误，重新检查 Step 3：
```bash
# 确认 prisma 目录是 sqlite 版本
cat ~/.openclaw/workspace/wewe-rss-main/apps/server/prisma/schema.prisma | grep provider
# 应该显示：provider = "sqlite"
```

### Step 7：启动服务

**直接运行（当前 session）：**
```bash
cd ~/.openclaw/workspace/wewe-rss-main
pnpm run start:server
```

**后台运行（PM2）：**
```bash
# 安装 PM2（如果未安装）
npm install -g pm2

# 启动服务
cd ~/.openclaw/workspace/wewe-rss-main
pm2 start apps/server/dist/main.js --name wewe-rss

# 开机自启
pm2 save
pm2 startup
```

### Step 8：保存安装路径

为了后续 Skill 能够找到项目，将路径写入配置：
```bash
mkdir -p ~/.openclaw/workspace/tools/
echo "~/.openclaw/workspace/wewe-rss-main" > ~/.openclaw/workspace/tools/wewe-rss-config.txt
```

### Step 9：验证部署

**检查服务是否运行：**
```bash
# Windows
netstat -ano | findstr ":4000"

# Mac/Linux
lsof -i :4000
```

**访问 Web UI：**`http://localhost:4000`

---

## 使用流程

1. 打开 `http://localhost:4000`
2. 点击「账号管理」→「添加账号」→ 微信读书扫码登录
3. 进入「公众号源」→「添加」→ 粘贴公众号分享链接
4. 订阅后返回文章列表

---

## API 接口

| 接口 | 说明 |
|------|------|
| `GET /feeds/{mp_id}.json?limit=10` | 获取公众号文章列表 |
| `GET /feeds/{mp_id}/{index}.json` | 获取指定文章正文 |
| `GET /api/v1/feeds` | 列出所有已订阅公众号 |

---

## 项目结构

```
~/.openclaw/workspace/wewe-rss-main/
├── apps/
│   ├── server/
│   │   ├── data/              # SQLite 数据库目录
│   │   │   └── wewe-rss.db
│   │   ├── dist/              # 构建输出
│   │   ├── prisma/            # 数据库 schema
│   │   └── .env               # 环境配置
│   └── data/                  # 数据文件软链接
└── package.json
```

---

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| `pnpm install` 失败 | 检查 Node.js 版本，确保 >= 16 |
| 构建报错 schema 相关 | 确认已切换到 SQLite schema（Step 3） |
| 数据库未创建 | 运行 `npx prisma migrate deploy` |
| 服务无法访问 | 检查防火墙，确保 4000 端口开放 |
| 微信读书登录失败 | 使用推荐 PLATFORM_URL，或检查网络 |
| 重启后服务消失 | 使用 PM2 后台运行（Step 7） |

---

## 卸载

```bash
# 停止服务
pm2 delete wewe-rss

# 删除项目
rm -rf ~/.openclaw/workspace/wewe-rss-main

# 清理配置
rm -f ~/.openclaw/workspace/tools/wewe-rss-config.txt
```
---

> 娆㈣繋鍏虫敞浣滆€呭井淇″叕浼楀彿锛?*寮€璁板仛浜у搧**