---
name: zcool-daily
description: 自动获取站酷（ZCOOL）首页热门设计作品（带链接、分类、亮点描述、趋势统计）
---

# 站酷每日热门作品推荐

## 功能说明

获取站酷（ZCOOL）首页的热门设计作品，输出格式：

- 标题带链接（可点击查看详情）
- 作品类型分类（AI绘画、插画、3D、动画、品牌设计等）
- 自动生成亮点描述
- 趋势统计（当日类型分布）

## 输出格式示例

详见 `references/output-example.md`

```bash
# 查看示例
cat references/output-example.md
```

## 亮点描述规则

- 针对热门作品标题有专门优化
- 根据关键词匹配自动生成
- 每个类型有默认描述作为兜底

## 使用方法

```bash
python3 scripts/zcool_daily.py --mode list
```

## 输出文件

作品列表保存至：`zcool_daily/zcool_{date}.txt`

## 依赖

- Python 3
- requests
- beautifulsoup4

安装：
```bash
pip install requests beautifulsoup4
```

## 支持的类型分类

AI绘画、插画、品牌设计、UI/UX、3D、动画、游戏、摄影、海报、手办、汽车/工业、电商、视频/MV