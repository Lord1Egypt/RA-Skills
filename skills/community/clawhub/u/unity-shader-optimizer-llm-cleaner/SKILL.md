---
name: unity-hlsl-style
description: Unity HLSL Shader 代码风格规范，要求减少重复代码、提取共用函数、合理使用头文件。使用场景：编写 Unity Shader、重构重复 Shader 代码、生成新 Shader 时遵循 DRY 原则。
---

# Unity HLSL Shader 代码风格规范 - 减少重复代码

## 核心原则：DRY (Don't Repeat Yourself)

**绝不复制粘贴整段重复代码**。如果发现多个 Pass 或多个 Shader 有大量相同代码，必须提取共用。

## 具体规范

### 1. 提取共用函数到头文件

**做法**：
- 把共用的函数（比如颜色调整、边缘检测、法线变换等）放到 `.hlsl` 头文件
- 在每个需要的 Pass 中 `#include "YourCommonFunctions.hlsl"`

**示例**：

```hlsl
// Common/ColorAdjustment.hlsl - 共用头文件
float CalculateLuminance(float3 rgb) {
    return 0.2126 * rgb.x + 0.7152 * rgb.y + 0.0722 * rgb.z;
}

float3 ApplyColorBalance(float3 rgb, ...) {
    // ... 实现代码
}

float3 ApplySaturation(float3 rgb, float saturation) {
    // ... 实现代码
}

float3 ApplyBrightnessContrast(float3 rgb, float brightness, float contrast) {
    // ... 实现代码
}
```

然后在 Pass 里只需要：
```hlsl
#include "Common/ColorAdjustment.hlsl"
```

**好处**：
- 修改只改一处，所有地方都更新
- Shader 文件变短，更容易阅读
- 避免复制粘贴带来的不一致

### 2. 共用 CB_BUFFER（材质属性）也放头文件

如果多个 Pass 使用完全相同的材质属性，可以把 CBUFFER 定义也放头文件：

```hlsl
// Common/MyShaderProperties.hlsl
CBUFFER_START(UnityPerMaterial)
    float4 _MainTex_ST;
    float4 _MainTex_TexelSize;
    float4 _Color;
    float _EnableEdgeLight;
    float3 _RimColor;
    float _RimPower;
    float _RimIntensity;
    float _Brightness;
    float _Contrast;
    float _Saturation;
    // ... 其他属性
CBUFFER_END
```

### 3. 多个 Pass 只有 Blend 不同？不要复制整份代码

**问题**：URP 中经常需要两个 Pass：一个 Straight Alpha，一个 Premultiply Alpha，大部分代码完全一样，只是 Blend 不同。

**不好的做法**：复制粘贴整个 Pass 的所有代码，包括所有函数。✖️

**好的做法**：
- 把 vertex/fragment 都放在头文件
- 两个 Pass 只保留 ShaderLab 框架（Pass 标签、Blend 状态），然后 `HLSLPROGRAM` 里 `#include` 共用代码

**示例结构**：

```shaderlab
Shader "My/Shader"
{
    Properties { /* ... 属性只写一次 ... */ }

    SubShader
    {
        // Pass 1: Straight Alpha
        Pass
        {
            Name "StraightAlpha"
            Blend One OneMinusSrcAlpha

            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #define IS_STRAIGHT_ALPHA 1
            #include "MyShader_Pass.hlsl"
            ENDHLSL
        }

        // Pass 2: Premultiply Alpha
        Pass
        {
            Name "PremultiplyAlpha"
            Blend SrcAlpha OneMinusSrcAlpha

            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #define IS_STRAIGHT_ALPHA 0
            #include "MyShader_Pass.hlsl"
            ENDHLSL
        }
    }
    Fallback "Sprites/Default"
}
```

这样，所有真正的代码都在 `MyShader_Pass.hlsl` 里，只写一次。

### 4. 文件组织结构推荐

对于一个有多个 Pass 的复杂 Shader：

```
YourShader/
├── YourShader.shader         (主文件，只放 Properties 和 Pass 框架)
├── YourShader_Common.hlsl    (共用函数和属性定义)
└── YourShader_Pass.hlsl      (vertex/fragment 实现，被两个 Pass include)
```

对于多个相似 Shader：

