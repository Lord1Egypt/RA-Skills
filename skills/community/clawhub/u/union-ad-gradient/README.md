# union-ad-gradient

> UnionSkill渐变梦幻广告PPT。图像型工作流：内容分析→大纲确认→逐页生图→PPTX装配。适合创意设计、品牌营销、视觉展示。

## 视觉风格
**渐变梦幻** — 深色渐变+橙色标题+紫色强调

背景：深色渐变底，日落/海洋/极光/彩虹渐变，软光晕

适用：创意设计、品牌营销、视觉展示

## 工作流
遵循 Aoran PPT Skill 图像型工作流范式：

1. 收集输入（文档/对话/引用）
2. 分析内容，确认渐变风格方向
3. 规划大纲 → **用户确认**
4. 逐页生图（image_generate → 16:9全页）
5. PPTX装配（union_pptx_assembler.py → 品牌尾页+水印+元数据）
6. 打包交付（ZIP + 可选HTML）
7. QA检查

## 使用
任何支持 image_generate 工具的AI Agent均可使用本Skill。

### 准备工作
1. 确保Agent有图像生成能力（GPT Image 2 / DALL-E 3 / Stable Diffusion 等）
2. 安装 python-pptx：
```bash
pip install python-pptx
```

### 调用方式
用户说："用渐变风做一份关于XX的PPT，给我先看大纲"

Agent按 `SKILL.md` 工作流执行。

## 品牌信息
- 官网：www.unionskillai.com
- 商务邮箱：miscdd@163.com

### 商业合作
本项目为通用开源工具。我们专注离散制造/机加工领域，提供工业级AI报价系统、API调用、私有化部署服务。

官方网站：www.unionskillai.com
商务合作邮箱：miscdd@163.com

## 技术栈
- PPTX装配：python-pptx + union_pptx_assembler.py
- 图像生成：GPT Image 2 / DALL-E 3 / 或用户自选图像模型
- 品牌引擎：UnionSkill

## License
MIT
