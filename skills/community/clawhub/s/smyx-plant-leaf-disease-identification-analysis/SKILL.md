---
name: "smyx-plant-leaf-disease-identification-analysis"
description: "AI-powered plant leaf disease identification from high-resolution leaf images. Detects disease lesion features (color, shape, distribution, surface deposits) such as white powdery patches (powdery mildew), rust-colored spore pustules (rust), brown necrotic spots (leaf spot), and outputs the most likely disease type with confidence score. Helps users quickly diagnose plant diseases and take timely measures. Scenarios: plant factories, greenhouses, home gardening, farm inspection. | 通过拍摄植物叶片的高清图像，利用AI视觉分析技术识别叶片上的病斑特征（颜色、形状、分布），检测是否有白色粉状物（白粉病）、锈色孢子堆（锈病）、褐色坏死斑（叶斑病）等典型症状，输出最可能的病害类型及置信度。帮助用户快速诊断植物病害，采取防治措施。应用场景：植物工厂、温室大棚、家庭盆栽、园艺养护。"
version: "1.0.2"
license: "MIT-0"
---

# Plant Leaf Disease Identification | 植物叶片病害特征识别

AI-powered plant leaf disease identification from high-resolution leaf images. Detects disease lesion features (color, shape, distribution, surface deposits) such as white powdery patches (powdery mildew), rust-colored spore pustules (rust), brown necrotic spots (leaf spot), and outputs the most likely disease type with confidence score. Helps users quickly diagnose plant diseases and take timely measures. Scenarios: plant factories, greenhouses, home gardening, farm inspection.

通过拍摄植物叶片的高清图像，利用AI视觉分析技术识别叶片上的病斑特征（颜色、形状、分布），检测是否有白色粉状物（白粉病）、锈色孢子堆（锈病）、褐色坏死斑（叶斑病）等典型症状，输出最可能的病害类型及置信度。帮助用户快速诊断植物病害，采取防治措施。应用场景：植物工厂、温室大棚、家庭盆栽、园艺养护。

## 🎯 AI 角色

**假设你是一个专业的植物病理学AI。你的任务是分析植物叶片的图像，识别叶片上的病斑特征（颜色、形状、分布、表面附着物），与常见病害特征库比对，输出最可能的病害类型及置信度。不要提供化学防治具体方案，仅输出病害识别结果。**

## 任务目标

- 本 Skill 用于：通过植物叶片高清图像进行病害特征识别，输出最可能的病害类型、置信度及通用防治方向建议
- 能力包含：叶片病斑检测、病斑特征提取（颜色/形状/分布/表面附着物）、常见病害比对（白粉病/锈病/叶斑病/霜霉病/炭疽病等）、置信度评分、通用防治方向建议
- 触发条件:
    1. **默认触发**：当用户提供植物叶片图像或视频需要分析时，默认触发本技能进行病害识别
    2. 当用户明确需要植物病害诊断时，提及植物病害、叶片发黄、白粉、锈斑、烂叶、植物诊断等关键词，并且上传了图像或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史植物病害报告、历史叶片诊断报告、植物病害报告清单、显示所有植物报告、查询植物诊断记录
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有植物病害报告"、"显示叶片诊断报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_plant_leaf_disease_identification_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行植物叶片病害识别前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：【最高优先级】检查技能所在目录的配置文件（优先）
        路径：scripts/config.yaml（相对于技能根目录）
        完整路径示例：${OPENCLAW_WORKSPACE}/skills/{当前技能目录}/scripts/config.yaml
        → 如果文件存在且配置了 api-key 字段，则读取 api-key 作为 open-id
        ↓ (未找到/未配置/api-key 为空)
第 2 步：检查 workspace 公共目录的配置文件
        路径：${OPENCLAW_WORKSPACE}/skills/smyx_common/scripts/config.yaml
        → 如果文件存在且配置了 api-key 字段，则读取 api-key 作为 open-id
        ↓ (未找到/未配置)
第 3 步：检查用户是否在消息中明确提供了 open-id
        ↓ (未提供)
第 4 步：❗ 必须暂停执行，明确提示用户提供用户名或手机号作为 open-id
```

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、userC113、user123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询历史报告记录），并询问是否继续

---

- 标准流程:
    1. **准备图像/视频输入**
        - 提供本地植物叶片高清图像/视频文件路径或网络 URL
        - 拍摄建议：
          - **近距离拍摄**（10-30cm），单片叶片占据画面主要区域
          - **光线充足**（自然光最佳），避免逆光、过曝、阴影遮挡病斑
          - **病斑清晰**：确保病斑区域对焦清晰、细节可辨
          - 建议同时拍摄正反面，正面可见病斑、反面可见孢子堆/菌丝
        - 支持图像（jpg/png）和视频（mp4/avi/mov）格式
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行病害识别**
        - 调用 `-m scripts.smyx_plant_leaf_disease_identification_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地植物叶片图像/视频文件路径
            - `--url`: 网络植物叶片图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 对象类型，植物场景默认 other
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示植物病害识别历史报告列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看识别结果**
        - 接收结构化的植物叶片病害识别报告
        - 包含：**病斑特征描述**（颜色、形状、大小、分布、表面附着物）、**最可能病害类型**（如白粉病/锈病/叶斑病）、**置信度评分**（0-100%）、**病情严重程度**（轻度/中度/重度）、**通用防治方向建议**（如"建议加强通风、隔离病叶"，不涉及具体化学方案）
        - **重要提示**：仅输出基于视觉的病害识别结果，**不提供具体化学防治方案**；专业用药请咨询植保专家

