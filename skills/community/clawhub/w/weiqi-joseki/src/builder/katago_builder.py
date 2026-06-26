#!/usr/bin/env python3
"""
KataGo定式库构建器
基于KataGo Archive棋谱构建定式库

核心算法（与原代码保持一致）：
1. Phase 1: CMS统计频率 + 临时文件存储
2. Phase 2: 逆向遍历 + 单链检测 + 小顶堆选top-k
3. Phase 3: 统一转ruld方向去重
4. Phase 4: 入库
"""

import gzip
import heapq
import os
import tempfile
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import Counter
from datetime import datetime

from ..extraction import extract_moves_all_corners, get_move_sequence
from ..extraction.katago_downloader import iter_sgf_from_tar
from ..core.coords import convert_to_top_right
from ..storage.json_storage import JsonStorage, DEFAULT_DB_PATH
from ..utils import CountMinSketch


# 四角配置
CORNERS = ['tl', 'tr', 'bl', 'br']


def convert_to_rudl(moves: List[str]) -> List[str]:
    """
    将ruld方向的着法序列转换为rudl方向
    
    使用 COORDINATE_SYSTEMS 中定义的坐标系进行转换：
    - ruld: 右上(左→下) - 原点是tr, x往左, y往下
    - rudl: 右上(下→左) - 原点是tr, x往下, y往左
    
    转换步骤：
    1. 用 ruld 坐标系将 SGF 坐标转为局部坐标 (x, y)
    2. 用 rudl 坐标系将局部坐标 (x, y) 转回 SGF 坐标
    """
    from ..core.coords import COORDINATE_SYSTEMS
    
    ruld_sys = COORDINATE_SYSTEMS['ruld']  # 源坐标系
    rudl_sys = COORDINATE_SYSTEMS['rudl']  # 目标坐标系
    
    rudl_moves = []
    for sgf in moves:
        if not sgf or sgf == 'pass' or sgf == 'tt':
            rudl_moves.append(sgf)
            continue
        
        # ruld SGF -> 局部坐标
        local = ruld_sys._to_local_cache.get(sgf)
        if local is None:
            rudl_moves.append(sgf)
            continue
        
        # 局部坐标 -> rudl SGF
        new_sgf = rudl_sys._to_sgf_cache.get(local)
        if new_sgf is None:
            rudl_moves.append(sgf)
            continue
        
        rudl_moves.append(new_sgf)
    
    return rudl_moves


def convert_to_ruld(moves: List[str]) -> List[str]:
    """
    将rudl方向的着法序列转换回ruld方向
    （convert_to_rudl的逆操作）
    
    使用 COORDINATE_SYSTEMS 中定义的坐标系进行转换
    """
    from ..core.coords import COORDINATE_SYSTEMS
    
    rudl_sys = COORDINATE_SYSTEMS['rudl']  # 源坐标系
    ruld_sys = COORDINATE_SYSTEMS['ruld']  # 目标坐标系
    
    ruld_moves = []
    for sgf in moves:
        if not sgf or sgf == 'pass' or sgf == 'tt':
            ruld_moves.append(sgf)
            continue
        
        # rudl SGF -> 局部坐标
        local = rudl_sys._to_local_cache.get(sgf)
        if local is None:
            ruld_moves.append(sgf)
            continue
        
        # 局部坐标 -> ruld SGF
        new_sgf = ruld_sys._to_sgf_cache.get(local)
        if new_sgf is None:
            ruld_moves.append(sgf)
            continue
        
        ruld_moves.append(new_sgf)
    
    return ruld_moves


class HeapItem:
    """堆项 - 用于小顶堆选top-k"""
    __slots__ = ['count', 'prefix', 'direction', 'prefix_hash']
    
    def __init__(self, count, prefix, direction, prefix_hash):
        self.count = count
        self.prefix = prefix
        self.direction = direction
        self.prefix_hash = prefix_hash
    
    def __lt__(self, other):
        return self.count < other.count


