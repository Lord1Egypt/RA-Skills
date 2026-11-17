# -*- coding: utf-8 -*-
"""bundle_3d.py — 把 three.js + OrbitControls + BufferGeometryUtils + GLTFLoader
打包成单个无 import 的 IIFE，挂到 window.ThreeBundle = {THREE, OrbitControls, GLTFLoader}
彻底消除运行时 Blob URL 动态 import（沙箱/file:// 下 Failed to fetch 的根因）。

用法：把四个库文件放同一目录后运行 `python bundle_3d.py [工作目录]`，产出 _three_bundle.js。
库文件来源（three r169 官方构建，任选其一获取）：
  - 既有课件提取：心脏/伯努利课件同目录下已有四件套
  - npm 取件：npx esbuild 三行命令或直接从 three@0.169 npm 包拷贝 build/three.module.min.js
    与 examples/jsm/controls/OrbitControls.js、loaders/GLTFLoader.js、utils/BufferGeometryUtils.js
  - 库文件丢失时报 FileNotFoundError——按上述来源补齐再跑
"""
import re, os, sys

# 工作目录 = 参数1（默认脚本所在目录）；库文件从工作目录读取
WORK = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
os.chdir(WORK)

def _read(name):
    try:
        return open(name, encoding='utf-8').read()
    except FileNotFoundError:
        sys.exit(f'[bundle_3d] 缺少库文件 {name} —— 请从 three@0.169 npm 包或既有课件目录补齐后重跑')

three = _read('three.module.min.js')
orbit = _read('orbit-controls.js')
bufu  = _read('bufferutils.js')
gltf  = _read('gltfloader.js')

# ---- 1. three: 提取 export {a as X, b as Y, ...} 的绑定表，去掉 export 语句 ----
# 找最后一个 export { ... }; 块（three.module.min.js 的导出在文件尾）
m = None
for m in re.finditer(r'export\s*\{[^}]*\}\s*;?', three):
    pass
assert m, 'three export block not found'
export_block = m.group(0)
three_body = three[:m.start()] + three[m.end():]
# 解析 "internalName as PublicName" 对
pairs = re.findall(r'([\w$]+)\s+as\s+([\w$]+)', export_block)
print(f'three: {len(pairs)} exports')

# 生成 three 模块工厂：把内部绑定收集成对象
three_fn = """
function __threeFactory(){
  const exports = {};
  // ===== three.module.min.js body（去 export）=====
  %s
  // ===== 收集导出 =====
  const __e = {};
  %s
  return __e;
}
""" % (
    three_body.rstrip().rstrip(';'),
    '\n'.join(f'__e["{pub}"] = {internal};' for internal, pub in pairs)
)
print('three_fn size:', len(three_fn)//1024, 'KB')

# ---- 2. orbit/bufu: import {..} from 'three' → 参数注入；export {X} → return ----
def strip_imports(src):
    # from 'three' 与 from '../utils/BufferGeometryUtils.js' 两种都剥
    src = re.sub(r"import\s*\{[^}]*\}\s*from\s*['\"]three['\"]\s*;?", '', src)
    src = re.sub(r"import\s*\{[^}]*\}\s*from\s*['\"][^'\"]*BufferGeometryUtils\.js['\"]\s*;?", '', src)
    return src

def make_fn(src, deps):
    # 解析原 import 语句里的全部名字，body 前插 const {...} = THREE 解构注入
    imported = []
    for m in re.finditer(r"import\s*\{([^}]*)\}\s*from\s*['\"][^'\"]+['\"]", src):
        for item in m.group(1).split(','):
            item = item.strip()
            if item:
                imported.append(item.split(' as ')[-1].strip())
    destructure = 'const { %s } = THREE;' % ', '.join(dict.fromkeys(imported))
    body = strip_imports(src)
    # 具名声明 export（export function X / export const X）→ 去掉 export 关键字
    body = re.sub(r'\bexport\s+(function|const|let|var|class)\s+', r'\1 ', body)
    # export { X } 块 → 包进对象返回
    em = None
    for em in re.finditer(r'export\s*\{([^}]*)\}\s*;?', body):
        pass
    if em:
        names = [n.strip() for n in em.group(1).split(',')]
        body = body[:em.start()] + body[em.end():]
        ret = 'return { %s };' % ', '.join(names)
    else:
        ret = 'return {};'
    dep_params = ', '.join(deps)
    return "function(%s){\n%s\n%s\n%s\n}" % (dep_params, destructure, body.rstrip().rstrip(';'), ret)

orbit_fn = make_fn(orbit, ['THREE'])
bufu_fn  = make_fn(bufu,  ['THREE'])
gltf_fn  = make_fn(gltf,  ['THREE', 'BufferGeometryUtils'])
print('orbit/gltf functions built')

# ---- 3. 组装单文件 IIFE ----
bundle = """
/* ThreeBundle: three r169 + OrbitControls + BufferGeometryUtils + GLTFLoader
   静态打包版（无 import/export/网络请求），由 bundle_3d.py 生成 */
window.ThreeBundle = (function(){
  'use strict';
  %s
  const THREE = __threeFactory();
  const OrbitControls = (%s)(THREE).OrbitControls;
  const BufferGeometryUtils = (%s)(THREE);
  const GLTFLoader = (%s)(THREE, BufferGeometryUtils).GLTFLoader;
  return { THREE, OrbitControls, GLTFLoader };
})();
""" % (three_fn, orbit_fn, bufu_fn, gltf_fn)

open('_three_bundle.js', 'w', encoding='utf-8').write(bundle)
print('_three_bundle.js written:', len(bundle)//1024, 'KB')

# ---- 4. 语法自检（node）----
import subprocess
r = subprocess.run(['node', '--check', '_three_bundle.js'], capture_output=True, text=True)
print('node --check:', 'PASS' if r.returncode == 0 else 'FAIL\n' + r.stderr[:500])
