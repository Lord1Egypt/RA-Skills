# SearX 1.1.0 部署指南

**旧版本无 bot 检测，JSON API 完全可用！**

---

## 🚀 一键部署（推荐）

```bash
# 进入技能目录
cd /home/admin/.openclaw/workspace/skills/smart-search

# 运行部署脚本
chmod +x deploy-searx.sh
./deploy-searx.sh
```

**部署完成后：**
- ✅ SearX 运行在 `http://localhost:8080`
- ✅ 配置文件在 `./searx-config/`
- ✅ 容器自动重启（`--restart unless-stopped`）

---

## 🐳 Docker 命令部署

### 快速部署
```bash
docker run -d --name searx \
  -p 8080:8080 \
  -e SEARX_SECRET='local-secret-2026' \
  --restart unless-stopped \
  searx/searx:1.1.0-69-75b859d2
```

### 带配置文件部署
```bash
# 创建配置目录
mkdir -p ~/searx-config

# 下载配置（可选）
curl -o ~/searx-config/settings.yml \
  https://raw.githubusercontent.com/searx/searx/master/searx/settings.yml

# 启动容器
docker run -d --name searx \
  -p 8080:8080 \
  -v ~/searx-config:/etc/searx:rw \
  -e SEARX_SECRET='local-secret-2026' \
  --restart unless-stopped \
  searx/searx:1.1.0-69-75b859d2
```

---

## ⚙️ 配置 smart-search

部署完成后，配置环境变量：

```bash
# 编辑配置文件
nano ~/.openclaw/.env

# 添加
SEARXNG_URL=http://localhost:8080

# 保存退出（Ctrl+X, Y, Enter）
```

---

## 🧪 测试

### Web 界面
```bash
# 浏览器访问
http://localhost:8080
```

### JSON API
```bash
curl "http://localhost:8080/search?q=AI+news&format=json"
```

### smart-search 集成
```bash
cd /home/admin/.openclaw/workspace/skills/smart-search
./search.sh "AI 新闻" 5
```

**预期输出：**
```
🔍 Smart Search: 使用 searx

1. 第一条结果...
2. 第二条结果...

✅ 共找到 10 条结果（SearX 免费）
```

---

## 🔧 管理命令

### 查看状态
```bash
docker ps | grep searx
```

### 查看日志
```bash
docker logs searx --tail 50
```

### 重启
```bash
docker restart searx
```

### 停止
```bash
docker stop searx
```

### 启动
```bash
docker start searx
```

### 删除
```bash
docker rm -f searx
```

### 更新
```bash
# 停止旧容器
docker stop searx && docker rm searx

# 启动新版本
docker run -d --name searx \
  -p 8080:8080 \
  -e SEARX_SECRET='local-secret-2026' \
  --restart unless-stopped \
  searx/searx:1.1.0-69-75b859d2
```

---

## 📁 配置文件

### settings.yml 位置
```
./searx-config/settings.yml
# 或
~/searx-config/settings.yml
# 或
/etc/searx/settings.yml（容器内）
```

### 关键配置项
```yaml
server:
  secret_key: "change-me-to-random-string"
  limiter: false          # 关闭限流
  public_instance: false  # 非公共实例
  port: 8080
  bind_address: "0.0.0.0"

search:
  safe_search: 0          # 0=关闭，1=中等，2=严格
  formats:
    - html
    - json                # 启用 JSON API

engines:
  - name: google
    disabled: false       # 启用 Google
  - name: bing
    disabled: false       # 启用 Bing
  - name: duckduckgo
    disabled: false       # 启用 DuckDuckGo
```

---

## 🛡️ 安全建议

### 1️⃣ 修改 Secret Key
```yaml
server:
  secret_key: "your-random-secret-$(openssl rand -hex 32)"
```

### 2️⃣ 限制访问（可选）
如果只在本地使用，绑定到 localhost：
```yaml
server:
  bind_address: "127.0.0.1"
```

### 3️⃣ 使用防火墙
```bash
# 只允许本地访问
sudo ufw deny 8080
sudo ufw allow from 127.0.0.1 to any port 8080
```

### 4️⃣ Docker 网络隔离
```bash
# 创建专用网络
docker network create searx-net

# 启动时加入网络
docker run -d --name searx \
  --network searx-net \
  -p 127.0.0.1:8080:8080 \
  searx/searx:1.1.0-69-75b859d2
```

---

## 📊 性能优化

### 内存限制
```bash
docker run -d --name searx \
  -p 8080:8080 \
  --memory="512m" \
  --cpus="1.0" \
  searx/searx:1.1.0-69-75b859d2
```

### 启用缓存
```yaml
valkey:
  url: valkey://localhost:6379/0
```

### 引擎超时
```yaml
outgoing:
  request_timeout: 3.0
  max_request_timeout: 10.0
```

---

## 🐛 故障排查

### 容器启动失败
```bash
# 查看日志
docker logs searx

# 检查端口占用
netstat -tuln | grep 8080

# 删除旧容器
docker rm -f searx
```

### API 返回 403
```bash
# 检查配置
docker exec searx cat /etc/searx/settings.yml

# 重启容器
docker restart searx
```

### 搜索结果为空
```bash
# 检查引擎状态
curl "http://localhost:8080/preferences"

# 测试单个引擎
curl "http://localhost:8080/search?q=test&format=json"
```

---

## 📈 监控

### 健康检查
```bash
# 简单检查
curl -f "http://localhost:8080/search?q=health&format=json" || echo "不健康"

# 详细检查
docker inspect searx --format='{{.State.Health.Status}}'
```

### 性能监控
```bash
# 资源使用
docker stats searx

# 响应时间
time curl "http://localhost:8080/search?q=test&format=json" > /dev/null
```

---

## 🔄 备份与恢复

### 备份配置
```bash
cp -r ~/searx-config ~/searx-config.backup.$(date +%Y%m%d)
```

### 恢复配置
```bash
docker stop searx
rm -rf ~/searx-config
cp -r ~/searx-config.backup.20260326 ~/searx-config
docker start searx
```

---

## 📚 相关资源

- **官方文档**: https://docs.searxng.org/
- **GitHub**: https://github.com/searx/searx
- **Docker Hub**: https://hub.docker.com/r/searx/searx
- **公共实例**: https://searx.space

---

**最后更新：** 2026-03-26  
**版本：** 1.1.0-69-75b859d2（稳定版，无 bot 检测）