class KatagoJosekiBuilder:
    """
    KataGo定式库构建器
    
    保留原代码核心算法：
    - CMS频率估算
    - 临时文件存储
    - 逆向遍历
    - 单链检测
    - 小顶堆选top-k
    """
    
    def __init__(self, db_path: Optional[str] = None):
        self.storage = JsonStorage(db_path)
        # CMS配置（与原代码一致）
        self._cms_width = 200000
        self._cms_depth = 5
    
    def set_cms_config(self, width: int = 200000, depth: int = 5):
        """设置CMS配置（与原代码一致）"""
        self._cms_width = width
        self._cms_depth = depth
    

    
    def process_sgf(self, sgf_data: str, first_n: int = 80, 
                    distance_threshold: int = 4) -> Dict[str, List[str]]:
        """
        处理单个SGF，提取四角着法
        
        Returns:
            {corner: [coord, ...], ...} 原始SGF坐标
        """
        corner_moves = extract_moves_all_corners(
            sgf_data, 
            first_n=first_n, 
            distance_threshold=distance_threshold
        )
        
        # 转换为纯坐标序列
        return {corner: get_move_sequence(moves) 
                for corner, moves in corner_moves.items()}
    

    def build_from_files(
        self,
        tar_paths: List[Path],
        min_freq: int = 5,
        top_k: int = 10000,
        first_n: int = 80,
        distance_threshold: int = 4,
        min_moves: int = 4,
        max_moves: int = 50,
        verbose: bool = True
    ) -> List[dict]:
        """
        从已下载的 tar 文件构建定式库（完整流程）
        
        Args:
            tar_paths: tar文件路径列表
            min_freq: 最小出现频率
            top_k: 入库定式数量上限
            first_n: 提取前N手
            distance_threshold: 连通块距离阈值
            min_moves: 最少手数
            max_moves: 最多手数
            verbose: 详细输出
        
        Returns:
            定式列表
        """
        # ===== Phase 1: CMS统计 + 临时文件存储 =====
        cms = CountMinSketch(width=4194304, depth=4)
        temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.gz', delete=False)
        temp_path = Path(temp_file.name)
        
        if verbose:
            print(f"📊 Phase 1: CMS统计前缀频率")
        
        config = {
            'first_n': first_n,
            'distance_threshold': distance_threshold,
            'min_moves': min_moves
        }
        
        processed = 0
        joseki_count = 0
        prefix_count = 0
        total_unique_sequences = 0
        
        with gzip.open(temp_path, 'wt', encoding='utf-8') as f_out:
            for tar_path in tar_paths:
                if verbose:
                    print(f"   处理: {tar_path.name}...")
                
                p, j, pref, uniq = self._extract_from_tar_to_temp(
                    tar_path, f_out, cms, config, verbose=False
                )
                processed += p
                joseki_count += j
                prefix_count += pref
                total_unique_sequences += uniq
                
                if verbose:
                    print(f"      累计: {processed}谱, {joseki_count}定式串, {prefix_count}前缀")
        
        if verbose:
            print(f"\n✅ Phase 1完成: {processed}谱, {joseki_count}定式串")
            print(f"   去重后着法串总数: {total_unique_sequences}")
        
        # ===== Phase 2-4: 逆向遍历 + 单链检测 + 去重 + 概率计算 =====
        joseki_list = self._build_from_cms_and_temp(
            temp_path, cms, min_freq, top_k, min_moves, max_moves,
            total_unique_sequences, verbose
        )
        
        # 清理临时文件
        temp_path.unlink()
        
        return joseki_list
    
    def _extract_from_tar_to_temp(
        self,
        tar_path: Path,
        temp_f_out,
        cms: CountMinSketch,
        config: dict,
        verbose: bool = False
    ) -> tuple:
        """从单个tar文件提取四角着法到temp文件，同时更新CMS
        
        这是一个可复用的核心函数，供自定义构建和自动构建共用。
        
        Args:
            tar_path: tar文件路径
            temp_f_out: 临时文件写入句柄（gzip.open后的文件对象）
            cms: CountMinSketch实例
            config: 配置字典，包含 first_n, distance_threshold, min_moves
            verbose: 是否打印进度
            
        Returns:
            (processed_sgf, joseki_count, prefix_count, unique_sequences)
        """
        first_n = config.get('first_n', 80)
        distance_threshold = config.get('distance_threshold', 4)
        min_moves = config.get('min_moves', 4)
        
        processed = 0
        joseki_count = 0
        prefix_count = 0
        total_unique_sequences = 0
        
        for sgf_data in iter_sgf_from_tar(str(tar_path)):
            try:
                corner_moves_dict = extract_moves_all_corners(
                    sgf_data, first_n=first_n, distance_threshold=distance_threshold
                )
                
                seen_sequences = set()
                
                for corner in CORNERS:
                    moves = corner_moves_dict.get(corner)
                    if not moves or len(moves) < min_moves:
                        continue
                    
                    coords = get_move_sequence(moves)
                    if len(coords) < min_moves:
                        continue
                    
                    # 检查该角9路范围内是否有棋子（转换前判断）
                    from ..core.coords import has_stone_in_corner_9lu
                    if not has_stone_in_corner_9lu(coords, corner):
                        continue  # 该角9路无棋子，跳过
                    
                    tr_coords = convert_to_top_right(coords, corner)
                    
                    # 标准化：统一到对角线上方（靠近上边缘）
                    from ..core.coords import normalize_corner_sequence
                    std_coords, _ = normalize_corner_sequence(tr_coords)
                    seq = " ".join(std_coords)
                    
                    if seq in seen_sequences:
                        continue
                    seen_sequences.add(seq)
                    
                    temp_f_out.write(f"std|{seq}\n")
                    joseki_count += 1
                    
                    seq_parts = seq.split()
                    for end in range(min_moves, len(seq_parts) + 1):
                        prefix = " ".join(seq_parts[:end])
                        cms.update(prefix)
                        prefix_count += 1
                
                total_unique_sequences += len(seen_sequences)
                processed += 1
                
            except Exception:
                continue
            
            if verbose and processed % 1000 == 0:
                print(f"\r  已处理: {processed}谱", end='', flush=True)
        
        if verbose:
            print(f"\r  完成: {processed}谱, {joseki_count}定式串, {prefix_count}前缀")
        
        return processed, joseki_count, prefix_count, total_unique_sequences
    
    def _iter_temp_files(self, temp_paths):
        """流式迭代多个temp文件的内容
        
        Args:
            temp_paths: temp文件路径列表
            
        Yields:
            每行的内容 (str)
        """
        for temp_path in temp_paths:
            with gzip.open(temp_path, 'rt', encoding='utf-8') as f_in:
                for line in f_in:
                    yield line
    
    def _build_from_cms_and_temp(
        self, temp_source, cms, min_freq: int, top_k: int,
        min_moves: int, max_moves: int, total_sequences: int, verbose: bool
    ) -> List[dict]:
        """从CMS和临时文件构建定式（Phase 2-4）
        
        Args:
            temp_source: 单个Path或List[Path]（支持多文件流式读取）
        """
        import heapq
        from datetime import datetime
        
        if verbose:
            print(f"🔄 Phase 2: 逆向遍历+单链检测，选取top-{top_k}...")
        
        heap = []
        seen_hashes = {}
        SINGLE_CHAIN_THRESHOLD = 0.05
        
        processed_seq = 0
        prefix_processed = 0
        skipped_single_chain = 0
        
        # 根据temp_source类型选择迭代方式
        if isinstance(temp_source, list):
            line_iter = self._iter_temp_files(temp_source)
        else:
            line_iter = gzip.open(temp_source, 'rt', encoding='utf-8')
        
        try:
            for line in line_iter:
                line = line.strip()
                if not line or '|' not in line:
                    continue
                
                direction, joseki_str = line.split('|', 1)
                seq_parts = joseki_str.split()
                
                if len(seq_parts) < min_moves:
                    continue
                
                last_count = float('inf')
                
                for end in range(len(seq_parts), min_moves - 1, -1):
                    prefix_parts = seq_parts[:end]
                    prefix = " ".join(prefix_parts)
                    est_count = cms.estimate(prefix)
                    
                    if est_count < min_freq:
                        last_count = est_count
                        continue
                    
                    prefix_hash = tuple(prefix_parts)
                    
                    if last_count != float('inf'):
                        count_diff_ratio = abs(est_count - last_count) / max(est_count, last_count, 1)
                        if count_diff_ratio < SINGLE_CHAIN_THRESHOLD:
                            skipped_single_chain += 1
                            last_count = est_count
                            continue
                    
                    last_count = est_count
                    
                    if prefix_hash in seen_hashes:
                        break
                    
                    if len(heap) < top_k:
                        item = HeapItem(est_count, prefix, direction, prefix_hash)
                        heapq.heappush(heap, item)
                        seen_hashes[prefix_hash] = True
                        prefix_processed += 1
                    elif est_count > heap[0].count:
                        old_item = heapq.heapreplace(heap, HeapItem(est_count, prefix, direction, prefix_hash))
                        del seen_hashes[old_item.prefix_hash]
                        seen_hashes[prefix_hash] = True
                        prefix_processed += 1
                
                processed_seq += 1
                if verbose and processed_seq % 10000 == 0:
                    print(f"\r  处理: {processed_seq}定式/{prefix_processed}前缀, "
                          f"堆大小: {len(heap)}, 单链跳过: {skipped_single_chain}", 
                          end='', flush=True)
        finally:
            # 如果是单文件模式，需要关闭文件
            if not isinstance(temp_source, list) and hasattr(line_iter, 'close'):
                line_iter.close()
        
        if verbose:
            print(f"\n  堆中候选: {len(heap)} 个, 单链跳过: {skipped_single_chain} 个")
        
        # Phase 3: 排序（去重已不需要，因为已标准化）
        if verbose:
            print("🔄 Phase 3: 排序...")
        
        candidates = []
        for item in heap:
            move_str = item.prefix
            if len(move_str.split()) > max_moves:
                continue
            candidates.append({
                'moves': move_str.split(),
                'count': item.count,
            })
        
        if verbose:
            print(f"  候选定式: {len(candidates)}")
        
        # Phase 4: 转换为定式格式
        total_seq = max(total_sequences, 1)
        joseki_list = []
        for i, cand in enumerate(candidates):
            joseki = {
                "id": f"kj_{i+1:05d}",
                "source": "katago",
                "moves": cand['moves'],
                "frequency": cand['count'],
                "probability": round(cand['count'] / total_seq, 6),
                "created_at": datetime.now().isoformat()
            }
            joseki_list.append(joseki)
        
        if verbose:
            print(f"✅ 构建完成: {len(joseki_list)} 条定式")
        
        return joseki_list

    def build_from_tar(self, 
                       tar_path: str,
                       min_freq: int = 5,
                       top_k: int = 10000,
                       first_n: int = 80,
                       distance_threshold: int = 4,
                       min_moves: int = 4,
                       max_moves: int = 50,
                       verbose: bool = True) -> List[dict]:
        """从单个 tar 文件构建定式库（便捷方法）"""
        return self.build_from_files(
            [Path(tar_path)],
            min_freq=min_freq,
            top_k=top_k,
            first_n=first_n,
            distance_threshold=distance_threshold,
            min_moves=min_moves,
            max_moves=max_moves,
            verbose=verbose
        )
    
    
    def save_to_db(self, joseki_list: List[dict], append: bool = False):
        """批量保存定式列表到数据库（优化版）"""
        if not append:
            self.storage._data["joseki_list"] = []
        
        # 批量添加到内存，最后统一写入
        self.storage._data["joseki_list"].extend(joseki_list)
        self.storage._save()
        
        print(f"已保存 {len(joseki_list)} 条定式到 {self.storage.db_path}")


