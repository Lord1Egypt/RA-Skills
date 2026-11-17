#!/usr/bin/env python3
"""
抽样执行器
支持简单随机、分层、系统、整群四种抽样算法
"""

import argparse
import json
import os
import random
from datetime import datetime
from collections import defaultdict
import pandas as pd

SCHEMES_DIR = "./sampling_schemes"
RECORDS_DIR = "./sampling_records"


def ensure_dirs():
    """确保目录存在"""
    os.makedirs(SCHEMES_DIR, exist_ok=True)
    os.makedirs(RECORDS_DIR, exist_ok=True)


def load_scheme(scheme_name):
    """加载抽样方案"""
    path = os.path.join(SCHEMES_DIR, f"{scheme_name}.json")
    if not os.path.exists(path):
        raise ValueError(f"方案不存在: {scheme_name}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_data(data_path):
    """加载解析后的数据"""
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def simple_random_sampling(data, params):
    """简单随机抽样"""
    records = data['data']
    total = len(records)
    
    # 获取样本量
    sample_size = params.get('sample_size')
    sample_rate = params.get('sample_rate')
    
    if sample_size:
        n = min(int(sample_size), total)
    elif sample_rate:
        n = max(1, int(total * float(sample_rate)))
    else:
        raise ValueError("缺少 sample_size 或 sample_rate 参数")
    
    # 无放回随机抽样
    indices = random.sample(range(total), n)
    
    samples = []
    for new_idx, orig_idx in enumerate(indices):
        sample = {"index": new_idx, "original_index": orig_idx}
        sample.update(records[orig_idx])
        samples.append(sample)
    
    return {
        "samples": samples,
        "sample_count": n,
        "sampling_rule": f"从{total}条记录中随机抽取{n}条，无放回抽样"
    }


def stratified_sampling(data, params):
    """分层抽样"""
    records = data['data']
    total = len(records)
    
    strata_field = params.get('strata_field')
    if not strata_field:
        raise ValueError("分层抽样需要指定 strata_field 参数")
    
    # 按分层字段分组
    strata = defaultdict(list)
    for idx, record in enumerate(records):
        key = str(record.get(strata_field, 'Unknown'))
        strata[key].append(idx)
    
    # 计算各层样本量
    n_total = params.get('sample_size', 100)
    allocation = params.get('allocation', 'proportional')
    
    if allocation == 'proportional':
        # 比例分配
        samples = []
        for stratum_name, indices in strata.items():
            n_stratum = max(1, int(n_total * len(indices) / total))
            n_stratum = min(n_stratum, len(indices))
            selected = random.sample(indices, n_stratum)
            for new_idx, orig_idx in enumerate(selected):
                sample = {"index": len(samples), "original_index": orig_idx, 
                         "_stratum": stratum_name}
                sample.update(records[orig_idx])
                samples.append(sample)
    else:
        # 等额分配
        samples = []
        for stratum_name, indices in strata.items():
            n_stratum = min(n_total // len(strata), len(indices))
            selected = random.sample(indices, n_stratum)
            for orig_idx in selected:
                sample = {"index": len(samples), "original_index": orig_idx,
                         "_stratum": stratum_name}
                sample.update(records[orig_idx])
                samples.append(sample)
    
    return {
        "samples": samples,
        "sample_count": len(samples),
        "strata": {k: len(v) for k, v in strata.items()},
        "sampling_rule": f"按'{strata_field}'分层，{allocation}分配，共抽取{len(samples)}条"
    }


def systematic_sampling(data, params):
    """系统抽样"""
    records = data['data']
    total = len(records)
    
    interval = params.get('interval')
    if not interval:
        # 根据样本比例计算间隔
        sample_rate = params.get('sample_rate', 0.1)
        interval = max(1, int(1 / sample_rate))
    
    interval = int(interval)
    random_start = params.get('random_start', random.randint(0, interval - 1))
    
    # 选择起始点
    start = random_start % interval
    
    # 等间隔选取
    indices = list(range(start, total, interval))
    
    samples = []
    for new_idx, orig_idx in enumerate(indices):
        sample = {"index": new_idx, "original_index": orig_idx, "_interval": interval}
        sample.update(records[orig_idx])
        samples.append(sample)
    
    return {
        "samples": samples,
        "sample_count": len(samples),
        "interval": interval,
        "start_point": start,
        "sampling_rule": f"从第{start + 1}条开始，每隔{interval}条抽取1条，共抽取{len(samples)}条"
    }


def cluster_sampling(data, params):
    """整群抽样"""
    records = data['data']
    
    cluster_field = params.get('cluster_field')
    if not cluster_field:
        raise ValueError("整群抽样需要指定 cluster_field 参数")
    
    # 按群字段分组
    clusters = defaultdict(list)
    for idx, record in enumerate(records):
        key = str(record.get(cluster_field, 'Unknown'))
        clusters[key].append(idx)
    
    # 计算抽取群数
    cluster_rate = params.get('cluster_rate', 0.2)
    n_clusters = max(1, int(len(clusters) * cluster_rate))
    
    # 随机抽取群
    selected_clusters = random.sample(list(clusters.keys()), 
                                      min(n_clusters, len(clusters)))
    
    # 抽中群内全部纳入
    samples = []
    for cluster_name in selected_clusters:
        for orig_idx in clusters[cluster_name]:
            sample = {"index": len(samples), "original_index": orig_idx,
                     "_cluster": cluster_name}
            sample.update(records[orig_idx])
            samples.append(sample)
    
    return {
        "samples": samples,
        "sample_count": len(samples),
        "clusters": {k: len(v) for k, v in clusters.items()},
        "selected_clusters": selected_clusters,
        "sampling_rule": f"按'{cluster_field}'分群，抽取{len(selected_clusters)}个群，群内全检，共{len(samples)}条"
    }


def execute_sampling(data, scheme):
    """执行抽样"""
    scheme_type = scheme['type']
    params = scheme['params']
    
    if scheme_type == 'simple':
        return simple_random_sampling(data, params)
    elif scheme_type == 'stratified':
        return stratified_sampling(data, params)
    elif scheme_type == 'systematic':
        return systematic_sampling(data, params)
    elif scheme_type == 'cluster':
        return cluster_sampling(data, params)
    else:
        raise ValueError(f"不支持的抽样类型: {scheme_type}")


def generate_record_id():
    """生成记录ID"""
    now = datetime.now()
    return f"REC{now.strftime('%Y%m%d%H%M%S')}{random.randint(10, 99)}"


def save_record(record_id, scheme_name, scheme_type, data_path, result, data_info):
    """保存抽样记录"""
    ensure_dirs()
    
    record = {
        "record_id": record_id,
        "scheme_name": scheme_name,
        "created_at": datetime.now().isoformat(),
        "operator": "system",
        "data_source": data_path,
        "original_record_count": data_info['record_count'],
        "sample_count": result['sample_count'],
        "status": "completed",
        "log": [
            {"time": datetime.now().strftime("%H:%M:%S"), 
             "action": "load_scheme", 
             "detail": f"加载方案 {scheme_name}"},
            {"time": datetime.now().strftime("%H:%M:%S"), 
             "action": "parse_data", 
             "detail": f"解析数据文件，共{data_info['record_count']}条记录"},
            {"time": datetime.now().strftime("%H:%M:%S"), 
             "action": "execute_sampling", 
             "detail": f"执行{scheme_type}抽样"},
            {"time": datetime.now().strftime("%H:%M:%S"), 
             "action": "save_result", 
             "detail": f"保存抽样结果"}
        ]
    }
    
    path = os.path.join(RECORDS_DIR, f"{record_id}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    
    return path


def main():
    parser = argparse.ArgumentParser(description='抽样执行器')
    parser.add_argument('--data', required=True, help='解析后的数据JSON文件路径')
    parser.add_argument('--scheme', required=True, help='抽样方案名称')
    parser.add_argument('--output', required=True, help='抽样结果输出路径')
    parser.add_argument('--record', action='store_true', help='是否保存抽样记录')
    
    args = parser.parse_args()
    
    try:
        # 加载数据和方案
        data = load_data(args.data)
        scheme = load_scheme(args.scheme)
        
        # 执行抽样
        result = execute_sampling(data, scheme)
        
        # 构建完整结果
        output = {
            "scheme_name": scheme['name'],
            "scheme_type": scheme['type'],
            "sampling_time": datetime.now().isoformat(),
            "data_summary": {
                "total_records": data['record_count'],
                "fields": data['fields']
            },
            "sampling_params": scheme['params'],
            "samples": result['samples'],
            "sample_count": result['sample_count'],
            "sampling_rule": result.get('sampling_rule', '')
        }
        
        # 保存结果
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        # 保存记录
        if args.record:
            record_id = generate_record_id()
            record_path = save_record(record_id, args.scheme, scheme['type'], args.data, result, data)
            print(json.dumps({
                "success": True, 
                "output": args.output,
                "record_id": record_id
            }, ensure_ascii=False))
        else:
            print(json.dumps({"success": True, "output": args.output}, ensure_ascii=False))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return


if __name__ == "__main__":
    main()
