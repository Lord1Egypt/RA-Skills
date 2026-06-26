# 安装指南

## 环境要求

- Node.js >= 14.0.0
- npm >= 6.0.0 或 yarn >= 1.0.0
- 磁盘空间 >= 100MB
- 内存 >= 512MB

## 安装方式

### 方式一: 从源码安装

```bash
# 克隆仓库
git clone https://github.com/your-repo/unified-memory-architect.git
cd unified-memory-architect

# 安装依赖
npm install

# 验证安装
node memory/scripts/verify-system.cjs
```

### 方式二: 下载发布包

```bash
# 下载最新版本
wget https://github.com/your-repo/unified-memory-architect/releases/latest/download/unified-memory-architect-v1.0.0.zip

# 解压
unzip unified-memory-architect-v1.0.0.zip
cd unified-memory-architect-v1.0.0

# 运行验证
node memory/scripts/verify-system.cjs
```

### 方式三: OpenClaw Skill 安装

```bash
# 通过 OpenClaw 安装
openclaw skill install unified-memory-architect

# 验证
openclaw skill verify unified-memory-architect
```

## 目录权限

确保以下目录可读写：

```bash
# 设置权限
chmod 755 memory/processed
chmod 755 memory/archive
chmod 755 memory/import
```

## 验证安装

```bash
# 运行系统验证
node memory/scripts/verify-system.cjs

# 测试查询
node memory/scripts/query.cjs stats

# 测试搜索
node memory/scripts/query.cjs tag reflection 5
```

## Docker 部署

### Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --production

COPY . .

CMD ["node", "memory/scripts/query.cjs", "stats"]
```

### 构建和运行

```bash
# 构建镜像
docker build -t unified-memory-architect:latest .

# 运行
docker run unified-memory-architect:latest stats
```

## 卸载

```bash
# 删除安装目录
rm -rf unified-memory-architect/

# 清理数据（可选）
rm -rf memory/
```
