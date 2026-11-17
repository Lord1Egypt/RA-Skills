"""second-reality-video CLI（Phase 0）。

子命令
------
  extract  世界 → states.jsonl（每 tick 一个 FrameState，含 content_digest）
  scene    states.jsonl + ShotGraph → scene_ir.jsonl + 结构验收报告（不渲染）
  bake-assets  states.jsonl → 离线烘焙资产目录（常量 + 哈希清单）
  render   states.jsonl + ShotGraph → mp4 + hashes.txt + frames.jsonl（+抽样 PNG）
  attest   mp4 + hashes + states → manifest.json（真跑审计，不预置结论）
  verify   由 manifest 记录的创世参数独立重建世界，与产物逐帧比对

设计约束
--------
- 帧走 rawvideo 管道直送 ffmpeg，不落盘 PNG 序列 —— 旧实现因帧号与音频序列
  不一致产出过 0.37 秒废片，管道消除了这一整类失败。
- 复现要求 data_dir 为空：世界存储是有状态的，复用它会让第二次运行读到
  已注册的灵魂。verify 用临时目录，不触碰用户目录。
- 1 tick → frames_per_tick 帧；位置线性插值，needs/relationships 阶梯保持
  （不插值，避免伪造状态）。
"""

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).parent.parent))

DEFAULT_TPS = 10
DEFAULT_FPS = 30


# ---------------------------------------------------------------- helpers

def _parse_range(spec: str) -> tuple:
    parts = spec.split('-')
    tick_from = int(parts[0])
    tick_to = int(parts[1]) if len(parts) > 1 else tick_from
    if tick_to < tick_from:
        raise SystemExit(f"invalid tick range: {spec}")
    return tick_from, tick_to


def _load_shot_graph(path: str):
    from video.shot_graph import ShotGraph
    if path.endswith(".yaml") or path.endswith(".yml"):
        return ShotGraph.from_yaml(path)
    return ShotGraph.from_json(path)


def _resolve_framing(shot_graph) -> tuple:
    """全片必须统一分辨率 —— rawvideo 管道是单一像素格式的流。"""
    resolutions = {
        tuple(s.get("framing", {}).get("resolution", [1920, 1080]))
        for s in shot_graph.shots
    }
    if len(resolutions) != 1:
        raise SystemExit(
            f"all shots must share one resolution for a rawvideo stream, got {resolutions}"
        )
    width, height = resolutions.pop()
    fps = shot_graph.shots[0].get("framing", {}).get("fps", DEFAULT_FPS)
    return int(width), int(height), int(fps)


def _pick_shot(shot_graph, tick: int):
    shots = shot_graph.get_shots_for_tick(tick)
    if not shots:
        raise SystemExit(f"no shot covers tick {tick} — ShotGraph must cover the tick range")
    return shots[0]


def _interpolate(states, index, sub, frames_per_tick):
    """按子帧插值出一个 FrameState：位置线性插值，needs 阶梯保持。"""
    current = states[index]
    nxt = states[index + 1] if index + 1 < len(states) else current
    ratio = sub / float(frames_per_tick)

    souls = {}
    for soul in sorted(current["souls"]):
        cur = current["souls"][soul]
        fut = nxt["souls"].get(soul, cur)
        pos = [
            round(a + (b - a) * ratio, 6)
            for a, b in zip(cur["position"], fut["position"])
        ]
        souls[soul] = {
            "position": pos,
            "needs": cur["needs"],
            "relationships": cur["relationships"],
        }

    frame_state = dict(current)
    frame_state["souls"] = souls
    return frame_state, current["content_digest"]


def _build_assets(souls, genesis_seed, out_path):
    """生成并持久化外观资产（身份恒定的可审计证据）。

    资产本身由 `identity_assets.build_assets` 确定性派生；这里只负责落盘，
    使第 29 维（身份恒定）有独立可查的产物。
    """
    from video.identity_assets import IdentityAssetRegistry, build_assets
    registry = IdentityAssetRegistry(storage_path=str(out_path))
    assets = build_assets(souls, genesis_seed)
    for soul in sorted(assets):
        registry.register(soul, assets[soul])
    return assets


