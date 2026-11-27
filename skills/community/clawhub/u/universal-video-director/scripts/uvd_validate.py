#!/usr/bin/env python3
"""universal-video-director 校验器（仅标准库）。
用法:
  uvd_validate.py stage <stage> <file> [--project DIR]   校验单个产物（schema + 跨文件规则）
  uvd_validate.py all <project_dir>                       全量校验，返回 first_failing_stage
  uvd_validate.py stale <project_dir>                     上游哈希比对，列出需要重做的阶段
  uvd_validate.py stamp <project_dir> <stage>             写入 upstream 哈希（阶段完成后调用）
输出 JSON: {ok, errors:[{level,root_stage,path,code,msg,fix}], warnings:[...]}
软门禁：只有确定性的机械问题才是 ERROR，启发式问题一律 WARNING，交给 Agent 复核。
"""
import json, os, re, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(os.path.dirname(HERE), "assets", "schemas")
ORDER = ["project","source_analysis","story","assets","staging","storyboard","video_prompts","production","edl","qa_report","repair_log"]
FILES = {s: f"{i:02d}_{s}.json" for i, s in enumerate(ORDER)}
UPSTREAM = {"source_analysis":["project"],"story":["project","source_analysis"],"assets":["story"],
  "staging":["story","assets"],"storyboard":["story","assets","staging"],"video_prompts":["storyboard","assets"],
  "production":["assets","storyboard","video_prompts"],"edl":["story","storyboard","production"],
  "qa_report":["edl"],"repair_log":["qa_report"]}
OPTIONAL = {"source_analysis","staging","video_prompts","repair_log"}
SCORE_KEYS = ["narrative","consistency","image_quality","camera","pacing","av_sync","captions","platform"]

class Rep:
    def __init__(s, stage): s.stage=stage; s.errors=[]; s.warnings=[]
    def e(s, path, code, msg, fix="", root=None):
        s.errors.append({"level":"ERROR","root_stage":root or s.stage,"path":path,"code":code,"msg":msg,"fix":fix})
    def w(s, path, code, msg, fix=""):
        s.warnings.append({"level":"WARNING","root_stage":s.stage,"path":path,"code":code,"msg":msg,"fix":fix})
    def out(s): return {"stage":s.stage,"ok":not s.errors,"errors":s.errors,"warnings":s.warnings}

# ---------- 迷你 JSON Schema 校验（draft-07 子集）----------
def check_schema(node, sch, path, r):
    if "enum" in sch and node not in sch["enum"]:
        r.e(path,"SCHEMA_ENUM",f"值 {node!r} 不在 {sch['enum']}"); return
    t = sch.get("type")
    tm = {"object":dict,"array":list,"string":str,"boolean":bool,"integer":int,"number":(int,float)}
    if t:
        ok = isinstance(node, tm[t]) and not (t in ("number","integer") and isinstance(node,bool))
        if not ok: r.e(path,"SCHEMA_TYPE",f"应为 {t}"); return
    if t=="string":
        if len(node) < sch.get("minLength",0): r.e(path,"SCHEMA_EMPTY","不能为空")
        if "pattern" in sch and not re.search(sch["pattern"], node): r.e(path,"SCHEMA_PATTERN",f"不匹配 {sch['pattern']}")
    if t in ("number","integer"):
        if "minimum" in sch and node < sch["minimum"]: r.e(path,"SCHEMA_MIN",f"应 >= {sch['minimum']}")
        if "maximum" in sch and node > sch["maximum"]: r.e(path,"SCHEMA_MAX",f"应 <= {sch['maximum']}")
    if t=="object":
        for k in sch.get("required",[]):
            if k not in node: r.e(f"{path}.{k}","SCHEMA_REQUIRED","缺少必填字段")
        for k, sub in sch.get("properties",{}).items():
            if k in node: check_schema(node[k], sub, f"{path}.{k}", r)
    if t=="array":
        if len(node) < sch.get("minItems",0): r.e(path,"SCHEMA_MIN_ITEMS",f"至少 {sch['minItems']} 项")
        if "items" in sch:
            for i, it in enumerate(node): check_schema(it, sch["items"], f"{path}[{i}]", r)

