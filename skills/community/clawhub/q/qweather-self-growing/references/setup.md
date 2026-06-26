# qweather 配置说明

## 前置条件

1. 在[和风天气控制台](https://console.qweather.com)创建项目
2. 创建 JWT 凭据（Ed25519），上传公钥
3. 在控制台 → 设置中获取你的 API Host（格式如 `xxx.qweatherapi.com`）

## 方式一：环境变量

```bash
export QWEATHER_KID="YOUR_KID"
export QWEATHER_PROJECT_ID="YOUR_PROJECT_ID"
export QWEATHER_PRIVATE_KEY_PATH="$HOME/.config/qweather/ed25519-private.pem"
export QWEATHER_API_HOST="YOUR_API_HOST"
```

## 方式二：本地配置文件

创建 `local/qweather.json`：

```json
{
  "kid": "YOUR_KID",
  "projectId": "YOUR_PROJECT_ID",
  "privateKeyPath": "/absolute/path/to/ed25519-private.pem",
  "apiHost": "YOUR_API_HOST"
}
```

## 初始化

配置完成后运行，下载城市数据并验证连通性：

```bash
bash ./scripts/init.sh
```

## 可选：本地城市快捷映射

创建 `local/cities.json`：

```json
{
  "苏州": "101190401",
  "杭州": "101210101"
}
```

## 密钥生成

```bash
openssl genpkey -algorithm ED25519 -out ed25519-private.pem
openssl pkey -pubout -in ed25519-private.pem > ed25519-public.pem
```

将公钥上传到和风天气控制台，私钥保留在本机安全目录。