def _audit_world(world_id: str, genesis_seed: int, agent_count: int, tick_to: int):
    """在同一确定性路径上重建世界并**实际执行**审计。"""
    from system.runtime import World
    from system.keys import build_genesis_proof
    from system.ledger import derive_soul_hash
    from video.state_feed import deterministic_soul_secret
    from audit_engine import SecondPerspectiveAuditor

    tmp_dir = tempfile.mkdtemp(prefix="nohn-audit-")
    world = World(world_id=world_id, data_dir=tmp_dir, genesis_seed=genesis_seed)
    for i in range(agent_count):
        secret = deterministic_soul_secret(genesis_seed, i)
        proof = build_genesis_proof(secret, {"genesis_id": f"agent-{i}"})
        world.spawn_agent(soul_hash=derive_soul_hash(proof), genesis_proof=proof)
    for _ in range(tick_to):
        world.tick()

    report = SecondPerspectiveAuditor().audit_world(world)
    summary = report.summary()
    verdict = "FAILED" if "FAILED" in summary else "PASS"
    return report, len(report.FIELDS), verdict, summary


# ---------------------------------------------------------------- commands

def cmd_extract(args):
    """世界 → FrameState 序列。"""
    from video.state_feed import derive_states, save_states

    tick_from, tick_to = _parse_range(args.ticks)
    print(f"=== extract: world_id={args.world_id} seed={args.seed} "
          f"agents={args.agents} ticks={tick_from}-{tick_to} ===")

    states = derive_states(args.world_id, args.seed, args.world,
                           args.agents, tick_from, tick_to)
    save_states(states, args.out)

    digests = [s["content_digest"] for s in states]
    unique = len(set(digests))
    print(f"  content_digest: {unique} unique / {len(digests)} ticks")
    print(f"  state_root: {len(set(s['state_root'] for s in states))} unique "
          f"(contains HLC wall-clock — auxiliary only)")
    print(f"  souls: {len(states[0]['souls'])}")


def cmd_bake_assets(args):
    """把外观资产固化为仓库常量（离线烘焙，Tier 2 的资产环节）。"""
    from video.state_feed import load_states
    from video.identity_assets import build_assets
    from video.baked_assets import bake_assets, asset_source

    states = load_states(args.state)
    if not states:
        raise SystemExit("no states in {0}".format(args.state))

    assets = build_assets(states[0]["souls"], states[0]["genesis_seed"])
    manifest = bake_assets(assets, args.out_dir)

    print("=== bake-assets: {0} assets ===".format(manifest["asset_count"]))
    print("  digest : {0}...".format(str(manifest["digest"])[:32]))
    print("  source : {0}".format(asset_source(manifest)))
    print("  out    : {0}".format(args.out_dir))
    return 0


def cmd_scene(args):
    """FrameState → Scene IR + 结构验收（不渲染像素）。

    这是逻辑层与像素层之间那条合同的独立入口：渲染器还没换，也能先证明
    「谁在哪、身份是谁、相机怎么摆」是可 diff、可断言、可复现的。
    """
    from video.state_feed import load_states
    from video.identity_assets import build_assets
    from video.scene_ir import compile_scene_ir, write_scene_ir
    from video.structure import validate_scene_sequence, format_report
    from video.render.frame import check_render_independence

    states = load_states(args.state)
    if not states:
        raise SystemExit("no states in {0}".format(args.state))

    shot_graph = _load_shot_graph(args.shot)
    assets = build_assets(states[0]["souls"], states[0]["genesis_seed"])

    irs = []
    for index, state in enumerate(states):
        shot = _pick_shot(shot_graph, state["tick"])
        irs.append(compile_scene_ir(state, shot, assets=assets,
                                    frame_index=index, sub=0))

    digest = write_scene_ir(irs, args.out)
    result = validate_scene_sequence(irs, max_step=args.max_step)
    report = format_report(result, scene_digest=digest)

    # 维度 31：渲染层无时序上下文（静态、确定性）
    contract = check_render_independence(scene_ir=irs[0] if irs else None)
    report += "\n=== 渲染层契约 / 维度 31 ===\n"
    report += "render entry    : {0}\n".format(contract["render_entry"])
    report += "checked         : {0}\n".format(", ".join(contract["checked"]) or "—")
    report += "violations      : {0}\n".format(len(contract["violations"]))
    report += "VERDICT         : {0}\n".format(
        "PASS" if contract["ok"] else "FAIL")
    for message in contract["violations"]:
        report += "[ERROR]   {0}\n".format(message)
    report += "\n"

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")

    ok = result["ok"] and contract["ok"]
    print("=== scene: {0} states → {1} Scene IR frames ===".format(
        len(states), len(irs)))
    print("  scene_ir     : {0}".format(args.out))
    print("  scene_digest : {0}...".format(digest[:32]))
    print("  structure    : {0} ({1} errors / {2} warnings)".format(
        "PASS" if result["ok"] else "FAIL",
        len(result["errors"]), len(result["warnings"])))
    print("  contract     : {0} (维度 31 · 渲染层无时序上下文)".format(
        "PASS" if contract["ok"] else "FAIL"))
    if args.report:
        print("  report       : {0}".format(args.report))
    if not ok:
        print(report)
    return 0 if ok else 1


