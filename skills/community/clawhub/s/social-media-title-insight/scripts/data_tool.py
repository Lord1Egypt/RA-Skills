#!/usr/bin/env python3
"""
社媒标题数据工具 v4
新增 verify（定量验证）和 report（HTML生成）命令，
让LLM只做"发现特征"，其余全由脚本完成。
"""

import argparse
import re
import os
import sys
import json
import html as html_lib
from datetime import datetime
from io import StringIO

try:
    import pandas as pd
except ImportError:
    sys.exit("ERROR: pandas not installed. Run: pip install pandas --break-system-packages")


def _cwd_path(filename):
    return os.path.join(os.getcwd(), filename)


def _marker_path():
    return _cwd_path(".social-media-title-insight-latest-run")


def _create_run_dir(base_dir=None):
    base = os.path.abspath(base_dir) if base_dir else _cwd_path("runs")
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = os.path.join(base, ts)
    os.makedirs(run_dir, exist_ok=True)
    return run_dir


def _write_latest_run_dir(run_dir):
    with open(_marker_path(), "w", encoding="utf-8") as f:
        f.write(os.path.abspath(run_dir))


def _read_latest_run_dir():
    marker = _marker_path()
    if not os.path.exists(marker):
        return None
    try:
        with open(marker, "r", encoding="utf-8") as f:
            run_dir = f.read().strip()
        if run_dir:
            return run_dir
    except Exception:
        return None
    return None


def _resolve_run_dir(args, create=False, prefer_new=False):
    if hasattr(args, "run_dir") and args.run_dir:
        run_dir = os.path.abspath(args.run_dir)
        if create:
            os.makedirs(run_dir, exist_ok=True)
        return run_dir
    if prefer_new:
        return _create_run_dir()
    latest = _read_latest_run_dir()
    if latest:
        if create:
            os.makedirs(latest, exist_ok=True)
        return latest
    if create:
        return _create_run_dir()
    return None


def _parse_number(value):
    s = str(value).strip().lower().replace(",", "")
    if s in {"", "nan", "none", "null", "-", "--"}:
        return None
    is_percent = s.endswith("%")
    if is_percent:
        s = s[:-1].strip()

    multiplier = 1.0
    if s.endswith("w") or s.endswith("万"):
        multiplier = 10000.0
        s = s[:-1].strip()
    elif s.endswith("k") or s.endswith("千"):
        multiplier = 1000.0
        s = s[:-1].strip()

    try:
        num = float(s) * multiplier
    except Exception:
        return None

    return num


def _to_numeric_series(series):
    return series.map(_parse_number).astype(float)


def _looks_like_ratio(raw_series, numeric_series):
    valid = numeric_series.dropna()
    if len(valid) == 0:
        return False
    text = raw_series.astype(str)
    has_percent_mark = text.str.contains("%", regex=False).mean() >= 0.3
    within_100 = valid.between(0, 100).mean() >= 0.9
    median_small = valid.median() <= 100
    return has_percent_mark or (within_100 and median_small)


def _infer_text_col(df):
    best_col = None
    best_score = -10**9
    for col in df.columns:
        s = df[col]
        s_text = s.astype(str)
        non_null = s.notna().mean()
        avg_len = s_text.str.len().mean() if len(s_text) > 0 else 0
        uniq_ratio = s_text.nunique(dropna=True) / max(1, s.notna().sum())
        num_ratio = _to_numeric_series(s).notna().mean()
        score = (non_null * 2.0) + min(avg_len / 20.0, 2.0) + uniq_ratio - (num_ratio * 2.5)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def _infer_numeric_cols(df):
    candidates = []
    for col in df.columns:
        numeric = _to_numeric_series(df[col])
        valid_ratio = numeric.notna().mean()
        if valid_ratio < 0.5:
            continue
        spread = numeric.dropna().std()
        spread = float(spread) if spread == spread else 0.0
        candidates.append({
            "col": col,
            "numeric": numeric,
            "valid_ratio": float(valid_ratio),
            "spread": spread,
            "is_ratio_like": _looks_like_ratio(df[col], numeric),
        })
    return candidates


def load_pasted_text(text):
    body = (text or "").strip()
    if not body:
        raise ValueError("粘贴内容为空")

    # 1) JSON
    try:
        data = json.loads(body)
        if isinstance(data, dict) and "result" in data:
            data = data["result"]
        if isinstance(data, list) and len(data) > 0:
            return pd.DataFrame(data)
    except Exception:
        pass

    # 2) 表格文本：优先 TSV，再 CSV，再管道
    for sep in ["\t", ",", "|"]:
        try:
            df = pd.read_csv(StringIO(body), sep=sep)
            if len(df) > 0 and len(df.columns) >= 1:
                return df
        except Exception:
            continue

    # 3) 单列文本：每行一个标题
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    if lines:
        return pd.DataFrame({"title": lines})

    raise ValueError("无法解析粘贴内容，请确认为JSON/CSV/TSV或逐行文本")


# ============================================================
# 数据加载（统一）
# ============================================================

def find_column(columns, candidates, fallback_idx=None):
    for c in candidates:
        for col in columns:
            if c in str(col).lower().strip():
                return col
    if fallback_idx is not None and fallback_idx < len(columns):
        return columns[fallback_idx]
    return None

