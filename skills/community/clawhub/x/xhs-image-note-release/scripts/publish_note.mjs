// publish_note.mjs — 小红书笔记发布（浏览器流程层）
//
// 由 publish_note.sh 调用：ego-browser nodejs < publish_note.mjs
// 参数通过 /tmp/xhs_publish_params.json 传入（ego-browser 的 nodejs 环境不继承 shell 环境变量）
//
// 设计约定：
//   1. 所有选择器集中在 SEL，所有超时集中在 T，改版时只动这两处
//   2. 每个业务步骤用 step() 包裹，自动计时；失败一律走 fail()，不裸抛异常
//   3. fail() 输出结构化失败块（step/code/exit/message/detail/what_now/space），
//      并默认保留 task space，让 agent 或人能接着看现场
//   4. 退出码见 EXIT，与 SKILL.md 的「退出码与失败处理」一章一一对应

import fs from 'fs'

// ============================================================
// 参数
// ============================================================
const PARAM_FILE = '/tmp/xhs_publish_params.json'
const params = JSON.parse(fs.readFileSync(PARAM_FILE, 'utf8'))

if (params.error) {
  // bash 侧已经校验过，这里是兜底：参数层拒绝时不启动浏览器
  process.stderr.write('E_PARAM: ' + params.error + '\n')
  process.exit(10)
}

const isVideo = params.mediaType === 'video'
const mediaDir = params.mediaDir
const filePaths = params.files.map((f) => mediaDir + '/' + f)
const title = params.title
const bodyText = (params.body || '').replace(/\\n/g, '\n')
const topics = params.topics || []
const MODE = params.mode || 'publish'
const coverImage = params.coverImage || ''
const keepOnFail = params.keepOnFail !== false
const LOG_FILE = params.logFile || ''

// ============================================================
// 选择器（小红书改版时优先改这里）
// ============================================================
const SEL = {
  videoInput: 'input[type="file"][accept*=".mp4"]',
  imageInput: 'input[type="file"][accept*=".png"]',
  coverInput: 'input[type="file"][accept*="image/png"]',
  titleInput: 'input[placeholder="填写标题会有更多赞哦"]',
  editor: 'div.tiptap',
  editorFallback: '[contenteditable="true"]',
  topicContainer: '#creator-editor-topic-container',
  publishHost: 'xhs-publish-btn',
  coverBox: '.cover',
  coverEditEntry: '.cover-edit-entry',
  coverModal: '.d-modal.cover-modal',
  coverDoneBtn: 'span.circle-button-content',
  coverGuide: '.pk-cover-guide-tooltip, .pk-cover-guide',
  draftEntry: '.header-draft',
}

const UPLOAD_SEL = isVideo ? SEL.videoInput : SEL.imageInput
const TAB_TEXT = isVideo ? '上传视频' : '上传图文'

// ============================================================
// 超时（毫秒）
// ============================================================
const T = {
  spaReady: 15,           // SPA 首屏渲染（秒，给 wait() 用）
  videoUpload: 120000,    // 上传 + 转码
  imageUpload: 90000,
  topicDropdown: 6000,    // 话题下拉出现
  coverHover: 2500,       // hover 后「编辑封面」渲染
  coverEditor: 15000,     // 封面编辑器打开
  publishResult: 25000,   // 提交后等待跳转
  poll: 800,              // 轮询间隔（毫秒）
}

// ============================================================
// 退出码（与 SKILL.md 表格一致，改动需同步文档）
// ============================================================
const EXIT = {
  OK: 0,
  PARAM: 10,
  AUTH: 20,
  TAB: 21,
  UPLOAD: 30,
  FORM: 40,
  TOPIC: 50,
  COVER: 60,
  SUBMIT: 70,
  VERIFY: 80,
  INTERNAL: 90,
}

// ============================================================
// 日志
// ============================================================
function log(msg) {
  const line = String(msg)
  cliLog(line)
  if (LOG_FILE) {
    try {
      fs.appendFileSync(LOG_FILE, line + '\n')
    } catch (e) {
      // 日志写失败不影响主流程
    }
  }
}

let TASK = null

