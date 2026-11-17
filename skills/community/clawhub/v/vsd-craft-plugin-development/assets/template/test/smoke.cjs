'use strict';

// Contract tests for this scaffold, not a vendor SDK compatibility certificate.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {spawn} = require('node:child_process');
const {once} = require('node:events');
const WebSocket = require('ws');
const {launchOptions} = require('../plugin.js');
const root = path.resolve(__dirname, '..');
const manifest = require('../manifest.json');
const keyAction = manifest.Actions.find((action) => action.Controllers.includes('Keypad')).UUID;
const dialAction = manifest.Actions.find((action) => action.Controllers.includes('Knob')).UUID;

async function host(t) {
  const server = new WebSocket.WebSocketServer({host: '127.0.0.1', port: 0});
  const records = [];
  const listeners = new Set();
  let plugin;
  let child;
  let exited;
  let stderr = '';
  function waitFor(predicate, after = 0) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        listeners.delete(check);
        reject(new Error(`Host response timed out. Plugin stderr: ${stderr}`));
      }, 3000);
      function check() {
        const record = records.slice(after).find(predicate);
        if (record) {
          clearTimeout(timer);
          listeners.delete(check);
          resolve(record);
        }
      }
      listeners.add(check);
      check();
    });
  }
  t.after(async () => {
    for (const socket of server.clients) socket.terminate();
    if (child && child.exitCode === null && child.signalCode === null) child.kill();
    if (exited) await exited;
    await new Promise((resolve) => server.close(resolve));
  });
  server.on('connection', (socket) => {
    socket.on('error', () => {});
    socket.on('message', (data) => {
      const message = JSON.parse(data.toString());
      if (message.event === 'registerPlugin') { socket.role = 'plugin'; plugin = socket; }
      if (message.event === 'registerPropertyInspector') socket.role = 'inspector';
      records.push({role: socket.role, message});
      // A small host broker: PI registration UUID != action instance context.
      if (socket.role === 'inspector' && message.event === 'sendToPlugin') {
        socket.actionContext = message.payload.actionContext;
        plugin.send(JSON.stringify(message));
      }
      if (socket.role === 'plugin' && message.event === 'sendToPropertyInspector') {
        for (const peer of server.clients) {
          if (peer.role === 'inspector' && peer.actionContext === message.context) {
            peer.send(JSON.stringify(message));
          }
        }
      }
      for (const check of [...listeners]) check();
    });
  });
  await once(server, 'listening');
  const port = server.address().port;
  child = spawn(process.execPath, [path.join(root, 'plugin.js'),
    '-info', '{}', '-registerEvent', 'registerPlugin',
    '-pluginUUID', 'plugin-session', '-port', String(port)],
  {cwd: root, stdio: ['ignore', 'ignore', 'pipe']});
  child.stderr.on('data', (data) => { stderr += data; });
  exited = once(child, 'exit');
  // Attach a rejection handler now, while waitFor is still awaiting registration.
  exited.catch(() => {});
  const registration = await waitFor((r) => r.message.event === 'registerPlugin');
  assert.deepEqual(registration.message, {event: 'registerPlugin', uuid: 'plugin-session'});
  const send = (message) => plugin.send(typeof message === 'string' ? message : JSON.stringify(message));
  const reply = (context, after = 0) => waitFor((r) =>
    r.role === 'plugin' && r.message.event === 'sendToPropertyInspector' && r.message.context === context, after);
  return {port, records, waitFor, reply, send, exited,
    close: () => plugin.close(), stderr: () => stderr};
}

function appear(context, action, device = 'device-a', settings = {step: 1}) {
  return {event: 'willAppear', action, context, device, payload: {settings}};
}
function input(event, context, payload = {}) { return {event, context, payload}; }
function imageValue(record) {
  const image = record.message.payload.image;
  assert.ok(image.startsWith('data:image/svg+xml;base64,'));
  const svg = Buffer.from(image.split(',')[1], 'base64').toString();
  return Number(svg.match(/>(-?\d+)<\/text>/)[1]);
}

test('manifest references real PNGs, entries and PI files', () => {
  assert.equal(manifest.SDKVersion, 1);
  assert.equal(manifest.Nodejs.Version, '20');
  assert.equal(path.basename(root), `${manifest.UUID}.sdPlugin`);
  const references = [manifest.Icon, manifest.CategoryIcon, manifest.CodePath, manifest.CodePathWin];
  for (const action of manifest.Actions) {
    assert.ok(action.UUID.startsWith(`${manifest.UUID}.`));
    references.push(action.Icon, action.PropertyInspectorPath, ...action.States.map((state) => state.Image));
  }
  for (const relative of references) {
    assert.ok(!path.isAbsolute(relative) && !relative.split(/[\\/]/).includes('..'));
    const contents = fs.readFileSync(path.join(root, relative));
    if (relative.endsWith('.png')) assert.equal(contents.subarray(0, 8).toString('hex'), '89504e470d0a1a0a');
  }
});