def map_columns(df, title_col=None, engagement_col=None, ratio_col=None):
    cols = list(df.columns)
    tcol = title_col or find_column(cols, ['标题','title','内容','content','笔记标题','帖子','text','headline'], 0)
    ecol = engagement_col or find_column(cols, ['互动量','engagement','互动','likes','点赞','赞','总互动','total','hot','热度'], 1)
    rcol = ratio_col or find_column(cols, ['转赞比','share_ratio','转赞','ratio','转发比','分享率','rate'])

    numeric_candidates = _infer_numeric_cols(df)
    if not tcol:
        tcol = _infer_text_col(df)
    if not ecol:
        non_ratio_candidates = [c for c in numeric_candidates if not c["is_ratio_like"]]
        if non_ratio_candidates:
            ecol = sorted(non_ratio_candidates, key=lambda x: (x["valid_ratio"], x["spread"]), reverse=True)[0]["col"]
        elif numeric_candidates:
            ecol = sorted(numeric_candidates, key=lambda x: (x["valid_ratio"], x["spread"]), reverse=True)[0]["col"]
    if not rcol:
        ratio_candidates = [c for c in numeric_candidates if c["is_ratio_like"] and c["col"] != ecol]
        if ratio_candidates:
            rcol = sorted(ratio_candidates, key=lambda x: (x["valid_ratio"], x["spread"]), reverse=True)[0]["col"]

    result = pd.DataFrame()
    result['title'] = df[tcol].astype(str) if tcol else df.iloc[:,0].astype(str)
    if ecol and ecol in df.columns:
        result['engagement'] = _to_numeric_series(df[ecol])
    elif len(cols) > 1:
        result['engagement'] = _to_numeric_series(df.iloc[:,1])
    else:
        result['engagement'] = pd.Series([None] * len(df), dtype=float)

    if rcol and rcol in df.columns:
        result['ratio'] = _to_numeric_series(df[rcol])
    elif len(cols) >= 3 and rcol is None:
        try:
            vals = _to_numeric_series(df.iloc[:,2])
            if vals.notna().sum() > len(df)*0.5:
                result['ratio'] = vals
        except: pass
    # 保留其他列
    for c in cols:
        mapped = [tcol, ecol, rcol]
        if c not in mapped and c not in result.columns:
            result[c] = df[c]
    return result

def load_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.json': return _load_json(filepath)
    if ext in ['.xlsx','.xls','.xlsm']:
        try: import openpyxl
        except: sys.exit("ERROR: openpyxl not installed")
        return pd.read_excel(filepath)
    if ext == '.tsv': return _try_csv(filepath, '\t')
    if ext == '.csv': return _try_csv(filepath, ',')
    for loader in [_load_json, lambda f: _try_csv(f,','), lambda f: _try_csv(f,'\t')]:
        try:
            df = loader(filepath)
            if len(df)>0: return df
        except: continue
    raise ValueError(f"Cannot parse: {filepath}")

def _load_json(filepath):
    for enc in ['utf-8','gbk','utf-8-sig']:
        try:
            with open(filepath,'r',encoding=enc) as f: data=json.load(f)
            break
        except: continue
    else: raise ValueError("Cannot read JSON")
    if isinstance(data, dict) and 'result' in data: data = data['result']
    if isinstance(data, list) and len(data)>0:
        for item in data:
            for k,v in list(item.items()):
                if isinstance(v, str) and v.endswith('%'):
                    try: item[k] = float(v.replace('%',''))
                    except: pass
        return pd.DataFrame(data)
    raise ValueError("JSON format not recognized")

def _try_csv(filepath, sep=','):
    for enc in ['utf-8','gbk','gb18030','utf-8-sig','latin1']:
        try:
            df = pd.read_csv(filepath, sep=sep, encoding=enc)
            if len(df.columns)>=2 and len(df)>0: return df
        except: continue
    raise ValueError("Cannot parse CSV/TSV")

def fetch_api(accounts, size=100, cookie=None, tenant_id="t221"):
    import urllib.request, urllib.error
    url = f"https://vms-service.tezign.com/datacenter/ai-insight/public/account-data?size={size}"
    body = json.dumps(accounts).encode('utf-8')
    headers = {"Content-Type":"application/json","x-tenant-id":tenant_id}
    if cookie: headers["Cookie"] = cookie
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e: sys.exit(f"ERROR: API请求失败: {e}")
    if str(data.get("code"))!="0": sys.exit(f"ERROR: {data.get('message','unknown')}")
    results = data.get("result",[])
    if not results: sys.exit("ERROR: API返回空数据")
    rows = []
    for item in results:
        rate_str = str(item.get("rate","0%")).replace("%","").strip()
        try: rate_val = float(rate_str)
        except: rate_val = 0.0
        rows.append({"title":str(item.get("title","")),"engagement":int(item.get("hot",0)),"ratio":rate_val,
                      "account":str(item.get("account","")),"author":str(item.get("author",""))})
    return pd.DataFrame(rows)