def load_schema(stage):
    with open(os.path.join(SCHEMA_DIR, f"{stage}.schema.json"), encoding="utf-8") as f: return json.load(f)

def load(p):
    with open(p, encoding="utf-8") as f: return json.load(f)

def ids(items, key="id"): return [x.get(key) for x in (items or []) if isinstance(x, dict)]
def dup(r, items, path):
    seen=set()
    for i,v in enumerate(ids(items)):
        if v in seen: r.e(f"{path}[{i}].id","DUP_ID",f"重复 id {v}")
        seen.add(v)

# ---------- 跨文件规则 ----------
def rules(stage, d, P, r):
    G = (P.get("project") or {}).get("gates", {})
    target = (P.get("project") or {}).get("duration_sec")
    if stage=="story":
        dup(r,d.get("characters"),"characters"); dup(r,d.get("beats"),"beats"); dup(r,d.get("scenes"),"scenes")
        cids=set(ids(d.get("characters"))); sids=set(ids(d.get("scenes"))); bids=set(ids(d.get("beats")))
        beats=sorted(d.get("beats",[]), key=lambda b:b.get("order",0))
        cps=G.get("chars_per_sec",4.5)
        for b in beats:
            p=f"beats[{b.get('id')}]"
            if b.get("scene_id") not in sids: r.e(p+".scene_id","REF_SCENE",f"未知场景 {b.get('scene_id')}")
            if b.get("type") in ("dialogue","os","vo"):
                if not b.get("line"): r.e(p+".line","LINE_MISSING","对白类 beat 必须有台词")
                if b.get("type")=="dialogue" and b.get("character_id") not in cids: r.e(p+".character_id","REF_CHAR",f"未知角色 {b.get('character_id')}")
                need=len(re.sub(r"\s","",b.get("line",""))) / cps
                if b.get("duration_sec",0) < need*0.8: r.e(p+".duration_sec","LINE_TOO_FAST",f"台词需约 {need:.1f}s，仅给 {b.get('duration_sec')}s","加时长或删字（锁定台词只能加时长）")
            elif not b.get("action"): r.e(p+".action","ACTION_MISSING","动作 beat 必须写可拍动作")
            for c in b.get("causal_from",[]) or []:
                if c not in bids: r.e(p+".causal_from","REF_BEAT",f"未知因果 beat {c}")
        if beats and not any(b.get("purpose")=="hook" for b in beats[:3]): r.e("beats","NO_COLD_HOOK","前 3 个 beat 中没有 hook","把冲突/悬念提前")
        if beats and beats[-1].get("purpose") not in ("cliff","payoff"): r.w("beats","WEAK_ENDING","结尾不是 cliff/payoff")
        tot=sum(b.get("duration_sec",0) for b in beats)
        if target and abs(tot-target) > 0.1*target: r.e("beats","DURATION_OFF",f"总时长 {tot:.1f}s，目标 {target}s ±10%","删减/合并 beat")
        elif target and abs(tot-target) > 0.05*target: r.w("beats","DURATION_EDGE",f"总时长 {tot:.1f}s 偏离目标 {target}s 超过 5%，下游一压缩就会越界","现在就补/删 beat，留出余量")
        for i,b in enumerate(beats):
            if b.get("type")=="action" and i>0 and b.get("action")==beats[i-1].get("action"): r.w(f"beats[{b.get('id')}]","REPEAT","与上一 beat 动作重复")
    if stage=="assets":
        dup(r,d.get("assets"),"assets")
        a_ids=set(ids(d.get("assets"))); st=P.get("story") or {}
        for c in st.get("characters",[]):
            if c.get("id") not in a_ids: r.e("assets","CHAR_NO_ASSET",f"角色 {c.get('id')} 没有资产")
        for s in st.get("scenes",[]):
            if s.get("id") not in a_ids: r.w("assets","SCENE_NO_ASSET",f"场景 {s.get('id')} 没有资产")
        locks=set()
        for a in d.get("assets",[]):
            p=f"assets[{a.get('id')}]"
            for l in a.get("locks",[]) or []:
                if l.get("id") in locks: r.e(p+".locks","DUP_LOCK",f"锁定词 {l.get('id')} 重复")
                locks.add(l.get("id"))
                if l.get("phrase") and l["phrase"] not in a.get("ref_prompt",""): r.e(p+".ref_prompt","LOCK_NOT_IN_REF",f"锁定词『{l['phrase']}』未原样写入 ref_prompt")
            if a.get("type")=="character":
                views={x.get("view") for x in a.get("ref_images",[]) or []}
                if "anchor_full" not in views: r.w(p+".ref_images","NO_ANCHOR","缺正面全身锚点图，跨镜一致性风险")
                if any(x.get("stale") for x in a.get("ref_images",[]) or []): r.e(p+".ref_images","REF_STALE","参考图已过期（描述改了图没重出）")
            if a.get("type")=="scene" and not any(x.get("view")=="plate" for x in a.get("ref_images",[]) or []):
                r.w(p+".ref_images","NO_PLATE","场景缺无人空镜（白板图）")
    if stage=="staging":
        st=P.get("story") or {}; scenes={s.get("id"):s for s in st.get("scenes",[])}
        for s in d.get("scenes",[]):
            p=f"scenes[{s.get('scene_id')}]"
            if s.get("scene_id") not in scenes: r.e(p,"REF_SCENE","未知场景"); continue
            pos={x.get("character_id") for x in s.get("positions",[])}
            for c in scenes[s["scene_id"]].get("characters",[]) or []:
                if c not in pos: r.e(p+".positions","CHAR_NOT_PLACED",f"角色 {c} 未定开场站位")
            ax=s.get("axis") or {}
            for k in ("a","b"):
                if ax and ax.get(k) not in pos: r.e(p+".axis","AXIS_REF",f"轴线端点 {ax.get(k)} 不在站位中")
            if ax and any(x.get("kind")=="prop" and x.get("character_id") in (ax.get("a"),ax.get("b")) for x in s.get("positions",[])):
                r.w(p+".axis","AXIS_PROP","关系轴线端点是道具；仅在人物与物件对峙的独角戏里合理")
            PROP_P={"placed","held","concealed"}; HUMAN_P={"stand","sit","lie","kneel","walk"}
            for x in s.get("positions",[]):
                kind=x.get("kind","character"); pz=x.get("posture")
                if kind=="prop" and pz in HUMAN_P: r.w(p+".positions","PROP_POSTURE",f"道具 {x.get('character_id')} 用了人物姿态 {pz}","改用 placed/held/concealed")
                if kind=="character" and pz in PROP_P: r.e(p+".positions","CHAR_POSTURE",f"角色 {x.get('character_id')} 不能用道具姿态 {pz}")
            anchors=[(x.get("anchor"),x.get("side")) for x in s.get("positions",[]) if x.get("posture")=="sit"]
            if len(anchors)!=len(set(anchors)): r.e(p+".positions","SEAT_CONFLICT","两人坐在同一位置")
            if s.get("provisional"): r.w(p,"PROVISIONAL","无场景图，站位为暂定")
    if stage=="storyboard":
        st=P.get("story") or {}; asg=P.get("assets") or {}; stg=P.get("staging")
        bids={b.get("id"):b for b in st.get("beats",[])}; a_ids=set(ids(asg.get("assets")))
        seg_max=G.get("segment_max_sec",15); cmin=G.get("cut_min_sec",1.0); cmax=G.get("cut_max_sec",8.0)
        covered=set(); allcuts=[]; cut_ids=set()
        locks={l["phrase"]:l for a in asg.get("assets",[]) for l in (a.get("locks") or []) if l.get("phrase")}
        assets_by={a.get("id"):a for a in asg.get("assets",[])}
        for sg in d.get("segments",[]):
            p=f"segments[{sg.get('id')}]"
            cuts=sorted(sg.get("cuts",[]), key=lambda c:c.get("order",0))
            tot=sum(c.get("duration_sec",0) for c in cuts)
            if abs(tot - sg.get("duration_sec",0))>0.05: r.e(p+".duration_sec","SEG_SUM",f"cut 时长合计 {tot:.2f}s ≠ segment {sg.get('duration_sec')}s")
            if sg.get("duration_sec",0) > seg_max: r.e(p,"SEG_TOO_LONG",f"超过单次生成上限 {seg_max}s","拆成多个 segment")
            if stg is not None:
                bs={s.get("scene_id"):s.get("blocking_sentence") for s in stg.get("scenes",[])}
                first=[x for x in d.get("segments",[]) if x.get("scene_id")==sg.get("scene_id")][0]
                if first is sg and bs.get(sg.get("scene_id")) and bs[sg["scene_id"]] not in (sg.get("opening_blocking") or ""):
                    r.e(p+".opening_blocking","BLOCKING_NOT_COPIED","场景首个 segment 未原样带入开场站位句",root="storyboard")
            t=0
            for c in cuts:
                cp=f"cuts[{c.get('id')}]"
                if c.get("id") in cut_ids: r.e(cp,"DUP_ID","cut id 重复")
                cut_ids.add(c.get("id"))
                if not (cmin <= c.get("duration_sec",0) <= cmax): r.e(cp+".duration_sec","CUT_LEN",f"cut 时长应在 {cmin}-{cmax}s")
                for b in c.get("beat_ids",[]):
                    if b not in bids: r.e(cp+".beat_ids","REF_BEAT",f"未知 beat {b}")
                    covered.add(b)
                for a in c.get("asset_ids",[]):
                    if a not in a_ids: r.e(cp+".asset_ids","REF_ASSET",f"未知资产 {a}",root="assets")
                    else:
                        for l in assets_by[a].get("locks") or []:
                            if l.get("phrase") and l["phrase"] not in c.get("first_frame_prompt",""):
                                r.e(cp+".first_frame_prompt","LOCK_MISSING",f"首帧提示词缺锁定词『{l['phrase']}』","原样粘贴锁定词")
                if c.get("start_frame")==c.get("end_frame"): r.w(cp,"STATIC","起止画面相同，镜头无推进")
                c["_t0"]=t; t+=c.get("duration_sec",0); allcuts.append((sg,c))
        for b in bids:
            if b not in covered: r.e("segments","BEAT_UNCOVERED",f"beat {b} 没有任何镜头")
        for i in range(1,len(allcuts)):
            (s0,a),(s1,b)=allcuts[i-1],allcuts[i]
            if s0.get("scene_id")!=s1.get("scene_id"): continue
            ca,cb=a.get("camera",{}),b.get("camera",{})
            if a.get("shot_size")==b.get("shot_size") and ca.get("station")==cb.get("station") and ca.get("angle")==cb.get("angle"):
                r.e(f"cuts[{b.get('id')}]","JUMP_CUT",f"与 {a.get('id')} 景别/机位/角度全同","换机位或景别")
        win=[c for _,c in allcuts]
        for i in range(len(win)-3):
            if len({w.get("camera",{}).get("station") for w in win[i:i+4]})==1: r.w(f"cuts[{win[i].get('id')}]","MONO_COVERAGE","连续 4 镜同一机位")
        bsum={}
        for _,c in allcuts:
            for b in c.get("beat_ids",[]): bsum[b]=bsum.get(b,0)+c.get("duration_sec",0)/len(c["beat_ids"])
        for b,v in bsum.items():
            bd=bids[b].get("duration_sec",0) if b in bids else 0
            if bd and abs(v-bd)>max(1.0,0.25*bd): r.w(f"beat {b}","BEAT_TIME",f"镜头合计 {v:.1f}s vs 剧本 {bd}s")
        for _,c in allcuts: c.pop("_t0",None)
    if stage=="video_prompts":
        sb=P.get("storyboard") or {}; asg=P.get("assets") or {}
        cuts={c.get("id"):(s,c) for s in sb.get("segments",[]) for c in s.get("cuts",[])}
        a_ids=set(ids(asg.get("assets"))); used=set(); mx=(P.get("project") or {}).get("backends",{}).get("max_clip_sec",15)
        dup(r,d.get("motions"),"motions")
        for m in d.get("motions",[]):
            p=f"motions[{m.get('id')}]"
            cs=m.get("cut_ids",[])
            for c in cs:
                if c not in cuts: r.e(p+".cut_ids","REF_CUT",f"未知 cut {c}",root="storyboard"); continue
                if c in used: r.e(p+".cut_ids","CUT_TWICE",f"cut {c} 被多条 motion 使用")
                used.add(c)
            known=[cuts[c][1] for c in cs if c in cuts]
            if len({cuts[c][0].get("id") for c in cs if c in cuts})>1: r.e(p,"GROUP_CROSS_SEG","GROUP 合生跨了 segment")
            exp=sum(k.get("duration_sec",0) for k in known)
            if known and abs(exp-m.get("duration_sec",0))>0.05: r.e(p+".duration_sec","DUR_MISMATCH",f"视频提示词 {m.get('duration_sec')}s 与分镜 {exp:.2f}s 不一致","以分镜为准")
            if m.get("duration_sec",0)>mx and (m.get("render") or d.get("mode"))!="still": r.e(p,"OVER_MODEL_MAX",f"超过模型单次上限 {mx}s",root="storyboard")
            slots=[b.get("slot") for b in m.get("ref_bindings",[])]
            if len(slots)!=len(set(slots)): r.e(p+".ref_bindings","SLOT_DUP","参考图槽位重复")
            for b in m.get("ref_bindings",[]):
                if b.get("asset_id") not in a_ids and not str(b.get("asset_id","")).startswith("FRAME:"): r.e(p+".ref_bindings","REF_ASSET",f"未知参考 {b.get('asset_id')}",root="assets")
            rmode=m.get("render") or ("still" if d.get("mode")=="still" else "video")
            pm=(P.get("project") or {}).get("render_mode","video")
            if pm=="video" and rmode=="still": r.e(p+".render","RENDER_MODE",f"项目 render_mode=video，不允许 still 段",root="project")
            if pm=="still" and rmode=="video": r.e(p+".render","RENDER_MODE",f"项目 render_mode=still，不应生成视频",root="project")
            if rmode=="still":
                sm=m.get("still_move")
                if not sm: r.e(p+".still_move","NO_STILL_MOVE","静帧段必须写 still_move（推拉摇移/视差），否则成片是幻灯片","按分镜 camera.movement 映射")
                elif sm.get("type") in ("push_in","pull_out") and (sm.get("from_scale",1)==sm.get("to_scale",1)): r.e(p+".still_move","STILL_NO_DELTA","推拉镜头的起止缩放相同")
                elif sm.get("type") in ("push_in",) and sm.get("to_scale",1)>1.35: r.w(p+".still_move","STILL_OVERZOOM","推近超过 1.35 倍，原图分辨率可能不够")
                if len(known)>1: r.w(p,"STILL_GROUP","静帧段合并了多个 cut；静帧通常一 cut 一图")
                if m.get("duration_sec",0)>8: r.w(p,"STILL_LONG","单张静帧超过 8 秒，观众易出戏，考虑拆镜或加 layers")
            elif d.get("mode") in ("i2v","flf2v","ref2v") and not m.get("ref_bindings"): r.e(p+".ref_bindings","NO_REF","图生视频模式却没有绑定参考图","绑定首帧与角色锚点图")
        for c in cuts:
            if c not in used: r.e("motions","CUT_NO_MOTION",f"cut {c} 没有视频提示词")
    if stage=="production":
        if not d.get("confirmed") and any(t.get("status") in ("submitted","done") for t in d.get("tasks",[])):
            r.e("confirmed","SPEND_WITHOUT_CONFIRM","未经确认就提交了生成任务","先预览并取得用户确认")
        bud=(P.get("project") or {}).get("budget",{}).get("limit"); est=(d.get("estimate") or {}).get("cost")
        if bud and est and est>bud: r.e("estimate","OVER_BUDGET",f"预估 {est} 超预算 {bud}")
        vp=P.get("video_prompts") or {}; mids=set(ids(vp.get("motions"))); refs=set()
        sb=P.get("storyboard") or {}; seg_dur={m.get("id"):m.get("duration_sec") for m in vp.get("motions",[])}
        root=P.get("_dir")
        for t in d.get("tasks",[]):
            p=f"tasks[{t.get('id')}]"; refs.add(t.get("ref"))
            if t.get("status")=="submitted" and not t.get("task_id"): r.e(p,"NO_TASK_ID","已提交但未保存平台任务 ID，断点无法续跑")
            if t.get("status")=="failed": r.e(p,"TASK_FAILED",t.get("error","生成失败"),"换 seed 重试，≥3 次失败则回到提示词阶段",root="production")
            if t.get("status")=="stale": r.e(p,"TASK_STALE","上游已变更，需重做")
            if t.get("status")=="done":
                if not t.get("output"): r.e(p,"NO_OUTPUT","done 但没有输出路径")
                elif root and not os.path.exists(os.path.join(root,t["output"])): r.e(p+".output","FILE_MISSING",f"文件不存在 {t['output']}")
                if t.get("kind")=="video" and t.get("ref") in seg_dur and isinstance(t.get("actual_duration_sec"),(int,float)):
                    if abs(t["actual_duration_sec"]-seg_dur[t["ref"]])>0.3: r.e(p,"CLIP_DURATION",f"实际 {t['actual_duration_sec']}s ≠ 计划 {seg_dur[t['ref']]}s")
        still={m.get("id"):m for m in vp.get("motions",[]) if (m.get("render") or ("still" if vp.get("mode")=="still" else "video"))=="still"}
        for m in mids:
            if m in still:
                frames={b["asset_id"][6:] for b in still[m].get("ref_bindings",[]) if str(b.get("asset_id","")).startswith("FRAME:")} or set(still[m].get("cut_ids",[]))
                for f in frames:
                    if f not in refs and m not in refs: r.e("tasks","STILL_NO_FRAME",f"静帧段 {m} 缺首帧图任务（ref={f}）")
                if any(t.get("ref")==m and t.get("kind")=="video" for t in d.get("tasks",[])): r.w("tasks","STILL_HAS_VIDEO",f"静帧段 {m} 却排了视频任务，浪费预算")
            elif m not in refs: r.e("tasks","MOTION_NO_TASK",f"motion {m} 没有生成任务")
    if stage=="edl":
        st=P.get("story") or {}; sb=P.get("storyboard") or {}; pr=P.get("production") or {}
        lines={b.get("id"):b.get("line") for b in st.get("beats",[]) if b.get("line")}
        cuts={c.get("id") for s in sb.get("segments",[]) for c in s.get("cuts",[])}
        outs={t.get("output") for t in pr.get("tasks",[]) if t.get("status")=="done"}
        used=set(); tl=0
        for c in sorted(d.get("clips",[]), key=lambda x:x.get("order",0)):
            p=f"clips[{c.get('order')}]"
            if c.get("cut_id") not in cuts: r.e(p+".cut_id","REF_CUT",f"未知 cut {c.get('cut_id')}")
            used.add(c.get("cut_id"))
            if c.get("out_sec",0)<=c.get("in_sec",0): r.e(p,"IN_OUT","出点必须大于入点")
            if pr and c.get("source") not in outs: r.e(p+".source","SRC_NOT_PRODUCED","素材不是已完成的生产任务输出",root="production")
            tl+=(c.get("out_sec",0)-c.get("in_sec",0))/(c.get("speed") or 1)
        for cid in cuts:
            if cid not in used: r.w("clips","CUT_DROPPED",f"cut {cid} 未进入成片")
        for i,s in enumerate(d.get("subtitles",[])):
            p=f"subtitles[{i}]"
            if s.get("beat_id") in lines and re.sub(r"\s","",s.get("text",""))!=re.sub(r"\s","",lines[s["beat_id"]]):
                r.e(p+".text","SUB_NOT_VERBATIM","字幕必须逐字取自剧本台词")
            if s.get("end_sec",0)<=s.get("start_sec",0): r.e(p,"SUB_TIME","字幕时间非法")
            if s.get("end_sec",0)>tl+0.05: r.e(p,"SUB_OVERFLOW","字幕超出成片时长")
        missing=[b for b in lines if b not in {s.get('beat_id') for s in d.get('subtitles',[])}]
        if missing: r.w("subtitles","LINE_NO_SUB",f"台词无字幕: {missing}")
        if target and abs(tl-target)>0.1*target: r.e("clips","TIMELINE_OFF",f"成片 {tl:.1f}s 偏离目标 {target}s",root="storyboard")
        elif target and abs(tl-target)>0.05*target: r.w("clips","TIMELINE_EDGE",f"成片 {tl:.1f}s 偏离目标 {target}s 超过 5%")
        au=d.get("audio",{})
        if isinstance(au.get("measured_lufs"),(int,float)) and abs(au["measured_lufs"]-au.get("target_lufs",-14))>1.0: r.e("audio.measured_lufs","LOUDNESS",f"实测 {au['measured_lufs']} LUFS 偏离目标")
        if au.get("fade_ms",0)<10: r.w("audio.fade_ms","NO_FADE","剪辑点音频淡化 <10ms，可能爆音")
        md=(d.get("output") or {}).get("measured_duration_sec")
        if isinstance(md,(int,float)) and abs(md-tl)>0.2: r.e("output.measured_duration_sec","RENDER_DURATION",f"渲染时长 {md}s ≠ 时间线 {tl:.2f}s")
        root=P.get("_dir"); v=(d.get("output") or {}).get("video")
        if root and v and not os.path.exists(os.path.join(root,v)): r.w("output.video","NOT_RENDERED","成片文件尚不存在")
    if stage=="qa_report":
        sc=d.get("scores",{}); vals=[sc.get(k) for k in SCORE_KEYS if isinstance(sc.get(k),(int,float))]
        if d.get("hard_caps") and vals and max(vals)>5: r.e("scores","HARD_CAP","触发硬性上限时所有分数须 ≤5")
        blocking=any(i.get("severity") in ("critical","major") for i in d.get("issues",[]))
        exp=bool(vals) and len(vals)==len(SCORE_KEYS) and min(vals)>=8 and not blocking and not d.get("hard_caps")
        if d.get("pass")!=exp: r.e("pass","PASS_INCONSISTENT",f"pass 应为 {exp}")
        if not d.get("evidence_frames"): r.w("evidence_frames","NO_EVIDENCE","评审未附帧证据")
        for i in d.get("issues",[]):
            if i.get("severity") in ("critical","major") and i.get("root_stage")=="edl" and "regenerat" in i.get("fix_hint","").lower():
                r.w(f"issues[{i.get('id')}]","ROOT_SUSPECT","修复需重生成素材，root_stage 可能应为 production/video_prompts")
    if stage=="repair_log":
        qa=P.get("qa_report") or {}; qids=set(ids(qa.get("issues")))
        mx=G.get("max_repair_rounds",3)
        if len(d.get("rounds",[]))>mx: r.e("rounds","OVER_ROUNDS",f"超过最大修复轮数 {mx}","停止并交付最佳版本")
        for i,rd in enumerate(d.get("rounds",[])):
            if rd.get("round")!=i+1: r.w(f"rounds[{i}]","ROUND_SEQ","轮次不连续")
            if rd.get("result")=="regressed": r.w(f"rounds[{i}]","REGRESSED","本轮修复导致分数下降，考虑回滚")

