# 学术论文检索小助手 - 使用说明

## 功能概览

支持五大数据源检索：
- **OpenAlex**（推荐，全学科，无需 Key）
- **Semantic Scholar**（CS 领域，可选 Key）
- **Crossref**（补充元数据）
- **arXiv**（预印本 + PDF 下载）
- **PubMed**（生物医学方向）

---

## S2_API_KEY 配置（可选）

### 为什么需要？

Semantic Scholar API Key 为**可选配置**：
- **有 Key：** 速率更快，每秒可发多个请求
- **无 Key：** 受限 1 次/秒，但不影响 OpenAlex / Crossref / arXiv / PubMed 的使用

### 申请步骤

1. 访问 https://www.semanticscholar.org/product/api
2. 注册账号，申请 Free tier（完全免费）
3. 获取 Key 后，在 `~/.bashrc` 中加入：

```bash
export S2_API_KEY='你的S2_API_KEY'
```

4. 重启终端或 `source ~/.bashrc` 使生效

**安全提醒：不要将 Key 写入 skill 文件或任何代码中。**

---

## 常用场景

### 场景 1：论文文献综述检索（推荐 multi 模式）

```bash
python scripts/research.py multi "your research topic" -n 30 -f bibtex -o literature_review.bib
```

### 场景 2：追踪某领域最新论文

```bash
python scripts/research.py openalex "large language model" -n 20 --year 2024 --sort-by date
```

### 场景 3：找高引用论文

```bash
python scripts/research.py semantic "machine learning" -n 20 --min-citations 500
```

### 场景 4：下载 arXiv 论文 PDF

```bash
python scripts/research.py arxiv "diffusion model" -n 10 --download --output-dir ./papers/
```

### 场景 5：用 DOI 查元数据

```bash
python scripts/research.py crossref "10.1038/nature12373" -f json
```

---

## 多源对比

| 数据源 | 覆盖范围 | PDF | 特色 |
|--------|---------|-----|------|
| OpenAlex | 全学科 | 部分有 | 免费、无 Key、元数据全 |
| Semantic Scholar | CS 为主 | 部分有 | 引用数、Influential Citations |
| Crossref | 全学科 | 无 | 卷期页、期刊元数据 |
| arXiv | 预印本 | ✅ 全部 | PDF 直接下 |
| PubMed | 生物医学 | 部分有 | 医学主题词 |

---

## 安装依赖

```bash
pip install -r scripts/requirements.txt
```

依赖包：
- `requests` - HTTP 请求
- `semanticscholar` - S2 API
- `arxiv` - arXiv 检索
- `biopython` - PubMed 检索

---

## 与旧版 academic-research-hub 的区别

| 对比项 | 旧版 | 新版（松哥版） |
|--------|------|----------------|
| 数据源 | arXiv / PubMed / S3 | OpenAlex + S2 + Crossref + arXiv + PubMed |
| Multi 模式 | ❌ | ✅ 三步串联自动补全 |
| Crossref 补元数据 | ❌ | ✅ 补卷期页 |
| Key 配置说明 | ❌ | ✅ 清晰说明有无 Key 区别 |
| 中文界面 | ❌ | ✅ 全中文输出 |
| 作者 | anisafifi | 松哥 |
