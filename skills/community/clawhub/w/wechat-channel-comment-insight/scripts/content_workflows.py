"""Bounded comment research and comparable official-account reports."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import statistics
import sys
from urllib.parse import urlparse

from workflow_core import (API, APIError, Job, analysis_text, atomic_json, digest, excel_ready,
                           export_bundle, list_items, micros, next_params, now, page_project,
                           read_json, select, workspace_lock)
from data_safety import public_data

CHANNEL_LIST = "wechat-native-channel-videos"
CHANNEL_SEARCH = "wechat-native-channel-search"
CHANNEL_RESOLVE = "wechat-native-channel-resolve"
COMMENTS = "wechat-native-channel-comments"
REPLIES = "wechat-native-channel-comment-replies"
HISTORY = "wechat-native-account-articles"
METRICS = "wechat-native-article-metrics"
CONTENT = "wechat-native-article-content"
VIDEO_FIELDS = ("objectId", "objectNonceId", "title", "description", "accountId", "accountName",
                "publishedTimestamp", "publishedAt", "commentCount", "warnings", "status")
COMMENT_FIELDS = ("commentId", "replyCommentId", "accountId", "accountName", "content", "publishedTimestamp",
                  "publishedAt", "likeCount", "replyCount", "ipRegion", "signature")
ARTICLE_FIELDS = ("url", "canonicalUrl", "title", "digest", "author", "publishTimestamp", "publishTime",
                  "biz", "mid", "idx", "sn", "linkStatus", "linkUnavailableReason", "contentType")
METRIC_FIELDS = ("readNum", "likeNum", "oldLikeNum", "shareNum", "commentNum", "collectNum",
                 "readText", "readCapped", "title", "accountName", "capturedAt")


def bounded(plan, name, default, maximum):
    value = plan.get(name, default)
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise ValueError(name + " 必须为 1～" + str(maximum) + " 的整数")
    return value


def validate_plan(plan, kind):
    if not isinstance(plan, dict):
        raise ValueError("计划必须是 JSON 对象")
    names = {"accounts", "videos", "keyword", "maxAccounts", "videosPerAccount", "maxVideos",
             "commentsPerVideo", "pagesPerVideo", "videoPagesPerAccount", "includeReplies",
             "replyPagesPerComment", "maxReplyParentsPerVideo"} if kind == "comments" else {
                 "accounts", "historyPagesPerAccount", "articlesPerAccount", "deepReadCount", "since", "until"}
    if set(plan) - names:
        raise ValueError("不支持的计划字段：" + ",".join(sorted(set(plan) - names)))
    if not any(plan.get(k) for k in ("accounts", "videos", "keyword")):
        raise ValueError("至少提供 accounts、videos 或 keyword")
    if not isinstance(plan.get("accounts", []), list) or len(plan.get("accounts", [])) > 100:
        raise ValueError("accounts 必须是至多 100 项的列表")
    for account in plan.get("accounts", []):
        if not isinstance(account, dict):
            raise ValueError("账号应为对象：公众号用 ghid/url，视频号用 accountId")
        identity = ("accountId",) if kind == "comments" else ("ghid", "url")
        if set(account) - set((*identity, "name")):
            raise ValueError("账号包含不支持的字段")
        if sum(bool(account.get(k)) for k in identity) != 1:
            raise ValueError("账号必须且只能提供一种身份：" + "/".join(identity))
        for k in identity:
            if k in account and not isinstance(account[k], str):
                raise ValueError("账号身份必须保留为字符串")
        if account.get("url") and urlparse(account["url"]).hostname != "mp.weixin.qq.com":
            raise ValueError("公众号文章须使用 mp.weixin.qq.com 链接")
    if kind == "comments":
        if "keyword" in plan and (not isinstance(plan["keyword"], str) or not plan["keyword"].strip()):
            raise ValueError("keyword 必须为非空文本")
        for n, default, maximum in (("maxAccounts", 1, 20), ("maxVideos", 10, 200),
                                  ("videosPerAccount", 10, 100), ("commentsPerVideo", 100, 10000),
                                  ("pagesPerVideo", 2, 100), ("videoPagesPerAccount", 1, 20),
                                  ("replyPagesPerComment", 1, 20), ("maxReplyParentsPerVideo", 5, 100)):
            bounded(plan, n, default, maximum)
        if not isinstance(plan.get("includeReplies", False), bool):
            raise ValueError("includeReplies 必须为布尔值")
        if not isinstance(plan.get("videos", []), list) or len(plan.get("videos", [])) > 200:
            raise ValueError("videos 必须为至多 200 项的列表")
        for v in plan.get("videos", []):
            if not isinstance(v, dict) or sum(bool(v.get(k)) for k in ("url", "objectId")) != 1:
                raise ValueError("每个视频提供 url 或 objectId（配套 objectNonceId），不要同时填写")
            if any(k in v and not isinstance(v[k], str) for k in ("url", "objectId", "objectNonceId")):
                raise ValueError("视频身份必须为字符串")
            if set(v) - set((*VIDEO_FIELDS, "url")):
                raise ValueError("视频包含不支持的字段")
            if v.get("url") and urlparse(v["url"]).hostname not in ("weixin.qq.com", "www.weixin.qq.com", "channels.weixin.qq.com"):
                raise ValueError("视频须使用微信视频号分享链接")
    else:
        if not plan.get("accounts"):
            raise ValueError("公众号对标必须提供 accounts")
        bounded(plan, "historyPagesPerAccount", 1, 50)
        bounded(plan, "articlesPerAccount", 10, 1000)
        deep = plan.get("deepReadCount", 5)
        if isinstance(deep, bool) or not isinstance(deep, int) or not 0 <= deep <= 100:
            raise ValueError("deepReadCount 须为 0～100")
        for name in ("since", "until"):
            if plan.get(name):
                parse_date(plan[name])
        if plan.get("since") and plan.get("until") and parse_date(plan["since"]) > parse_date(plan["until"]):
            raise ValueError("since 不能晚于 until")
    return plan


def estimate(api, plan, kind):
    calls = []
    def add(slug, params, count):
        if count:
            unit = api.unit(slug, params)
            calls.append({"product": slug, "maxCalls": count, "unitMicros": unit, "maxMicros": unit * count})
    if kind == "comments":
        account_count = len(plan.get("accounts", [])) + (plan.get("maxAccounts", 1) if plan.get("keyword") else 0)
        if plan.get("keyword"):
            add(CHANNEL_SEARCH, {"keyword": plan["keyword"]}, 1)
        add(CHANNEL_LIST, {"accountId": "estimate"}, account_count * plan.get("videoPagesPerAccount", 1))
        add(CHANNEL_RESOLVE, {"url": "https://weixin.qq.com/sph/estimate"}, sum(bool(v.get("url")) for v in plan.get("videos", [])[:plan.get("maxVideos", 10)]))
        n = min(plan.get("maxVideos", 10), len(plan.get("videos", [])) + account_count * plan.get("videosPerAccount", 10))
        add(COMMENTS, {"objectId": "estimate"}, n * plan.get("pagesPerVideo", 2))
        if plan.get("includeReplies"):
            add(REPLIES, {"objectId": "estimate", "commentId": "estimate"},
                n * plan.get("maxReplyParentsPerVideo", 5) * plan.get("replyPagesPerComment", 1))
    else:
        n = len(plan["accounts"])
        add(HISTORY, {"ghid": "estimate"}, n * plan.get("historyPagesPerAccount", 1))
        add(METRICS, {"url": "https://mp.weixin.qq.com/s?__biz=estimate"}, n * plan.get("articlesPerAccount", 10))
        add(CONTENT, {"url": "https://mp.weixin.qq.com/s?__biz=estimate", "format": "text"},
            min(plan.get("deepReadCount", 5), n * plan.get("articlesPerAccount", 10)))
    return {"calls": calls, "maxMicros": sum(c["maxMicros"] for c in calls),
            "priceSource": "account_catalog" if api.key else "public_catalog",
            "note": "调用上限估算；每页条数不固定，模型使用费不含在内。执行还有独立金额上限。"}


def comment_projection(data):
    result = select(data, COMMENT_FIELDS)
    if isinstance(data.get("replies"), list):
        result["replies"] = [select(r, COMMENT_FIELDS) for r in data["replies"]]
    return result


def collect_comments(job, plan):
    accounts = list(plan.get("accounts", []))
    videos, errors, candidates = {}, [], []
    cap = plan.get("maxVideos", 10)
    def check_page(page, stage, ident):
        if page.get("partial") or page.get("status") in ("partial", "failed") or page.get("warnings"):
            errors.append({"stage": stage, "identity": ident, "message": "上游返回部分结果或提示", "warnings": page.get("warnings")})
    def add_video(row):
        if not row.get("objectId"):
            errors.append({"stage": "video_identity", "message": "作品缺少 objectId", "title": row.get("title", "")})
            return
        if len(videos) < cap:
            videos[str(row["objectId"])] = select(row, VIDEO_FIELDS)
    if plan.get("keyword"):
        try:
            data = job.call(CHANNEL_SEARCH, {"keyword": plan["keyword"]},
                            lambda d: {"accounts": [select(r, ("accountId", "accountName", "signature"))
                                                      for r in list_items(d, ("accounts",))]})
            candidates = data["accounts"]
            accounts.extend(candidates[:plan.get("maxAccounts", 1)])
        except (APIError, ValueError) as e:
            errors.append({"stage": "search", "message": str(e)})
    for raw in plan.get("videos", []):
        if len(videos) >= cap:
            break
        try:
            video = job.call(CHANNEL_RESOLVE, {"url": raw["url"]}, lambda d: select(d, VIDEO_FIELDS)) if raw.get("url") else raw
            add_video(video)
        except (APIError, ValueError) as e:
            errors.append({"stage": "resolve", "message": str(e)})
    seen_accounts = set()
    for account in accounts:
        account_id = account.get("accountId")
        if not account_id or account_id in seen_accounts or len(videos) >= cap:
            continue
        seen_accounts.add(account_id)
        params, seen, accepted = {"accountId": account_id}, set(), 0
        for _ in range(plan.get("videoPagesPerAccount", 1)):
            try:
                signature = digest(params)
                if signature in seen:
                    raise APIError("PAGINATION_CURSOR_REPEATED")
                seen.add(signature)
                page = job.call(CHANNEL_LIST, params, lambda d: page_project(d, lambda r: select(r, VIDEO_FIELDS)))
                check_page(page, "video_list", account_id)
                for video in page["items"]:
                    if accepted >= plan.get("videosPerAccount", 10) or len(videos) >= cap:
                        break
                    before = len(videos)
                    add_video(video)
                    accepted += len(videos) > before
                if accepted >= plan.get("videosPerAccount", 10) or len(videos) >= cap:
                    break
                params = next_params(page, params)
                if params is None:
                    break
            except (APIError, ValueError) as e:
                errors.append({"stage": "video_list", "accountId": account_id, "message": str(e)})
                break
    comments, states = {}, []
    def add_comment(row, video, parent=""):
        cid = row.get("commentId")
        if cid is None or str(cid) == "":
            errors.append({"stage": "comment_identity", "objectId": video["objectId"], "message": "评论缺少 ID，未纳入去重统计"})
            return
        ref = str(video["objectId"]) + ":" + str(cid)
        parent = str(parent or row.get("replyCommentId") or "")
        if parent == "0":
            parent = ""
        comments[ref] = {**select(row, COMMENT_FIELDS), "evidenceId": ref, "objectId": str(video["objectId"]),
                         "videoTitle": video.get("title", ""), "parentCommentId": parent,
                         "level": 2 if parent else 1}
    for video in videos.values():
        params = {"objectId": str(video["objectId"]), "limit": min(100, plan.get("commentsPerVideo", 100))}
        if video.get("objectNonceId"):
            params["objectNonceId"] = str(video["objectNonceId"])
        parents, seen, count, stop = {}, set(), 0, "page_limit"
        for _ in range(plan.get("pagesPerVideo", 2)):
            try:
                signature = digest(params)
                if signature in seen:
                    raise APIError("PAGINATION_CURSOR_REPEATED")
                seen.add(signature)
                page = job.call(COMMENTS, params, lambda d: page_project(d, comment_projection))
                check_page(page, "comments", video["objectId"])
                for row in page["items"]:
                    if count >= plan.get("commentsPerVideo", 100):
                        break
                    cid = row.get("commentId")
                    if cid is None or str(cid) in parents:
                        continue
                    parents[str(cid)] = row
                    add_comment(row, video)
                    count += 1
                    if plan.get("includeReplies"):
                        for reply in row.get("replies", []):
                            add_comment(reply, video, str(cid))
                if count >= plan.get("commentsPerVideo", 100):
                    stop = "comment_limit"
                    break
                params = next_params(page, params)
                if params is None:
                    stop = "end"
                    break
            except (APIError, ValueError) as e:
                stop = "partial"
                errors.append({"stage": "comments", "objectId": video["objectId"], "message": str(e)})
                break
        if plan.get("includeReplies"):
            for parent_id, parent in list(parents.items())[:plan.get("maxReplyParentsPerVideo", 5)]:
                embedded = {str(r.get("commentId")) for r in parent.get("replies", []) if r.get("commentId") is not None}
                if isinstance(parent.get("replyCount"), int) and len(embedded) >= parent["replyCount"]:
                    continue
                rp = {"objectId": video["objectId"], "commentId": parent_id, "limit": 100}
                if video.get("objectNonceId"):
                    rp["objectNonceId"] = video["objectNonceId"]
                positions = set()
                for _ in range(plan.get("replyPagesPerComment", 1)):
                    try:
                        if digest(rp) in positions:
                            raise APIError("PAGINATION_CURSOR_REPEATED")
                        positions.add(digest(rp))
                        page = job.call(REPLIES, rp, lambda d: page_project(d, comment_projection))
                        check_page(page, "replies", parent_id)
                        for row in page["items"]:
                            add_comment(row, video, parent_id)
                        rp = next_params(page, rp)
                        if rp is None:
                            break
                    except (APIError, ValueError) as e:
                        errors.append({"stage": "replies", "objectId": video["objectId"], "commentId": parent_id, "message": str(e)})
                        break
        states.append({"objectId": video["objectId"], "title": video.get("title"), "primaryComments": count,
                       "stopReason": stop, "displayedCommentCount": video.get("commentCount")})
    return {"kind": "comments", "capturedAt": now(), "scope": plan, "videos": list(videos.values()),
            "comments": list(comments.values()), "states": states, "errors": errors, "candidates": candidates,
            "cost": job.totals()}


def parse_date(value):
    dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    # Date-only and naive user input are China business time.
    if dt.tzinfo is None:
        from datetime import timedelta
        dt = dt.replace(tzinfo=timezone(timedelta(hours=8)))
    return dt.timestamp()


def article_identity(row):
    if row.get("biz") and row.get("mid") and row.get("idx"):
        return ":".join(str(row[k]) for k in ("biz", "mid", "idx"))
    return row.get("canonicalUrl") or row.get("url") or "metadata:" + digest(row)


def collect_competitors(job, plan):
    articles, summaries, errors = {}, [], []
    start = parse_date(plan["since"]) if plan.get("since") else None
    end = parse_date(plan["until"]) if plan.get("until") else None
    account_inputs = set()
    for account in plan["accounts"]:
        input_key = digest({k: account[k] for k in ("ghid", "url") if account.get(k)})
        if input_key in account_inputs:
            continue
        account_inputs.add(input_key)
        label = account.get("name") or account.get("ghid") or account.get("url")
        params = {k: account[k] for k in ("ghid", "url") if account.get(k)}
        params["page"] = 1
        seen, chosen, complete = set(), {}, False
        for _ in range(plan.get("historyPagesPerAccount", 1)):
            try:
                if digest(params) in seen:
                    raise APIError("PAGINATION_CURSOR_REPEATED")
                seen.add(digest(params))
                page = job.call(HISTORY, params, lambda d: page_project(d, lambda r: select(r, ARTICLE_FIELDS)))
                if page.get("partial") or page.get("status") in ("partial", "failed") or page.get("warnings"):
                    errors.append({"stage": "history", "account": label, "message": "上游返回部分结果或提示", "warnings": page.get("warnings")})
                if isinstance(page.get("account"), dict):
                    label = page["account"].get("accountName") or label
                reached_start = False
                for row in page["items"]:
                    stamp = row.get("publishTimestamp")
                    if stamp is not None:
                        try:
                            stamp = float(stamp)
                        except (TypeError, ValueError):
                            stamp = None
                    if (start is not None or end is not None) and not stamp:
                        continue
                    if start is not None and stamp < start:
                        reached_start = True
                        continue
                    if end is not None and stamp > end:
                        continue
                    ident = article_identity(row)
                    if len(chosen) < plan.get("articlesPerAccount", 10):
                        chosen[ident] = {**row, "evidenceId": ident, "accountName": label}
                complete = page.get("hasMore") is False or reached_start
                if complete or len(chosen) >= plan.get("articlesPerAccount", 10):
                    break
                params = next_params(page, params)
                if params is None:
                    break
            except (APIError, ValueError) as e:
                errors.append({"stage": "history", "account": label, "message": str(e)})
                break
        for ident, row in chosen.items():
            if ident in articles:
                chosen[ident] = articles[ident]
                continue
            url = row.get("canonicalUrl") or row.get("url")
            if url:
                try:
                    row["metrics"] = job.call(METRICS, {"url": url}, lambda d: select(d, METRIC_FIELDS))
                except (APIError, ValueError) as e:
                    errors.append({"stage": "metrics", "evidenceId": ident, "message": str(e)})
            else:
                errors.append({"stage": "metrics", "evidenceId": ident, "message": "没有稳定公开链接，保留元数据"})
            articles[ident] = row
        values = [row.get("metrics", {}).get("readNum") for row in chosen.values()
                  if not row.get("metrics", {}).get("readCapped")]
        values = [v for v in values if isinstance(v, int) and not isinstance(v, bool)]
        summaries.append({"accountName": label, "sampleCount": len(chosen), "exactReadSamples": len(values),
                          "medianRead": statistics.median(values) if values else None,
                          "minRead": min(values) if values else None, "maxRead": max(values) if values else None,
                          "windowScanned": complete, "sampleLimited": len(chosen) >= plan.get("articlesPerAccount", 10),
                          "comparison": "选中样本；累计阅读受文章年龄影响，不表示粉丝或增长率"})
    ranked = sorted(articles.values(), key=lambda r: r.get("metrics", {}).get("readNum") or -1, reverse=True)
    for row in ranked[:plan.get("deepReadCount", 5)]:
        url = row.get("canonicalUrl") or row.get("url")
        if not url:
            continue
        try:
            data = job.call(CONTENT, {"url": url, "format": "text"},
                            lambda d: {"text": d.get("content", {}).get("text", "") if isinstance(d.get("content"), dict)
                                       else str(d.get("content") or ""), "article": select(d.get("article") or {}, ("title", "accountName"))})
            row["text"] = data["text"]
        except (APIError, ValueError) as e:
            errors.append({"stage": "content", "evidenceId": row["evidenceId"], "message": str(e)})
    return {"kind": "competitors", "capturedAt": now(), "scope": plan, "articles": list(articles.values()),
            "accounts": summaries, "errors": errors, "cost": job.totals()}


THEMES = {"价格与购买方式": r"多少[钱元]|价格|怎么买|哪里买|链接|贵|便宜",
          "方法与使用疑问": r"怎么|如何|为什么|请问|教程|步骤|不会|[？?]",
          "效果与使用反馈": r"用了|用过|效果|没用|有用|失败|成功|体验",
          "希望补充内容": r"想看|讲讲|能不能|求|再出|下一期|详细"}


def render(directory, data, analysis_path=None):
    data = public_data(data)
    kind = data["kind"]
    records = data["comments"] if kind == "comments" else data["articles"]
    facts_hash = digest(data)
    analysis_input = {"factsHash": facts_hash, "kind": kind, "scope": data["scope"], "records": records,
                      "instruction": "分析公开内容，结论引用 evidenceId；不编造数字，不将评论者推断为潜在客户。findings 每项包含 finding/action/evidenceIds。"}
    atomic_json(Path(directory) / "analysis-input.json", analysis_input)
    evidence_ids = {r["evidenceId"] for r in records}
    findings = analysis_text(analysis_path, evidence_ids, facts_hash)
    cost = data["cost"]
    notes = ["采集时间：" + data["capturedAt"], "已确认接口费用：%.6f 元" % (cost["confirmedMicros"] / 1000000),
             "结果不明的费用预留：%.6f 元（不代表已扣费或已退款）" % (cost["unconfirmedReserveMicros"] / 1000000),
             "费用不包含 AI 宿主/模型使用费。", "数据为本次有限样本，未知值不按 0 统计。",
             "采集存在部分失败" if data["errors"] else "采集按计划完成；数量或页数上限不代表全量数据。",
             "含证据分析已导入" if findings else "数据已就绪，AI 解读待生成；使用 analysis-input.json 完成分析后重渲染，无需再次采集。"]
    if kind == "comments":
        themes = []
        for name, pattern in THEMES.items():
            matches = [r for r in records if re.search(pattern, str(r.get("content", "")))]
            themes.append({"规则初筛主题": name, "命中去重评论数": len(matches),
                           "证据编号": [r["evidenceId"] for r in matches], "口径": "关键词规则，可多标签，不是 AI 判断或全体用户比例"})
        notes.append("一级评论数量上限与二级回复范围分别设置；评论点赞保持原义，不套用作品指标映射。")
        sheets = {"作品清单": data["videos"], "评论明细": records, "主题初筛": themes,
                  "采集状态": data["states"], "失败明细": data["errors"]}
        title = "视频号评论洞察"
    else:
        sheets = {"账号对比": data["accounts"], "文章明细": [{k: v for k, v in r.items() if k != "text"} for r in records],
                  "精读内容": [{"evidenceId": r["evidenceId"], "title": r.get("title"), "text": r["text"]}
                              for r in records if "text" in r], "失败明细": data["errors"]}
        title = "公众号同行对标"
        notes.append("无历史快照不计算增长；10万+不纳入精确阅读中位数；报告不推断真实粉丝规模。")
    files = export_bundle(directory, title, sheets, notes, data, findings)
    return {"files": files, "analysisInput": str((Path(directory) / "analysis-input.json").resolve()),
            "status": "analyzed" if findings else "collected_needs_analysis" if records else "no_data", "partial": bool(data["errors"]), "cost": cost}


def main(kind):
    parser = argparse.ArgumentParser(description="曼格云：有限采集、断点恢复、费用与证据报告")
    parser.add_argument("--plan", help="JSON 采集计划")
    parser.add_argument("--workspace", required=True, help="本任务工作区；恢复使用同一路径，刷新使用新目录")
    parser.add_argument("--estimate", action="store_true")
    parser.add_argument("--budget", help="本任务最多使用多少元；执行必须指定")
    parser.add_argument("--yes", action="store_true", help="用户已同意当前范围和预算")
    parser.add_argument("--render", action="store_true", help="只重渲染已采数据，不联网")
    parser.add_argument("--analysis", help="分析 JSON：factsHash + findings[{finding,action,evidenceIds}]")
    args = parser.parse_args()
    directory = Path(args.workspace)
    try:
        if args.render:
            with workspace_lock(directory):
                output = render(directory, read_json(directory / "evidence.json"), args.analysis)
        else:
            if not args.plan:
                raise ValueError("需要 --plan")
            plan = validate_plan(read_json(args.plan), kind)
            api = API(require_key=not args.estimate)
            quote = estimate(api, plan, kind)
            print(json.dumps({"estimate": quote}, ensure_ascii=False))
            if args.estimate:
                return 0
            if not args.yes or args.budget is None:
                raise ValueError("请在用户同意本次范围与金额后传 --yes --budget 金额；未发起采集")
            excel_ready()
            with workspace_lock(directory):
                job = Job(directory, api, {"kind": kind, "plan": plan}, micros(args.budget))
                data = collect_comments(job, plan) if kind == "comments" else collect_competitors(job, plan)
                output = render(directory, data, args.analysis)
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0 if not output["partial"] else 5
    except (ValueError, APIError, OSError) as e:
        print(str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main("comments"))
