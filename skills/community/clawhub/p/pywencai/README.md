# PyWenCai 问财选股 Skill

[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](https://github.com/zsrl/pywencai)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-BossQuant-purple.svg)](https://clawhub.com)

同花顺问财自然语言数据查询工具，用中文自然语言查询A股数据。

## ✨ 特性

- 🗣️ **中文自然语言查询** - 用自然语言描述选股条件，无需记忆接口
- 🌐 **多市场支持** - 股票、指数、基金、可转债等多种查询类型
- 📄 **自动翻页** - 支持 loop 参数自动获取全部结果
- 🔍 **多种查询类型** - stock/zhishu/fund/conbond 等

## 📥 安装

```bash
pip install pywencai --upgrade
```

## ⚙️ 配置

需要问财网站 Cookie 才能使用：

1. 登录 [问财网站](https://www.iwencai.com/)
2. 打开浏览器开发者工具，获取 Cookie
3. 在代码中传入 cookie 参数或设置环境变量 `WENCAI_COOKIE`

## 🚀 快速开始

```python
import pywencai

# 基本查询 - 今日涨停股票
df = pywencai.get(query='今日涨停股票', cookie='your_cookie_here')
print(df.head())

# 财务筛选
df = pywencai.get(query='市盈率小于20，市值大于100亿', cookie='your_cookie_here')
print(df.head())
```

## 📊 支持的查询类型

| 类型 | query_type | 说明 |
|------|-----------|------|
| 股票 | `stock` | A股股票查询（默认） |
| 指数 | `zhishu` | 指数数据查询 |
| 基金 | `fund` | 基金数据查询 |
| 可转债 | `conbond` | 可转债数据查询 |

## 📖 更多示例

```python
import pywencai

# 指定查询类型
df = pywencai.get(query='沪深300成分股', query_type='stock', cookie='xxx')

# 排序
df = pywencai.get(query='今日涨幅前50', sort_key='涨跌幅', sort_order='desc', cookie='xxx')

# 自动翻页获取全部结果
df = pywencai.get(query='市盈率小于15的股票', loop=True, cookie='xxx')

# 可转债查询
df = pywencai.get(query='转股溢价率小于10%', query_type='conbond', cookie='xxx')
```

## 📄 许可证

MIT License

## 📊 更新日志

### v1.3.0 (2026-03-23)
- 🎉 增加更丰富的AI Agent演示和高阶使用指南
- 🔄 更新版本号并清理失效链接


### v1.2.0 (2026-03-15)
- 🎉 初始版本发布
- 📊 支持中文自然语言A股数据查询

---

## 🤝 社区与支持

- **维护者**：大佬量化 (Boss Quant)
- **主页**：https://github.com/zsrl/pywencai
- **ClawHub**：https://clawhub.com
