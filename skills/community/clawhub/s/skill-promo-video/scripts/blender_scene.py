# -*- coding: utf-8 -*-
"""Blender 运镜场景渲染（headless Cycles）——skill-promo-video v2

「数据长廊」：暗色展厅长廊 + 悬浮图表面板（贴真实图表 PNG）+ 相机 dolly。
确定性运镜（3D 几何层保证多镜头一致性——纯 AI 生成的死穴）。

场景：
  dolly_in   开场：相机沿长廊缓缓推进，两侧图表渐次掠过，尽头主面板
  pull_out   收尾：相机从主面板缓缓拉远升起，全廊图表尽收眼底

用法（在 Blender 内执行）：
  blender -b -P blender_scene.py -- \
      --scene dolly_in --charts chart1.png chart2.png ... --out frames_dolly/ \
      --frames 135 --fps 30 --width 1920 --height 1080 --samples 96
输出：frames 目录内 PNG 序列（用 ffmpeg 编码：compose 前转 mp4）。
纪律：白模铁律=细节最少化；视觉迭代 ≥2 轮再批量；不过验收就降级静帧+zoompan，不硬磕。
"""
import argparse, glob, math, os, sys

import bpy  # noqa: E402  (由 blender -b -P 载入)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.images, bpy.data.cameras, bpy.data.lights):
        for x in list(block):
            if x.users == 0:
                block.remove(x)


