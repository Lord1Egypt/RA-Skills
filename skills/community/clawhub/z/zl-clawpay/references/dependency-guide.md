# Node.js 依赖管理指南

ZL-ClawPay 技能的 Node.js 版本依赖管理。

## 所需依赖

| 包名 | 版本 | 用途 |
|---------|---------|---------|
| sm-crypto | ^0.3.14 | SM2/SM3/SM4 国密算法 |
| axios | ^1.16.0 | HTTP 客户端 |
| dotenv | ^16.6.1 | 环境变量管理 |

## 安装

在技能根目录执行：

```bash
npm install
```

**要求**：Node.js 版本 >= 18.0.0

## 常见问题

### 依赖安装失败

执行 `npm install` 即可安装所需依赖。如果安装失败，请检查网络连接或 Node.js 版本。

### Node.js 版本过低

检查当前版本：
```bash
node --version
```

如版本低于 18.0.0，需要升级 Node.js。
