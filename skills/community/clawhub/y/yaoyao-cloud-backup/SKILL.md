---
name: yaoyao-cloud-backup
version: 1.0.1
description: |
  云端与外部备份同步套件
  【首次自动引导】安装后首次访问即自动引导配置
  【多云支持】IMA、WebDAV、S3、FTP/SFTP、Samba 等
  【小白友好】全对话式操作，无需查看任何文档
---

# yaoyao-cloud-backup

🦞 云端与外部备份同步套件 - 零配置、零手动

---

## 核心理念

**安装即用，首次访问自动引导**

- ✅ 安装后首次访问即自动引导配置
- ✅ 不需要记任何命令
- ✅ 不需要查任何文档
- ✅ 遇到云备份话题自动询问

---

## 首次使用体验

### 场景：用户首次访问云备份功能

```
你：云备份怎么用？

摇摇：
  🔍 检测到您还没有配置任何云备份服务
  
  📋 推荐方案（国内用户首选）：
  
  [1] 🥜 坚果云
      国内可用，稳定可靠，免费额度够用
      → 适合：大多数国内用户
      
  [2] ☁️ 阿里云 OSS
      企业级存储，低成本
      → 适合：有技术背景的用户
      
  [3] 🖥️ Samba/NAS
      局域网高速传输
      → 适合：有 NAS 的用户
      
  [4] 📡 SFTP
      SSH 加固，安全可靠
      → 适合：有自己服务器的用户
  
  请选择编号（1-4），或说"跳过"稍后配置
```

---

## 自动检测范围

| 类型 | 示例 | 检测方式 |
|------|------|----------|
| ☁️ 本地云客户端 | iCloud Drive、Dropbox、OneDrive | 自动检测已安装的客户端 |
| 🌐 WebDAV | 坚果云、Nextcloud、ownCloud | 客户端/配置 |
| 🪣 云存储 API | 阿里云 OSS、腾讯云 COS、IMA | 环境变量/secrets.env |
| 🖥️ 服务器存储 | Samba/NAS、SFTP | 已挂载/配置文件 |
| 📡 SFTP | 远程服务器 | SSH 配置 |

---

## 快速安装指南

### 选择 1：坚果云（推荐国内用户）🥜

**特点**：国内可用、稳定、免费额度够用

**步骤**：
1. 访问 https://www.jianguoyun.com/ 注册
2. 进入「账户信息」→「安全设置」→「第三方应用管理」
3. 创建应用密码
4. 把邮箱和应用密码告诉我，我帮你配置

### 选择 2：阿里云 OSS ☁️

**特点**：企业级存储、低成本、国内高速

**步骤**：
1. 访问 https://www.aliyun.com/product/oss 开通
2. 创建 AccessKey（Root AccessKey 或子用户 AccessKey）
3. 创建存储桶（Bucket）
4. 把 AccessKey ID/Secret 和 Bucket 名称告诉我，我帮你配置

### 选择 3：Samba/NAS 🖥️

**特点**：局域网高速传输，无需互联网

**步骤**：
1. 确保 NAS 已开启 SMB/Samba 服务
2. 在 NAS 上创建共享文件夹（如 memory 或 家庭共享）
3. 告诉我 NAS 的 IP 地址、共享名称和登录信息，我帮你配置

**凭证配置**：在 `~/.openclaw/credentials/secrets.env` 中添加：
```bash
SAMBA_HOST=192.168.10.216
SAMBA_USER=你的用户名
SAMBA_PASS=你的密码
SAMBA_SHARE=家庭共享
SAMBA_PORT=445
SAMBA_REMOTE_PATH=/
```

**依赖**：pysmb（自动安装）

**使用**：
```bash
# 上传到所有已配置的云服务（包括Samba）
python3 scripts/unified_sync.py --upload

# 查看状态
python3 scripts/unified_sync.py --status
```

### 选择 4：SFTP 📡

**特点**：SSH 加固，安全可靠

**步骤**：
1. 确保服务器已开启 SSH 服务
2. 告诉我服务器地址、端口、用户名和密码，我帮你配置

---

## 使用方式

### 自动引导（首次/未配置时）

```
你：云备份怎么用？
     备份到云
     云同步
     ...

摇摇：自动检测 → 发现未配置 → 直接引导安装
```

### 已配置后的同步

```bash
# 上传到所有已配置的云服务
python3 scripts/unified_sync.py --upload

# 从所有云服务下载
python3 scripts/unified_sync.py --download

# 查看状态
python3 scripts/unified_sync.py --status
```

---

## 工作流程

```
用户首次访问云备份功能
          │
          ▼
┌─────────────────────────┐
│   自动检测云服务配置     │
└────────────┬────────────┘
             │
      ┌──────┴──────┐
      │             │
  已有配置       未配置
      │             │
      ▼             ▼
   执行同步     首次自动引导
                      │
                      ▼
              ┌───────────────┐
              │ 显示推荐方案   │
              │ 用户选择编号   │
              │ 自动配置完成  │
              └───────────────┘
```

---

## 凭证管理

所有凭证存储在 `~/.openclaw/credentials/secrets.env`：

```bash
# 坚果云 WebDAV
WEBDAV_URL=https://dav.jianguoyun.com/dav/
WEBDAV_USERNAME=你的邮箱
WEBDAV_PASSWORD=你的密码

# 阿里云 OSS
S3_ENDPOINT=https://oss-cn-hangzhou.aliyuncs.com
S3_ACCESS_KEY=你的 AccessKey ID
S3_SECRET_KEY=你的 AccessKey Secret
S3_BUCKET=你的 bucket 名称

# IMA 知识库
IMA_OPENAPI_CLIENTID=xxx
IMA_OPENAPI_APIKEY=xxx

# Samba/NAS（配置文件：config/samba.json）
# 详见上方"选择 3：Samba/NAS"章节
```

---

## 安全特性

| 特性 | 说明 |
|------|------|
| 🔒 凭证隔离 | 所有凭证存储在独立文件 |
| 🏷️ 来源标记 | 同步文件带来源标记，防死循环 |
| 📁 目录隔离 | 只能访问 exports/ 目录 |
| 🤖 自动检测 | 不收集用户敏感信息 |
