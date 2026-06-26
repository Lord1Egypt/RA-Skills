"""数据解析器。将 CSV、Excel、JSON、TXT 等文件解析为 DataFrame。"""

import sys
import pandas as pd
import numpy as np
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

if __name__ == '__main__' and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from core.exceptions import FileError, DataError, ErrorCode
else:
    from .exceptions import FileError, DataError, ErrorCode


class DataParser:

    MAX_FILE_SIZE_MB = 100  # 单文件最大允许大小（MB）

    def __init__(self):
        self._parsers = {
            '.csv': self._parse_csv,
            '.tsv': self._parse_tsv,
            '.xlsx': self._parse_excel,
            '.xls': self._parse_excel,
            '.json': self._parse_json,
            '.txt': self._parse_text,
        }

    def parse_file(self, file_path: str, **kwargs) -> pd.DataFrame:
        path = Path(file_path)
        if not path.exists():
            raise FileError(f"文件不存在: {file_path}", ErrorCode.FILE_NOT_FOUND)
        if not path.is_file():
            raise FileError(f"不是文件: {file_path}", ErrorCode.FILE_PERMISSION_DENIED)
        if path.stat().st_size > self.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise FileError(f"文件超过{self.MAX_FILE_SIZE_MB}MB限制", ErrorCode.FILE_SIZE_EXCEEDED)

        ext = path.suffix.lower()
        if ext not in self._parsers:
            ext = self._detect_type(path)
        if ext not in self._parsers:
            supported = ', '.join(self._parsers.keys())
            raise FileError(f"不支持的格式: {ext}，支持: {supported}", ErrorCode.FILE_FORMAT_INVALID)

        df = self._parsers[ext](path, **kwargs)
        if df.empty:
            raise DataError("文件内容为空", ErrorCode.DATA_EMPTY)

        df = self._clean(df)
        self._validate(df)
        return df

    def parse_files(self, file_paths: List[str], merge: bool = False) -> Any:
        """解析多个文件，返回 DataFrame 列表或合并后的 DataFrame。"""
        results = []
        for fp in file_paths:
            df = self.parse_file(fp)
            results.append({'file': Path(fp).name, 'data': df})

        if not merge:
            return results

        return self._merge(results)

    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        summary: Dict[str, Any] = {
            'shape': list(df.shape),
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
            'missing': {k: int(v) for k, v in df.isnull().sum().to_dict().items()},
            'sample': df.head(5).to_dict('records'),
        }
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            summary['stats'] = df[numeric_cols].describe().to_dict()
        return summary

    def _merge(self, results: List[Dict]) -> Tuple[pd.DataFrame, str]:
        """尝试合并多个 DataFrame。返回 (merged_df, merge_type)。"""
        dfs = [r['data'] for r in results]
        col_sets = [set(df.columns) for df in dfs]

        # 纵向拼接：所有文件列名完全相同
        if all(len(cs) > 0 for cs in col_sets) and all(cs == col_sets[0] for cs in col_sets):
            merged = pd.concat(dfs, ignore_index=True)
            merged['source_file'] = [r['file'] for r in results for _ in range(len(r['data']))]
            cols = list(merged.columns)
            cols.remove('source_file')
            merged = merged[cols + ['source_file']]
            return merged, '纵向拼接'

        # 横向关联：公共列占比 >= 50%
        if len(dfs) >= 2 and all(len(cs) > 0 for cs in col_sets):
            intersection = col_sets[0]
            for cs in col_sets[1:]:
                intersection = intersection & cs
            avg_col_count = sum(len(cs) for cs in col_sets) / len(col_sets)
            if len(intersection) >= avg_col_count * 0.5:
                merged = dfs[0]
                for df in dfs[1:]:
                    merged = pd.merge(merged, df, on=list(intersection), how='outer', suffixes=('', '_dup'))
                merged.columns = [c.replace('_dup', '') if c.endswith('_dup') else c for c in merged.columns]
                merged = merged.loc[:, ~merged.columns.duplicated()]
                return merged, '横向关联'

        # 无法自动合并
        summary_parts = []
        for r in results:
            summary_parts.append(f"{r['file']}: {r['data'].shape[0]}行 {r['data'].shape[1]}列, 列={list(r['data'].columns)}")
        raise DataError(
            f"文件结构差异大，无法自动合并。各文件信息：\n" + "\n".join(summary_parts) +
            "\n请指定关联方式，或分别分析。",
            ErrorCode.DATA_PARSE_ERROR
        )

    # ---- 解析实现 ----

    def _parse_csv(self, path: Path, **kw) -> pd.DataFrame:
        encoding = kw.get('encoding', 'utf-8')
        try:
            return pd.read_csv(path, encoding=encoding, low_memory=False)
        except pd.errors.EmptyDataError:
            raise DataError("文件内容为空", ErrorCode.DATA_EMPTY)
        except UnicodeDecodeError:
            for enc in ('gbk', 'gb2312', 'utf-16', 'latin1'):
                try:
                    return pd.read_csv(path, encoding=enc, low_memory=False)
                except (UnicodeDecodeError, pd.errors.EmptyDataError):
                    continue
            raise DataError("无法解码文件", ErrorCode.DATA_PARSE_ERROR)

    def _parse_tsv(self, path: Path, **kw) -> pd.DataFrame:
        """解析 TSV 文件，支持多编码回退（与 CSV 一致）。"""
        encoding = kw.get('encoding', 'utf-8')
        try:
            return pd.read_csv(path, sep='\t', encoding=encoding, low_memory=False)
        except pd.errors.EmptyDataError:
            raise DataError("文件内容为空", ErrorCode.DATA_EMPTY)
        except UnicodeDecodeError:
            for enc in ('gbk', 'gb2312', 'utf-16', 'latin1'):
                try:
                    return pd.read_csv(path, sep='\t', encoding=enc, low_memory=False)
                except (UnicodeDecodeError, pd.errors.EmptyDataError):
                    continue
            raise DataError("无法解码文件", ErrorCode.DATA_PARSE_ERROR)

    def _parse_excel(self, path: Path, **kw) -> pd.DataFrame:
        sheet = kw.get('sheet_name', 0)
        # 根据扩展名选择引擎：.xlsx 用 openpyxl，.xls 用 xlrd
        ext = path.suffix.lower()
        engine = 'xlrd' if ext == '.xls' else 'openpyxl'
        try:
            df = pd.read_excel(path, sheet_name=sheet, engine=engine)
            if df.empty:
                xl = pd.ExcelFile(path, engine=engine)
                for s in xl.sheet_names:
                    df = pd.read_excel(path, sheet_name=s, engine=engine)
                    if not df.empty:
                        return df
            return df
        except Exception as e:
            raise DataError(f"Excel读取失败: {e}", ErrorCode.DATA_PARSE_ERROR)

    def _parse_json(self, path: Path, **kw) -> pd.DataFrame:
        """解析 JSON 文件，支持多编码回退。"""
        data = None
        last_error = None
        for enc in ('utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'latin1'):
            try:
                with open(path, 'r', encoding=enc) as f:
                    data = json.load(f)
                break
            except UnicodeDecodeError:
                continue
            except json.JSONDecodeError as e:
                last_error = e
                continue
        if data is None:
            if last_error:
                raise DataError(f"JSON 解析失败: {last_error}", ErrorCode.DATA_PARSE_ERROR)
            raise DataError("无法解码 JSON 文件", ErrorCode.DATA_PARSE_ERROR)

        if isinstance(data, list):
            return pd.DataFrame(data)
        if isinstance(data, dict):
            for v in data.values():
                if isinstance(v, list):
                    return pd.DataFrame(v)
            return pd.json_normalize(data)
        raise DataError("不支持的JSON结构", ErrorCode.DATA_PARSE_ERROR)

    def _parse_text(self, path: Path, **kw) -> pd.DataFrame:
        """解析文本文件，支持多编码回退。"""
        lines = None
        for enc in ('utf-8', 'gbk', 'gb2312', 'latin1'):
            try:
                with open(path, 'r', encoding=enc) as f:
                    lines = [l.strip() for l in f if l.strip()]
                break
            except UnicodeDecodeError:
                continue
        if not lines:
            raise DataError("文件为空", ErrorCode.DATA_EMPTY)
        for delim in (',', '\t', ';', '|'):
            if delim in lines[0] and len(lines[0].split(delim)) > 1:
                return pd.read_csv(path, sep=delim, low_memory=False)
        return pd.DataFrame({'content': lines})

    def _detect_type(self, path: Path) -> str:
        try:
            header = path.read_bytes(1024)
            text = header.decode('utf-8', errors='ignore')
            if text.strip().startswith(('{', '[')):
                return '.json'
            if header.startswith(b'\x50\x4B\x03\x04'):
                return '.xlsx'
            for delim in (',', '\t', ';'):
                if delim in text:
                    return '.csv'
        except Exception:
            pass
        return path.suffix.lower()

    def _clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(axis=1, how='all').dropna(axis=0, how='all').drop_duplicates().reset_index(drop=True)
        df.columns = [self._normalize_col(c) for c in df.columns]
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except Exception:
                    pass
        return df

    @staticmethod
    def _normalize_col(name: Any) -> str:
        if pd.isna(name):
            return 'unnamed'
        s = re.sub(r'[^\w\s]', '_', str(name).strip())
        s = re.sub(r'[\s_]+', '_', s).strip('_').lower()
        return s or 'unnamed'

    @staticmethod
    def _validate(df: pd.DataFrame):
        if df.empty:
            raise DataError("数据为空", ErrorCode.DATA_EMPTY)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python data_parser.py <file1> [file2 ...] [--summary] [--merge]")
        sys.exit(1)

    paths = [a for a in sys.argv[1:] if not a.startswith('--')]
    do_summary = '--summary' in sys.argv
    do_merge = '--merge' in sys.argv
    parser = DataParser()

    try:
        if len(paths) == 1 and not do_merge:
            df = parser.parse_file(paths[0])
            if do_summary:
                print(json.dumps(parser.get_data_summary(df), ensure_ascii=False, indent=2, default=str))
            else:
                print(f"解析成功: {df.shape[0]} 行, {df.shape[1]} 列")
                print(f"列名: {list(df.columns)}")
                print(df.head(5).to_string())
        else:
            result = parser.parse_files(paths, merge=do_merge)
            if do_merge:
                merged_df, merge_type = result
                print(f"合并方式: {merge_type}")
                if do_summary:
                    print(json.dumps(parser.get_data_summary(merged_df), ensure_ascii=False, indent=2, default=str))
                else:
                    print(f"合并后: {merged_df.shape[0]} 行, {merged_df.shape[1]} 列")
                    print(f"列名: {list(merged_df.columns)}")
                    print(merged_df.head(5).to_string())
            else:
                summaries = []
                for item in result:
                    s = parser.get_data_summary(item['data'])
                    summaries.append({'file': item['file'], **s})
                if do_summary:
                    print(json.dumps(summaries, ensure_ascii=False, indent=2, default=str))
                else:
                    for item in result:
                        df = item['data']
                        print(f"\n--- {item['file']}: {df.shape[0]} 行, {df.shape[1]} 列 ---")
                        print(f"列名: {list(df.columns)}")
                        print(df.head(3).to_string())
    except (FileError, DataError) as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