def get_dataframe(args):
    if hasattr(args,'input') and args.input:
        df = load_file(args.input)
        return map_columns(df, getattr(args,'title_col',None), getattr(args,'engagement_col',None), getattr(args,'ratio_col',None))
    elif hasattr(args, 'paste') and args.paste:
        df = load_pasted_text(args.paste)
        return map_columns(df, getattr(args,'title_col',None), getattr(args,'engagement_col',None), getattr(args,'ratio_col',None))
    elif hasattr(args, 'stdin') and args.stdin:
        pasted = sys.stdin.read()
        df = load_pasted_text(pasted)
        return map_columns(df, getattr(args,'title_col',None), getattr(args,'engagement_col',None), getattr(args,'ratio_col',None))
    elif hasattr(args,'accounts') and args.accounts:
        accounts = [a.strip() for a in args.accounts.split(',')]
        return fetch_api(accounts, getattr(args,'size',100), getattr(args,'cookie',None), getattr(args,'tenant_id','tx_t1'))
    sys.exit("ERROR: 需要 --input / --paste / --stdin 或 --accounts")

def _resolve_col(df, col_ref):
    if col_ref is None: return None
    if col_ref in df.columns: return col_ref
    try:
        idx=int(col_ref)
        if 0<=idx<len(df.columns): return df.columns[idx]
    except: pass
    for c in df.columns:
        if col_ref.lower() in str(c).lower(): return c
    return None

def _fmt(val):
    if isinstance(val, float):
        return f"{val:.4f}" if abs(val)<10 else f"{val:.1f}"
    return str(val)


def _json_safe(obj):
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_safe(v) for v in obj]
    if hasattr(obj, 'item'):
        return obj.item()
    return obj


# ============================================================
# cmd: preview
# ============================================================

def cmd_preview(args):
    df = get_dataframe(args)
    n = args.rows or 8
    print(f"=== 数据概览 ===")
    print(f"总行数: {len(df)}")
    print(f"总列数: {len(df.columns)}")
    print(f"\n=== 列信息 ===")
    for i, col in enumerate(df.columns):
        dtype = str(df[col].dtype)
        non_null = df[col].notna().sum()
        if df[col].dtype in ['int64','float64']:
            print(f"  [{i}] \"{col}\" | {dtype} | 非空:{non_null} | 范围:{df[col].min():.2f}~{df[col].max():.2f} | 均值:{df[col].mean():.2f}")
        else:
            avg_len = df[col].astype(str).str.len().mean()
            samples = df[col].dropna().head(2).tolist()
            print(f"  [{i}] \"{col}\" | {dtype} | 非空:{non_null} | 平均长度:{avg_len:.1f} | 示例:{samples}")
    print(f"\n=== 前 {n} 行 ===")
    print(df.head(n).to_string(index=False))
    # 缓存
    run_dir = _resolve_run_dir(args, create=True, prefer_new=True)
    _write_latest_run_dir(run_dir)
    cache = os.path.join(run_dir, "_data_cache.csv")
    os.makedirs(os.path.dirname(cache) or ".", exist_ok=True)
    df.to_csv(cache, index=False, encoding='utf-8-sig')
    print(f"\n[本次运行目录: {run_dir}]")
    print(f"\n[已缓存至 {cache}]")


# ============================================================
# cmd: sort
# ============================================================

