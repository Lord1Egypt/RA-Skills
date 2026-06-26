---
name: rxnim
description: >
  RxnIM 化学反应图像解析技能。当用户需要：(1) 从化学反应图像提取 SMILES 结构，
  (2) 识别反应条件（试剂/溶剂/温度/产率），(3) 将反应图转化学结构数据时触发。
  基于 Chem. Sci. 2025 论文 "Towards Large-scale Chemical Reaction Image Parsing via a Multimodal Large Language Model"。
  支持 HuggingFace 在线 API（推荐）和本地 conda 部署两种调用路径。
---

# RxnIM - 化学反应图像多模态大模型

## 技能概述

RxnIM 是一个多模态大语言模型，专门从化学反应图像中提取结构化数据，无需人工标注。支持三种核心任务：

| 任务 | 描述 |
|------|------|
| **反应提取** | 从图像中提取反应物→产物的 SMILES 结构 |
| **条件 OCR** | 识别试剂、溶剂、温度、产率等反应条件 |
| **角色识别** | 判断各化学物种在反应中的角色（reactant/product/reagent/solvent） |

**模型性能**: 在 Pistachio（合成）和 ACS（真实）数据集上，soft-match F1 达到 **84%–92%**，显著优于先前方法。

---

## 触发判断

当用户表达以下意图时，激活本技能：

- "从这张图里提取反应"
- "把化学反应图像转成 SMILES"
- "识别这张反应图的条件"
- "化学反应图像 OCR"
- 上传/描述化学反应图片并要求分析
- "RxnIM"、"reaction image parsing"、"反应图像提取"

---

## 调用路径

### 路径一：HuggingFace 在线 API（推荐，无需本地部署）

```
POST https://CYF200127-RxnIM.hf.space/run/predict
Headers: Content-Type: application/json
Body: { "data": ["data:image/png;base64,<base64_image>"] }
```

**Python 调用示例：**

```python
import base64, requests, json

def parse_reaction_image(image_path: str, hf_space: str = "https://CYF200127-RxnIM.hf.space") -> dict:
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    resp = requests.post(
        f"{hf_space}/run/predict",
        json={"data": [f"data:image/png;base64,{b64}"]},
        timeout=120
    )
    return resp.json()

# 使用
result = parse_reaction_image("reaction.png")
print(result["data"])  # 完整文本输出
```

**输出字段说明：**

```json
{
  "data": "Reaction: 1\nReactants: CC(C)(C)OC(=O)N[C@@H]1C[C@H]2C(=O)O[C@H]2[C@@H]1Br\nConditions: Br2, Pyridine[reagent], DME/H2O[solvent], 0-5°C[temperature], 68%[yield]\nProducts: CC(C)(C)OC(=O)N[C@@H]1C[C@@H](CO)[C@@H](O)[C@@H]1Br\nFull Reaction: ... | ..."
}
```

### 路径二：本地 conda 部署

```bash
# 1. 克隆仓库
git clone https://github.com/CYF2000127/RxnIM
cd RxnIM

# 2. 创建环境
conda create -n rxnim python=3.10
conda activate rxnim

# 3. 安装依赖
pip install -r requirements.txt

# 4. 下载模型权重（~14GB）
# https://huggingface.co/datasets/CYF200127/RxnIM → RxnIM-7b.zip
# 解压到本地路径，修改 config/_base_/dataset/DEFAULT_TRAIN_DATASET.py 中的路径

# 5. 推理
sh eval.sh
```

> ⚠️ 本地部署需要约 16GB GPU 显存，推荐 Linux + CUDA 环境。

---

## 任务流程

### 标准流程：化学反应图像解析

```
用户上传/提供图像 → base64 编码 → 调用 HF API → 解析 JSON 输出 → 格式化呈现
```

1. **接收图像**：从用户上传、URL 或文件路径获取化学反应图像
2. **编码**：转换为 base64 字符串，构造 `data:image/png;base64,...` 格式
3. **请求**：POST 到 HuggingFace Space，timeout 设为 120s（大模型推理较慢）
4. **解析**：从 `response["data"]` 提取文本，手动分割各字段
5. **格式化**：以结构化 Markdown 表格呈现给用户
6. **校验（可选）**：将提取的 SMILES 传入 `pharmaclaw-chemistry-query` 技能验证有效性

---

## 输出格式规范

解析后，按以下格式组织结果：

```
✅ 反应解析成功

**Reaction: 1**
| 角色 | 内容 |
|------|------|
| Reactants（反应物） | `CC(C)(C)OC(=O)N[C@@H]1C[C@H]2C(=O)O[C@H]2[C@@H]1Br` |
| Conditions（条件） | Br2, Pyridine[reagent], DME/H2O[solvent], 0-5°C[temperature], 68%[yield] |
| Products（产物） | `CC(C)(C)OC(=O)N[C@@H]1C[C@@H](CO)[C@@H](O)[C@@H]1Br` |
| Full Reaction | `>>` 格式完整反应式 |

📝 完整输出:
{radio_output}
```

