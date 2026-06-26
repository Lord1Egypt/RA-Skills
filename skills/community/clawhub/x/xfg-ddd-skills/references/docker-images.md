# Docker 镜像加速参考

## 背景

由于网络原因，直接从 Docker Hub 拉取镜像可能很慢或失败。
本项目提供阿里云镜像仓库代理，所有镜像均已同步到：

```
registry.cn-hangzhou.aliyuncs.com/xfg-studio/
```

## 使用方式

将原始镜像名替换为阿里云代理地址即可：

```bash
# 原始
docker pull mysql:8.0.32

# 替换为
docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/mysql:8.0.32
```

## 常用镜像速查表

| 镜像 | 拉取命令 |
|------|---------|
| **数据库** | |
| mysql:8.0.32 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/mysql:8.0.32` |
| mysql:8.4.4 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/mysql:8.4.4` |
| redis:6.2 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/redis:6.2` |
| redis:7.2 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/redis:7.2` |
| phpmyadmin:5.2.1 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/phpmyadmin:5.2.1` |
| redis-commander:0.8.0 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/redis-commander:0.8.0` |
| **JDK** | |
| openjdk:8-jre-slim | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/openjdk:8-jre-slim` |
| openjdk:17-jdk-slim | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/openjdk:17-jdk-slim` |
| **Web** | |
| nginx:1.25.1 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/nginx:1.25.1` |
| nginx:1.28.0-alpine | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/nginx:1.28.0-alpine` |
| **消息队列** | |
| rabbitmq:3.12.9 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/rabbitmq:3.12.9` |
| rocketmq:5.1.0 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/rocketmq:5.1.0` |
| kafka:3.7.0 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/kafka:3.7.0` |
| zookeeper:3.9.0 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/zookeeper:3.9.0` |
| **注册中心** | |
| nacos-server:v2.2.3-slim | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/nacos-server:v2.2.3-slim` |
| nacos-server:v3.1.1 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/nacos-server:v3.1.1` |
| **监控** | |
| prometheus:2.47.2 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/prometheus:2.47.2` |
| grafana:10.2.0 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/grafana:10.2.0` |
| skywalking-oap-server:9.3.0 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/skywalking-oap-server:9.3.0` |
| **搜索** | |
| elasticsearch:7.17.14 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/elasticsearch:7.17.14` |
| kibana:7.17.14 | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/kibana:7.17.14` |
| **Node** | |
| node:18-alpine | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/node:18-alpine` |
| node:20-alpine | `docker pull registry.cn-hangzhou.aliyuncs.com/xfg-studio/node:20-alpine` |

## 在 docker-compose.yml 中使用

```yaml
services:
  mysql:
    image: registry.cn-hangzhou.aliyuncs.com/xfg-studio/mysql:8.0.32
    container_name: mysql
    command: --default-authentication-plugin=mysql_native_password
    restart: always
    environment:
      TZ: Asia/Shanghai
      MYSQL_ROOT_PASSWORD: 123456
    ports:
      - "13306:3306"
    volumes:
      - ./mysql/my.cnf:/etc/mysql/conf.d/mysql.cnf:ro
      - ./mysql/sql:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 10s
      retries: 10
      start_period: 15s

  redis:
    image: registry.cn-hangzhou.aliyuncs.com/xfg-studio/redis:7.2
    container_name: redis
    restart: always
    environment:
      TZ: Asia/Shanghai
    ports:
      - "16379:6379"

  app:
    image: registry.cn-hangzhou.aliyuncs.com/xfg-studio/openjdk:17-jdk-slim
    container_name: form-app
    ports:
      - "8080:8080"
    depends_on:
      mysql:
        condition: service_healthy
```

## 在 Dockerfile 中使用

```dockerfile
# 构建阶段
FROM registry.cn-hangzhou.aliyuncs.com/xfg-studio/openjdk:17-jdk-slim AS builder

WORKDIR /build
COPY . .
RUN apt-get update && apt-get install -y maven && \
    mvn clean package -DskipTests -B

# 运行阶段
FROM registry.cn-hangzhou.aliyuncs.com/xfg-studio/openjdk:17-jdk-slim

WORKDIR /app
COPY --from=builder /build/*/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## 添加新镜像

如需添加新镜像，向 [docker-image-pusher](https://github.com/fuzhengwei/docker-image-pusher) 仓库提 PR，
在 `images.txt` 中添加镜像名，约 1 分钟后自动同步到阿里云。

## 参考

- 镜像仓库：https://github.com/fuzhengwei/docker-image-pusher
- 阿里云仓库：`registry.cn-hangzhou.aliyuncs.com/xfg-studio/`