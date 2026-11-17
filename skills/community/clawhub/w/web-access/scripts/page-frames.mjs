// 页面中的 iframe：列举、在其中执行、把视口坐标点击路由到所在的 frame - 单一职责模块
// 被 cdp-proxy.mjs 使用。不持有连接和 session 表，只经注入的 send / ensureSession 访问浏览器（唯一连接所有者仍是 cdp-connection）。
//
// 依据的 CDP 事实（Chrome 155 实测）：
//   - DOM.describeNode 对 iframe 元素给出 frameId；跨进程 iframe 的 frameId 同时是它的 iframe target id
//   - 父页面的 Page.getFrameTree 不包含跨进程 iframe，它的网址取自 Target.getTargets
//   - 后台标签页里，经父页面 session 发出的鼠标事件命中不了跨进程 iframe；需换算坐标后发给该 iframe 的子 session
//   - Page.createIsolatedWorld 用同一个名字重复调用返回同一个执行上下文，不会累积
//   - 隔离环境有自己的一套 DOM 原型：页面改写 Document.prototype.querySelectorAll / elementFromPoint 不影响它
// 列举与命中测试都在隔离环境里执行，不受页面脚本改写 DOM API 的影响。
//   - DOM.getBoxModel 的内容框是当前 session 根视口坐标，已含边框、内边距、transform、zoom 与滚动；同进程子 frame 里的元素也相对根视口
// 范围：列举只覆盖页面主文档里直接的 <iframe> / <frame>（不含嵌套与 shadow root 内的）；点击按坐标逐层进入，最多 MAX_NESTING 层。

import { randomUUID } from 'node:crypto';

// 调用方参数问题（frameId 格式不对、该页面没有这个 iframe），由调用方映射为 400
export class FrameError extends Error {}

const FRAME_ID = /^[A-Za-z0-9._-]{1,128}$/;
const WORLD_NAME = 'web-access';
const MAX_NESTING = 5; // 点击最多逐层进入 5 层 iframe

