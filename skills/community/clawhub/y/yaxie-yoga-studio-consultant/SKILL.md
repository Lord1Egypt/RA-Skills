---
name: yaxie-knowledge-base
description: 亚协体育瑜伽馆经营知识库读取技能。当需要查询瑜伽馆经营相关知识时使用，包括：销售话术、活动策划、团队管理、股权合伙、抖音运营、私教成交、会员运营、卡项设计等亚协知识库内容。支持关键词搜索、文件内容读取、知识点总结。触发场景：(1)用户询问瑜伽馆经营问题 (2)需要调用亚协知识库内容回答 (3)查询馆主关心的经营痛点解决方案
---

# 亚协体育瑜伽馆经营知识库

## 知识库信息
- **space_id**: 7547251789502922755
- **文件总数**: 97个
- **格式支持**: docx(50+), pdf(47), xls(1)
- **内容分类**: 销售培训/活动策划/抖音直播/股权合伙/店长管理/卡项设计/法律合同

## 核心脚本

### scripts/wiki_search.js - 搜索文件
```bash
node scripts/wiki_search.js <关键词>
```
搜索知识库中包含关键词的文件，返回文件列表（名称+obj_token）

### scripts/wiki_read.js - 读取文件内容
```bash
node scripts/wiki_read.js <obj_token> [输出文件]
```
根据obj_token下载并读取文件内容，提取文字返回

### scripts/wiki_list.js - 列出所有文件
```bash
node scripts/wiki_list.js
```
返回知识库完整文件列表（97个）

## 快速使用流程

1. **用户提问** → 识别关键词
2. **搜索文件** → `node scripts/wiki_search.js <关键词>`
3. **获取obj_token** → 从搜索结果中找到匹配文件
4. **读取内容** → `node scripts/wiki_read.js <obj_token>`
5. **总结回答** → 结合知识库内容回答用户

## 常用文件参考

| 分类 | 文件名 | obj_token |
|------|--------|-----------|
| 销售培训 | 打造瑜伽馆百万销售团队.docx | W6kkbVuX6okeVfxjdGcckS88n2c |
| 体测销售 | 高效打造私教业绩100%增长--高成交体测＆实操.docx | GyiIbQIRioRXB9x908Vcb5RZnyf |
| 抖音运营 | 伽人荟高阶课-抖音同城流量全面破局.docx | T2Q1bNdVroy0kexIWSIciu0XnMs |
| 流量运营 | 瑜伽馆全域流量破局-抖音同城.docx | 待查询 |
| 活动策划 | 亚协体育2025年开门红方案细节.docx | 待查询 |
| 股权合伙 | 瑜伽馆股东合伙合同.docx | 待查询 |
| 销售话术 | 亚协体育电话邀约话术.pdf | FV5qb5yIsoV6XNxU8e3cnpw8nxg |

## 权限配置

飞书应用凭证（在TOOLS.md中查找）：
- App ID: cli_a93b38f075b89cc4
- App Secret: CRSq1ZHlMM0QE488w9ph1fX0gG2eDXox

## 注意事项

- docx文件：直接解析word/document.xml提取文字
- pdf文件：用PyPDF2提取文字
- 图片型文档（如某些抖音课件）：需用OCR识别图片文字
- 文件名匹配：搜索时忽略.docx/.pdf扩展名
