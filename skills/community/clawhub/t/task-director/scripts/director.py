#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
task-director — 任务导演系统 / Task Director

把复杂任务编排成电影剧本，分镜确认后再执行。
Organize complex tasks into a storyboard. Review, approve, then execute.

Usage:
  python director.py create --title "..." --scenes scenes.json
  python director.py show [--id MOVIE_ID]
  python director.py approve [--id MOVIE_ID]
  python director.py action [--id MOVIE_ID] [--scene N] [--shot N]
  python director.py cut [--id MOVIE_ID]
  python director.py wrap [--id MOVIE_ID]
  python director.py status [--id MOVIE_ID]
  python director.py list
"""

import json, sys, time, argparse, os
from pathlib import Path
from datetime import datetime, timezone, timedelta
from copy import deepcopy

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def get_data_dir():
    d = Path.home() / ".openclaw" / "memory" / "movies"
    d.mkdir(parents=True, exist_ok=True)
    return d


def gen_id():
    return f"movie_{int(time.time() * 1000) % 10000000:07d}"


def now_iso():
    return datetime.now(timezone(timedelta(hours=8))).isoformat()


def load_movie(movie_id):
    f = get_data_dir() / f"{movie_id}.json"
    if not f.exists():
        return None
    return json.loads(f.read_text(encoding="utf-8"))


def save_movie(movie):
    f = get_data_dir() / f"{movie['id']}.json"
    f.write_text(json.dumps(movie, ensure_ascii=False, indent=2), encoding="utf-8")


def all_movies():
    d = get_data_dir()
    movies = []
    for f in sorted(d.glob("movie_*.json"), reverse=True):
        try:
            movies.append(json.loads(f.read_text(encoding="utf-8")))
        except:
            continue
    return movies


def find_active():
    """Find the most recent non-wrapped movie."""
    for m in all_movies():
        if m["status"] not in ("wrapped",):
            return m
    return None


# ────────────────────────────────────────
# Display
# ────────────────────────────────────────

STATUS_ICONS = {
    "draft": "📝",
    "approved": "✅",
    "filming": "🎬",
    "cut": "⏸️",
    "wrapped": "🎉",
}

SHOT_ICONS = {
    "pending": "⬜",
    "running": "🔄",
    "done": "✅",
    "ng": "❌",
    "skipped": "⏭️",
    "fallback": "🎭",
}


def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}min"
    else:
        return f"{seconds/3600:.1f}h"


def display_movie(movie, verbose=False):
    icon = STATUS_ICONS.get(movie["status"], "❓")
    print(f"\n{'='*60}")
    print(f"{icon} 《{movie['title']}》  [{movie['status'].upper()}]")
    print(f"   ID: {movie['id']}")
    print(f"   Created: {movie.get('created_at', '?')[:16]}")
    if movie.get("started_at"):
        print(f"   Started: {movie['started_at'][:16]}")
    if movie.get("finished_at"):
        print(f"   Finished: {movie['finished_at'][:16]}")
    print(f"{'='*60}")

    total_shots = 0
    done_shots = 0
    ng_shots = 0

    for si, scene in enumerate(movie.get("scenes", []), 1):
        scene_icon = "✅" if all(
            s["status"] in ("done", "skipped") for s in scene.get("shots", [])
        ) else "🎬" if scene.get("shots") and any(
            s["status"] == "running" for s in scene.get("shots", [])
        ) else "⬜"

        print(f"\n  {scene_icon} 第{si}幕: {scene['name']}")
        if scene.get("description") and verbose:
            print(f"     {scene['description']}")
        if scene.get("estimated_time"):
            print(f"     ⏱️ 预计: {scene['estimated_time']}")

        for j, shot in enumerate(scene.get("shots", []), 1):
            total_shots += 1
            shot_icon = SHOT_ICONS.get(shot["status"], "❓")
            if shot["status"] == "done":
                done_shots += 1
            elif shot["status"] == "ng":
                ng_shots += 1

            action_str = shot["action"]
            if len(action_str) > 50 and not verbose:
                action_str = action_str[:47] + "..."

            print(f"     {shot_icon} {si}.{j} {action_str}")

            if shot.get("command") and verbose:
                print(f"        $ {shot['command']}")
            if shot.get("output") and shot["status"] in ("done", "ng", "fallback"):
                output = shot["output"].strip()
                if len(output) > 100 and not verbose:
                    output = output[:97] + "..."
                for line in output.split("\n")[:3]:
                    print(f"        │ {line}")
            if shot.get("fallback") and shot["status"] == "ng":
                fb = shot["fallback"]
                fb_icon = SHOT_ICONS.get(fb.get("status", "pending"), "❓")
                print(f"        🎭 备选: {fb['action']} [{fb_icon}]")
                if fb.get("output") and fb["status"] in ("done", "ng"):
                    for line in fb["output"].strip().split("\n")[:2]:
                        print(f"           │ {line}")

    if total_shots > 0:
        print(f"\n  📊 进度: {done_shots}/{total_shots} 完成", end="")
        if ng_shots:
            print(f" | {ng_shots} 失败", end="")
        pct = done_shots / total_shots * 100
        bar_len = 20
        filled = int(bar_len * pct / 100)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"\n  [{bar}] {pct:.0f}%")

    if movie.get("notes"):
        print(f"\n  📝 导演笔记:")
        for note in movie["notes"][-5:]:
            print(f"     {note}")


# ────────────────────────────────────────
# Commands
# ────────────────────────────────────────

def cmd_create(args):
    """Create a new movie (task plan)."""
    scenes_file = args.scenes
    if scenes_file and Path(scenes_file).exists():
        scenes = json.loads(Path(scenes_file).read_text(encoding="utf-8"))
    elif scenes_file:
        # Try parsing as inline JSON
        scenes = json.loads(scenes_file)
    else:
        print("Error: --scenes required (file path or inline JSON)")
        return

    # Validate and normalize scenes
    for i, scene in enumerate(scenes):
        scene.setdefault("name", f"Scene {i+1}")
        scene.setdefault("description", "")
        scene.setdefault("estimated_time", "")
        for j, shot in enumerate(scene.get("shots", [])):
            shot.setdefault("action", f"Shot {j+1}")
            shot.setdefault("command", "")
            shot.setdefault("status", "pending")
            shot.setdefault("output", "")
            if "fallback" in shot:
                shot["fallback"].setdefault("status", "pending")
                shot["fallback"].setdefault("output", "")

    movie = {
        "id": gen_id(),
        "title": args.title,
        "created_at": now_iso(),
        "started_at": None,
        "finished_at": None,
        "status": "draft",
        "scenes": scenes,
        "current_scene": 0,
        "current_shot": 0,
        "notes": [],
    }

    save_movie(movie)
    print(f"📝 剧本已创建: {movie['id']}")
    display_movie(movie)


def cmd_show(args):
    """Show movie details."""
    movie_id = args.id or (find_active()["id"] if find_active() else None)
    if not movie_id:
        print("No active movie found.")
        return
    movie = load_movie(movie_id)
    if not movie:
        print(f"Movie not found: {movie_id}")
        return
    display_movie(movie, verbose=True)


def cmd_approve(args):
    """Approve a draft movie to start filming."""
    movie_id = args.id or (find_active()["id"] if find_active() else None)
    if not movie_id:
        print("No active movie found.")
        return
    movie = load_movie(movie_id)
    if not movie:
        print(f"Movie not found: {movie_id}")
        return
    if movie["status"] != "draft":
        print(f"Cannot approve: status is {movie['status']}")
        return
    movie["status"] = "approved"
    movie["notes"].append(f"[{now_iso()[:16]}] 剧本通过审核，准备开机")
    save_movie(movie)
    print(f"✅ 剧本已批准！运行 `action` 开机拍摄")


def cmd_action(args):
    """Execute the next shot (or a specific shot)."""
    movie_id = args.id or (find_active()["id"] if find_active() else None)
    if not movie_id:
        print("No active movie found.")
        return
    movie = load_movie(movie_id)
    if not movie:
        print(f"Movie not found: {movie_id}")
        return
    if movie["status"] not in ("approved", "filming"):
        print(f"Cannot action: status is {movie['status']}")
        return

    movie["status"] = "filming"
    if not movie.get("started_at"):
        movie["started_at"] = now_iso()

    # Find target shot
    if args.scene is not None and args.shot is not None:
        si = args.scene - 1
        ji = args.shot - 1
    else:
        # Find next pending shot
        si, ji = None, None
        for i, scene in enumerate(movie["scenes"]):
            for j, shot in enumerate(scene.get("shots", [])):
                if shot["status"] == "pending":
                    si, ji = i, j
                    break
                elif shot["status"] == "ng" and shot.get("fallback", {}).get("status") == "pending":
                    si, ji = i, j
                    break
            if si is not None:
                break

    if si is None:
        print("🎉 All shots completed! Run `wrap` to finish.")
        return

    scene = movie["scenes"][si]
    shot = scene["shots"][ji]

    # Check if we should try fallback instead
    if shot["status"] == "ng" and shot.get("fallback", {}).get("status") == "pending":
        fb = shot["fallback"]
        print(f"🎭 尝试备选方案: {si+1}.{ji+1} {fb['action']}")
        fb["status"] = "running"
        save_movie(movie)
        # Return info for the agent to execute
        print(json.dumps({
            "movie_id": movie["id"],
            "scene": si + 1,
            "shot": ji + 1,
            "action": fb["action"],
            "command": fb.get("command", ""),
            "is_fallback": True,
        }, ensure_ascii=False))
        return

    print(f"🎬 Action! 第{si+1}幕 第{ji+1}个镜头: {shot['action']}")
    shot["status"] = "running"
    movie["current_scene"] = si
    movie["current_shot"] = ji
    save_movie(movie)

    # Return shot info for the agent to execute
    print(json.dumps({
        "movie_id": movie["id"],
        "scene": si + 1,
        "shot": ji + 1,
        "action": shot["action"],
        "command": shot.get("command", ""),
        "is_fallback": False,
    }, ensure_ascii=False))


def cmd_result(args):
    """Record the result of the current shot."""
    movie = load_movie(args.id)
    if not movie:
        print(f"Movie not found: {args.id}")
        return

    si = movie.get("current_scene", 0)
    ji = movie.get("current_shot", 0)
    scene = movie["scenes"][si]
    shot = scene["shots"][ji]

    if args.fallback:
        if not shot.get("fallback"):
            print("No fallback defined for this shot")
            return
        fb = shot["fallback"]
        fb["status"] = args.outcome
        fb["output"] = args.output or ""
        if args.outcome == "done":
            shot["status"] = "fallback"
            shot["output"] = f"备选方案成功: {fb['action']}"
            print(f"🎭 备选方案成功！")
        else:
            print(f"❌ 备选方案也失败了")
    else:
        shot["status"] = args.outcome
        shot["output"] = args.output or ""
        if args.outcome == "ng" and shot.get("fallback"):
            print(f"❌ 失败，但有备选方案可用。运行 `action` 重试备选")
        elif args.outcome == "ng":
            print(f"❌ 失败，无备选方案")

    save_movie(movie)

    # Check if all done
    all_done = all(
        s["status"] in ("done", "skipped", "fallback")
        for sc in movie["scenes"]
        for s in sc.get("shots", [])
    )
    if all_done:
        print("🎉 所有镜头完成！可以运行 `wrap` 杀青")


def cmd_cut(args):
    """Pause filming."""
    movie_id = args.id or (find_active()["id"] if find_active() else None)
    if not movie_id:
        print("No active movie found.")
        return
    movie = load_movie(movie_id)
    if not movie:
        print(f"Movie not found: {movie_id}")
        return
    movie["status"] = "cut"
    movie["notes"].append(f"[{now_iso()[:16]}] 导演喊卡，暂停拍摄")
    save_movie(movie)
    print("⏸️ 拍摄暂停。运行 `action` 继续")


def cmd_wrap(args):
    """Finish the movie."""
    movie_id = args.id or (find_active()["id"] if find_active() else None)
    if not movie_id:
        print("No active movie found.")
        return
    movie = load_movie(movie_id)
    if not movie:
        print(f"Movie not found: {movie_id}")
        return

    movie["status"] = "wrapped"
    movie["finished_at"] = now_iso()

    # Calculate stats
    total = sum(len(sc.get("shots", [])) for sc in movie["scenes"])
    done = sum(
        1 for sc in movie["scenes"]
        for s in sc.get("shots", [])
        if s["status"] in ("done", "skipped", "fallback")
    )
    ng = sum(
        1 for sc in movie["scenes"]
        for s in sc.get("shots", [])
        if s["status"] == "ng"
    )

    if movie.get("started_at"):
        start = datetime.fromisoformat(movie["started_at"])
        end = datetime.fromisoformat(movie["finished_at"])
        elapsed = (end - start).total_seconds()
        movie["notes"].append(
            f"[{now_iso()[:16]}] 杀青！耗时 {format_time(elapsed)}，"
            f"完成 {done}/{total}，失败 {ng}"
        )

    save_movie(movie)
    display_movie(movie)
    print(f"\n🎉 杀青！《{movie['title']}》拍摄完成")


def cmd_status(args):
    """Show current status."""
    movie_id = args.id or (find_active()["id"] if find_active() else None)
    if not movie_id:
        print("No active movie found.")
        return
    movie = load_movie(movie_id)
    if not movie:
        print(f"Movie not found: {movie_id}")
        return
    display_movie(movie)


def cmd_list(args):
    """List all movies."""
    movies = all_movies()
    if not movies:
        print("No movies found.")
        return
    print(f"\n{'🎬'*3} 剧本列表 {'🎬'*3}\n")
    for m in movies:
        icon = STATUS_ICONS.get(m["status"], "❓")
        total = sum(len(sc.get("shots", [])) for sc in m["scenes"])
        done = sum(
            1 for sc in m["scenes"]
            for s in sc.get("shots", [])
            if s["status"] in ("done", "skipped", "fallback")
        )
        print(f"  {icon} [{m['id']}] 《{m['title']}》 {done}/{total} - {m['status']}")
        print(f"     {m.get('created_at', '?')[:16]}")


def cmd_skip(args):
    """Skip a shot."""
    movie_id = args.id or (find_active()["id"] if find_active() else None)
    if not movie_id:
        print("No active movie found.")
        return
    movie = load_movie(movie_id)
    if not movie:
        return

    si = args.scene - 1 if args.scene else movie.get("current_scene", 0)
    ji = args.shot - 1 if args.shot else movie.get("current_shot", 0)

    shot = movie["scenes"][si]["shots"][ji]
    shot["status"] = "skipped"
    shot["output"] = args.reason or "跳过"
    save_movie(movie)
    print(f"⏭️ 跳过: {si+1}.{ji+1} {shot['action']}")


# ────────────────────────────────────────
# Main
# ────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="director",
        description="Task Director / 任务导演",
    )
    sub = parser.add_subparsers(dest="command")

    # create
    p = sub.add_parser("create", help="Create a new movie (task plan)")
    p.add_argument("--title", required=True, help="Movie title / 任务标题")
    p.add_argument("--scenes", required=True, help="Scenes JSON file or inline JSON")

    # show
    p = sub.add_parser("show", help="Show movie details")
    p.add_argument("--id", default=None)

    # approve
    p = sub.add_parser("approve", help="Approve a draft movie")
    p.add_argument("--id", default=None)

    # action
    p = sub.add_parser("action", help="Execute next shot")
    p.add_argument("--id", default=None)
    p.add_argument("--scene", type=int, default=None)
    p.add_argument("--shot", type=int, default=None)

    # result
    p = sub.add_parser("result", help="Record shot result")
    p.add_argument("--id", required=True)
    p.add_argument("--outcome", required=True, choices=["done", "ng", "skipped"])
    p.add_argument("--output", default="")
    p.add_argument("--fallback", action="store_true")

    # cut
    p = sub.add_parser("cut", help="Pause filming")
    p.add_argument("--id", default=None)

    # wrap
    p = sub.add_parser("wrap", help="Finish the movie")
    p.add_argument("--id", default=None)

    # status
    p = sub.add_parser("status", help="Show status")
    p.add_argument("--id", default=None)

    # list
    sub.add_parser("list", help="List all movies")

    # skip
    p = sub.add_parser("skip", help="Skip a shot")
    p.add_argument("--id", default=None)
    p.add_argument("--scene", type=int, default=None)
    p.add_argument("--shot", type=int, default=None)
    p.add_argument("--reason", default="")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    cmds = {
        "create": cmd_create,
        "show": cmd_show,
        "approve": cmd_approve,
        "action": cmd_action,
        "result": cmd_result,
        "cut": cmd_cut,
        "wrap": cmd_wrap,
        "status": cmd_status,
        "list": cmd_list,
        "skip": cmd_skip,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
