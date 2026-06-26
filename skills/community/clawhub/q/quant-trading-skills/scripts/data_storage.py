#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Union

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def save_to_parquet(
    data: Union[pd.DataFrame, list, dict],
    file_path: str,
    partition_cols: Optional[List[str]] = None
) -> str:
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        df = pd.DataFrame(data)
    else:
        df = data
    
    if df.empty:
        raise ValueError("数据为空，无法保存")
    
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if partition_cols:
        partition_root = path.parent / path.stem
        partition_root.mkdir(parents=True, exist_ok=True)
        table = pa.Table.from_pandas(df, preserve_index=False)
        pq.write_to_dataset(
            table,
            root_path=str(partition_root),
            partition_cols=partition_cols,
            compression='snappy'
        )
        return str(partition_root)
    else:
        table = pa.Table.from_pandas(df, preserve_index=False)
        pq.write_table(table, str(path), compression='snappy')
        return str(path)


def read_parquet(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    if path.is_dir():
        table = pq.read_table(str(path))
    else:
        table = pq.read_table(str(path))
    
    return table.to_pandas()


def append_to_parquet(data: Union[pd.DataFrame, list, dict], file_path: str) -> str:
    if isinstance(data, list):
        new_df = pd.DataFrame(data)
    elif isinstance(data, dict):
        new_df = pd.DataFrame(data)
    else:
        new_df = data
    
    if new_df.empty:
        raise ValueError("数据为空，无法追加")
    
    path = Path(file_path)
    
    if path.exists() and path.is_file():
        existing_df = read_parquet(str(path))
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df = combined_df.drop_duplicates()
        table = pa.Table.from_pandas(combined_df, preserve_index=False)
        pq.write_table(table, str(path), compression='snappy')
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        table = pa.Table.from_pandas(new_df, preserve_index=False)
        pq.write_table(table, str(path), compression='snappy')
    
    return str(path)


def save_market_data(data: Union[pd.DataFrame, list, dict], base_path: str) -> List[str]:
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        if 'items' in data:
            df = pd.DataFrame(data['items'])
            if 'symbol' in data:
                df['symbol'] = data['symbol']
        else:
            df = pd.DataFrame(data)
    else:
        df = data
    
    if df.empty:
        raise ValueError("行情数据为空，无法保存")
    
    if 'date' not in df.columns:
        raise ValueError("行情数据缺少 'date' 字段")
    
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.strftime('%Y-%m')
    
    if 'symbol' not in df.columns:
        raise ValueError("行情数据缺少 'symbol' 字段")
    
    saved_files = []
    base = Path(base_path)
    
    for symbol in df['symbol'].unique():
        symbol_df = df[df['symbol'] == symbol].copy()
        
        for year_month in symbol_df['year_month'].unique():
            month_df = symbol_df[symbol_df['year_month'] == year_month].copy()
            month_df = month_df.drop(columns=['year_month'])
            
            file_path = base / str(symbol) / f"{year_month}.parquet"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if file_path.exists():
                existing_df = read_parquet(str(file_path))
                combined_df = pd.concat([existing_df, month_df], ignore_index=True)
                combined_df = combined_df.drop_duplicates(subset=['date'], keep='last')
                month_df = combined_df
            
            table = pa.Table.from_pandas(month_df, preserve_index=False)
            pq.write_table(table, str(file_path), compression='snappy')
            saved_files.append(str(file_path))
    
    return saved_files


def save_north_flow_data(data: Union[pd.DataFrame, list, dict], base_path: str) -> List[str]:
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        if 'items' in data:
            df = pd.DataFrame(data['items'])
        else:
            df = pd.DataFrame(data)
    else:
        df = data
    
    if df.empty:
        raise ValueError("北向资金数据为空，无法保存")
    
    if 'date' not in df.columns:
        raise ValueError("北向资金数据缺少 'date' 字段")
    
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.strftime('%Y-%m')
    
    saved_files = []
    base = Path(base_path)
    
    for year_month in df['year_month'].unique():
        month_df = df[df['year_month'] == year_month].copy()
        month_df = month_df.drop(columns=['year_month'])
        
        file_path = base / f"{year_month}.parquet"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if file_path.exists():
            existing_df = read_parquet(str(file_path))
            combined_df = pd.concat([existing_df, month_df], ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=['date'], keep='last')
            month_df = combined_df
        
        table = pa.Table.from_pandas(month_df, preserve_index=False)
        pq.write_table(table, str(file_path), compression='snappy')
        saved_files.append(str(file_path))
    
    return saved_files


def save_lhb_data(data: Union[pd.DataFrame, list, dict], base_path: str) -> List[str]:
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        if 'items' in data:
            df = pd.DataFrame(data['items'])
        else:
            df = pd.DataFrame(data)
    else:
        df = data
    
    if df.empty:
        raise ValueError("龙虎榜数据为空，无法保存")
    
    if 'date' not in df.columns:
        raise ValueError("龙虎榜数据缺少 'date' 字段")
    
    df['date'] = pd.to_datetime(df['date'])
    df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')
    
    saved_files = []
    base = Path(base_path)
    
    for date_str in df['date_str'].unique():
        date_df = df[df['date_str'] == date_str].copy()
        date_df = date_df.drop(columns=['date_str'])
        
        file_path = base / f"{date_str}.parquet"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if file_path.exists():
            existing_df = read_parquet(str(file_path))
            combined_df = pd.concat([existing_df, date_df], ignore_index=True)
            if 'symbol' in combined_df.columns:
                combined_df = combined_df.drop_duplicates(subset=['date', 'symbol'], keep='last')
            else:
                combined_df = combined_df.drop_duplicates(subset=['date'], keep='last')
            date_df = combined_df
        
        table = pa.Table.from_pandas(date_df, preserve_index=False)
        pq.write_table(table, str(file_path), compression='snappy')
        saved_files.append(str(file_path))
    
    return saved_files


def save_sentiment_data(data: Union[pd.DataFrame, list, dict], base_path: str) -> List[str]:
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        if 'items' in data:
            df = pd.DataFrame(data['items'])
            if 'symbol' in data:
                df['symbol'] = data['symbol']
        else:
            df = pd.DataFrame(data)
    else:
        df = data
    
    if df.empty:
        raise ValueError("舆情数据为空，无法保存")
    
    if 'date' not in df.columns:
        raise ValueError("舆情数据缺少 'date' 字段")
    
    if 'symbol' not in df.columns:
        raise ValueError("舆情数据缺少 'symbol' 字段")
    
    df['date'] = pd.to_datetime(df['date'])
    df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')
    
    saved_files = []
    base = Path(base_path)
    
    for symbol in df['symbol'].unique():
        symbol_df = df[df['symbol'] == symbol].copy()
        
        for date_str in symbol_df['date_str'].unique():
            date_df = symbol_df[symbol_df['date_str'] == date_str].copy()
            date_df = date_df.drop(columns=['date_str'])
            
            file_path = base / str(symbol) / f"{date_str}.parquet"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if file_path.exists():
                existing_df = read_parquet(str(file_path))
                combined_df = pd.concat([existing_df, date_df], ignore_index=True)
                if 'title' in combined_df.columns:
                    combined_df = combined_df.drop_duplicates(subset=['date', 'title'], keep='last')
                else:
                    combined_df = combined_df.drop_duplicates(subset=['date'], keep='last')
                date_df = combined_df
            
            table = pa.Table.from_pandas(date_df, preserve_index=False)
            pq.write_table(table, str(file_path), compression='snappy')
            saved_files.append(str(file_path))
    
    return saved_files


def save_financial_data(data: Union[pd.DataFrame, list, dict], base_path: str) -> List[str]:
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        if 'items' in data:
            df = pd.DataFrame(data['items'])
            if 'symbol' in data:
                df['symbol'] = data['symbol']
        else:
            df = pd.DataFrame(data)
    else:
        df = data
    
    if df.empty:
        raise ValueError("财报数据为空，无法保存")
    
    if 'symbol' not in df.columns:
        raise ValueError("财报数据缺少 'symbol' 字段")
    
    date_col = None
    for col in ['report_date', 'date', 'reportDate']:
        if col in df.columns:
            date_col = col
            break
    
    if date_col is None:
        raise ValueError("财报数据缺少日期字段 (report_date, date 或 reportDate)")
    
    df[date_col] = pd.to_datetime(df[date_col])
    df['year'] = df[date_col].dt.year
    
    saved_files = []
    base = Path(base_path)
    
    for symbol in df['symbol'].unique():
        symbol_df = df[df['symbol'] == symbol].copy()
        
        for year in symbol_df['year'].unique():
            year_df = symbol_df[symbol_df['year'] == year].copy()
            year_df = year_df.drop(columns=['year'])
            
            file_path = base / str(symbol) / f"{year}.parquet"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if file_path.exists():
                existing_df = read_parquet(str(file_path))
                combined_df = pd.concat([existing_df, year_df], ignore_index=True)
                combined_df = combined_df.drop_duplicates(subset=[date_col], keep='last')
                year_df = combined_df
            
            table = pa.Table.from_pandas(year_df, preserve_index=False)
            pq.write_table(table, str(file_path), compression='snappy')
            saved_files.append(str(file_path))
    
    return saved_files


if __name__ == '__main__':
    import json
    
    if len(sys.argv) < 2:
        print(json.dumps({'error': '缺少参数'}))
        sys.exit(1)
    
    action = sys.argv[1]
    input_data = sys.stdin.read()
    params = json.loads(input_data) if input_data else {}
    
    try:
        if action == 'save_parquet':
            result = save_to_parquet(
                params.get('data'),
                params.get('file_path'),
                params.get('partition_cols')
            )
        elif action == 'read_parquet':
            result = read_parquet(params.get('file_path')).to_dict(orient='records')
        elif action == 'append_parquet':
            result = append_to_parquet(
                params.get('data'),
                params.get('file_path')
            )
        elif action == 'save_market':
            result = save_market_data(
                params.get('data'),
                params.get('base_path', 'data/market')
            )
        elif action == 'save_north_flow':
            result = save_north_flow_data(
                params.get('data'),
                params.get('base_path', 'data/north_flow')
            )
        elif action == 'save_lhb':
            result = save_lhb_data(
                params.get('data'),
                params.get('base_path', 'data/lhb')
            )
        elif action == 'save_sentiment':
            result = save_sentiment_data(
                params.get('data'),
                params.get('base_path', 'data/sentiment')
            )
        elif action == 'save_financial':
            result = save_financial_data(
                params.get('data'),
                params.get('base_path', 'data/financial')
            )
        else:
            print(json.dumps({'error': '未知的操作类型'}))
            sys.exit(1)
        
        print(json.dumps({'success': True, 'result': result}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)