## 🌿 常见叶片病害特征对照

| 病害名称 | 典型特征 | 易发植物 |
|----------|----------|----------|
| ⚪ 白粉病 | 叶面/叶背覆盖白色粉状物 | 月季、葡萄、黄瓜、瓜类 |
| 🟠 锈病 | 叶背出现锈黄色/橙色孢子堆 | 玫瑰、小麦、菊花、豆科 |
| 🟤 叶斑病 | 褐色/黑色坏死斑，常带同心轮纹 | 番茄、辣椒、苹果、月季 |
| 🟡 霜霉病 | 叶面黄斑，叶背灰白色霉层 | 葡萄、黄瓜、十字花科 |
| ⚫ 炭疽病 | 暗褐色凹陷斑，中央有橙红色孢子盘 | 草莓、芒果、辣椒 |
| 🟢 病毒病 | 叶片花叶/卷曲/畸形，无明显斑点 | 番茄、黄瓜、烟草 |
| 💧 细菌性叶斑 | 水浸状斑点，边缘有黄晕 | 番茄、辣椒、白菜 |

## 🔍 病斑特征识别维度

| 维度 | 观察重点 |
|------|----------|
| 颜色 | 白/黄/橙/褐/黑/紫色等 |
| 形状 | 圆形/椭圆/不规则/多角形 |
| 边缘 | 清晰/模糊/有/无晕圈 |
| 分布 | 散生/聚集/沿叶脉/全叶 |
| 表面附着物 | 粉状/绒毛状/孢子堆/水浸状 |
| 病斑组合 | 是否同心轮纹、凹陷、穿孔 |

## 📊 病情严重程度分级

| 等级 | 病叶占比 | 处置建议 |
|------|----------|----------|
| 🟢 轻度 | <10% | 加强通风、摘除病叶、监测扩散 |
| 🟡 中度 | 10%-30% | 隔离病株、调整环境湿度、考虑生物防治 |
| 🟠 重度 | 30%-50% | 立即隔离、咨询植保专家、必要时使用药剂 |
| 🔴 严重 | >50% | 严重感染，建议销毁病株防止扩散 |

## 💡 通用防治方向参考

| 防治方向 | 适用场景 |
|----------|----------|
| 🌬️ 加强通风 | 白粉病、霜霉病等高湿度诱发病害 |
| ✂️ 摘除病叶 | 早期所有病害，减少病原基数 |
| 💧 调整浇水 | 避免叶面长期湿润，改为根部浇水 |
| ☀️ 增加光照 | 弱光环境下植株易感病 |
| 🛡️ 隔离病株 | 防止健康植株感染 |
| 🌱 选用抗病品种 | 长期解决方案 |
| 🔬 咨询植保专家 | 重度病害需专业指导 |

> ⚠️ 本技能仅提供**通用防治方向**，**不提供具体化学药剂方案**；专业用药需根据植物种类、病害类型、当地法规咨询植保专家。

## 资源索引

- 必要脚本：见 [scripts/smyx_plant_leaf_disease_identification_analysis.py](scripts/smyx_plant_leaf_disease_identification_analysis.py)(用途：调用 API 进行植物叶片病害识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持 jpg/png/mp4/avi/mov 格式，最大 10MB
- **拍摄要求**：近距离、光线充足、病斑清晰；模糊/逆光/距离过远的图像无法得出可靠结果
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **识别结果仅供病害诊断参考，不提供具体化学防治方案**；专业用药请咨询植保专家
- 部分病害症状相似（如细菌性与真菌性叶斑），AI 识别可能存在不确定性，建议结合植物种类与环境综合判断
- 同一叶片可能存在多种病害混合感染，需结合症状综合判定
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史识别报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"对象类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`植物叶片病害识别报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 对象类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 植物叶片病害识别报告-20260312172200001 | 植物 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地植物叶片图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_plant_leaf_disease_identification_analysis --input /path/to/leaf.jpg --open-id your-open-id

# 分析网络植物叶片图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_plant_leaf_disease_identification_analysis --url https://example.com/leaf.jpg --open-id your-open-id

# 显示历史识别报告/显示报告清单列表
python -m scripts.smyx_plant_leaf_disease_identification_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_plant_leaf_disease_identification_analysis --input leaf.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_plant_leaf_disease_identification_analysis --input leaf.jpg --open-id your-open-id --output result.json
```
