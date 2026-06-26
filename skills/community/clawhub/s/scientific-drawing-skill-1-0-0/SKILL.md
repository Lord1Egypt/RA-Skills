---
name: scientific-drawing
description: 基于 AutoFigure-Edit 的科研级科学插图生成与编辑系统，能够从长篇方法描述自动生成完全可编辑的矢量图（SVG），支持参考图风格迁移和浏览器内交互式编辑
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["python3"], "env": ["GEMINI_API_KEY"], "config": ["skills.entries.scientific-drawing.enabled"] },
        "primaryEnv": "GEMINI_API_KEY",
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "packages": ["flask", "flask-cors", "svgwrite", "svgpathtools", "torch", "torchvision", "opencv-python", "pillow"],
              "label": "安装 Python 依赖",
            },
          ],
      },
  }
---

# 科学绘图技能

基于 AutoFigure-Edit 的科研级科学插图生成与编辑系统，能够从长篇方法描述自动生成完全可编辑的矢量图（SVG），支持参考图风格迁移和浏览器内交互式编辑。

## 核心特性

### 🎯 从像素到矢量的跨越
- **可编辑 SVG 输出**: 不再生成静态PNG图片，而是完全可编辑的SVG文件
- **结构化组件**: 每个图标、模块、连接线都是独立可编辑对象
- **矢量精度**: 无限缩放不失真，完美适配学术出版要求

### 🎨 参考图引导的风格迁移
- **智能风格学习**: 上传一张你喜欢的风格图，AI自动学习配色、字体、图标风格
- **跨论文风格统一**: 保持实验室或期刊的视觉一致性
- **无需复杂Prompt**: 摆脱反复调试提示词的困扰

### 🖥️ 内置交互式编辑器
- **实时编辑画布**: 生成后立即进入可视化编辑界面
- **拖拽式操作**: 调整布局、修改标注、替换图标
- **所见即所得**: 所有修改实时预览，支持撤销/重做

### 🔧 五阶段生成流程
1. **风格条件生图**: 基于文本和参考图生成初始栅格图像
2. **分割与结构索引**: 利用SAM3技术识别视觉组件并构建结构骨架
3. **资产提取**: 提取透明背景的视觉资产
4. **SVG模板生成与精炼**: 生成结构化的SVG布局模板
5. **资产注入**: 将视觉资产注入模板，形成完全可编辑的SVG

### 🧠 推理式渲染范式
- **概念锚定**: 从长篇方法描述提取核心实体和关系
- **评审-精炼闭环**: AI Designer与AI Critic多轮迭代优化
- **美学渲染与"擦除-修正"**: OCR识别模糊文字并用清晰矢量文字重新覆盖

## 先决条件

### 系统要求
- Python 3.10+
- Git
- 至少8GB RAM
- 支持CUDA的GPU（可选，可加速处理）

### API密钥需求
- **Google Gemini API密钥** (推荐) 或 **OpenRouter API密钥**
- 可选的 **Bianxie API密钥**
- **Hugging Face Token** (用于SAM3模型下载)

## 安装步骤

### 1. 自动安装（推荐）
```bash
# 在OpenClaw环境中，只需激活技能即可自动安装
# 技能会检查并安装所有依赖
```

### 2. 手动安装
```bash
# 克隆AutoFigure-Edit仓库
git clone https://github.com/ResearAI/AutoFigure-Edit.git

# 进入技能目录
cd /home/davidzhao/.openclaw/workspace/skills/scientific-drawing-skill

# 安装Python依赖
pip install -r requirements.txt

# 安装额外依赖
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install transformers datasets accelerate
pip install opencv-python pillow scikit-image
pip install lxml svgwrite svgpathtools
pip install flask flask-cors
```

### 3. 环境配置
```bash
# 复制环境配置文件
cp .env.example .env

# 编辑.env文件，添加你的API密钥
# GEMINI_API_KEY=your_gemini_api_key_here
# OPENROUTER_API_KEY=your_openrouter_api_key_here
# HF_TOKEN=your_huggingface_token_here
```

## 使用方法

### 基础生成：从文本到可编辑SVG
```bash
# 方法1：使用技能工具
scientific_drawing_generate --text "论文方法描述文本" --output_dir ./output

# 方法2：直接调用Python脚本
python autofigure2.py --method_file paper_method.txt --output_dir ./output --api_key $GEMINI_API_KEY
```

### 风格迁移：应用参考图风格
```bash
# 上传参考图并生成风格化插图
scientific_drawing_style_transfer \
  --text "方法描述" \
  --reference_image style_reference.png \
  --output_dir ./styled_output
```

### 交互式编辑：浏览器内编辑SVG
```bash
# 启动本地编辑服务器
scientific_drawing_edit_server --port 8080

# 在浏览器中打开 http://localhost:8080
# 上传生成的SVG文件进行可视化编辑
```

### 批量处理：多篇论文插图生成
```bash
# 处理目录中的所有文本文件
scientific_drawing_batch \
  --input_dir ./papers \
  --output_dir ./figures \
  --style_reference ./lab_style.png
```

