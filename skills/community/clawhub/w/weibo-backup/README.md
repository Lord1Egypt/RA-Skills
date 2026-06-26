使用 Playwright 自动化下载微博收藏，本人或其他博主微博内容的工具， 以Markdown格式保存。

---

## 功能特性

- 支持下载微博收藏、本人微博、他人微博
- 图片（支持九宫格排列，支持多种尺寸：360px、480px、690px、2000px、原图 large）
- 视频（可选下载， 默认最高质量）
- 长文章（可选下载）
- 微博新支持的markdown展现的长文章
- **Markdown 双向链接** - 在保存的 Markdown 文件中添加"前一条"和"下一条"导航链接，方便浏览

请正确使用本技能，用于微博收藏、个人数据备份或者关注博主的内容备份保存。不能用于大规模的商业数据采集。
## 前置要求

1. **Python 环境**：需要 Python 3.8+
2. **依赖安装**：
   ```bash
   pip install playwright
   playwright install chromium
   ```

## 通过Agent Skill 运行

- 自动安装Skill (推荐)
  npx skills add https://www.modelscope.cn/skills/hhjinhh/weibo-data-backup
- 手动安装Skill
  把项目clone到本地, 把weibo-data-backup 目录复制到agent skills目录下， 如 .opencode/skills 或 .claude/skills/目录下

## 手动运行脚本

### 首次使用（下载10条记录，360px图片， 不下载视频，  可以快速得到预览结果）

1. 运行脚本，会自动打开浏览器
2. 在 60 秒内完成微博登录，并进入需要下载的页面（收藏页/本人主页/他人主页）
3. 等待自动开始下载

```bash
python weibo_favorites_4skill.py
```

注： 不提供output-dir参数，默认输出到python脚本所在目录下的output目录。

### 日常使用（推荐配置，推荐给用户后续的日常使用，headless 模式，下载600条记录包括高清图片，视频，长文章， 跳过已存在的记录）

首次使用后，后续运行时不用登录微博，直接从第一次运行生成的cookies.json文件中读取登录状态。

```bash
python weibo_favorites_4skill.py \
  --image-size large \
  --download-video \
  --download-article \
  --max-download 600 \
  --skip-existing \
  --headless
```

### 指定输出目录

```bash
python weibo_favorites_4skill.py \
  --output-dir "/path/to/custom/output" \
  --max-download 100
```

## 参数说明

| 参数                  | 说明                           | 默认值                                      |
| -------------------  | ------------------------------ | ---------------------------------------    |
| `--url`              | 目标微博用户主页或收藏页面URL      | https://weibo.com                          |
| `--max-download`     | 最大下载数量                     | 10                                         |
| `--skip-existing`    | 跳过已存在的记录                  | False                                      |
| `--image-size`       | 图片尺寸：360/480/690/2000/large | 360                                        |
| `--download-video`   | 下载视频到本地                    | 开关参数，不需要指定值，无此参数则只保留视频链接   |
| `--download-article` | 下载长文章到本地                  | 开关参数，不需要指定值，无此参数则只保留文章链接   |
| `--batch-size`       | 分批次每次下载记录数               | 20                                         |
| `--headless`         | 无头模式（不显示浏览器）            | 开关参数，不需要指定值，无此参数则显示浏览器窗口   |
| `--user-data-dir`    | 浏览器用户数据目录                 | 无此参数默认使用 cookies.json                 |
| `--output-dir`       | 自定义输出目录                    | python脚本所在目录下的output目录               |

## 输出目录结构

```
output/
├── pictures/          ## 图片目录
│   └── {record_id}/   ## 每条微博的图片
├── videos/            ## 视频目录
├── articles/          ## 长文章目录
│   └── pictures/      ## 文章中的图片
└── {author}_{date}_{id}.md  ## 微博内容Markdown文件
```

### Markdown 文件格式示例

```markdown
## 作者名  发布时间 : 

前一条：[前一条微博描述](作者名_2024-01-15_xxxx.md) | 下一条：[下一条微博描述](作者名_2024-01-15_yyyy.md)

## 正文

微博正文内容...

## 图片

![图片1](pictures/record_id/group1_1.jpg)
![图片2](pictures/record_id/group1_2.jpg)

## 视频

[视频文件](videos/record_id.mp4)

 
```

## 故障排除

### 登录问题

- 检查网络连接
- 尝试删除 cookies.json 或 browser_data 目录重新登录
- 确保没有开启 VPN 或代理导致访问异常

### 下载失败

- 检查磁盘空间
- 检查目录权限
- 尝试降低 `--max-download` 数量

### 浏览器启动失败

- 确保已运行 `playwright install chromium`
- 检查系统是否支持 Chromium 运行

### 内容展开问题

- 程序会自动点击"展开"按钮获取完整内容
- 如果仍有内容被截断，可能是微博平台的限制
