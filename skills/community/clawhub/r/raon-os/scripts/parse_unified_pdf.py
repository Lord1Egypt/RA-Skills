#!/usr/bin/env python3
"""통합공고 PDF → JSONL 파서"""

import fitz
import json
import re
from pathlib import Path

PDF_PATH = Path(os.environ.get("RAON_PDF_PATH", str(Path(__file__).parent.parent / "drafts" / "gov" / "2026-통합공고.pdf")))
OUT_PATH = Path(__file__).resolve().parent.parent / "eval_data" / "unified_announcement_2026.jsonl"


def extract_all_text(pdf_path: Path) -> str:
    doc = fitz.open(str(pdf_path))
    texts = []
    for page in doc:
        texts.append(page.get_text())
    return "\n".join(texts)


def extract_tables(pdf_path: Path) -> list[dict]:
    """Extract program entries from PDF tables."""
    doc = fitz.open(str(pdf_path))
    programs = []
    
    # Strategy: extract tables page by page using PyMuPDF table extraction
    for page_num in range(len(doc)):
        page = doc[page_num]
        tables = page.find_tables()
        for table in tables:
            data = table.extract()
            if not data:
                continue
            # Find header row
            header_idx = -1
            for i, row in enumerate(data):
                row_text = " ".join(str(c) for c in row if c)
                if "사업명" in row_text and "사업개요" in row_text:
                    header_idx = i
                    break
            
            start = header_idx + 1 if header_idx >= 0 else 0
            # If no header found and this doesn't look like program data, skip
            if header_idx < 0:
                # Check if rows look like program entries (have numbers and Korean text)
                if not any(row[0] and str(row[0]).strip().isdigit() for row in data if row and row[0]):
                    continue
            
            for row in data[start:]:
                if not row or len(row) < 5:
                    continue
                cells = [str(c).strip() if c else "" for c in row]
                
                # Skip empty or header rows
                if not any(cells):
                    continue
                if "사업명" in cells[0] or "연번" in " ".join(cells[:2]):
                    continue
                
                # Try to parse based on column count
                prog = {}
                if len(cells) >= 8:
                    # Standard: 연번, 사업명, 사업개요, 지원내용, 지원대상, 예산, 공고일, 소관부처, 주관기관, 비고
                    idx = 0
                    # Skip 연번 if it's a number
                    if cells[0].replace('.', '').strip().isdigit():
                        idx = 1
                    prog["program"] = cells[idx].replace("ㆍ", "").strip()
                    prog["description"] = cells[idx+1] if idx+1 < len(cells) else ""
                    prog["support_content"] = cells[idx+2] if idx+2 < len(cells) else ""
                    prog["target"] = cells[idx+3] if idx+3 < len(cells) else ""
                    prog["budget"] = cells[idx+4] if idx+4 < len(cells) else ""
                    prog["announcement_date"] = cells[idx+5] if idx+5 < len(cells) else ""
                    prog["ministry"] = cells[idx+6] if idx+6 < len(cells) else ""
                    prog["agency"] = cells[idx+7] if idx+7 < len(cells) else ""
                
                if prog.get("program") and len(prog["program"]) > 1:
                    programs.append(prog)
    
    return programs


def fallback_text_parse(pdf_path: Path) -> list[dict]:
    """Fallback: parse from raw text using regex patterns."""
    doc = fitz.open(str(pdf_path))
    programs = []
    
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"
    
    # Pattern: look for numbered entries with ㆍ prefix for program names
    # Split by numbered entries
    pattern = re.compile(
        r'(\d+)\s*\n?\s*ㆍ([^\n]+)',
        re.MULTILINE
    )
    
    matches = list(pattern.finditer(full_text))
    
    for i, match in enumerate(matches):
        num = match.group(1).strip()
        name = match.group(2).strip()
        
        # Get text until next match
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else start + 2000
        block = full_text[start:end].strip()
        
        prog = {
            "program": name,
            "description": "",
            "support_content": "",
            "target": "",
            "budget": "",
            "announcement_date": "",
            "ministry": "",
            "agency": "",
        }
        
        # Try to extract budget (억원)
        budget_match = re.search(r'([\d,]+)\s*\n?\s*\d{2,4}[.\s년]', block)
        if budget_match:
            prog["budget"] = budget_match.group(1).strip() + "억원"
        
        # Extract ministry
        ministry_patterns = [
            r'(중소벤처기업부|과학기술정보통신부|산업통상자원부|농림축산식품부|문화체육관광부|'
            r'국토교통부|환경부|기후에너지환경부|보건복지부|교육부|고용노동부|'
            r'해양수산부|국방부|행정안전부|여성가족부|외교부|통일부|법무부|'
            r'기획재정부|특허청|관세청|방위사업청|산림청|기상청|소방청|경찰청|'
            r'방송통신위원회|공정거래위원회|금융위원회|원자력안전위원회|'
            r'국가보훈부|식품의약품안전처)'
        ]
        for mp in ministry_patterns:
            m = re.search(mp, block)
            if m:
                prog["ministry"] = m.group(1)
                break
        
        # Extract announcement date
        date_match = re.search(r"(\d{2,4})[.년]\s*(\d{1,2})월", block)
        if date_match:
            prog["announcement_date"] = f"{date_match.group(1)}.{date_match.group(2)}월"
        
        # Use first ~200 chars as description
        desc_text = block[:300].replace("\n", " ").strip()
        prog["description"] = desc_text
        
        if name and len(name) > 1:
            programs.append(prog)
    
    return programs


def main():
    print("📄 통합공고 PDF 파싱 시작...")
    
    # Try table extraction first
    programs = extract_tables(PDF_PATH)
    print(f"  테이블 추출: {len(programs)}건")
    
    # If table extraction got few results, try text parsing
    if len(programs) < 100:
        print("  테이블 추출 부족, 텍스트 파싱으로 보완...")
        text_programs = fallback_text_parse(PDF_PATH)
        print(f"  텍스트 파싱: {len(text_programs)}건")
        
        # Merge: use text_programs if significantly more
        existing_names = {p["program"] for p in programs}
        for tp in text_programs:
            if tp["program"] not in existing_names:
                programs.append(tp)
                existing_names.add(tp["program"])
        print(f"  병합 후: {len(programs)}건")
    
    # Write JSONL
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w") as f:
        for prog in programs:
            entry = {
                "type": "gov_program",
                "source": "2026-통합공고",
                "program": prog["program"],
                "description": prog.get("description", ""),
                "support_content": prog.get("support_content", ""),
                "target": prog.get("target", ""),
                "budget": prog.get("budget", ""),
                "announcement_date": prog.get("announcement_date", ""),
                "ministry": prog.get("ministry", ""),
                "agency": prog.get("agency", ""),
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    print(f"✅ 저장 완료: {OUT_PATH} ({len(programs)}건)")


if __name__ == "__main__":
    main()
