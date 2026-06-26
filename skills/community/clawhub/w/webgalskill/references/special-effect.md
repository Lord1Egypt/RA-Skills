# 特效

## 命令速查

| 命令 | 语法 | 说明 |
| :--- | :--- | :--- |
| 初始化Pixi | `pixiInit;` | 初始化特效系统 |
| 添加特效 | `pixiPerform:特效名;` | 添加粒子特效 |
| 清除特效 | `pixiInit;` | 重新初始化可清除所有特效 |

## 使用特效

WebGAL 特效系统由 PixiJS 实现。

### 初始化

使用特效前必须先初始化：

```ws
pixiInit;
```

> 重新初始化会清除所有已应用的效果。

### 预制特效

```ws
pixiPerform:rain;        // 雨
pixiPerform:snow;       // 雪
pixiPerform:heavySnow;  // 大雪
pixiPerform:cherryBlossoms; // 樱花
```

### 叠加特效

不使用 `pixiInit` 的情况下可叠加多个效果：

```ws
pixiPerform:rain;
pixiPerform:snow;
```

### 清除特效

重新执行 `pixiInit` 即可清除所有效果：

```ws
pixiInit; // 清除所有已叠加的特效
```

## 自定义特效

### 开发步骤

1. 下载 WebGAL 源代码
2. 在 `/Core/gameScripts/pixiPerformScripts/` 创建新的 `PIXI.Container`
3. 编译：`yarn run build`

### 代码结构

```ts
import {registerPerform} from '../pixiPerformManager';

// 获取效果容器
const effectsContainer = WebGAL.gameplay.pixiStage!.foregroundEffectsContainer!;
const app = WebGAL.gameplay.pixiStage!.currentApp!;

// 创建自定义特效容器
const container = new PIXI.Container();
effectsContainer.addChild(container);

// 注册特效
function myPerform() {
    // ... 特效逻辑
}

registerPerform('myPerform', { fg: () => myPerform() });
```

### 纹理文件

自定义特效使用的纹理文件放在 `game/tex/` 目录下。

### 调用自定义特效

```ws
pixiPerform:myPerform;
```