## 工具函数

### `scientific_drawing_generate`
从文本生成可编辑的科学插图SVG。

**参数**:
- `--text`: 论文方法描述文本（可直接提供或通过文件）
- `--method_file`: 包含方法描述的文本文件路径
- `--output_dir`: 输出目录路径
- `--api_provider`: API提供商 (gemini, openrouter, bianxie)
- `--api_key`: API密钥（如未在.env中设置）
- `--placeholder_mode`: 占位符模式 (none, box, label)
- `--sam_prompt`: SAM3检测提示词，逗号分隔 (如 "icon,diagram,arrow")
- `--style_reference`: 风格参考图路径（可选）

**示例**:
```bash
scientific_drawing_generate \
  --text "Our method consists of three modules: feature extraction, attention fusion, and classification. The feature extractor uses ResNet-50..." \
  --output_dir ./figure_output \
  --placeholder_mode label \
  --sam_prompt "icon,module,arrow,text"
```

### `scientific_drawing_style_transfer`
基于参考图进行风格迁移。

**参数**:
- `--text`: 方法描述文本
- `--reference_image`: 风格参考图路径
- `--output_dir`: 输出目录
- `--style_strength`: 风格迁移强度 (0.0-1.0)
- `--preserve_content`: 是否保持内容结构 (true/false)

**示例**:
```bash
scientific_drawing_style_transfer \
  --method_file paper.txt \
  --reference_image nature_style.png \
  --output_dir ./nature_style_figures \
  --style_strength 0.7
```

### `scientific_drawing_edit_server`
启动交互式SVG编辑服务器。

**参数**:
- `--port`: 服务器端口 (默认: 8080)
- `--host`: 绑定主机 (默认: 0.0.0.0)
- `--data_dir`: SVG文件存储目录

**示例**:
```bash
scientific_drawing_edit_server --port 8080
# 访问 http://localhost:8080 使用编辑器
```

### `scientific_drawing_batch`
批量处理多篇论文。

**参数**:
- `--input_dir`: 包含文本文件的输入目录
- `--output_dir`: 输出目录
- `--style_reference`: 统一的风格参考图（可选）
- `--threads`: 并行处理线程数

## 配置文件

技能使用以下配置文件：

### `config.yaml`
```yaml
# API配置
api:
  default_provider: "gemini"
  gemini:
    model: "gemini-2.0-flash-exp"
    temperature: 0.7
  openrouter:
    model: "openai/gpt-4o"
    temperature: 0.7

# 生成参数
generation:
  placeholder_mode: "label"
  sam_prompt: "icon,diagram,arrow,chart,module"
  merge_threshold: 0.9
  optimize_iterations: 2

# 风格迁移
style_transfer:
  default_strength: 0.8
  content_preservation: true

# 编辑器设置
editor:
  port: 8080
  allow_upload: true
  max_file_size: 50MB
```

### 环境变量 (.env)
```
# API密钥
GEMINI_API_KEY=your_gemini_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
BIANXIE_API_KEY=your_bianxie_api_key_here
HF_TOKEN=your_huggingface_token_here

# 模型路径
SAM3_MODEL_PATH=./models/sam3
RMBG2_MODEL_PATH=./models/rmbg2

# 缓存设置
CACHE_DIR=./cache
MAX_CACHE_SIZE=10GB
```

## 输出文件结构

每次生成会创建以下文件：

```
output_dir/
├── figure.png              # 初始生成的栅格图
├── samed.png              # SAM3分割结果
├── boxlib.json            # 检测框坐标和标签
├── template.svg           # SVG模板
├── optimized_template.svg # 优化后的模板
├── final.svg              # 最终可编辑SVG
├── final.png              # 最终渲染图
└── icons/                 # 提取的图标资产
    ├── icon_AF01_nobg.png
    ├── icon_AF02_nobg.png
    └── ...
```

## 高级功能

### 自定义图标库
```bash
# 使用自定义图标替换默认生成
scientific_drawing_generate \
  --text "方法描述" \
  --custom_icons ./my_icons/ \
  --icon_mapping ./mapping.json
```

### 多模态输入支持
```bash
# 结合文本和草图生成
scientific_drawing_multimodal \
  --text "方法描述" \
  --sketch ./sketch.png \
  --output_dir ./output
```

### 学术出版优化
```bash
# 生成符合期刊要求的插图
scientific_drawing_publish \
  --input_svg ./final.svg \
  --journal "Nature" \
  --output_dir ./nature_ready
```

## 故障排除

### 常见问题

1. **API密钥错误**
   ```
   Error: Invalid API key
   ```
   **解决方案**: 检查.env文件中的API密钥，或通过--api_key参数提供

2. **内存不足**
   ```
   CUDA out of memory
   ```
   **解决方案**: 使用--no_cuda参数切换到CPU模式，或减小图片尺寸

3. **SAM3检测不准确**
   ```
   No icons detected
   ```
   **解决方案**: 调整--sam_prompt参数，尝试更具体的提示词

