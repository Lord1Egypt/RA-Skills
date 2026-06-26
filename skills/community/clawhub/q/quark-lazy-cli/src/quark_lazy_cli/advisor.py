"""
QasAdvisor - QAS 决策顾问模块

职责：
1. advice_search_result - 从搜索结果中挑选 URL 入口 + 确认最高剧集

支持多种顾问模式（通过 LAZY_CLI_ADVISOR 环境变量切换）：
- human  ：人类交互式
- code   ：规则代码自动
- llm    ：OpenAI 兼容接口 LLM
- agent  ：隔离环境用，文件轮询（OpenClaw 等 Agent 代决策）
"""

import os
import re
import json
import sys
import time
import requests
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional

from quark_lazy_cli.models import (
    DiskStatus,
    SearchGoal,
    SearchContext,
    AdvisorDecision,
)


class AdvisorError(Exception):
    """顾问异常"""

    pass


# ============================================================
# 工具函数
# ============================================================


def get_policy_desc(policy: str) -> str:
    """获取策略的中文描述"""
    if policy == "prefer_quality":
        return "最高画质优先"
    elif policy == "prefer_size":
        return "节省空间优先"
    return f"默认 (当前: {policy})"


# ============================================================
# 工具函数
# ============================================================


from quark_lazy_cli.config import get_settings

def within_days(ts_val: float, days: int = None) -> bool:
    """判断资源是否在 N 天内（严格 < days）"""
    if ts_val <= 0:
        return False
    if days is None:
        days = get_settings().search_expiration_days
    return (datetime.now() - datetime.fromtimestamp(ts_val)).days < days


def human_time(ts_val) -> str:
    if not ts_val:
        return "未知时间"
    try:
        if isinstance(ts_val, str) and "-" in ts_val:
            t_str = ts_val.split(".")[0]
            dt = (
                datetime.strptime(t_str, "%Y-%m-%d %H:%M:%S")
                if " " in t_str
                else datetime.strptime(t_str, "%Y-%m-%d")
            )
        else:
            ts = float(ts_val)
            dt = datetime.fromtimestamp(ts / 1000.0 if ts > 1e11 else ts)

        time_part = dt.strftime("%H:%M")
        weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][dt.weekday()]
        today = datetime.now()
        dt_date = dt.date()
        today_date = today.date()

        if dt_date == today_date:
            return f"今天: {time_part} {weekday}"
        elif dt_date == today_date - timedelta(days=1):
            return f"昨天: {time_part} {weekday}"
        else:
            diff_days = (today - dt).days
            return f"{diff_days}天前 {time_part} {weekday}"
    except:
        return "未知时间"


def simple_relative_day(ts_val) -> str:
    """返回简化相对日期：今天/昨天/n天前（无时间）"""
    if not ts_val:
        return ""
    try:
        if isinstance(ts_val, str):
            ts = datetime.strptime(ts_val.split(".")[0], "%Y-%m-%d %H:%M:%S").timestamp()
        else:
            ts = float(ts_val) / (1000.0 if ts_val > 1e11 else 1)
        dt = datetime.fromtimestamp(ts)
        today = datetime.now()
        diff_days = (today - dt).days
        if diff_days == 0:
            return "今天"
        elif diff_days == 1:
            return "昨天"
        elif diff_days > 1:
            return f"{diff_days}天前"
        else:
            return ""
    except:
        return ""


def format_resource_line(idx: int, item: dict, ts_key: str = None) -> str:
    """格式化资源显示行"""
    ts = parse_ts(item) if ts_key is None else item.get(ts_key, 0)
    time_str = human_time(ts) if ts > 0 else "未知时间"
    title = item.get("title") or item.get("taskname") or f"资源{idx + 1}"
    return f"  [{idx + 1}] [{time_str}] {title}"


def format_invalid_resource_line(item: dict, reason: str) -> str:
    """格式化失效资源显示行"""
    ts = parse_ts(item)
    time_str = human_time(ts) if ts > 0 else "未知时间"
    title = item.get("title") or item.get("taskname") or "未知资源"
    reason_str = f"（失效：{reason}）" if reason else "（失效）"
    return f"  [X] [{time_str}] {title}{reason_str}"


