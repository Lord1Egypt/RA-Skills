# Stock Analysis Skill - 股票投资分析 v1.4.1

## Description
对上市公司进行系统性的投资价值分析，包括基本面、技术面、估值、同业对比。支持 A 股、港股、美股。

**新增功能：** 分析后自动生成可下载的 HTML/PDF 报告

## Location
/app/skills/stock-analysis/

## Triggers
- "分析 XX 股票/公司"
- "XX 值得投资吗"  
- "给 XX 估值/目标价"
- "对比 XX 和 XX"
- "生成 PDF 报告"

## Scripts

| 脚本 | 功能 |
|------|------|
| analyze.sh | 综合分析主入口 |
| analyze-with-pdf.sh | **分析 + PDF 生成一体化** 🔴 |
| generate-pdf-report.sh | **PDF 报告生成 + 下载链接** 🔴 |
| fetch-price.sh | 实时价格获取 |
| technical-analysis.sh | 技术分析 |
| ...其他脚本 | |

## 🔴 PDF 报告下载功能

### 使用方式
```bash
cd /app/skills/stock-analysis/scripts
./analyze-with-pdf.sh 300433 蓝思科技
```

### 输出结果
- 自动生成 HTML 报告
- 启动 HTTP 服务器 (端口 8888)
- **提供直接下载链接**
- 用户点击链接即可在浏览器中查看并另存为 PDF

### 下载链接格式
```
http://<服务器IP>:8888/<公司名>_<股票代码>.html
```

### 用户操作
1. 点击提供的下载链接
2. 在浏览器中打开报告
3. 按 **Ctrl+P** 选择 **"另存为 PDF"**
4. 或右键链接选择 **"另存为"**

## Workflow

### Phase 1: 数据获取
1. 自动获取实时行情
2. 获取财务数据
3. 获取技术面数据

### Phase 2: 分析处理
4. 财务比率计算
5. 估值分析
6. 同业对比
7. 生成优选提示

### Phase 3: 报告生成
8. **生成 HTML 报告**
9. **启动 HTTP 服务器**
10. **提供下载链接**
11. **用户直接点击下载**

## Output Format

### 完整报告（HTML 格式）
- 路径：`/app/skills/stock-analysis/reports/`
- **直接可访问的下载链接**
- 浏览器友好，支持打印为 PDF

## Configuration
在 TOOLS.md 中配置：
```markdown
### Stock Analysis

- PDF 生成：启用
- HTTP 端口：8888
- 报告目录：/app/skills/stock-analysis/reports/
```

## Version History
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.4.1 | 2026-03-16 | **PDF 报告 + 直接下载链接** 🔴 |
| v1.4.0 | 2026-03-16 | PDF 生成基础功能 |
| v1.3.0 | 2026-03-16 | 同业优选提示 |
| v1.2.0 | 2026-03-16 | 技术分析功能 |
| v1.1.0 | 2026-03-16 | 数据获取功能 |
| v1.0.0 | 2026-03-16 | 初始版本 |

## Dependencies
- curl (必需)
- jq (推荐)
- bc (必需)
- python3 (必需，用于 HTTP 服务器)
- bash 4.0+

## Limitations
⚠️ 部分 API 可能有访问限制
⚠️ 不构成投资建议
⚠️ 数据可能存在延迟