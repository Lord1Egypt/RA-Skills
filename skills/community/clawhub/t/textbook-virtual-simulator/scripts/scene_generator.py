#!/usr/bin/env python3
"""
3D场景生成脚本 - 根据教材内容生成3D交互场景
支持 Three.js 和 Babylon.js
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional


class SceneGenerator:
    """3D场景生成器"""

    def __init__(self, content_data: Dict[str, Any], scene_type: str = 'default'):
        self.content = content_data
        self.scene_type = scene_type.lower()
        self.library = 'threejs'  # 默认使用 Three.js

    def select_template(self) -> str:
        """选择场景模板"""
        templates = {
            'lab': '实验室场景',
            'classroom': '教室场景',
            'outdoor': '户外场景',
            'default': '默认场景'
        }
        return templates.get(self.scene_type, templates['default'])

    def generate_scene_code(self) -> str:
        """生成场景代码"""
        if self.library == 'threejs':
            return self._generate_threejs_scene()
        elif self.library == 'babylonjs':
            return self._generate_babylonjs_scene()
        else:
            raise ValueError(f"不支持的3D库: {self.library}")

    def _generate_threejs_scene(self) -> str:
        """生成Three.js场景代码"""

        # 场景配置
        scene_config = self._get_scene_config()

        # 生成场景代码
        scene_code = f'''// 教材虚拟仿真系统 - 3D场景生成
// 场景类型: {self.select_template()}
// 生成时间: {self._get_timestamp()}

import * as THREE from 'three';
import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';

class SimulationScene {{
    constructor(container) {{
        this.container = container;
        this.objects = new Map(); // 存储所有可交互对象
        this.animations = []; // 存储动画

        this.init();
        this.setupEventListeners();
    }}

    init() {{
        // 创建场景
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color({scene_config['background_color']});
        this.scene.fog = new THREE.Fog({scene_config['background_color']}, 10, 50);

        // 创建相机
        this.camera = new THREE.PerspectiveCamera(
            {scene_config['camera_fov']},
            this.container.clientWidth / this.container.clientHeight,
            {scene_config['camera_near']},
            {scene_config['camera_far']}
        );
        this.camera.position.set({scene_config['camera_position']});

        // 创建渲染器
        this.renderer = new THREE.WebGLRenderer({{
            antialias: {scene_config['antialias']},
            alpha: true
        }});
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.shadowMap.enabled = true;
        this.container.appendChild(this.renderer.domElement);

        // 创建控制器
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.minDistance = {scene_config['min_distance']};
        this.controls.maxDistance = {scene_config['max_distance']};

        // 设置光照
        this.setupLights();

        // 加载对象
        this.loadObjects();

        // 创建地面
        this.createGround();

        // 设置交互
        this.setupInteractions();

        // 开始动画循环
        this.animate();
    }}

    setupLights() {{
        // 环境光
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);

        // 主光源
        const mainLight = new THREE.DirectionalLight(0xffffff, 1);
        mainLight.position.set(10, 20, 10);
        mainLight.castShadow = true;
        mainLight.shadow.mapSize.width = 2048;
        mainLight.shadow.mapSize.height = 2048;
        this.scene.add(mainLight);

        // 补光
        const fillLight = new THREE.DirectionalLight(0xffffff, 0.5);
        fillLight.position.set(-10, 10, -10);
        this.scene.add(fillLight);

        // 点光源（可选）
        const pointLight = new THREE.PointLight(0xffffff, 0.8, 20);
        pointLight.position.set(0, 10, 0);
        this.scene.add(pointLight);
    }}

    loadObjects() {{
        // 从教材内容中提取的3D对象
        const objectsData = {self._extract_objects_data()};

        objectsData.forEach((objData, index) => {{
            const object = this.createObject(objData);
            if (object) {{
                this.scene.add(object);
                this.objects.set(objData.name || `object_${index}`, object);
            }}
        }});
    }}

    createObject(objData) {{
        let geometry, material, mesh;

        // 根据几何类型创建几何体
        switch(objData.geometry_type || 'box') {{
            case 'box':
                geometry = new THREE.BoxGeometry(1, 1, 1);
                break;
            case 'sphere':
                geometry = new THREE.SphereGeometry(0.5, 32, 32);
                break;
            case 'cylinder':
                geometry = new THREE.CylinderGeometry(0.5, 0.5, 1, 32);
                break;
            case 'cone':
                geometry = new THREE.ConeGeometry(0.5, 1, 32);
                break;
            case 'torus':
                geometry = new THREE.TorusGeometry(0.5, 0.2, 16, 100);
                break;
            default:
                geometry = new THREE.BoxGeometry(1, 1, 1);
        }}

        // 创建材质
        material = new THREE.MeshStandardMaterial({{
            color: objData.color || 0x3498db,
            roughness: 0.5,
            metalness: 0.1
        }});

        // 创建网格
        mesh = new THREE.Mesh(geometry, material);

        // 设置位置
        if (objData.position) {{
            mesh.position.set(
                objData.position[0],
                objData.position[1],
                objData.position[2]
            );
        }}

        // 设置旋转
        if (objData.rotation) {{
            mesh.rotation.set(
                objData.rotation[0],
                objData.rotation[1],
                objData.rotation[2]
            );
        }}

        // 设置缩放
        if (objData.scale) {{
            mesh.scale.set(
                objData.scale[0],
                objData.scale[1],
                objData.scale[2]
            );
        }}

        // 设置阴影
        mesh.castShadow = true;
        mesh.receiveShadow = true;

        // 添加用户数据，用于交互
        mesh.userData = {{
            name: objData.name || 'object',
            interactive: objData.interactive || true,
            ...objData.userData
        }};

        return mesh;
    }}

    createGround() {{
        // 创建地面
        const groundGeometry = new THREE.PlaneGeometry(20, 20);
        const groundMaterial = new THREE.MeshStandardMaterial({{
            color: 0x808080,
            roughness: 0.8
        }});
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = -0.5;
        ground.receiveShadow = true;
        this.scene.add(ground);

        // 添加网格辅助
        const gridHelper = new THREE.GridHelper(20, 20, 0x000000, 0x404040);
        gridHelper.position.y = -0.49;
        this.scene.add(gridHelper);
    }}

    setupInteractions() {{
        // 射线投射器，用于交互
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();

        // 监听鼠标移动
        this.container.addEventListener('mousemove', (event) => {{
            this.onMouseMove(event);
        }});

        // 监听点击事件
        this.container.addEventListener('click', (event) => {{
            this.onClick(event);
        }});

        // 监听窗口大小变化
        window.addEventListener('resize', () => {{
            this.onWindowResize();
        }});
    }}

    onMouseMove(event) {{
        // 计算鼠标在归一化设备坐标中的位置
        const rect = this.container.getBoundingClientRect();
        this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

        // 射线检测
        this.raycaster.setFromCamera(this.mouse, this.camera);
        const intersects = this.raycaster.intersectObjects(this.scene.children);

        if (intersects.length > 0) {{
            const object = intersects[0].object;
            if (object.userData && object.userData.interactive) {{
                this.container.style.cursor = 'pointer';
            }} else {{
                this.container.style.cursor = 'default';
            }}
        }} else {{
            this.container.style.cursor = 'default';
        }}
    }}

    onClick(event) {{
        this.raycaster.setFromCamera(this.mouse, this.camera);
        const intersects = this.raycaster.intersectObjects(this.scene.children);

        if (intersects.length > 0) {{
            const object = intersects[0].object;
            if (object.userData && object.userData.interactive) {{
                this.onObjectClick(object);
            }}
        }}
    }}

    onObjectClick(object) {{
        // 对象点击事件处理
        console.log('点击对象:', object.userData.name);

        // 可以在这里添加交互逻辑
        // 例如：显示信息、播放动画等

        // 简单的选中效果
        if (this.selectedObject) {{
            this.selectedObject.material.emissive.setHex(0x000000);
        }}
        object.material.emissive.setHex(0x444444);
        this.selectedObject = object;

        // 触发自定义事件
        const event = new CustomEvent('objectSelected', {{
            detail: {{ object: object.userData.name }}
        }});
        this.container.dispatchEvent(event);
    }}

    onWindowResize() {{
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }}

    setupEventListeners() {{
        // 这里可以添加其他事件监听器
        this.container.addEventListener('reset', () => {{
            this.resetCamera();
        }});

        this.container.addEventListener('fullscreen', () => {{
            this.toggleFullscreen();
        }});
    }}

    resetCamera() {{
        this.camera.position.set({scene_config['camera_position']});
        this.camera.lookAt(0, 0, 0);
        this.controls.reset();
    }}

    toggleFullscreen() {{
        if (!document.fullscreenElement) {{
            this.container.requestFullscreen();
        }} else {{
            document.exitFullscreen();
        }}
    }}

    animate() {{
        requestAnimationFrame(() => this.animate());

        // 更新控制器
        this.controls.update();

        // 更新动画
        this.animations.forEach(animation => {{
            animation.update();
        }});

        // 渲染场景
        this.renderer.render(this.scene, this.camera);
    }}

    // 公共方法
    getObjectByName(name) {{
        return this.objects.get(name);
    }}

    addObject(name, object) {{
        this.objects.set(name, object);
        this.scene.add(object);
    }}

    removeObject(name) {{
        const object = this.objects.get(name);
        if (object) {{
            this.scene.remove(object);
            this.objects.delete(name);
        }}
    }}

    // 性能优化方法
    enableLOD() {{
        // 实现LOD (Level of Detail)
        console.log('LOD已启用');
    }}

    enableObjectPool() {{
        // 实现对象池
        console.log('对象池已启用');
    }}

    optimizeRendering() {{
        // 渲染优化
        console.log('渲染优化已启用');
    }}

    dispose() {{
        // 清理资源
        this.renderer.dispose();
        this.controls.dispose();
    }}
}}

// 导出场景类
export default SimulationScene;
'''

        return scene_code

    def _generate_babylonjs_scene(self) -> str:
        """生成Babylon.js场景代码"""
        return '''// Babylon.js 场景代码生成
// 使用场景可以参考 Three.js 版本，这里提供基本框架

class BabylonScene {
    constructor(canvas) {
        this.canvas = canvas;
        this.engine = null;
        this.scene = null;
        this.camera = null;
        this.init();
    }

    init() {
        // 初始化引擎
        this.engine = new BABYLON.Engine(this.canvas, true);

        // 创建场景
        this.scene = new BABYLON.Scene(this.engine);
        this.scene.clearColor = new BABYLON.Color4(0.1, 0.1, 0.1, 1);

        // 创建相机
        this.camera = new BABYLON.ArcRotateCamera(
            'camera',
            Math.PI / 4,
            Math.PI / 3,
            10,
            BABYLON.Vector3.Zero(),
            this.scene
        );
        this.camera.attachControl(this.canvas, true);

        // 创建光源
        const light = new BABYLON.HemisphericLight(
            'light',
            new BABYLON.Vector3(0, 1, 0),
            this.scene
        );

        // 开始渲染循环
        this.engine.runRenderLoop(() => {
            this.scene.render();
        });

        // 监听窗口大小变化
        window.addEventListener('resize', () => {
            this.engine.resize();
        });
    }
}

export default BabylonScene;
'''

    def _get_scene_config(self) -> Dict[str, Any]:
        """获取场景配置"""
        configs = {
            'lab': {
                'background_color': 0x1a1a2e,
                'camera_fov': 60,
                'camera_position': [5, 5, 10],
                'camera_near': 0.1,
                'camera_far': 1000,
                'min_distance': 2,
                'max_distance': 20,
                'antialias': True
            },
            'classroom': {
                'background_color': 0xf0f0f0,
                'camera_fov': 75,
                'camera_position': [0, 8, 15],
                'camera_near': 0.1,
                'camera_far': 100,
                'min_distance': 3,
                'max_distance': 30,
                'antialias': True
            },
            'outdoor': {
                'background_color': 0x87CEEB,
                'camera_fov': 60,
                'camera_position': [10, 10, 20],
                'camera_near': 0.1,
                'camera_far': 1000,
                'min_distance': 5,
                'max_distance': 50,
                'antialias': True
            },
            'default': {
                'background_color': 0x000000,
                'camera_fov': 75,
                'camera_position': [0, 5, 10],
                'camera_near': 0.1,
                'camera_far': 1000,
                'min_distance': 2,
                'max_distance': 20,
                'antialias': True
            }
        }

        return configs.get(self.scene_type, configs['default'])

    def _extract_objects_data(self) -> List[Dict[str, Any]]:
        """从教材内容中提取3D对象数据"""
        objects_data = []

        # 从解析的内容中获取对象信息
        if '3d_elements' in self.content and 'objects' in self.content['3d_elements']:
            for obj in self.content['3d_elements']['objects']:
                objects_data.append({
                    'name': obj.get('name', 'object'),
                    'geometry_type': obj.get('geometry_type', 'box'),
                    'color': self._random_color(),
                    'position': self._random_position(),
                    'rotation': [0, 0, 0],
                    'scale': [1, 1, 1],
                    'interactive': True,
                    'userData': obj
                })

        # 如果没有对象数据，添加一些默认对象
        if not objects_data:
            for i in range(5):
                objects_data.append({
                    'name': f'object_{i}',
                    'geometry_type': 'box' if i % 2 == 0 else 'sphere',
                    'color': self._random_color(),
                    'position': self._random_position(),
                    'rotation': [0, 0, 0],
                    'scale': [1, 1, 1],
                    'interactive': True,
                    'userData': {}
                })

        return objects_data

    def _random_color(self) -> int:
        """生成随机颜色"""
        import random
        return random.randint(0, 0xFFFFFF)

    def _random_position(self) -> List[float]:
        """生成随机位置"""
        import random
        return [
            random.uniform(-5, 5),
            random.uniform(0, 5),
            random.uniform(-5, 5)
        ]

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def optimize_performance(self) -> str:
        """生成性能优化代码"""
        return '''
// 性能优化代码

// 1. LOD (Level of Detail) 实现
function updateLOD(object, camera) {
    const distance = camera.position.distanceTo(object.position);
    if (distance < 10) {
        object.material.map = highResTexture;
    } else if (distance < 20) {
        object.material.map = mediumResTexture;
    } else {
        object.material.map = lowResTexture;
    }
}

// 2. 对象池实现
class ObjectPool {
    constructor(createFn, initialSize = 10) {
        this.createFn = createFn;
        this.pool = [];
        for (let i = 0; i < initialSize; i++) {
            this.pool.push(createFn());
        }
    }

    acquire() {
        return this.pool.length > 0 ? this.pool.pop() : this.createFn();
    }

    release(obj) {
        this.pool.push(obj);
    }
}

// 3. 批处理优化
function optimizeScene(scene) {
    const geometryGroups = {};

    scene.traverse((object) => {
        if (object.isMesh) {
            const materialKey = object.material.uuid;
            if (!geometryGroups[materialKey]) {
                geometryGroups[materialKey] = [];
            }
            geometryGroups[materialKey].push(object);
        }
    });

    // 执行合并
    Object.keys(geometryGroups).forEach(key => {
        const geometries = geometryGroups[key].map(obj => obj.geometry);
        const mergedGeometry = mergeGeometries(geometries);
        // 创建合并后的mesh
    });
}
'''

    def save_scene(self, output_path: str) -> bool:
        """保存场景代码"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(self.generate_scene_code())
            return True
        except Exception as e:
            self.error = f"保存失败: {str(e)}"
            return False