def parse_ts(item) -> float:
    ts_val = item.get("datetime") or item.get("l_updated_at") or item.get("timestamp")
    if not ts_val:
        return 0.0
    try:
        if isinstance(ts_val, str) and "-" in ts_val:
            t_str = ts_val.split(".")[0]
            dt = (
                datetime.strptime(t_str, "%Y-%m-%d %H:%M:%S")
                if " " in t_str
                else datetime.strptime(t_str, "%Y-%m-%d")
            )
            return dt.timestamp()
        ts = float(ts_val)
        return ts / 1000.0 if ts > 1e11 else ts
    except:
        return 0.0


def predict_latest_ep_from_urls(title: str) -> Optional[int]:
    if not title:
        return None
    m = re.search(r"[更新](?:至)?EP\s*(\d{1,3})", title, re.I)
    if m:
        return int(m.group(1))
    m = re.search(r"(?:[更新](?:至)?)?[^第Ee\d]*?(\d{1,3})集", title, re.I)
    if m:
        return int(m.group(1))
    eps = [int(x) for x in re.findall(r"E\s*(\d{1,3})", title, re.I)]
    if eps:
        return max(eps)
    m = re.search(r"第\s*(\d+)\s*集", title)
    if m:
        return int(m.group(1))
    return None


def normalize_taskname(taskname: str) -> str:
    """纯净化剧名：移除年份、季号等，与 QasLazyCli._normalize_taskname 保持一致"""
    pure = (
        re.sub(
            r"(?i)\((19|20)\d{2}\)|（\d{4}）|\.?S\d+.*|第\d+季.*|\（.*?\）|\(.*?\)",
            "",
            taskname,
        )
        .split(".")[0]
        .strip()
    )
    return pure or taskname[:10]


class QasAdvisor(ABC):
    @property
    def FRESH_DAYS(self) -> int:
        return get_settings().search_expiration_days

    @abstractmethod
    def advice_search_result(self, ctx: SearchContext) -> AdvisorDecision:
        pass

    def _format_header(self, ctx: SearchContext) -> str:
        """生成任务状态头，所有顾问共用"""
        disk = ctx.disk
        if not disk.quark_userlocal_owned_eps_set:
            disk_str = "空目录"
        else:
            disk_str = f"最高第{disk.quark_userlocal_max_ep}集"
            if disk.last_updated:
                disk_str += f"（更新于：{simple_relative_day(disk.last_updated)}）"
            disk_str += f"，最低第{disk.quark_userlocal_min_ep}集"
            disk_str += (
                f"，缺 {sorted(disk.quark_userlocal_hole_eps_set)}"
                if disk.quark_userlocal_hole_eps_set
                else "，无缺集"
            )
        goal_str = (
            "尽可能获取全部发布的剧集"
            if not disk.quark_userlocal_owned_eps_set
            else f"第{disk.quark_userlocal_max_ep}集以上资源"
            + (
                "，补全缺失剧集"
                if ctx.goal.mode == "all" and disk.quark_userlocal_hole_eps_set
                else ""
            )
        )
        dup_str = (
            f" ⚠️  发现 {len(ctx.dup_eps)} 个重复剧集：{sorted(ctx.dup_eps)}"
            if ctx.dup_eps
            else ""
        )
        ep0_str = (
            f" ⚠️  发现 {len(ctx.ep0_files)} 个无效 EP0 文件" if ctx.ep0_files else ""
        )
        unmatch_str = (
            f" ⚠️  发现 {len(ctx.unmatch_files)} 个文件不符合命名模板"
            if ctx.unmatch_files
            else ""
        )
        sep = "=" * 60
        return f"\n{sep}\n  📋 订阅：{ctx.taskname}\n  💾 当前：{disk_str}{dup_str}{ep0_str}{unmatch_str}\n  🎯 目标：{goal_str}\n  💎 偏好：{get_policy_desc(ctx.ep_selection_policy)}\n\n{sep}"

    def _split_fresh_old(self, results: list[dict]) -> tuple[list, list]:
        """按新鲜/旧资源分类，所有顾问共用
        fresh: < LAZY_CLI_SEARCH_EXPIRATION_DAYS 天
        old:   >= LAZY_CLI_SEARCH_EXPIRATION_DAYS 天（无上限）
        """
        fresh, old = [], []
        for r in results:
            ts = parse_ts(r)
            if within_days(ts):
                fresh.append(r)
            else:
                old.append(r)
        return fresh, old