def build_katago_joseki_db(
    tar_path: str,
    db_path: Optional[str] = None,
    min_freq: int = 5,
    top_k: int = 10000,
    first_n: int = 80,
    distance_threshold: int = 4,
    min_moves: int = 4,
    max_moves: int = 50
) -> int:
    """便捷函数：从KataGo棋谱构建定式库"""
    builder = KatagoJosekiBuilder(db_path)
    
    joseki_list = builder.build_from_tar(
        tar_path=tar_path,
        min_freq=min_freq,
        top_k=top_k,
        first_n=first_n,
        distance_threshold=distance_threshold,
        min_moves=min_moves,
        max_moves=max_moves
    )
    
    builder.save_to_db(joseki_list, append=False)
    return len(joseki_list)


# ========== 自动增量构建方法 ==========

def _ensure_auto_dirs(auto_dir: Path):
    """确保自动构建目录存在"""
    (auto_dir / "temp").mkdir(parents=True, exist_ok=True)


class KatagoJosekiBuilderAutoMixin:
    """自动构建功能混入类（简化版）
    
    核心思想：状态即文件系统，不依赖复杂的进度跟踪。
    通过多重继承或monkey patch方式添加到KatagoJosekiBuilder。
    """
    
    def run_auto(self, state, cache_dir: Path, limit: Optional[int] = None) -> Optional[List[dict]]:
        """自动增量构建主入口（批量保存优化版）
        
        优化：每30天保存一次CMS，减少写入次数
        
        Args:
            state: 状态管理器（只使用config）
            cache_dir: tar文件缓存目录
            limit: 限制处理的tar文件数量（用于测试）
            
        Returns:
            重建后的定式列表
        """
        from ..auto import AutoState, get_adaptive_cms_config
        
        print("=" * 60)
        print("🚀 Katago 自动增量构建")
        print("=" * 60)
        
        # 确保目录存在
        _ensure_auto_dirs(state.auto_dir)
        
        # 获取所有tar文件（按日期升序）
        tar_files = sorted(cache_dir.glob("*rating.tar.bz2"))
        
        if not tar_files:
            print("⚠️  缓存目录中没有tar文件")
            return None
        
        # 检查断点（读取cms文件的修改时间）
        cms_path = state.auto_dir / "cms.pkl"
        last_date = None
        if cms_path.exists():
            mtime = cms_path.stat().st_mtime
            last_date = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
            print(f"📍 断点恢复：上次处理到 {last_date}")
        
        # 过滤tar文件（从断点下一个开始）
        if last_date:
            tar_files = [f for f in tar_files 
                         if f.name.replace("rating.tar.bz2", "") > last_date]
            if not tar_files:
                print("✅ 所有日期已处理，无需增量")
        
        # 限制处理数量（用于测试）
        if limit is not None and limit > 0:
            tar_files = tar_files[:limit]
            print(f"🧪 测试模式：限制处理前 {limit} 个tar文件")
        
        # 加载或创建CMS
        cms_config = get_adaptive_cms_config(state.config.get('global_top_k', 100000) * 20)
        if cms_path.exists():
            cms = CountMinSketch.load_from_file(cms_path)
            print(f"📊 加载CMS: width={cms.width}, depth={cms.depth}")
        else:
            cms = CountMinSketch(width=cms_config['width'], depth=cms_config['depth'])
            print(f"📊 创建CMS: width={cms.width}, depth={cms.depth}")
        
        config = {
            'first_n': state.config.get('first_n', 80),
            'distance_threshold': state.config.get('distance_threshold', 4),
            'min_moves': state.config.get('min_moves', 4)
        }
        
        # 步骤1&2: 提取并批量更新CMS
        print("\n【步骤1/2】提取棋谱并更新CMS...")
        
        BATCH_SIZE = 30  # 每30天保存一次
        processed_count = 0
        batch_count = 0
        
        for idx, tar_path in enumerate(tar_files, 1):
            date_str = tar_path.name.replace("rating.tar.bz2", "")
            temp_path = state.auto_dir / "temp" / f"{date_str}.txt.gz"
            
            # 如果temp已存在且有效，跳过（已处理过）
            if temp_path.exists() and temp_path.stat().st_size > 100:
                continue
            
            print(f"   处理: {date_str}...")
            
            # 提取到temp，同时更新CMS（直接传入真正的cms，避免二次遍历）
            with gzip.open(temp_path, 'wt', encoding='utf-8') as f_out:
                processed, joseki_count, prefix_count, _ = self._extract_from_tar_to_temp(
                    tar_path, f_out, cms, config, verbose=False
                )
            
            if processed == 0:
                print(f"      ⚠️  未提取到有效棋谱")
                continue
            
            processed_count += 1
            print(f"      ✅ 提取: {processed}谱, {joseki_count}定式串, {prefix_count}前缀")
            
            # 每30天或最后一个保存一次
            if processed_count % BATCH_SIZE == 0 or idx == len(tar_files):
                cms.save_to_file(cms_path)
                # 更新mtime为当前处理日期（断点记录）
                timestamp = datetime.strptime(date_str, "%Y-%m-%d").timestamp()
                os.utime(cms_path, (timestamp, timestamp))
                batch_count += 1
                print(f"      💾 批次 {batch_count} 保存完成（{min(BATCH_SIZE, processed_count % BATCH_SIZE or BATCH_SIZE)}天）")
        
        if processed_count == 0:
            print("   ℹ️  没有新的棋谱需要处理")
        else:
            print(f"   ✅ 共处理 {processed_count} 个新日期，保存 {batch_count} 次")
        
        # 步骤3: 重建
        print("\n【步骤3】重建定式库...")
        return self._auto_rebuild(state, cms, config)
    
    def _auto_rebuild(self, state, cms: CountMinSketch, config: dict) -> List[dict]:
        """步骤3: 重建定式库"""
        print("🔄 重建定式库...")
        
        # 收集所有temp文件
        temp_dir = state.auto_dir / "temp"
        temp_files = sorted(temp_dir.glob("*.txt.gz"))
        
        if not temp_files:
            print("⚠️  没有可用的temp文件")
            return []
        
        print(f"   共 {len(temp_files)} 个temp文件")
        
        # 估算总序列数
        total_sequences = sum(1 for _ in self._iter_temp_files(temp_files)) // 2
        
        # 调用构建函数
        joseki_list = self._build_from_cms_and_temp(
            temp_files,
            cms,
            min_freq=state.config.get('min_freq', 5),
            top_k=state.config.get('global_top_k', 10000),
            min_moves=state.config.get('min_moves', 4),
            max_moves=state.config.get('max_moves', 50),
            total_sequences=max(total_sequences, 1),
            verbose=True
        )
        
        # 整库替换
        self.save_to_db(joseki_list, append=False)
        
        print(f"✅ 重建完成，共 {len(joseki_list)} 条定式")
        return joseki_list


# 将自动构建方法混入KatagoJosekiBuilder
KatagoJosekiBuilder.run_auto = KatagoJosekiBuilderAutoMixin.run_auto
KatagoJosekiBuilder._auto_rebuild = KatagoJosekiBuilderAutoMixin._auto_rebuild
