---
name: wos-paper-downloader
description: "Web of Science 文献搜索与下载助手。自动从 WOS 搜索文献、提取元数据，并协助批量下载 PDF。使用场景：需要批量获取学术文献时，特别是环境心理学、恢复性环境等研究方向。需要有效的 WOS 机构订阅。"
---

# wos-paper-downloader

自动从 Web of Science 搜索文献、提取元数据，并协助批量下载 PDF。

**⚠️ 重要说明：**
- 需要有效的 Web of Science 机构订阅
- PDF 下载需要个人账号登录（脚本会指导你完成）
- 请遵守机构的使用政策和版权规定

## 功能特点

1. **智能检索** - 根据关键词自动生成优化的 WOS 检索式
2. **元数据提取** - 导出标题、作者、期刊、DOI、摘要等信息
3. **批量下载** - 自动下载开放获取(OA)文献，协助获取订阅文献
4. **自动整理** - 按日期/主题自动分类存储

## 使用方法

### 快速开始

```bash
# 1. 运行主脚本
python scripts/wos_downloader.py

# 2. 按提示输入检索关键词
# 3. 脚本会生成检索结果和下载列表
```

### 命令行参数

```bash
# 基础检索
python scripts/wos_downloader.py --query "restorative environment health" --limit 50

# 高级检索（使用WOS检索式）
python scripts/wos_downloader.py --advanced --query 'TS=("attention restoration theory") AND TS=(health)' --limit 100

# 指定输出目录
python scripts/wos_downloader.py --query "green space mental health" --output ./papers/2024

# 只下载开放获取文献
python scripts/wos_downloader.py --query "nature exposure" --oa-only
```

## 工作流程

### 第一步：配置环境

1. 确保你有 Web of Science 访问权限
2. 安装依赖：
   ```bash
   pip install -r scripts/requirements.txt
   ```

### 第二步：执行检索

脚本会：
- 打开浏览器并导航到 Web of Science
- 根据你的关键词执行检索
- 导出检索结果（标题、作者、DOI等）

### 第三步：下载文献

- **开放获取文献**：自动通过 Unpaywall/API 下载
- **订阅文献**：生成下载清单，指导你手动批量下载

### 第四步：整理归档

自动按以下结构整理：
```
papers/
├── 2024-01-15_restorative-environment/
│   ├── metadata.csv          # 文献元数据
│   ├── download_list.txt     # 待下载清单
│   ├── oa_papers/            # 开放获取文献
│   │   ├── paper1.pdf
│   │   └── paper2.pdf
│   └── subscribed/           # 订阅文献（手动下载后放入）
```

## 检索式构建指南

### 环境心理学常用检索式

```
# 恢复性环境
TS=("attention restoration theory" OR "stress recovery theory" OR "restorative environment*") AND TS=(health OR well-being)

# 亲环境行为  
TS=("pro-environmental behavior" OR "sustainable behavior") AND TS=(attitude* OR motivation)

# 绿色空间与健康
TS=("green space" OR "greenspace" OR "urban nature") AND TS=(health OR "mental health" OR well-being)
```

### 检索技巧

- `TS=` - 主题检索（标题+摘要+关键词）
- `AU=` - 作者检索
- `SO=` - 期刊检索
- `PY=` - 出版年份
- `*` - 通配符（如 `restor*` 匹配 restore, restorative, restoration）

## 注意事项

1. **下载限制**：Web of Science 有每日下载限额，脚本会自动控制频率
2. **版权问题**：只下载你有权限访问的文献
3. **稳定性**：网络波动可能导致中断，脚本支持断点续传

## 故障排除

**问题：无法登录 Web of Science**
- 确认你通过机构网络或 VPN 访问
- 检查账号是否有效

**问题：下载速度慢**
- 使用 `--oa-only` 只下载开放获取文献
- 调整 `--delay` 参数控制请求间隔

**问题：PDF 下载失败**
- 部分文献可能没有 OA 版本
- 检查 `download_list.txt` 手动获取

## 参考资料

- [Web of Science 高级检索指南](references/wos_search_guide.md)
- [DOI 解析与开放获取检测](references/doi_resolver.md)

## 依赖

- Python 3.8+
- Selenium / Playwright（浏览器自动化）
- requests（HTTP 请求）
- pandas（数据处理）
