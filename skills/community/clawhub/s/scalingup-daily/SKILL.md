# 搜广推领域模型 Scaling Up 日报生成技能 v2.0

## 适用场景

- 用户说"生成今天的搜广推日报"或"跑一下 ScalingUp 日报"
- 自动化任务每周一 08:00 触发（任务 ID: scaling-up-2）
- 需要系统性追踪搜广推领域最新论文、技术文章、开源项目动态

## 信息源（6 类优先级）

### 优先级 1：ArXiv 论文 — 最新学术论文
使用 `web_search` 搜索以下关键词（最近 7 天的新论文）：
- `"arxiv recommendation system scaling law {year}"`
- `"arxiv CTR prediction transformer {year}"`
- `"arxiv generative recommendation advertising {year}"`
- `"arxiv sequential recommendation token mixer {year}"`
- `"arxiv unified modeling search recommendation {year}"`
- `"arxiv recommendation foundation model {year}"`
- `"arxiv scaling law recommendation {year}"`
- `"arxiv ads ranking model {year}"`
每个搜索取前 5 条结果。
对每篇论文记录：标题、arXiv ID、作者/机构、核心贡献、链接。

### 优先级 2：微信公众号 — 国内技术深度解读
使用 `wechat-article-search` skill 搜索以下关键词（最近 7 天）：
- `"推荐系统 Scaling Law"`
- `"搜广推 大模型"`
- `"序列建模 推荐"`
- `"生成式推荐"`
- `"TokenMixer 排序"`
每个关键词搜索 3-5 条。
对每篇文章记录：标题、公众号名、链接、发布日期、核心内容。

**微信搜索命令格式**：
```bash
cd {skill_dir} && NODE_PATH={skill_dir}/node_modules {node_path} scripts/search_wechat.js "关键词" -n 5
```
其中 `{skill_dir}` 为本 skill 的安装路径，`{node_path}` 为 Node.js 可执行文件路径。

### 优先级 3：知乎 — 深度技术分析
使用 `web_search` 搜索以下关键词（最近 7 天）：
- `"site:zhuanlan.zhihu.com 推荐系统 Scaling Law {year}"`
- `"site:zhuanlan.zhihu.com TokenMixer 推荐 {year}"`
- `"site:zhuanlan.zhihu.com 生成式推荐 广告 {year}"`
- `"site:zhuanlan.zhihu.com 搜广推 序列建模 {year}"`
- `"site:zhuanlan.zhihu.com OneRec OneRanker GR4AD"`
- `"site:zhuanlan.zhihu.com 推荐系统 大模型 {year}"`
- `"site:zhuanlan.zhihu.com UniMixer 推荐 {year}"`
- `"site:zhuanlan.zhihu.com 推荐系统 MoE 稀疏 {year}"`
每个搜索取前 5 条结果。

### 优先级 4：技术博客 — 大厂团队博客
使用 `web_search` 搜索以下关键词：
- `"site:ai.meta.com blog recommendation {year}"`
- `"site:research.google blog recommendation {year}"`
- `"美团技术团队 推荐 {year}"`
- `"字节跳动技术博客 推荐 {year}"`
- `"阿里巴巴技术 推荐系统 {year}"`
- `"快手技术博客 生成式推荐 {year}"`
- `"腾讯技术 推荐系统 {year}"`

### 优先级 5：GitHub Trending — 热门开源项目
使用 `web_search` 搜索以下关键词：
- `"GitHub recommendation system trending {year} stars"`
- `"GitHub awesome recommendation system {year}"`
- `"GitHub bytedance recommendation model open source"`
- `"GitHub Meta HSTU recommendation"`
- `"GitHub Kuaishou OneRec OpenOneRec"`
- `"github.com/trending 机器学习 推荐系统"`

### 优先级 6：行业会议 — KDD/WWW/ICML/NeurIPS/SIGIR 等
使用 `web_search` 搜索以下关键词：
- `"KDD {year} accepted papers recommendation"`
- `"WWW {year} recommendation system paper"`
- `"ICML {year} recommendation transformer paper"`
- `"NeurIPS {year} recommendation system paper accepted"`
- `"SIGIR {year} recommendation scaling sequential"`
- `"RecSys {year} accepted papers call"`
- `"WSDM {year} recommendation paper"`
- `"AAAI {year} recommendation system paper"`

## 重点关注的技术方向

- Scaling Law 在搜广推领域的验证与落地（Wukong/SUAN/EST/TokenMixer-Large 路线）
- TokenMixer 架构演进（RankMixer → TokenMixer-Large → UniMixer）
- 生成式端到端统一建模（OneRec/OneRanker/GR4AD）
- 稀疏注意力与 MoE 高效扩展（ULTRA-HSTU/LightSUAN）
- 多行为序列推荐与基础模型

## 已知核心论文（去重用，不需要重复列出）

参考 `references/known_papers.md` 文件。

---

## 日报生成格式

1. **标题**：`搜广推领域模型 Scaling Up 日报 | {当天日期}`
2. **驱动模型声明**：标题下方紧跟 `> 驱动模型：{AI模型名称}`（如 Claude-Opus-4.6、Gemini-3.0-Pro 等），标注本次辅助生成所使用的大模型名称
3. **趋势概览**：简要总结当日最重要的 2-3 个动态
4. 按信息源优先级分章节展示内容
5. 每个条目必须包含：标题/论文名、来源、**可访问的真实链接**、核心要点
6. 文末附「引文索引」，按平台分类整理所有链接
7. 在每个章节末尾标注当日该源检索到的条目数量
8. **强制结构化排版**：使用多级标题、列表、加粗高亮等 Markdown 元素增强可读性，严禁大段纯散文