# ============================================================
# Human 顾问
# ============================================================


class HumanQasAdvisor(QasAdvisor):

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.batch_size = get_settings().search_batch_disp

    def _parse_nums(self, user_input: str) -> set[int]:
        user_input = user_input.replace(",", " ").replace("，", " ")
        result: set[int] = set()
        for part in user_input.split():
            if "-" in part:
                try:
                    s, e = part.split("-", 1)
                    result.update(range(int(s) - 1, int(e)))
                except:
                    pass
            elif part.isdigit():
                result.add(int(part) - 1)
        return result

    def advice_search_result(self, ctx: SearchContext) -> AdvisorDecision:
        raw = list(ctx.search_results)
        if not raw:
            return AdvisorDecision()

        fresh_items, old_items = self._split_fresh_old(raw)

        records = []
        for i, item in enumerate(raw):
            ts = parse_ts(item)
            records.append(
                {
                    "global_idx": i,
                    "item": item,
                    "ts": ts,
                    "time_str": human_time(ts),
                    "has_ts": ts > 0,
                }
            )
        records.sort(key=lambda r: r["ts"], reverse=True)

        fresh = [r for r in records if within_days(r["ts"])]
        old = [r for r in records if not within_days(r["ts"])]

        disk = ctx.disk
        disk_str = (
            f"最高 {disk.quark_userlocal_max_ep}，最低 {disk.quark_userlocal_min_ep}"
        )
        if not disk.quark_userlocal_owned_eps_set:
            disk_str = "空目录"
        disk_str += (
            f"，缺 {sorted(disk.quark_userlocal_hole_eps_set)}"
            if disk.quark_userlocal_hole_eps_set
            else "，无缺集"
        )
        fresh_total = len(fresh) + ctx.fresh_invalid_count
        if ctx.fresh_invalid_count > 0:
            fresh_label = f"搜索到 {self.FRESH_DAYS} 天内新鲜分享链接：{fresh_total} 个，验证链接有效后：{len(fresh)} 个（其中 {ctx.fresh_invalid_count} 个失效）"
        else:
            fresh_label = f"搜索到 {self.FRESH_DAYS} 天内新鲜分享链接：{fresh_total} 个，验证链接有效后：{len(fresh)} 个"
        print(f"\n  🔍 {fresh_label}")

        advisor_selected_urls_index: set[int] = set()
        already_shown: set[int] = set()
        self._confirmed_limit = 0
        max_ep_confirmed = False

        # 收集需要展示的失效资源，按时间窗口分组
        fresh_invalid_records = []
        old_invalid_records = []
        for inv in ctx.invalid_search_items:
            item = inv["item"]
            reason = inv.get("reason", "")
            ts = parse_ts(item)
            rec = {
                "ts": ts,
                "time_str": human_time(ts) if ts > 0 else "未知时间",
                "item": item,
                "reason": reason,
            }
            if within_days(ts):
                fresh_invalid_records.append(rec)
            else:
                old_invalid_records.append(rec)
        fresh_invalid_records.sort(key=lambda r: r["ts"], reverse=True)
        old_invalid_records.sort(key=lambda r: r["ts"], reverse=True)

        def show_batch(target: list[dict], phase: str, invalid_pool: list) -> bool:
            """target: 有效资源记录列表（fresh 或 old）；invalid_pool: 对应窗口的失效记录"""
            nonlocal max_ep_confirmed
            idx = 0
            valid_idx = 1  # 有效资源用数字编号
            while idx < len(target):
                batch = target[idx : idx + self.batch_size]
                for r in batch:
                    already_shown.add(r["global_idx"])
                    title = re.sub(
                        r"https?://\S+",
                        "",
                        r["item"].get("title") or r["item"].get("taskname") or "",
                    ).strip()
                    tag = f"[{r['time_str']}]" if r["has_ts"] else "[未知时间]"
                    print(f"  [{r['global_idx'] + 1}] {tag} {title}")
                    valid_idx += 1
                idx += self.batch_size

                # 这批有效资源显示完后，如还有未展示的失效资源，先展示它们
                if invalid_pool:
                    for inv_r in invalid_pool[:len(invalid_pool)]:
                        item = inv_r["item"]
                        title = re.sub(r"https?://\S+", "", item.get("title") or item.get("taskname") or "").strip()
                        reason_str = f"（失效：{inv_r['reason']}）" if inv_r["reason"] else "（失效）"
                        print(f"  [X] [{inv_r['time_str']}] {title}{reason_str}")
                    invalid_pool.clear()

                while True:
                    u = input("\n  请选择序号 (如：1 2), 0=结束, 回车=下页: ").strip()
                    if u == "0":
                        return True
                    if u == "":
                        break
                    nums = self._parse_nums(u)
                    invalid = [n for n in nums if n not in already_shown]
                    if invalid:
                        print(f"      ⚠️  序号 {invalid} 尚未展示，请等待。")
                        continue
                    new = nums - advisor_selected_urls_index
                    if new:
                        advisor_selected_urls_index.update(new)
                        for n in sorted(new):
                            t = re.sub(
                                r"https?://\S+",
                                "",
                                raw[n].get("title") or raw[n].get("taskname") or "",
                            ).strip()
                            ep = predict_latest_ep_from_urls(t)
                            print(
                                f"     ✅ 已入选: {t[:50]}{f' → E{ep}' if ep else ''}"
                            )

                        if not max_ep_confirmed:
                            sel_eps = [
                                predict_latest_ep_from_urls(
                                    raw[n].get("title") or raw[n].get("taskname") or ""
                                )
                                for n in advisor_selected_urls_index
                            ]
                            sel_eps = [e for e in sel_eps if e]
                            suggested = (
                                max(sel_eps)
                                if sel_eps
                                else (ctx.goal.suggested_max_ep or 0)
                            )
                            limit_input = input(
                                f"\n  💡 当前最高剧集 (从发布资源判断，默认 {suggested}): "
                            ).strip()
                            self._confirmed_limit = (
                                int(limit_input)
                                if limit_input and limit_input.isdigit()
                                else (0 if limit_input == "0" else suggested)
                            )
                            max_ep_confirmed = True
                    else:
                        print("     ⚠️  所选均已在列表中。")
                    break
            return False

        # fresh 有效 + fresh 失效 混排
        if fresh or fresh_invalid_records:
            if not fresh:
                # 无有效资源但有失效资源，先展示 [X]
                for inv_r in fresh_invalid_records:
                    item = inv_r["item"]
                    title = re.sub(r"https?://\S+", "", item.get("title") or item.get("taskname") or "").strip()
                    reason_str = f"（失效：{inv_r['reason']}）" if inv_r["reason"] else "（失效）"
                    print(f"  [X] [{inv_r['time_str']}] {title}{reason_str}")
                fresh_invalid_records.clear()
                print(f"\n--- ⚠️ 无可选有效新鲜资源 ---")
            stop = show_batch(fresh, "新鲜资源", fresh_invalid_records)
        else:
            print(f"\n--- ⚠️ 无可选有效新鲜资源 ---")
            stop = True

        if stop:
            print(f"\n--- 🎉 所有 {self.FRESH_DAYS} 天内新鲜资源已展示完毕 ---")

        # old 有效 + old 失效 混排（用户选择后才展示）
        if not stop and (old or old_invalid_records):
            if (
                input(
                    f"\n👉 是否继续查看{len(old)}个{self.FRESH_DAYS}天以上、验证链接有效后的旧分享链接？(y/n) [n]: "
                )
                .strip()
                .lower()
                == "y"
            ):
                show_batch(old, "旧资源", old_invalid_records)

        if not advisor_selected_urls_index:
            advisor_selected_urls_index = set(range(len(raw)))
        return AdvisorDecision(
            advisor_selected_urls_index=sorted(advisor_selected_urls_index),
            advisor_confirmed_max_ep=self._confirmed_limit,
        )