def mat_simple(name, color, rough=0.4, metal=0.0, emit=None, emit_strength=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if emit:
        bsdf.inputs["Emission Color"].default_value = (*emit, 1.0)
        try:
            bsdf.inputs["Emission Strength"].default_value = emit_strength
        except KeyError:
            pass
    return m


def mat_chart(img_path, glow=1.6):
    """图表面板：Emission 着色器直连输出（灯箱行为，不依赖 Principled 发光通道）。"""
    m = bpy.data.materials.new("chart_" + os.path.basename(img_path)[:12])
    m.use_nodes = True
    nt = m.node_tree
    out = nt.nodes["Material Output"]
    for n in list(nt.nodes):
        if n != out:
            nt.nodes.remove(n)
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(img_path)
    tex.image.colorspace_settings.name = "sRGB"
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = glow
    nt.links.new(tex.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    return m


def add_plane(name, size, loc, rot, mat):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.data.materials.append(mat)
    return o


def build_hall(charts, hall_len=42.0):
    """长廊：地板+两侧悬浮图表列+尽头主面板+条形顶灯。"""
    dark = mat_simple("floor", (0.012, 0.014, 0.02), rough=0.25, metal=0.35)
    add_plane("floor", 200, (0, 0, 0), (0, 0, 0), dark)
    add_plane("ceil", 200, (0, 0, 7.5), (math.pi, 0, 0), mat_simple("ceil_m", (0.01, 0.01, 0.012), rough=0.9))

    n = len(charts)
    for i, c in enumerate(charts):
        side = 1 if i % 2 == 0 else -1
        row = i // 2
        y = -8.0 - row * 8.0
        x = side * 3.4
        yaw = math.pi / 2 - side * math.radians(4)
        p = add_plane("chart_%d" % i, 1.0, (x, y, 2.6), (math.pi / 2, 0, yaw),
                      mat_chart(c, glow=2.2))
        p.scale = (3.36, 1.89, 1.0)  # 16:9 面板
        # 面板背光条：金色细发光框（在图表外侧后方，避免遮挡面板）
        add_plane("edge_%d" % i, 1.0, (x + side * 0.07, y, 2.6),
                  (math.pi / 2, 0, yaw),
                  mat_simple("edge_m", (0, 0, 0), emit=(1.0, 0.72, 0.28), emit_strength=5.0)
                  ).scale = (3.56, 2.09, 1.0)

    # 尽头主面板（品牌/主视觉位）
    main = add_plane("main_panel", 1.0, (0, -hall_len, 3.2), (math.pi / 2, 0, 0),
                     mat_chart(charts[len(charts) // 2] if charts else "", glow=2.2) if charts
                     else mat_simple("m0", (0.05, 0.06, 0.08)))
    main.scale = (7.2, 4.05, 1.0)

    # 顶灯条（沿走廊）
    for k in range(6):
        y = -4 - k * 7
        add_plane("lamp_%d" % k, 1.0, (0, y, 7.3), (math.pi, 0, 0),
                  mat_simple("lamp_m", (0, 0, 0), emit=(1.0, 0.93, 0.82), emit_strength=40.0)).scale = (0.28, 5.0, 1.0)


def setup_camera(scene_kind, n_frames):
    # Blender 5.x：不直接操作 fcurves（API 已移除），用偏好默认插值/手柄实现缓入缓出
    try:
        bpy.context.preferences.edit.keyframe_new_interpolation_type = "BEZIER"
        bpy.context.preferences.edit.keyframe_new_handle_type = "AUTO_CLAMPED"
    except (AttributeError, TypeError):
        pass
    fill_data = bpy.data.lights.new("fill", type="AREA")
    fill_data.energy = 2600.0
    fill_data.size = 6.0
    fill = bpy.data.objects.new("fill", fill_data)
    bpy.context.collection.objects.link(fill)

    cam_data = bpy.data.cameras.new("cam")
    cam_data.lens = 26
    cam = bpy.data.objects.new("cam", cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    fill.parent = cam            # 相机局部 -Z=视线前方：子节点跟随运镜
    fill.location = (0.0, 0.8, -3.5)

    def key(loc, rot, f):
        cam.location, cam.rotation_euler = loc, rot
        cam.keyframe_insert(data_path="location", frame=f)
        cam.keyframe_insert(data_path="rotation_euler", frame=f)

    import mathutils
    # ⛔俯仰角必须为负：Blender 相机默认看本地 -Z，X 旋转 +θ 会朝 +Y（背后）看
    if scene_kind == "dolly_in":
        key(mathutils.Vector((0, 6.0, 2.2)), mathutils.Euler((math.radians(-87.5), 0, 0)), 1)
        key(mathutils.Vector((0, -16.0, 2.3)), mathutils.Euler((math.radians(-89), 0, 0)), n_frames)
    else:  # pull_out：从主面板处后退拉远升起，俯角渐增俯瞰全廊
        key(mathutils.Vector((0, -36.0, 2.6)), mathutils.Euler((math.radians(-90), 0, 0)), 1)
        key(mathutils.Vector((0, 6.0, 6.2)), mathutils.Euler((math.radians(-70), 0, 0)), n_frames)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", choices=["dolly_in", "pull_out"], default="dolly_in")
    ap.add_argument("--charts", nargs="*", default=[])
    ap.add_argument("--out", required=True)
    ap.add_argument("--frames", type=int, default=135)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--samples", type=int, default=96)
    a = ap.parse_args(argv)

    charts = [c for c in a.charts if os.path.exists(c)]
    missing = len(a.charts) - len(charts)
    if missing:
        print("WARN: %d chart files missing, skipped" % missing)

    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "GPU"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    # ⛔ 旧驱动上 OptiX 内核加载会失败（OPTIX_ERROR_INTERNAL_COMPILER_ERROR）——首选 CUDA，失败回退 CPU
    used_gpu = False
    for dt in ("CUDA", "OPTIX"):
        try:
            prefs.compute_device_type = dt
            prefs.get_devices()
            if any(d.type == dt for d in prefs.devices):
                for d in prefs.devices:
                    d.use = d.type == dt
                used_gpu = True
                print("Cycles device:", dt)
                break
        except Exception:
            continue
    if not used_gpu:
        sc.cycles.device = "CPU"
        print("Cycles device: CPU (fallback)")
    sc.cycles.samples = a.samples
    sc.cycles.use_denoising = True
    sc.render.resolution_x = a.width
    sc.render.resolution_y = a.height
    sc.render.fps = a.fps
    sc.frame_start, sc.frame_end = 1, a.frames
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "Filmic"
    sc.view_settings.exposure = 0.55
    sc.view_settings.look = "Medium High Contrast"

    clear_scene()
    build_hall(charts)
    # 世界环境：深色微光，避免死黑
    w = bpy.data.worlds.new("w")
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.32, 0.34, 0.42, 1.0)
    bg.inputs[1].default_value = 1.0
    sc.world = w
    setup_camera(a.scene, a.frames)

    os.makedirs(a.out, exist_ok=True)
    sc.render.filepath = os.path.join(a.out, "") + "fr_"
    bpy.ops.render.render(animation=True)
    frames = sorted(glob.glob(os.path.join(a.out, "fr_*.png")))
    print("RENDER OK:", len(frames), "frames ->", a.out)


if __name__ == "__main__":
    main()