def cmd_render(args):
    """FrameState 序列 + ShotGraph → mp4（含逐帧哈希与背书记录）。"""
    from video.state_feed import load_states
    from video.timebase import Timebase
    from video.render.deterministic import DeterministicRenderer
    from video.scene_ir import compile_scene_ir
    from video.encode import encode_raw_stream, save_frame_hashes

    if args.tier != "R1":
        raise SystemExit(
            "tier {0} 尚未实现。R2 是**无时序帧渲染器**（只吃单帧 Scene IR，"
            "不含跨帧上下文），需要训练权重 —— 教师=R1，配对数据契约见 HLD §4.3，"
            "接口契约见 MANUAL §8.1。当前可用的只有 R1（确定性、逐字节可复现）。"
            .format(args.tier))

    states = load_states(args.state)
    shot_graph = _load_shot_graph(args.shot)
    width, height, fps = _resolve_framing(shot_graph)
    timebase = Timebase(tps=DEFAULT_TPS, fps=fps)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    assets = _build_assets(states[0]["souls"].keys(), states[0]["genesis_seed"],
                           out_path.parent / "identity_assets.json")
    renderer = DeterministicRenderer(assets=assets)

    print(f"=== render: {len(states)} states → {timebase.frames_per_tick} frames/tick "
          f"→ {len(states) * timebase.frames_per_tick} frames @ {width}x{height} {fps}fps "
          f"(input contract: scene_ir) ===")

    records = []
    samples = []
    total_frames = len(states) * timebase.frames_per_tick
    # 抽样点均匀铺满全片（只取前 N 帧会看不到镜头切换之后的样子）
    sample_indices = {
        int(i * (total_frames - 1) / (args.samples - 1))
        for i in range(args.samples)
    } if args.samples > 1 else ({0} if args.samples == 1 else set())

    def frame_stream():
        for index in range(len(states)):
            tick = states[index]["tick"]
            shot = _pick_shot(shot_graph, tick)
            for sub in range(timebase.frames_per_tick):
                frame_state, digest = _interpolate(
                    states, index, sub, timebase.frames_per_tick
                )
                frame_index = index * timebase.frames_per_tick + sub
                scene_ir = compile_scene_ir(frame_state, shot, assets=assets,
                                            frame_index=frame_index, sub=sub)
                buffer = renderer.render_ir(scene_ir)
                records.append({
                    "frame_index": frame_index,
                    "tick": tick,
                    "sub": sub,
                    "content_digest": digest,
                    "backing": "deterministic",
                })
                if frame_index in sample_indices:
                    samples.append((frame_index, buffer))
                yield buffer

    hashes = encode_raw_stream(frame_stream(), str(out_path), width, height, fps)

    hashes_path = out_path.parent / "hashes.txt"
    hashes_digest = save_frame_hashes(hashes, str(hashes_path))

    frames_path = out_path.parent / "frames.jsonl"
    with open(frames_path, 'w', encoding='utf-8') as f:
        for record, h in zip(records, hashes):
            record = dict(record)
            record["frame_sha256"] = h
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + '\n')

    for frame_index, buffer in samples:
        _write_sample_png(buffer, width, height,
                          out_path.parent / f"sample_{frame_index:05d}.png")

    print(f"  frames written : {len(hashes)}")
    print(f"  frame_hashes_digest: {hashes_digest[:32]}...")
    print(f"  hashes         : {hashes_path}")
    print(f"  frames manifest: {frames_path}")