# ============================================================
# Code 顾问
# ============================================================


class CodeQasAdvisor(QasAdvisor):
    """
    Code 顾问（自动决策）
    注意：QasLazyCli 已做过"剧名"过滤，传进来的 search_results 已二次筛选
    本顾问只做：
    1. FRESH_DAYS 天内过滤
    2. 用 predict_latest_ep_from_urls 找最高EP
    3. 返回选中资源 + advisor_confirmed_max_ep
    """

    def __init__(self, debug: bool = False):
        self.debug = debug

    def advice_search_result(self, ctx: SearchContext) -> AdvisorDecision:
        raw = list(ctx.search_results)
        if not raw:
            return AdvisorDecision()

        fresh_items, _ = self._split_fresh_old(raw)
        if self.debug:
            print(f"\n[CODE Debug] 共 {len(raw)} 个分享链接:")
            for i, item in enumerate(raw):
                ts = parse_ts(item)
                ts_fresh = within_days(ts)
                title = item.get("title") or item.get("taskname") or ""
                ep = predict_latest_ep_from_urls(title)
                url = item.get("shareurl") or ""
                sid = url.split("/s/")[1].split("#")[0] if "/s/" in url else "-"
                fresh_mark = "✓" if ts_fresh else "✗"
                title_disp = title[:80] if len(title) <= 80 else title[:80] + "..."
                print(f"  [{i + 1}] {fresh_mark} | EP{ep} | sid={sid[:12]} | {title_disp}")
            print(f"[CODE Debug] FRESH天内: {len(fresh_items)} 个")
        if not fresh_items:
            return AdvisorDecision()

        # 建立 fresh_items 中每个元素的原始索引
        fresh_map = {id(item): i for i, item in enumerate(raw)}
        candidates = []
        for item in fresh_items:
            title = item.get("title") or item.get("taskname") or ""
            ep = predict_latest_ep_from_urls(title)
            if ep:
                candidates.append((fresh_map[id(item)], ep))

        if not candidates:
            sys.stderr.write("[CODE] 未找到最高集数，无法自动决策，退出\n")
            return AdvisorDecision()
        # 返回所有新鲜资源，BFS pool 会做 PK 选最优
        best_ep = max(ep for _, ep in candidates)
        selected_indices = [idx for idx, ep in candidates]
        if self.debug:
            print(f"[CODE Debug] 最高EP: {best_ep}，返回全部新鲜资源 {len(selected_indices)} 个")
        limit = (
            min(best_ep, ctx.goal.suggested_max_ep)
            if ctx.goal.suggested_max_ep > 0
            else best_ep
        )
        return AdvisorDecision(
            advisor_selected_urls_index=selected_indices, advisor_confirmed_max_ep=limit
        )

    @staticmethod
    def _fuzzy_match(title: str, taskname: str) -> bool:
        base = normalize_taskname(taskname)
        if not base:
            return False
        return base in title