def validate_stage(stage, path, proj_dir=None):
    r=Rep(stage)
    try: d=load(path)
    except Exception as ex:
        r.e("$","LOAD",f"无法读取 JSON: {ex}"); return r.out()
    check_schema(d, load_schema(stage), "$", r)
    P={"_dir":proj_dir}
    if proj_dir:
        for s,f in FILES.items():
            fp=os.path.join(proj_dir,f)
            if os.path.exists(fp) and s!=stage:
                try: P[s]=load(fp)
                except Exception: pass
    try: rules(stage, d, P, r)
    except Exception as ex: r.e("$","RULE_CRASH",f"规则执行异常（多半是结构错误）: {ex}")
    return r.out()

def h(path):
    with open(path,"rb") as f: return hashlib.sha256(f.read()).hexdigest()[:12]

def stale(proj):
    res=[]
    for s in ORDER:
        fp=os.path.join(proj,FILES[s])
        if not os.path.exists(fp): continue
        up=(load(fp).get("upstream") or {})
        for u in UPSTREAM.get(s,[]):
            ufp=os.path.join(proj,FILES[u])
            if os.path.exists(ufp) and up.get(FILES[u]) and up[FILES[u]]!=h(ufp):
                res.append({"stage":s,"because":u}); break
    # 传递失效
    bad={x["stage"] for x in res}; changed=True
    while changed:
        changed=False
        for s in ORDER:
            if s not in bad and any(u in bad for u in UPSTREAM.get(s,[])) and os.path.exists(os.path.join(proj,FILES[s])):
                bad.add(s); res.append({"stage":s,"because":"transitive"}); changed=True
    return res