// ============================================================
// 统一失败出口
// ============================================================
async function fail(step, code, exitCode, message, detail, whatNow) {
  const lines = ['']
  lines.push('=== FAILED ===')
  lines.push('step     : ' + step)
  lines.push('code     : ' + code)
  lines.push('exit     : ' + exitCode)
  lines.push('message  : ' + message)
  if (detail && Object.keys(detail).length > 0) {
    lines.push('detail   : ' + JSON.stringify(detail).slice(0, 600))
  }
  lines.push('what_now :')
  ;(whatNow || ['把以上输出发给 agent 排查']).forEach((w, i) => {
    lines.push('  ' + (i + 1) + '. ' + w)
  })
  if (TASK) {
    lines.push('space    : ' + TASK.id + (keepOnFail ? '（页面已保留）' : '（已关闭）'))
    if (keepOnFail) {
      lines.push('takeover : ego-browser nodejs -e "await claimTaskSpace(' + TASK.id + ')"')
      lines.push('cleanup  : ego-browser nodejs -e "await completeTaskSpace(' + TASK.id + ', { keep: false })"')
    }
  }
  lines.push('=== END FAILED ===')
  lines.forEach((l) => log(l))

  try {
    if (TASK) await completeTaskSpace(TASK.id, { keep: keepOnFail })
  } catch (e) {
    // 清理失败不应掩盖原始错误
  }
  process.exit(exitCode)
}

// ============================================================
// 步骤包装：计时 + 意外异常兜底
// ============================================================
async function step(name, fn) {
  const t0 = Date.now()
  log('')
  log('▶ ' + name)
  try {
    const r = await fn()
    log('✔ ' + name + ' (' + (Date.now() - t0) + 'ms)')
    return r
  } catch (e) {
    await fail(
      name,
      'E_UNEXPECTED',
      EXIT.INTERNAL,
      String((e && e.message) || e),
      { stack: String((e && e.stack) || '').split('\n').slice(0, 3).join(' | ').slice(0, 400) },
      [
        '这是未预期的异常，通常是脚本 bug 或 ego-browser 连接中断',
        '页面已保留，可直接接管看现场（见下方 takeover 命令）',
        '把这个 code 和 detail 一起发给 agent，便于定位',
      ]
    )
  }
}

// ============================================================
// 轮询工具：替代固定 sleep
// ============================================================
async function waitFor(desc, probe, timeoutMs, intervalMs) {
  const interval = intervalMs || T.poll
  const t0 = Date.now()
  let last = null
  while (Date.now() - t0 < timeoutMs) {
    last = await probe()
    if (last && last.done) {
      return { ok: true, state: last, elapsed: Date.now() - t0 }
    }
    await wait(interval / 1000)
  }
  return { ok: false, state: last, elapsed: Date.now() - t0 }
}

// ============================================================
// 主流程
// ============================================================
log('mediaType=' + params.mediaType + ' files=' + filePaths.length + ' mode=' + MODE + ' cover=' + (coverImage || '(default)'))

// ---- 1. 建立 task space 并打开创作平台 ----
await step('open-publish-page', async () => {
  TASK = await useOrCreateTaskSpace('publish xhs note ' + Date.now())
  log('task space: ' + TASK.id)
  await openOrReuseTab('https://creator.xiaohongshu.com/publish/publish', { wait: true, timeout: 25 })
  await wait(T.spaReady)
})

// ---- 2. 登录态 ----
await step('auth', async () => {
  const st = await js(`(() => {
    const href = location.href || ''
    if (href.includes('/login')) return { ok: false, reason: 'redirected_to_login', url: href }
    const text = document.body ? document.body.innerText : ''
    if (!text.includes('笔记管理') && !text.includes('草稿箱')) {
      return { ok: false, reason: 'no_manage_entry', url: href }
    }
    return { ok: true, url: href }
  })()`)
  if (!st.ok) {
    await fail('auth', 'E_AUTH_EXPIRED', EXIT.AUTH, '登录态失效（' + st.reason + '）', st, [
      '在 ego-lite 浏览器窗口手动打开 creator.xiaohongshu.com 并完成登录',
      '登录后回复 continue，让 agent 用 claimTaskSpace(' + (TASK ? TASK.id : '<space>') + ') 认领同一个 space（该 space 的控制权已转给你，claimTaskSpace 才对）',
      '如果 agent 操作时报 "user has taken control"，说明登录把控制权交给你了，这是正常现象，接管后继续即可',
      '登录态正常后重跑本脚本',
    ])
  }
  log('logged in: ' + st.url)
})

