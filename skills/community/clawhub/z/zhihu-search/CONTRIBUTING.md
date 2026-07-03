# Contributing to zhihu-search

感谢对 zhihu-search 的关注!本 skill 目标是**稳定、易用、零对抗**地抓取知乎内容。

## 开发环境

```bash
git clone https://github.com/excalibursssooo/zhihu-search.git
cd zhihu-search

# 准备 cookie (跟正式使用一样)
mkdir -p data
echo "_xsrf=xxx; d_c0=xxx; z_c0=xxx; ..." > data/cookies.txt
chmod 600 data/cookies.txt

# 跑测试 (随便抓一个)
python3 zhihu-fetch.py hotlist --limit 3
```

## 提交代码

1. **Fork** → 创建 feature branch (`git checkout -b feat/xxx`)
2. **改动** + 跑端到端测试 (见下方)
3. **Commit**: 写清楚改了什么、为什么 (中文 OK)
4. **Push** → **Pull Request** 到 `main` 分支

## 端到端测试 checklist

提交前必跑:
```bash
# 1. 搜索 (5 种 type 各跑一次)
python3 zhihu-fetch.py search "AI" --type question --limit 3
python3 zhihu-fetch.py search "AI" --type column --limit 3
python3 zhihu-fetch.py search "AI" --type people --limit 3
python3 zhihu-fetch.py search "AI" --type topic --limit 3
python3 zhihu-fetch.py search "AI" --type zvideo --limit 3

# 2. quick 一键 (用紧凑+完整两种模式)
python3 zhihu-fetch.py quick "AI 热点" --compact --md-out /tmp/test-quick-c.md
python3 zhihu-fetch.py quick "AI 热点" --md-out /tmp/test-quick.md

# 3. 答案 + 评论
python3 zhihu-fetch.py answers 2050261467174101567 --limit 5
python3 zhihu-fetch.py comments 2050463219832164626 --limit 3

# 4. 专栏
python3 zhihu-fetch.py column-articles c_1297485212247425024 --limit 3
python3 zhihu-fetch.py article 2039840725727195825

# 5. 热榜 + 路径
python3 zhihu-fetch.py hotlist --limit 3
python3 zhihu-fetch.py paths
python3 keepalive.py paths
```

## 路径管理约定

- **所有路径常量必须在 `paths.py` 定义** — 不要在脚本里硬编码 `/tmp/zhihu/` 或 `$SKILL/...`
- 新增命令时:
  - 落盘到 `$SKILL/data/<subdir>/` 下的子目录 (在 `paths.py` 加 `_ensure_dir(DATA_DIR / "<subdir>")`)
  - 用环境变量 `ZHIHU_DATA_DIR` / `ZHIHU_COOKIE_FILE` 支持覆盖
- 路径变更时要**保持向后兼容** — 老路径不删,自动 fallback

## 反爬策略

- **永远优先用 API** — `grep -nE "(\"/api/v4/|api\.zhihu\.com)"` 验证
- **不要 patch navigator.webdriver / 拖滑块** — 工业级 captcha 不可行
- **不要循环重试 captcha 触发** — 等 30s 再试
- **评论区反爬**: 用 `/api/v4/answers/<aid>/comments` 而非 `comment_v5` (后者 `data=[]`)
- **话题 API 已废**: `/api/v4/topics/<t_id>/feeds*` 全 10003,不要尝试

## 代码风格

- Python 3.8+ 兼容 (不要用 3.10+ 的 `match` 语法)
- 函数 docstring 用三引号中文 (跟现有风格一致)
- print 信息简洁, 错误用 `sys.exit(1)` + stderr
- 不要新增第三方依赖 (只用 `subprocess` + `json` + `re` + `urllib`)

## 发布流程

1. 更新 `CHANGELOG.md` (新版本号 + 改动列表)
2. 更新 `SKILL.md` frontmatter 的 `version`
3. 跑端到端测试,确认所有命令正常
4. `git tag v1.x.x` + `git push --tags`
5. 在 GitHub 创建 release (标题 + 详细说明)
6. clawhub 自动同步(无需手动)

## 报告 Bug

提交 issue 时请包含:
- 你跑的命令 (完整, 含参数)
- 报错信息 (stdout + stderr)
- `python3 zhihu-fetch.py paths` 的输出
- 知乎是否刚改版 (可附上 https://www.zhihu.com/ 是否正常访问的截图)

## License

贡献的代码采用 MIT License — 详见 [LICENSE](LICENSE)。