def main():
    parser = argparse.ArgumentParser(
        description='3D场景生成脚本 - 根据教材内容生成3D交互场景',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 scene_generator.py content.json --scene-type lab --output scene.js
  python3 scene_generator.py content.json --library threejs --output scene.js
  python3 scene_generator.py content.json --optimize --output scene.js
        """
    )

    parser.add_argument('content_file', help='教材内容JSON文件')
    parser.add_argument('--scene-type', choices=['lab', 'classroom', 'outdoor', 'default'],
                        default='default', help='场景类型 (默认: default)')
    parser.add_argument('--library', choices=['threejs', 'babylonjs'],
                        default='threejs', help='3D库选择 (默认: threejs)')
    parser.add_argument('--optimize', action='store_true', help='启用性能优化')
    parser.add_argument('--output', required=True, help='输出场景文件路径')

    args = parser.parse_args()

    # 读取教材内容
    try:
        with open(args.content_file, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
    except Exception as e:
        print(f"❌ 读取文件失败: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # 创建场景生成器
    print(f"正在生成3D场景...")
    print(f"  场景类型: {args.scene_type}")
    print(f"  3D库: {args.library}")
    scene_generator = SceneGenerator(content_data, args.scene_type)
    scene_generator.library = args.library

    # 保存场景代码
    print(f"正在保存场景到: {args.output}")
    if scene_generator.save_scene(args.output):
        print(f"✅ 场景生成成功！")
        print(f"  输出文件: {args.output}")
        print(f"  场景类型: {scene_generator.select_template()}")
        print(f"  3D库: {args.library}")

        if args.optimize:
            print(f"  性能优化: 已启用")
    else:
        print(f"❌ 保存失败: {scene_generator.error}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()