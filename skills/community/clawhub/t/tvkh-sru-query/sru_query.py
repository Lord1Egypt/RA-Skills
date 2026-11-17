import sys
import time
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import json
import argparse


def clean_marc_text(text):
    """Xóa bỏ các dấu câu chuẩn ISBD còn sót lại ở hai đầu chuỗi"""
    if not text:
        return ""
    return text.strip().strip(" /:;,.")


def clean_year(year_text):
    """Trích xuất 4 chữ số năm từ các chuỗi như 'c1995.', '[2020]'"""
    if not year_text:
        return ""
    match = re.search(r'\b(19\d{2}|20\d{2})\b', year_text)
    return match.group(0) if match else clean_marc_text(year_text)


def search_sru(query, maximum_records=20, retries=3, backoff_factor=1.5):
    # Tăng mạnh mẻ lưới lên 150 để "đào" xuyên qua hàng trăm số báo rác
    fetch_limit = 150 
    
    base_url = "https://sru.thuvienkhanhhoa.gov.vn/khanhhoa"
    params = {
        "operation": "searchRetrieve",
        "version": "1.1",
        "query": query,
        "recordSchema": "marcxml",
        "maximumRecords": str(fetch_limit)
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw-SRU-Client/1.1'})
    
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
            return parse_marcxml(xml_data, maximum_records)
        except Exception as e:
            if attempt == retries:
                print(f"Lỗi kết nối SRU (Attempt {attempt}/{retries}): {e}", file=sys.stderr)
                return []
            time.sleep(backoff_factor ** attempt)


def parse_marcxml(xml_bytes, return_limit):
    results = []
    try:
        root = ET.fromstring(xml_bytes)
        namespaces = {
            'zs': 'http://www.loc.gov/zing/srw/',
            'marc': 'http://www.loc.gov/MARC21/slim'
        }
        
        # BỘ DÒ MÌN
        diagnostics = root.findall('.//zs:diagnostic', namespaces)
        if diagnostics:
            for diag in diagnostics:
                msg = diag.find('zs:message', namespaces)
                detail = diag.find('zs:details', namespaces)
                err_msg = msg.text if msg is not None else "Lỗi không xác định"
                err_detail = detail.text if detail is not None else ""
                print(f"[!] SRU Server Error: {err_msg} - {err_detail}", file=sys.stderr)
            return []
            
        records = root.findall('.//marc:record', namespaces)
        if not records:
            records = root.findall('.//{http://www.loc.gov/MARC21/slim}record')
            
        for record in records:
            # Chỉ trả về đúng số lượng user yêu cầu (mặc định 20 sách xịn)
            if len(results) >= return_limit:
                break
                
            item = {
                "id": "",
                "title": "",
                "author": "",
                "authors": [],
                "publisher": "",
                "year": "",
                "call_number": "",
                "price": "",
                "location": "",
                "locations": [],
                "summary": ""
            }
            
            f001 = record.find('.//marc:controlfield[@tag="001"]', namespaces)
            if f001 is not None and f001.text:
                item["id"] = f001.text.strip()
                
            authors_list = []
            f100 = record.find('.//marc:datafield[@tag="100"]/marc:subfield[@code="a"]', namespaces)
            if f100 is not None and f100.text:
                authors_list.append(clean_marc_text(f100.text))
                
            for f700 in record.findall('.//marc:datafield[@tag="700"]', namespaces):
                sub_a = f700.find('marc:subfield[@code="a"]', namespaces)
                if sub_a is not None and sub_a.text:
                    name = clean_marc_text(sub_a.text)
                    if name not in authors_list:
                        authors_list.append(name)
                        
            f245 = record.find('.//marc:datafield[@tag="245"]', namespaces)
            if f245 is not None:
                sub_a = f245.find('marc:subfield[@code="a"]', namespaces)
                sub_b = f245.find('marc:subfield[@code="b"]', namespaces)
                sub_c = f245.find('marc:subfield[@code="c"]', namespaces)
                
                title_parts = []
                if sub_a is not None and sub_a.text:
                    title_parts.append(clean_marc_text(sub_a.text))
                if sub_b is not None and sub_b.text:
                    title_parts.append(clean_marc_text(sub_b.text))
                item["title"] = " - ".join(title_parts) if len(title_parts) > 1 else "".join(title_parts)
                
                if not authors_list and sub_c is not None and sub_c.text:
                    authors_list.append(clean_marc_text(sub_c.text))
            
            item["authors"] = authors_list
            item["author"] = ", ".join(authors_list)
                
            f082 = record.find('.//marc:datafield[@tag="082"]', namespaces)
            if f082 is not None:
                sub_a = f082.find('marc:subfield[@code="a"]', namespaces)
                sub_b = f082.find('marc:subfield[@code="b"]', namespaces)
                ddc_parts = []
                if sub_a is not None and sub_a.text:
                    ddc_parts.append(clean_marc_text(sub_a.text))
                if sub_b is not None and sub_b.text:
                    ddc_parts.append(clean_marc_text(sub_b.text))
                item["call_number"] = " ".join(ddc_parts)

            f26x = record.find('.//marc:datafield[@tag="260"]', namespaces)
            if f26x is None:
                f26x = record.find('.//marc:datafield[@tag="264"]', namespaces)
                
            if f26x is not None:
                sub_b = f26x.find('marc:subfield[@code="b"]', namespaces)
                sub_c = f26x.find('marc:subfield[@code="c"]', namespaces)
                if sub_b is not None and sub_b.text:
                    item["publisher"] = clean_marc_text(sub_b.text)
                if sub_c is not None and sub_c.text:
                    item["year"] = clean_year(sub_c.text)
                    
            f020 = record.find('.//marc:datafield[@tag="020"]/marc:subfield[@code="c"]', namespaces)
            if f020 is not None and f020.text:
                item["price"] = clean_marc_text(f020.text)
                
            loc_list = []
            for f852 in record.findall('.//marc:datafield[@tag="852"]', namespaces):
                sub_b = f852.find('marc:subfield[@code="b"]', namespaces)
                sub_c = f852.find('marc:subfield[@code="c"]', namespaces)
                parts = []
                if sub_b is not None and sub_b.text:
                    parts.append(clean_marc_text(sub_b.text))
                if sub_c is not None and sub_c.text:
                    parts.append(clean_marc_text(sub_c.text))
                if parts:
                    loc_str = " / ".join(parts)
                    if loc_str not in loc_list:
                        loc_list.append(loc_str)
            item["locations"] = loc_list
            item["location"] = " ; ".join(loc_list)
            
            # --- BỘ LỌC BÁO CHÍ THÔNG MINH ---
            is_only_newspaper = True
            for loc in item["locations"]:
                if "Kho Báo" not in loc and "Kho báo" not in loc:
                    is_only_newspaper = False
                    break
            
            if len(item["locations"]) > 0 and is_only_newspaper:
                continue # Gạt bỏ báo, vòng lặp sang biểu ghi tiếp theo
            # ---------------------------------

            f520 = record.find('.//marc:datafield[@tag="520"]', namespaces)
            if f520 is not None:
                sub_a = f520.find('marc:subfield[@code="a"]', namespaces)
                if sub_a is not None and sub_a.text:
                    item["summary"] = clean_marc_text(sub_a.text)

            results.append(item)
    except Exception as e:
        print(f"Error parsing MARCXML: {e}", file=sys.stderr)
        
    return results


def main():
    parser = argparse.ArgumentParser(description="Query Khanh Hoa Provincial Library SRU catalog.")
    parser.add_argument("query", help="CQL query or search term")
    parser.add_argument("--author", help="Optional author name filter")
    parser.add_argument("--title", help="Optional title filter")
    parser.add_argument("--limit", type=int, default=20, help="Max records to return")
    
    args = parser.parse_args()
    raw_query = args.query.strip()
    
    # Cú pháp Keyword Search mặc định của CQL (Bọc ngoặc kép để tìm cụm từ trên toàn bộ các trường)
    if not any(token in raw_query for token in ["=", " AND ", " OR ", " all "]):
        cql_query = f'"{raw_query}"'
    else:
        cql_query = raw_query
        
    if args.author:
        cql_query += f' AND dc.creator="{args.author.strip()}"'
    if args.title:
        cql_query += f' AND dc.title="{args.title.strip()}"'
        
    records = search_sru(cql_query, args.limit)
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()