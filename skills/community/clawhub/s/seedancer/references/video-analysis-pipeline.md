> **Language**: This document is in Chinese only. For English overview, see [README.md](../README.md).
>
> **语言说明**: 本文档仅提供中文版本。英文概述请查看 [README.md](../README.md)。

---
# 视频分析管线协议 v1.0

> 借鉴 ShotFunClaw `shotfun-drama-localization-pipeline` 视频分析管线

---

## 核心概念

视频分析管线用于自动分析源视频，提取结构化信息（角色、场景、道具、对白、镜头等），为后续生成提供依据。

---

## 1. 分析流程

### 1.1 流程概览

```
源视频上传
  ↓
代理视频生成（480p，降低分析成本）
  ↓
视频分析模型调用（gemini-3.5-flash）
  ↓
结构化输出解析
  ↓
视频理解文档生成
```

### 1.2 详细步骤

#### 步骤1：生成代理视频

```bash
# 使用 ffmpeg 生成 480p 代理视频
ffmpeg -i source.mp4 -vf "scale=-1:480" -c:v libx264 -crf 23 proxy.mp4
```

**参数说明**：
- `-vf "scale=-1:480"`: 高度缩放到480p，宽度自动计算
- `-c:v libx264`: 使用H.264编码
- `-crf 23`: 质量控制（23为默认值，数值越小质量越高）

#### 步骤2：调用视频分析模型

```json
{
  "model": "gemini-3.5-flash",
  "input": {
    "video": "proxy.mp4",
    "prompt": "分析这个视频，提取以下信息：..."
  }
}
```

#### 步骤3：解析结构化输出

将模型输出解析为结构化JSON，包含：
- 角色列表
- 场景列表
- 道具列表
- 对白/旁白
- 镜头列表

#### 步骤4：生成视频理解文档

输出 `video_understanding.json`，包含完整的视频分析结果。

---

## 2. 分析单元切分

### 2.1 切分策略

长视频需要切分为多个分析单元，每个单元：
- **时长**: 45秒
- **重叠**: 1-2秒（确保连续性）

### 2.2 切分示例

```json
{
  "units": [
    {
      "unitId": "unit-001",
      "startTime": 0,
      "endTime": 45,
      "overlap": 0
    },
    {
      "unitId": "unit-002",
      "startTime": 44,
      "endTime": 89,
      "overlap": 1
    },
    {
      "unitId": "unit-003",
      "startTime": 88,
      "endTime": 133,
      "overlap": 1
    }
  ]
}
```

### 2.3 合并策略

分析完成后，需要合并多个单元的结果：
- 去重：相同角色/场景/道具只保留一次
- 连续性：确保时间线连续
- 冲突解决：如果同一时间点有矛盾信息，优先选择后面的单元

---

## 3. 结构化输出规范

### 3.1 输出Schema

```json
{
  "schemaVersion": "video_understanding.v2",
  "video": {
    "title": "视频标题",
    "duration": 180,
    "resolution": "1920x1080",
    "fps": 30
  },
  "characters": [
    {
      "id": "character-001",
      "name": "角色名",
      "description": "角色描述",
      "firstAppearance": 10,
      "lastAppearance": 170,
      "appearances": [
        {
          "startTime": 10,
          "endTime": 30,
          "action": "角色动作描述"
        }
      ]
    }
  ],
  "scenes": [
    {
      "id": "scene-001",
      "name": "场景名",
      "description": "场景描述",
      "startTime": 0,
      "endTime": 60
    }
  ],
  "props": [
    {
      "id": "prop-001",
      "name": "道具名",
      "description": "道具描述",
      "firstAppearance": 20,
      "lastAppearance": 150
    }
  ],
  "dialogues": [
    {
      "id": "dialogue-001",
      "characterId": "character-001",
      "text": "对白内容",
      "startTime": 15,
      "endTime": 20,
      "type": "dialogue"
    }
  ],
  "shots": [
    {
      "id": "shot-001",
      "startTime": 0,
      "endTime": 5,
      "description": "镜头描述",
      "cameraMovement": "推镜头",
      "shotType": "中景"
    }
  ]
}
```

### 3.2 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `video` | object | ✅ | 视频基本信息 |
| `characters` | array | ✅ | 角色列表 |
| `scenes` | array | ✅ | 场景列表 |
| `props` | array | ❌ | 道具列表 |
| `dialogues` | array | ❌ | 对白列表 |
| `shots` | array | ✅ | 镜头列表 |

---

## 4. 并发控制

### 4.1 并发策略

多个分析单元可以并发执行：
- **默认并发数**: 10
- **环境变量**: `SEEDANCER_ANALYSIS_CONCURRENCY`

### 4.2 并发示例

```javascript
const units = getAnalysisUnits(video);
const limiter = createLimiter(10);

const results = await Promise.all(
  units.map(unit => limiter(() => analyzeUnit(unit)))
);

const merged = mergeAnalysisResults(results);
```

---

## 5. 错误处理

### 5.1 常见错误

| 错误码 | 含义 | 处理方式 |
|--------|------|----------|
| `F-ANALYSIS-PROXY-FAILED` | 代理视频生成失败 | 检查源视频格式，重新生成 |
| `F-ANALYSIS-MODEL-FAILED` | 模型调用失败 | 重试或更换模型 |
| `F-ANALYSIS-PARSE-FAILED` | 结构化输出解析失败 | 检查模型输出格式 |
| `F-ANALYSIS-MERGE-FAILED` | 合并失败 | 检查单元时间线连续性 |

### 5.2 重试策略

```
失败 → 等待5秒 → 重试（最多3次）
3次失败 → 记录错误 → 跳过该单元 → 继续下一单元
```

---

## 6. 实施检查清单

### 6.1 代理视频生成
- [ ] 源视频格式检查
- [ ] ffmpeg命令正确
- [ ] 代理视频质量检查

### 6.2 模型调用
- [ ] 模型API可用
- [ ] 提示词正确
- [ ] 输出格式正确

### 6.3 结果合并
- [ ] 时间线连续
- [ ] 无重复项
- [ ] 无冲突信息

### 6.4 最终输出
- [ ] video_understanding.json 生成
- [ ] 所有必填字段存在
- [ ] 数据结构正确

---

## 7. 参考

- ShotFunClaw `shotfun-drama-localization-pipeline` 视频分析管线
- Seedancer `references/story-analysis.md`

---

**版本**: v1.0  
**创建时间**: 2026-09-10  
**来源**: ShotFunClaw 视频分析管线设计