// ---- 3. 切到对应的上传 tab ----
await step('ensure-upload-tab', async () => {
  let ready = await js(`!!document.querySelector('${UPLOAD_SEL}')`)
  if (ready) {
    log('already on ' + TAB_TEXT)
    return
  }

  const clicked = await js(`((want) => {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false)
    let node
    while ((node = walker.nextNode())) {
      if (node.textContent.trim() === want) {
        let el = node.parentElement
        for (let i = 0; i < 4; i++) {
          if (!el) break
          el.click()
          el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }))
          el = el.parentElement
        }
        return true
      }
    }
    return false
  })('${TAB_TEXT}')`)
  log('tab click: ' + clicked)
  await wait(3)
  ready = await js(`!!document.querySelector('${UPLOAD_SEL}')`)

  if (!ready) {
    // 回退：走「发布笔记」下拉菜单
    const pageText = await snapshotText()
    const m1 = pageText.match(/发布笔记.*?\[ref=(\d+)/)
    if (m1) {
      await click('@' + m1[1], { label: 'click 发布笔记 dropdown' })
      await wait(2)
      const t2 = await snapshotText()
      const m2 = t2.match(new RegExp(TAB_TEXT + '.*?\\\\[ref=(\\\\d+)'))
      if (m2) {
        await click('@' + m2[1], { label: 'click ' + TAB_TEXT })
        await waitForNetworkIdle(5)
        await wait(3)
      }
    }
    ready = await js(`!!document.querySelector('${UPLOAD_SEL}')`)
  }

  if (!ready) {
    await fail('ensure-upload-tab', 'E_TAB_NOT_FOUND', EXIT.TAB, '未能进入「' + TAB_TEXT + '」页', { selector: UPLOAD_SEL }, [
      '手动在页面上点一下「' + TAB_TEXT + '」，确认能进入编辑页',
      '如果页面停在别的 tab，重跑脚本会再次尝试点击',
      '页面已保留，可直接接管检查：见下方 takeover 命令',
    ])
  }
  log('upload page ready: ' + TAB_TEXT)
})

// ---- 4. 上传素材 ----
await step('upload-media', async () => {
  if (isVideo) {
    log('uploading video: ' + filePaths[0])
    await uploadFile(UPLOAD_SEL, filePaths[0])
    await wait(5)

    const r = await waitFor('video', async () => {
      const v = await js(`(() => {
        const text = document.body ? document.body.innerText : ''
        let readyState = 0
        try {
          readyState = Math.max(0, ...[...document.querySelectorAll('video')].map((el) => el.readyState || 0))
        } catch (e) {}
        return {
          done: text.includes('重新上传') && !!document.querySelector('${SEL.titleInput}'),
          hasReupload: text.includes('重新上传'),
          hasTitleInput: !!document.querySelector('${SEL.titleInput}'),
          readyState: readyState
        }
      })()`)
      return v
    }, T.videoUpload)

    if (!r.ok) {
      await fail('upload-media', 'E_VIDEO_UPLOAD_TIMEOUT', EXIT.UPLOAD,
        '视频上传/转码超时（' + Math.round(T.videoUpload / 1000) + 's）',
        r.state ? r.state : {},
        [
          '确认视频文件本身能正常播放（ffprobe 检查时长与编码）',
          '大文件或高码率视频转码会更久，可先压缩到 1080p 再传',
          '网络抖动时直接重跑本脚本，会重新上传',
        ])
    }
    log('video ready after ' + r.elapsed + 'ms')
  } else {
    for (let i = 0; i < filePaths.length; i++) {
      log('uploading ' + (i + 1) + '/' + filePaths.length + ': ' + filePaths[i])
      await uploadFile(UPLOAD_SEL, filePaths[i])
      await wait(6)
    }
    await wait(4)

    // 三个独立信号，任一命中即认为上传完成（v2.0.1 修正）：
    //   ① 「图片编辑 N/18」——小红书把标签和数字渲染在**两行**里，旧实现按行取
    //      再 split('/')[0]，拿到的永远是标签本身，editCount 恒为空串、主判据失效。
    //   ② 编辑区每张图各有一个「编辑」入口，数量应与张数一致（结构判据）。
    //   ③ 图床缩略图数量——必须排除 avatar，旧实现把用户头像也算进了 cdnImages，
    //      导致数字既可能虚高也可能永远凑不满。
    const r = await waitFor('images', async () => {
      const v = await js(`(() => {
        const expect = ${filePaths.length}
        const text = document.body.innerText || ''

        let editCount = -1
        let slotTotal = -1
        const m = text.match(/图片编辑[\\s:：]{0,6}(\\d{1,2})\\s*\\/\\s*(\\d{1,2})/)
        if (m) {
          editCount = parseInt(m[1], 10)
          slotTotal = parseInt(m[2], 10)
        }

        let editEntries = 0
        for (const el of document.querySelectorAll('div, span, a, button')) {
          if (el.children.length === 0 && (el.textContent || '').trim() === '编辑') editEntries++
        }

        const cdn = [...document.querySelectorAll('img')].filter((i) => {
          const s = i.src || ''
          if (s.indexOf('avatar') >= 0) return false
          return s.indexOf('xhscdn.com') >= 0 || s.indexOf('spectrum/') >= 0
        }).length

        return {
          done: editCount >= expect || editEntries >= expect || cdn >= expect,
          editCount: editCount >= 0 ? editCount + '/' + slotTotal : 'n/a',
          editEntries: editEntries,
          cdnImages: cdn,
          expected: expect
        }
      })()`)
      return v
    }, T.imageUpload)

    if (!r.ok) {
      await fail('upload-media', 'E_IMAGE_UPLOAD_TIMEOUT', EXIT.UPLOAD,
        '图片未在预期时间内全部进入编辑区（三个信号都不达标）',
        r.state ? r.state : {},
        [
          '确认图片是 png/jpg/webp 且单张 < 32MB',
          '小红书对批量 setFileInputFiles 只留空占位，本脚本已用 uploadFile 逐个上传，若仍失败多半是网络',
          '若 detail 里 editCount 已 >= expected，说明是判定逻辑又跟不上改版，按上面 space 接管页面手动收尾',
          '直接重跑本脚本',
        ])
    }
    log('images ready: ' + JSON.stringify(r.state))
  }
})

// 核对草稿是否真的写进了浏览器本地库。
// 不走「点草稿箱面板」那条路：小红书的草稿入口位置改过版（原左侧栏 → 现右上角 .header-draft），
// 且点击不一定能展开面板，容易误判。直接读 IndexedDB 更稳：
//   draft-database-v1 → video-draft / image-draft，每条的 content 里递归找 title 字段
async function verifyDraftEntry(expectedTitle) {
  try {
    const st = await js(`(async () => {
      const storeName = ${JSON.stringify(isVideo ? 'video-draft' : 'image-draft')}
      const want = ${JSON.stringify(expectedTitle || '')}
      const db = await new Promise(function (res, rej) {
        const r = indexedDB.open('draft-database-v1')
        r.onsuccess = function () { res(r.result) }
        r.onerror = function () { rej(r.error || new Error('open failed')) }
      })
      const all = await new Promise(function (res) {
        try {
          const tx = db.transaction([storeName], 'readonly')
          const req = tx.objectStore(storeName).getAll()
          req.onsuccess = function () { res(req.result || []) }
          req.onerror = function () { res([]) }
        } catch (e) { res([]) }
      })
      db.close()
      if (!all.length) return { ok: false, reason: 'store ' + storeName + ' 为空' }
      all.sort(function (a, b) { return Number(b.timeStamp) - Number(a.timeStamp) })
      const latest = all[0]
      const titles = []
      const walk = function (o, d) {
        if (!o || typeof o !== 'object' || d > 5) return
        Object.keys(o).forEach(function (k) {
          const v = o[k]
          if (k.toLowerCase().indexOf('title') >= 0 && typeof v === 'string' && v.trim()) titles.push(v.trim())
          else if (v && typeof v === 'object') walk(v, d + 1)
        })
      }
      walk(latest.content, 0)
      return {
        ok: titles.indexOf(want) >= 0,
        count: all.length,
        latestTitle: titles[0] || '(无标题字段)',
        latestTime: new Date(Number(latest.timeStamp)).toLocaleString('zh-CN')
      }
    })()`)
    return st
  } catch (e) {
    return { ok: false, reason: String((e && e.message) || e).slice(0, 120) }
  }
}

// ---- 5. 视频封面（可选）----
async function setVideoCover(coverPath) {
  // 读取封面缩略图当前的 background-image，作为最终「是否真的换掉」的校验基准
  const readCoverUrl = () =>
    js(`(() => {
      const c = document.querySelector('${SEL.coverBox}')
      if (!c) return ''
      const el = [...c.querySelectorAll('*')].find((e) => (e.style.backgroundImage || '').includes('url'))
      return el ? el.style.backgroundImage : ''
    })()`)

  const beforeUrl = await readCoverUrl()
  log('cover url before: ' + (beforeUrl ? String(beforeUrl).slice(0, 70) : '(empty)'))

  // PK 封面引导气泡会遮挡封面区，先隐藏（纯视觉层，不影响提交数据）
  await js(`(() => {
    document.querySelectorAll('${SEL.coverGuide}').forEach((e) => { e.style.display = 'none' })
    return true
  })()`)

  const rect = await js(`(() => {
    const c = document.querySelector('${SEL.coverBox}')
    if (!c) return null
    const r = c.getBoundingClientRect()
    if (r.width < 50) return null
    return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }
  })()`)
  if (!rect) {
    return { ok: false, code: 'E_COVER_AREA_MISSING', detail: {} }
  }
  log('cover area: ' + JSON.stringify(rect))

  // 「编辑封面」平时 boundingRect 为 0×0，只有真实 hover 才渲染，必须用 CDP 派发鼠标移动
  await cdp('Input.dispatchMouseEvent', {
    type: 'mouseMoved',
    x: rect.x + 65,
    y: rect.y + Math.round(rect.h / 2),
    button: 'none',
  })

  const shown = await waitFor('cover-entry', async () => {
    const r2 = await js(`(() => {
      const el = document.querySelector('${SEL.coverEditEntry}')
      if (!el) return { done: false }
      const b = el.getBoundingClientRect()
      return { done: b.width > 0 && b.height > 0, w: Math.round(b.width), h: Math.round(b.height) }
    })()`)
    return r2
  }, T.coverHover)

  if (!shown.ok) {
    return { ok: false, code: 'E_COVER_ENTRY_HIDDEN', detail: shown.state || {} }
  }

  await click(SEL.coverEditEntry, { label: 'open cover editor', timeout: 8000 })

  const editorOk = await waitFor('cover-editor', async () => {
    const ok = await js(`!!document.querySelector('${SEL.coverInput}')`)
    return { done: !!ok }
  }, T.coverEditor)

  if (!editorOk.ok) {
    return { ok: false, code: 'E_COVER_EDITOR_NOT_OPEN', detail: {} }
  }

  await uploadFile(SEL.coverInput, coverPath)

  // 注意：小红书上传组件接收文件后会立刻清空 input.files，
  // 所以不要用 files.length > 0 判断上传是否成功（永远读到 0）。
  // 图片解码 → 渲染进裁剪画布这段没有可靠 DOM 信号，给足固定时间；
  // 真正的成败由最后「封面缩略图 URL 是否变化」判定。
  await wait(5)

  // 「完成」按钮在视口外右侧，必须先 scrollIntoView 再点
  const doneClicked = await js(`(() => {
    const el = [...document.querySelectorAll('${SEL.coverDoneBtn}')].find((e) => e.textContent.trim() === '完成')
    if (!el) return false
    el.scrollIntoView({ block: 'center', inline: 'center' })
    el.click()
    return true
  })()`)
  if (!doneClicked) {
    return { ok: false, code: 'E_COVER_DONE_BTN_MISSING', detail: {} }
  }

  const closed = await waitFor('cover-modal-closed', async () => {
    const ok = await js(`(() => {
      const m = document.querySelector('${SEL.coverModal}')
      return !m || m.offsetParent === null
    })()`)
    return { done: !!ok }
  }, 8000, 500)

  if (!closed.ok) {
    return { ok: false, code: 'E_COVER_MODAL_STUCK', detail: {} }
  }

  // 最终校验：封面缩略图的 CDN URL 必须变化。
  // 只校验「弹窗关了」是不够的——图片没渲染完就点完成时，弹窗照样关，但封面还是旧的。
  const changed = await waitFor('cover-url-changed', async () => {
    const u = await readCoverUrl()
    return { done: !!u && u !== beforeUrl, url: u }
  }, 12000, 1000)

  if (!changed.ok) {
    return {
      ok: false,
      code: 'E_COVER_NOT_APPLIED',
      detail: {
        before: String(beforeUrl).slice(0, 70),
        after: String((changed.state && changed.state.url) || '').slice(0, 70),
      },
    }
  }
  log('cover url after: ' + String(changed.state.url).slice(0, 70))
  return { ok: true }
}

if (isVideo && coverImage) {
  await step('set-cover', async () => {
    log('custom cover: ' + coverImage)
    const r = await setVideoCover(coverImage)
    if (!r.ok) {
      const hints = {
        E_COVER_AREA_MISSING: [
          '页面没有找到封面区域，可能视频还没完全渲染完',
          '重跑脚本；若反复失败，先不传 COVER_IMAGE 用默认第一帧',
        ],
        E_COVER_ENTRY_HIDDEN: [
          '「编辑封面」按钮没有因 hover 出现，页面结构可能改版',
          '先不传 COVER_IMAGE 用默认第一帧发布，再在网页上手动换封面',
          '把这段输出发给 agent，需要更新 SEL.coverEditEntry 选择器',
        ],
        E_COVER_EDITOR_NOT_OPEN: [
          '封面编辑器没打开，可能被引导气泡或弹窗挡住',
          '页面已保留，可手动点「编辑封面」看是否有异常',
          '先不传 COVER_IMAGE 重跑，发出后手动改封面',
        ],
        E_COVER_FILE_NOT_PICKED: [
          '封面图没有被写入 file input，可能图片格式不被接受',
          '确认是 png/jpg/webp，且文件可正常打开',
          '换一张图重试，或先不传 COVER_IMAGE',
        ],
        E_COVER_NOT_APPLIED: [
          '走完了流程但封面缩略图 URL 没变，说明图片没真正替换（常见于图片未渲染完就点了完成）',
          '重跑一次通常就能成功；若连续失败，先不传 COVER_IMAGE 用默认第一帧，发出后手动换封面',
          '页面已保留，可接管后手动在编辑器里确认图片已加载再点完成',
        ],
        E_COVER_DONE_BTN_MISSING: [
          '找不到「完成」按钮，选择器可能变了',
          '页面已保留，可手动点完成',
          '把输出发给 agent 更新 SEL.coverDoneBtn',
        ],
        E_COVER_MODAL_STUCK: [
          '点了完成但弹窗没关，可能图片还在上传',
          '等 10 秒后接管页面手动点完成',
        ],
      }
      await fail('set-cover', r.code, EXIT.COVER, '自定义封面设置失败', r.detail, hints[r.code] || ['先不传 COVER_IMAGE 重跑'])
    }
    log('cover applied')
  })
}

// ---- 6. 标题 ----
await step('fill-title', async () => {
  const exists = await js(`!!document.querySelector('${SEL.titleInput}')`)
  if (!exists) {
    await fail('fill-title', 'E_TITLE_INPUT_MISSING', EXIT.FORM, '找不到标题输入框', {}, [
      '页面可能还没切换到编辑态，重跑脚本',
      '若反复失败，说明标题框 placeholder 变了，需要更新 SEL.titleInput',
    ])
  }
  await fillInput('css:' + SEL.titleInput, title, { label: 'fill title' })
  const got = await js(`document.querySelector('${SEL.titleInput}').value`)
  if (got !== title) {
    await fail('fill-title', 'E_TITLE_NOT_APPLIED', EXIT.FORM, '标题写入后读回不一致', { expect: title, got: got }, [
      '标题可能含特殊字符被过滤，检查是否含单引号',
      '重跑脚本',
    ])
  }
  log('title ok: ' + got)
})

// ---- 7. 正文 + 话题 ----
let editorSel = ''

await step('fill-body', async () => {
  editorSel = await js(`(() => {
    if (document.querySelector('${SEL.editor}')) return '${SEL.editor}'
    if (document.querySelector('${SEL.editorFallback}')) return '${SEL.editorFallback}'
    return ''
  })()`)
  if (!editorSel) {
    await fail('fill-body', 'E_EDITOR_MISSING', EXIT.FORM, '找不到正文编辑器', {}, [
      '确认页面已经进入编辑态（能看到标题框和正文区）',
      '编辑器容器可能从 div.tiptap 换成别的结构，需要更新 SEL.editor',
    ])
  }
  log('editor: ' + editorSel)
  // 用 focus 而不是 click：发布按钮浮层会拦截指针事件
  await js(`document.querySelector('${editorSel}')?.focus()`)
  await wait(0.5)
  await typeText(bodyText, { label: 'type body text' })
  await wait(1)

  const len = await js(`(document.querySelector('${editorSel}').innerText || '').length`)
  if (len < Math.min(10, bodyText.length / 2)) {
    await fail('fill-body', 'E_BODY_NOT_APPLIED', EXIT.FORM, '正文写入后长度异常', { expect: bodyText.length, got: len }, [
      '编辑器可能未获得焦点，重跑脚本',
      '若正文含反引号或 ${，bash 侧已拦截，检查是否有其它特殊字符',
    ])
  }
  log('body length: ' + len)
})

async function moveCaretToEnd() {
  await js(`(() => {
    const el = document.querySelector('${editorSel}')
    if (!el) return false
    el.focus()
    const r = document.createRange()
    r.selectNodeContents(el)
    r.collapse(false)
    const s = window.getSelection()
    s.removeAllRanges()
    s.addRange(r)
    return true
  })()`)
  await wait(0.3)
}

async function tryAddTopic(topic) {
  await moveCaretToEnd()
  await typeText('#' + topic, { label: 'type topic #' + topic })

  const found = await waitFor('topic-' + topic, async () => {
    const st = await js(`(() => {
      const c = document.getElementById('creator-editor-topic-container')
      if (!c) return { done: false, reason: 'no_container' }
      const items = [...c.querySelectorAll('.item')]
      if (!items.length) return { done: false, reason: 'no_item' }
      return { done: true, count: items.length }
    })()`)
    return st
  }, T.topicDropdown)

  if (!found.ok) {
    return { ok: false, reason: (found.state && found.state.reason) || 'timeout' }
  }

  const clicked = await js(`((topic) => {
    const c = document.getElementById('creator-editor-topic-container')
    if (!c) return 'NO_CONTAINER'
    const items = [...c.querySelectorAll('.item')]
    if (!items.length) return 'NO_ITEM'
    const exact = items.find((el) => {
      const n = el.querySelector('.name')
      return n && n.innerText.trim().split('\\n')[0] === '#' + topic
    })
    const target = exact || items[0]
    const nameEl = target.querySelector('.name')
    ;(nameEl || target).click()
    return (exact ? 'EXACT:' : 'FALLBACK:') + (target.innerText || '').split('\\n')[0]
  })('${topic.replace(/'/g, "\\'")}')`)

  await wait(1.2)
  const popupStillOpen = await js(`!!document.getElementById('tippy-1')?.offsetParent`)
  if (popupStillOpen) {
    await pressKey('Escape')
    await wait(0.4)
  }
  await typeText(' ', { label: 'space after topic' })
  await wait(0.4)
  return { ok: String(clicked).startsWith('EXACT') || String(clicked).startsWith('FALLBACK'), clicked: clicked }
}

if (topics.length > 0) {
  await step('add-topics', async () => {
    await moveCaretToEnd()
    await typeText('\n\n', { label: 'newline before topics' })
    await wait(0.5)

    const failed = []
    for (const topic of topics) {
      let r = await tryAddTopic(topic)
      if (!r.ok) {
        // 下拉没出来时重试一次（常见于刚打完字或网络慢）
        log('topic retry: #' + topic + ' (' + r.reason + ')')
        await pressKey('Escape')
        await wait(0.8)
        r = await tryAddTopic(topic)
      }
      if (!r.ok) {
        failed.push({ topic: topic, reason: r.reason })
      } else {
        log('topic ok: ' + r.clicked)
      }
    }

    if (failed.length > 0) {
      await fail('add-topics', 'E_TOPIC_NOT_ATTACHED', EXIT.TOPIC,
        failed.length + '/' + topics.length + ' 个话题未挂载成功',
        { failed: failed },
        [
          '话题没挂上不影响发布，只是少了流量入口，可以继续发',
          '页面已保留，接管后手动补打 #话题 并从下拉选中',
          '若想重跑，注意重跑会重新上传素材',
        ])
    }
  })
}

await pressKey('Escape')
await wait(0.4)

// ---- 8. 收尾 ----
if (MODE === 'stage') {
  await step('stage-hold', async () => {
    log('STAGE MODE：内容已准备好，页面保持不动，等待人工检查后点发布')
    log('  type   : ' + params.mediaType)
    log('  files  : ' + filePaths.length)
    log('  title  : ' + title)
    log('  body   : ' + bodyText.length + ' 字')
    log('  topics : ' + (topics.length ? topics.join(', ') : '无'))
    log('  cover  : ' + (isVideo ? (coverImage || '默认第一帧') : 'N/A'))
    const shot = await captureScreenshot()
    log('  shot   : ' + shot)
    log('SUCCESS: stage 完成，task space ' + TASK.id + ' 保持开启')
    // stage 模式保留页面，不关闭 space
  })
  log('')
  log('=== OK ===')
  log('step     : stage-hold')
  log('exit     : 0')
  log('space    : ' + TASK.id + '（页面已保留，供人工检查后手动发布）')
  log('takeover : ego-browser nodejs -e "await claimTaskSpace(' + TASK.id + ')"')
  log('cleanup  : ego-browser nodejs -e "await completeTaskSpace(' + TASK.id + ', { keep: false })"')
  log('=== END OK ===')
} else {
  await step('submit', async () => {
    const action = MODE === 'draft' ? '_onSave' : '_onPublish'
    log('triggering ' + action + '()')
    const r = await js(`((mode) => {
      const host = document.querySelector('${SEL.publishHost}')
      if (!host) return { error: 'E_NO_PUBLISH_HOST' }
      if (mode === 'draft') {
        if (typeof host._onSave !== 'function') return { error: 'E_NO_ONSAVE' }
        const d = host.getAttribute('save-disabled')
        if (d === 'true') return { error: 'E_SAVE_DISABLED', saveDisabled: d }
        host._onSave()
        return { triggered: true, action: 'draft' }
      }
      if (typeof host._onPublish !== 'function') return { error: 'E_NO_ONPUBLISH' }
      const d = host.getAttribute('submit-disabled')
      if (d === 'true') return { error: 'E_SUBMIT_DISABLED', submitDisabled: d, submitLoading: host.getAttribute('submit-loading') }
      host._onPublish()
      return { triggered: true, action: 'publish' }
    })('${MODE}')`)

    if (r.error) {
      await fail('submit', r.error, EXIT.SUBMIT, '提交按钮不可用', r, [
        '按钮 disabled 通常是必填项没填完（标题/正文/封面）',
        '页面已保留，接管后看哪个字段标红',
        '修好后可以直接在该页面手动点发布',
      ])
    }

    if (MODE === 'draft') {
      await wait(6)
      const cnt = await js(`(() => {
        const m = document.body.innerText.match(/草稿箱\\((\\d+)\\)/)
        return m ? m[1] : 'n/a'
      })()`)
      log('draft count after save: ' + cnt)
      if (cnt === 'n/a') {
        await fail('submit', 'E_DRAFT_COUNT_UNREADABLE', EXIT.VERIFY, '存草稿后读不到草稿箱计数', {}, [
          '页面可能已跳转，接管后到草稿箱确认是否已保存',
          '草稿存于当前浏览器本地，换浏览器就看不到',
        ])
      }

      // 计数 +1 只能证明「多了条草稿」，不能证明「内容对」。
      // 再从 IndexedDB 读最新草稿的标题做端到端核对；读不到只告警、不判失败，
      // 避免本地库结构变化把成功误判成失败。
      const verified = await verifyDraftEntry(title)
      if (verified.ok) {
        log('draft verified: 标题「' + verified.latestTitle + '」，保存于 ' + verified.latestTime + '（库内共 ' + verified.count + ' 条）')
      } else {
        log('WARN: 未能核对草稿内容（' + (verified.reason || ('最新草稿标题是「' + verified.latestTitle + '」')) + '）')
        log('      草稿计数已增长，请在创作平台右上角「草稿箱」手动确认内容')
      }
    } else {
      const r2 = await waitFor('publish-done', async () => {
        const info = await pageInfo()
        const done = info.url.includes('published=true') || info.url.includes('note-manage')
        return { done: done, url: info.url }
      }, T.publishResult, 1500)

      if (!r2.ok) {
        await fail('submit', 'E_PUBLISH_UNCONFIRMED', EXIT.VERIFY, '发布后未检测到跳转，状态不确定',
          r2.state || {},
          [
            '不要立刻重发，先去创作平台「笔记管理」确认这条是否已发出',
            '重复发布会产生重复笔记，确认没发出后再重跑',
            '页面已保留，接管后可看到当前状态',
          ])
      }
      log('published: ' + r2.state.url)
    }
  })

  const shot = await captureScreenshot()
  log('final screenshot: ' + shot)
  try {
    await completeTaskSpace(TASK.id, { keep: false })
    log('space ' + TASK.id + ' closed')
  } catch (e) {
    log('space close failed (ignored): ' + e.message)
  }
  log('')
  log('=== OK ===')
  log('step     : submit')
  log('exit     : 0')
  log('mode     : ' + MODE)
  log('=== END OK ===')
}
