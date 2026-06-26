# AI绘图

调用 NanaBanana 2 和 NanaBanana Pro 生成图片。

## 可用模型

| 模型 | 适用场景 | 优先级 |
|------|----------|--------|
| NanaBanana 2 | 日常绘图、文字图、快速出图、批量生成 | ⭐ 默认优先使用 |
| NanaBanana Pro | 用户明确要求"高质量""写实""最终稿""电影感"时使用 | 备选 |

默认始终使用 NanaBanana 2，除非用户明确要求更高画质才切换到 Pro。

## API 密钥

所有接口共用同一密钥：`【你的密钥】`

---

## NanaBanana 2 接口

### 第一步：提交任务

- 方式：POST
- 地址：`https://api.wuyinkeji.com/api/async/image_nanoBanana2`
- Headers：
  - Authorization: `【你的密钥】`
  - Content-Type: application/json
- Body（JSON）：
  ```json
  {
    "key": "【你的密钥】",
    "prompt": "详细的英文图片描述",
    "size": "1K",
    "aspectRatio": "auto"
  }
  ```

### 第二步：查询结果

- 方式：GET
- 地址：`https://api.wuyinkeji.com/api/async/detail?key=【你的密钥】&id={task_id}`
- Headers：
  - Authorization: `【你的密钥】`

---

## NanaBanana Pro 接口

### 第一步：提交任务

- 方式：POST
- 地址：`https://api.wuyinkeji.com/api/async/image_nanoBanana_pro`
- Headers：
  - Authorization: `【你的密钥】`
  - Content-Type: application/json
- Body（JSON）：
  ```json
  {
    "key": "【你的密钥】",
    "prompt": "详细的英文图片描述",
    "size": "1K",
    "aspectRatio": "auto"
  }
  ```

### 第二步：查询结果

- 方式：GET
- 地址：`https://api.wuyinkeji.com/api/async/detail?key=【你的密钥】&id={task_id}`
- Headers：
  - Authorization: `【你的密钥】`

---

## 通用参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| prompt | ✅ | 图片描述，务必翻译为英文，越详细越好 |
| size | ❌ | 分辨率，可选 1K / 2K / 4K，默认 1K |
| aspectRatio | ❌ | 画面比例，可选 auto / 1:1 / 16:9 / 9:16 / 4:3 / 3:4 / 3:2 / 2:3 / 5:4 / 4:5 / 21:9，默认 auto |

---

## 轮询策略

1. 提交任务后，从返回的 `data.id` 获取 task_id
2. 每隔 **3秒** 请求一次结果接口
3. 最多请求 **20次**（约60秒）
4. 当返回 `code=200` 且 `data.status=2` 且 `data.result` 包含图片URL时，视为成功

### 状态码说明

| status | 说明 |
|--------|------|
| 0 | 处理中 |
| 1 | 排队中 |
| 2 | ✅ 成功，result字段包含图片URL |
| 3 | 失败，message字段包含错误信息 |

---

## 输出规则

1. 获取到图片地址后，用 `<qqimg>URL</qqimg>` 标签发送给用户
2. 告知用户使用了哪个模型、比例和分辨率
3. 若用户未指定 size 和 aspectRatio，根据描述内容智能推断最合适的参数
4. 若超时未获取结果（20次轮询后仍无结果），告知用户稍后重试

---

## 模型选择示例

- 用户：帮我画一只猫 → 使用 **NanaBanana 2**
- 用户：帮我画一张高质量的产品宣传图 → 使用 **NanaBanana Pro**
- 用户：快速生成几张草图 → 使用 **NanaBanana 2**
- 用户：我要最终交付的写实人像 → 使用 **NanaBanana Pro**

---

## 注意事项

- 注意敏感词过滤，某些词汇可能触发审核导致失败（如"睡衣"、"性感"等）
- 提交时key可以放在URL参数里，也可以放在Body的json里
- 查询时key必须放在URL参数里