def _write_sample_png(buffer: bytes, width: int, height: int, path: Path):
    """落盘一张抽样 PNG，供人工目视核对（不参与编码链路）。"""
    try:
        import pygame
        if not pygame.get_init():
            pygame.init()
        surface = pygame.image.frombytes(buffer, (width, height), "RGB")
        pygame.image.save(surface, str(path))
    except Exception as exc:
        print(f"  (sample PNG skipped: {exc})")


def cmd_attest(args):
    """生成凭证：填入真实字段 + 真跑审计 + 可验签名。"""
    from video.state_feed import load_states
    from video.encode import load_frame_hashes, hashes_digest
    from video.manifest import RenderManifest, compute_video_hash, deterministic_signing_key

    states = load_states(args.state)
    hashes = load_frame_hashes(args.hashes)
    shot_graph = _load_shot_graph(args.shot)

    print(f"=== attest: {len(hashes)} frame hashes ===")

    manifest = RenderManifest()
    manifest.set_world_info(
        world_id=states[0]["world_id"],
        genesis_seed=states[0]["genesis_seed"],
        state_root_start=states[0]["state_root"],
        state_root_end=states[-1]["state_root"],
    )
    manifest.set_world_params(
        agent_count=len(states[0]["souls"]),
        tick_from=states[0]["tick"],
        tick_to=states[-1]["tick"],
    )
    manifest.set_content_anchors(
        digest_start=states[0]["content_digest"],
        digest_end=states[-1]["content_digest"],
        frame_hashes_digest=hashes_digest(hashes),
        frame_count=len(hashes),
    )
    manifest.set_frame_backing(total_frames=len(hashes), unbacked_frames=0)

    from video.identity_assets import build_assets, assets_digest
    from video.scene_ir import compile_scene_ir, scene_ir_sequence_digest
    derived_assets = build_assets(states[0]["souls"], states[0]["genesis_seed"])
    pipeline_kind = "derived-from-genesis"
    if args.baked_assets:
        from video.baked_assets import load_baked_assets
        from video.baked_assets import assets_digest as baked_assets_digest
        baked = load_baked_assets(args.baked_assets)
        if baked_assets_digest(baked) != assets_digest(derived_assets):
            raise SystemExit(
                "baked assets differ from genesis-derived assets; "
                "pixels would not replay — refusing to attest"
            )
        pipeline_kind = "offline-baked"

    manifest.set_identity_assets(
        digest=assets_digest(derived_assets),
        registry_file=str(Path(args.manifest).parent / "identity_assets.json"),
    )
    manifest.set_asset_pipeline(pipeline_kind, assets_digest(derived_assets))

    scene_irs = [
        compile_scene_ir(state, _pick_shot(shot_graph, state["tick"]),
                         assets=derived_assets, frame_index=index, sub=0)
        for index, state in enumerate(states)
    ]
    manifest.set_scene_ir(scene_ir_sequence_digest(scene_irs))

    manifest.set_pixel_tier(
        "R1-deterministic-bytes",
        "byte-exact",
        "逐帧 sha256 可逐字节复算；mp4 容器哈希仅旁证",
    )
    manifest.set_shot_graph_hash(shot_graph.hash())
    manifest.set_timebase(tps=DEFAULT_TPS, fps=shot_graph.shots[0]
                          .get("framing", {}).get("fps", DEFAULT_FPS))

    from video.render.deterministic import DeterministicRenderer
    manifest.set_renderer(DeterministicRenderer().provenance())

    video_hash = compute_video_hash(args.video)
    manifest.set_video_info(
        duration_s=len(hashes) / float(DEFAULT_FPS), video_hash=video_hash)

    report, dimensions, verdict, summary = _audit_world(
        states[0]["world_id"], states[0]["genesis_seed"],
        len(states[0]["souls"]), states[-1]["tick"],
    )
    manifest.set_audit(dimensions=dimensions, verdict=verdict, summary=summary)

    manifest.sign(deterministic_signing_key(states[0]["genesis_seed"]))
    manifest.save(args.manifest)

    audit_path = Path(args.manifest).parent / "audit_report.txt"
    audit_path.write_text(summary, encoding='utf-8')

    data = manifest.to_dict()
    print(f"  content_digest_start: {data['content_digest_start'][:32]}...")
    print(f"  frame_hashes_digest : {data['frame_hashes_digest'][:32]}...")
    print(f"  video_sha256        : {data['video_sha256'][:32]}...")
    print(f"  audit               : {data['audit']['verdict']} "
          f"({data['audit']['dimensions']} dimensions)")
    print(f"  signature           : {data['signature'][:32]}...")
    print(f"  audit report        : {audit_path}")


