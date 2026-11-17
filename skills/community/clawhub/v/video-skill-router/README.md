# 视频创作技能路由器 · Video Creation Skill Router

[English](./README.en.md) · **在线文档：** https://guipi888.github.io/video-skill-router/

想做视频却不知道用什么工具？想让 AI 帮你「找技能 → 装技能 → 做视频 → 一条龙」？视频创作技能路由器（Video Creation Skill Router）是一个 AI video skill / animation skill 元技能——视频/动画创作的能力发现与编排层——你只管说需求（"把勾股定理做成讲解动画""给我的 APP 做个宣传片""剪掉这段口播的口误"），它自动完成：判定视频类别（商业宣传/知识科普/其他）→ 优先匹配本地已装技能 → 本地没有就按类别走对应渠道发现并下载安装（内置精选目录 → GitHub 实时搜索 → 网络搜索）→ 编排执行所装技能，输出剪辑后的视频文件 → 最后告诉你装了什么技能、有什么用，问你要保留还是卸载。

安装/卸载全程走安全协议：git 快照可回滚、frontmatter 强校验、多技能包需明确选择、禁 rm -rf。适合：自媒体视频创作者、知识科普 UP 主、电商带货团队、想用 AI 做视频但零技能起步的普通用户。Video creation skill router for animation & video makers.

## 解决什么问题

- **不知道用什么技能做视频**：内置 11 个 GitHub 实证技能包精选目录（manim_skill 1201★、motion-design-skill 2441★、OpenMontage 70908★、herk-edit-kit 2017★ 等），按视频类别自动匹配，零网络成本
- **本地没有相关能力**：按类别走不同渠道——商业宣传类淘动效/模板/广告技能，知识科普类淘数学动画/数据可视化，其他类淘剪辑/字幕/配音，GitHub + 网络双通道兜底
- **装了技能不会编排**：下载完成后自动通读并调用所装技能，按其工作流执行，缺环用 FFmpeg 补齐，直接产出成片
- **技能越装越乱**：每次生成后输出安装清单（技能/作用/来源），一键卸载走 git rm 或回收站机制，可回滚、零残留

Unlike single-engine skills (Manim-only or Remotion-only), this router covers the full pipeline: category detection → discovery → install → orchestration → output.

## Use Cases 适用场景

| 场景 | 示例需求 | 走哪条渠道 |
|------|----------|-----------|
| 数学/科学讲解动画（math explainer video） | 「把勾股定理的证明做成讲解动画」 | 知识科普类 → manim_skill 等 |
| 产品演示/宣传片（product demo & promo video） | 「给我的 APP 做个产品演示宣传视频」 | 商业宣传类 → motion-design 模板技能 |
| 口播剪辑（talking-head editing） | 「剪掉这段口播的口误和静音」 | 其他类 → herk-edit-kit 等 |
| 数据可视化视频（data visualization video） | 「把这份销售数据做成动态图表视频」 | 知识科普类 → 数据动画技能 |
| 字幕/白板动画（subtitle & whiteboard animation） | 「把 SRT 字幕做成白板手绘动画」 | 其他类 → 字幕动画技能 |
| 电商带货视频（e-commerce video） | 「给这款商品做个带货短视频」 | 商业宣传类 → 广告模板技能 |
| Lottie 网页动效（lottie web animation） | 「网页加载 lottie 动画」 | 商业宣传类 → motion-design-skill |

## 安装

### WorkBuddy 技能市场（推荐）

在 WorkBuddy 中搜索「视频创作技能路由器」一键安装。

### 手动安装

```bash
git clone https://github.com/guipi888/video-skill-router.git \
  ~/.workbuddy/skills/video-skill-router
```

### 环境依赖

- Python 3.8+（纯标准库，零第三方依赖）
- git（安装/卸载走 git 快照；非 git 环境自动降级为回收站机制）
- FFmpeg（执行层缺环时兜底，可选）

## 使用

安装后直接对 Agent 说需求即可，例如：

- 「把勾股定理的证明做成讲解动画」
- 「给我的 APP 做个产品演示宣传视频」
- 「这段口播素材帮我剪掉口误和静音」

路由器自动完成类别判定 → 匹配 → 下载 → 执行 → 善后询问，无需手动选技能。

也可单独调用三个脚本：

```bash
# 1. 匹配（本地已装技能 + 内置精选目录合并打分）
python3 scripts/match_skill.py --query "做数学公式讲解动画"

# 2. 发现（按类别走 GitHub 渠道）
python3 scripts/search_anim.py --category education --query "math animation"

# 3. 安装 / 清单 / 卸载
python3 scripts/manage_skill.py install --repo shuyicc/MathLens --reason "数学讲解"
python3 scripts/manage_skill.py list
python3 scripts/manage_skill.py uninstall --name MathLens
```

## 输出

- **成片**：`video-output/<日期>-<主题>/` 目录下的视频文件
- **善后报告**：本次安装清单表（技能名/作用/来源）+ 保留（回复 1）或卸载（回复 2）的交互询问

## 项目结构

```
SKILL.md                          # 路由编排主文件（五步流水线）
data/curated-catalog.json         # 内置精选目录（11 技能包 + 11 引擎库，GitHub API 实证）
references/
  categories.md                   # 视频类别 → 渠道矩阵
  catalog.md                      # 动画能力分类目录与本地登记表
  sources.md                      # 外部渠道清单 + GitHub 搜索语法 + 候选池
  repos.md                        # 本地 34 个视频技能 → 上游仓库溯源表
  install-protocol.md             # 安装/卸载安全协议
scripts/
  match_skill.py                  # 需求→技能匹配打分（本地+目录）
  search_anim.py                  # 多渠道动画技能搜索（GitHub API）
  manage_skill.py                 # 安装/清单/卸载管理（快照+校验+回滚）
docs/
  index.html                      # 落地页（GitHub Pages: guipi888.github.io/video-skill-router）
  social-preview.html             # 社交预览图源文件（1280×640）
  images/social-preview.png       # 社交预览图（Settings → Social preview 上传用，仓库内留存真值）
```

## 关于作者

**桂皮 Guipi** — AI Agent 开发者 · 超级个体践行者
专注 AI 效率工具与一人公司方法论，帮普通人用 AI 成为超级个体

| 平台 | 账号 |
|------|------|
| 📱 小红书 | [桂皮AI实战](https://www.xiaohongshu.com/user/profile/5a409dda44363b313b9d7e15) |
| 🎬 抖音 | [桂皮AI实战](https://v.douyin.com/QJRjHGAtrvA/) |
| 📺 视频号 | 微信内搜「桂皮AI实战」 |
| 💬 公众号 | 微信搜「桂皮AI实战」 |
| 🌟 知识星球 | [AI超级个体](https://t.zsxq.com/guSUk) — AI工具 · 创作 · 产品 · 流量 · 变现 |
| 🐙 GitHub | [guipi888](https://github.com/guipi888) |
| 💬 微信 | guipi996（注明来意） |

## License

MIT License — 详见 [LICENSE](./LICENSE)