def cmd_sort(args):
    df = get_dataframe(args)
    col = _resolve_col(df, args.col)
    if not col: sys.exit(f"ERROR: 列 '{args.col}' 不存在。可用列: {list(df.columns)}")
    title_col = _resolve_col(df, args.title_col) if args.title_col else None
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=[col])
    n = min(args.n or 50, len(df)//2)
    if n<1: n=1
    sorted_df = df.sort_values(col, ascending=False)
    top_n = sorted_df.head(n)
    bottom_n = sorted_df.tail(n)
    show_cols = [title_col, col] if title_col else list(df.columns)
    print(f"=== 排序列: \"{col}\" | 总量:{len(df)} | 全局均值:{df[col].mean():.2f} | 中位数:{df[col].median():.2f} ===")
    print(f"Top{n}均值: {top_n[col].mean():.2f} | Bottom{n}均值: {bottom_n[col].mean():.2f}\n")
    print(f"=== TOP {n} ===")
    for idx, (_, row) in enumerate(top_n.iterrows(), 1):
        print(f"[{idx}] " + " | ".join(_fmt(row[c]) for c in show_cols if c))
    print(f"\n=== BOTTOM {n} ===")
    for idx, (_, row) in enumerate(bottom_n.iterrows(), 1):
        print(f"[{idx}] " + " | ".join(_fmt(row[c]) for c in show_cols if c))


# ============================================================
# cmd: verify - 定量验证LLM发现的特征
# ============================================================

def _verify_features_dataframe(df, features, min_hit=2, min_diff=15):
    has_ratio = 'ratio' in df.columns and df['ratio'].notna().sum() > 0
    results = []
    all_titles = df['title'].tolist()

    for feat in features:
        label = feat.get('label', '')
        keywords = feat.get('match_keywords', [])
        match_indices = feat.get('match_titles', None)

        if match_indices:
            hits = pd.Series([False] * len(df), index=df.index)
            for idx in match_indices:
                if 0 <= idx < len(df):
                    hits.iloc[idx] = True
        else:
            hits = pd.Series([False] * len(df), index=df.index)
            for i, title in enumerate(all_titles):
                tl = title.lower()
                if any(kw.lower() in tl for kw in keywords):
                    hits.iloc[i] = True

        yes_df = df[hits]
        no_df = df[~hits]

        if len(yes_df) < min_hit:
            continue

        r = {
            'label': label,
            'description': feat.get('description', ''),
            'yes_count': int(len(yes_df)),
            'no_count': int(len(no_df)),
            'yes_titles': yes_df['title'].head(3).tolist(),
        }

        avg_eng_yes = float(yes_df['engagement'].mean())
        avg_eng_no = float(no_df['engagement'].mean()) if len(no_df) > 0 else 0
        eng_diff = ((avg_eng_yes - avg_eng_no) / avg_eng_no * 100) if avg_eng_no > 0 else 0
        r['avg_eng_yes'] = round(avg_eng_yes, 1)
        r['avg_eng_no'] = round(avg_eng_no, 1)
        r['eng_diff_pct'] = round(eng_diff, 1)
        r['eng_significant'] = bool(abs(eng_diff) >= min_diff)

        if has_ratio:
            avg_rat_yes = float(yes_df['ratio'].mean())
            avg_rat_no = float(no_df['ratio'].mean()) if len(no_df) > 0 else 0
            rat_diff = ((avg_rat_yes - avg_rat_no) / avg_rat_no * 100) if avg_rat_no > 0 else 0
            r['avg_rat_yes'] = round(avg_rat_yes, 2)
            r['avg_rat_no'] = round(avg_rat_no, 2)
            r['rat_diff_pct'] = round(rat_diff, 1)
            r['rat_significant'] = bool(abs(rat_diff) >= min_diff)
        else:
            r['rat_significant'] = False

        r['any_significant'] = r['eng_significant'] or r['rat_significant']
        results.append(r)

    results.sort(key=lambda x: abs(x['eng_diff_pct']), reverse=True)
    output = {
        'total_items': int(len(df)),
        'has_ratio': has_ratio,
        'global_avg_eng': round(float(df['engagement'].mean()), 1),
        'global_med_eng': round(float(df['engagement'].median()), 1),
        'features': results,
        'significant_count': sum(1 for r in results if r['any_significant']),
    }
    if has_ratio:
        output['global_avg_rat'] = round(float(df['ratio'].mean()), 2)
    return output


def _extract_title_tokens(text):
    raw = str(text)
    lower = raw.lower()
    zh_tokens = re.findall(r'[\u4e00-\u9fff]{2,6}', raw)
    en_tokens = re.findall(r'[a-z][a-z0-9_-]{2,}', lower)
    stop_tokens = {'我们', '你们', '他们', '这个', '那个', '真的', '可以', '一下', '就是', 'today', 'with'}
    merged = zh_tokens + en_tokens
    return [t for t in merged if t not in stop_tokens]


def _auto_build_features(df, n=30, max_features=12):
    if 'engagement' not in df.columns:
        return []
    sorted_df = df.dropna(subset=['engagement']).sort_values('engagement', ascending=False)
    if len(sorted_df) == 0:
        return []
    n = max(10, min(n, len(sorted_df) // 2 if len(sorted_df) > 20 else len(sorted_df)))
    top_df = sorted_df.head(n)
    bottom_df = sorted_df.tail(n)

    top_hits = {}
    bottom_hits = {}

    for title in top_df['title'].tolist():
        for tok in set(_extract_title_tokens(title)):
            top_hits[tok] = top_hits.get(tok, 0) + 1
    for title in bottom_df['title'].tolist():
        for tok in set(_extract_title_tokens(title)):
            bottom_hits[tok] = bottom_hits.get(tok, 0) + 1

    scored = []
    for tok, top_cnt in top_hits.items():
        if top_cnt < 2:
            continue
        bottom_cnt = bottom_hits.get(tok, 0)
        lift = (top_cnt / max(1, len(top_df))) - (bottom_cnt / max(1, len(bottom_df)))
        if lift <= 0.12:
            continue
        scored.append((tok, top_cnt, bottom_cnt, lift))

    scored.sort(key=lambda x: (x[3], x[1]), reverse=True)
    features = []
    for tok, top_cnt, bottom_cnt, lift in scored[:max_features]:
        features.append({
            "label": f"关键词:{tok[:6]}",
            "description": f"标题包含“{tok}”，Top命中{top_cnt}次，Bottom命中{bottom_cnt}次",
            "match_keywords": [tok],
        })

    # 兜底：若token特征不足，补充结构性规则特征
    if len(features) < 4:
        features.extend([
            {"label": "问句结构", "description": "标题包含问号", "match_keywords": ["?", "？"]},
            {"label": "数字信息", "description": "标题包含数字", "match_keywords": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]},
            {"label": "感叹语气", "description": "标题包含感叹符号", "match_keywords": ["!", "！"]},
            {"label": "方法导向", "description": "标题偏方法论表述", "match_keywords": ["如何", "怎么", "教程", "攻略", "技巧"]},
        ])
        uniq = []
        seen = set()
        for f in features:
            k = tuple(f.get("match_keywords", []))
            if k in seen:
                continue
            seen.add(k)
            uniq.append(f)
        features = uniq[:max_features]

    return features


def cmd_verify(args):
    """
    接收LLM发现的特征（JSON文件），对每个特征在全量数据中做定量验证。
    特征JSON格式：
    [
      {
        "label": "实用指南型",
        "description": "包含具体的使用方法、选购指导、穿搭教程等实用信息",
        "match_keywords": ["如何","怎么选","指南","攻略","教程","法则","怎么"],
        "match_titles": [可选，直接指定标题索引]
      },
      ...
    ]
    """
    df = get_dataframe(args)
    features_path = args.features
    with open(features_path, 'r', encoding='utf-8') as f:
        features = json.load(f)

    min_hit = args.min_hit or 2
    min_diff = args.min_diff or 15
    output = _verify_features_dataframe(df, features, min_hit=min_hit, min_diff=min_diff)
    has_ratio = output.get("has_ratio", False)
    results = output.get("features", [])

    output = _json_safe(output)

    out_path = args.output
    if not out_path:
        run_dir = _resolve_run_dir(args, create=True, prefer_new=False)
        _write_latest_run_dir(run_dir)
        out_path = os.path.join(run_dir, "_verify_result.json")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ 验证完成: {len(results)} 个特征通过最低命中数要求，{output['significant_count']} 个差异显著")
    print(f"结果已保存至: {out_path}")

    # 同时输出摘要
    print(f"\n=== 验证摘要 ===")
    for r in results:
        sig = "✅" if r['any_significant'] else "—"
        direction = "↑" if r['eng_diff_pct']>0 else "↓"
        print(f"  {sig} {r['label']}: 命中{r['yes_count']}条, 互动量{direction}{abs(r['eng_diff_pct']):.1f}%", end="")
        if has_ratio:
            rd = "↑" if r.get('rat_diff_pct',0)>0 else "↓"
            print(f", 转赞比{rd}{abs(r.get('rat_diff_pct',0)):.1f}%", end="")
        print()


# ============================================================
# cmd: report - 生成HTML报告
# ============================================================

def cmd_report(args):
    """读取verify输出的JSON，生成HTML报告"""
    with open(args.verify_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    account_name = args.name or "社媒账号"
    has_ratio = data.get('has_ratio', False)
    features = data.get('features', [])
    total = data.get('total_items', 0)
    sig_count = data.get('significant_count', 0)

    # 取显著特征
    sig_features = [f for f in features if f.get('any_significant')]
    # 也展示不显著的作为参考
    nonsig_features = [f for f in features if not f.get('any_significant')]

    # 互动量TOP特征
    eng_top = sorted([f for f in sig_features if f.get('eng_significant')],
                     key=lambda x: abs(x['eng_diff_pct']), reverse=True)[:5]
    # 转赞比TOP特征
    rat_top = sorted([f for f in sig_features if f.get('rat_significant')],
                     key=lambda x: abs(x.get('rat_diff_pct',0)), reverse=True)[:5] if has_ratio else []

    # 读取LLM的定性洞察（如果有）
    qualitative = []
    if args.insights:
        with open(args.insights, 'r', encoding='utf-8') as f:
            qualitative = json.load(f)

    html = _gen_html(account_name, total, sig_count, has_ratio, data, sig_features, nonsig_features, eng_top, rat_top, qualitative)

    out_path = args.output
    if not out_path:
        run_dir = _resolve_run_dir(args, create=True, prefer_new=False)
        _write_latest_run_dir(run_dir)
        out_path = os.path.join(run_dir, "report.html")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ HTML报告已生成: {out_path}")


def cmd_auto(args):
    df = get_dataframe(args)
    if len(df) == 0:
        sys.exit("ERROR: 数据为空，无法自动分析")
    if 'title' not in df.columns or 'engagement' not in df.columns:
        sys.exit("ERROR: 无法识别标题列或互动量列，请使用 --title-col/--engagement-col 显式指定")

    run_dir = _resolve_run_dir(args, create=True, prefer_new=True)
    _write_latest_run_dir(run_dir)

    cache_path = os.path.join(run_dir, "_data_cache.csv")
    df.to_csv(cache_path, index=False, encoding='utf-8-sig')

    features = _auto_build_features(df, n=args.n, max_features=args.max_features)
    features_path = os.path.join(run_dir, "_features.auto.json")
    with open(features_path, "w", encoding="utf-8") as f:
        json.dump(_json_safe(features), f, ensure_ascii=False, indent=2)

    verify_data = _verify_features_dataframe(
        df,
        features,
        min_hit=args.min_hit,
        min_diff=args.min_diff,
    )
    verify_path = os.path.join(run_dir, "_verify_result.json")
    with open(verify_path, "w", encoding="utf-8") as f:
        json.dump(_json_safe(verify_data), f, ensure_ascii=False, indent=2)

    account_name = args.name or "社媒账号"
    has_ratio = verify_data.get("has_ratio", False)
    all_features = verify_data.get("features", [])
    sig_features = [f for f in all_features if f.get("any_significant")]
    nonsig_features = [f for f in all_features if not f.get("any_significant")]
    eng_top = sorted(
        [f for f in sig_features if f.get("eng_significant")],
        key=lambda x: abs(x.get("eng_diff_pct", 0)),
        reverse=True,
    )[:5]
    if has_ratio:
        rat_top = sorted(
            [f for f in sig_features if f.get("rat_significant")],
            key=lambda x: abs(x.get("rat_diff_pct", 0)),
            reverse=True,
        )[:5]
    else:
        rat_top = []
    html = _gen_html(
        account_name,
        verify_data.get("total_items", 0),
        verify_data.get("significant_count", 0),
        has_ratio,
        verify_data,
        sig_features,
        nonsig_features,
        eng_top,
        rat_top,
        [],
    )
    report_path = os.path.join(run_dir, "report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    detect_info = {
        "run_dir": run_dir,
        "columns": list(df.columns),
        "rows": int(len(df)),
        "auto_feature_count": len(features),
        "significant_count": int(verify_data.get("significant_count", 0)),
        "input_mode": "paste" if getattr(args, "paste", None) else ("stdin" if getattr(args, "stdin", False) else ("file_or_api")),
    }
    detect_path = os.path.join(run_dir, "auto_detect.json")
    with open(detect_path, "w", encoding="utf-8") as f:
        json.dump(_json_safe(detect_info), f, ensure_ascii=False, indent=2)

    print(f"✅ 全自动分析完成")
    print(f"运行目录: {run_dir}")
    print(f"缓存数据: {cache_path}")
    print(f"自动特征: {features_path}")
    print(f"验证结果: {verify_path}")
    print(f"分析报告: {report_path}")
    print(f"识别信息: {detect_path}")


def _esc(text):
    return html_lib.escape(str(text))

def _gen_html(name, total, sig_count, has_ratio, data, sig_features, nonsig_features, eng_top, rat_top, qualitative):
    # 指标名称
    eng_label = "互动量/热度"
    rat_label = "转赞比"

    cards_html = ""
    for i, f in enumerate(sig_features, 1):
        direction = "+" if f['eng_diff_pct']>0 else ""
        diff_color = "text-green-700" if f['eng_diff_pct']>0 else "text-red-600"
        rat_section = ""
        if has_ratio and 'avg_rat_yes' in f:
            rd = "+" if f.get('rat_diff_pct',0)>0 else ""
            rc = "text-green-700" if f.get('rat_diff_pct',0)>0 else "text-red-600"
            rat_section = f"""
            <div class="mt-3 pt-3 border-t border-gray-100 grid grid-cols-2 gap-4 text-sm">
                <div><span class="text-gray-400 text-xs">{_esc(rat_label)}（含特征）</span><p class="font-semibold">{f['avg_rat_yes']}%</p></div>
                <div><span class="text-gray-400 text-xs">{_esc(rat_label)}（不含）</span><p class="font-semibold">{f['avg_rat_no']}%</p></div>
            </div>
            <p class="text-xs mt-1 {rc}">{_esc(rat_label)}差异：{rd}{f.get('rat_diff_pct',0)}%</p>"""

        # 典型标题
        examples = "".join(f'<span class="inline-block bg-gray-50 text-xs text-gray-600 rounded px-2 py-1 mr-2 mb-1">"{_esc(t[:40])}"</span>' for t in f.get('yes_titles',[])[:3])

        cards_html += f"""
        <article class="bg-white border border-gray-100 p-6 mb-4">
            <div class="flex items-start justify-between mb-3">
                <div>
                    <p class="text-xs text-gray-400 mb-1">洞察 #{i}</p>
                    <h4 class="text-base font-bold text-gray-900">{_esc(f['label'])}</h4>
                    <p class="text-xs text-gray-500 mt-1">{_esc(f.get('description',''))}</p>
                </div>
                <div class="text-right flex-shrink-0 ml-4">
                    <p class="text-3xl font-bold {diff_color}">{direction}{f['eng_diff_pct']}%</p>
                    <p class="text-xs text-gray-400">{_esc(eng_label)}差异</p>
                </div>
            </div>
            <div class="grid grid-cols-2 gap-4 text-sm">
                <div class="bg-gray-50 rounded px-4 py-3">
                    <p class="text-xs text-gray-400 mb-1">含该特征</p>
                    <p class="font-bold text-lg">{f['yes_count']} 条</p>
                    <p class="text-gray-600">平均{_esc(eng_label)} {f['avg_eng_yes']}</p>
                </div>
                <div class="bg-gray-50 rounded px-4 py-3">
                    <p class="text-xs text-gray-400 mb-1">不含该特征</p>
                    <p class="font-bold text-lg">{f['no_count']} 条</p>
                    <p class="text-gray-600">平均{_esc(eng_label)} {f['avg_eng_no']}</p>
                </div>
            </div>
            {rat_section}
            <div class="mt-3 pt-3 border-t border-gray-100">
                <p class="text-xs text-gray-400 mb-1">典型高赞标题</p>
                <div class="flex flex-wrap">{examples}</div>
            </div>
        </article>"""

    # 总结表
    summary_rows = ""
    all_display = sig_features + nonsig_features[:3]
    for f in all_display:
        ed = f"{'+'if f['eng_diff_pct']>0 else ''}{f['eng_diff_pct']}%"
        ec = "font-bold" if f.get('eng_significant') else "text-gray-400"
        rd = ""
        rc = "text-gray-400"
        if has_ratio and 'rat_diff_pct' in f:
            rd = f"{'+'if f.get('rat_diff_pct',0)>0 else ''}{f.get('rat_diff_pct',0)}%"
            rc = "font-bold" if f.get('rat_significant') else "text-gray-400"
        sig_mark = "✅" if f.get('any_significant') else "—"
        summary_rows += f"""
        <tr class="border-b border-gray-100">
            <td class="py-2">{sig_mark}</td>
            <td class="py-2">{_esc(f['label'])}</td>
            <td class="py-2 text-right {ec}">{ed}</td>
            {'<td class="py-2 text-right '+rc+'">'+rd+'</td>' if has_ratio else ''}
            <td class="py-2 text-right text-gray-500">{f['yes_count']}条</td>
        </tr>"""

    # 定性洞察
    insights_html = ""
    if qualitative:
        insights_items = ""
        for ins in qualitative[:5]:
            border = "border-gray-900" if ins.get('importance','normal') == 'high' else "border-gray-300"
            insights_items += f"""
            <article class="bg-white border-l-4 {border} p-4 mb-3">
                <p class="text-sm text-gray-700 leading-relaxed">
                    <strong>{_esc(ins.get('title',''))}</strong>：{_esc(ins.get('content',''))}
                </p>
            </article>"""
        insights_html = f"""
        <section class="mx-8 mb-8">
            <h3 class="text-lg font-bold text-gray-900 mb-4">⚠️ 定性洞察 · 因果辨析</h3>
            {insights_items}
        </section>"""

    # 建议区（基于数据自动生成）
    advice_items = ""
    if eng_top:
        top_labels = "、".join(f['label'] for f in eng_top[:3])
        advice_items += f'<div class="mb-3"><p class="font-bold text-gray-900 mb-1">🏆 对{_esc(eng_label)}最有效的特征</p><p class="text-sm text-gray-700">{_esc(top_labels)}</p></div>'
    if rat_top:
        top_labels = "、".join(f['label'] for f in rat_top[:3])
        advice_items += f'<div class="mb-3"><p class="font-bold text-gray-900 mb-1">📊 对{_esc(rat_label)}最有效的特征</p><p class="text-sm text-gray-700">{_esc(top_labels)}</p></div>'

    # 组装HTML
    ratio_header_col = f'<th class="text-right py-2 font-medium">{_esc(rat_label)}影响</th>' if has_ratio else ''
    ratio_stat = f"""
        <div class="border-l-2 border-gray-900 pl-4">
            <p class="text-2xl font-bold">{data.get('global_avg_rat','—')}%</p>
            <p class="text-xs text-gray-500 mt-1">平均{_esc(rat_label)}</p>
        </div>""" if has_ratio else ""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_esc(name)} 内容标题洞察报告</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; background:#fafafa; color:#1a1a1a; }}
@media print {{ body {{ background:white; }} .page-break {{ page-break-before:always; }} }}
</style>
</head>
<body class="min-h-screen">

<!-- 封面 -->
<header class="bg-white border-b border-gray-200 px-8 py-12 mb-8">
    <p class="text-sm tracking-widest text-gray-400 uppercase mb-4">Social Media Title Insight</p>
    <h1 class="text-4xl font-bold text-gray-900 mb-2">{_esc(name)}</h1>
    <h2 class="text-xl font-light text-gray-500 mb-8">内容标题洞察报告</h2>
    <div class="grid grid-cols-4 gap-6 mt-8">
        <div class="border-l-2 border-gray-900 pl-4">
            <p class="text-2xl font-bold">{total}</p>
            <p class="text-xs text-gray-500 mt-1">分析内容条数</p>
        </div>
        <div class="border-l-2 border-gray-900 pl-4">
            <p class="text-2xl font-bold">{'2' if has_ratio else '1'}</p>
            <p class="text-xs text-gray-500 mt-1">分析指标维度</p>
        </div>
        <div class="border-l-2 border-gray-900 pl-4">
            <p class="text-2xl font-bold">{sig_count}</p>
            <p class="text-xs text-gray-500 mt-1">显著特征发现</p>
        </div>
        <div class="border-l-2 border-gray-900 pl-4">
            <p class="text-2xl font-bold">{data.get('global_avg_eng','—')}</p>
            <p class="text-xs text-gray-500 mt-1">平均{_esc(eng_label)}</p>
        </div>
        {ratio_stat}
    </div>
</header>

<!-- 洞察发现 -->
<section class="mx-8 mb-8">
    <h3 class="text-lg font-bold text-gray-900 mb-6">洞察发现</h3>
    {cards_html}
</section>

<div class="page-break"></div>

<!-- 定量总结 -->
<section class="bg-white mx-8 mb-8 p-6 border border-gray-100">
    <h3 class="text-lg font-bold text-gray-900 mb-4">定量总结</h3>
    <table class="w-full text-sm">
        <thead><tr class="border-b-2 border-gray-900">
            <th class="text-left py-2 w-8"></th>
            <th class="text-left py-2 font-medium">特征</th>
            <th class="text-right py-2 font-medium">{_esc(eng_label)}影响</th>
            {ratio_header_col}
            <th class="text-right py-2 font-medium">命中</th>
        </tr></thead>
        <tbody>{summary_rows}</tbody>
    </table>
</section>

{insights_html}

<!-- 建议 -->
<section class="bg-white mx-8 mb-8 p-6 border border-gray-100">
    <h3 class="text-lg font-bold text-gray-900 mb-4">标题创作建议</h3>
    {advice_items}
    <div class="mb-3"><p class="font-bold text-gray-900 mb-1">⚠️ 注意</p><p class="text-sm text-gray-700">若希望提升转赞比而非单纯互动量，可减少泛互动引导，强化内容深度和实用价值。</p></div>
</section>

<!-- 来源 -->
<footer class="mx-8 mb-12 py-4 border-t border-gray-200 text-xs text-gray-400">
    <p>数据来源：API拉取 / 用户上传 | 分析条数：{total}条 | 分析维度：{_esc(eng_label)}{'、'+_esc(rat_label) if has_ratio else ''}</p>
</footer>

</body>
</html>"""


# ============================================================
# cmd: compute
# ============================================================

def cmd_compute(args):
    df = get_dataframe(args)
    expr = args.expr
    n = min(args.n or 50, len(df)//2)
    title_col = _resolve_col(df, args.title_col) if args.title_col else None
    try: df['_score'] = df.eval(expr)
    except Exception as e: sys.exit(f"ERROR: 表达式计算失败: {e}\n可用列: {list(df.columns)}")
    df = df.dropna(subset=['_score'])
    sorted_df = df.sort_values('_score', ascending=False)
    top_n = sorted_df.head(n)
    bottom_n = sorted_df.tail(n)
    show_cols = [title_col, '_score'] if title_col else list(df.columns)+['_score']
    print(f"=== 公式: {expr} | 总量:{len(df)} | 均值:{df['_score'].mean():.2f} ===")
    print(f"Top{n}均值: {top_n['_score'].mean():.2f} | Bottom{n}均值: {bottom_n['_score'].mean():.2f}\n")
    print(f"=== TOP {n} ===")
    for idx, (_, row) in enumerate(top_n.iterrows(), 1):
        print(f"[{idx}] " + " | ".join(_fmt(row[c]) for c in show_cols if c and c in row.index))
    print(f"\n=== BOTTOM {n} ===")
    for idx, (_, row) in enumerate(bottom_n.iterrows(), 1):
        print(f"[{idx}] " + " | ".join(_fmt(row[c]) for c in show_cols if c and c in row.index))


# ============================================================
# 主入口
# ============================================================

def add_data_args(p):
    g = p.add_argument_group('数据源')
    g.add_argument('--input','-i', default=None)
    g.add_argument('--accounts','-a', default=None)
    g.add_argument('--paste', default=None, help='可选：直接粘贴JSON/CSV/TSV/逐行文本数据')
    g.add_argument('--stdin', action='store_true', help='可选：从标准输入读取粘贴数据')
    p.add_argument('--size', type=int, default=100)
    p.add_argument('--cookie', default=None)
    p.add_argument('--tenant-id', default='tx_t1')
    p.add_argument('--run-dir', default=None, help='可选：指定运行目录（默认自动使用 ./runs/<timestamp>）')

def main():
    parser = argparse.ArgumentParser(description='社媒标题数据工具 v4')
    sub = parser.add_subparsers(dest='command')

    p1 = sub.add_parser('preview')
    add_data_args(p1)
    p1.add_argument('--rows','-r', type=int, default=8)

    p2 = sub.add_parser('sort')
    add_data_args(p2)
    p2.add_argument('--col','-c', required=True)
    p2.add_argument('--n', type=int, default=50)
    p2.add_argument('--title-col','-t', default=None)

    p3 = sub.add_parser('compute')
    add_data_args(p3)
    p3.add_argument('--expr','-e', required=True)
    p3.add_argument('--n', type=int, default=50)
    p3.add_argument('--title-col','-t', default=None)

    p4 = sub.add_parser('verify')
    add_data_args(p4)
    p4.add_argument('--features','-f', required=True, help='LLM输出的特征JSON文件路径')
    p4.add_argument('--output','-o', default=None)
    p4.add_argument('--min-hit', type=int, default=2)
    p4.add_argument('--min-diff', type=float, default=15)
    p4.add_argument('--title-col','-t', default=None)
    p4.add_argument('--engagement-col', default=None)
    p4.add_argument('--ratio-col', default=None)

    p5 = sub.add_parser('report')
    p5.add_argument('--verify-json','-v', required=True, help='verify命令输出的JSON')
    p5.add_argument('--name','-n', default='社媒账号', help='账号/品牌名')
    p5.add_argument('--output','-o', default=None)
    p5.add_argument('--insights', default=None, help='可选：LLM定性洞察JSON')
    p5.add_argument('--run-dir', default=None, help='可选：指定运行目录（默认沿用最近一次运行目录）')

    p6 = sub.add_parser('auto')
    add_data_args(p6)
    p6.add_argument('--name','-n', default='社媒账号', help='账号/品牌名')
    p6.add_argument('--title-col','-t', default=None)
    p6.add_argument('--engagement-col', default=None)
    p6.add_argument('--ratio-col', default=None)
    p6.add_argument('--n', type=int, default=30, help='Top/Bottom采样数量')
    p6.add_argument('--min-hit', type=int, default=2)
    p6.add_argument('--min-diff', type=float, default=15)
    p6.add_argument('--max-features', type=int, default=12, help='自动特征最多数量')

    args = parser.parse_args()
    cmds = {'preview':cmd_preview, 'sort':cmd_sort, 'compute':cmd_compute, 'verify':cmd_verify, 'report':cmd_report, 'auto':cmd_auto}
    if args.command in cmds:
        cmds[args.command](args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
