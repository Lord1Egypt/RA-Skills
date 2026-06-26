# 微信小程序内容安全全指南

## 激活契约

**符合以下任一场景时加载：**
- 内容审核、内容安全、security check
- 文本审核、msgSecCheck、敏感词过滤
- 图片审核、imageSecCheck、色情/暴恐检测
- 用户发布内容、UGC、评论发帖
- 广告检测、违禁词检测、反垃圾

---

## 一、内容安全 API 概览

| API | 功能 | 调用位置 | 费用 |
|-----|------|---------|------|
| `security.msgSecCheck` | 文本安全检测 | 云函数 / 云托管 | 免费（有调用量限制）|
| `security.imgSecCheck` | 图片安全检测 | 云函数 / 云托管 | 免费（有调用量限制）|
| `security.mediaSecCheckAsync` | 音视频异步检测 | 云函数 / 云托管 | 按量计费 |

> ⚠️ 云开发内置了内容安全 SDK（`module security`），无需自行调用微信 HTTP API。

---

## 二、文本安全检测（msgSecCheck）

### 2.1 小程序端 → 云函数调用

```javascript
// utils/content-check.js

/**
 * 文本内容安全检测
 * @param {string} text - 待检测文本
 * @returns {Promise<{safe: boolean, detail?: object}>}
 */
async function checkText(text) {
  if (!text || text.trim().length === 0) {
    return { safe: true }
  }

  try {
    const res = await wx.cloud.callFunction({
      name: 'msgSecCheck',
      data: { content: text }
    })

    // wx-server-sdk security API 响应结构：
    // { errCode: number, errMsg: string, result: { errCode, suggest, label, ... } }
    // suggest: 'pass' | 'review' | 'block'
    if (res.result.errCode === 0 && res.result.suggest === 'pass') {
      return { safe: true }
    }

    // suggest: 'pass'=正常, 'review'=可疑需复核, 'block'=违规
    return {
      safe: false,
      detail: {
        suggest: res.result.suggest,
        label: res.result.label,  // 可选，违规分类标签
        message: getMessage(res.result.suggest),
      }
    }
  } catch (err) {
    console.error('[内容安全] 文本检测失败', err)
    // 失败时应走人工审核，不要直接放行
    return { safe: false, detail: { suggest: 'error', message: '检测服务异常，请稍后重试' } }
  }
}

function getMessage(suggest) {
  const map = {
    'pass':   '内容正常',
    'review': '内容可疑，建议人工复核',
    'block':  '内容违规，已拦截',
    'error':  '检测失败',
  }
  return map[suggest] ?? `未知状态（${suggest}）`
}

export { checkText }
```

### 2.2 云函数实现

```javascript
// cloudfunctions/msgSecCheck/index.js
const cloud = require('wx-server-sdk')
cloud.init()

// 云开发内置内容安全 SDK
const security = cloud.security

exports.main = async (event, context) => {
  const { content } = event

  if (!content) {
    return { code: -1, message: 'content is required', flag: -1 }
  }

  try {
    // wx-server-sdk security API 响应结构：
    // v1:  { errCode, errMsg }
    // v2:  { errCode, errMsg, result: { errCode, suggest, label, ... } }
    // suggest: 'pass' | 'review' | 'block'
    const res = await security.msgSecCheck({
      content,
      // openid: context.OPENID,  // 可选，传入后返回更精确的违规分析
      version: 2,               // v2 版本，更准确
    })

    console.log('[msgSecCheck]', JSON.stringify(res))

    // v2 响应中 result.suggest 才是内容安全判断依据
    const suggest = res.result?.suggest ?? res.suggest

    if (res.errCode === 0 && suggest === 'pass') {
      return { code: 0, flag: 0, message: 'pass', suggest }
    } else if (suggest === 'review') {
      return { code: 1, flag: 1, message: '需要人工审核', suggest }
    } else {
      return { code: 2, flag: 2, message: '内容违规，已拦截', suggest }
    }
  } catch (err) {
    console.error('[msgSecCheck Error]', err)
    return { code: -1, message: err.message || '检测异常', flag: -1 }
  }
}
```

### 2.3 典型业务场景

```javascript
// 发布评论
async function publishComment(text, images = []) {
  // 1. 先检测文本
  const textCheck = await checkText(text)
  if (!textCheck.safe) {
    wx.showModal({
      title: '内容审核',
      content: textCheck.detail.message,
      showCancel: false,
    })
    return
  }

  // 2. 检测图片（每张图单独检测）
  for (const img of images) {
    const imgCheck = await checkImage(img)
    if (!imgCheck.safe) {
      wx.showModal({
        title: '图片审核',
        content: `第 ${images.indexOf(img) + 1} 张图片未通过审核，请更换后重试`,
        showCancel: false,
      })
      return
    }
  }

  // 3. 全部通过，提交内容
  await wx.cloud.callFunction({
    name: 'publishComment',
    data: { text, images }
  })

  wx.showToast({ title: '发布成功', icon: 'success' })
}
```

---

## 三、图片安全检测（imgSecCheck）

### 3.1 小程序端 → 云函数调用

```javascript
/**
 * 图片安全检测（支持本地临时文件 / 云存储 fileID）
 * @param {string} path - 图片路径（本地路径或云存储 fileID）
 */
async function checkImage(path) {
  try {
    const res = await wx.cloud.callFunction({
      name: 'imgSecCheck',
      data: { filePath: path }
    })

    if (res.result.code === 0) {
      return { safe: true }
    }

    return { safe: false, detail: { message: res.result.message } }
  } catch (err) {
    return { safe: false, detail: { message: '图片检测失败', error: err } }
  }
}
```