```
Shaders/
├── Common/
│   ├── ColorAdjustment.hlsl  (所有 Shader 共用的颜色调整函数)
│   ├── RimLighting.hlsl      (所有 Shader 共用的边缘光计算)
│   └── ...
├── ShaderA/
│   ├── ShaderA.shader
│   └── ShaderA_Pass.hlsl
└── ShaderB/
    ├── ShaderB.shader
    └── ShaderB_Pass.hlsl
```

### 5. 什么时候可以接受少量重复？

- **单个 Pass 的非常简单的 Shader**：可以全写在一个文件里，不需要拆分
- **只有一两个重复的小函数**：可以接受留在文件里，不用为了两三行拆个头文件
- **实验性/测试代码**：可以先写重复的，稳定了再重构

**记住**：大于 20 行的重复代码 → 必须提取。

## 代码审查要点

当生成或修改 Shader 代码时，检查：

- [ ] 是否有大于 20 行的重复代码块？
- [ ] 多个 Pass 是否重复了相同的函数和 CBUFFER？
- [ ] 共用函数是否应该提取到头文件？
- [ ] 文件拆分是否清晰，主文件是否只保留框架？
- [ ] **换行符一致性**：在 Windows 平台开发 Unity 项目，所有 Shader 文件必须使用 Windows CRLF (`\r\n`) 换行符，避免混合换行符导致 Unity 警告。

## 换行符规范

- **Windows Unity 开发**：统一使用 CRLF (`\r\n`)
- **避免**：混合 LF 和 CRLF，这会导致 Unity 输出 "inconsistent line endings" 警告
- 创建新文件后，统一转换为当前平台的换行符格式

## ShaderLab 基础结构规范

**必须严格遵守 ShaderLab 三级结构**：
```shaderlab
Shader "Your/Shader/Name"
{
    Properties { ... }

    SubShader
    {
        Tags { ... }

        // 每个 Pass 必须独立用 {} 包裹
        Pass
        {
            // HLSLPROGRAM / ENDHLSL 必须放在 Pass {} 里面
            HLSLPROGRAM
            // ... 代码 ...
            ENDHLSL
        }
    }
    Fallback "...";
}
```

**典型错误**（❌ 非法结构）：
```shaderlab
Shader "Wrong/Shader"
{
    Properties { ... }
    SubShader
    {
        Tags { ... }
        // ❌ HLSLPROGRAM 直接放在 SubShader，没有 Pass 包裹
        HLSLPROGRAM
        ...
        ENDHLSL
    }
}
```

**为什么报错**：Unity ShaderLab 解析器要求 `HLSLPROGRAM` 必须在 `Pass` 块内，否则解析会失败，报 "unexpected }" 语法错误。

**URP 额外要求**：必须给 Pass 添加 `LightMode = "UniversalForward"` Tag：
```shaderlab
Tags
{
    "RenderPipeline" = "UniversalPipeline"
    "RenderType" = "Transparent"
    "Queue" = "Transparent"
    "IgnoreProjector" = "True"
    "LightMode" = "UniversalForward" // ⭐ URP 必需
}
```

**纹理采样规范（URP）**：
URP (SRP) 推荐使用现代宏定义方式采样纹理，避免老写法 `tex2D` 在部分平台出问题：
```hlsl
// ✅ 正确 URP 写法
TEXTURE2D(_MainTex);
SAMPLER(sampler_MainTex);
...
half4 col = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv);
```

❌ 不推荐（但是兼容大多数平台）：
```hlsl
sampler2D _MainTex;
...
half4 col = tex2D(_MainTex, uv);
```

## 错误示例（不好）

```hlsl
// Pass 1
half4 frag (Varyings input) : SV_Target {
    // 100 行代码...
}

// Pass 2
half4 frag (Varyings input) : SV_Target {
    // 一模一样的 100 行代码... 只有一行 Blend 相关不同
}
```

❌ 这是错误的，必须提取。

## 正确示例（好）

```hlsl
// Pass 1
HLSLPROGRAM
#pragma vertex vert
#pragma fragment frag
#define STRAIGHT_ALPHA 1
#include "SpineURP_EdgeLight_Pass.hlsl"
ENDHLSL

// Pass 2
HLSLPROGRAM
#pragma vertex vert
#pragma fragment frag
#define STRAIGHT_ALPHA 0
#include "SpineURP_EdgeLight_Pass.hlsl"
ENDHLSL
```

✅ 这样只有一份代码，维护方便。