test('launch arguments are named, validated and preserve the host registration event', () => {
  assert.deepEqual(launchOptions(['-info', '{}', '--port', '32123', '-registerEvent', 'vendorRegister',
    '-pluginUUID', 'session-id']), {port: 32123, uuid: 'session-id', registerEvent: 'vendorRegister'});
  for (const args of [[], ['-port'], ['port', '2'], ['-port', '65536', '-pluginUUID', 'x', '-registerEvent', 'r'],
    ['-port', '22', '-pluginUUID', 'x', '-registerEvent', 'r', '-info', 'not-json']]) {
    assert.throws(() => launchOptions(args));
  }
});

test('PI reopening ignores late events from the old connection', () => {
  const sockets = [];
  class Socket {
    static OPEN = 1;
    constructor() { this.readyState = 1; this.sent = []; sockets.push(this); }
    send(value) { this.sent.push(JSON.parse(value)); }
    close() { this.readyState = 3; }
  }
  const controls = Object.fromEntries(['status', 'step', 'save'].map((id) => [id,
    {value: '1', disabled: true, addEventListener() {}}]));
  const sandbox = {window: {}, document: {getElementById: (id) => controls[id]}, WebSocket: Socket};
  vm.runInNewContext(fs.readFileSync(path.join(root, 'ui/inspector.js'), 'utf8'), sandbox);
  const connect = (id, info = JSON.stringify({action: keyAction, context: 'target'})) =>
    sandbox.window.connectSocket(32123, id, 'registerPropertyInspector', '{}', info);
  connect('old');
  connect('new');
  sockets[1].onopen();
  sockets[0].onopen();
  sockets[0].onclose();
  assert.equal(controls.save.disabled, false);
  assert.deepEqual(sockets[1].sent.map((message) => message.event), ['registerPropertyInspector', 'sendToPlugin']);
  assert.equal(sockets[1].sent[0].uuid, 'new');
  assert.equal(sockets[0].sent.length, 0);
  connect('invalid', 'null');
  assert.equal(controls.save.disabled, true);
});

test('real child: key/dial input, independent contexts and malformed messages', {timeout: 12000}, async (t) => {
  const h = await host(t);
  h.send(appear('key-a', keyAction, 'device-a', {step: 2}));
  h.send(appear('key-b', keyAction));
  h.send(appear('dial-a', dialAction));
  await h.reply('dial-a');
  h.send(input('keyUp', 'key-a')); // Unpaired release must do nothing.
  h.send('not-json');
  h.send('null');
  h.send(input('keyDown', 'key-a'));
  h.send(input('keyUp', 'key-a'));
  const first = await h.waitFor((r) => r.message.context === 'key-a' && r.message.payload?.value === 2);
  assert.equal(first.message.payload.step, 2);
  h.send(input('dialRotate', 'dial-a', {ticks: -3, pressed: true}));
  await h.waitFor((r) => r.message.context === 'dial-a' && r.message.payload?.value === -3);
  h.send(input('dialRotate', 'dial-a', {ticks: 5}));
  await h.waitFor((r) => r.message.context === 'dial-a' && r.message.payload?.value === 2);
  const after = h.records.length;
  h.send(input('dialDown', 'dial-a'));
  h.send(input('dialUp', 'dial-a'));
  await h.reply('dial-a', after);
  assert.equal(h.records.filter((r) => r.message.context === 'dial-a' && r.message.event === 'setImage').map(imageValue).at(-1), 0);
  h.send({event: 'sendToPlugin', context: 'pi-query', payload: {op: 'get', actionContext: 'key-b'}});
  assert.equal((await h.reply('key-b', after)).message.payload.value, 0);
  assert.ok(h.records.every((r) => r.message.event !== 'setTitle'), 'manual titles remain untouched');
  h.close();
  const [code, signal] = await h.exited;
  assert.equal(code, 0);
  assert.equal(signal, null);
  assert.match(h.stderr(), /Ignored invalid/);
});

