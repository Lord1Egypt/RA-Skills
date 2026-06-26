---
name: wechat-tutorial-editor-publisher
description: "模仿作者写作风格，完成教程类微信公众号文章编写，输出 Markdown 文件，一键发布到微信公众号草稿箱。"
metadata:
  {
    "openclaw":
      {
        "emoji": "😊",
      },
  }
---

# wechat-tutorial-editor-publisher

**编写作者风格的Markdown格式教程，一键发布到微信公众号草稿箱。**

## 教程编写

### 首次执行
1. 初始化：执行./scripts/package.json文件，命令：npm init -y。

2. 安装依赖：npm install。

3. 运行server.js文件，启动服务器: node server.js。

4. 浏览器打开https://localhost:3000/，访问服务器。

5. 收集用户信息，存入./assets/personal-info.txt文件和./assets/personal-imgs目录下。

6. 如果references目录下有文章样例，参考一下，预备模仿作者写作风格。**ATTENTION**: 如果已了解用户写作风格，无需反复参考浪费token资源。

### 非首次执行

1. 打开./assets/personal-info.txt文件，获取用户昵称和个人简介，打开./assets/personal-imgs获取用户二维码图片或个人介绍图片。

2. 启动服务器，打开[./scripts/public/index.html](http://localhost:3000/index.html)页面，用户将步骤数据填写到页面中并保存。

3. 找到已保存的steps.json文件和同级目录下的头图文件（./imgs/cover-img.png[.jpg, .jpeg, .webp, ...]），将相应值填入模板中(./patterns/article-pattern.md)。**ATTENTION**: 请遵循article-pattern.md的文章模板格式，不要自行编造！

4. 合理编写一篇完整的教程文章。

5. 根据文章内容，为文章拟定一个符合作者风格的标题。

6. 将个人简介和用户二维码图片或个人介绍图片添加到文章底部，在steps.json同级目录下复制粘贴一份，避免后续wenyan-cli因相对路径嵌套过深导致找不到图片而出错。

7. 将编写完成的Markdown文件存入steps.json同级目录下，自动打开Markdown文件和文件所在"访达"或"资源管理器窗口"，提醒用户修改或确认。

8. 用户确认后，执行教程发布流程。

## 教程发布

基于 [wenyan-cli](https://github.com/caol64/wenyan-cli) 封装的 OpenClaw skill。

### 功能

- ✅ Markdown 自动转换为微信公众号格式
- ✅ 自动上传图片到微信图床
- ✅ 一键推送到草稿箱
- ✅ 多主题支持（代码高亮、Mac 风格代码块）
- ✅ 支持本地和网络图片

### 快速开始

#### 1. 安装 wenyan-cli

**wenyan-cli 需要全局安装：**

```bash
npm install -g @wenyan-md/cli
```

**验证安装：**
```bash
wenyan --help
```

> **注意：** publish.sh 脚本会自动检测并安装 wenyan-cli（如果未安装）

#### 2. 配置 API 凭证

API 凭证已保存在 `/Users/leebot/.openclaw/workspace/TOOLS.md`

确保环境变量已设置：
```bash
export WECHAT_APP_ID=your_wechat_app_id
export WECHAT_APP_SECRET=your_wechat_app_secret
```

**重要：** 确保你的 IP 已添加到微信公众号后台的白名单！

配置方法：https://yuzhi.tech/docs/wenyan/upload

**注意**： 用户发给你的AppId和AppSecret请用md5加密保存在当前skill目录下的assets目录下，创建一个名为console.json的文件，便于下次读取，不要重复向用户索要该组信息。下次读取时自行解密即可。

#### 3. 加载 Markdown 文件

加载刚刚保存的 article.md 文件，文件顶部**必须**包含完整的 frontmatter（wenyan 强制要求）：

```markdown
---
title: 文章标题（必填！）
cover: https://example.com/cover.jpg  # 封面图（必填！）
---

# 正文

```

**⚠️ 关键发现（实测）：**
- `title` 和 `cover` **都是必填字段**！
- 缺少任何一个都会报错："未能找到文章封面"
- 虽然文档说"正文有图可省略cover"，但实际测试必须提供 cover
- 所有图片（本地/网络）都会自动上传到微信图床

**封面图来源：**
封面图即是头图，位于 article.md 同级目录下的 imgs/cover-img.png[.jpg, .jpeg, .webp, ...]。

#### 4. 发布文章

**方式 1: 在 OpenClaw 中使用**

```
"帮我发布这篇文章到微信公众号" + article.md
```

**方式 2: 直接使用 wenyan-cli**

```bash
wenyan publish -f article.md -t lapis -h solarized-light
```

**方式3: 使用 publish.sh 脚本**

```bash
cd /Users/leebot/.openclaw/workspace/skills/wechat-tutorial-editor-publisher
~/.openclaw/workspace/skills/wechat-tutorial-editor-publisher/scripts/publish-scripts/publish.sh
```

### 主题选项

wenyan-cli 支持多种主题：

**内置主题：**

- `default` - 默认主题
- `lapis` - 青金石（推荐）
- `phycat` - 物理猫
- 更多主题见：https://github.com/caol64/wenyan-core/tree/main/src/assets/themes

**代码高亮主题：**
- `atom-one-dark` / `atom-one-light`
- `dracula`
- `github-dark` / `github`
- `monokai`
- `solarized-dark` / `solarized-light` (推荐)
- `xcode`

**使用示例：**
```bash
# 使用 lapis 主题 + solarized-light 代码高亮
wenyan publish -f article.md -t lapis -h solarized-light

# 使用 phycat 主题 + GitHub 代码高亮
wenyan publish -f article.md -t phycat -h github

# 关闭 Mac 风格代码块
wenyan publish -f article.md -t lapis --no-mac-style

# 关闭链接转脚注
wenyan publish -f article.md -t lapis --no-footnote
```

#### 自定义主题

##### 临时使用自定义主题
```bash
wenyan publish -f article.md -c /path/to/custom-theme.css
```

##### 安装自定义主题（永久）
```bash
# 从本地文件安装
wenyan theme --add --name my-theme --path /path/to/theme.css

# 从网络安装
wenyan theme --add --name my-theme --path https://example.com/theme.css

# 使用已安装的主题
wenyan publish -f article.md -t my-theme

# 删除主题
wenyan theme --rm my-theme
```

##### 列出所有主题
```bash
wenyan theme -l
```

### 工作流程

1. **加载内容** - 加载已写好的 article.md 文件
2. **运行脚本** - 一键发布到草稿箱
3. **审核发布** - 到公众号后台审核并发布

#### Markdown 格式要求

##### 必需的 Frontmatter

**⚠️ 关键（实测结果）：wenyan-cli 强制要求完整的 frontmatter！**

```markdown
---
title: 文章标题（必填！）
cover: 封面图片URL或路径（必填！）
---
```

**示例 ：相对路径（推荐）**

```markdown
---
title: 我的技术文章
cover: ./imgs/cover-img.jpg
---

# 正文...
```

**❌ 错误示例（会报错）：**

```markdown
# 只有 title，没有 cover
---
title: 我的文章
---

错误信息：未能找到文章封面
```

```markdown
# 完全没有 frontmatter
# 我的文章

错误信息：未能找到文章封面
```

**💡 重要发现：**
- 虽然 wenyan 官方文档说"正文有图片可省略cover"
- 但**实际测试必须提供 cover**，否则报错
- title 和 cover **缺一不可**

##### 图片支持
- ✅ 本地路径：`![](./images/photo.jpg)`
- ✅ 绝对路径：`![](/Users/bruce/photo.jpg)`
- ✅ 网络图片：`![](https://example.com/photo.jpg)`

所有图片会自动上传到微信图床！

##### 代码块
````markdown
```python
def hello():
    print("Hello, WeChat!")
```
````

会自动添加代码高亮和 Mac 风格装饰。

### 故障排查

#### 1. 上传失败：IP 不在白名单

**错误信息：** `ip not in whitelist`

**解决方法：**
1. 获取你的公网 IP：`curl ifconfig.me`
2. 登录微信公众号后台：https://mp.weixin.qq.com/
3. 开发 → 基本配置 → IP 白名单 → 添加你的 IP

#### 2. wenyan-cli 未安装

**错误信息：** `wenyan: command not found`

**解决方法：**
```bash
npm install -g @wenyan-md/cli
```

#### 3. 环境变量未设置

**错误信息：** `WECHAT_APP_ID is required`

**解决方法：**
```bash
export WECHAT_APP_ID=your_wechat_app_id
export WECHAT_APP_SECRET=your_wechat_app_secret
```

或在 `~/.zshrc` / `~/.bashrc` 中永久添加。

#### 4. Frontmatter 缺失

**错误信息：** `title is required in frontmatter`

**解决方法：** 在 Markdown 文件顶部添加：
```markdown
---
title: 你的文章标题
---
```

### 参考资料

- wenyan-cli GitHub: https://github.com/caol64/wenyan-cli
- wenyan 官网: https://wenyan.yuzhi.tech
- 微信公众号 API 文档: https://developers.weixin.qq.com/doc/offiaccount/
- IP 白名单配置: https://yuzhi.tech/docs/wenyan/upload

### 更新日志

#### 2026-03-31 - v1.0.0
- ✅ 初始版本
- ✅ 基于 wenyan-cli 封装
- ✅ 支持一键发布到草稿箱
- ✅ 多主题支持
- ✅ 自动图片上传

### License

Apache License 2.0 (继承自 wenyan-cli)