4. **SVG生成失败**
   ```
   Failed to generate SVG
   ```
   **解决方案**: 检查网络连接，尝试减少--optimize_iterations次数

### 调试模式
```bash
# 启用详细日志
export SCIENTIFIC_DRAWING_DEBUG=1
scientific_drawing_generate --text "..." --output_dir ./debug

# 查看完整日志
tail -f ./debug/generation.log
```

## 性能优化

### GPU加速
```bash
# 启用CUDA加速（如有NVIDIA GPU）
export CUDA_VISIBLE_DEVICES=0
scientific_drawing_generate --use_cuda ...
```

### 缓存利用
```bash
# 启用结果缓存，加速重复生成
scientific_drawing_generate --enable_cache ...
```

### 并行处理
```bash
# 批量处理时使用多线程
scientific_drawing_batch --threads 4 ...
```

## 集成示例

### 与OpenClaw工作流集成
```python
# 在Python脚本中使用
from scientific_drawing_skill import generate_scientific_figure

result = generate_scientific_figure(
    method_text="...",
    output_dir="./figures",
    style_reference="./lab_style.png"
)
print(f"生成成功: {result['svg_path']}")
```

### 作为研究流水线的一部分
```bash
# 从arXiv论文自动生成插图
arxiv_paper_to_figures \
  --arxiv_id "2603.06674" \
  --output_dir ./paper_figures \
  --style_reference ./journal_style.png
```

## 更新与维护

### 检查更新
```bash
# 更新技能到最新版本
clawhub update scientific-drawing-skill
```

### 重新安装依赖
```bash
# 重新安装所有Python依赖
cd /home/davidzhao/.openclaw/workspace/skills/scientific-drawing-skill
pip install -r requirements.txt --upgrade
```

### 清除缓存
```bash
# 清除生成的缓存文件
scientific_drawing_clean_cache --all
```

## 许可证与引用

### 许可证
本技能基于MIT许可证开源。

### 引用
如果您在研究中使用了本技能，请引用以下论文：

```bibtex
@article{lin2026autofigureedit,
  title={AutoFigure-Edit: Generating Editable Scientific Illustration},
  author={Lin, Zhen and Xie, Qiujie and Zhu, Minjun and Li, Shichen and Sun, Qiyao and Gu, Enhao and Ding, Yiran and Sun, Ke and Guo, Fang and Lu, Panzhong and Ning, Zhiyuan and Weng, Yixuan and Zhang, Yue},
  journal={arXiv preprint arXiv:2603.06674},
  year={2026}
}
```

### 致谢
- 基于 [AutoFigure-Edit](https://github.com/ResearAI/AutoFigure-Edit) 项目
- 使用 Meta 的 [SAM3](https://github.com/facebookresearch/segment-anything-3) 进行图像分割
- 使用 Google 的 [Gemini](https://ai.google.dev/) 进行多模态生成

## 支持与反馈

### 问题报告
如在技能使用中遇到问题，请：
1. 检查 [故障排除](#故障排除) 部分
2. 查看 [GitHub Issues](https://github.com/ResearAI/AutoFigure-Edit/issues)
3. 提交新的Issue，附上详细错误信息和日志

### 功能建议
欢迎提出新功能建议或改进意见：
- 通过GitHub Issues提交
- 或在OpenClaw社区讨论

### 贡献代码
欢迎提交Pull Request改进本技能：
1. Fork本技能仓库
2. 创建特性分支
3. 提交更改
4. 创建Pull Request

## 📊 用户反馈收集

为了持续改进本技能，我们非常重视您的使用体验反馈。请通过以下方式提供反馈：

### 1. 功能使用调查
请回答以下问题帮助我们改进：
1. 您使用本技能的主要场景是什么？（论文写作、研究演示、教学材料等）
2. 生成结果的质量如何？（1-5分，5分最佳）
3. 安装和配置过程是否顺利？
4. 您最常使用哪些功能？（SVG生成、风格迁移、交互式编辑等）
5. 您希望添加哪些新功能？

### 2. 问题报告模板
报告问题时请提供以下信息：
```
- OpenClaw版本: 
- 技能版本: 1.0.0
- 操作系统: 
- Python版本: 
- API提供商: 
- 错误信息: 
- 复现步骤: 
- 期望结果: 
- 实际结果: 
- 相关截图/日志: 
```

### 3. 反馈提交渠道
- **GitHub Issues**: https://github.com/ResearAI/AutoFigure-Edit/issues
- **OpenClaw社区**: https://discord.com/invite/clawd
- **直接反馈**: 通过ClawHub技能页面的评论功能

### 4. 使用统计（匿名）
技能会匿名收集以下使用数据以改进性能：
- 功能使用频率（生成、编辑、批量处理等）
- 平均处理时间
- 常见错误类型
- 系统配置信息（CPU/GPU、内存等）

**隐私说明**: 所有数据均为匿名收集，不会包含个人身份信息或具体内容数据。

---

**让科学插图生成变得简单而强大！** 🚀

*技能版本: 1.0.0 | 最后更新: 2026-04-07*