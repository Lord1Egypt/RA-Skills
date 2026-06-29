"""
PubMed 文献搜索 — NCBI E-Utilities 封装
支持命令行传入参数，方便 AI agent 调用

用法:
  python search_pubmed.py "CRISPR cancer"
  python search_pubmed.py "hopanoid" --max 10
  python search_pubmed.py "cancer AND immunotherapy" --db pmc
  python search_pubmed.py --pmid 41185614  (查看指定文献摘要)

输出: 纯文本格式（便于 agent 阅读）
"""
import sys
import io
import argparse
from Bio import Entrez

# Windows GBK 终端兼容
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def configure(email=None, api_key=None, tool=None):
    """配置 NCBI 连接参数"""
    if email:
        Entrez.email = email
    if api_key:
        Entrez.api_key = api_key
    if tool:
        Entrez.tool = tool


def search(db, query, max_results):
    """ESearch — 搜索数据库，返回 PMID 列表 + 总数"""
    handle = Entrez.esearch(db=db, term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"], int(record["Count"])


def fetch_summaries(db, id_list):
    """ESummary — 批量获取文献摘要"""
    if not id_list:
        return []
    handle = Entrez.esummary(db=db, id=",".join(id_list))
    summaries = Entrez.read(handle)
    handle.close()
    return summaries


def fetch_full(db, id_list, rettype="medline", retmode="xml"):
    """EFetch — 获取完整记录（含摘要文本）"""
    ids = ",".join(id_list)
    handle = Entrez.efetch(db=db, id=ids, rettype=rettype, retmode=retmode)
    records = Entrez.read(handle)
    handle.close()
    return records


# ============================================================
# 主程序
# ============================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PubMed 文献搜索 — NCBI E-Utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python search_pubmed.py "CRISPR cancer"              # 基础搜索
  python search_pubmed.py "hopanoid" --max 10           # 指定返回数量
  python search_pubmed.py "biomarker" --db pmc           # 搜 PMC 全文库
  python search_pubmed.py --pmid 41185614               # 按 PMID 查摘要
  python search_pubmed.py --pmid 41185614 --full        # 含摘要文本全文
        """,
    )
    parser.add_argument("query", nargs="?", default=None, help="搜索关键词（支持 Entrez 语法）")
    parser.add_argument("--max", dest="max_results", type=int, default=10,
                        help="最大返回条数 (默认 10)")
    parser.add_argument("--db", default="pubmed", help="目标数据库 (默认 pubmed)")
    parser.add_argument("--email", default=None,
                        help="联系邮箱 (NCBI 建议填写，超频时用于联系你)")
    parser.add_argument("--api-key", default=None, dest="api_key",
                        help="NCBI API Key (可选，提升速率)")
    parser.add_argument("--pmid", default=None, dest="pmid",
                        help="直接按 PMID 查看摘要 (跳过搜索)")
    parser.add_argument("--full", action="store_true",
                        help="输出包含摘要文本全文 (需搭配 --pmid)")

    args = parser.parse_args()

    # 检查参数
    if not args.query and not args.pmid:
        parser.print_help()
        print("\n[Error] 请提供搜索关键词或 --pmid 参数")
        sys.exit(1)

    configure(email=args.email, api_key=args.api_key)

    # ---- 按 PMID 查看 ----
    if args.pmid:
        pmids = [args.pmid]
        # 尝试逗号分隔的多个 PMID
        if "," in args.pmid:
            pmids = args.pmid.split(",")

        summaries = fetch_summaries(args.db, pmids)
        for i, doc in enumerate(summaries):
            print(f"[{i+1}] PMID: {pmids[i]}")
            print(f"    Title:  {doc['Title']}")
            print(f"    Author: {doc.get('FirstAuthorName', '?')} | {doc.get('LastAuthor', '?')}")
            print(f"    Source: {doc['Source']}")
            print(f"    Date:   {doc['PubDate']}")
            print(f"    DOI:    {doc.get('DOI', 'N/A')}")

            if args.full:
                try:
                    full = fetch_full(args.db, [pmids[i]])
                    art = full["PubmedArticle"][0]["MedlineCitation"]["Article"]
                    abstract_parts = art.get("Abstract", {}).get("AbstractText", [])
                    if abstract_parts:
                        # 可能是一段或多段
                        if isinstance(abstract_parts[0], str):
                            text = " ".join(abstract_parts)
                        else:
                            text = " ".join(str(p) for p in abstract_parts)
                        print(f"    Abstract: {text[:500]}{'...' if len(text)>500 else ''}")
                    else:
                        print("    Abstract: (none)")
                except Exception as e:
                    print(f"    Abstract: [fetch failed: {e}]")
            print()
        sys.exit()

    # ---- 搜索 ----
    print(f"\n{'='*60}")
    print(f"DB:    {args.db}")
    print(f"Query: {args.query}")
    print(f"Max:   {args.max_results}")
    print(f"{'='*60}")

    id_list, total = search(args.db, args.query, args.max_results)
    print(f"Hits: {total}  |  Showing: {len(id_list)}\n")

    if not id_list:
        print("[No results]")
        sys.exit()

    # ---- 摘要 ----
    print(f"{'='*60}")
    print(f"Results:")
    print(f"{'='*60}")

    summaries = fetch_summaries(args.db, id_list)
    for i, doc in enumerate(summaries):
        print(f"[{i+1}] PMID: {id_list[i]}")
        print(f"    Title:  {doc['Title']}")
        print(f"    Author: {doc.get('FirstAuthorName', '?')} | {doc.get('LastAuthor', '?')}")
        print(f"    Source: {doc['Source']}")
        print(f"    Date:   {doc['PubDate']}")
        print(f"    DOI:    {doc.get('DOI', 'N/A')}")
        print()

    print(f"[Done] {args.db} / {args.query}  |  {total} hits, showed {len(id_list)}")
