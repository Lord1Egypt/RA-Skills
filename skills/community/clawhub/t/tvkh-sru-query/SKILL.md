---
name: "tvkh-sru-query"
description: "Query Khánh Hòa Provincial Library SRU catalog via CQL and output structured JSON records"
---

# SRU Library Query Skill

## Overview
Enable querying the Khánh Hòa Provincial Library SRU service via CQL (Common Query Language) to search for books, articles, and other resources at https://sru.thuvienkhanhhoa.gov.vn. The SRU endpoint (`/khanhhoa`) runs on top of the **Zebra** search and indexing engine, successfully modernizing and expanding upon the library's traditional **Z39.50** bibliographic protocol infrastructure.

## Installation
```bash
openclaw skills install @baolinhtv/tvkh-sru-query
```
*(Or via Git: `openclaw skills install https://github.com/baolinhtv/openclaw-skill-sru-query.git`)*

## Prerequisites
- Access to https://sru.thuvienkhanhhoa.gov.vn
- Basic understanding of CQL syntax

## Usage

### Primary Function: `sru_query.py` CLI
```bash
python3 sru_query.py "Văn hóa Chăm"
python3 sru_query.py "Khánh Hòa" --limit 20
python3 sru_query.py "Xứ Trầm Hương" --author "Quách Tấn"
```

#### Parameters
- `query`: search term or raw CQL query (required)
- `author`: optional, author name filter (`dc.creator`)
- `title`: optional, specific title keywords (`dc.title`)
- `limit`: optional, max records to return (default 20)

### Smart Newspaper Filter (Bộ lọc báo chí thông minh)
The Khanh Hoa Provincial Library catalog contains thousands of bound local newspaper issues that often overwhelm search results. This skill features a built-in smart filter:
1. It automatically fetches a large pool of records from the Zebra server (bypassing the server's default sorting limits).
2. It filters out any records whose storage locations consist entirely of `"Kho Báo"` (Newspaper Archive).
3. It returns a clean list of actual books, magazines, and documents up to the requested `--limit`.

### CQL Query Syntax Examples

#### 1. Search by Keyword (Broad Search)
By default, if you input a simple string, the script wraps it in quotes `""` to trigger a broad phrase search across the Zebra indexes:
```text
"Văn hóa Chăm"
"Lịch sử Khánh Hòa"
```

#### 2. Search by Specific Field
- By Author: `dc.creator="Quách Tấn"`
- By Title Phrase: `dc.title="Xứ Trầm Hương"`
- By Subject: `dc.subject="Văn hóa"`

#### 3. Combined / Advanced Queries
```text
"Văn hóa" AND dc.creator="Bố Xuân Hổ"
dc.title="Chăm" AND dc.subject="Kiến trúc"
```

### Direct SRU URL Examples (Working)
```text
[https://sru.thuvienkhanhhoa.gov.vn/khanhhoa?operation=searchRetrieve&version=1.1&query=%22V%C4%83n+h%C3%B3a+Ch%C4%83m%22&recordSchema=marcxml&maximumRecords=10](https://sru.thuvienkhanhhoa.gov.vn/khanhhoa?operation=searchRetrieve&version=1.1&query=%22V%C4%83n+h%C3%B3a+Ch%C4%83m%22&recordSchema=marcxml&maximumRecords=10)

[https://sru.thuvienkhanhhoa.gov.vn/khanhhoa?operation=searchRetrieve&version=1.1&query=dc.title%3D%22Kh%C3%A1nh+H%C3%B2a%22&recordSchema=marcxml&maximumRecords=10](https://sru.thuvienkhanhhoa.gov.vn/khanhhoa?operation=searchRetrieve&version=1.1&query=dc.title%3D%22Kh%C3%A1nh+H%C3%B2a%22&recordSchema=marcxml&maximumRecords=10)
```

## Output Data Structure (JSON)
The skill parses raw MARC21 XML into clean, AI-ready JSON objects:
```json
[
  {
    "id": "14350",
    "title": "Truyền thuyết về các tháp Chăm trên miền đất cực Nam Trung bộ",
    "author": "Bố, Xuân Hổ",
    "authors": [
      "Bố, Xuân Hổ"
    ],
    "publisher": "Văn hóa dân tộc",
    "year": "1995",
    "call_number": "305.899 TR527TH",
    "price": "35000đ",
    "location": "Kho mở / Kho Đọc ; Kho Lưu động",
    "locations": [
      "Kho mở / Kho Đọc",
      "Kho Lưu động"
    ],
    "summary": "Giới thiệu văn hóa Chăm qua các tháp cổ ở miền Nam Trung Bộ, tập trung vào kiến trúc và các truyền thuyết dân gian xoay quanh việc xây dựng tháp."
  }
]
```

## Implementation Details
- Uses CQL/SRU protocol standard (Z39.50) with YAZ/Zebra backend.
- Fetches MARC21 XML schema (`recordSchema=marcxml`).
- Robust metadata extraction:
  - Handles primary authors (`100`), co-authors/contributors (`700`), and statement of responsibility (`245$c`).
  - Supports modern RDA publishing statements (`264`) and traditional imprint (`260`).
  - Cleans ISBD punctuation and normalizes publication years.
  - Aggregates multiple shelf locations (`852`) and DDC call numbers (`082`).
- Retries with exponential backoff (3 attempts) on network/server hiccups.