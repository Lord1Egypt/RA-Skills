# 数据模型参考

## 核心实体

### Project

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 项目名称 |
| type | string | 类型（都市/古风/悬疑/科幻等） |
| artStyle | string | 艺术风格 |
| videoRatio | string | 视频比例 |
| episodeCount | number | 计划集数 |
| chapters | number[] | 关联章节号 |
| styleReference | string | 风格样张路径 |
| versions | object | 文件版本追踪 |
| models | object | AI 模型配置 |
| characters | Character[] | 角色列表（含一致性参数） |
| scenes | Scene[] | 场景列表 |
| props | Prop[] | 道具列表 |

### Character

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 角色名 |
| description | string | 外貌/性格描述 |
| seed | number | 图像生成种子 |
| consistencyId | string | 一致性 ID（如模型支持） |
| voiceType | string | TTS 音色 |
| voiceEmotion | string | 默认情感 |
| filePath | string | 参考图路径 |

### Scene

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 场景名 |
| description | string | 环境描述 |
| filePath | string | 参考图路径 |

### Prop

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 道具名 |
| description | string | 外观描述 |
| filePath | string | 参考图路径 |

### EpisodeData (大纲)

| 字段 | 类型 | 说明 |
|------|------|------|
| episodeIndex | number | 集数 |
| title | string | 标题 |
| chapterRange | number[] | 关联章节 |
| coreConflict | string | 核心矛盾 |
| outline | string | 剧情主干 |
| openingHook | string | 开场镜头 |
| keyEvents | string[] | [起, 承, 转, 合] |
| emotionalCurve | string | 情绪曲线 |
| visualHighlights | string[] | 视觉重点 |
| endingHook | string | 结尾悬念 |
| classicQuotes | string[] | 经典台词 |
| scenes | AssetItem[] | 场景列表 |
| characters | AssetItem[] | 角色列表 |
| props | AssetItem[] | 道具列表 |

### AssetItem

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 名称 |
| description | string | 详细描述 |

## 版本追踪

```json
{
  "versions": {
    "storyline.md": {
      "version": 2,
      "timestamp": "2026-05-01T10:00:00"
    },
    "outline/outline-01.md": {
      "version": 3,
      "timestamp": "2026-05-01T11:00:00",
      "depends_on": "storyline.md"
    }
  }
}
```

## 关系图

```
Project
  ├── Storyline (1:1)
  ├── Outline (1:N) → Script (1:1) → Storyboard (1:1)
  ├── Characters (1:N)
  ├── Scenes (1:N)
  ├── Props (1:N)
  └── Videos (1:N)
```