---

## 输入输出示例

### 示例 1：单步反应

**输入图像**: 含一个化学反应的 PNG/JPG

**API 输出（原始）:**
```
Reaction: 1
Reactants: CC(C)(C)OC(=O)N[C@H]1C=C[C@H](C(=O)O)C1
Conditions: Br2, Pyridine[reagent], DME/H2O[solvent], 0-5°C[temperature], 68%[yield]
Products: CC(C)(C)OC(=O)N[C@@H]1C[C@H]2C(=O)O[C@H]2[C@@H]1Br
Full Reaction: CC(C)(C)OC(=O)N[C@H]1C=C[C@H](C(=O)O)C1>>CC(C)(C)OC(=O)N[C@@H]1C[C@H]2C(=O)O[C@H]2[C@@H]1Br | Br2[reagent], Pyridine[reagent], DME/H2O[solvent], 0-5°C[temperature], 68%[yield]
```

### 示例 2：多步反应

RxnIM 支持从一张图中解析多步反应：

```
Reaction: 2
Reactants: CC(C)(C)OC(=O)N[C@@H]1C[C@H]2C(=O)O[C@H]2[C@@H]1Br
Conditions: LiBH4[reagent], THF/H2O[solvent], -5°C[temperature], 90%[yield]
Products: CC(C)(C)OC(=O)N[C@@H]1C[C@@H](CO)[C@@H](O)[C@@H]1Br

Reaction: 3
Reactants: CC(C)(C)OC(=O)N[C@@H]1C[C@@H](CO)[C@@H](O)[C@@H]1Br
Conditions: 48% aq. HBr[reagent], IPA[solvent], 55°C[temperature]
Products: Br.N[C@@H]1C[C@@H](CO)[C@@H](O)[C@@H]1Br
```

---

## 与其他技能的 Chaining

### → pharmaclaw-chemistry-query（推荐）

提取的 SMILES 可直接传给 `pharmaclaw-chemistry-query` 技能进行二次分析：

```
用户: 分析这个反应图像 → RxnIM 提取 SMILES → 传入 pharmaclaw-chemistry-query → 
  → 分子性质查询 + 2D 可视化 + 逆合成分析
```

触发词："分析产物性质"、"可视化这个反应"、"做逆合成规划"

### → wecom-doc / tencent-docs

将结构化结果写入企业微信文档或腾讯文档存档。

---

## 已知限制与注意事项

| 限制 | 说明 | 缓解方案 |
|------|------|---------|
| 图像质量依赖 | 低分辨率/模糊图像解析效果下降 | 建议上传 300 DPI 以上的清晰图 |
| SMILES 有效性 | 极少数情况下可能输出无效 SMILES | 使用 RDKit 验证，失败时提示用户 |
| API 延迟 | HuggingFace 免费版推理较慢 | 设置 timeout=120s，用户等待时显示进度 |
| 手写/扫描图像 | 效果弱于印刷版化学图像 | 建议使用印刷版或高清截图 |
| 显存要求 | 本地部署需要 ~16GB GPU | 优先推荐 HF 在线 API |

---

## 数据集与资源

| 资源 | 链接 |
|------|------|
| HuggingFace 在线 Demo | https://huggingface.co/spaces/CYF200127/RxnIM |
| 模型权重下载 | https://huggingface.co/datasets/CYF200127/RxnIM（RxnIM-7b.zip） |
| 合成数据集 | Pistachio（HuggingFace 同上） |
| 真实数据集 | ACS Publications（HuggingFace 同上） |
| 源代码 | https://github.com/CYF2000127/RxnIM |
| 相关工作 ChemEAGLE | https://github.com/CYF2000127/ChemEAGLE |

---

## 引用

```bibtex
@article{D5SC04173B,
  author = {Chen, Yufan and Leung, Ching Ting and Sun, Jianwei and
            Huang, Yong and Li, Linyan and Chen, Hao and Gao, Hanyu},
  title  = {Towards large-scale chemical reaction image parsing via a
            multimodal large language model},
  journal = {Chem. Sci.},
  year   = {2025},
  volume = {16},
  issue  = {45},
  pages  = {21464--21474},
  publisher = {The Royal Society of Chemistry},
  doi    = {10.1039/D5SC04173B},
  url    = {http://dx.doi.org/10.1039/D5SC04173B}
}
```

---

## 依赖项

| 类别 | 依赖 |
|------|------|
| 在线 API | requests, base64（标准库） |
| 本地部署 | torch, transformers, datasets, pillow, numpy, nltk, pandas, mmengine, tensorboard, einops, tqdm, matplotlib, accelerate, SentencePiece, gradio, fastapi, uvicorn, bitsandbytes |
| 验证（可选） | RDKit（通过 chaining 调用 pharmaclaw-chemistry-query） |
| 环境 | Python 3.10+, CUDA 11.8+（本地部署） |
