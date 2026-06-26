#!/usr/bin/env python3
"""
白板手绘动画生成器
输入一张彩色图片，生成包含线稿绘制和上色两个阶段的白板手绘动画视频。
"""
import argparse
import os
import sys
import math
import time
import datetime
import cv2
import numpy as np
from pathlib import Path

# === 素材路径（相对于脚本位置） ===
_SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
_ASSETS_DIR = _SCRIPT_DIR.parent / "assets"
HAND_PATH = str(_ASSETS_DIR / "drawing-hand.png")

# === 固定算法参数 ===
FRAME_RATE = 60  # 输出视频帧率；越高越流畅，文件体积和生成帧数也会增加
SPLIT_LEN = 10  # 网格切分边长（像素）；越小绘制越细，计算量越大
MAX_1080P = True  # 是否将输入图最长边限制到 1080 像素，保证输出分辨率可控
DEFAULT_TOTAL_DURATION_SECONDS = 10  # 未传 --duration 时的视频默认总时长（秒）
HOLD_PHASE_DURATION_SECONDS = 3  # 停留阶段基准时长（秒）；实际可能会加上 0~2ms 的余数补偿
SKETCH_PHASE_WEIGHT = 2  # 手绘阶段时长权重；和 COLOR_PHASE_WEIGHT 一起决定动画阶段分配比例
COLOR_PHASE_WEIGHT = 1  # 上色阶段时长权重；例如 2:1 表示手绘占 2/3、上色占 1/3
COLOR_BRUSH_RADIUS = 50  # 上色笔刷半径（像素）；越大上色越快、覆盖边缘越柔和
SKIP_RATE = 4  # 每帧推进的网格步数基准；越大绘制越快，但运动更跳跃
BACKGROUND_HEX = "#F6F1E3"  # 背景画布颜色
HAND_TARGET_HT = 493  # 手部素材缩放后的目标高度（像素），基于 1080p 画布调优
BLACK_PIXEL_THRESHOLD = 10  # 判定为“黑色线稿像素”的阈值；越大越容易把深色算作线稿
ROW_GROUP_MAX_GAP = 1  # 行分组时允许的最大空行间隔；越大越容易把相邻块合并
BLOCK_SPAN_MAX_GAP = 1  # 布局块跨度合并时允许的最大空列/空行间隔
BLOCK_SUB_BAND_ROWS = 3  # 结构化块内部再切分时，每个子带默认包含的行数
TEXT_LIKE_MIN_HEIGHT = 3  # 判定为“文本样式块”的最小高度（网格行数）
TEXT_LIKE_MAX_HEIGHT = 12  # 判定为“文本样式块”的最大高度（网格行数）
TEXT_LIKE_MIN_ASPECT_RATIO = 2.2  # 判定为文本块的最小宽高比；越大越偏向横向文本
TEXT_LIKE_MIN_DENSITY = 0.5  # 判定为文本块的最小密度；越大越要求内容更连续
TEXT_SEGMENT_MIN_WIDTH = 3  # 文本块内单段最小宽度（网格列数）
TEXT_SEGMENT_MAX_WIDTH = 6  # 文本块内单段最大宽度（网格列数）
ORGANIC_MAX_ASPECT_RATIO = 2.0  # 判定为有机形状块的最大宽高比；过宽会更像结构化内容
ORGANIC_MIN_LARGEST_CC_RATIO = 0.90  # 最大连通域占比阈值；越高越要求主体轮廓更完整
ORGANIC_MAX_PROVISIONAL_BLOCKS = 3  # 有机形状预分块时允许的最大块数
ORGANIC_START_TOP_RATIO = 0.15  # 有机形状起笔偏顶部的比例，用于模拟更自然的下笔位置
ORGANIC_WIDE_START_TOP_RATIO = 0.25  # 横向较宽的有机形状起笔偏顶部比例
ORGANIC_WIDE_MIN_ASPECT_RATIO = 1.4  # 进入“宽有机形状”规则的最小宽高比
COMPONENT_PRIORITY_MIN_SIZE = 8  # 连通域优先级判断的最小尺寸（网格数）
COMPONENT_PRIORITY_MIN_RATIO = 0.03  # 连通域优先级判断的最小面积占比
STRUCTURED_SPAN_SUPPORT_COL_MARGIN = 2  # 结构化块判断列支撑时额外容忍的边缘列数
STRUCTURED_PRIMARY_SCORE_RATIO = 0.79  # 结构化块主路径得分阈值；越高越偏向主干优先
STRUCTURED_PRIMARY_SUPPORT_RATIO = 0.45  # 结构化块主路径支撑阈值；越高越要求附着内容更充分


# === 核心函数 ===


def _hex_to_rgb(hex_color):
    normalized = hex_color.lstrip("#")
    if len(normalized) != 6:
        raise ValueError(f"无效颜色值: {hex_color}")
    return tuple(int(normalized[index:index + 2], 16) for index in (0, 2, 4))


BACKGROUND_RGB = np.array(_hex_to_rgb(BACKGROUND_HEX), dtype=np.uint8)
BACKGROUND_BGR = BACKGROUND_RGB[::-1].copy()

def euc_dist(arr1, point):
    square_sub = (arr1 - point) ** 2
    return np.sqrt(np.sum(square_sub, axis=1))


def get_extreme_coordinates(mask):
    indices = np.where(mask > 0)
    x = indices[1]
    y = indices[0]
    topleft = (np.min(x), np.min(y))
    bottomright = (np.max(x), np.max(y))
    return topleft, bottomright


def preprocess_image(img, variables):
    img = cv2.resize(img, (variables["resize_wd"], variables["resize_ht"]))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_thresh = cv2.adaptiveThreshold(
        img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 10
    )
    variables["img_gray"] = img_gray
    variables["img_thresh"] = img_thresh
    variables["img"] = img
    return variables