def cmd_verify(args):
    """第三方复验：只用 manifest 里的创世参数独立重建，比对产物。"""
    from video.state_feed import derive_states
    from video.encode import load_frame_hashes, diff_hash_sequences, hashes_digest
    from video.manifest import RenderManifest

    manifest = RenderManifest.load(args.manifest)
    data = manifest.to_dict()

    print(f"=== verify: world_id={data['world_id']} seed={data['genesis_seed']} ===")
    results = []

    sig_ok = manifest.verify()
    results.append(("manifest signature", sig_ok))
    print(f"  signature            : {'PASS' if sig_ok else 'FAIL'}")

    expected_hashes = load_frame_hashes(args.hashes)
    total_frames = data["frame_backing"]["total_frames"]
    backing_ok = (data["frame_backing"]["unbacked_frames"] == 0
                  and total_frames == len(expected_hashes))
    results.append(("frame backing (dim 30)", backing_ok))
    print(f"  frame backing        : {'PASS' if backing_ok else 'FAIL'} "
          f"({data['frame_backing']['unbacked_frames']} unbacked / {total_frames})")

    # 帧数相等不等于内容相等：frame_hashes_digest 才是像素层复现锚，必须逐字节复核。
    # 少了这一项，篡改 hashes.txt 在不传 --frames 时会被判 PASS。
    hashes_ok = hashes_digest(expected_hashes) == data["frame_hashes_digest"]
    results.append(("frame hashes digest", hashes_ok))
    print(f"  frame hashes digest  : {'PASS' if hashes_ok else 'FAIL'}")

    tmp_dir = tempfile.mkdtemp(prefix="nohn-verify-world-")
    states = derive_states(data["world_id"], data["genesis_seed"], tmp_dir,
                           data["agent_count"], data["tick_from"], data["tick_to"])
    digest_ok = (states[0]["content_digest"] == data["content_digest_start"]
                 and states[-1]["content_digest"] == data["content_digest_end"])
    results.append(("content_digest replay", digest_ok))
    print(f"  content_digest replay: {'PASS' if digest_ok else 'FAIL'}")

    # 身份锚定（第 29 维）：复验方独立重建同一份外观资产并比摘要
    from video.identity_assets import build_assets, assets_digest
    rebuilt_assets = build_assets(states[0]["souls"], data["genesis_seed"])
    identity_ok = assets_digest(rebuilt_assets) == data.get("identity_assets_digest")
    results.append(("identity anchors (dim 29)", identity_ok))
    print(f"  identity anchors     : {'PASS' if identity_ok else 'FAIL'}")

    # 结构层（Scene IR）：与像素层分开验；旧 manifest 没有该字段则跳过
    shot_graph = _load_shot_graph(args.shot)
    if data.get("scene_ir_digest"):
        from video.scene_ir import compile_scene_ir, scene_ir_sequence_digest
        scene_irs = [
            compile_scene_ir(state, _pick_shot(shot_graph, state["tick"]),
                             assets=rebuilt_assets, frame_index=index, sub=0)
            for index, state in enumerate(states)
        ]
        scene_ok = scene_ir_sequence_digest(scene_irs) == data["scene_ir_digest"]
        results.append(("scene ir replay", scene_ok))
        print(f"  scene ir replay      : {'PASS' if scene_ok else 'FAIL'}")

    if args.frames:
        from video.render.deterministic import DeterministicRenderer
        from video.render.tier import RenderContext
        from video.encode import encode_raw_stream
        from video.timebase import Timebase

        width, height, fps = _resolve_framing(shot_graph)
        timebase = Timebase(tps=DEFAULT_TPS, fps=fps)
        # 必须传入与生产链路同源的资产 —— 否则像素层必然分歧
        renderer = DeterministicRenderer(assets=rebuilt_assets)

        def stream():
            for index in range(len(states)):
                shot = _pick_shot(shot_graph, states[index]["tick"])
                for sub in range(timebase.frames_per_tick):
                    frame_state, _ = _interpolate(states, index, sub,
                                                  timebase.frames_per_tick)
                    ctx = RenderContext(shot=shot,
                                        frame_index=index * timebase.frames_per_tick + sub,
                                        tick=states[index]["tick"], sub=sub)
                    yield renderer.render(frame_state, shot, ctx)

        actual_hashes = encode_raw_stream(stream(), args.frames, width, height, fps)
        diff = diff_hash_sequences(expected_hashes, actual_hashes)
        results.append(("pixel replay (R1)", diff["identical"]))
        print(f"  pixel replay (R1)    : {'PASS' if diff['identical'] else 'FAIL'} "
              f"({diff['identical_count']}/{diff['frames_a']} identical, "
              f"first mismatch={diff['first_mismatch_index']})")

    ok = all(passed for _, passed in results)
    print(f"\nVERDICT: {'PASS' if ok else 'FAIL'}")
    for name, passed in results:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
    return 0 if ok else 1