export function createPageFrames({ send, ensureSession }) {
  // CDP 错误一律抛出，带上方法名
  async function call(method, params, sessionId) {
    const resp = await send(method, params, sessionId);
    if (resp.error) throw new Error(`${method}: ${resp.error.message}`);
    return resp.result;
  }

  // 用对象组承载临时远程对象，结束后整组释放。组名每次调用唯一：
  // 同一标签页上重叠的请求共用 session，固定组名会让先结束的请求释放另一个请求还在用的对象。
  async function withObjectGroup(sessionId, prefix, fn) {
    const group = `${prefix}-${randomUUID()}`;
    try { return await fn(group); }
    finally { await send('Runtime.releaseObjectGroup', { objectGroup: group }, sessionId).catch(() => {}); }
  }

  // frame 的隔离环境（同名复用同一个上下文）
  async function isolatedWorld(sessionId, frameId) {
    const world = await call('Page.createIsolatedWorld', { frameId, worldName: WORLD_NAME }, sessionId);
    if (!world.executionContextId) throw new Error('iframe 执行环境不可用');
    return world.executionContextId;
  }

  // session 根 frame 的 id 与 frame 树
  async function frameTree(sessionId) {
    return (await call('Page.getFrameTree', {}, sessionId)).frameTree;
  }

  async function iframeTargets() {
    const { targetInfos } = await call('Target.getTargets');
    return new Map(targetInfos.filter(info => info.type === 'iframe').map(info => [info.targetId, info]));
  }

  // 列出页面主文档中的 iframe：[{ index, frameId, crossProcess, url, id?, name?, src? }]
  // frameId 为 null 表示该 iframe 尚未加载出文档
  async function listFrames(targetId) {
    const sessionId = await ensureSession(targetId);
    const tree = await frameTree(sessionId);
    const contextId = await isolatedWorld(sessionId, tree.frame.id);
    return withObjectGroup(sessionId, 'web-access-frames', async group => {
      const list = await call('Runtime.evaluate', {
        expression: "document.querySelectorAll('iframe, frame')", objectGroup: group, contextId,
      }, sessionId);
      if (list.exceptionDetails || !list.result?.objectId) throw new Error('无法读取页面中的 iframe');
      const { result: props } = await call('Runtime.getProperties', {
        objectId: list.result.objectId, ownProperties: true,
      }, sessionId);
      const elements = props.filter(prop => /^\d+$/.test(prop.name))
        .sort((a, b) => Number(a.name) - Number(b.name))
        .map(prop => prop.value.objectId);
      if (!elements.length) return [];

      const oopifs = await iframeTargets();
      const local = new Map();
      const walk = node => { for (const child of node?.childFrames || []) { local.set(child.frame.id, child.frame); walk(child); } };
      walk(tree);

      const frames = [];
      for (const [index, objectId] of elements.entries()) {
        const { node } = await call('DOM.describeNode', { objectId }, sessionId);
        const attrs = {};
        for (let i = 0; i + 1 < (node.attributes || []).length; i += 2) attrs[node.attributes[i]] = node.attributes[i + 1];
        const frameId = node.frameId || null;
        const oopif = frameId ? oopifs.get(frameId) : undefined;
        frames.push({
          index,
          frameId,
          crossProcess: Boolean(oopif),
          url: oopif?.url ?? local.get(frameId)?.url ?? attrs.src ?? null,
          ...(attrs.id ? { id: attrs.id } : {}),
          ...(attrs.name ? { name: attrs.name } : {}),
          ...(attrs.src ? { src: attrs.src } : {}),
        });
      }
      return frames;
    });
  }

  // 为 /eval 准备 iframe 的执行环境：{ sessionId, contextId, frame }
  // 在 iframe 的隔离环境中执行：DOM 与页面共享，看不到页面自己的 JS 全局变量
  async function frameContext(targetId, frameId) {
    if (!FRAME_ID.test(frameId || '')) throw new FrameError('frame 参数应为 /frames 返回的 frameId');
    const frame = (await listFrames(targetId)).find(item => item.frameId === frameId);
    if (!frame) throw new FrameError(`该页面没有 frameId 为 ${frameId} 的 iframe，请先用 /frames 查看`);
    // 跨进程 iframe 只能在它自己的子 session 里执行；同进程 iframe 用页面 session 加 frameId
    const sessionId = frame.crossProcess ? await ensureSession(frameId) : await ensureSession(targetId);
    const world = await call('Page.createIsolatedWorld', { frameId, worldName: WORLD_NAME }, sessionId);
    if (!world.executionContextId) throw new Error('iframe 执行环境不可用');
    return { sessionId, contextId: world.executionContextId, frame };
  }

  // 视口坐标 → 实际接收鼠标事件的 session 与坐标：{ sessionId, x, y, frameId?, crossProcess?, depth? }
  // 逐层命中测试：命中 iframe 的内容区时进入该 frame 继续，直到命中普通元素或达到 MAX_NESTING 层。
  //   - 跨进程 iframe：换到它的子 session，坐标换算到 iframe 视口内（扣除边框与内边距，按缩放比例换算）
  //   - 同进程 iframe：鼠标事件仍发给当前 session（坐标不变），只把命中测试的坐标换算到该 frame 内
  //   - 落在 iframe 的边框或内边距上：点的是 iframe 元素本身，留在当前 frame
  // 坐标不在页面视口内时抛 FrameError（不发出鼠标事件）。
  async function routePoint(targetId, x, y) {
    const pageSession = await ensureSession(targetId);
    let frameId = (await frameTree(pageSession)).frame.id;
    let sessionId = pageSession;
    let contextId = await isolatedWorld(sessionId, frameId);
    let rootX = x;   // 当前 session 根视口坐标：鼠标事件用
    let rootY = y;
    let frameX = x;  // 当前 frame 视口坐标：命中测试用
    let frameY = y;
    let entered = null;
    let paint = false;
    let oopifs = null;
    const scopes = new Map(); // sessionId → 对象组名：每个 session 上的临时对象分别释放
    const groupFor = sid => {
      if (!scopes.has(sid)) scopes.set(sid, `web-access-click-${randomUUID()}`);
      return scopes.get(sid);
    };
    try {
      for (let depth = 0; depth <= MAX_NESTING; depth++) {
        const hit = await call('Runtime.evaluate', {
          expression: `document.elementFromPoint(${frameX}, ${frameY})`, objectGroup: groupFor(sessionId), contextId,
        }, sessionId);
        const objectId = hit.result?.objectId;
        if (!objectId) {
          if (depth === 0) throw new FrameError(`坐标 (${x}, ${y}) 不在页面视口内，没有发出点击`);
          break;
        }
        const { node } = await call('DOM.describeNode', { objectId }, sessionId);
        if (!node.frameId || depth === MAX_NESTING) break;
        // 内容框四角（当前 session 根视口坐标，已含 transform / zoom 与页面滚动）
        const { model } = await call('DOM.getBoxModel', { objectId }, sessionId);
        const [left, top, right, , , bottom] = model.content;
        if (rootX < left || rootX >= right || rootY < top || rootY >= bottom) break;
        oopifs ??= await iframeTargets();
        const crossProcess = oopifs.has(node.frameId);
        const childSession = crossProcess ? await ensureSession(node.frameId) : sessionId;
        const childContext = await isolatedWorld(childSession, node.frameId);
        const viewport = await call('Runtime.evaluate', {
          expression: '[innerWidth, innerHeight]', returnByValue: true, contextId: childContext,
        }, childSession);
        const [width, height] = viewport.result?.value || [];
        if (!(width > 0 && height > 0)) throw new Error('iframe 视口尺寸不可用');
        frameX = (rootX - left) / ((right - left) / width);
        frameY = (rootY - top) / ((bottom - top) / height);
        if (crossProcess) {
          sessionId = childSession;
          rootX = frameX;
          rootY = frameY;
          paint = false;
        } else {
          paint = true;
        }
        frameId = node.frameId;
        contextId = childContext;
        entered = { frameId, crossProcess, depth: depth + 1 };
      }
      if (paint) {
        // 后台标签页中同进程 iframe 可能还没有可用的命中测试数据：截一张最低质量的图触发绘制，不激活页面
        await call('Page.captureScreenshot', { format: 'jpeg', quality: 1, captureBeyondViewport: false }, sessionId);
      }
      return { sessionId, x: rootX, y: rootY, ...(entered || {}) };
    } finally {
      for (const [sid, group] of scopes) {
        await send('Runtime.releaseObjectGroup', { objectGroup: group }, sid).catch(() => {});
      }
    }
  }

  return { listFrames, frameContext, routePoint };
}