def preprocess_hand_image(hand_path, variables):
    hand_rgba = cv2.imread(hand_path, cv2.IMREAD_UNCHANGED)
    if hand_rgba.shape[2] == 4:
        # 透明背景 PNG：直接从 alpha 通道提取蒙版
        hand_mask = hand_rgba[:, :, 3]
        hand = hand_rgba[:, :, :3]
    else:
        # 无 alpha 通道的回退：用白色背景检测
        hand = hand_rgba
        gray = cv2.cvtColor(hand, cv2.COLOR_BGR2GRAY)
        _, hand_mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    # 裁剪到有效区域
    top_left, bottom_right = get_extreme_coordinates(hand_mask)
    hand = hand[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    hand_mask = hand_mask[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    # 按高度缩放到固定目标尺寸，宽度等比跟随
    hand_scale = HAND_TARGET_HT / hand.shape[0]
    new_ht = HAND_TARGET_HT
    new_wd = max(1, int(hand.shape[1] * hand_scale))
    interp = cv2.INTER_AREA if hand_scale < 1 else cv2.INTER_LINEAR
    hand = cv2.resize(hand, (new_wd, new_ht), interpolation=interp)
    hand_mask = cv2.resize(hand_mask, (new_wd, new_ht), interpolation=interp)
    # 归一化蒙版到 0.0~1.0，保留半透明边缘的平滑过渡
    hand_mask = hand_mask.astype(np.float32) / 255.0
    hand_mask_inv = 1.0 - hand_mask
    # 预乘：蒙版外区域置黑
    hand_bg_ind = np.where(hand_mask == 0)
    hand[hand_bg_ind] = [0, 0, 0]
    hand_ht, hand_wd = hand.shape[0], hand.shape[1]
    variables["hand_ht"] = hand_ht
    variables["hand_wd"] = hand_wd
    variables["hand"] = hand
    variables["hand_mask"] = hand_mask
    variables["hand_mask_inv"] = hand_mask_inv
    return variables


def create_background_canvas(shape, dtype=np.uint8):
    canvas = np.zeros(shape, dtype=dtype)
    canvas[...] = BACKGROUND_BGR.astype(dtype, copy=False)
    return canvas


def compute_phase_frames(total_duration_ms, frame_rate=FRAME_RATE):
    """
    根据总时长计算三阶段帧数。

    停留阶段使用固定基准秒数；剩余时长按线稿/上色权重分配。
    若动画时长无法被权重和整除，则将余数补偿给停留阶段，避免比例分配丢精度。
    """
    phase_weight_total = SKETCH_PHASE_WEIGHT + COLOR_PHASE_WEIGHT
    hold_ms = HOLD_PHASE_DURATION_SECONDS * 1000
    anim_ms = total_duration_ms - hold_ms
    remainder = anim_ms % phase_weight_total
    if remainder != 0:
        anim_ms -= remainder
        hold_ms += remainder

    hold_frames = round(hold_ms * frame_rate / 1000)
    sketch_frames = round(
        anim_ms * SKETCH_PHASE_WEIGHT / phase_weight_total * frame_rate / 1000
    )
    color_frames = round(
        anim_ms * COLOR_PHASE_WEIGHT / phase_weight_total * frame_rate / 1000
    )
    if sketch_frames <= 0 and color_frames <= 0:
        sketch_frames = 0
        color_frames = 0

    return {
        "hold_ms": hold_ms,
        "anim_ms": anim_ms,
        "hold_frames": hold_frames,
        "sketch_frames": sketch_frames,
        "color_frames": color_frames,
        "phase_ratio_label": f"{SKETCH_PHASE_WEIGHT}:{COLOR_PHASE_WEIGHT}",
    }


def draw_hand_on_img(drawing, hand, x, y, hand_mask, hand_mask_inv, hand_ht, hand_wd, img_ht, img_wd):
    remaining_ht = img_ht - y
    remaining_wd = img_wd - x
    crop_hand_ht = min(remaining_ht, hand_ht)
    crop_hand_wd = min(remaining_wd, hand_wd)
    if crop_hand_ht <= 0 or crop_hand_wd <= 0:
        return drawing
    hand_cropped = hand[:crop_hand_ht, :crop_hand_wd]
    hand_mask_cropped = hand_mask[:crop_hand_ht, :crop_hand_wd]
    hand_mask_inv_cropped = hand_mask_inv[:crop_hand_ht, :crop_hand_wd]
    for c in range(3):
        drawing[y:y + crop_hand_ht, x:x + crop_hand_wd, c] = (
            drawing[y:y + crop_hand_ht, x:x + crop_hand_wd, c] * hand_mask_inv_cropped
            + hand_cropped[:, :, c] * hand_mask_cropped
        )
    return drawing


def split_image_into_cells(img, split_len):
    img = np.ascontiguousarray(img)
    img_ht, img_wd = img.shape[:2]
    if img_ht % split_len != 0 or img_wd % split_len != 0:
        raise ValueError("图像尺寸必须是 split_len 的整数倍")

    n_rows = img_ht // split_len
    n_cols = img_wd // split_len
    if img.ndim == 2:
        return img.reshape(n_rows, split_len, n_cols, split_len).transpose(0, 2, 1, 3)
    return img.reshape(n_rows, split_len, n_cols, split_len, img.shape[2]).transpose(0, 2, 1, 3, 4)


def extract_active_grid(img_thresh, split_len, grid_of_cuts=None):
    if grid_of_cuts is None:
        grid_of_cuts = split_image_into_cells(img_thresh, split_len)
    active_grid = np.any(grid_of_cuts < BLACK_PIXEL_THRESHOLD, axis=(2, 3))
    active_cells = [tuple(int(v) for v in cell) for cell in np.argwhere(active_grid)]
    return active_grid, active_cells


def _merge_sorted_indices(indices, max_gap):
    if len(indices) == 0:
        return []

    spans = []
    start = int(indices[0])
    end = int(indices[0])
    for idx in indices[1:]:
        idx = int(idx)
        if idx - end <= max_gap + 1:
            end = idx
        else:
            spans.append((start, end))
            start = idx
            end = idx
    spans.append((start, end))
    return spans


def _span_center(span):
    return (span[0] + span[1]) / 2.0


def _assign_index_to_spans(index, spans, between_policy="nearest"):
    if not spans:
        raise ValueError("spans 不能为空")

    for span_index, (start, end) in enumerate(spans):
        if start <= index <= end:
            return span_index

    if index < spans[0][0] or index > spans[-1][1]:
        distances = [abs(index - _span_center(span)) for span in spans]
        return int(np.argmin(distances))

    for span_index in range(len(spans) - 1):
        left_span = spans[span_index]
        right_span = spans[span_index + 1]
        if left_span[1] < index < right_span[0]:
            if between_policy == "previous":
                return span_index
            if between_policy == "left":
                return span_index

            left_distance = abs(index - _span_center(left_span))
            right_distance = abs(index - _span_center(right_span))
            if left_distance <= right_distance:
                return span_index
            return span_index + 1

    return len(spans) - 1


def _nearest_neighbor_order(cells, seed_cell):
    if not cells:
        return []

    remaining = [tuple(cell) for cell in cells]
    seed_cell = tuple(seed_cell)
    if seed_cell not in remaining:
        raise ValueError("seed_cell 必须在 cells 中")

    ordered = [seed_cell]
    remaining.remove(seed_cell)
    current = seed_cell
    while remaining:
        remaining_arr = np.array(remaining, dtype=np.int32)
        next_index = int(np.argmin(euc_dist(remaining_arr, np.array(current, dtype=np.int32))))
        current = remaining.pop(next_index)
        ordered.append(current)
    return ordered


def _get_cell_bounds(cells):
    rows = [cell[0] for cell in cells]
    cols = [cell[1] for cell in cells]
    return min(rows), max(rows), min(cols), max(cols)


def _looks_like_text_block(cells):
    if not cells:
        return False

    top_row, bottom_row, left_col, right_col = _get_cell_bounds(cells)
    block_height = bottom_row - top_row + 1
    block_width = right_col - left_col + 1
    if block_height < TEXT_LIKE_MIN_HEIGHT or block_height > TEXT_LIKE_MAX_HEIGHT:
        return False

    aspect_ratio = block_width / max(1, block_height)
    density = len(cells) / max(1, block_height * block_width)
    return (
        aspect_ratio >= TEXT_LIKE_MIN_ASPECT_RATIO
        and density >= TEXT_LIKE_MIN_DENSITY
    )


def _build_local_mask(cells):
    top_row, bottom_row, left_col, right_col = _get_cell_bounds(cells)
    mask = np.zeros(
        (bottom_row - top_row + 1, right_col - left_col + 1), dtype=np.uint8
    )
    for row, col in cells:
        mask[row - top_row, col - left_col] = 1
    return mask


def _largest_connected_component_ratio(cells):
    if not cells:
        return 0.0

    components = _get_connected_components(cells)
    if not components:
        return 0.0
    return components[0]["size"] / len(cells)


def _get_connected_components(cells):
    if not cells:
        return []

    top_row, bottom_row, left_col, right_col = _get_cell_bounds(cells)
    mask = _build_local_mask(cells)
    n_labels, labels = cv2.connectedComponents(mask, connectivity=8)
    components = []
    for label in range(1, n_labels):
        positions = np.argwhere(labels == label)
        component_cells = [
            (int(row + top_row), int(col + left_col))
            for row, col in positions
        ]
        component_rows = [cell[0] for cell in component_cells]
        component_cols = [cell[1] for cell in component_cells]
        components.append({
            "label": label,
            "size": len(component_cells),
            "cells": sorted(component_cells, key=lambda cell: (cell[0], cell[1])),
            "top": min(component_rows),
            "bottom": max(component_rows),
            "left": min(component_cols),
            "right": max(component_cols),
            "center_row": float(np.mean(component_rows)),
            "center_col": float(np.mean(component_cols)),
        })

    components.sort(
        key=lambda component: (
            -component["size"],
            component["top"],
            component["left"],
        )
    )
    return components


def _split_component_priority_buckets(cells):
    components = _get_connected_components(cells)
    if not components:
        return [], []

    priority_threshold = max(
        COMPONENT_PRIORITY_MIN_SIZE,
        math.ceil(len(cells) * COMPONENT_PRIORITY_MIN_RATIO),
    )
    priority_components = [
        component for component in components
        if component["size"] >= priority_threshold
    ]
    deferred_components = [
        component for component in components
        if component["size"] < priority_threshold
    ]

    if not priority_components:
        priority_components = [components[0]]
        deferred_components = components[1:]

    return priority_components, deferred_components


def _flatten_components(components):
    return [
        tuple(cell)
        for component in components
        for cell in component["cells"]
    ]


def _build_provisional_blocks(cells, n_cols, group_height):
    if not cells:
        return []

    col_counts = np.zeros(n_cols, dtype=np.int32)
    for _, col in cells:
        col_counts[col] += 1

    major_col_threshold = max(2, math.ceil(group_height * 0.15))
    major_cols = np.where(col_counts >= major_col_threshold)[0]
    block_spans = _merge_sorted_indices(major_cols, BLOCK_SPAN_MAX_GAP)
    if not block_spans:
        block_spans = [(min(cell[1] for cell in cells), max(cell[1] for cell in cells))]

    raw_blocks = []
    for block_index, block_span in enumerate(block_spans):
        raw_blocks.append({
            "block_index": block_index,
            "anchor_span": block_span,
            "cells": [],
        })

    for cell in cells:
        block_index = _assign_index_to_spans(
            cell[1], block_spans, between_policy="left"
        )
        raw_blocks[block_index]["cells"].append(cell)

    return [block for block in raw_blocks if block["cells"]]


def _classify_row_group(cells, n_cols):
    top_row, bottom_row, left_col, right_col = _get_cell_bounds(cells)
    group_height = bottom_row - top_row + 1
    group_width = right_col - left_col + 1
    aspect_ratio = group_width / max(1, group_height)
    group_density = len(cells) / max(1, group_height * group_width)
    largest_cc_ratio = _largest_connected_component_ratio(cells)
    provisional_blocks = _build_provisional_blocks(cells, n_cols, group_height)
    provisional_block_count = len(provisional_blocks)

    if _looks_like_text_block(cells):
        return {
            "group_strategy": "text_like",
            "aspect_ratio": aspect_ratio,
            "group_density": group_density,
            "largest_cc_ratio": largest_cc_ratio,
            "provisional_blocks": provisional_blocks,
            "provisional_block_count": provisional_block_count,
        }

    if (
        aspect_ratio <= ORGANIC_MAX_ASPECT_RATIO
        and largest_cc_ratio >= ORGANIC_MIN_LARGEST_CC_RATIO
        and provisional_block_count <= ORGANIC_MAX_PROVISIONAL_BLOCKS
        and not (
            provisional_block_count == 1
            and group_density >= 0.90
        )
    ):
        return {
            "group_strategy": "organic_like",
            "aspect_ratio": aspect_ratio,
            "group_density": group_density,
            "largest_cc_ratio": largest_cc_ratio,
            "provisional_blocks": provisional_blocks,
            "provisional_block_count": provisional_block_count,
        }

    return {
        "group_strategy": "structured_like",
        "aspect_ratio": aspect_ratio,
        "group_density": group_density,
        "largest_cc_ratio": largest_cc_ratio,
        "provisional_blocks": provisional_blocks,
        "provisional_block_count": provisional_block_count,
    }


def _build_text_like_draw_order(cells):
    if not cells:
        return []

    _, bottom_row, left_col, right_col = _get_cell_bounds(cells)
    block_height = bottom_row - min(cell[0] for cell in cells) + 1
    segment_width = max(
        TEXT_SEGMENT_MIN_WIDTH,
        min(TEXT_SEGMENT_MAX_WIDTH, block_height),
    )
    normalized_cells = [tuple(cell) for cell in cells]
    ordered_cells = []
    active_cols = sorted({cell[1] for cell in normalized_cells})
    coarse_spans = _merge_sorted_indices(active_cols, BLOCK_SPAN_MAX_GAP)
    if not coarse_spans:
        coarse_spans = [(left_col, right_col)]

    for coarse_start, coarse_end in coarse_spans:
        span_start = coarse_start
        while span_start <= coarse_end:
            span_end = min(span_start + segment_width - 1, coarse_end)
            span_cells = [
                cell for cell in normalized_cells
                if span_start <= cell[1] <= span_end
            ]
            if span_cells:
                span_cells.sort(key=lambda cell: (cell[0], cell[1]))
                ordered_cells.extend(_nearest_neighbor_order(span_cells, span_cells[0]))
            span_start = span_end + 1

    return ordered_cells


def _nearest_cell_to_point(cells, point):
    if point is None:
        return min(cells, key=lambda cell: (cell[0], cell[1]))

    point_arr = np.array(point, dtype=np.int32)
    return min(
        cells,
        key=lambda cell: (
            np.sum((np.array(cell, dtype=np.int32) - point_arr) ** 2),
            cell[0],
            cell[1],
        ),
    )


def _order_spans_by_proximity(spans, start_index):
    if not spans:
        return []

    remaining = list(range(len(spans)))
    ordered_indices = [start_index]
    remaining.remove(start_index)
    current_index = start_index

    while remaining:
        current_center = _span_center(spans[current_index])
        next_index = min(
            remaining,
            key=lambda index: (
                abs(_span_center(spans[index]) - current_center),
                spans[index][0],
                spans[index][1],
            ),
        )
        ordered_indices.append(next_index)
        remaining.remove(next_index)
        current_index = next_index

    return ordered_indices


def _count_structured_future_support(cells, band_end, span, col_margin=STRUCTURED_SPAN_SUPPORT_COL_MARGIN):
    col_start, col_end = span
    return sum(
        1
        for row, col in cells
        if row > band_end and (col_start - col_margin) <= col <= (col_end + col_margin)
    )


def _build_structured_band_infos(cells, band_rows=BLOCK_SUB_BAND_ROWS):
    if not cells:
        return []

    top_row = min(cell[0] for cell in cells)
    bottom_row = max(cell[0] for cell in cells)
    normalized_cells = [tuple(cell) for cell in cells]
    block_left = min(cell[1] for cell in normalized_cells)
    block_right = max(cell[1] for cell in normalized_cells)
    block_half_width = max(1.0, (block_right - block_left + 1) / 2.0)
    block_center_col = float(np.mean([cell[1] for cell in normalized_cells]))
    local_density_scores = _build_local_density_scores(normalized_cells)
    components = _get_connected_components(normalized_cells)
    total_cells = max(1, len(normalized_cells))
    component_ratio_by_cell = {
        tuple(cell): component["size"] / total_cells
        for component in components
        for cell in component["cells"]
    }
    band_infos = []
    band_index = 0

    for band_start in range(top_row, bottom_row + 1, band_rows):
        band_end = band_start + band_rows - 1
        band_cells = [
            cell for cell in normalized_cells
            if band_start <= cell[0] <= band_end
        ]
        if not band_cells:
            continue

        band_cols = sorted({cell[1] for cell in band_cells})
        col_spans = _merge_sorted_indices(band_cols, BLOCK_SPAN_MAX_GAP)
        if not col_spans:
            continue

        span_infos = []
        for col_start, col_end in col_spans:
            span_cells = [
                cell for cell in band_cells
                if col_start <= cell[1] <= col_end
            ]
            span_center = _span_center((col_start, col_end))
            span_infos.append({
                "span": (col_start, col_end),
                "cells": span_cells,
                "cell_count": len(span_cells),
                "mean_density": float(np.mean([local_density_scores[cell] for cell in span_cells])),
                "component_ratio": max(
                    component_ratio_by_cell.get(cell, 0.0) for cell in span_cells
                ),
                "future_support": _count_structured_future_support(
                    normalized_cells, band_end, (col_start, col_end)
                ),
                "centrality": max(
                    0.0,
                    1.0 - abs(span_center - block_center_col) / block_half_width,
                ),
            })

        if len(span_infos) <= 2:
            for span_info in span_infos:
                span_info["is_primary"] = True
                span_info["score"] = 1.0
        else:
            max_cell_count = max(span_info["cell_count"] for span_info in span_infos)
            max_density = max(span_info["mean_density"] for span_info in span_infos)
            max_future_support = max(span_info["future_support"] for span_info in span_infos)
            max_component_ratio = max(span_info["component_ratio"] for span_info in span_infos)

            for span_info in span_infos:
                size_ratio = span_info["cell_count"] / max(1, max_cell_count)
                density_ratio = span_info["mean_density"] / max(1.0, max_density)
                support_ratio = (
                    span_info["future_support"] / max(1, max_future_support)
                    if max_future_support > 0 else 0.0
                )
                component_ratio = (
                    span_info["component_ratio"] / max(1e-6, max_component_ratio)
                    if max_component_ratio > 0 else 0.0
                )
                span_info["score"] = (
                    1.2 * size_ratio
                    + 1.2 * support_ratio
                    + 0.6 * density_ratio
                    + 0.4 * component_ratio
                    + 0.2 * span_info["centrality"]
                )
                span_info["size_ratio"] = size_ratio
                span_info["support_ratio"] = support_ratio

            max_score = max(span_info["score"] for span_info in span_infos)
            for span_info in span_infos:
                span_info["is_primary"] = (
                    span_info["score"] >= max_score * STRUCTURED_PRIMARY_SCORE_RATIO
                    or span_info["support_ratio"] >= STRUCTURED_PRIMARY_SUPPORT_RATIO
                )

            if not any(span_info["is_primary"] for span_info in span_infos):
                best_span = max(
                    span_infos,
                    key=lambda span_info: (
                        span_info["score"],
                        span_info["cell_count"],
                        span_info["span"][0],
                    ),
                )
                best_span["is_primary"] = True

        band_infos.append({
            "band_index": band_index,
            "band_start": band_start,
            "band_end": band_end,
            "spans": span_infos,
        })

        band_index += 1

    return band_infos


def _walk_structured_band_infos(band_infos, current_exit=None, primary_only=True):
    ordered_cells = []
    has_drawn_anything = current_exit is not None

    for band_info in band_infos:
        span_infos = [
            span_info for span_info in band_info["spans"]
            if span_info["is_primary"] == primary_only
        ]
        if not span_infos:
            continue

        spans = [span_info["span"] for span_info in span_infos]
        if not has_drawn_anything and primary_only:
            start_index = min(
                range(len(span_infos)),
                key=lambda index: (
                    span_infos[index]["span"][0],
                    -span_infos[index]["cell_count"],
                ),
            )
        else:
            start_index = min(
                range(len(span_infos)),
                key=lambda index: (
                    abs(_span_center(spans[index]) - current_exit[1]),
                    spans[index][0],
                ),
            )

        for span_index in _order_spans_by_proximity(spans, start_index):
            span_cells = span_infos[span_index]["cells"]
            seed_cell = _nearest_cell_to_point(span_cells, current_exit)
            span_order = _nearest_neighbor_order(span_cells, seed_cell)
            ordered_cells.extend(span_order)
            current_exit = span_order[-1]
            has_drawn_anything = True

    return ordered_cells, current_exit


def _build_structured_core_draw_order(cells, previous_exit=None, band_rows=BLOCK_SUB_BAND_ROWS):
    if not cells:
        return []

    band_infos = _build_structured_band_infos(cells, band_rows=band_rows)
    primary_order, current_exit = _walk_structured_band_infos(
        band_infos, current_exit=previous_exit, primary_only=True
    )
    secondary_order, _ = _walk_structured_band_infos(
        band_infos, current_exit=current_exit, primary_only=False
    )
    return primary_order + secondary_order


def _step_direction(start_cell, end_cell):
    delta_row = end_cell[0] - start_cell[0]
    delta_col = end_cell[1] - start_cell[1]
    row_dir = 0 if delta_row == 0 else (1 if delta_row > 0 else -1)
    col_dir = 0 if delta_col == 0 else (1 if delta_col > 0 else -1)
    return row_dir, col_dir


def _direction_change_score(previous_direction, candidate_direction):
    return (
        (candidate_direction[0] - previous_direction[0]) ** 2
        + (candidate_direction[1] - previous_direction[1]) ** 2
    )


def _build_cell_adjacency(cells):
    cell_set = {tuple(cell) for cell in cells}
    adjacency = {}
    for row, col in cell_set:
        neighbors = set()
        for delta_row in (-1, 0, 1):
            for delta_col in (-1, 0, 1):
                if delta_row == 0 and delta_col == 0:
                    continue
                neighbor = (row + delta_row, col + delta_col)
                if neighbor in cell_set:
                    neighbors.add(neighbor)
        adjacency[(row, col)] = neighbors
    return adjacency


def _build_local_density_scores(cells, radius=2):
    normalized_cells = [tuple(cell) for cell in cells]
    densities = {}
    for cell in normalized_cells:
        densities[cell] = sum(
            1
            for other in normalized_cells
            if max(abs(other[0] - cell[0]), abs(other[1] - cell[1])) <= radius
        )
    return densities


def _count_unvisited_neighbors(cell, adjacency, unvisited, current=None):
    return sum(
        1
        for neighbor in adjacency[cell]
        if neighbor in unvisited and neighbor != current
    )


def _count_frontier_support(cell, adjacency, unvisited, current=None, max_depth=2):
    visited = {cell}
    queue = [(cell, 0)]
    support = 0

    while queue:
        node, depth = queue.pop(0)
        if depth >= max_depth:
            continue

        for neighbor in adjacency[node]:
            if neighbor == current or neighbor in visited or neighbor not in unvisited:
                continue
            visited.add(neighbor)
            support += 1
            queue.append((neighbor, depth + 1))

    return support


def _order_components_by_transition(components, start_point):
    if not components:
        return []

    remaining = list(components)
    current_point = start_point
    ordered_components = []

    while remaining:
        next_component = min(
            remaining,
            key=lambda component: (
                min(
                    (cell[0] - current_point[0]) ** 2
                    + (cell[1] - current_point[1]) ** 2
                    for cell in component["cells"]
                ) if current_point is not None else 0,
                -component["size"],
                component["top"],
                component["left"],
            ),
        )
        ordered_components.append(next_component)
        remaining.remove(next_component)
        current_point = (
            next_component["center_row"],
            next_component["center_col"],
        )

    return ordered_components


def _build_structured_draw_order(cells, previous_exit=None, band_rows=BLOCK_SUB_BAND_ROWS):
    if not cells:
        return []

    priority_components, deferred_components = _split_component_priority_buckets(cells)
    priority_cells = _flatten_components(priority_components)
    ordered_cells = _build_structured_core_draw_order(
        priority_cells, previous_exit=previous_exit, band_rows=band_rows
    )
    current_exit = ordered_cells[-1] if ordered_cells else previous_exit
    for component in _order_components_by_transition(deferred_components, current_exit):
        seed_cell = _nearest_cell_to_point(component["cells"], current_exit)
        component_order = _nearest_neighbor_order(component["cells"], seed_cell)
        ordered_cells.extend(component_order)
        current_exit = component_order[-1]

    return ordered_cells


def _build_organic_core_draw_order(cells, seed_hint=None):
    if not cells:
        return []

    normalized_cells = sorted({tuple(cell) for cell in cells})
    adjacency = _build_cell_adjacency(normalized_cells)
    local_density_scores = _build_local_density_scores(normalized_cells)
    centroid_row = float(np.mean([cell[0] for cell in normalized_cells]))
    centroid_col = float(np.mean([cell[1] for cell in normalized_cells]))
    if seed_hint is None:
        top_row, bottom_row, left_col, right_col = _get_cell_bounds(normalized_cells)
        block_height = bottom_row - top_row + 1
        block_width = right_col - left_col + 1
        aspect_ratio = block_width / max(1, block_height)
        start_ratio = (
            ORGANIC_WIDE_START_TOP_RATIO
            if aspect_ratio >= ORGANIC_WIDE_MIN_ASPECT_RATIO
            else ORGANIC_START_TOP_RATIO
        )
        anchor_row = top_row + block_height * start_ratio
        horizontal_centroid = float(np.mean([cell[1] for cell in normalized_cells]))
        seed_cell = min(
            normalized_cells,
            key=lambda cell: (
                (cell[0] - anchor_row) ** 2
                + (cell[1] - horizontal_centroid) ** 2,
                cell[0],
                abs(cell[1] - horizontal_centroid),
                cell[1],
            ),
        )
    else:
        seed_cell = _nearest_cell_to_point(normalized_cells, seed_hint)

    unvisited = set(normalized_cells)
    ordered_cells = [seed_cell]
    unvisited.remove(seed_cell)
    current = seed_cell
    previous_direction = (1, 0)

    while unvisited:
        neighbor_candidates = [
            candidate for candidate in adjacency[current]
            if candidate in unvisited
        ]

        if neighbor_candidates:
            next_cell = min(
                neighbor_candidates,
                key=lambda cell: (
                    _count_unvisited_neighbors(
                        cell, adjacency, unvisited, current=current
                    ) <= 1,
                    -_count_frontier_support(
                        cell, adjacency, unvisited, current=current, max_depth=2
                    ),
                    -local_density_scores[cell],
                    (cell[0] - centroid_row) ** 2 + (cell[1] - centroid_col) ** 2,
                    _direction_change_score(
                        previous_direction, _step_direction(current, cell)
                    ),
                    abs(cell[0] - current[0]) + abs(cell[1] - current[1]) != 1,
                    cell[0],
                    abs(cell[1] - current[1]),
                    cell[1],
                ),
            )
        else:
            next_cell = min(
                unvisited,
                key=lambda cell: (
                    (cell[0] - current[0]) ** 2 + (cell[1] - current[1]) ** 2,
                    -local_density_scores[cell],
                    (cell[0] - centroid_row) ** 2 + (cell[1] - centroid_col) ** 2,
                    cell[0],
                    abs(cell[1] - current[1]),
                    cell[1],
                ),
            )

        previous_direction = _step_direction(current, next_cell)
        ordered_cells.append(next_cell)
        unvisited.remove(next_cell)
        current = next_cell

    return ordered_cells


def _build_organic_draw_order(cells):
    if not cells:
        return []

    priority_components, deferred_components = _split_component_priority_buckets(cells)
    priority_cells = _flatten_components(priority_components)
    ordered_cells = _build_organic_core_draw_order(priority_cells)
    current_exit = ordered_cells[-1] if ordered_cells else None
    for component in _order_components_by_transition(deferred_components, current_exit):
        component_order = _build_organic_core_draw_order(
            component["cells"], seed_hint=current_exit
        )
        ordered_cells.extend(component_order)
        current_exit = component_order[-1]

    return ordered_cells


def _build_layout_block(
    row_group_index,
    row_group_top,
    row_group_bottom,
    block_index,
    anchor_span,
    cells,
    group_strategy,
    path_strategy,
    draw_order,
):
    block_rows = [cell[0] for cell in cells]
    block_cols = [cell[1] for cell in cells]
    return {
        "row_group_index": row_group_index,
        "row_group_top": row_group_top,
        "row_group_bottom": row_group_bottom,
        "block_index": block_index,
        "anchor_span": anchor_span,
        "top": min(block_rows),
        "bottom": max(block_rows),
        "left": min(block_cols),
        "right": max(block_cols),
        "is_text_like": path_strategy == "text_segments",
        "group_strategy": group_strategy,
        "path_strategy": path_strategy,
        "cells": cells,
        "draw_order": draw_order,
    }


def build_layout_blocks(active_grid):
    active_cells = [tuple(int(v) for v in cell) for cell in np.argwhere(active_grid)]
    if not active_cells:
        return []

    n_rows, n_cols = active_grid.shape
    row_counts = np.sum(active_grid, axis=1)
    row_threshold = max(3, math.ceil(n_cols * 0.05))
    layout_active_rows = np.where(row_counts >= row_threshold)[0]
    row_spans = _merge_sorted_indices(layout_active_rows, ROW_GROUP_MAX_GAP)

    if not row_spans:
        non_empty_rows = np.where(row_counts > 0)[0]
        if len(non_empty_rows) == 0:
            return []
        row_spans = [(int(non_empty_rows[0]), int(non_empty_rows[-1]))]

    row_groups = []
    for row_group_index, row_span in enumerate(row_spans):
        row_groups.append({
            "row_group_index": row_group_index,
            "anchor_span": row_span,
            "cells": [],
        })

    for cell in active_cells:
        row_group_index = _assign_index_to_spans(
            cell[0], row_spans, between_policy="previous"
        )
        row_groups[row_group_index]["cells"].append(cell)

    ordered_blocks = []
    for row_group in row_groups:
        group_cells = sorted(row_group["cells"], key=lambda cell: (cell[0], cell[1]))
        if not group_cells:
            continue

        group_rows = [cell[0] for cell in group_cells]
        group_cols = [cell[1] for cell in group_cells]
        row_group_top = min(group_rows)
        row_group_bottom = max(group_rows)
        group_height = row_group_bottom - row_group_top + 1
        row_group_profile = _classify_row_group(group_cells, n_cols)
        group_strategy = row_group_profile["group_strategy"]

        if group_strategy == "text_like":
            ordered_blocks.append(
                _build_layout_block(
                    row_group_index=row_group["row_group_index"],
                    row_group_top=row_group_top,
                    row_group_bottom=row_group_bottom,
                    block_index=0,
                    anchor_span=(min(group_cols), max(group_cols)),
                    cells=group_cells,
                    group_strategy=group_strategy,
                    path_strategy="text_segments",
                    draw_order=_build_text_like_draw_order(group_cells),
                )
            )
            continue

        if group_strategy == "organic_like":
            ordered_blocks.append(
                _build_layout_block(
                    row_group_index=row_group["row_group_index"],
                    row_group_top=row_group_top,
                    row_group_bottom=row_group_bottom,
                    block_index=0,
                    anchor_span=(min(group_cols), max(group_cols)),
                    cells=group_cells,
                    group_strategy=group_strategy,
                    path_strategy="organic_walk",
                    draw_order=_build_organic_draw_order(group_cells),
                )
            )
            continue

        previous_exit = None
        for raw_block in row_group_profile["provisional_blocks"]:
            block_cells = sorted(raw_block["cells"], key=lambda cell: (cell[0], cell[1]))
            if not block_cells:
                continue

            if _looks_like_text_block(block_cells):
                path_strategy = "text_segments"
                draw_order = _build_text_like_draw_order(block_cells)
            else:
                path_strategy = "structured_bands"
                draw_order = _build_structured_draw_order(
                    block_cells, previous_exit=previous_exit
                )

            previous_exit = draw_order[-1] if draw_order else previous_exit
            ordered_blocks.append(
                _build_layout_block(
                    row_group_index=row_group["row_group_index"],
                    row_group_top=row_group_top,
                    row_group_bottom=row_group_bottom,
                    block_index=raw_block["block_index"],
                    anchor_span=raw_block["anchor_span"],
                    cells=block_cells,
                    group_strategy=group_strategy,
                    path_strategy=path_strategy,
                    draw_order=draw_order,
                )
            )

    return ordered_blocks


def build_draw_order(active_grid, layout_blocks=None):
    if layout_blocks is None:
        layout_blocks = build_layout_blocks(active_grid)

    ordered_cells = []
    for block in layout_blocks:
        ordered_cells.extend(block["draw_order"])
    return ordered_cells


def draw_masked_object(variables, target_cells, skip_rate=SKIP_RATE):
    split_len = variables["split_len"]
    resize_ht = variables["resize_ht"]
    resize_wd = variables["resize_wd"]
    draw_order = variables["draw_order"]
    active_grid = variables["active_grid"]
    grid_of_cuts = variables["grid_of_cuts"]

    actual_cells = len(draw_order)
    n_cuts_vertical, n_cuts_horizontal = active_grid.shape
    target_frames = target_cells // skip_rate if skip_rate > 0 else actual_cells
    print(
        f"  网格总数: {n_cuts_vertical}x{n_cuts_horizontal}, "
        f"有内容的格子: {actual_cells}, 目标帧: {target_frames}"
    )

    if actual_cells == 0:
        print("  无可绘制内容，跳过线稿阶段")
        return

    counter = 0
    frame_accumulator = 0.0
    frames_written = 0
    frame_ratio = target_frames / actual_cells if actual_cells > 0 else 1.0
    for row, col in draw_order:
        range_v_start = row * split_len
        range_v_end = range_v_start + split_len
        range_h_start = col * split_len
        range_h_end = range_h_start + split_len

        threshold_cell = grid_of_cuts[row, col]
        temp_drawing = np.repeat(threshold_cell[:, :, None], 3, axis=2)
        cell_region = variables["drawn_frame"][
            range_v_start:range_v_end, range_h_start:range_h_end
        ]
        ink_mask = threshold_cell < BLACK_PIXEL_THRESHOLD
        if np.any(ink_mask):
            cell_region[ink_mask] = temp_drawing[ink_mask]

        if variables["draw_hand"]:
            hand_coord_x = range_h_start + split_len // 2
            hand_coord_y = range_v_start + split_len // 2
            drawn_frame_with_hand = draw_hand_on_img(
                variables["drawn_frame"].copy(),
                variables["hand"].copy(),
                hand_coord_x,
                hand_coord_y,
                variables["hand_mask"].copy(),
                variables["hand_mask_inv"].copy(),
                variables["hand_ht"],
                variables["hand_wd"],
                resize_ht,
                resize_wd,
            )
        else:
            drawn_frame_with_hand = variables["drawn_frame"].copy()

        counter += 1
        frame_accumulator += frame_ratio
        n_frames = int(frame_accumulator) - frames_written
        if n_frames > 0:
            frame = drawn_frame_with_hand.astype(np.uint8)
            for _ in range(n_frames):
                variables["video_object"].write(frame)
            frames_written += n_frames

        if counter % 100 == 0:
            pct = int(counter / actual_cells * 100)
            print(f"  进度: {pct}% ({counter}/{actual_cells})")

    print(f"  绘制完成，共 {counter} 步, 写入 {frames_written} 帧")


def _build_brush_mask(radius):
    """预生成一个圆形笔刷蒙版，边缘高斯羽化，值域 0.0~1.0"""
    y, x = np.ogrid[-radius:radius + 1, -radius:radius + 1]
    dist = np.sqrt(x * x + y * y).astype(np.float32)
    mask = np.clip(1.0 - (dist - radius * 0.75) / (radius * 0.25), 0, 1)
    return mask


def _apply_brush(drawn_frame, color_img, cx, cy, brush_mask, radius):
    """在 (cx, cy) 处用圆形笔刷将 drawn_frame 混合为 color_img"""
    h, w = drawn_frame.shape[:2]
    size = radius * 2 + 1

    y1 = max(cy - radius, 0)
    y2 = min(cy + radius + 1, h)
    x1 = max(cx - radius, 0)
    x2 = min(cx + radius + 1, w)

    by1 = y1 - (cy - radius)
    by2 = size - ((cy + radius + 1) - y2)
    bx1 = x1 - (cx - radius)
    bx2 = size - ((cx + radius + 1) - x2)

    mask_region = brush_mask[by1:by2, bx1:bx2]

    for c in range(3):
        drawn_frame[y1:y2, x1:x2, c] = (
            drawn_frame[y1:y2, x1:x2, c] * (1.0 - mask_region) +
            color_img[y1:y2, x1:x2, c] * mask_region
        )


def colorize_animation(
    variables,
    target_cells,
    skip_rate=SKIP_RATE,
    brush_radius=COLOR_BRUSH_RADIUS,
):
    """
    第二阶段：上色。沿素描阶段同样的路径上色，手跟随移动。
    用圆形笔刷+羽化边缘替代矩形格子，模拟真实画笔上色效果。
    """
    split_len = variables["split_len"]
    resize_ht = variables["resize_ht"]
    resize_wd = variables["resize_wd"]
    color_img = variables["img"].astype(np.float32)
    draw_order = variables["draw_order"]

    variables["drawn_frame"] = variables["drawn_frame"].astype(np.float32)

    actual_cells = len(draw_order)
    target_frames = target_cells // skip_rate if skip_rate > 0 else actual_cells
    brush_mask = _build_brush_mask(brush_radius)
    print(
        f"  上色格子数: {actual_cells} "
        f"(笔刷半径: {brush_radius}px, 目标帧: {target_frames})"
    )

    if actual_cells == 0:
        print("  无可绘制内容，跳过上色阶段")
        return

    counter = 0
    frame_accumulator = 0.0
    frames_written = 0
    frame_ratio = target_frames / actual_cells if actual_cells > 0 else 1.0
    for row, col in draw_order:
        cx = col * split_len + split_len // 2
        cy = row * split_len + split_len // 2

        _apply_brush(variables["drawn_frame"], color_img, cx, cy, brush_mask, brush_radius)

        if variables["draw_hand"]:
            drawn_frame_with_hand = draw_hand_on_img(
                variables["drawn_frame"].copy().astype(np.uint8),
                variables["hand"].copy(),
                cx,
                cy,
                variables["hand_mask"].copy(),
                variables["hand_mask_inv"].copy(),
                variables["hand_ht"],
                variables["hand_wd"],
                resize_ht,
                resize_wd,
            )
        else:
            drawn_frame_with_hand = variables["drawn_frame"].copy().astype(np.uint8)

        counter += 1
        frame_accumulator += frame_ratio
        n_frames = int(frame_accumulator) - frames_written
        if n_frames > 0:
            frame = drawn_frame_with_hand.astype(np.uint8)
            for _ in range(n_frames):
                variables["video_object"].write(frame)
            frames_written += n_frames

        if counter % 100 == 0:
            pct = int(counter / actual_cells * 100)
            print(f"  上色进度: {pct}%")

    print(f"  上色完成，共 {counter} 步, 写入 {frames_written} 帧")


def ffmpeg_convert(source_vid, dest_vid):
    try:
        import av
        input_container = av.open(source_vid, mode="r")
        output_container = av.open(dest_vid, mode="w")
        in_stream = input_container.streams.video[0]
        width = in_stream.codec_context.width
        height = in_stream.codec_context.height
        fps = in_stream.average_rate
        out_stream = output_container.add_stream("h264", rate=fps)
        out_stream.width = width
        out_stream.height = height
        out_stream.pix_fmt = "yuv420p"
        out_stream.options = {"crf": "20"}
        for frame in input_container.decode(video=0):
            packet = out_stream.encode(frame)
            if packet:
                output_container.mux(packet)
        packet = out_stream.encode(None)
        if packet:
            output_container.mux(packet)
        output_container.close()
        input_container.close()
        print(f"  H.264 转码完成: {dest_vid}")
        return True
    except Exception as e:
        print(f"  FFmpeg 转码失败: {e}")
        return False


def parse_args():
    parser = argparse.ArgumentParser(
        description="从一张彩色图片生成白板手绘动画视频"
    )
    parser.add_argument(
        "image_path",
        help="输入图片路径"
    )
    parser.add_argument(
        "--output-dir",
        default="./output",
        help="输出目录 (默认: ./output)"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=DEFAULT_TOTAL_DURATION_SECONDS * 1000,
        help=(
            "视频总时长，单位毫秒 "
            f"(默认: {DEFAULT_TOTAL_DURATION_SECONDS * 1000}ms)"
        )
    )
    parser.add_argument(
        "--no-hand",
        action="store_true",
        help="禁用手部覆盖"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    image_path = args.image_path
    output_dir = args.output_dir
    duration = args.duration
    draw_hand = not args.no_hand
    skip_rate = SKIP_RATE

    print("=" * 50)
    print("白板手绘动画生成器")
    print("=" * 50)

    # 读取图片
    print(f"\n读取图片: {image_path}")
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        print(f"错误: 无法读取图片: {image_path}")
        sys.exit(1)

    img_ht, img_wd = image_bgr.shape[0], image_bgr.shape[1]
    print(f"  原始尺寸: {img_wd}x{img_ht}")

    # 计算目标分辨率（保持原始宽高比，长边统一缩放到 1080）
    max_dim = 1080 if MAX_1080P else max(img_wd, img_ht)
    scale = max_dim / max(img_wd, img_ht)
    img_wd = int(img_wd * scale)
    img_ht = int(img_ht * scale)
    # 确保宽高为 SPLIT_LEN 的倍数（网格切分需要）且为偶数（视频编码需要）
    lcm = SPLIT_LEN if SPLIT_LEN % 2 == 0 else SPLIT_LEN * 2
    img_wd = (img_wd // lcm) * lcm
    img_ht = (img_ht // lcm) * lcm

    print(f"  目标尺寸: {img_wd}x{img_ht}")

    # 准备输出路径
    os.makedirs(output_dir, exist_ok=True)
    now = datetime.datetime.now()
    ts = now.strftime("%Y%m%d_%H%M%S")
    raw_video_path = os.path.join(output_dir, f"vid_{ts}.mp4")
    h264_video_path = os.path.join(output_dir, f"vid_{ts}_h264.mp4")

    # 初始化变量
    variables = {
        "frame_rate": FRAME_RATE,
        "resize_wd": img_wd,
        "resize_ht": img_ht,
        "split_len": SPLIT_LEN,
        "draw_hand": draw_hand,
    }

    # 预处理图片
    print("\n预处理图片...")
    variables = preprocess_image(image_bgr, variables)
    variables["grid_of_cuts"] = split_image_into_cells(
        variables["img_thresh"], variables["split_len"]
    )
    active_grid, active_cells = extract_active_grid(
        variables["img_thresh"],
        variables["split_len"],
        grid_of_cuts=variables["grid_of_cuts"],
    )
    variables["active_grid"] = active_grid
    variables["active_cells"] = active_cells
    variables["layout_blocks"] = build_layout_blocks(active_grid)
    variables["draw_order"] = build_draw_order(
        active_grid, layout_blocks=variables["layout_blocks"]
    )
    print(
        f"  绘制顺序已生成: {len(active_cells)} 个格子, "
        f"{len(variables['layout_blocks'])} 个布局块"
    )

    # 预处理手部素材
    if draw_hand:
        print("加载手部素材...")
        if not os.path.exists(HAND_PATH):
            print(f"错误: 手部素材不存在: {HAND_PATH}")
            sys.exit(1)
        variables = preprocess_hand_image(HAND_PATH, variables)
        print(f"  手部尺寸: {variables['hand_wd']}x{variables['hand_ht']}")

    # 根据 duration（毫秒）计算每阶段目标格子数
    phase_frames = compute_phase_frames(duration, frame_rate=FRAME_RATE)
    hold_frames = phase_frames["hold_frames"]
    sketch_frames = phase_frames["sketch_frames"]
    color_frames = phase_frames["color_frames"]
    sketch_target_cells = sketch_frames * skip_rate
    color_target_cells = color_frames * skip_rate
    anim_duration = (sketch_frames + color_frames) / FRAME_RATE
    hold_duration = hold_frames / FRAME_RATE
    total_frames = sketch_frames + color_frames + hold_frames
    print(f"\n时长计算: 总时长 {duration}ms ({duration / 1000:.3f}s) = {total_frames}帧")
    print(
        f"  动画: {anim_duration:.3f}s ({sketch_frames + color_frames}帧), "
        f"停留: {hold_duration:.3f}s ({hold_frames}帧)"
    )
    print(
        f"  线稿: {sketch_frames}帧, 上色: {color_frames}帧 "
        f"({phase_frames['phase_ratio_label']})"
    )
    print(f"  skip_rate={skip_rate}, 线稿格子数: {sketch_target_cells}, 上色格子数: {color_target_cells}")

    # 创建视频写入器
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    variables["video_object"] = cv2.VideoWriter(
        raw_video_path, fourcc, FRAME_RATE, (img_wd, img_ht)
    )

    # 创建空白画布
    variables["drawn_frame"] = create_background_canvas(variables["img"].shape)

    # 开始绘制动画
    print(f"\n开始生成动画 (split_len={SPLIT_LEN}, skip_rate={skip_rate})...")
    start_time = time.time()

    draw_masked_object(variables, sketch_target_cells, skip_rate=skip_rate)

    # 第二阶段：上色
    print("\n开始上色阶段...")
    colorize_animation(
        variables,
        color_target_cells,
        skip_rate=skip_rate,
        brush_radius=COLOR_BRUSH_RADIUS,
    )

    # 结尾展示完整彩色原图
    end_img = variables["img"]
    for _ in range(hold_frames):
        variables["video_object"].write(end_img)

    variables["video_object"].release()

    elapsed = time.time() - start_time
    print(f"\n原始视频生成完成: {raw_video_path}")
    print(f"  耗时: {elapsed:.1f}秒")

    # H.264 转码
    print("\n转码为 H.264...")
    if ffmpeg_convert(raw_video_path, h264_video_path):
        os.unlink(raw_video_path)
        final_path = h264_video_path
    else:
        final_path = raw_video_path

    # 获取文件大小
    size_mb = os.path.getsize(final_path) / (1024 * 1024)
    print(f"\n最终视频: {final_path}")
    print(f"  文件大小: {size_mb:.1f} MB")
    print("=" * 50)
    print("完成!")


if __name__ == "__main__":
    main()