test('real child: USB reconnect redraws retained contexts, discards held input and respects disappearance',
  {timeout: 12000}, async (t) => {
    const h = await host(t);
    h.send(appear('retained', keyAction));
    h.send(appear('gone', keyAction));
    h.send(appear('other-device', keyAction, 'device-b'));
    await h.reply('other-device');
    const after = h.records.length;
    h.send(input('keyDown', 'retained'));
    h.send({event: 'deviceDidDisconnect', device: 'device-a'});
    h.send(input('keyUp', 'retained'));
    h.send(input('keyDown', 'retained')); // Offline input cannot start a new hold.
    h.send({event: 'willDisappear', context: 'gone'});
    h.send(input('keyDown', 'gone'));
    h.send(input('keyUp', 'gone'));
    h.send({event: 'sendToPlugin', context: 'retained', payload: {op: 'get'}});
    assert.equal((await h.reply('retained', after)).message.payload.value, 0);
    assert.equal(h.records.slice(after).filter((r) => r.message.event === 'setImage').length, 0);
    const reconnect = h.records.length;
    h.send({event: 'deviceDidConnect', device: 'device-a'}); // No second willAppear.
    await h.reply('retained', reconnect);
    const images = h.records.slice(reconnect).filter((r) => r.message.event === 'setImage');
    assert.deepEqual(images.map((r) => [r.message.context, imageValue(r)]), [['retained', 0]]);
    const release = h.records.length;
    h.send(input('keyUp', 'retained'));
    h.send({event: 'sendToPlugin', context: 'retained', payload: {op: 'get'}});
    assert.equal((await h.reply('retained', release)).message.payload.value, 0);
    h.send(input('keyDown', 'retained'));
    h.send(input('keyUp', 'retained'));
    await h.waitFor((r) => r.message.context === 'retained' && r.message.payload?.value === 1, release);
  });

test('PI script: actual socket roundtrip separates PI UUID, preserves settings and handles invalid input',
  {timeout: 12000}, async (t) => {
    const h = await host(t);
    h.send(appear('pi-target', keyAction, 'device-a', {step: 2, retained: 'user-setting'}));
    await h.reply('pi-target');
    const uiRecords = [];
    const uiListeners = new Set();
    const controls = Object.fromEntries(['status', 'step', 'save'].map((id) => [id,
      {value: '1', disabled: true, textContent: '', addEventListener(event, handler) { this[event] = handler; }}]));
    // Only the DOM is mocked. The PI and plugin communicate through real ws sockets.
    class InspectorSocket extends WebSocket {
      constructor(url) {
        super(url);
        this.on('message', (data) => {
          uiRecords.push(JSON.parse(data.toString()));
          queueMicrotask(() => { for (const check of [...uiListeners]) check(); });
        });
      }
    }
    const sandbox = {window: {}, document: {getElementById: (id) => controls[id]}, WebSocket: InspectorSocket};
    vm.runInNewContext(fs.readFileSync(path.join(root, 'ui/inspector.js'), 'utf8'), sandbox);
    assert.equal(sandbox.window.connectSocket, sandbox.window.connectElgatoStreamDeckSocket);
    sandbox.window.connectSocket(h.port, 'pi-session-not-action-context', 'registerPropertyInspector', '{}',
      JSON.stringify({action: keyAction, context: 'pi-target', payload: {settings: {step: 2}}}));
    await h.waitFor((r) => r.role === 'inspector' && r.message.event === 'sendToPlugin');
    // Use the PI's received response to synchronize the UI, rather than sleeping.
    async function uiResponse(value) {
      await new Promise((resolve, reject) => {
        const deadline = setTimeout(() => {
          uiListeners.delete(check);
          reject(new Error('PI response timed out'));
        }, 3000);
        const check = () => {
          if (uiRecords.some((r) => r.payload?.step === value) && controls.step.value === String(value)) {
            clearTimeout(deadline);
            uiListeners.delete(check);
            resolve();
          }
        };
        uiListeners.add(check);
        check();
      });
    }
    await uiResponse(2);
    assert.equal(controls.save.disabled, false);
    controls.step.value = '7';
    controls.save.click();
    const saved = await h.waitFor((r) => r.message.event === 'setSettings');
    assert.deepEqual(saved.message, {event: 'setSettings', context: 'pi-target', payload: {step: 7, retained: 'user-setting'}});
    await uiResponse(7);
    const request = h.records.find((r) => r.role === 'inspector' && r.message.payload?.op === 'setStep').message;
    assert.equal(request.context, 'pi-session-not-action-context');
    assert.equal(request.action, keyAction);
    assert.equal(request.payload.actionContext, 'pi-target');
    const count = h.records.length;
    controls.step.value = '1.5';
    controls.save.click();
    assert.match(controls.status.textContent, /integer/);
    // A following valid request is the ordering barrier for the rejected input.
    controls.step.value = '8';
    controls.save.click();
    await uiResponse(8);
    const saves = h.records.slice(count).filter((r) => r.message.event === 'setSettings');
    assert.deepEqual(saves.map((r) => r.message.payload.step), [8]);
    const update = h.records.length;
    h.send({event: 'didReceiveSettings', context: 'pi-target', payload: {settings: {step: 3, retained: 'host-update'}}});
    await h.reply('pi-target', update);
    await uiResponse(3);
    h.send(input('keyDown', 'pi-target'));
    h.send(input('keyUp', 'pi-target'));
    await h.waitFor((r) => r.message.context === 'pi-target' && r.message.payload?.value === 3, update);
  });
