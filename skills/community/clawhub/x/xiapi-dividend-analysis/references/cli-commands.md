# CLI 命令参考

## 基本命令

### 获取红利指数打分数据

```bash
npx daxiapi-cli@latest dividend score -c <code>
```

**参数说明**：
- `-c, --code <code>`：指数代码（必填）

**返回数据**：
- 日期（date）
- 分数（score）
- cs值（cs）
- rsi值（rsi）

## 常用指数代码

| 指数名称      | 代码       |
| ------------- | ---------- |
| 红利低波      | 2.H30269   |
| 红利低波100   | 2.930955   |
| 中证红利      | 1.000922   |
| 中证现金流    | 2.932365   |

## HTTP API 请求

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://daxiapi.com/coze/get_dividend_score?code=2.H30269"
```

## 配置命令

### 设置 Token

```bash
npx daxiapi-cli@latest config set token YOUR_TOKEN
```

### 查看 Token 配置

```bash
npx daxiapi-cli@latest config get token
```

## 使用示例

### 分析红利低波指数

```bash
npx daxiapi-cli@latest dividend score -c 2.H30269
```

### 分析中证红利指数

```bash
npx daxiapi-cli@latest dividend score -c 1.000922
```
