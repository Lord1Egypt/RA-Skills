---
name: zdat-publish-skill
description: ZDAT全平台发文技能。定时+格式转换+多平台一键分发+发布日志。封装 zdat-mpg-multi-publish 引擎，支持头条号/微信公众号/知乎/小红书/微博/抖音。
---

# 📝 ZDAT 全平台发文技能

## 身份定位
ZDAT博士军团内容分发引擎。统一管理各平台发文格式、定时调度、发布日志追溯。

## 触发关键词
`发文`、`一键分发`、`定时发布`、`全平台发布`、`格式转换`、`发布日志`

## 依赖技能
- `zdat-mpg-multi-publish` — 头条/微信/知乎/小红书一键分发
- `cron` — 定时执行
- `xlsx` — 发布日志写入

## 配置文件
- `skill_config/zd_publish_rule.yaml` — 各平台格式+定时
- `skill_config/zd_keyword.yaml` — 发文话题关键词参考

## 执行流程

### 步骤1：内容适配（按平台转格式）
| 平台 | 转换动作 |
|:----|:--------|
| 微信公众号 | 长文1800~3000字，理论+落地案例，开篇摘要 |
| 知乎 | 问答体800~1200字，针对用户问题作答 |
| 小红书 | 300~500字短句，分段+少量emoji，务实干货 |
| 微博 | 100~120字短观点 |
| 抖音/视频号 | 口播脚本200~320字，痛点切入+解决方案 |

### 步骤2：去AI化处理
- 拆分长句
- 替换同质化表述
- 规避各平台原创检测

### 步骤3：调用发布引擎
```bash
# 头条号（全自动+二次确认）
python zd_auto_publish_v5.py --platform toutiao --title "标题" --content "正文"

# 微信公众号（保存草稿）
python zd_auto_publish_v5.py --platform weixin --title "标题" --content "正文"

# 小红书（全自动）
python zd_auto_publish_v5.py --platform xiaohongshu --title "标题" --content "正文"

# 知乎（半自动填表）
python zd_auto_publish_v5.py --platform zhihu --title "标题" --content "正文"
```

### 步骤4：发布日志回写
发布结果（成功/失败+原因）自动写入 `publish_log.xlsx`

## 定时调度
| 时间 | 平台 |
|:----|:----|
| 周二09:00 | 微信公众号 |
| 周五09:00 | 微信公众号 |
| 每日10:00 | 知乎 |
| 隔日15:00 | 小红书 |
| 每日12:00/18:00 | 微博（2条） |
| 每日19:00 | 抖音/视频号 |

## 示例命令
```bash
# 单平台发布
python active_skills/zdat-publish-skill/scripts/zd_publish_single.py --platform zhihu --title "..." --content "..."

# 多平台一键分发
python active_skills/zdat-publish-skill/scripts/zd_publish_all.py --article "文章路径"

# 查看发布日志
python active_skills/zdat-publish-skill/scripts/zd_publish_log.py
```
