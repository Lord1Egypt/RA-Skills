# Skills Monitor 部署指南

## 服务器要求

| 项目 | 最低要求 | 你的配置 |
|------|---------|---------|
| CPU | 1核 | 2核 ✅ |
| 内存 | 1GB | 2GB ✅ |
| 硬盘 | 20GB | 40GB SSD ✅ |
| 带宽 | 3Mbps | 200Mbps ✅ |
| 系统 | Ubuntu 20.04+ / CentOS 7+ | - |

## ⚡ 前置条件：配置 SSH 密钥登录

腾讯云轻量应用服务器默认开启微信扫码/验证码验证，**必须先配置 SSH 密钥登录**，否则 scp 等非交互式命令会失败。

```bash
# 方式 1: 运行配置脚本（会引导你完成）
bash deploy/setup_ssh_key.sh root@82.156.182.240

# 方式 2: 通过腾讯云控制台 OrcaTerm 手动添加公钥
# 先复制你的公钥:
cat ~/.ssh/id_ed25519.pub
# 然后在 OrcaTerm 终端执行:
mkdir -p ~/.ssh && echo '你的公钥内容' >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
```

验证免密登录：
```bash
ssh -o BatchMode=yes root@82.156.182.240 "echo OK"
# 应该直接输出 OK，无需输入密码
```

## 🚀 一键部署（3 步完成）

### Step 1: 在 Mac 上执行打包上传

```bash
cd /Users/lynn/CodeBuddy/20260311140550

# 不带域名（后续手动配）
bash deploy/pack_and_upload.sh root@你的服务器IP

# 带域名（自动配置 Nginx）
SM_DOMAIN=monitor.yourdomain.com bash deploy/pack_and_upload.sh root@你的服务器IP
```

脚本会自动完成：
1. ✅ 打包 `server/` + `skills_monitor/` + 依赖文件
2. ✅ 上传到服务器 `/tmp/skills-monitor-deploy/`
3. ✅ 在服务器上执行部署（安装依赖、配置进程、启动服务）

### Step 2: 编辑服务器上的 .env 配置

```bash
ssh root@你的服务器IP
vim /www/wwwroot/skills-monitor/.env

# 主要填写：
# SM_H5_BASE_URL=https://你的域名
# SM_WECHAT_OA_APP_ID=...
# SM_WECHAT_OA_APP_SECRET=...
```

### Step 3: 宝塔面板配置反向代理 + SSL

1. 登录宝塔面板
2. **网站** → **添加站点** → 域名填你的域名
3. **站点设置** → **反向代理** → 目标 URL 填 `http://127.0.0.1:5100`
4. **SSL** → **Let's Encrypt** → 申请免费证书
5. 重启服务：`supervisorctl restart skills-monitor`

## 📁 部署后目录结构

```
/www/wwwroot/skills-monitor/
├── server/                 ← Flask 服务端代码
│   ├── api/                ← API 蓝图
│   ├── models/             ← 数据库模型
│   ├── services/           ← 业务服务
│   ├── templates/          ← H5 页面模板
│   ├── static/             ← 静态资源
│   ├── data/               ← SQLite 数据库
│   ├── app.py              ← 应用入口
│   └── config.py           ← 配置文件
├── skills_monitor/         ← 监控核心包
├── venv/                   ← Python 虚拟环境
├── logs/                   ← 日志目录
├── .env                    ← 环境变量（敏感信息）
├── gunicorn.conf.py        ← Gunicorn 配置
├── start.sh                ← 启动脚本
└── requirements.txt        ← Python 依赖
```

## 🔧 运维命令

```bash
# 查看服务状态
supervisorctl status skills-monitor

# 查看日志
tail -f /www/wwwroot/skills-monitor/logs/error.log
tail -f /www/wwwroot/skills-monitor/logs/access.log

# 重启服务
supervisorctl restart skills-monitor

# 停止服务
supervisorctl stop skills-monitor

# 健康检查
curl http://127.0.0.1:5100/health
```

## 🔄 更新代码

每次修改代码后，重新执行打包上传即可（数据库自动保留）：

```bash
bash deploy/pack_and_upload.sh root@你的服务器IP
```

## ⚠️ 2核2G 内存优化说明

针对你的 2GB 内存配置，部署脚本已做以下优化：

- **Gunicorn**: 1 worker + 4 threads（约 150MB 内存）
- **SQLite**: 无需额外数据库进程（节省 200MB+）
- **preload_app**: 减少 worker 内存占用
- **max_requests=500**: 自动回收防内存泄漏

预估内存占用：
| 组件 | 内存 |
|------|------|
| 系统 + 宝塔 | ~600MB |
| Nginx | ~20MB |
| Supervisor | ~10MB |
| Skills Monitor | ~150MB |
| **剩余可用** | **~1.2GB** ✅ |

## 🔒 安全清单

- [ ] SM_SECRET_KEY 已替换为随机值（部署脚本自动生成）
- [ ] .env 文件权限 600（仅 root 可读）
- [ ] 腾讯云安全组只开放 22/80/443
- [ ] SSH 使用密钥登录，禁用密码
- [ ] 宝塔面板设置强密码 + 修改默认端口