# ============================================================
# LLM 顾问
# ============================================================


class LLMQasAdvisor(QasAdvisor):
    """
    LLM 顾问（调用外部LLM决策）
    注意：QasLazyCli 已做过"剧名"过滤，传进来的 search_results 已二次筛选
    本顾问只做：
    1. FRESH_DAYS 天内过滤
    2. 调LLM决策选哪些 + 最高EP
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.base_url = get_settings().llm_api_base
        self.api_key = get_settings().llm_api_key
        self.model = get_settings().llm_model
        self._tag = f"[LLM-{self.model} 顾问]"
        if self.debug:
            sys.stderr.write(
                f"[LLM Init] base_url='{self.base_url}', api_key set={bool(self.api_key)}, model={self.model}\n"
            )
        if not self.base_url or not self.api_key:
            raise AdvisorError("LLM 顾问需要设置环境变量")

    @staticmethod
    def _robust_json_parse(content: str) -> dict:
        # 1. 预处理：去掉 Markdown 代码块和 think 标签
        clean = re.sub(r"```(?:json)?|```|<think>.*?</think>", "", content, flags=re.DOTALL)

        # 2. 找 { 到 } 之间的内容，用 json.loads 解析
        m = re.search(r"(\{.*\})", clean, re.DOTALL)
        if m:
            try:
                obj = json.loads(m.group(1))
                if "selected" in obj and "max_ep" in obj:
                    return {"selected": obj["selected"], "max_ep": int(obj["max_ep"])}
            except (json.JSONDecodeError, ValueError, KeyError):
                pass

        # 3. 降级：独立提取两个字段（不限顺序）
        result = {}
        sel = re.search(r'"selected"\s*:\s*\[([\d,\s]*)\]', content)
        mx = re.search(r'"max_ep"\s*:\s*(\d+)', content)
        if sel:
            result["selected"] = [int(x) for x in sel.group(1).split(",") if x.strip()]
        if mx:
            result["max_ep"] = int(mx.group(1))
        return result

    def advice_search_result(self, ctx: SearchContext) -> AdvisorDecision:
        raw = list(ctx.search_results)
        if self.debug:
            sys.stderr.write(
                f"\n[LLM Advisor] 收到搜索结果: {len(raw)} 条\n"
            )
        fresh_items, _ = self._split_fresh_old(raw)
        if self.debug:
            sys.stderr.write(f"[LLM Advisor] {self.FRESH_DAYS}天内新鲜资源: {len(fresh_items)} 条\n")
        if not fresh_items:
            return AdvisorDecision()

        # 构建当前状态描述
        disk_info = f"最高第{ctx.disk.quark_userlocal_max_ep}集，最低第{ctx.disk.quark_userlocal_min_ep}集"
        if ctx.disk.quark_userlocal_hole_eps_set:
            disk_info += f"，缺集 {sorted(ctx.disk.quark_userlocal_hole_eps_set)}"
        else:
            disk_info += "，无缺集"

        # 构建目标描述
        target_desc = (
            f"第{ctx.disk.quark_userlocal_max_ep}集以上剧集"
            if ctx.goal.mode == "new"
            else "追新+补全缺失剧集"
        )

        # 构建判断依据说明
        # 构建判断依据说明（内嵌于用户提示，暂不单独使用）

        fresh_total = len(fresh_items) + ctx.fresh_invalid_count
        if ctx.fresh_invalid_count > 0:
            fresh_label = f"搜索到 {self.FRESH_DAYS} 天内新鲜分享链接：{fresh_total} 个，验证链接有效后：{len(fresh_items)} 个（其中 {ctx.fresh_invalid_count} 个失效）"
        else:
            fresh_label = f"搜索到 {self.FRESH_DAYS} 天内新鲜分享链接：{fresh_total} 个，验证链接有效后：{len(fresh_items)} 个"

        results_text = [
            f"[{i + 1}] [{human_time(parse_ts(item))}] {re.sub(r'https?://\S+', '', (item.get('title') or item.get('taskname') or '')).strip()}"
            for i, item in enumerate(fresh_items)
        ]
        invalid_count = len(ctx.invalid_search_items)
        if invalid_count > 0:
            results_text.append(f"注意：另有 {invalid_count} 个失效资源已排除，不可选择。")

        llm_fresh_label = f"搜到 {self.FRESH_DAYS} 天内有效的分享链接：{len(fresh_items)} 个"

        system_prompt = (
            "你是一个严谨的更新决策助手。RETURN JSON ONLY. 禁止任何解释性文字。"
        )
        user_prompt = f"""📋 夸克订阅任务：{ctx.taskname}
