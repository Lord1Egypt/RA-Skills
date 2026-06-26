# TradeAlpha Skill

这个目录是独立发布的 skill。

它只包含自然语言路由规则，不包含真正的登录或新闻执行代码。

## 依赖

这个 skill 需要外部插件提供以下两个工具：

- `tradealpha_login`
- `tradealpha_news`

如果当前会话里没有这两个工具，skill 本身不能直接完成登录或拉新闻。

## 发布

在仓库根目录执行：

```bash
npx clawhub@latest publish ./liangxi_news_skill --slug tradealpha-open-platform --version 0.6.0
```
