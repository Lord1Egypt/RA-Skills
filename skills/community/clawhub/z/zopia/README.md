# Zopia Skills

Zopia AI 视频创作技能 — 通过 [Zopia](https://zopia.ai) 平台的 AI Agent 进行视频/图片创作。

覆盖场景：AI 视频生成（文生视频、图生视频）、AI 图片生成（角色设定图、分镜关键帧）、剧本创作、角色设计、分镜设计、多集连续剧制作。

## 安装

### 通过 npx 安装（推荐）

```bash
npx skills add 11cafe/zopia-skills
```

> [`skills`](https://github.com/vercel-labs/skills) 是 Vercel Labs 开发的跨平台技能安装 CLI，支持 Claude Code、Gemini CLI、Codex、Cursor 等 40+ 个 Agent。

安装到指定 Agent：

```bash
npx skills add 11cafe/zopia-skills -a claude-code
```

### 通过 OpenClaw 安装

在 [OpenClaw](https://openclaw.ai) 技能市场搜索 `zopia-skill`，或使用命令行：

```bash
npx clawhub install zopia-skill
```

### 手动安装

```bash
git clone https://github.com/11cafe/zopia-skills.git
```

将 `SKILL.md` 和 `scripts/` 目录复制到对应的技能目录：

| 范围 | 路径 |
|------|------|
| 个人全局 | `~/.claude/skills/zopia-skill/` |
| 项目级别 | `.claude/skills/zopia-skill/` |

## 配置

使用前需设置环境变量：

```bash
export ZOPIA_ACCESS_KEY="zopia-xxxxxxxxxxxx"   # 必需，30天有效
export ZOPIA_BASE_URL="https://zopia.ai"  # 可选，默认值即可
```

仅依赖 Python 标准库，无需安装第三方包。需要 `python3` 可用。

## 使用

安装技能后，在 Claude Code 中直接描述你的创作需求即可：

```
帮我做一个赛博朋克风格的短剧，讲一个机器人在废墟中寻找最后一朵花
```

技能会自动完成：创建项目 → 配置设置 → 发送创作指令 → 轮询进度 → 下载结果。

### 支持的风格

| ID | 说明 |
|----|------|
| `anime_japanese_korean` | 日韩动漫 |
| `realistic_3d_cg` | 3D CG 写实 |
| `pixar_3d_cartoon` | Pixar 3D 卡通 |
| `photorealistic_real_human` | 真人写实 |
| `3D_CG_Animation` | 3D CG 动画 |
| `anime_chibi` | Q版可爱 |
| `anime_shinkai` | 新海诚 |
| `anime_ghibli` | 吉卜力 |
| `stylized_pixel` | 像素艺术 |

### 支持的图片模型

分镜图（storyboard）与角色/场景图（entity）可分别配置，两者共享同一组可选值：

| 模型 | 名称 |
|------|------|
| `generate_image_by_nano_banana_2` | Nano Banana 2（storyboard 默认）|
| `generate_image_by_doubao_seedream_4` | Doubao Seedream 4（entity 默认）|
| `generate_image_by_nano_banana` | Nano Banana |
| `generate_image_by_gpt_image_2` | GPT Image 2 |

### 支持的视频模型

| 模型 | 名称 |
|------|------|
| `generate_video_by_kling_o3` | Kling O3 |
| `generate_video_by_kling_v3_0` | Kling V3.0 |
| `generate_video_by_hailuo_02` | Hailuo 2.3 |
| `generate_video_by_wan26_i2v` | Wan 2.6 |
| `generate_video_by_wan26_i2v_flash` | Wan 2.6 Flash |
| `generate_video_by_viduq2_pro` | Vidu Q2 Pro |
| `generate_video_by_viduq3_pro` | Vidu Q3 Pro |
| `generate_video_by_viduq3` | Vidu Q3 |
| `generate_video_by_seedance_15` | Seedance 1.5 Pro |

### 脚本列表

| 脚本 | 用途 |
|------|------|
| `create_project.py` | 创建项目 |
| `save_settings.py` | 配置项目设置 |
| `send_message.py` | 发送创作指令 |
| `query_session.py` | 查询创作进度 |
| `download_results.py` | 下载媒体资源 |
| `get_balance.py` | 查询余额 |
| `list_projects.py` | 列出所有项目 |
| `manage_episodes.py` | 管理剧集 |
| `render_episode.py` | 合成最终视频（MP4） |

## License

[MIT](LICENSE)