💾 网盘：{disk_info}
🎯 目标：{target_desc}

============================================================
🔍 {llm_fresh_label}
注意：以下候选均已通过分享链接有效性验证。请尽量选择3-5个符合条件的新鲜资源，放入selected字段，如[1, 2, 3, 5]
{chr(10).join(results_text)}

============================================================
{f"【用户附加指令】\n{ctx.add_prompt}\n" if ctx.add_prompt else ""}请根据资源标题中的"更新至X集"或"E数字"判断最新（最高）剧集数（取最大值），并选择3-5个符合条件的新鲜资源，返回JSON：
{{"selected": [1, 2, 3, 5], "max_ep": 19}}
{"（注意：追新模式下，只有最高集数 > 本地最高集数时才选择资源；如最高集数不超过本地最高集数，selected 必须返回空数组 []）" if ctx.goal.mode == "new" else ""}"""
        try:
            # 构造 payload，先于 MiniMax 判断
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": get_settings().llm_temperature,
            }
            # MiniMax reasoning_split 开关
            base_lower = self.base_url.lower()
            model_lower = self.model.lower()
            if ("minimax" in base_lower or "minimaxi" in base_lower
                    or model_lower.startswith("minimax")):
                payload["reasoning_split"] = True
            if self.debug:
                # 打印发送给LLM的消息
                sys.stderr.write(f"\n[LLM 发送]\n{system_prompt}\n\n{user_prompt}\n")
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=60,
            )
            if self.debug:
                sys.stderr.write(f"[LLM 收到响应] status={resp.status_code}\n")
            if not resp.ok:
                error_msg = f"LLM API错误 HTTP {resp.status_code}: {resp.text[:200]}"
                sys.stderr.write(f"[LLM 错误] {error_msg}\n")
                return AdvisorDecision(error=error_msg)
            resp_data = resp.json()
            if self.debug:
                sys.stderr.write(f"[LLM 响应结构] {list(resp_data.keys())}\n")
                sys.stderr.write(
                    f"[LLM choices[0]] {resp_data.get('choices', [{}])[0]}\n"
                )
            # MiniMax thinking 模式：choices[0] 可能是 {"message": {"content": "..."}} 或其他结构
            choice0 = resp_data.get("choices", [{}])[0]
            if isinstance(choice0, dict):
                # 尝试从 message.content 提取
                msg_content = choice0.get("message", {}).get("content", "")
                if not msg_content:
                    # 尝试从 text 提取（某些API格式）
                    msg_content = choice0.get("text", "") or str(choice0)
            else:
                msg_content = str(choice0)
            raw_response = msg_content
            if self.debug:
                # 打印收到LLM的回复
                sys.stderr.write(f"[LLM 收到]\n{raw_response[:800]}\n")
            parsed = self._robust_json_parse(raw_response)
            quark_userlocal_max_ep = (
                int(parsed.get("max_ep", 0)) if parsed.get("max_ep") else 0
            )
            # Build display-index -> raw-index mapping
            raw_index_by_fresh_display = []
            raw_index_by_id = {id(item): idx for idx, item in enumerate(raw)}
            for item in fresh_items:
                raw_index_by_fresh_display.append(raw_index_by_id[id(item)])
            # 解析 selected（1-based转raw-index），通过 mapping 转换
            if "selected" not in parsed:
                selected = []
            else:
                raw_selected = parsed.get("selected", [])
                if not isinstance(raw_selected, list):
                    return AdvisorDecision(error="LLM selected 字段必须是 list")
                selected = []
                invalid = []
                for n in raw_selected:
                    if not isinstance(n, int):
                        invalid.append(n)
                        continue
                    if not (1 <= n <= len(raw_index_by_fresh_display)):
                        invalid.append(n)
                        continue
                    selected.append(raw_index_by_fresh_display[n - 1])
                if invalid:
                    return AdvisorDecision(
                        error=f"LLM selected 序号越界或非法，有效范围 1-{len(raw_index_by_fresh_display)}: {invalid}"
                    )
            if self.debug:
                sys.stderr.write(
                    f"[LLM 解析结果] selected(1-based)={raw_selected} -> raw_index={sorted(selected)}, quark_userlocal_max_ep={quark_userlocal_max_ep}\n"
                )
            return AdvisorDecision(
                advisor_selected_urls_index=sorted(selected),
                advisor_confirmed_max_ep=quark_userlocal_max_ep,
            )
        except Exception as e:
            if self.debug:
                sys.stderr.write(f"[LLM 异常] {e}\n")
            err_str = str(e)
            if "ReadTimeout" in err_str or "timed out" in err_str.lower():
                return AdvisorDecision(error="LLM API 调用超时（60秒无响应）")
            return AdvisorDecision(error=f"LLM 顾问异常：{err_str[:100]}")


def create_advisor(debug: bool = False) -> QasAdvisor:
    kind = get_settings().advisor
    if kind == "code":
        return CodeQasAdvisor(debug=debug)
    if kind == "llm":
        return LLMQasAdvisor(debug=debug)
    if kind == "agent":
        return AgentQasAdvisor(debug=debug)
    return HumanQasAdvisor(debug=debug)


# ============================================================
# Agent 顾问（隔离环境用，文件轮询）
# ============================================================


class AgentQasAdvisor(QasAdvisor):
    """隔离环境用：不阻塞 input，改为文件轮询等待 Agent 决策"""

    MAX_TRIES = 20  # 5 分钟（20 × 15s）

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.msg_dir = get_settings().agent_msg_dir
        self.poll_interval = get_settings().agent_poll_interval

    def advice_search_result(self, ctx: SearchContext) -> AdvisorDecision:
        raw = list(ctx.search_results)
        if not raw:
            return AdvisorDecision()

        fresh_items, old_items = self._split_fresh_old(raw)

        if not fresh_items:
            return AdvisorDecision()

        # Build display-index -> raw-index mapping
        raw_index_by_fresh_display = []
        raw_index_by_id = {id(item): idx for idx, item in enumerate(raw)}
        for item in fresh_items:
            raw_index_by_fresh_display.append(raw_index_by_id[id(item)])

        # 打印与 Human 相同的显示内容
        print(self._format_header(ctx))
        for i, item in enumerate(fresh_items):
            ts = parse_ts(item)
            ts_str = human_time(ts) if ts > 0 else "未知时间"
            title = re.sub(r"https?://\S+", "", (item.get("title") or item.get("taskname") or "")).strip()
            print(f"  [{i + 1}] [{ts_str}] {title}")

        # 生成文件路径
        ts = int(time.time())
        taskname_safe = re.sub(r"[^\w]", "_", ctx.taskname)
        decision_file = os.path.join(self.msg_dir, f"advisor__{taskname_safe}__{ts}.json")

        print(f"\n  请将您的选择写入以下文件：")
        print(f"  路径：{decision_file}")
        print(f"  格式：{{\"selected\": [1, 2], \"max_ep\": 23}}")
        print(f"  提示：请在搜索资源中选择有效订阅资源，selected 序号对应上方 [1] [2]...，并判断当前最新剧集 max_ep")
        if ctx.goal.mode == "new":
            print("  追新规则：只有最高集数 > 本地最高集数时才选择资源；如最高集数不超过本地最高集数，selected 必须返回空数组 []")
        print(f"\n  ⏳ 等待 Agent 决策（最多 5 分钟）...")

        # 轮询等待
        for _ in range(self.MAX_TRIES):
            time.sleep(self.poll_interval)
            if os.path.exists(decision_file):
                try:
                    raw_content = open(decision_file).read().strip()
                    data = json.loads(raw_content)
                    selected, max_ep = self._validate(data, raw_index_by_fresh_display)
                    return AdvisorDecision(
                        advisor_selected_urls_index=sorted(selected),
                        advisor_confirmed_max_ep=max_ep,
                    )
                except json.JSONDecodeError as e:
                    return AdvisorDecision(
                        error=f"Agent 顾问回复无法解析：{raw_content[:200]}"
                    )
                except Exception as e:
                    return AdvisorDecision(error=f"Agent 顾问决策异常：{e}")

        # 超时
        return AdvisorDecision(error="Agent 顾问响应超时（5分钟）")

    def _validate(self, data: dict, mapping: list[int]) -> tuple[list, int]:
        raw_selected = data.get("selected", [])
        if not isinstance(raw_selected, list):
            raise ValueError("selected must be a list")
        if not all(isinstance(n, int) for n in raw_selected):
            raise ValueError("selected must contain only integers")
        if not all(1 <= n <= len(mapping) for n in raw_selected):
            raise ValueError(f"selected values must be 1-{len(mapping)}")
        selected = [mapping[n - 1] for n in raw_selected]
        max_ep = data.get("max_ep", 0)
        return selected, max_ep
