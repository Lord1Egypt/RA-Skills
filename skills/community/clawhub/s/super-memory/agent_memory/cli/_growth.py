"""Growth: achievements, share-card, annual-report, growth-feedback."""

from __future__ import annotations

import json
from argparse import Namespace
from datetime import datetime

from agent_memory.cli._utils import get_memory


def cmd_annual_report(args):
    """生成记忆年报（Spotify Wrapped 风格）"""
    mem = get_memory()
    try:
        from agent_memory.growth.annual_report import AnnualReportGenerator
        generator = AnnualReportGenerator(mem.store)

        year = args.year if args.year else None

        if args.html:
            html = generator.generate_html_report(year=year)
            output_path = args.output or f"annual_report_{year or datetime.now().year}.html"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"📄 年报已生成: {output_path}")
        elif args.share_card:
            html = generator.generate_share_card(year=year)
            output_path = args.output or f"annual_card_{year or datetime.now().year}.html"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"🃏 分享卡片已生成: {output_path}")
        else:
            report = generator.generate_report(year=year)
            print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def cmd_achievements(args):
    """查看成就徽章"""
    mem = get_memory()
    try:
        from agent_memory.growth.achievements import AchievementSystem
        system = AchievementSystem(mem.store)

        if args.check:
            # Compute stats and check for new achievements
            stats = system.compute_stats()
            newly_unlocked = system.check_achievements(stats)
            if newly_unlocked:
                print(f"🎉 解锁新成就！")
                for a in newly_unlocked:
                    print(f"   {a['icon']} {a['name']} — {a['description']}")
            else:
                print("暂无新成就解锁")
        else:
            # List all achievements
            achievements = system.get_achievements()
            unlocked = sum(1 for a in achievements if a["unlocked"])
            total = len(achievements)
            print(f"🏆 成就进度: {unlocked}/{total}")
            print()
            for a in achievements:
                status = "✅" if a["unlocked"] else "🔒"
                if a["unlocked"]:
                    dt = datetime.fromtimestamp(a["unlocked_at"]).strftime("%Y-%m-%d")
                    print(f"  {status} {a['icon']} {a['name']} — {a['description']} ({dt})")
                else:
                    print(f"  {status} {a['icon']} {a['name']} — {a['description']}")
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def cmd_growth_feedback(args):
    """提交检索反馈（影响未来检索排序）"""
    mem = get_memory()
    try:
        from agent_memory.growth.feedback import FeedbackLoop
        feedback = FeedbackLoop(mem.store)

        rating = 1 if args.useful else -1
        query = args.query or ""
        feedback.submit_feedback(
            memory_id=args.memory_id,
            query=query,
            rating=rating,
        )
        action = "👍 标记为有用" if rating == 1 else "👎 标记为没用"
        print(f"{action}: {args.memory_id}")

        if args.stats:
            stats = feedback.get_feedback_stats()
            print(f"\n📊 反馈统计:")
            print(f"   总反馈: {stats['total']}")
            print(f"   正面: {stats['positive']} | 负面: {stats['negative']}")
            print(f"   涉及记忆: {stats['unique_memories']} 条")
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def cmd_share_card(args):
    """生成可分享的洞察卡片"""
    mem = get_memory()
    try:
        from agent_memory.growth.share_card import ShareCardGenerator
        generator = ShareCardGenerator(mem.store)

        if args.query:
            # Recall + share card
            result = mem.recall(query=args.query, limit=5)
            if hasattr(result, 'to_dict'):
                result = result.to_dict()
            elif not isinstance(result, dict):
                result = {"total": 0, "primary": []}
            results = result.get("primary", [])
            html = generator.generate_recall_card(args.query, results)
        else:
            # Stats card
            html = generator.generate_stat_card()

        output_path = args.output or "share_card.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"🃏 分享卡片已生成: {output_path}")
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()