def stamp(proj, stage):
    fp=os.path.join(proj,FILES[stage]); d=load(fp)
    d["upstream"]={FILES[u]:h(os.path.join(proj,FILES[u])) for u in UPSTREAM.get(stage,[]) if os.path.exists(os.path.join(proj,FILES[u]))}
    with open(fp,"w",encoding="utf-8") as f: json.dump(d,f,ensure_ascii=False,indent=2)
    return d["upstream"]

def validate_all(proj):
    res=[]
    for s in ORDER:
        fp=os.path.join(proj,FILES[s])
        if os.path.exists(fp): res.append(validate_stage(s,fp,proj))
        elif s not in OPTIONAL and s not in ("qa_report",): res.append({"stage":s,"ok":None,"missing":True,"errors":[],"warnings":[]})
    first=next((x["stage"] for x in res if x.get("ok") is False), None)
    nxt=next((x["stage"] for x in res if x.get("missing")), None)
    st=stale(proj)
    # 根因：stale 链条里最上游的、本身没过期的变更源；有它时优先于 first_failing_stage
    srcs=[x["because"] for x in st if x["because"]!="transitive" and x["because"] not in {y["stage"] for y in st}]
    root=min(srcs,key=ORDER.index) if srcs else first
    return {"ok":first is None and not st,"first_failing_stage":first,"root_cause_stage":root,"next_missing_stage":nxt,"stale":st,"results":res}

def main(argv):
    if len(argv)<2: print(__doc__); return 2
    cmd=argv[1]
    if cmd=="stage":
        proj=argv[argv.index("--project")+1] if "--project" in argv else os.path.dirname(os.path.abspath(argv[3]))
        o=validate_stage(argv[2],argv[3],proj)
    elif cmd=="all": o=validate_all(argv[2])
    elif cmd=="stale": o={"stale":stale(argv[2])}
    elif cmd=="stamp": o={"upstream":stamp(argv[2],argv[3])}
    else: print(__doc__); return 2
    print(json.dumps(o,ensure_ascii=False,indent=2))
    return 0 if o.get("ok",True) is not False else 1

if __name__=="__main__": sys.exit(main(sys.argv))