日报模板参考 `templates/daily_report_template.md`。

---

## 引用链接规范（P0 级，强制执行）

日报中所有条目必须附上**真实可访问的引用链接**，**严禁使用占位符或编造链接**。

1. **ArXiv 论文**：必须通过 `web_search` 搜索论文标题确认真实的 `arxiv.org/abs/XXXX.XXXXX` 链接，绝不允许编造 abs ID（如 `2504.xxxxx`）
2. **GitHub 项目**：必须搜索确认真实的仓库 URL，不允许猜测 URL 路径
3. **微信公众号文章**：必须通过 `wechat-article-search` skill 搜索获取真实 `mp.weixin.qq.com` 链接
4. **知乎/博客文章**：必须提供可点击访问的原始链接
5. **学术会议**：必须提供会议官网或具体 proceedings 链接
6. **每条引用**在写入报告前必须通过 `web_search` 验证其真实性
7. 如果确实无法找到可验证的链接，应明确标注「链接待补充」，而非编造假链接

### 事实准确性

- 论文的作者归属、机构、发表会议等信息必须经过验证
- **机构归属必须基于作者 affiliation**，不可按部署场景/业务线推断（详见 `references/known_papers.md`）
- 会议论文数量、录取率等统计数据需从官方来源获取
- 遇到不确定的信息，优先 `web_fetch` arxiv 页面核对作者 affiliation，而非凭记忆填写

---

## 发布同步（双平台，强制执行）

日报生成后，**必须同时同步到以下两个平台**（缺一不可）：

### 平台 1：IMA 知识库「龙虾-模型ScalingUp」

- 知识库 ID：`6peD1tTQj2UYi41MTaDgLpfVnbCegcA-sjzZLJ0zVPA=`
- 上传流程：
  1. `create_media` 获取 COS 上传凭证
     - 必填参数：`file_name`, `file_size`, `content_type=text/markdown`, `knowledge_base_id`, `file_ext=md`
  2. 使用 `cos-upload.cjs` 脚本上传文件到 COS
  3. `add_knowledge` 将文件挂到知识库（`media_type=7`）
     - 必填参数：`media_type`, `media_id`, `title`, `knowledge_base_id`, `file_info.cos_key/file_size/file_name`
- 认证：`ima-openapi-clientid` + `ima-openapi-apikey`（凭证存于 `~/.config/ima/client_id`、`~/.config/ima/api_key`）
- Base URL：`https://ima.qq.com`（Base Path: `/openapi/wiki/v1/`）
- **限流处理**：遇 `code=220030` 时 sleep 15 秒后重试即可

### 平台 2：腾讯文档（Markdown 格式）

- 上传命令：
  ```bash
  # 用 jq 生成参数文件，避免命令行转义问题
  jq -Rn --arg title "搜广推模型ScalingUp日报_{日期}" \
         --rawfile mdx "{report_file}" \
         '{title:$title, mdx:$mdx, content_format:"markdown"}' > /tmp/td_args.json
  mcporter call tencent-docs create_smartcanvas_by_mdx --args "$(cat /tmp/td_args.json)"
  ```
- **标题上限 36 字符**（按字符数计算），超长会报 `business 400001`
- 前置条件：`mcporter` 已注册 `tencent-docs` server，token 有效

### 双平台一致性要求

- 两平台文件名/标题保持一致：`搜广推领域模型 Scaling Up 日报_YYYY-MM-DD`（腾讯文档标题可适当缩短以满足 36 字符限制）
- 日报以纯 Markdown 文本为主，图片若为外链可直接引用
- 若含本地图片或 base64，腾讯文档版需替换为 `upload_image` 返回的 `image_id`
- **IMA 和腾讯文档上传链应并行启动**，不要串行等待

---

## 输出文件

将日报保存为：`{workspace_dir}/搜广推领域模型 Scaling Up 日报_YYYY-MM-DD.md`

---

## 效率优化

- **并行化**：IMA 上传链与腾讯文档上传链必须并行启动
- **长流程三段分离**：检索 → 落盘 → 上传，每段完成后立即持久化到文件
- **subagent 并发上限 2 个**：每完成一个信息源就 append 到草稿文件
- **质量校验合并**：用一条 Python 脚本输出所有指标，不要分 5-6 条命令

---

## 依赖说明

### 前置 Skill
- `wechat-article-search`：微信公众号文章搜索（需先安装）
- `ima-skills`（或"腾讯ima"）：IMA 知识库操作（需先安装）
- `tencent-docs`：腾讯文档 MCP（需通过 mcporter 注册）

### 运行时依赖
- Node.js >= 18（微信搜索脚本）
- Python 3（IMA 上传脚本）
- npm 包：cheerio（微信搜索脚本依赖）
- jq（腾讯文档参数构建）

### 凭证要求
- IMA API：`~/.config/ima/client_id` + `~/.config/ima/api_key`
- 腾讯文档 MCP：mcporter 已注册 `tencent-docs` server（token 存于 `~/.mcporter/mcporter.json`）

---

## 安装后首次运行检查清单

1. 确认 `wechat-article-search` skill 已安装
2. 确认 `ima-skills` skill 已安装
3. 运行 `npm install` 安装 cheerio 依赖
4. 确认 IMA API 凭证已配置
5. 创建 IMA 知识库并记录 KB ID
6. 确认 mcporter 已注册 `tencent-docs` MCP server 且 token 有效（双平台发布所需）
7. 配置自动化任务（每周一 08:00）
8. 执行一次测试运行验证全流程（需验证 IMA 和腾讯文档双平台均同步成功）
