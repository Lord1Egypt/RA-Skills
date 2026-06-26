# 微信小程序分包策略

## 核心限制

| 项目 | 限制 |
|------|------|
| 主包大小 | ≤ 2MB |
| 单个分包大小 | ≤ 2MB |
| 单个分包加载后可使用的随机读取资源 | ≤ 200KB |
| 小程序总大小（含主包+全部分包） | ≤ 20MB（静态资源另计） |
| 分包数量上限 | 无明确限制，但建议 ≤ 10 |

---

## 分包结构

```
miniprogram/
├── app.js / app.json / app.wxss / app.wxss    # 主包（必须存在）
├── pages/                                      # 主包页面（启动时必需）
│   ├── index/
│   └── logs/
├── subpackages/                                # 分包根目录（也可放于其他路径）
│   ├── packageA/                               # 分包 A
│   │   ├── pages/
│   │   │   ├── cat/
│   │   │   └── dog/
│   │   └── package.json                       # 可选，分包私有配置
│   └── packageB/                               # 分包 B
│       └── pages/
└── static/                                     # 公共静态资源（主包使用）
```

---

## app.json 配置示例

```json
{
  "pages": [
    "pages/index/index",
    "pages/logs/logs"
  ],
  "subpackages": [
    {
      "root": "subpackages/packageA",
      "name": "packageA",
      "pages": [
        "pages/cat/index",
        "pages/dog/index"
      ]
    },
    {
      "root": "subpackages/packageB",
      "name": "packageB",
      "pages": [
        "pages/detail/index"
      ]
    }
  ],
  "preloadRule": {
    "pages/index/index": {
      "network": "all",
      "packages": ["packageA"]
    }
  }
}
```

### 关键字段说明

- `root`: 分包根路径，相对 `app.json` 所在目录
- `name`: 分包别名，用于预加载等场景
- `pages`: 该分包下的页面路径（相对于 root）
- `preloadRule`: 分包预加载规则（可选）

---

## 分包加载规则

### 触发时机
- 用户首次访问分包内页面时，微信自动下载该分包
- 可通过 `preloadRule` 提前预加载

### 页面跳转（分包间跳转）
- **同分包内**：直接 `wx.navigateTo`
- **跨分包跳转**：使用 `navigateToMiniProgram` 或 `navigateBack`

### 分包间页面引用
- **主包 → 分包**：可 require 分包代码（会导致主包增大，需谨慎）
- **分包 → 主包**：可直接 require 主包代码
- **分包 A ↔ 分包 B**：不可直接互相 require，需通过 `postMessage` / events 通信

---

## 分包独立设置（package.json）

分包可有自己的 `app.json`（命名为 `package.json`），用于分包私有配置：

```json
{
  "private": true,
  "setting": {
    "urlCheck": false
  }
}
```

---

## 资源加载规则

| 资源类型 | 主包 | 分包 |
|----------|------|------|
| `wxss` 中引用的图片 | ✅ | ✅ |
| `js` 中 `require('path')` 的图片 | ❌ 必须用 `static` 相对路径 | ❌ 同左 |
| `wx.preloadResources` | ✅ | ✅ |
| 网络图片 | ✅ | ✅ |
| 分包私有静态资源 | ❌ 放主包或 CDN | ✅ 放分包内 |

> ⚠️ **重要**：所有在 WXSS 中通过相对路径引用的图片，编译时会被打入引用者所在的包。小程序不执行动态路径拼接的资源引用。

---

## 分包大小计算方法

在微信开发者工具中：**详情 → 基本信息 → 已使用包大小**  
或使用命令：
```bash
npm run build --report   # 配合 taro/webpack 分析
```

---

## 常见问题

### Q: 分包页面首次加载慢？
A: 使用 `preloadRule` 预加载，或将首屏页面放主包。

### Q: 分包间共享代码怎么办？
A: 将公共代码抽取到 **common 分包** 或放在主包，使用 `require` 引用。

### Q: 静态资源放哪里？
A: 公共资源放 `static/`（主包），分包私有资源放分包目录下。

### Q: 分包加载失败？
A: 检查 `app.json` 中 `root` 路径是否正确，确保分包目录下有 `pages/`。