# ---------------------------------------------------------------- argparse

def main():
    parser = argparse.ArgumentParser(description="second-reality-video CLI (Phase 0)")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("extract", help="世界 → FrameState 序列")
    p.add_argument("--world-id", default="video-demo")
    p.add_argument("--world", default=".world_data/video")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--agents", type=int, default=10)
    p.add_argument("--ticks", default="0-600")
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_extract)

    p = sub.add_parser("scene", help="states + ShotGraph → Scene IR + 结构验收")
    p.add_argument("--state", required=True)
    p.add_argument("--shot", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--report", default="",
                   help="结构验收报告落盘路径（可选）")
    p.add_argument("--max-step", type=float, default=20.0,
                   help="单帧位移告警阈值（世界坐标单位）")
    p.set_defaults(func=cmd_scene)

    p = sub.add_parser("bake-assets", help="states.jsonl → 离线烘焙资产目录")
    p.add_argument("--state", required=True)
    p.add_argument("--out-dir", required=True)
    p.set_defaults(func=cmd_bake_assets)

    p = sub.add_parser("render", help="states + ShotGraph → mp4")
    p.add_argument("--state", required=True)
    p.add_argument("--shot", required=True)
    p.add_argument("--tier", default="R1", choices=["R1", "R2"])
    p.add_argument("--samples", type=int, default=3,
                   help="额外落盘多少张抽样 PNG 供目视核对（0 = 不落盘）")
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_render)

    p = sub.add_parser("attest", help="生成 manifest（含真实审计）")
    p.add_argument("--video", required=True)
    p.add_argument("--hashes", required=True)
    p.add_argument("--state", required=True)
    p.add_argument("--shot", required=True)
    p.add_argument("--manifest", required=True)
    p.add_argument("--baked-assets", default="",
                   help="离线烘焙资产目录；须与创世派生资产一致，否则拒绝签发")
    p.set_defaults(func=cmd_attest)

    p = sub.add_parser("verify", help="由 manifest 独立复验")
    p.add_argument("--manifest", required=True)
    p.add_argument("--hashes", required=True)
    p.add_argument("--shot", required=True)
    p.add_argument("--frames", default="", help="重渲到该 mp4 路径以比对像素层")
    p.set_defaults(func=cmd_verify)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        raise SystemExit(1)
    raise SystemExit(args.func(args) or 0)


if __name__ == "__main__":
    main()