### 3.2 云函数实现

```javascript
// cloudfunctions/imgSecCheck/index.js
const cloud = require('wx-server-sdk')
const fs = require('fs')
const path = require('path')
cloud.init()

const security = cloud.security

exports.main = async (event, context) => {
  const { filePath } = event

  if (!filePath) {
    return { code: -1, message: 'filePath is required' }
  }

  try {
    // 判断是云存储 fileID 还是本地临时文件
    if (filePath.startsWith('cloud://')) {
      // 云存储 fileID 方式（推荐，文件已在云端）
      // ⚠️ imgSecCheck 的 img.url 支持云存储 fileID（cloud://xxx）直接传入
      // 但需确保 fileType 与实际文件 MIME 类型一致
      const res = await security.imgSecCheck({
        fileType: 'image/png',  // ⚠️ 需根据实际文件类型动态设置：image/png | image/jpeg | image/gif
        img: {
          url: filePath,        // 支持 cloud:// 开头的 fileID
        },
        version: 2,
      })

      const cloudSuggest = res.result?.suggest ?? res.suggest
      if (res.errCode === 0 && cloudSuggest === 'pass') {
        return { code: 0, message: 'pass', suggest: cloudSuggest }
      }
      return {
        code: cloudSuggest === 'block' ? 2 : 1,
        message: '图片违规',
        suggest: cloudSuggest,
      }
    } else {
      // 本地临时文件，需要先上传到云存储
      const uploadRes = await cloud.uploadFile({
        cloudPath: `temp/${Date.now()}.jpg`,
        filePath,
      })

      const checkRes = await security.imgSecCheck({
        fileType: 'image/jpeg',
        img: { url: uploadRes.fileID },
        version: 2,
      })

      // 清理临时文件
      await cloud.deleteFile({ fileList: [uploadRes.fileID] })

      // imgSecCheck 响应同 msgSecCheck：{ errCode, result: { suggest } }
      const imgSuggest = checkRes.result?.suggest ?? checkRes.suggest
      if (checkRes.errCode === 0 && imgSuggest === 'pass') {
        return { code: 0, message: 'pass', suggest: imgSuggest }
      }
      return {
        code: imgSuggest === 'block' ? 2 : 1,
        message: '图片违规',
        suggest: imgSuggest,
      }
    }
  } catch (err) {
    console.error('[imgSecCheck Error]', err)
    return { code: -1, message: err.message || '检测异常' }
  }
}
```

---

## 四、昵称/头像审核（security.nicknameCheck）

```javascript
// 用户修改昵称时的审核
async function checkNickname(nickname) {
  const res = await wx.cloud.callFunction({
    name: 'nicknameCheck',
    data: { nickname }
  })

  if (res.result.code === 0) {
    return true  // 通过
  }
  wx.showModal({
    title: '昵称审核未通过',
    content: '昵称可能包含敏感词，请修改后重试',
    showCancel: false,
  })
  return false
}
```

```javascript
// cloudfunctions/nicknameCheck/index.js
const cloud = require('wx-server-sdk')
cloud.init()
const security = cloud.security

exports.main = async (event, context) => {
  try {
    const res = await security.msgSecCheck({
      content: event.nickname,
      version: 2,
    })

    const suggest = res.result?.suggest ?? res.suggest
    if (res.errCode === 0 && suggest === 'pass') {
      return { code: 0, suggest }
    }
    return { code: 2, message: '昵称包含敏感词', suggest }
  } catch (err) {
    return { code: -1, message: err.message }
  }
}
```

---

## 五、调用限制与配额

| 接口 | 每日免费额度（参考值）| 超额后 |
|------|------------|--------|
| msgSecCheck | 10,000 次/天 | 需申请提高配额或付费 |
| imgSecCheck | 1,000 次/天 | 需申请提高配额或付费 |
| mediaSecCheckAsync | 100 次/天 | 按量计费 |

> ⚠️ 以上为估算值，**实际配额以微信云开发控制台（云开发 → 内容安全 → 配额管理）实时数据为准**。敏感行业（社交、直播等）建议申请企业认证并申请更高配额。

---

## 六、Common Mistakes（高频错误）

| 错误 | 正确做法 |
|------|---------|
| 检测失败后直接放行 | 失败应走人工复核或拒绝，不要直接放行 |
| 图片检测用本地路径而非 fileID | 云存储图片用 `cloud://` fileID，本地文件需先上传 |
| 文本为空也调用检测 | 空文本直接返回 safe，跳过调用节省配额 |
| 一次检测大量文本 | msgSecCheck 单次限制 500KB，分段截断后再检测 |
| 图片太大导致超时 | 图片建议先压缩（max 2MB），过大文件不检测 |
| 版本号写错 | version 必填，建议使用 v2 版本（更准确）|
| 昵称审核不处理 emoji | 昵称中 emoji 也参与检测，过滤需保留原字符串 |

---

## 七、官方文档链接

- 内容安全 API：https://developers.weixin.qq.com/miniprogram/dev/open-functional-content/security.html
- 文本内容安全：https://developers.weixin.qq.com/miniprogram/dev/user-information/legal-information.html
- 敏感词过滤：https://developers.weixin.qq.com/miniprogram/dev/framework/client-lib/checker.html
