#!/usr/bin/env node

// src/cli/standalone.ts
import { homedir } from "node:os";
import { basename, resolve, relative as relative3 } from "node:path";
import { copyFile, readFile as readFile4, writeFile as writeFile2, mkdir as mkdir3, rm, readdir as readdir3, stat, cp } from "node:fs/promises";

// src/core/packer.ts
import { createHash } from "node:crypto";
import { writeFile, readFile, mkdir } from "node:fs/promises";
import { join } from "node:path";

// ../../node_modules/.pnpm/tar@7.5.10/node_modules/tar/dist/esm/index.min.js
import Hr from "events";
import I from "fs";
import { EventEmitter as Oi } from "node:events";
import Ds from "node:stream";
import { StringDecoder as Ir } from "node:string_decoder";
import or from "node:path";
import Vt from "node:fs";
import { dirname as bn, parse as gn } from "path";
import { EventEmitter as wn } from "events";
import vi from "assert";
import { Buffer as _t } from "buffer";
import * as vs from "zlib";
import Yr from "zlib";
import { posix as Zt } from "node:path";
import { basename as dn } from "node:path";
import ci from "fs";
import $ from "fs";
import Xs from "path";
import { win32 as xn } from "node:path";
import rr from "path";
import Lr from "node:fs";
import io from "node:assert";
import { randomBytes as xr } from "node:crypto";
import u from "node:fs";
import R from "node:path";
import lr from "fs";
import ui from "node:fs";
import Ee from "node:path";
import k from "node:fs";
import qn from "node:fs/promises";
import mi from "node:path";
import { join as Er } from "node:path";
import v from "node:fs";
import Nr from "node:path";
var Dr = Object.defineProperty;
var Ar = (s3, t) => {
  for (var e in t) Dr(s3, e, { get: t[e], enumerable: true });
};
var Ts = typeof process == "object" && process ? process : { stdout: null, stderr: null };
var Cr = (s3) => !!s3 && typeof s3 == "object" && (s3 instanceof A || s3 instanceof Ds || Fr(s3) || kr(s3));
var Fr = (s3) => !!s3 && typeof s3 == "object" && s3 instanceof Oi && typeof s3.pipe == "function" && s3.pipe !== Ds.Writable.prototype.pipe;
var kr = (s3) => !!s3 && typeof s3 == "object" && s3 instanceof Oi && typeof s3.write == "function" && typeof s3.end == "function";
var q = Symbol("EOF");
var j = Symbol("maybeEmitEnd");
var rt = Symbol("emittedEnd");
var xe = Symbol("emittingEnd");
var jt = Symbol("emittedError");
var Le = Symbol("closed");
var xs = Symbol("read");
var Ne = Symbol("flush");
var Ls = Symbol("flushChunk");
var z = Symbol("encoding");
var Mt = Symbol("decoder");
var b = Symbol("flowing");
var Qt = Symbol("paused");
var Bt = Symbol("resume");
var g = Symbol("buffer");
var D = Symbol("pipes");
var _ = Symbol("bufferLength");
var Si = Symbol("bufferPush");
var De = Symbol("bufferShift");
var L = Symbol("objectMode");
var w = Symbol("destroyed");
var yi = Symbol("error");
var Ri = Symbol("emitData");
var Ns = Symbol("emitEnd");
var bi = Symbol("emitEnd2");
var Z = Symbol("async");
var gi = Symbol("abort");
var Ae = Symbol("aborted");
var Jt = Symbol("signal");
var yt = Symbol("dataListeners");
var C = Symbol("discarded");
var te = (s3) => Promise.resolve().then(s3);
var vr = (s3) => s3();
var Mr = (s3) => s3 === "end" || s3 === "finish" || s3 === "prefinish";
var Br = (s3) => s3 instanceof ArrayBuffer || !!s3 && typeof s3 == "object" && s3.constructor && s3.constructor.name === "ArrayBuffer" && s3.byteLength >= 0;
var Pr = (s3) => !Buffer.isBuffer(s3) && ArrayBuffer.isView(s3);
var Ie = class {
  src;
  dest;
  opts;
  ondrain;
  constructor(t, e, i) {
    this.src = t, this.dest = e, this.opts = i, this.ondrain = () => t[Bt](), this.dest.on("drain", this.ondrain);
  }
  unpipe() {
    this.dest.removeListener("drain", this.ondrain);
  }
  proxyErrors(t) {
  }
  end() {
    this.unpipe(), this.opts.end && this.dest.end();
  }
};
var _i = class extends Ie {
  unpipe() {
    this.src.removeListener("error", this.proxyErrors), super.unpipe();
  }
  constructor(t, e, i) {
    super(t, e, i), this.proxyErrors = (r) => this.dest.emit("error", r), t.on("error", this.proxyErrors);
  }
};
var zr = (s3) => !!s3.objectMode;
var Ur = (s3) => !s3.objectMode && !!s3.encoding && s3.encoding !== "buffer";
var A = class extends Oi {
  [b] = false;
  [Qt] = false;
  [D] = [];
  [g] = [];
  [L];
  [z];
  [Z];
  [Mt];
  [q] = false;
  [rt] = false;
  [xe] = false;
  [Le] = false;
  [jt] = null;
  [_] = 0;
  [w] = false;
  [Jt];
  [Ae] = false;
  [yt] = 0;
  [C] = false;
  writable = true;
  readable = true;
  constructor(...t) {
    let e = t[0] || {};
    if (super(), e.objectMode && typeof e.encoding == "string") throw new TypeError("Encoding and objectMode may not be used together");
    zr(e) ? (this[L] = true, this[z] = null) : Ur(e) ? (this[z] = e.encoding, this[L] = false) : (this[L] = false, this[z] = null), this[Z] = !!e.async, this[Mt] = this[z] ? new Ir(this[z]) : null, e && e.debugExposeBuffer === true && Object.defineProperty(this, "buffer", { get: () => this[g] }), e && e.debugExposePipes === true && Object.defineProperty(this, "pipes", { get: () => this[D] });
    let { signal: i } = e;
    i && (this[Jt] = i, i.aborted ? this[gi]() : i.addEventListener("abort", () => this[gi]()));
  }
  get bufferLength() {
    return this[_];
  }
  get encoding() {
    return this[z];
  }
  set encoding(t) {
    throw new Error("Encoding must be set at instantiation time");
  }
  setEncoding(t) {
    throw new Error("Encoding must be set at instantiation time");
  }
  get objectMode() {
    return this[L];
  }
  set objectMode(t) {
    throw new Error("objectMode must be set at instantiation time");
  }
  get async() {
    return this[Z];
  }
  set async(t) {
    this[Z] = this[Z] || !!t;
  }
  [gi]() {
    this[Ae] = true, this.emit("abort", this[Jt]?.reason), this.destroy(this[Jt]?.reason);
  }
  get aborted() {
    return this[Ae];
  }
  set aborted(t) {
  }
  write(t, e, i) {
    if (this[Ae]) return false;
    if (this[q]) throw new Error("write after end");
    if (this[w]) return this.emit("error", Object.assign(new Error("Cannot call write after a stream was destroyed"), { code: "ERR_STREAM_DESTROYED" })), true;
    typeof e == "function" && (i = e, e = "utf8"), e || (e = "utf8");
    let r = this[Z] ? te : vr;
    if (!this[L] && !Buffer.isBuffer(t)) {
      if (Pr(t)) t = Buffer.from(t.buffer, t.byteOffset, t.byteLength);
      else if (Br(t)) t = Buffer.from(t);
      else if (typeof t != "string") throw new Error("Non-contiguous data written to non-objectMode stream");
    }
    return this[L] ? (this[b] && this[_] !== 0 && this[Ne](true), this[b] ? this.emit("data", t) : this[Si](t), this[_] !== 0 && this.emit("readable"), i && r(i), this[b]) : t.length ? (typeof t == "string" && !(e === this[z] && !this[Mt]?.lastNeed) && (t = Buffer.from(t, e)), Buffer.isBuffer(t) && this[z] && (t = this[Mt].write(t)), this[b] && this[_] !== 0 && this[Ne](true), this[b] ? this.emit("data", t) : this[Si](t), this[_] !== 0 && this.emit("readable"), i && r(i), this[b]) : (this[_] !== 0 && this.emit("readable"), i && r(i), this[b]);
  }
  read(t) {
    if (this[w]) return null;
    if (this[C] = false, this[_] === 0 || t === 0 || t && t > this[_]) return this[j](), null;
    this[L] && (t = null), this[g].length > 1 && !this[L] && (this[g] = [this[z] ? this[g].join("") : Buffer.concat(this[g], this[_])]);
    let e = this[xs](t || null, this[g][0]);
    return this[j](), e;
  }
  [xs](t, e) {
    if (this[L]) this[De]();
    else {
      let i = e;
      t === i.length || t === null ? this[De]() : typeof i == "string" ? (this[g][0] = i.slice(t), e = i.slice(0, t), this[_] -= t) : (this[g][0] = i.subarray(t), e = i.subarray(0, t), this[_] -= t);
    }
    return this.emit("data", e), !this[g].length && !this[q] && this.emit("drain"), e;
  }
  end(t, e, i) {
    return typeof t == "function" && (i = t, t = void 0), typeof e == "function" && (i = e, e = "utf8"), t !== void 0 && this.write(t, e), i && this.once("end", i), this[q] = true, this.writable = false, (this[b] || !this[Qt]) && this[j](), this;
  }
  [Bt]() {
    this[w] || (!this[yt] && !this[D].length && (this[C] = true), this[Qt] = false, this[b] = true, this.emit("resume"), this[g].length ? this[Ne]() : this[q] ? this[j]() : this.emit("drain"));
  }
  resume() {
    return this[Bt]();
  }
  pause() {
    this[b] = false, this[Qt] = true, this[C] = false;
  }
  get destroyed() {
    return this[w];
  }
  get flowing() {
    return this[b];
  }
  get paused() {
    return this[Qt];
  }
  [Si](t) {
    this[L] ? this[_] += 1 : this[_] += t.length, this[g].push(t);
  }
  [De]() {
    return this[L] ? this[_] -= 1 : this[_] -= this[g][0].length, this[g].shift();
  }
  [Ne](t = false) {
    do
      ;
    while (this[Ls](this[De]()) && this[g].length);
    !t && !this[g].length && !this[q] && this.emit("drain");
  }
  [Ls](t) {
    return this.emit("data", t), this[b];
  }
  pipe(t, e) {
    if (this[w]) return t;
    this[C] = false;
    let i = this[rt];
    return e = e || {}, t === Ts.stdout || t === Ts.stderr ? e.end = false : e.end = e.end !== false, e.proxyErrors = !!e.proxyErrors, i ? e.end && t.end() : (this[D].push(e.proxyErrors ? new _i(this, t, e) : new Ie(this, t, e)), this[Z] ? te(() => this[Bt]()) : this[Bt]()), t;
  }
  unpipe(t) {
    let e = this[D].find((i) => i.dest === t);
    e && (this[D].length === 1 ? (this[b] && this[yt] === 0 && (this[b] = false), this[D] = []) : this[D].splice(this[D].indexOf(e), 1), e.unpipe());
  }
  addListener(t, e) {
    return this.on(t, e);
  }
  on(t, e) {
    let i = super.on(t, e);
    if (t === "data") this[C] = false, this[yt]++, !this[D].length && !this[b] && this[Bt]();
    else if (t === "readable" && this[_] !== 0) super.emit("readable");
    else if (Mr(t) && this[rt]) super.emit(t), this.removeAllListeners(t);
    else if (t === "error" && this[jt]) {
      let r = e;
      this[Z] ? te(() => r.call(this, this[jt])) : r.call(this, this[jt]);
    }
    return i;
  }
  removeListener(t, e) {
    return this.off(t, e);
  }
  off(t, e) {
    let i = super.off(t, e);
    return t === "data" && (this[yt] = this.listeners("data").length, this[yt] === 0 && !this[C] && !this[D].length && (this[b] = false)), i;
  }
  removeAllListeners(t) {
    let e = super.removeAllListeners(t);
    return (t === "data" || t === void 0) && (this[yt] = 0, !this[C] && !this[D].length && (this[b] = false)), e;
  }
  get emittedEnd() {
    return this[rt];
  }
  [j]() {
    !this[xe] && !this[rt] && !this[w] && this[g].length === 0 && this[q] && (this[xe] = true, this.emit("end"), this.emit("prefinish"), this.emit("finish"), this[Le] && this.emit("close"), this[xe] = false);
  }
  emit(t, ...e) {
    let i = e[0];
    if (t !== "error" && t !== "close" && t !== w && this[w]) return false;
    if (t === "data") return !this[L] && !i ? false : this[Z] ? (te(() => this[Ri](i)), true) : this[Ri](i);
    if (t === "end") return this[Ns]();
    if (t === "close") {
      if (this[Le] = true, !this[rt] && !this[w]) return false;
      let n = super.emit("close");
      return this.removeAllListeners("close"), n;
    } else if (t === "error") {
      this[jt] = i, super.emit(yi, i);
      let n = !this[Jt] || this.listeners("error").length ? super.emit("error", i) : false;
      return this[j](), n;
    } else if (t === "resume") {
      let n = super.emit("resume");
      return this[j](), n;
    } else if (t === "finish" || t === "prefinish") {
      let n = super.emit(t);
      return this.removeAllListeners(t), n;
    }
    let r = super.emit(t, ...e);
    return this[j](), r;
  }
  [Ri](t) {
    for (let i of this[D]) i.dest.write(t) === false && this.pause();
    let e = this[C] ? false : super.emit("data", t);
    return this[j](), e;
  }
  [Ns]() {
    return this[rt] ? false : (this[rt] = true, this.readable = false, this[Z] ? (te(() => this[bi]()), true) : this[bi]());
  }
  [bi]() {
    if (this[Mt]) {
      let e = this[Mt].end();
      if (e) {
        for (let i of this[D]) i.dest.write(e);
        this[C] || super.emit("data", e);
      }
    }
    for (let e of this[D]) e.end();
    let t = super.emit("end");
    return this.removeAllListeners("end"), t;
  }
  async collect() {
    let t = Object.assign([], { dataLength: 0 });
    this[L] || (t.dataLength = 0);
    let e = this.promise();
    return this.on("data", (i) => {
      t.push(i), this[L] || (t.dataLength += i.length);
    }), await e, t;
  }
  async concat() {
    if (this[L]) throw new Error("cannot concat in objectMode");
    let t = await this.collect();
    return this[z] ? t.join("") : Buffer.concat(t, t.dataLength);
  }
  async promise() {
    return new Promise((t, e) => {
      this.on(w, () => e(new Error("stream destroyed"))), this.on("error", (i) => e(i)), this.on("end", () => t());
    });
  }
  [Symbol.asyncIterator]() {
    this[C] = false;
    let t = false, e = async () => (this.pause(), t = true, { value: void 0, done: true });
    return { next: () => {
      if (t) return e();
      let r = this.read();
      if (r !== null) return Promise.resolve({ done: false, value: r });
      if (this[q]) return e();
      let n, o, h = (d) => {
        this.off("data", a), this.off("end", l), this.off(w, c), e(), o(d);
      }, a = (d) => {
        this.off("error", h), this.off("end", l), this.off(w, c), this.pause(), n({ value: d, done: !!this[q] });
      }, l = () => {
        this.off("error", h), this.off("data", a), this.off(w, c), e(), n({ done: true, value: void 0 });
      }, c = () => h(new Error("stream destroyed"));
      return new Promise((d, S) => {
        o = S, n = d, this.once(w, c), this.once("error", h), this.once("end", l), this.once("data", a);
      });
    }, throw: e, return: e, [Symbol.asyncIterator]() {
      return this;
    }, [Symbol.asyncDispose]: async () => {
    } };
  }
  [Symbol.iterator]() {
    this[C] = false;
    let t = false, e = () => (this.pause(), this.off(yi, e), this.off(w, e), this.off("end", e), t = true, { done: true, value: void 0 }), i = () => {
      if (t) return e();
      let r = this.read();
      return r === null ? e() : { done: false, value: r };
    };
    return this.once("end", e), this.once(yi, e), this.once(w, e), { next: i, throw: e, return: e, [Symbol.iterator]() {
      return this;
    }, [Symbol.dispose]: () => {
    } };
  }
  destroy(t) {
    if (this[w]) return t ? this.emit("error", t) : this.emit(w), this;
    this[w] = true, this[C] = true, this[g].length = 0, this[_] = 0;
    let e = this;
    return typeof e.close == "function" && !this[Le] && e.close(), t ? this.emit("error", t) : this.emit(w), this;
  }
  static get isStream() {
    return Cr;
  }
};
var Wr = I.writev;
var ot = Symbol("_autoClose");
var H = Symbol("_close");
var ee = Symbol("_ended");
var m = Symbol("_fd");
var Ti = Symbol("_finished");
var J = Symbol("_flags");
var xi = Symbol("_flush");
var Ai = Symbol("_handleChunk");
var Ii = Symbol("_makeBuf");
var se = Symbol("_mode");
var Ce = Symbol("_needDrain");
var Ut = Symbol("_onerror");
var Ht = Symbol("_onopen");
var Li = Symbol("_onread");
var Pt = Symbol("_onwrite");
var ht = Symbol("_open");
var U = Symbol("_path");
var nt = Symbol("_pos");
var Y = Symbol("_queue");
var zt = Symbol("_read");
var Ni = Symbol("_readSize");
var Q = Symbol("_reading");
var ie = Symbol("_remain");
var Di = Symbol("_size");
var Fe = Symbol("_write");
var Rt = Symbol("_writing");
var ke = Symbol("_defaultFlag");
var bt = Symbol("_errored");
var gt = class extends A {
  [bt] = false;
  [m];
  [U];
  [Ni];
  [Q] = false;
  [Di];
  [ie];
  [ot];
  constructor(t, e) {
    if (e = e || {}, super(e), this.readable = true, this.writable = false, typeof t != "string") throw new TypeError("path must be a string");
    this[bt] = false, this[m] = typeof e.fd == "number" ? e.fd : void 0, this[U] = t, this[Ni] = e.readSize || 16 * 1024 * 1024, this[Q] = false, this[Di] = typeof e.size == "number" ? e.size : 1 / 0, this[ie] = this[Di], this[ot] = typeof e.autoClose == "boolean" ? e.autoClose : true, typeof this[m] == "number" ? this[zt]() : this[ht]();
  }
  get fd() {
    return this[m];
  }
  get path() {
    return this[U];
  }
  write() {
    throw new TypeError("this is a readable stream");
  }
  end() {
    throw new TypeError("this is a readable stream");
  }
  [ht]() {
    I.open(this[U], "r", (t, e) => this[Ht](t, e));
  }
  [Ht](t, e) {
    t ? this[Ut](t) : (this[m] = e, this.emit("open", e), this[zt]());
  }
  [Ii]() {
    return Buffer.allocUnsafe(Math.min(this[Ni], this[ie]));
  }
  [zt]() {
    if (!this[Q]) {
      this[Q] = true;
      let t = this[Ii]();
      if (t.length === 0) return process.nextTick(() => this[Li](null, 0, t));
      I.read(this[m], t, 0, t.length, null, (e, i, r) => this[Li](e, i, r));
    }
  }
  [Li](t, e, i) {
    this[Q] = false, t ? this[Ut](t) : this[Ai](e, i) && this[zt]();
  }
  [H]() {
    if (this[ot] && typeof this[m] == "number") {
      let t = this[m];
      this[m] = void 0, I.close(t, (e) => e ? this.emit("error", e) : this.emit("close"));
    }
  }
  [Ut](t) {
    this[Q] = true, this[H](), this.emit("error", t);
  }
  [Ai](t, e) {
    let i = false;
    return this[ie] -= t, t > 0 && (i = super.write(t < e.length ? e.subarray(0, t) : e)), (t === 0 || this[ie] <= 0) && (i = false, this[H](), super.end()), i;
  }
  emit(t, ...e) {
    switch (t) {
      case "prefinish":
      case "finish":
        return false;
      case "drain":
        return typeof this[m] == "number" && this[zt](), false;
      case "error":
        return this[bt] ? false : (this[bt] = true, super.emit(t, ...e));
      default:
        return super.emit(t, ...e);
    }
  }
};
var ve = class extends gt {
  [ht]() {
    let t = true;
    try {
      this[Ht](null, I.openSync(this[U], "r")), t = false;
    } finally {
      t && this[H]();
    }
  }
  [zt]() {
    let t = true;
    try {
      if (!this[Q]) {
        this[Q] = true;
        do {
          let e = this[Ii](), i = e.length === 0 ? 0 : I.readSync(this[m], e, 0, e.length, null);
          if (!this[Ai](i, e)) break;
        } while (true);
        this[Q] = false;
      }
      t = false;
    } finally {
      t && this[H]();
    }
  }
  [H]() {
    if (this[ot] && typeof this[m] == "number") {
      let t = this[m];
      this[m] = void 0, I.closeSync(t), this.emit("close");
    }
  }
};
var tt = class extends Hr {
  readable = false;
  writable = true;
  [bt] = false;
  [Rt] = false;
  [ee] = false;
  [Y] = [];
  [Ce] = false;
  [U];
  [se];
  [ot];
  [m];
  [ke];
  [J];
  [Ti] = false;
  [nt];
  constructor(t, e) {
    e = e || {}, super(e), this[U] = t, this[m] = typeof e.fd == "number" ? e.fd : void 0, this[se] = e.mode === void 0 ? 438 : e.mode, this[nt] = typeof e.start == "number" ? e.start : void 0, this[ot] = typeof e.autoClose == "boolean" ? e.autoClose : true;
    let i = this[nt] !== void 0 ? "r+" : "w";
    this[ke] = e.flags === void 0, this[J] = e.flags === void 0 ? i : e.flags, this[m] === void 0 && this[ht]();
  }
  emit(t, ...e) {
    if (t === "error") {
      if (this[bt]) return false;
      this[bt] = true;
    }
    return super.emit(t, ...e);
  }
  get fd() {
    return this[m];
  }
  get path() {
    return this[U];
  }
  [Ut](t) {
    this[H](), this[Rt] = true, this.emit("error", t);
  }
  [ht]() {
    I.open(this[U], this[J], this[se], (t, e) => this[Ht](t, e));
  }
  [Ht](t, e) {
    this[ke] && this[J] === "r+" && t && t.code === "ENOENT" ? (this[J] = "w", this[ht]()) : t ? this[Ut](t) : (this[m] = e, this.emit("open", e), this[Rt] || this[xi]());
  }
  end(t, e) {
    return t && this.write(t, e), this[ee] = true, !this[Rt] && !this[Y].length && typeof this[m] == "number" && this[Pt](null, 0), this;
  }
  write(t, e) {
    return typeof t == "string" && (t = Buffer.from(t, e)), this[ee] ? (this.emit("error", new Error("write() after end()")), false) : this[m] === void 0 || this[Rt] || this[Y].length ? (this[Y].push(t), this[Ce] = true, false) : (this[Rt] = true, this[Fe](t), true);
  }
  [Fe](t) {
    I.write(this[m], t, 0, t.length, this[nt], (e, i) => this[Pt](e, i));
  }
  [Pt](t, e) {
    t ? this[Ut](t) : (this[nt] !== void 0 && typeof e == "number" && (this[nt] += e), this[Y].length ? this[xi]() : (this[Rt] = false, this[ee] && !this[Ti] ? (this[Ti] = true, this[H](), this.emit("finish")) : this[Ce] && (this[Ce] = false, this.emit("drain"))));
  }
  [xi]() {
    if (this[Y].length === 0) this[ee] && this[Pt](null, 0);
    else if (this[Y].length === 1) this[Fe](this[Y].pop());
    else {
      let t = this[Y];
      this[Y] = [], Wr(this[m], t, this[nt], (e, i) => this[Pt](e, i));
    }
  }
  [H]() {
    if (this[ot] && typeof this[m] == "number") {
      let t = this[m];
      this[m] = void 0, I.close(t, (e) => e ? this.emit("error", e) : this.emit("close"));
    }
  }
};
var Wt = class extends tt {
  [ht]() {
    let t;
    if (this[ke] && this[J] === "r+") try {
      t = I.openSync(this[U], this[J], this[se]);
    } catch (e) {
      if (e?.code === "ENOENT") return this[J] = "w", this[ht]();
      throw e;
    }
    else t = I.openSync(this[U], this[J], this[se]);
    this[Ht](null, t);
  }
  [H]() {
    if (this[ot] && typeof this[m] == "number") {
      let t = this[m];
      this[m] = void 0, I.closeSync(t), this.emit("close");
    }
  }
  [Fe](t) {
    let e = true;
    try {
      this[Pt](null, I.writeSync(this[m], t, 0, t.length, this[nt])), e = false;
    } finally {
      if (e) try {
        this[H]();
      } catch {
      }
    }
  }
};
var Gr = /* @__PURE__ */ new Map([["C", "cwd"], ["f", "file"], ["z", "gzip"], ["P", "preservePaths"], ["U", "unlink"], ["strip-components", "strip"], ["stripComponents", "strip"], ["keep-newer", "newer"], ["keepNewer", "newer"], ["keep-newer-files", "newer"], ["keepNewerFiles", "newer"], ["k", "keep"], ["keep-existing", "keep"], ["keepExisting", "keep"], ["m", "noMtime"], ["no-mtime", "noMtime"], ["p", "preserveOwner"], ["L", "follow"], ["h", "follow"], ["onentry", "onReadEntry"]]);
var As = (s3) => !!s3.sync && !!s3.file;
var Is = (s3) => !s3.sync && !!s3.file;
var Cs = (s3) => !!s3.sync && !s3.file;
var Fs = (s3) => !s3.sync && !s3.file;
var ks = (s3) => !!s3.file;
var Zr = (s3) => {
  let t = Gr.get(s3);
  return t || s3;
};
var re = (s3 = {}) => {
  if (!s3) return {};
  let t = {};
  for (let [e, i] of Object.entries(s3)) {
    let r = Zr(e);
    t[r] = i;
  }
  return t.chmod === void 0 && t.noChmod === false && (t.chmod = true), delete t.noChmod, t;
};
var K = (s3, t, e, i, r) => Object.assign((n = [], o, h) => {
  Array.isArray(n) && (o = n, n = {}), typeof o == "function" && (h = o, o = void 0), o ? o = Array.from(o) : o = [];
  let a = re(n);
  if (r?.(a, o), As(a)) {
    if (typeof h == "function") throw new TypeError("callback not supported for sync tar functions");
    return s3(a, o);
  } else if (Is(a)) {
    let l = t(a, o), c = h || void 0;
    return c ? l.then(() => c(), c) : l;
  } else if (Cs(a)) {
    if (typeof h == "function") throw new TypeError("callback not supported for sync tar functions");
    return e(a, o);
  } else if (Fs(a)) {
    if (typeof h == "function") throw new TypeError("callback only supported with file option");
    return i(a, o);
  } else throw new Error("impossible options??");
}, { syncFile: s3, asyncFile: t, syncNoFile: e, asyncNoFile: i, validate: r });
var Kr = Yr.constants || { ZLIB_VERNUM: 4736 };
var M = Object.freeze(Object.assign(/* @__PURE__ */ Object.create(null), { Z_NO_FLUSH: 0, Z_PARTIAL_FLUSH: 1, Z_SYNC_FLUSH: 2, Z_FULL_FLUSH: 3, Z_FINISH: 4, Z_BLOCK: 5, Z_OK: 0, Z_STREAM_END: 1, Z_NEED_DICT: 2, Z_ERRNO: -1, Z_STREAM_ERROR: -2, Z_DATA_ERROR: -3, Z_MEM_ERROR: -4, Z_BUF_ERROR: -5, Z_VERSION_ERROR: -6, Z_NO_COMPRESSION: 0, Z_BEST_SPEED: 1, Z_BEST_COMPRESSION: 9, Z_DEFAULT_COMPRESSION: -1, Z_FILTERED: 1, Z_HUFFMAN_ONLY: 2, Z_RLE: 3, Z_FIXED: 4, Z_DEFAULT_STRATEGY: 0, DEFLATE: 1, INFLATE: 2, GZIP: 3, GUNZIP: 4, DEFLATERAW: 5, INFLATERAW: 6, UNZIP: 7, BROTLI_DECODE: 8, BROTLI_ENCODE: 9, Z_MIN_WINDOWBITS: 8, Z_MAX_WINDOWBITS: 15, Z_DEFAULT_WINDOWBITS: 15, Z_MIN_CHUNK: 64, Z_MAX_CHUNK: 1 / 0, Z_DEFAULT_CHUNK: 16384, Z_MIN_MEMLEVEL: 1, Z_MAX_MEMLEVEL: 9, Z_DEFAULT_MEMLEVEL: 8, Z_MIN_LEVEL: -1, Z_MAX_LEVEL: 9, Z_DEFAULT_LEVEL: -1, BROTLI_OPERATION_PROCESS: 0, BROTLI_OPERATION_FLUSH: 1, BROTLI_OPERATION_FINISH: 2, BROTLI_OPERATION_EMIT_METADATA: 3, BROTLI_MODE_GENERIC: 0, BROTLI_MODE_TEXT: 1, BROTLI_MODE_FONT: 2, BROTLI_DEFAULT_MODE: 0, BROTLI_MIN_QUALITY: 0, BROTLI_MAX_QUALITY: 11, BROTLI_DEFAULT_QUALITY: 11, BROTLI_MIN_WINDOW_BITS: 10, BROTLI_MAX_WINDOW_BITS: 24, BROTLI_LARGE_MAX_WINDOW_BITS: 30, BROTLI_DEFAULT_WINDOW: 22, BROTLI_MIN_INPUT_BLOCK_BITS: 16, BROTLI_MAX_INPUT_BLOCK_BITS: 24, BROTLI_PARAM_MODE: 0, BROTLI_PARAM_QUALITY: 1, BROTLI_PARAM_LGWIN: 2, BROTLI_PARAM_LGBLOCK: 3, BROTLI_PARAM_DISABLE_LITERAL_CONTEXT_MODELING: 4, BROTLI_PARAM_SIZE_HINT: 5, BROTLI_PARAM_LARGE_WINDOW: 6, BROTLI_PARAM_NPOSTFIX: 7, BROTLI_PARAM_NDIRECT: 8, BROTLI_DECODER_RESULT_ERROR: 0, BROTLI_DECODER_RESULT_SUCCESS: 1, BROTLI_DECODER_RESULT_NEEDS_MORE_INPUT: 2, BROTLI_DECODER_RESULT_NEEDS_MORE_OUTPUT: 3, BROTLI_DECODER_PARAM_DISABLE_RING_BUFFER_REALLOCATION: 0, BROTLI_DECODER_PARAM_LARGE_WINDOW: 1, BROTLI_DECODER_NO_ERROR: 0, BROTLI_DECODER_SUCCESS: 1, BROTLI_DECODER_NEEDS_MORE_INPUT: 2, BROTLI_DECODER_NEEDS_MORE_OUTPUT: 3, BROTLI_DECODER_ERROR_FORMAT_EXUBERANT_NIBBLE: -1, BROTLI_DECODER_ERROR_FORMAT_RESERVED: -2, BROTLI_DECODER_ERROR_FORMAT_EXUBERANT_META_NIBBLE: -3, BROTLI_DECODER_ERROR_FORMAT_SIMPLE_HUFFMAN_ALPHABET: -4, BROTLI_DECODER_ERROR_FORMAT_SIMPLE_HUFFMAN_SAME: -5, BROTLI_DECODER_ERROR_FORMAT_CL_SPACE: -6, BROTLI_DECODER_ERROR_FORMAT_HUFFMAN_SPACE: -7, BROTLI_DECODER_ERROR_FORMAT_CONTEXT_MAP_REPEAT: -8, BROTLI_DECODER_ERROR_FORMAT_BLOCK_LENGTH_1: -9, BROTLI_DECODER_ERROR_FORMAT_BLOCK_LENGTH_2: -10, BROTLI_DECODER_ERROR_FORMAT_TRANSFORM: -11, BROTLI_DECODER_ERROR_FORMAT_DICTIONARY: -12, BROTLI_DECODER_ERROR_FORMAT_WINDOW_BITS: -13, BROTLI_DECODER_ERROR_FORMAT_PADDING_1: -14, BROTLI_DECODER_ERROR_FORMAT_PADDING_2: -15, BROTLI_DECODER_ERROR_FORMAT_DISTANCE: -16, BROTLI_DECODER_ERROR_DICTIONARY_NOT_SET: -19, BROTLI_DECODER_ERROR_INVALID_ARGUMENTS: -20, BROTLI_DECODER_ERROR_ALLOC_CONTEXT_MODES: -21, BROTLI_DECODER_ERROR_ALLOC_TREE_GROUPS: -22, BROTLI_DECODER_ERROR_ALLOC_CONTEXT_MAP: -25, BROTLI_DECODER_ERROR_ALLOC_RING_BUFFER_1: -26, BROTLI_DECODER_ERROR_ALLOC_RING_BUFFER_2: -27, BROTLI_DECODER_ERROR_ALLOC_BLOCK_TYPE_TREES: -30, BROTLI_DECODER_ERROR_UNREACHABLE: -31 }, Kr));
var Vr = _t.concat;
var Ms = Object.getOwnPropertyDescriptor(_t, "concat");
var $r = (s3) => s3;
var Fi = Ms?.writable === true || Ms?.set !== void 0 ? (s3) => {
  _t.concat = s3 ? $r : Vr;
} : (s3) => {
};
var Ot = Symbol("_superWrite");
var Gt = class extends Error {
  code;
  errno;
  constructor(t, e) {
    super("zlib: " + t.message, { cause: t }), this.code = t.code, this.errno = t.errno, this.code || (this.code = "ZLIB_ERROR"), this.message = "zlib: " + t.message, Error.captureStackTrace(this, e ?? this.constructor);
  }
  get name() {
    return "ZlibError";
  }
};
var ki = Symbol("flushFlag");
var ne = class extends A {
  #t = false;
  #i = false;
  #s;
  #n;
  #r;
  #e;
  #o;
  get sawError() {
    return this.#t;
  }
  get handle() {
    return this.#e;
  }
  get flushFlag() {
    return this.#s;
  }
  constructor(t, e) {
    if (!t || typeof t != "object") throw new TypeError("invalid options for ZlibBase constructor");
    if (super(t), this.#s = t.flush ?? 0, this.#n = t.finishFlush ?? 0, this.#r = t.fullFlushFlag ?? 0, typeof vs[e] != "function") throw new TypeError("Compression method not supported: " + e);
    try {
      this.#e = new vs[e](t);
    } catch (i) {
      throw new Gt(i, this.constructor);
    }
    this.#o = (i) => {
      this.#t || (this.#t = true, this.close(), this.emit("error", i));
    }, this.#e?.on("error", (i) => this.#o(new Gt(i))), this.once("end", () => this.close);
  }
  close() {
    this.#e && (this.#e.close(), this.#e = void 0, this.emit("close"));
  }
  reset() {
    if (!this.#t) return vi(this.#e, "zlib binding closed"), this.#e.reset?.();
  }
  flush(t) {
    this.ended || (typeof t != "number" && (t = this.#r), this.write(Object.assign(_t.alloc(0), { [ki]: t })));
  }
  end(t, e, i) {
    return typeof t == "function" && (i = t, e = void 0, t = void 0), typeof e == "function" && (i = e, e = void 0), t && (e ? this.write(t, e) : this.write(t)), this.flush(this.#n), this.#i = true, super.end(i);
  }
  get ended() {
    return this.#i;
  }
  [Ot](t) {
    return super.write(t);
  }
  write(t, e, i) {
    if (typeof e == "function" && (i = e, e = "utf8"), typeof t == "string" && (t = _t.from(t, e)), this.#t) return;
    vi(this.#e, "zlib binding closed");
    let r = this.#e._handle, n = r.close;
    r.close = () => {
    };
    let o = this.#e.close;
    this.#e.close = () => {
    }, Fi(true);
    let h;
    try {
      let l = typeof t[ki] == "number" ? t[ki] : this.#s;
      h = this.#e._processChunk(t, l), Fi(false);
    } catch (l) {
      Fi(false), this.#o(new Gt(l, this.write));
    } finally {
      this.#e && (this.#e._handle = r, r.close = n, this.#e.close = o, this.#e.removeAllListeners("error"));
    }
    this.#e && this.#e.on("error", (l) => this.#o(new Gt(l, this.write)));
    let a;
    if (h) if (Array.isArray(h) && h.length > 0) {
      let l = h[0];
      a = this[Ot](_t.from(l));
      for (let c = 1; c < h.length; c++) a = this[Ot](h[c]);
    } else a = this[Ot](_t.from(h));
    return i && i(), a;
  }
};
var Me = class extends ne {
  #t;
  #i;
  constructor(t, e) {
    t = t || {}, t.flush = t.flush || M.Z_NO_FLUSH, t.finishFlush = t.finishFlush || M.Z_FINISH, t.fullFlushFlag = M.Z_FULL_FLUSH, super(t, e), this.#t = t.level, this.#i = t.strategy;
  }
  params(t, e) {
    if (!this.sawError) {
      if (!this.handle) throw new Error("cannot switch params when binding is closed");
      if (!this.handle.params) throw new Error("not supported in this implementation");
      if (this.#t !== t || this.#i !== e) {
        this.flush(M.Z_SYNC_FLUSH), vi(this.handle, "zlib binding closed");
        let i = this.handle.flush;
        this.handle.flush = (r, n) => {
          typeof r == "function" && (n = r, r = this.flushFlag), this.flush(r), n?.();
        };
        try {
          this.handle.params(t, e);
        } finally {
          this.handle.flush = i;
        }
        this.handle && (this.#t = t, this.#i = e);
      }
    }
  }
};
var Be = class extends Me {
  #t;
  constructor(t) {
    super(t, "Gzip"), this.#t = t && !!t.portable;
  }
  [Ot](t) {
    return this.#t ? (this.#t = false, t[9] = 255, super[Ot](t)) : super[Ot](t);
  }
};
var Pe = class extends Me {
  constructor(t) {
    super(t, "Unzip");
  }
};
var ze = class extends ne {
  constructor(t, e) {
    t = t || {}, t.flush = t.flush || M.BROTLI_OPERATION_PROCESS, t.finishFlush = t.finishFlush || M.BROTLI_OPERATION_FINISH, t.fullFlushFlag = M.BROTLI_OPERATION_FLUSH, super(t, e);
  }
};
var Ue = class extends ze {
  constructor(t) {
    super(t, "BrotliCompress");
  }
};
var He = class extends ze {
  constructor(t) {
    super(t, "BrotliDecompress");
  }
};
var We = class extends ne {
  constructor(t, e) {
    t = t || {}, t.flush = t.flush || M.ZSTD_e_continue, t.finishFlush = t.finishFlush || M.ZSTD_e_end, t.fullFlushFlag = M.ZSTD_e_flush, super(t, e);
  }
};
var Ge = class extends We {
  constructor(t) {
    super(t, "ZstdCompress");
  }
};
var Ze = class extends We {
  constructor(t) {
    super(t, "ZstdDecompress");
  }
};
var Bs = (s3, t) => {
  if (Number.isSafeInteger(s3)) s3 < 0 ? jr(s3, t) : qr(s3, t);
  else throw Error("cannot encode number outside of javascript safe integer range");
  return t;
};
var qr = (s3, t) => {
  t[0] = 128;
  for (var e = t.length; e > 1; e--) t[e - 1] = s3 & 255, s3 = Math.floor(s3 / 256);
};
var jr = (s3, t) => {
  t[0] = 255;
  var e = false;
  s3 = s3 * -1;
  for (var i = t.length; i > 1; i--) {
    var r = s3 & 255;
    s3 = Math.floor(s3 / 256), e ? t[i - 1] = zs(r) : r === 0 ? t[i - 1] = 0 : (e = true, t[i - 1] = Us(r));
  }
};
var Ps = (s3) => {
  let t = s3[0], e = t === 128 ? Jr(s3.subarray(1, s3.length)) : t === 255 ? Qr(s3) : null;
  if (e === null) throw Error("invalid base256 encoding");
  if (!Number.isSafeInteger(e)) throw Error("parsed number outside of javascript safe integer range");
  return e;
};
var Qr = (s3) => {
  for (var t = s3.length, e = 0, i = false, r = t - 1; r > -1; r--) {
    var n = Number(s3[r]), o;
    i ? o = zs(n) : n === 0 ? o = n : (i = true, o = Us(n)), o !== 0 && (e -= o * Math.pow(256, t - r - 1));
  }
  return e;
};
var Jr = (s3) => {
  for (var t = s3.length, e = 0, i = t - 1; i > -1; i--) {
    var r = Number(s3[i]);
    r !== 0 && (e += r * Math.pow(256, t - i - 1));
  }
  return e;
};
var zs = (s3) => (255 ^ s3) & 255;
var Us = (s3) => (255 ^ s3) + 1 & 255;
var Mi = {};
Ar(Mi, { code: () => Ye, isCode: () => oe, isName: () => en, name: () => he });
var oe = (s3) => he.has(s3);
var en = (s3) => Ye.has(s3);
var he = /* @__PURE__ */ new Map([["0", "File"], ["", "OldFile"], ["1", "Link"], ["2", "SymbolicLink"], ["3", "CharacterDevice"], ["4", "BlockDevice"], ["5", "Directory"], ["6", "FIFO"], ["7", "ContiguousFile"], ["g", "GlobalExtendedHeader"], ["x", "ExtendedHeader"], ["A", "SolarisACL"], ["D", "GNUDumpDir"], ["I", "Inode"], ["K", "NextFileHasLongLinkpath"], ["L", "NextFileHasLongPath"], ["M", "ContinuationFile"], ["N", "OldGnuLongPath"], ["S", "SparseFile"], ["V", "TapeVolumeHeader"], ["X", "OldExtendedHeader"]]);
var Ye = new Map(Array.from(he).map((s3) => [s3[1], s3[0]]));
var F = class {
  cksumValid = false;
  needPax = false;
  nullBlock = false;
  block;
  path;
  mode;
  uid;
  gid;
  size;
  cksum;
  #t = "Unsupported";
  linkpath;
  uname;
  gname;
  devmaj = 0;
  devmin = 0;
  atime;
  ctime;
  mtime;
  charset;
  comment;
  constructor(t, e = 0, i, r) {
    Buffer.isBuffer(t) ? this.decode(t, e || 0, i, r) : t && this.#i(t);
  }
  decode(t, e, i, r) {
    if (e || (e = 0), !t || !(t.length >= e + 512)) throw new Error("need 512 bytes for header");
    this.path = i?.path ?? Tt(t, e, 100), this.mode = i?.mode ?? r?.mode ?? at(t, e + 100, 8), this.uid = i?.uid ?? r?.uid ?? at(t, e + 108, 8), this.gid = i?.gid ?? r?.gid ?? at(t, e + 116, 8), this.size = i?.size ?? r?.size ?? at(t, e + 124, 12), this.mtime = i?.mtime ?? r?.mtime ?? Bi(t, e + 136, 12), this.cksum = at(t, e + 148, 12), r && this.#i(r, true), i && this.#i(i);
    let n = Tt(t, e + 156, 1);
    if (oe(n) && (this.#t = n || "0"), this.#t === "0" && this.path.slice(-1) === "/" && (this.#t = "5"), this.#t === "5" && (this.size = 0), this.linkpath = Tt(t, e + 157, 100), t.subarray(e + 257, e + 265).toString() === "ustar\x0000") if (this.uname = i?.uname ?? r?.uname ?? Tt(t, e + 265, 32), this.gname = i?.gname ?? r?.gname ?? Tt(t, e + 297, 32), this.devmaj = i?.devmaj ?? r?.devmaj ?? at(t, e + 329, 8) ?? 0, this.devmin = i?.devmin ?? r?.devmin ?? at(t, e + 337, 8) ?? 0, t[e + 475] !== 0) {
      let h = Tt(t, e + 345, 155);
      this.path = h + "/" + this.path;
    } else {
      let h = Tt(t, e + 345, 130);
      h && (this.path = h + "/" + this.path), this.atime = i?.atime ?? r?.atime ?? Bi(t, e + 476, 12), this.ctime = i?.ctime ?? r?.ctime ?? Bi(t, e + 488, 12);
    }
    let o = 256;
    for (let h = e; h < e + 148; h++) o += t[h];
    for (let h = e + 156; h < e + 512; h++) o += t[h];
    this.cksumValid = o === this.cksum, this.cksum === void 0 && o === 256 && (this.nullBlock = true);
  }
  #i(t, e = false) {
    Object.assign(this, Object.fromEntries(Object.entries(t).filter(([i, r]) => !(r == null || i === "path" && e || i === "linkpath" && e || i === "global"))));
  }
  encode(t, e = 0) {
    if (t || (t = this.block = Buffer.alloc(512)), this.#t === "Unsupported" && (this.#t = "0"), !(t.length >= e + 512)) throw new Error("need 512 bytes for header");
    let i = this.ctime || this.atime ? 130 : 155, r = sn(this.path || "", i), n = r[0], o = r[1];
    this.needPax = !!r[2], this.needPax = xt(t, e, 100, n) || this.needPax, this.needPax = lt(t, e + 100, 8, this.mode) || this.needPax, this.needPax = lt(t, e + 108, 8, this.uid) || this.needPax, this.needPax = lt(t, e + 116, 8, this.gid) || this.needPax, this.needPax = lt(t, e + 124, 12, this.size) || this.needPax, this.needPax = Pi(t, e + 136, 12, this.mtime) || this.needPax, t[e + 156] = this.#t.charCodeAt(0), this.needPax = xt(t, e + 157, 100, this.linkpath) || this.needPax, t.write("ustar\x0000", e + 257, 8), this.needPax = xt(t, e + 265, 32, this.uname) || this.needPax, this.needPax = xt(t, e + 297, 32, this.gname) || this.needPax, this.needPax = lt(t, e + 329, 8, this.devmaj) || this.needPax, this.needPax = lt(t, e + 337, 8, this.devmin) || this.needPax, this.needPax = xt(t, e + 345, i, o) || this.needPax, t[e + 475] !== 0 ? this.needPax = xt(t, e + 345, 155, o) || this.needPax : (this.needPax = xt(t, e + 345, 130, o) || this.needPax, this.needPax = Pi(t, e + 476, 12, this.atime) || this.needPax, this.needPax = Pi(t, e + 488, 12, this.ctime) || this.needPax);
    let h = 256;
    for (let a = e; a < e + 148; a++) h += t[a];
    for (let a = e + 156; a < e + 512; a++) h += t[a];
    return this.cksum = h, lt(t, e + 148, 8, this.cksum), this.cksumValid = true, this.needPax;
  }
  get type() {
    return this.#t === "Unsupported" ? this.#t : he.get(this.#t);
  }
  get typeKey() {
    return this.#t;
  }
  set type(t) {
    let e = String(Ye.get(t));
    if (oe(e) || e === "Unsupported") this.#t = e;
    else if (oe(t)) this.#t = t;
    else throw new TypeError("invalid entry type: " + t);
  }
};
var sn = (s3, t) => {
  let i = s3, r = "", n, o = Zt.parse(s3).root || ".";
  if (Buffer.byteLength(i) < 100) n = [i, r, false];
  else {
    r = Zt.dirname(i), i = Zt.basename(i);
    do
      Buffer.byteLength(i) <= 100 && Buffer.byteLength(r) <= t ? n = [i, r, false] : Buffer.byteLength(i) > 100 && Buffer.byteLength(r) <= t ? n = [i.slice(0, 99), r, true] : (i = Zt.join(Zt.basename(r), i), r = Zt.dirname(r));
    while (r !== o && n === void 0);
    n || (n = [s3.slice(0, 99), "", true]);
  }
  return n;
};
var Tt = (s3, t, e) => s3.subarray(t, t + e).toString("utf8").replace(/\0.*/, "");
var Bi = (s3, t, e) => rn(at(s3, t, e));
var rn = (s3) => s3 === void 0 ? void 0 : new Date(s3 * 1e3);
var at = (s3, t, e) => Number(s3[t]) & 128 ? Ps(s3.subarray(t, t + e)) : on(s3, t, e);
var nn = (s3) => isNaN(s3) ? void 0 : s3;
var on = (s3, t, e) => nn(parseInt(s3.subarray(t, t + e).toString("utf8").replace(/\0.*$/, "").trim(), 8));
var hn = { 12: 8589934591, 8: 2097151 };
var lt = (s3, t, e, i) => i === void 0 ? false : i > hn[e] || i < 0 ? (Bs(i, s3.subarray(t, t + e)), true) : (an(s3, t, e, i), false);
var an = (s3, t, e, i) => s3.write(ln(i, e), t, e, "ascii");
var ln = (s3, t) => cn(Math.floor(s3).toString(8), t);
var cn = (s3, t) => (s3.length === t - 1 ? s3 : new Array(t - s3.length - 1).join("0") + s3 + " ") + "\0";
var Pi = (s3, t, e, i) => i === void 0 ? false : lt(s3, t, e, i.getTime() / 1e3);
var fn = new Array(156).join("\0");
var xt = (s3, t, e, i) => i === void 0 ? false : (s3.write(i + fn, t, e, "utf8"), i.length !== Buffer.byteLength(i) || i.length > e);
var ct = class s {
  atime;
  mtime;
  ctime;
  charset;
  comment;
  gid;
  uid;
  gname;
  uname;
  linkpath;
  dev;
  ino;
  nlink;
  path;
  size;
  mode;
  global;
  constructor(t, e = false) {
    this.atime = t.atime, this.charset = t.charset, this.comment = t.comment, this.ctime = t.ctime, this.dev = t.dev, this.gid = t.gid, this.global = e, this.gname = t.gname, this.ino = t.ino, this.linkpath = t.linkpath, this.mtime = t.mtime, this.nlink = t.nlink, this.path = t.path, this.size = t.size, this.uid = t.uid, this.uname = t.uname;
  }
  encode() {
    let t = this.encodeBody();
    if (t === "") return Buffer.allocUnsafe(0);
    let e = Buffer.byteLength(t), i = 512 * Math.ceil(1 + e / 512), r = Buffer.allocUnsafe(i);
    for (let n = 0; n < 512; n++) r[n] = 0;
    new F({ path: ("PaxHeader/" + dn(this.path ?? "")).slice(0, 99), mode: this.mode || 420, uid: this.uid, gid: this.gid, size: e, mtime: this.mtime, type: this.global ? "GlobalExtendedHeader" : "ExtendedHeader", linkpath: "", uname: this.uname || "", gname: this.gname || "", devmaj: 0, devmin: 0, atime: this.atime, ctime: this.ctime }).encode(r), r.write(t, 512, e, "utf8");
    for (let n = e + 512; n < r.length; n++) r[n] = 0;
    return r;
  }
  encodeBody() {
    return this.encodeField("path") + this.encodeField("ctime") + this.encodeField("atime") + this.encodeField("dev") + this.encodeField("ino") + this.encodeField("nlink") + this.encodeField("charset") + this.encodeField("comment") + this.encodeField("gid") + this.encodeField("gname") + this.encodeField("linkpath") + this.encodeField("mtime") + this.encodeField("size") + this.encodeField("uid") + this.encodeField("uname");
  }
  encodeField(t) {
    if (this[t] === void 0) return "";
    let e = this[t], i = e instanceof Date ? e.getTime() / 1e3 : e, r = " " + (t === "dev" || t === "ino" || t === "nlink" ? "SCHILY." : "") + t + "=" + i + `
`, n = Buffer.byteLength(r), o = Math.floor(Math.log(n) / Math.log(10)) + 1;
    return n + o >= Math.pow(10, o) && (o += 1), o + n + r;
  }
  static parse(t, e, i = false) {
    return new s(un(mn(t), e), i);
  }
};
var un = (s3, t) => t ? Object.assign({}, t, s3) : s3;
var mn = (s3) => s3.replace(/\n$/, "").split(`
`).reduce(pn, /* @__PURE__ */ Object.create(null));
var pn = (s3, t) => {
  let e = parseInt(t, 10);
  if (e !== Buffer.byteLength(t) + 1) return s3;
  t = t.slice((e + " ").length);
  let i = t.split("="), r = i.shift();
  if (!r) return s3;
  let n = r.replace(/^SCHILY\.(dev|ino|nlink)/, "$1"), o = i.join("=");
  return s3[n] = /^([A-Z]+\.)?([mac]|birth|creation)time$/.test(n) ? new Date(Number(o) * 1e3) : /^[0-9]+$/.test(o) ? +o : o, s3;
};
var En = process.env.TESTING_TAR_FAKE_PLATFORM || process.platform;
var f = En !== "win32" ? (s3) => s3 : (s3) => s3 && s3.replace(/\\/g, "/");
var Yt = class extends A {
  extended;
  globalExtended;
  header;
  startBlockSize;
  blockRemain;
  remain;
  type;
  meta = false;
  ignore = false;
  path;
  mode;
  uid;
  gid;
  uname;
  gname;
  size = 0;
  mtime;
  atime;
  ctime;
  linkpath;
  dev;
  ino;
  nlink;
  invalid = false;
  absolute;
  unsupported = false;
  constructor(t, e, i) {
    switch (super({}), this.pause(), this.extended = e, this.globalExtended = i, this.header = t, this.remain = t.size ?? 0, this.startBlockSize = 512 * Math.ceil(this.remain / 512), this.blockRemain = this.startBlockSize, this.type = t.type, this.type) {
      case "File":
      case "OldFile":
      case "Link":
      case "SymbolicLink":
      case "CharacterDevice":
      case "BlockDevice":
      case "Directory":
      case "FIFO":
      case "ContiguousFile":
      case "GNUDumpDir":
        break;
      case "NextFileHasLongLinkpath":
      case "NextFileHasLongPath":
      case "OldGnuLongPath":
      case "GlobalExtendedHeader":
      case "ExtendedHeader":
      case "OldExtendedHeader":
        this.meta = true;
        break;
      default:
        this.ignore = true;
    }
    if (!t.path) throw new Error("no path provided for tar.ReadEntry");
    this.path = f(t.path), this.mode = t.mode, this.mode && (this.mode = this.mode & 4095), this.uid = t.uid, this.gid = t.gid, this.uname = t.uname, this.gname = t.gname, this.size = this.remain, this.mtime = t.mtime, this.atime = t.atime, this.ctime = t.ctime, this.linkpath = t.linkpath ? f(t.linkpath) : void 0, this.uname = t.uname, this.gname = t.gname, e && this.#t(e), i && this.#t(i, true);
  }
  write(t) {
    let e = t.length;
    if (e > this.blockRemain) throw new Error("writing more to entry than is appropriate");
    let i = this.remain, r = this.blockRemain;
    return this.remain = Math.max(0, i - e), this.blockRemain = Math.max(0, r - e), this.ignore ? true : i >= e ? super.write(t) : super.write(t.subarray(0, i));
  }
  #t(t, e = false) {
    t.path && (t.path = f(t.path)), t.linkpath && (t.linkpath = f(t.linkpath)), Object.assign(this, Object.fromEntries(Object.entries(t).filter(([i, r]) => !(r == null || i === "path" && e))));
  }
};
var Lt = (s3, t, e, i = {}) => {
  s3.file && (i.file = s3.file), s3.cwd && (i.cwd = s3.cwd), i.code = e instanceof Error && e.code || t, i.tarCode = t, !s3.strict && i.recoverable !== false ? (e instanceof Error && (i = Object.assign(e, i), e = e.message), s3.emit("warn", t, e, i)) : e instanceof Error ? s3.emit("error", Object.assign(e, i)) : s3.emit("error", Object.assign(new Error(`${t}: ${e}`), i));
};
var Sn = 1024 * 1024;
var Gi = Buffer.from([31, 139]);
var Zi = Buffer.from([40, 181, 47, 253]);
var yn = Math.max(Gi.length, Zi.length);
var B = Symbol("state");
var Nt = Symbol("writeEntry");
var et = Symbol("readEntry");
var zi = Symbol("nextEntry");
var Hs = Symbol("processEntry");
var V = Symbol("extendedHeader");
var ae = Symbol("globalExtendedHeader");
var ft = Symbol("meta");
var Ws = Symbol("emitMeta");
var p = Symbol("buffer");
var it = Symbol("queue");
var dt = Symbol("ended");
var Ui = Symbol("emittedEnd");
var Dt = Symbol("emit");
var y = Symbol("unzip");
var Ke = Symbol("consumeChunk");
var Ve = Symbol("consumeChunkSub");
var Hi = Symbol("consumeBody");
var Gs = Symbol("consumeMeta");
var Zs = Symbol("consumeHeader");
var le = Symbol("consuming");
var Wi = Symbol("bufferConcat");
var $e = Symbol("maybeEnd");
var Kt = Symbol("writing");
var ut = Symbol("aborted");
var Xe = Symbol("onDone");
var At = Symbol("sawValidEntry");
var qe = Symbol("sawNullBlock");
var je = Symbol("sawEOF");
var Ys = Symbol("closeStream");
var Rn = () => true;
var st = class extends wn {
  file;
  strict;
  maxMetaEntrySize;
  filter;
  brotli;
  zstd;
  writable = true;
  readable = false;
  [it] = [];
  [p];
  [et];
  [Nt];
  [B] = "begin";
  [ft] = "";
  [V];
  [ae];
  [dt] = false;
  [y];
  [ut] = false;
  [At];
  [qe] = false;
  [je] = false;
  [Kt] = false;
  [le] = false;
  [Ui] = false;
  constructor(t = {}) {
    super(), this.file = t.file || "", this.on(Xe, () => {
      (this[B] === "begin" || this[At] === false) && this.warn("TAR_BAD_ARCHIVE", "Unrecognized archive format");
    }), t.ondone ? this.on(Xe, t.ondone) : this.on(Xe, () => {
      this.emit("prefinish"), this.emit("finish"), this.emit("end");
    }), this.strict = !!t.strict, this.maxMetaEntrySize = t.maxMetaEntrySize || Sn, this.filter = typeof t.filter == "function" ? t.filter : Rn;
    let e = t.file && (t.file.endsWith(".tar.br") || t.file.endsWith(".tbr"));
    this.brotli = !(t.gzip || t.zstd) && t.brotli !== void 0 ? t.brotli : e ? void 0 : false;
    let i = t.file && (t.file.endsWith(".tar.zst") || t.file.endsWith(".tzst"));
    this.zstd = !(t.gzip || t.brotli) && t.zstd !== void 0 ? t.zstd : i ? true : void 0, this.on("end", () => this[Ys]()), typeof t.onwarn == "function" && this.on("warn", t.onwarn), typeof t.onReadEntry == "function" && this.on("entry", t.onReadEntry);
  }
  warn(t, e, i = {}) {
    Lt(this, t, e, i);
  }
  [Zs](t, e) {
    this[At] === void 0 && (this[At] = false);
    let i;
    try {
      i = new F(t, e, this[V], this[ae]);
    } catch (r) {
      return this.warn("TAR_ENTRY_INVALID", r);
    }
    if (i.nullBlock) this[qe] ? (this[je] = true, this[B] === "begin" && (this[B] = "header"), this[Dt]("eof")) : (this[qe] = true, this[Dt]("nullBlock"));
    else if (this[qe] = false, !i.cksumValid) this.warn("TAR_ENTRY_INVALID", "checksum failure", { header: i });
    else if (!i.path) this.warn("TAR_ENTRY_INVALID", "path is required", { header: i });
    else {
      let r = i.type;
      if (/^(Symbolic)?Link$/.test(r) && !i.linkpath) this.warn("TAR_ENTRY_INVALID", "linkpath required", { header: i });
      else if (!/^(Symbolic)?Link$/.test(r) && !/^(Global)?ExtendedHeader$/.test(r) && i.linkpath) this.warn("TAR_ENTRY_INVALID", "linkpath forbidden", { header: i });
      else {
        let n = this[Nt] = new Yt(i, this[V], this[ae]);
        if (!this[At]) if (n.remain) {
          let o = () => {
            n.invalid || (this[At] = true);
          };
          n.on("end", o);
        } else this[At] = true;
        n.meta ? n.size > this.maxMetaEntrySize ? (n.ignore = true, this[Dt]("ignoredEntry", n), this[B] = "ignore", n.resume()) : n.size > 0 && (this[ft] = "", n.on("data", (o) => this[ft] += o), this[B] = "meta") : (this[V] = void 0, n.ignore = n.ignore || !this.filter(n.path, n), n.ignore ? (this[Dt]("ignoredEntry", n), this[B] = n.remain ? "ignore" : "header", n.resume()) : (n.remain ? this[B] = "body" : (this[B] = "header", n.end()), this[et] ? this[it].push(n) : (this[it].push(n), this[zi]())));
      }
    }
  }
  [Ys]() {
    queueMicrotask(() => this.emit("close"));
  }
  [Hs](t) {
    let e = true;
    if (!t) this[et] = void 0, e = false;
    else if (Array.isArray(t)) {
      let [i, ...r] = t;
      this.emit(i, ...r);
    } else this[et] = t, this.emit("entry", t), t.emittedEnd || (t.on("end", () => this[zi]()), e = false);
    return e;
  }
  [zi]() {
    do
      ;
    while (this[Hs](this[it].shift()));
    if (!this[it].length) {
      let t = this[et];
      !t || t.flowing || t.size === t.remain ? this[Kt] || this.emit("drain") : t.once("drain", () => this.emit("drain"));
    }
  }
  [Hi](t, e) {
    let i = this[Nt];
    if (!i) throw new Error("attempt to consume body without entry??");
    let r = i.blockRemain ?? 0, n = r >= t.length && e === 0 ? t : t.subarray(e, e + r);
    return i.write(n), i.blockRemain || (this[B] = "header", this[Nt] = void 0, i.end()), n.length;
  }
  [Gs](t, e) {
    let i = this[Nt], r = this[Hi](t, e);
    return !this[Nt] && i && this[Ws](i), r;
  }
  [Dt](t, e, i) {
    !this[it].length && !this[et] ? this.emit(t, e, i) : this[it].push([t, e, i]);
  }
  [Ws](t) {
    switch (this[Dt]("meta", this[ft]), t.type) {
      case "ExtendedHeader":
      case "OldExtendedHeader":
        this[V] = ct.parse(this[ft], this[V], false);
        break;
      case "GlobalExtendedHeader":
        this[ae] = ct.parse(this[ft], this[ae], true);
        break;
      case "NextFileHasLongPath":
      case "OldGnuLongPath": {
        let e = this[V] ?? /* @__PURE__ */ Object.create(null);
        this[V] = e, e.path = this[ft].replace(/\0.*/, "");
        break;
      }
      case "NextFileHasLongLinkpath": {
        let e = this[V] || /* @__PURE__ */ Object.create(null);
        this[V] = e, e.linkpath = this[ft].replace(/\0.*/, "");
        break;
      }
      default:
        throw new Error("unknown meta: " + t.type);
    }
  }
  abort(t) {
    this[ut] = true, this.emit("abort", t), this.warn("TAR_ABORT", t, { recoverable: false });
  }
  write(t, e, i) {
    if (typeof e == "function" && (i = e, e = void 0), typeof t == "string" && (t = Buffer.from(t, typeof e == "string" ? e : "utf8")), this[ut]) return i?.(), false;
    if ((this[y] === void 0 || this.brotli === void 0 && this[y] === false) && t) {
      if (this[p] && (t = Buffer.concat([this[p], t]), this[p] = void 0), t.length < yn) return this[p] = t, i?.(), true;
      for (let a = 0; this[y] === void 0 && a < Gi.length; a++) t[a] !== Gi[a] && (this[y] = false);
      let o = false;
      if (this[y] === false && this.zstd !== false) {
        o = true;
        for (let a = 0; a < Zi.length; a++) if (t[a] !== Zi[a]) {
          o = false;
          break;
        }
      }
      let h = this.brotli === void 0 && !o;
      if (this[y] === false && h) if (t.length < 512) if (this[dt]) this.brotli = true;
      else return this[p] = t, i?.(), true;
      else try {
        new F(t.subarray(0, 512)), this.brotli = false;
      } catch {
        this.brotli = true;
      }
      if (this[y] === void 0 || this[y] === false && (this.brotli || o)) {
        let a = this[dt];
        this[dt] = false, this[y] = this[y] === void 0 ? new Pe({}) : o ? new Ze({}) : new He({}), this[y].on("data", (c) => this[Ke](c)), this[y].on("error", (c) => this.abort(c)), this[y].on("end", () => {
          this[dt] = true, this[Ke]();
        }), this[Kt] = true;
        let l = !!this[y][a ? "end" : "write"](t);
        return this[Kt] = false, i?.(), l;
      }
    }
    this[Kt] = true, this[y] ? this[y].write(t) : this[Ke](t), this[Kt] = false;
    let n = this[it].length ? false : this[et] ? this[et].flowing : true;
    return !n && !this[it].length && this[et]?.once("drain", () => this.emit("drain")), i?.(), n;
  }
  [Wi](t) {
    t && !this[ut] && (this[p] = this[p] ? Buffer.concat([this[p], t]) : t);
  }
  [$e]() {
    if (this[dt] && !this[Ui] && !this[ut] && !this[le]) {
      this[Ui] = true;
      let t = this[Nt];
      if (t && t.blockRemain) {
        let e = this[p] ? this[p].length : 0;
        this.warn("TAR_BAD_ARCHIVE", `Truncated input (needed ${t.blockRemain} more bytes, only ${e} available)`, { entry: t }), this[p] && t.write(this[p]), t.end();
      }
      this[Dt](Xe);
    }
  }
  [Ke](t) {
    if (this[le] && t) this[Wi](t);
    else if (!t && !this[p]) this[$e]();
    else if (t) {
      if (this[le] = true, this[p]) {
        this[Wi](t);
        let e = this[p];
        this[p] = void 0, this[Ve](e);
      } else this[Ve](t);
      for (; this[p] && this[p]?.length >= 512 && !this[ut] && !this[je]; ) {
        let e = this[p];
        this[p] = void 0, this[Ve](e);
      }
      this[le] = false;
    }
    (!this[p] || this[dt]) && this[$e]();
  }
  [Ve](t) {
    let e = 0, i = t.length;
    for (; e + 512 <= i && !this[ut] && !this[je]; ) switch (this[B]) {
      case "begin":
      case "header":
        this[Zs](t, e), e += 512;
        break;
      case "ignore":
      case "body":
        e += this[Hi](t, e);
        break;
      case "meta":
        e += this[Gs](t, e);
        break;
      default:
        throw new Error("invalid state: " + this[B]);
    }
    e < i && (this[p] ? this[p] = Buffer.concat([t.subarray(e), this[p]]) : this[p] = t.subarray(e));
  }
  end(t, e, i) {
    return typeof t == "function" && (i = t, e = void 0, t = void 0), typeof e == "function" && (i = e, e = void 0), typeof t == "string" && (t = Buffer.from(t, e)), i && this.once("finish", i), this[ut] || (this[y] ? (t && this[y].write(t), this[y].end()) : (this[dt] = true, (this.brotli === void 0 || this.zstd === void 0) && (t = t || Buffer.alloc(0)), t && this.write(t), this[$e]())), this;
  }
};
var mt = (s3) => {
  let t = s3.length - 1, e = -1;
  for (; t > -1 && s3.charAt(t) === "/"; ) e = t, t--;
  return e === -1 ? s3 : s3.slice(0, e);
};
var _n = (s3) => {
  let t = s3.onReadEntry;
  s3.onReadEntry = t ? (e) => {
    t(e), e.resume();
  } : (e) => e.resume();
};
var Yi = (s3, t) => {
  let e = new Map(t.map((n) => [mt(n), true])), i = s3.filter, r = (n, o = "") => {
    let h = o || gn(n).root || ".", a;
    if (n === h) a = false;
    else {
      let l = e.get(n);
      l !== void 0 ? a = l : a = r(bn(n), h);
    }
    return e.set(n, a), a;
  };
  s3.filter = i ? (n, o) => i(n, o) && r(mt(n)) : (n) => r(mt(n));
};
var On = (s3) => {
  let t = new st(s3), e = s3.file, i;
  try {
    i = Vt.openSync(e, "r");
    let r = Vt.fstatSync(i), n = s3.maxReadSize || 16 * 1024 * 1024;
    if (r.size < n) {
      let o = Buffer.allocUnsafe(r.size), h = Vt.readSync(i, o, 0, r.size, 0);
      t.end(h === o.byteLength ? o : o.subarray(0, h));
    } else {
      let o = 0, h = Buffer.allocUnsafe(n);
      for (; o < r.size; ) {
        let a = Vt.readSync(i, h, 0, n, o);
        if (a === 0) break;
        o += a, t.write(h.subarray(0, a));
      }
      t.end();
    }
  } finally {
    if (typeof i == "number") try {
      Vt.closeSync(i);
    } catch {
    }
  }
};
var Tn = (s3, t) => {
  let e = new st(s3), i = s3.maxReadSize || 16 * 1024 * 1024, r = s3.file;
  return new Promise((o, h) => {
    e.on("error", h), e.on("end", o), Vt.stat(r, (a, l) => {
      if (a) h(a);
      else {
        let c = new gt(r, { readSize: i, size: l.size });
        c.on("error", h), c.pipe(e);
      }
    });
  });
};
var It = K(On, Tn, (s3) => new st(s3), (s3) => new st(s3), (s3, t) => {
  t?.length && Yi(s3, t), s3.noResume || _n(s3);
});
var Ki = (s3, t, e) => (s3 &= 4095, e && (s3 = (s3 | 384) & -19), t && (s3 & 256 && (s3 |= 64), s3 & 32 && (s3 |= 8), s3 & 4 && (s3 |= 1)), s3);
var { isAbsolute: Ln, parse: Ks } = xn;
var ce = (s3) => {
  let t = "", e = Ks(s3);
  for (; Ln(s3) || e.root; ) {
    let i = s3.charAt(0) === "/" && s3.slice(0, 4) !== "//?/" ? "/" : e.root;
    s3 = s3.slice(i.length), t += i, e = Ks(s3);
  }
  return [t, s3];
};
var Qe = ["|", "<", ">", "?", ":"];
var Vi = Qe.map((s3) => String.fromCharCode(61440 + s3.charCodeAt(0)));
var Nn = new Map(Qe.map((s3, t) => [s3, Vi[t]]));
var Dn = new Map(Vi.map((s3, t) => [s3, Qe[t]]));
var $i = (s3) => Qe.reduce((t, e) => t.split(e).join(Nn.get(e)), s3);
var Vs = (s3) => Vi.reduce((t, e) => t.split(e).join(Dn.get(e)), s3);
var tr = (s3, t) => t ? (s3 = f(s3).replace(/^\.(\/|$)/, ""), mt(t) + "/" + s3) : f(s3);
var An = 16 * 1024 * 1024;
var qs = Symbol("process");
var js = Symbol("file");
var Qs = Symbol("directory");
var qi = Symbol("symlink");
var Js = Symbol("hardlink");
var fe = Symbol("header");
var Je = Symbol("read");
var ji = Symbol("lstat");
var ti = Symbol("onlstat");
var Qi = Symbol("onread");
var Ji = Symbol("onreadlink");
var ts = Symbol("openfile");
var es = Symbol("onopenfile");
var pt = Symbol("close");
var ei = Symbol("mode");
var is = Symbol("awaitDrain");
var Xi = Symbol("ondrain");
var X = Symbol("prefix");
var de = class extends A {
  path;
  portable;
  myuid = process.getuid && process.getuid() || 0;
  myuser = process.env.USER || "";
  maxReadSize;
  linkCache;
  statCache;
  preservePaths;
  cwd;
  strict;
  mtime;
  noPax;
  noMtime;
  prefix;
  fd;
  blockLen = 0;
  blockRemain = 0;
  buf;
  pos = 0;
  remain = 0;
  length = 0;
  offset = 0;
  win32;
  absolute;
  header;
  type;
  linkpath;
  stat;
  onWriteEntry;
  #t = false;
  constructor(t, e = {}) {
    let i = re(e);
    super(), this.path = f(t), this.portable = !!i.portable, this.maxReadSize = i.maxReadSize || An, this.linkCache = i.linkCache || /* @__PURE__ */ new Map(), this.statCache = i.statCache || /* @__PURE__ */ new Map(), this.preservePaths = !!i.preservePaths, this.cwd = f(i.cwd || process.cwd()), this.strict = !!i.strict, this.noPax = !!i.noPax, this.noMtime = !!i.noMtime, this.mtime = i.mtime, this.prefix = i.prefix ? f(i.prefix) : void 0, this.onWriteEntry = i.onWriteEntry, typeof i.onwarn == "function" && this.on("warn", i.onwarn);
    let r = false;
    if (!this.preservePaths) {
      let [o, h] = ce(this.path);
      o && typeof h == "string" && (this.path = h, r = o);
    }
    this.win32 = !!i.win32 || process.platform === "win32", this.win32 && (this.path = Vs(this.path.replace(/\\/g, "/")), t = t.replace(/\\/g, "/")), this.absolute = f(i.absolute || Xs.resolve(this.cwd, t)), this.path === "" && (this.path = "./"), r && this.warn("TAR_ENTRY_INFO", `stripping ${r} from absolute path`, { entry: this, path: r + this.path });
    let n = this.statCache.get(this.absolute);
    n ? this[ti](n) : this[ji]();
  }
  warn(t, e, i = {}) {
    return Lt(this, t, e, i);
  }
  emit(t, ...e) {
    return t === "error" && (this.#t = true), super.emit(t, ...e);
  }
  [ji]() {
    $.lstat(this.absolute, (t, e) => {
      if (t) return this.emit("error", t);
      this[ti](e);
    });
  }
  [ti](t) {
    this.statCache.set(this.absolute, t), this.stat = t, t.isFile() || (t.size = 0), this.type = In(t), this.emit("stat", t), this[qs]();
  }
  [qs]() {
    switch (this.type) {
      case "File":
        return this[js]();
      case "Directory":
        return this[Qs]();
      case "SymbolicLink":
        return this[qi]();
      default:
        return this.end();
    }
  }
  [ei](t) {
    return Ki(t, this.type === "Directory", this.portable);
  }
  [X](t) {
    return tr(t, this.prefix);
  }
  [fe]() {
    if (!this.stat) throw new Error("cannot write header before stat");
    this.type === "Directory" && this.portable && (this.noMtime = true), this.onWriteEntry?.(this), this.header = new F({ path: this[X](this.path), linkpath: this.type === "Link" && this.linkpath !== void 0 ? this[X](this.linkpath) : this.linkpath, mode: this[ei](this.stat.mode), uid: this.portable ? void 0 : this.stat.uid, gid: this.portable ? void 0 : this.stat.gid, size: this.stat.size, mtime: this.noMtime ? void 0 : this.mtime || this.stat.mtime, type: this.type === "Unsupported" ? void 0 : this.type, uname: this.portable ? void 0 : this.stat.uid === this.myuid ? this.myuser : "", atime: this.portable ? void 0 : this.stat.atime, ctime: this.portable ? void 0 : this.stat.ctime }), this.header.encode() && !this.noPax && super.write(new ct({ atime: this.portable ? void 0 : this.header.atime, ctime: this.portable ? void 0 : this.header.ctime, gid: this.portable ? void 0 : this.header.gid, mtime: this.noMtime ? void 0 : this.mtime || this.header.mtime, path: this[X](this.path), linkpath: this.type === "Link" && this.linkpath !== void 0 ? this[X](this.linkpath) : this.linkpath, size: this.header.size, uid: this.portable ? void 0 : this.header.uid, uname: this.portable ? void 0 : this.header.uname, dev: this.portable ? void 0 : this.stat.dev, ino: this.portable ? void 0 : this.stat.ino, nlink: this.portable ? void 0 : this.stat.nlink }).encode());
    let t = this.header?.block;
    if (!t) throw new Error("failed to encode header");
    super.write(t);
  }
  [Qs]() {
    if (!this.stat) throw new Error("cannot create directory entry without stat");
    this.path.slice(-1) !== "/" && (this.path += "/"), this.stat.size = 0, this[fe](), this.end();
  }
  [qi]() {
    $.readlink(this.absolute, (t, e) => {
      if (t) return this.emit("error", t);
      this[Ji](e);
    });
  }
  [Ji](t) {
    this.linkpath = f(t), this[fe](), this.end();
  }
  [Js](t) {
    if (!this.stat) throw new Error("cannot create link entry without stat");
    this.type = "Link", this.linkpath = f(Xs.relative(this.cwd, t)), this.stat.size = 0, this[fe](), this.end();
  }
  [js]() {
    if (!this.stat) throw new Error("cannot create file entry without stat");
    if (this.stat.nlink > 1) {
      let t = `${this.stat.dev}:${this.stat.ino}`, e = this.linkCache.get(t);
      if (e?.indexOf(this.cwd) === 0) return this[Js](e);
      this.linkCache.set(t, this.absolute);
    }
    if (this[fe](), this.stat.size === 0) return this.end();
    this[ts]();
  }
  [ts]() {
    $.open(this.absolute, "r", (t, e) => {
      if (t) return this.emit("error", t);
      this[es](e);
    });
  }
  [es](t) {
    if (this.fd = t, this.#t) return this[pt]();
    if (!this.stat) throw new Error("should stat before calling onopenfile");
    this.blockLen = 512 * Math.ceil(this.stat.size / 512), this.blockRemain = this.blockLen;
    let e = Math.min(this.blockLen, this.maxReadSize);
    this.buf = Buffer.allocUnsafe(e), this.offset = 0, this.pos = 0, this.remain = this.stat.size, this.length = this.buf.length, this[Je]();
  }
  [Je]() {
    let { fd: t, buf: e, offset: i, length: r, pos: n } = this;
    if (t === void 0 || e === void 0) throw new Error("cannot read file without first opening");
    $.read(t, e, i, r, n, (o, h) => {
      if (o) return this[pt](() => this.emit("error", o));
      this[Qi](h);
    });
  }
  [pt](t = () => {
  }) {
    this.fd !== void 0 && $.close(this.fd, t);
  }
  [Qi](t) {
    if (t <= 0 && this.remain > 0) {
      let r = Object.assign(new Error("encountered unexpected EOF"), { path: this.absolute, syscall: "read", code: "EOF" });
      return this[pt](() => this.emit("error", r));
    }
    if (t > this.remain) {
      let r = Object.assign(new Error("did not encounter expected EOF"), { path: this.absolute, syscall: "read", code: "EOF" });
      return this[pt](() => this.emit("error", r));
    }
    if (!this.buf) throw new Error("should have created buffer prior to reading");
    if (t === this.remain) for (let r = t; r < this.length && t < this.blockRemain; r++) this.buf[r + this.offset] = 0, t++, this.remain++;
    let e = this.offset === 0 && t === this.buf.length ? this.buf : this.buf.subarray(this.offset, this.offset + t);
    this.write(e) ? this[Xi]() : this[is](() => this[Xi]());
  }
  [is](t) {
    this.once("drain", t);
  }
  write(t, e, i) {
    if (typeof e == "function" && (i = e, e = void 0), typeof t == "string" && (t = Buffer.from(t, typeof e == "string" ? e : "utf8")), this.blockRemain < t.length) {
      let r = Object.assign(new Error("writing more data than expected"), { path: this.absolute });
      return this.emit("error", r);
    }
    return this.remain -= t.length, this.blockRemain -= t.length, this.pos += t.length, this.offset += t.length, super.write(t, null, i);
  }
  [Xi]() {
    if (!this.remain) return this.blockRemain && super.write(Buffer.alloc(this.blockRemain)), this[pt]((t) => t ? this.emit("error", t) : this.end());
    if (!this.buf) throw new Error("buffer lost somehow in ONDRAIN");
    this.offset >= this.length && (this.buf = Buffer.allocUnsafe(Math.min(this.blockRemain, this.buf.length)), this.offset = 0), this.length = this.buf.length - this.offset, this[Je]();
  }
};
var ii = class extends de {
  sync = true;
  [ji]() {
    this[ti]($.lstatSync(this.absolute));
  }
  [qi]() {
    this[Ji]($.readlinkSync(this.absolute));
  }
  [ts]() {
    this[es]($.openSync(this.absolute, "r"));
  }
  [Je]() {
    let t = true;
    try {
      let { fd: e, buf: i, offset: r, length: n, pos: o } = this;
      if (e === void 0 || i === void 0) throw new Error("fd and buf must be set in READ method");
      let h = $.readSync(e, i, r, n, o);
      this[Qi](h), t = false;
    } finally {
      if (t) try {
        this[pt](() => {
        });
      } catch {
      }
    }
  }
  [is](t) {
    t();
  }
  [pt](t = () => {
  }) {
    this.fd !== void 0 && $.closeSync(this.fd), t();
  }
};
var si = class extends A {
  blockLen = 0;
  blockRemain = 0;
  buf = 0;
  pos = 0;
  remain = 0;
  length = 0;
  preservePaths;
  portable;
  strict;
  noPax;
  noMtime;
  readEntry;
  type;
  prefix;
  path;
  mode;
  uid;
  gid;
  uname;
  gname;
  header;
  mtime;
  atime;
  ctime;
  linkpath;
  size;
  onWriteEntry;
  warn(t, e, i = {}) {
    return Lt(this, t, e, i);
  }
  constructor(t, e = {}) {
    let i = re(e);
    super(), this.preservePaths = !!i.preservePaths, this.portable = !!i.portable, this.strict = !!i.strict, this.noPax = !!i.noPax, this.noMtime = !!i.noMtime, this.onWriteEntry = i.onWriteEntry, this.readEntry = t;
    let { type: r } = t;
    if (r === "Unsupported") throw new Error("writing entry that should be ignored");
    this.type = r, this.type === "Directory" && this.portable && (this.noMtime = true), this.prefix = i.prefix, this.path = f(t.path), this.mode = t.mode !== void 0 ? this[ei](t.mode) : void 0, this.uid = this.portable ? void 0 : t.uid, this.gid = this.portable ? void 0 : t.gid, this.uname = this.portable ? void 0 : t.uname, this.gname = this.portable ? void 0 : t.gname, this.size = t.size, this.mtime = this.noMtime ? void 0 : i.mtime || t.mtime, this.atime = this.portable ? void 0 : t.atime, this.ctime = this.portable ? void 0 : t.ctime, this.linkpath = t.linkpath !== void 0 ? f(t.linkpath) : void 0, typeof i.onwarn == "function" && this.on("warn", i.onwarn);
    let n = false;
    if (!this.preservePaths) {
      let [h, a] = ce(this.path);
      h && typeof a == "string" && (this.path = a, n = h);
    }
    this.remain = t.size, this.blockRemain = t.startBlockSize, this.onWriteEntry?.(this), this.header = new F({ path: this[X](this.path), linkpath: this.type === "Link" && this.linkpath !== void 0 ? this[X](this.linkpath) : this.linkpath, mode: this.mode, uid: this.portable ? void 0 : this.uid, gid: this.portable ? void 0 : this.gid, size: this.size, mtime: this.noMtime ? void 0 : this.mtime, type: this.type, uname: this.portable ? void 0 : this.uname, atime: this.portable ? void 0 : this.atime, ctime: this.portable ? void 0 : this.ctime }), n && this.warn("TAR_ENTRY_INFO", `stripping ${n} from absolute path`, { entry: this, path: n + this.path }), this.header.encode() && !this.noPax && super.write(new ct({ atime: this.portable ? void 0 : this.atime, ctime: this.portable ? void 0 : this.ctime, gid: this.portable ? void 0 : this.gid, mtime: this.noMtime ? void 0 : this.mtime, path: this[X](this.path), linkpath: this.type === "Link" && this.linkpath !== void 0 ? this[X](this.linkpath) : this.linkpath, size: this.size, uid: this.portable ? void 0 : this.uid, uname: this.portable ? void 0 : this.uname, dev: this.portable ? void 0 : this.readEntry.dev, ino: this.portable ? void 0 : this.readEntry.ino, nlink: this.portable ? void 0 : this.readEntry.nlink }).encode());
    let o = this.header?.block;
    if (!o) throw new Error("failed to encode header");
    super.write(o), t.pipe(this);
  }
  [X](t) {
    return tr(t, this.prefix);
  }
  [ei](t) {
    return Ki(t, this.type === "Directory", this.portable);
  }
  write(t, e, i) {
    typeof e == "function" && (i = e, e = void 0), typeof t == "string" && (t = Buffer.from(t, typeof e == "string" ? e : "utf8"));
    let r = t.length;
    if (r > this.blockRemain) throw new Error("writing more to entry than is appropriate");
    return this.blockRemain -= r, super.write(t, i);
  }
  end(t, e, i) {
    return this.blockRemain && super.write(Buffer.alloc(this.blockRemain)), typeof t == "function" && (i = t, e = void 0, t = void 0), typeof e == "function" && (i = e, e = void 0), typeof t == "string" && (t = Buffer.from(t, e ?? "utf8")), i && this.once("finish", i), t ? super.end(t, i) : super.end(i), this;
  }
};
var In = (s3) => s3.isFile() ? "File" : s3.isDirectory() ? "Directory" : s3.isSymbolicLink() ? "SymbolicLink" : "Unsupported";
var ri = class s2 {
  tail;
  head;
  length = 0;
  static create(t = []) {
    return new s2(t);
  }
  constructor(t = []) {
    for (let e of t) this.push(e);
  }
  *[Symbol.iterator]() {
    for (let t = this.head; t; t = t.next) yield t.value;
  }
  removeNode(t) {
    if (t.list !== this) throw new Error("removing node which does not belong to this list");
    let e = t.next, i = t.prev;
    return e && (e.prev = i), i && (i.next = e), t === this.head && (this.head = e), t === this.tail && (this.tail = i), this.length--, t.next = void 0, t.prev = void 0, t.list = void 0, e;
  }
  unshiftNode(t) {
    if (t === this.head) return;
    t.list && t.list.removeNode(t);
    let e = this.head;
    t.list = this, t.next = e, e && (e.prev = t), this.head = t, this.tail || (this.tail = t), this.length++;
  }
  pushNode(t) {
    if (t === this.tail) return;
    t.list && t.list.removeNode(t);
    let e = this.tail;
    t.list = this, t.prev = e, e && (e.next = t), this.tail = t, this.head || (this.head = t), this.length++;
  }
  push(...t) {
    for (let e = 0, i = t.length; e < i; e++) Fn(this, t[e]);
    return this.length;
  }
  unshift(...t) {
    for (var e = 0, i = t.length; e < i; e++) kn(this, t[e]);
    return this.length;
  }
  pop() {
    if (!this.tail) return;
    let t = this.tail.value, e = this.tail;
    return this.tail = this.tail.prev, this.tail ? this.tail.next = void 0 : this.head = void 0, e.list = void 0, this.length--, t;
  }
  shift() {
    if (!this.head) return;
    let t = this.head.value, e = this.head;
    return this.head = this.head.next, this.head ? this.head.prev = void 0 : this.tail = void 0, e.list = void 0, this.length--, t;
  }
  forEach(t, e) {
    e = e || this;
    for (let i = this.head, r = 0; i; r++) t.call(e, i.value, r, this), i = i.next;
  }
  forEachReverse(t, e) {
    e = e || this;
    for (let i = this.tail, r = this.length - 1; i; r--) t.call(e, i.value, r, this), i = i.prev;
  }
  get(t) {
    let e = 0, i = this.head;
    for (; i && e < t; e++) i = i.next;
    if (e === t && i) return i.value;
  }
  getReverse(t) {
    let e = 0, i = this.tail;
    for (; i && e < t; e++) i = i.prev;
    if (e === t && i) return i.value;
  }
  map(t, e) {
    e = e || this;
    let i = new s2();
    for (let r = this.head; r; ) i.push(t.call(e, r.value, this)), r = r.next;
    return i;
  }
  mapReverse(t, e) {
    e = e || this;
    var i = new s2();
    for (let r = this.tail; r; ) i.push(t.call(e, r.value, this)), r = r.prev;
    return i;
  }
  reduce(t, e) {
    let i, r = this.head;
    if (arguments.length > 1) i = e;
    else if (this.head) r = this.head.next, i = this.head.value;
    else throw new TypeError("Reduce of empty list with no initial value");
    for (var n = 0; r; n++) i = t(i, r.value, n), r = r.next;
    return i;
  }
  reduceReverse(t, e) {
    let i, r = this.tail;
    if (arguments.length > 1) i = e;
    else if (this.tail) r = this.tail.prev, i = this.tail.value;
    else throw new TypeError("Reduce of empty list with no initial value");
    for (let n = this.length - 1; r; n--) i = t(i, r.value, n), r = r.prev;
    return i;
  }
  toArray() {
    let t = new Array(this.length);
    for (let e = 0, i = this.head; i; e++) t[e] = i.value, i = i.next;
    return t;
  }
  toArrayReverse() {
    let t = new Array(this.length);
    for (let e = 0, i = this.tail; i; e++) t[e] = i.value, i = i.prev;
    return t;
  }
  slice(t = 0, e = this.length) {
    e < 0 && (e += this.length), t < 0 && (t += this.length);
    let i = new s2();
    if (e < t || e < 0) return i;
    t < 0 && (t = 0), e > this.length && (e = this.length);
    let r = this.head, n = 0;
    for (n = 0; r && n < t; n++) r = r.next;
    for (; r && n < e; n++, r = r.next) i.push(r.value);
    return i;
  }
  sliceReverse(t = 0, e = this.length) {
    e < 0 && (e += this.length), t < 0 && (t += this.length);
    let i = new s2();
    if (e < t || e < 0) return i;
    t < 0 && (t = 0), e > this.length && (e = this.length);
    let r = this.length, n = this.tail;
    for (; n && r > e; r--) n = n.prev;
    for (; n && r > t; r--, n = n.prev) i.push(n.value);
    return i;
  }
  splice(t, e = 0, ...i) {
    t > this.length && (t = this.length - 1), t < 0 && (t = this.length + t);
    let r = this.head;
    for (let o = 0; r && o < t; o++) r = r.next;
    let n = [];
    for (let o = 0; r && o < e; o++) n.push(r.value), r = this.removeNode(r);
    r ? r !== this.tail && (r = r.prev) : r = this.tail;
    for (let o of i) r = Cn(this, r, o);
    return n;
  }
  reverse() {
    let t = this.head, e = this.tail;
    for (let i = t; i; i = i.prev) {
      let r = i.prev;
      i.prev = i.next, i.next = r;
    }
    return this.head = e, this.tail = t, this;
  }
};
function Cn(s3, t, e) {
  let i = t, r = t ? t.next : s3.head, n = new ue(e, i, r, s3);
  return n.next === void 0 && (s3.tail = n), n.prev === void 0 && (s3.head = n), s3.length++, n;
}
function Fn(s3, t) {
  s3.tail = new ue(t, s3.tail, void 0, s3), s3.head || (s3.head = s3.tail), s3.length++;
}
function kn(s3, t) {
  s3.head = new ue(t, void 0, s3.head, s3), s3.tail || (s3.tail = s3.head), s3.length++;
}
var ue = class {
  list;
  next;
  prev;
  value;
  constructor(t, e, i, r) {
    this.list = r, this.value = t, e ? (e.next = this, this.prev = e) : this.prev = void 0, i ? (i.prev = this, this.next = i) : this.next = void 0;
  }
};
var fi = class {
  path;
  absolute;
  entry;
  stat;
  readdir;
  pending = false;
  ignore = false;
  piped = false;
  constructor(t, e) {
    this.path = t || "./", this.absolute = e;
  }
};
var er = Buffer.alloc(1024);
var ni = Symbol("onStat");
var me = Symbol("ended");
var W = Symbol("queue");
var Ct = Symbol("current");
var Ft = Symbol("process");
var pe = Symbol("processing");
var ss = Symbol("processJob");
var G = Symbol("jobs");
var rs = Symbol("jobDone");
var oi = Symbol("addFSEntry");
var ir = Symbol("addTarEntry");
var hs = Symbol("stat");
var as = Symbol("readdir");
var hi = Symbol("onreaddir");
var ai = Symbol("pipe");
var sr = Symbol("entry");
var ns = Symbol("entryOpt");
var li = Symbol("writeEntryClass");
var nr = Symbol("write");
var os = Symbol("ondrain");
var Et = class extends A {
  sync = false;
  opt;
  cwd;
  maxReadSize;
  preservePaths;
  strict;
  noPax;
  prefix;
  linkCache;
  statCache;
  file;
  portable;
  zip;
  readdirCache;
  noDirRecurse;
  follow;
  noMtime;
  mtime;
  filter;
  jobs;
  [li];
  onWriteEntry;
  [W];
  [G] = 0;
  [pe] = false;
  [me] = false;
  constructor(t = {}) {
    if (super(), this.opt = t, this.file = t.file || "", this.cwd = t.cwd || process.cwd(), this.maxReadSize = t.maxReadSize, this.preservePaths = !!t.preservePaths, this.strict = !!t.strict, this.noPax = !!t.noPax, this.prefix = f(t.prefix || ""), this.linkCache = t.linkCache || /* @__PURE__ */ new Map(), this.statCache = t.statCache || /* @__PURE__ */ new Map(), this.readdirCache = t.readdirCache || /* @__PURE__ */ new Map(), this.onWriteEntry = t.onWriteEntry, this[li] = de, typeof t.onwarn == "function" && this.on("warn", t.onwarn), this.portable = !!t.portable, t.gzip || t.brotli || t.zstd) {
      if ((t.gzip ? 1 : 0) + (t.brotli ? 1 : 0) + (t.zstd ? 1 : 0) > 1) throw new TypeError("gzip, brotli, zstd are mutually exclusive");
      if (t.gzip && (typeof t.gzip != "object" && (t.gzip = {}), this.portable && (t.gzip.portable = true), this.zip = new Be(t.gzip)), t.brotli && (typeof t.brotli != "object" && (t.brotli = {}), this.zip = new Ue(t.brotli)), t.zstd && (typeof t.zstd != "object" && (t.zstd = {}), this.zip = new Ge(t.zstd)), !this.zip) throw new Error("impossible");
      let e = this.zip;
      e.on("data", (i) => super.write(i)), e.on("end", () => super.end()), e.on("drain", () => this[os]()), this.on("resume", () => e.resume());
    } else this.on("drain", this[os]);
    this.noDirRecurse = !!t.noDirRecurse, this.follow = !!t.follow, this.noMtime = !!t.noMtime, t.mtime && (this.mtime = t.mtime), this.filter = typeof t.filter == "function" ? t.filter : () => true, this[W] = new ri(), this[G] = 0, this.jobs = Number(t.jobs) || 4, this[pe] = false, this[me] = false;
  }
  [nr](t) {
    return super.write(t);
  }
  add(t) {
    return this.write(t), this;
  }
  end(t, e, i) {
    return typeof t == "function" && (i = t, t = void 0), typeof e == "function" && (i = e, e = void 0), t && this.add(t), this[me] = true, this[Ft](), i && i(), this;
  }
  write(t) {
    if (this[me]) throw new Error("write after end");
    return t instanceof Yt ? this[ir](t) : this[oi](t), this.flowing;
  }
  [ir](t) {
    let e = f(rr.resolve(this.cwd, t.path));
    if (!this.filter(t.path, t)) t.resume();
    else {
      let i = new fi(t.path, e);
      i.entry = new si(t, this[ns](i)), i.entry.on("end", () => this[rs](i)), this[G] += 1, this[W].push(i);
    }
    this[Ft]();
  }
  [oi](t) {
    let e = f(rr.resolve(this.cwd, t));
    this[W].push(new fi(t, e)), this[Ft]();
  }
  [hs](t) {
    t.pending = true, this[G] += 1;
    let e = this.follow ? "stat" : "lstat";
    ci[e](t.absolute, (i, r) => {
      t.pending = false, this[G] -= 1, i ? this.emit("error", i) : this[ni](t, r);
    });
  }
  [ni](t, e) {
    this.statCache.set(t.absolute, e), t.stat = e, this.filter(t.path, e) ? e.isFile() && e.nlink > 1 && t === this[Ct] && !this.linkCache.get(`${e.dev}:${e.ino}`) && !this.sync && this[ss](t) : t.ignore = true, this[Ft]();
  }
  [as](t) {
    t.pending = true, this[G] += 1, ci.readdir(t.absolute, (e, i) => {
      if (t.pending = false, this[G] -= 1, e) return this.emit("error", e);
      this[hi](t, i);
    });
  }
  [hi](t, e) {
    this.readdirCache.set(t.absolute, e), t.readdir = e, this[Ft]();
  }
  [Ft]() {
    if (!this[pe]) {
      this[pe] = true;
      for (let t = this[W].head; t && this[G] < this.jobs; t = t.next) if (this[ss](t.value), t.value.ignore) {
        let e = t.next;
        this[W].removeNode(t), t.next = e;
      }
      this[pe] = false, this[me] && !this[W].length && this[G] === 0 && (this.zip ? this.zip.end(er) : (super.write(er), super.end()));
    }
  }
  get [Ct]() {
    return this[W] && this[W].head && this[W].head.value;
  }
  [rs](t) {
    this[W].shift(), this[G] -= 1, this[Ft]();
  }
  [ss](t) {
    if (!t.pending) {
      if (t.entry) {
        t === this[Ct] && !t.piped && this[ai](t);
        return;
      }
      if (!t.stat) {
        let e = this.statCache.get(t.absolute);
        e ? this[ni](t, e) : this[hs](t);
      }
      if (t.stat && !t.ignore) {
        if (!this.noDirRecurse && t.stat.isDirectory() && !t.readdir) {
          let e = this.readdirCache.get(t.absolute);
          if (e ? this[hi](t, e) : this[as](t), !t.readdir) return;
        }
        if (t.entry = this[sr](t), !t.entry) {
          t.ignore = true;
          return;
        }
        t === this[Ct] && !t.piped && this[ai](t);
      }
    }
  }
  [ns](t) {
    return { onwarn: (e, i, r) => this.warn(e, i, r), noPax: this.noPax, cwd: this.cwd, absolute: t.absolute, preservePaths: this.preservePaths, maxReadSize: this.maxReadSize, strict: this.strict, portable: this.portable, linkCache: this.linkCache, statCache: this.statCache, noMtime: this.noMtime, mtime: this.mtime, prefix: this.prefix, onWriteEntry: this.onWriteEntry };
  }
  [sr](t) {
    this[G] += 1;
    try {
      return new this[li](t.path, this[ns](t)).on("end", () => this[rs](t)).on("error", (i) => this.emit("error", i));
    } catch (e) {
      this.emit("error", e);
    }
  }
  [os]() {
    this[Ct] && this[Ct].entry && this[Ct].entry.resume();
  }
  [ai](t) {
    t.piped = true, t.readdir && t.readdir.forEach((r) => {
      let n = t.path, o = n === "./" ? "" : n.replace(/\/*$/, "/");
      this[oi](o + r);
    });
    let e = t.entry, i = this.zip;
    if (!e) throw new Error("cannot pipe without source");
    i ? e.on("data", (r) => {
      i.write(r) || e.pause();
    }) : e.on("data", (r) => {
      super.write(r) || e.pause();
    });
  }
  pause() {
    return this.zip && this.zip.pause(), super.pause();
  }
  warn(t, e, i = {}) {
    Lt(this, t, e, i);
  }
};
var kt = class extends Et {
  sync = true;
  constructor(t) {
    super(t), this[li] = ii;
  }
  pause() {
  }
  resume() {
  }
  [hs](t) {
    let e = this.follow ? "statSync" : "lstatSync";
    this[ni](t, ci[e](t.absolute));
  }
  [as](t) {
    this[hi](t, ci.readdirSync(t.absolute));
  }
  [ai](t) {
    let e = t.entry, i = this.zip;
    if (t.readdir && t.readdir.forEach((r) => {
      let n = t.path, o = n === "./" ? "" : n.replace(/\/*$/, "/");
      this[oi](o + r);
    }), !e) throw new Error("Cannot pipe without source");
    i ? e.on("data", (r) => {
      i.write(r);
    }) : e.on("data", (r) => {
      super[nr](r);
    });
  }
};
var vn = (s3, t) => {
  let e = new kt(s3), i = new Wt(s3.file, { mode: s3.mode || 438 });
  e.pipe(i), hr(e, t);
};
var Mn = (s3, t) => {
  let e = new Et(s3), i = new tt(s3.file, { mode: s3.mode || 438 });
  e.pipe(i);
  let r = new Promise((n, o) => {
    i.on("error", o), i.on("close", n), e.on("error", o);
  });
  return ar(e, t), r;
};
var hr = (s3, t) => {
  t.forEach((e) => {
    e.charAt(0) === "@" ? It({ file: or.resolve(s3.cwd, e.slice(1)), sync: true, noResume: true, onReadEntry: (i) => s3.add(i) }) : s3.add(e);
  }), s3.end();
};
var ar = async (s3, t) => {
  for (let e = 0; e < t.length; e++) {
    let i = String(t[e]);
    i.charAt(0) === "@" ? await It({ file: or.resolve(String(s3.cwd), i.slice(1)), noResume: true, onReadEntry: (r) => {
      s3.add(r);
    } }) : s3.add(i);
  }
  s3.end();
};
var Bn = (s3, t) => {
  let e = new kt(s3);
  return hr(e, t), e;
};
var Pn = (s3, t) => {
  let e = new Et(s3);
  return ar(e, t), e;
};
var zn = K(vn, Mn, Bn, Pn, (s3, t) => {
  if (!t?.length) throw new TypeError("no paths specified to add to archive");
});
var Un = process.env.__FAKE_PLATFORM__ || process.platform;
var Hn = Un === "win32";
var { O_CREAT: Wn, O_TRUNC: Gn, O_WRONLY: Zn } = lr.constants;
var cr = Number(process.env.__FAKE_FS_O_FILENAME__) || lr.constants.UV_FS_O_FILEMAP || 0;
var Yn = Hn && !!cr;
var Kn = 512 * 1024;
var Vn = cr | Gn | Wn | Zn;
var ls = Yn ? (s3) => s3 < Kn ? Vn : "w" : () => "w";
var cs = (s3, t, e) => {
  try {
    return ui.lchownSync(s3, t, e);
  } catch (i) {
    if (i?.code !== "ENOENT") throw i;
  }
};
var di = (s3, t, e, i) => {
  ui.lchown(s3, t, e, (r) => {
    i(r && r?.code !== "ENOENT" ? r : null);
  });
};
var $n = (s3, t, e, i, r) => {
  if (t.isDirectory()) fs(Ee.resolve(s3, t.name), e, i, (n) => {
    if (n) return r(n);
    let o = Ee.resolve(s3, t.name);
    di(o, e, i, r);
  });
  else {
    let n = Ee.resolve(s3, t.name);
    di(n, e, i, r);
  }
};
var fs = (s3, t, e, i) => {
  ui.readdir(s3, { withFileTypes: true }, (r, n) => {
    if (r) {
      if (r.code === "ENOENT") return i();
      if (r.code !== "ENOTDIR" && r.code !== "ENOTSUP") return i(r);
    }
    if (r || !n.length) return di(s3, t, e, i);
    let o = n.length, h = null, a = (l) => {
      if (!h) {
        if (l) return i(h = l);
        if (--o === 0) return di(s3, t, e, i);
      }
    };
    for (let l of n) $n(s3, l, t, e, a);
  });
};
var Xn = (s3, t, e, i) => {
  t.isDirectory() && ds(Ee.resolve(s3, t.name), e, i), cs(Ee.resolve(s3, t.name), e, i);
};
var ds = (s3, t, e) => {
  let i;
  try {
    i = ui.readdirSync(s3, { withFileTypes: true });
  } catch (r) {
    let n = r;
    if (n?.code === "ENOENT") return;
    if (n?.code === "ENOTDIR" || n?.code === "ENOTSUP") return cs(s3, t, e);
    throw n;
  }
  for (let r of i) Xn(s3, r, t, e);
  return cs(s3, t, e);
};
var we = class extends Error {
  path;
  code;
  syscall = "chdir";
  constructor(t, e) {
    super(`${e}: Cannot cd into '${t}'`), this.path = t, this.code = e;
  }
  get name() {
    return "CwdError";
  }
};
var wt = class extends Error {
  path;
  symlink;
  syscall = "symlink";
  code = "TAR_SYMLINK_ERROR";
  constructor(t, e) {
    super("TAR_SYMLINK_ERROR: Cannot extract through symbolic link"), this.symlink = t, this.path = e;
  }
  get name() {
    return "SymlinkError";
  }
};
var jn = (s3, t) => {
  k.stat(s3, (e, i) => {
    (e || !i.isDirectory()) && (e = new we(s3, e?.code || "ENOTDIR")), t(e);
  });
};
var fr = (s3, t, e) => {
  s3 = f(s3);
  let i = t.umask ?? 18, r = t.mode | 448, n = (r & i) !== 0, o = t.uid, h = t.gid, a = typeof o == "number" && typeof h == "number" && (o !== t.processUid || h !== t.processGid), l = t.preserve, c = t.unlink, d = f(t.cwd), S = (E, x) => {
    E ? e(E) : x && a ? fs(x, o, h, (_s) => S(_s)) : n ? k.chmod(s3, r, e) : e();
  };
  if (s3 === d) return jn(s3, S);
  if (l) return qn.mkdir(s3, { mode: r, recursive: true }).then((E) => S(null, E ?? void 0), S);
  let N = f(mi.relative(d, s3)).split("/");
  us(d, N, r, c, d, void 0, S);
};
var us = (s3, t, e, i, r, n, o) => {
  if (!t.length) return o(null, n);
  let h = t.shift(), a = f(mi.resolve(s3 + "/" + h));
  k.mkdir(a, e, dr(a, t, e, i, r, n, o));
};
var dr = (s3, t, e, i, r, n, o) => (h) => {
  h ? k.lstat(s3, (a, l) => {
    if (a) a.path = a.path && f(a.path), o(a);
    else if (l.isDirectory()) us(s3, t, e, i, r, n, o);
    else if (i) k.unlink(s3, (c) => {
      if (c) return o(c);
      k.mkdir(s3, e, dr(s3, t, e, i, r, n, o));
    });
    else {
      if (l.isSymbolicLink()) return o(new wt(s3, s3 + "/" + t.join("/")));
      o(h);
    }
  }) : (n = n || s3, us(s3, t, e, i, r, n, o));
};
var Qn = (s3) => {
  let t = false, e;
  try {
    t = k.statSync(s3).isDirectory();
  } catch (i) {
    e = i?.code;
  } finally {
    if (!t) throw new we(s3, e ?? "ENOTDIR");
  }
};
var ur = (s3, t) => {
  s3 = f(s3);
  let e = t.umask ?? 18, i = t.mode | 448, r = (i & e) !== 0, n = t.uid, o = t.gid, h = typeof n == "number" && typeof o == "number" && (n !== t.processUid || o !== t.processGid), a = t.preserve, l = t.unlink, c = f(t.cwd), d = (E) => {
    E && h && ds(E, n, o), r && k.chmodSync(s3, i);
  };
  if (s3 === c) return Qn(c), d();
  if (a) return d(k.mkdirSync(s3, { mode: i, recursive: true }) ?? void 0);
  let T = f(mi.relative(c, s3)).split("/"), N;
  for (let E = T.shift(), x = c; E && (x += "/" + E); E = T.shift()) {
    x = f(mi.resolve(x));
    try {
      k.mkdirSync(x, i), N = N || x;
    } catch {
      let Os = k.lstatSync(x);
      if (Os.isDirectory()) continue;
      if (l) {
        k.unlinkSync(x), k.mkdirSync(x, i), N = N || x;
        continue;
      } else if (Os.isSymbolicLink()) return new wt(x, x + "/" + T.join("/"));
    }
  }
  return d(N);
};
var ms = /* @__PURE__ */ Object.create(null);
var mr = 1e4;
var $t = /* @__PURE__ */ new Set();
var pr = (s3) => {
  $t.has(s3) ? $t.delete(s3) : ms[s3] = s3.normalize("NFD").toLocaleLowerCase("en").toLocaleUpperCase("en"), $t.add(s3);
  let t = ms[s3], e = $t.size - mr;
  if (e > mr / 10) {
    for (let i of $t) if ($t.delete(i), delete ms[i], --e <= 0) break;
  }
  return t;
};
var Jn = process.env.TESTING_TAR_FAKE_PLATFORM || process.platform;
var to = Jn === "win32";
var eo = (s3) => s3.split("/").slice(0, -1).reduce((e, i) => {
  let r = e[e.length - 1];
  return r !== void 0 && (i = Er(r, i)), e.push(i || "/"), e;
}, []);
var pi = class {
  #t = /* @__PURE__ */ new Map();
  #i = /* @__PURE__ */ new Map();
  #s = /* @__PURE__ */ new Set();
  reserve(t, e) {
    t = to ? ["win32 parallelization disabled"] : t.map((r) => mt(Er(pr(r))));
    let i = new Set(t.map((r) => eo(r)).reduce((r, n) => r.concat(n)));
    this.#i.set(e, { dirs: i, paths: t });
    for (let r of t) {
      let n = this.#t.get(r);
      n ? n.push(e) : this.#t.set(r, [e]);
    }
    for (let r of i) {
      let n = this.#t.get(r);
      if (!n) this.#t.set(r, [/* @__PURE__ */ new Set([e])]);
      else {
        let o = n[n.length - 1];
        o instanceof Set ? o.add(e) : n.push(/* @__PURE__ */ new Set([e]));
      }
    }
    return this.#r(e);
  }
  #n(t) {
    let e = this.#i.get(t);
    if (!e) throw new Error("function does not have any path reservations");
    return { paths: e.paths.map((i) => this.#t.get(i)), dirs: [...e.dirs].map((i) => this.#t.get(i)) };
  }
  check(t) {
    let { paths: e, dirs: i } = this.#n(t);
    return e.every((r) => r && r[0] === t) && i.every((r) => r && r[0] instanceof Set && r[0].has(t));
  }
  #r(t) {
    return this.#s.has(t) || !this.check(t) ? false : (this.#s.add(t), t(() => this.#e(t)), true);
  }
  #e(t) {
    if (!this.#s.has(t)) return false;
    let e = this.#i.get(t);
    if (!e) throw new Error("invalid reservation");
    let { paths: i, dirs: r } = e, n = /* @__PURE__ */ new Set();
    for (let o of i) {
      let h = this.#t.get(o);
      if (!h || h?.[0] !== t) continue;
      let a = h[1];
      if (!a) {
        this.#t.delete(o);
        continue;
      }
      if (h.shift(), typeof a == "function") n.add(a);
      else for (let l of a) n.add(l);
    }
    for (let o of r) {
      let h = this.#t.get(o), a = h?.[0];
      if (!(!h || !(a instanceof Set))) if (a.size === 1 && h.length === 1) {
        this.#t.delete(o);
        continue;
      } else if (a.size === 1) {
        h.shift();
        let l = h[0];
        typeof l == "function" && n.add(l);
      } else a.delete(t);
    }
    return this.#s.delete(t), n.forEach((o) => this.#r(o)), true;
  }
};
var wr = () => process.umask();
var Sr = Symbol("onEntry");
var Ss = Symbol("checkFs");
var yr = Symbol("checkFs2");
var ys = Symbol("isReusable");
var P = Symbol("makeFs");
var Rs = Symbol("file");
var bs = Symbol("directory");
var wi = Symbol("link");
var Rr = Symbol("symlink");
var br = Symbol("hardlink");
var ye = Symbol("ensureNoSymlink");
var gr = Symbol("unsupported");
var _r = Symbol("checkPath");
var ps = Symbol("stripAbsolutePath");
var St = Symbol("mkdir");
var O = Symbol("onError");
var Ei = Symbol("pending");
var Or = Symbol("pend");
var Xt = Symbol("unpend");
var Es = Symbol("ended");
var ws = Symbol("maybeClose");
var gs = Symbol("skip");
var Re = Symbol("doChown");
var be = Symbol("uid");
var ge = Symbol("gid");
var _e = Symbol("checkedCwd");
var so = process.env.TESTING_TAR_FAKE_PLATFORM || process.platform;
var Oe = so === "win32";
var ro = 1024;
var no = (s3, t) => {
  if (!Oe) return u.unlink(s3, t);
  let e = s3 + ".DELETE." + xr(16).toString("hex");
  u.rename(s3, e, (i) => {
    if (i) return t(i);
    u.unlink(e, t);
  });
};
var oo = (s3) => {
  if (!Oe) return u.unlinkSync(s3);
  let t = s3 + ".DELETE." + xr(16).toString("hex");
  u.renameSync(s3, t), u.unlinkSync(t);
};
var Tr = (s3, t, e) => s3 !== void 0 && s3 === s3 >>> 0 ? s3 : t !== void 0 && t === t >>> 0 ? t : e;
var qt = class extends st {
  [Es] = false;
  [_e] = false;
  [Ei] = 0;
  reservations = new pi();
  transform;
  writable = true;
  readable = false;
  uid;
  gid;
  setOwner;
  preserveOwner;
  processGid;
  processUid;
  maxDepth;
  forceChown;
  win32;
  newer;
  keep;
  noMtime;
  preservePaths;
  unlink;
  cwd;
  strip;
  processUmask;
  umask;
  dmode;
  fmode;
  chmod;
  constructor(t = {}) {
    if (t.ondone = () => {
      this[Es] = true, this[ws]();
    }, super(t), this.transform = t.transform, this.chmod = !!t.chmod, typeof t.uid == "number" || typeof t.gid == "number") {
      if (typeof t.uid != "number" || typeof t.gid != "number") throw new TypeError("cannot set owner without number uid and gid");
      if (t.preserveOwner) throw new TypeError("cannot preserve owner in archive and also set owner explicitly");
      this.uid = t.uid, this.gid = t.gid, this.setOwner = true;
    } else this.uid = void 0, this.gid = void 0, this.setOwner = false;
    t.preserveOwner === void 0 && typeof t.uid != "number" ? this.preserveOwner = !!(process.getuid && process.getuid() === 0) : this.preserveOwner = !!t.preserveOwner, this.processUid = (this.preserveOwner || this.setOwner) && process.getuid ? process.getuid() : void 0, this.processGid = (this.preserveOwner || this.setOwner) && process.getgid ? process.getgid() : void 0, this.maxDepth = typeof t.maxDepth == "number" ? t.maxDepth : ro, this.forceChown = t.forceChown === true, this.win32 = !!t.win32 || Oe, this.newer = !!t.newer, this.keep = !!t.keep, this.noMtime = !!t.noMtime, this.preservePaths = !!t.preservePaths, this.unlink = !!t.unlink, this.cwd = f(R.resolve(t.cwd || process.cwd())), this.strip = Number(t.strip) || 0, this.processUmask = this.chmod ? typeof t.processUmask == "number" ? t.processUmask : wr() : 0, this.umask = typeof t.umask == "number" ? t.umask : this.processUmask, this.dmode = t.dmode || 511 & ~this.umask, this.fmode = t.fmode || 438 & ~this.umask, this.on("entry", (e) => this[Sr](e));
  }
  warn(t, e, i = {}) {
    return (t === "TAR_BAD_ARCHIVE" || t === "TAR_ABORT") && (i.recoverable = false), super.warn(t, e, i);
  }
  [ws]() {
    this[Es] && this[Ei] === 0 && (this.emit("prefinish"), this.emit("finish"), this.emit("end"));
  }
  [ps](t, e) {
    let i = t[e], { type: r } = t;
    if (!i || this.preservePaths) return true;
    let [n, o] = ce(i), h = o.replace(/\\/g, "/").split("/");
    if (h.includes("..") || Oe && /^[a-z]:\.\.$/i.test(h[0] ?? "")) {
      if (e === "path" || r === "Link") return this.warn("TAR_ENTRY_ERROR", `${e} contains '..'`, { entry: t, [e]: i }), false;
      {
        let a = R.posix.dirname(t.path), l = R.posix.normalize(R.posix.join(a, i));
        if (l.startsWith("../") || l === "..") return this.warn("TAR_ENTRY_ERROR", `${e} escapes extraction directory`, { entry: t, [e]: i }), false;
      }
    }
    return n && (t[e] = String(o), this.warn("TAR_ENTRY_INFO", `stripping ${n} from absolute ${e}`, { entry: t, [e]: i })), true;
  }
  [_r](t) {
    let e = f(t.path), i = e.split("/");
    if (this.strip) {
      if (i.length < this.strip) return false;
      if (t.type === "Link") {
        let r = f(String(t.linkpath)).split("/");
        if (r.length >= this.strip) t.linkpath = r.slice(this.strip).join("/");
        else return false;
      }
      i.splice(0, this.strip), t.path = i.join("/");
    }
    if (isFinite(this.maxDepth) && i.length > this.maxDepth) return this.warn("TAR_ENTRY_ERROR", "path excessively deep", { entry: t, path: e, depth: i.length, maxDepth: this.maxDepth }), false;
    if (!this[ps](t, "path") || !this[ps](t, "linkpath")) return false;
    if (R.isAbsolute(t.path) ? t.absolute = f(R.resolve(t.path)) : t.absolute = f(R.resolve(this.cwd, t.path)), !this.preservePaths && typeof t.absolute == "string" && t.absolute.indexOf(this.cwd + "/") !== 0 && t.absolute !== this.cwd) return this.warn("TAR_ENTRY_ERROR", "path escaped extraction target", { entry: t, path: f(t.path), resolvedPath: t.absolute, cwd: this.cwd }), false;
    if (t.absolute === this.cwd && t.type !== "Directory" && t.type !== "GNUDumpDir") return false;
    if (this.win32) {
      let { root: r } = R.win32.parse(String(t.absolute));
      t.absolute = r + $i(String(t.absolute).slice(r.length));
      let { root: n } = R.win32.parse(t.path);
      t.path = n + $i(t.path.slice(n.length));
    }
    return true;
  }
  [Sr](t) {
    if (!this[_r](t)) return t.resume();
    switch (io.equal(typeof t.absolute, "string"), t.type) {
      case "Directory":
      case "GNUDumpDir":
        t.mode && (t.mode = t.mode | 448);
      case "File":
      case "OldFile":
      case "ContiguousFile":
      case "Link":
      case "SymbolicLink":
        return this[Ss](t);
      default:
        return this[gr](t);
    }
  }
  [O](t, e) {
    t.name === "CwdError" ? this.emit("error", t) : (this.warn("TAR_ENTRY_ERROR", t, { entry: e }), this[Xt](), e.resume());
  }
  [St](t, e, i) {
    fr(f(t), { uid: this.uid, gid: this.gid, processUid: this.processUid, processGid: this.processGid, umask: this.processUmask, preserve: this.preservePaths, unlink: this.unlink, cwd: this.cwd, mode: e }, i);
  }
  [Re](t) {
    return this.forceChown || this.preserveOwner && (typeof t.uid == "number" && t.uid !== this.processUid || typeof t.gid == "number" && t.gid !== this.processGid) || typeof this.uid == "number" && this.uid !== this.processUid || typeof this.gid == "number" && this.gid !== this.processGid;
  }
  [be](t) {
    return Tr(this.uid, t.uid, this.processUid);
  }
  [ge](t) {
    return Tr(this.gid, t.gid, this.processGid);
  }
  [Rs](t, e) {
    let i = typeof t.mode == "number" ? t.mode & 4095 : this.fmode, r = new tt(String(t.absolute), { flags: ls(t.size), mode: i, autoClose: false });
    r.on("error", (a) => {
      r.fd && u.close(r.fd, () => {
      }), r.write = () => true, this[O](a, t), e();
    });
    let n = 1, o = (a) => {
      if (a) {
        r.fd && u.close(r.fd, () => {
        }), this[O](a, t), e();
        return;
      }
      --n === 0 && r.fd !== void 0 && u.close(r.fd, (l) => {
        l ? this[O](l, t) : this[Xt](), e();
      });
    };
    r.on("finish", () => {
      let a = String(t.absolute), l = r.fd;
      if (typeof l == "number" && t.mtime && !this.noMtime) {
        n++;
        let c = t.atime || /* @__PURE__ */ new Date(), d = t.mtime;
        u.futimes(l, c, d, (S) => S ? u.utimes(a, c, d, (T) => o(T && S)) : o());
      }
      if (typeof l == "number" && this[Re](t)) {
        n++;
        let c = this[be](t), d = this[ge](t);
        typeof c == "number" && typeof d == "number" && u.fchown(l, c, d, (S) => S ? u.chown(a, c, d, (T) => o(T && S)) : o());
      }
      o();
    });
    let h = this.transform && this.transform(t) || t;
    h !== t && (h.on("error", (a) => {
      this[O](a, t), e();
    }), t.pipe(h)), h.pipe(r);
  }
  [bs](t, e) {
    let i = typeof t.mode == "number" ? t.mode & 4095 : this.dmode;
    this[St](String(t.absolute), i, (r) => {
      if (r) {
        this[O](r, t), e();
        return;
      }
      let n = 1, o = () => {
        --n === 0 && (e(), this[Xt](), t.resume());
      };
      t.mtime && !this.noMtime && (n++, u.utimes(String(t.absolute), t.atime || /* @__PURE__ */ new Date(), t.mtime, o)), this[Re](t) && (n++, u.chown(String(t.absolute), Number(this[be](t)), Number(this[ge](t)), o)), o();
    });
  }
  [gr](t) {
    t.unsupported = true, this.warn("TAR_ENTRY_UNSUPPORTED", `unsupported entry type: ${t.type}`, { entry: t }), t.resume();
  }
  [Rr](t, e) {
    let i = f(R.relative(this.cwd, R.resolve(R.dirname(String(t.absolute)), String(t.linkpath)))).split("/");
    this[ye](t, this.cwd, i, () => this[wi](t, String(t.linkpath), "symlink", e), (r) => {
      this[O](r, t), e();
    });
  }
  [br](t, e) {
    let i = f(R.resolve(this.cwd, String(t.linkpath))), r = f(String(t.linkpath)).split("/");
    this[ye](t, this.cwd, r, () => this[wi](t, i, "link", e), (n) => {
      this[O](n, t), e();
    });
  }
  [ye](t, e, i, r, n) {
    let o = i.shift();
    if (this.preservePaths || o === void 0) return r();
    let h = R.resolve(e, o);
    u.lstat(h, (a, l) => {
      if (a) return r();
      if (l?.isSymbolicLink()) return n(new wt(h, R.resolve(h, i.join("/"))));
      this[ye](t, h, i, r, n);
    });
  }
  [Or]() {
    this[Ei]++;
  }
  [Xt]() {
    this[Ei]--, this[ws]();
  }
  [gs](t) {
    this[Xt](), t.resume();
  }
  [ys](t, e) {
    return t.type === "File" && !this.unlink && e.isFile() && e.nlink <= 1 && !Oe;
  }
  [Ss](t) {
    this[Or]();
    let e = [t.path];
    t.linkpath && e.push(t.linkpath), this.reservations.reserve(e, (i) => this[yr](t, i));
  }
  [yr](t, e) {
    let i = (h) => {
      e(h);
    }, r = () => {
      this[St](this.cwd, this.dmode, (h) => {
        if (h) {
          this[O](h, t), i();
          return;
        }
        this[_e] = true, n();
      });
    }, n = () => {
      if (t.absolute !== this.cwd) {
        let h = f(R.dirname(String(t.absolute)));
        if (h !== this.cwd) return this[St](h, this.dmode, (a) => {
          if (a) {
            this[O](a, t), i();
            return;
          }
          o();
        });
      }
      o();
    }, o = () => {
      u.lstat(String(t.absolute), (h, a) => {
        if (a && (this.keep || this.newer && a.mtime > (t.mtime ?? a.mtime))) {
          this[gs](t), i();
          return;
        }
        if (h || this[ys](t, a)) return this[P](null, t, i);
        if (a.isDirectory()) {
          if (t.type === "Directory") {
            let l = this.chmod && t.mode && (a.mode & 4095) !== t.mode, c = (d) => this[P](d ?? null, t, i);
            return l ? u.chmod(String(t.absolute), Number(t.mode), c) : c();
          }
          if (t.absolute !== this.cwd) return u.rmdir(String(t.absolute), (l) => this[P](l ?? null, t, i));
        }
        if (t.absolute === this.cwd) return this[P](null, t, i);
        no(String(t.absolute), (l) => this[P](l ?? null, t, i));
      });
    };
    this[_e] ? n() : r();
  }
  [P](t, e, i) {
    if (t) {
      this[O](t, e), i();
      return;
    }
    switch (e.type) {
      case "File":
      case "OldFile":
      case "ContiguousFile":
        return this[Rs](e, i);
      case "Link":
        return this[br](e, i);
      case "SymbolicLink":
        return this[Rr](e, i);
      case "Directory":
      case "GNUDumpDir":
        return this[bs](e, i);
    }
  }
  [wi](t, e, i, r) {
    u[i](e, String(t.absolute), (n) => {
      n ? this[O](n, t) : (this[Xt](), t.resume()), r();
    });
  }
};
var Se = (s3) => {
  try {
    return [null, s3()];
  } catch (t) {
    return [t, null];
  }
};
var Te = class extends qt {
  sync = true;
  [P](t, e) {
    return super[P](t, e, () => {
    });
  }
  [Ss](t) {
    if (!this[_e]) {
      let n = this[St](this.cwd, this.dmode);
      if (n) return this[O](n, t);
      this[_e] = true;
    }
    if (t.absolute !== this.cwd) {
      let n = f(R.dirname(String(t.absolute)));
      if (n !== this.cwd) {
        let o = this[St](n, this.dmode);
        if (o) return this[O](o, t);
      }
    }
    let [e, i] = Se(() => u.lstatSync(String(t.absolute)));
    if (i && (this.keep || this.newer && i.mtime > (t.mtime ?? i.mtime))) return this[gs](t);
    if (e || this[ys](t, i)) return this[P](null, t);
    if (i.isDirectory()) {
      if (t.type === "Directory") {
        let o = this.chmod && t.mode && (i.mode & 4095) !== t.mode, [h] = o ? Se(() => {
          u.chmodSync(String(t.absolute), Number(t.mode));
        }) : [];
        return this[P](h, t);
      }
      let [n] = Se(() => u.rmdirSync(String(t.absolute)));
      this[P](n, t);
    }
    let [r] = t.absolute === this.cwd ? [] : Se(() => oo(String(t.absolute)));
    this[P](r, t);
  }
  [Rs](t, e) {
    let i = typeof t.mode == "number" ? t.mode & 4095 : this.fmode, r = (h) => {
      let a;
      try {
        u.closeSync(n);
      } catch (l) {
        a = l;
      }
      (h || a) && this[O](h || a, t), e();
    }, n;
    try {
      n = u.openSync(String(t.absolute), ls(t.size), i);
    } catch (h) {
      return r(h);
    }
    let o = this.transform && this.transform(t) || t;
    o !== t && (o.on("error", (h) => this[O](h, t)), t.pipe(o)), o.on("data", (h) => {
      try {
        u.writeSync(n, h, 0, h.length);
      } catch (a) {
        r(a);
      }
    }), o.on("end", () => {
      let h = null;
      if (t.mtime && !this.noMtime) {
        let a = t.atime || /* @__PURE__ */ new Date(), l = t.mtime;
        try {
          u.futimesSync(n, a, l);
        } catch (c) {
          try {
            u.utimesSync(String(t.absolute), a, l);
          } catch {
            h = c;
          }
        }
      }
      if (this[Re](t)) {
        let a = this[be](t), l = this[ge](t);
        try {
          u.fchownSync(n, Number(a), Number(l));
        } catch (c) {
          try {
            u.chownSync(String(t.absolute), Number(a), Number(l));
          } catch {
            h = h || c;
          }
        }
      }
      r(h);
    });
  }
  [bs](t, e) {
    let i = typeof t.mode == "number" ? t.mode & 4095 : this.dmode, r = this[St](String(t.absolute), i);
    if (r) {
      this[O](r, t), e();
      return;
    }
    if (t.mtime && !this.noMtime) try {
      u.utimesSync(String(t.absolute), t.atime || /* @__PURE__ */ new Date(), t.mtime);
    } catch {
    }
    if (this[Re](t)) try {
      u.chownSync(String(t.absolute), Number(this[be](t)), Number(this[ge](t)));
    } catch {
    }
    e(), t.resume();
  }
  [St](t, e) {
    try {
      return ur(f(t), { uid: this.uid, gid: this.gid, processUid: this.processUid, processGid: this.processGid, umask: this.processUmask, preserve: this.preservePaths, unlink: this.unlink, cwd: this.cwd, mode: e });
    } catch (i) {
      return i;
    }
  }
  [ye](t, e, i, r, n) {
    if (this.preservePaths || !i.length) return r();
    let o = e;
    for (let h of i) {
      o = R.resolve(o, h);
      let [a, l] = Se(() => u.lstatSync(o));
      if (a) return r();
      if (l.isSymbolicLink()) return n(new wt(o, R.resolve(e, i.join("/"))));
    }
    r();
  }
  [wi](t, e, i, r) {
    let n = `${i}Sync`;
    try {
      u[n](e, String(t.absolute)), r(), t.resume();
    } catch (o) {
      return this[O](o, t);
    }
  }
};
var ho = (s3) => {
  let t = new Te(s3), e = s3.file, i = Lr.statSync(e), r = s3.maxReadSize || 16 * 1024 * 1024;
  new ve(e, { readSize: r, size: i.size }).pipe(t);
};
var ao = (s3, t) => {
  let e = new qt(s3), i = s3.maxReadSize || 16 * 1024 * 1024, r = s3.file;
  return new Promise((o, h) => {
    e.on("error", h), e.on("close", o), Lr.stat(r, (a, l) => {
      if (a) h(a);
      else {
        let c = new gt(r, { readSize: i, size: l.size });
        c.on("error", h), c.pipe(e);
      }
    });
  });
};
var lo = K(ho, ao, (s3) => new Te(s3), (s3) => new qt(s3), (s3, t) => {
  t?.length && Yi(s3, t);
});
var co = (s3, t) => {
  let e = new kt(s3), i = true, r, n;
  try {
    try {
      r = v.openSync(s3.file, "r+");
    } catch (a) {
      if (a?.code === "ENOENT") r = v.openSync(s3.file, "w+");
      else throw a;
    }
    let o = v.fstatSync(r), h = Buffer.alloc(512);
    t: for (n = 0; n < o.size; n += 512) {
      for (let c = 0, d = 0; c < 512; c += d) {
        if (d = v.readSync(r, h, c, h.length - c, n + c), n === 0 && h[0] === 31 && h[1] === 139) throw new Error("cannot append to compressed archives");
        if (!d) break t;
      }
      let a = new F(h);
      if (!a.cksumValid) break;
      let l = 512 * Math.ceil((a.size || 0) / 512);
      if (n + l + 512 > o.size) break;
      n += l, s3.mtimeCache && a.mtime && s3.mtimeCache.set(String(a.path), a.mtime);
    }
    i = false, fo(s3, e, n, r, t);
  } finally {
    if (i) try {
      v.closeSync(r);
    } catch {
    }
  }
};
var fo = (s3, t, e, i, r) => {
  let n = new Wt(s3.file, { fd: i, start: e });
  t.pipe(n), mo(t, r);
};
var uo = (s3, t) => {
  t = Array.from(t);
  let e = new Et(s3), i = (n, o, h) => {
    let a = (T, N) => {
      T ? v.close(n, (E) => h(T)) : h(null, N);
    }, l = 0;
    if (o === 0) return a(null, 0);
    let c = 0, d = Buffer.alloc(512), S = (T, N) => {
      if (T || typeof N > "u") return a(T);
      if (c += N, c < 512 && N) return v.read(n, d, c, d.length - c, l + c, S);
      if (l === 0 && d[0] === 31 && d[1] === 139) return a(new Error("cannot append to compressed archives"));
      if (c < 512) return a(null, l);
      let E = new F(d);
      if (!E.cksumValid) return a(null, l);
      let x = 512 * Math.ceil((E.size ?? 0) / 512);
      if (l + x + 512 > o || (l += x + 512, l >= o)) return a(null, l);
      s3.mtimeCache && E.mtime && s3.mtimeCache.set(String(E.path), E.mtime), c = 0, v.read(n, d, 0, 512, l, S);
    };
    v.read(n, d, 0, 512, l, S);
  };
  return new Promise((n, o) => {
    e.on("error", o);
    let h = "r+", a = (l, c) => {
      if (l && l.code === "ENOENT" && h === "r+") return h = "w+", v.open(s3.file, h, a);
      if (l || !c) return o(l);
      v.fstat(c, (d, S) => {
        if (d) return v.close(c, () => o(d));
        i(c, S.size, (T, N) => {
          if (T) return o(T);
          let E = new tt(s3.file, { fd: c, start: N });
          e.pipe(E), E.on("error", o), E.on("close", n), po(e, t);
        });
      });
    };
    v.open(s3.file, h, a);
  });
};
var mo = (s3, t) => {
  t.forEach((e) => {
    e.charAt(0) === "@" ? It({ file: Nr.resolve(s3.cwd, e.slice(1)), sync: true, noResume: true, onReadEntry: (i) => s3.add(i) }) : s3.add(e);
  }), s3.end();
};
var po = async (s3, t) => {
  for (let e = 0; e < t.length; e++) {
    let i = String(t[e]);
    i.charAt(0) === "@" ? await It({ file: Nr.resolve(String(s3.cwd), i.slice(1)), noResume: true, onReadEntry: (r) => s3.add(r) }) : s3.add(i);
  }
  s3.end();
};
var vt = K(co, uo, () => {
  throw new TypeError("file is required");
}, () => {
  throw new TypeError("file is required");
}, (s3, t) => {
  if (!ks(s3)) throw new TypeError("file is required");
  if (s3.gzip || s3.brotli || s3.zstd || s3.file.endsWith(".br") || s3.file.endsWith(".tbr")) throw new TypeError("cannot append to compressed archives");
  if (!t?.length) throw new TypeError("no paths specified to add/replace");
});
var Eo = K(vt.syncFile, vt.asyncFile, vt.syncNoFile, vt.asyncNoFile, (s3, t = []) => {
  vt.validate?.(s3, t), wo(s3);
});
var wo = (s3) => {
  let t = s3.filter;
  s3.mtimeCache || (s3.mtimeCache = /* @__PURE__ */ new Map()), s3.filter = t ? (e, i) => t(e, i) && !((s3.mtimeCache?.get(e) ?? i.mtime ?? 0) > (i.mtime ?? 0)) : (e, i) => !((s3.mtimeCache?.get(e) ?? i.mtime ?? 0) > (i.mtime ?? 0));
};

// src/core/packer.ts
function sha256(data) {
  return createHash("sha256").update(data).digest("hex");
}
async function pack(input) {
  const stagingDir = join(input.outputDir, ".staging");
  await mkdir(join(stagingDir, "config"), { recursive: true });
  await mkdir(join(stagingDir, "workspace"), { recursive: true });
  const files = [];
  if (input.sanitizedConfig) {
    const configJson = JSON.stringify(input.sanitizedConfig, null, 2);
    const configPath = "config/openclaw.sanitized.json";
    await writeFile(join(stagingDir, configPath), configJson);
    files.push({
      path: configPath,
      sha256: sha256(configJson),
      size: Buffer.byteLength(configJson)
    });
  }
  for (const file of input.workspaceFiles) {
    const destPath = `workspace/${file.relativePath}`;
    const destDir = join(stagingDir, "workspace", file.relativePath, "..");
    await mkdir(destDir, { recursive: true });
    await writeFile(join(stagingDir, destPath), file.content);
    files.push({
      path: destPath,
      sha256: sha256(file.content),
      size: file.size
    });
  }
  const bundledSkills = [];
  if (input.skills && input.skills.length > 0) {
    for (const skill of input.skills) {
      const skillDir = join(stagingDir, "skills", skill.name);
      await mkdir(skillDir, { recursive: true });
      for (const file of skill.files) {
        const destPath = `skills/${skill.name}/${file.relativePath}`;
        const destDir = join(skillDir, file.relativePath, "..");
        await mkdir(destDir, { recursive: true });
        await writeFile(join(stagingDir, destPath), file.content);
        files.push({
          path: destPath,
          sha256: sha256(file.content),
          size: file.size
        });
      }
      bundledSkills.push({
        name: skill.name,
        version: skill.version,
        source: skill.source,
        fileCount: skill.files.length
      });
    }
  }
  const manifest = {
    schemaVersion: 1,
    name: `${input.ref.namespace}/${input.ref.name}`,
    tag: input.ref.tag,
    created: (/* @__PURE__ */ new Date()).toISOString(),
    description: input.description,
    openclaw: {},
    requiredCredentials: input.removedCredentials.map((c) => ({
      provider: c.provider,
      type: c.type
    })),
    plugins: [...input.plugins],
    bundledSkills: bundledSkills.length > 0 ? bundledSkills : void 0,
    channels: [...input.channels],
    permissions: {
      network: true,
      filesystem: false,
      shell: false,
      tools: []
    },
    files,
    integrity: {
      checksum: ""
    }
  };
  await writeFile(join(stagingDir, "manifest.json"), JSON.stringify(manifest, null, 2));
  const archiveName = `${input.ref.name}-${input.ref.tag}.claw`;
  const archivePath = join(input.outputDir, archiveName);
  const tarEntries = ["manifest.json", "config", "workspace"];
  if (bundledSkills.length > 0) {
    tarEntries.push("skills");
  }
  await zn({ gzip: true, file: archivePath, cwd: stagingDir }, tarEntries);
  const archiveBuffer = await readFile(archivePath);
  const checksum = `sha256:${sha256(archiveBuffer)}`;
  const finalManifest = { ...manifest, integrity: { checksum } };
  await writeFile(join(stagingDir, "manifest.json"), JSON.stringify(finalManifest, null, 2));
  await zn({ gzip: true, file: archivePath, cwd: stagingDir }, tarEntries);
  const finalArchive = await readFile(archivePath);
  return {
    archivePath,
    manifest: {
      ...finalManifest,
      integrity: { checksum: `sha256:${sha256(finalArchive)}` }
    },
    totalSize: finalArchive.length
  };
}

// src/core/unpacker.ts
import { createHash as createHash2 } from "node:crypto";
import { readFile as readFile2, readdir, mkdir as mkdir2 } from "node:fs/promises";
import { join as join2, relative } from "node:path";
async function collectAllFiles(dir, base) {
  const results = [];
  const entries = await readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = join2(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...await collectAllFiles(full, base));
    } else {
      const content = await readFile2(full);
      results.push({
        relativePath: relative(base, full),
        absolutePath: full,
        size: content.length
      });
    }
  }
  return results;
}
async function unpack(archivePath, outputDir) {
  await mkdir2(outputDir, { recursive: true });
  await lo({
    file: archivePath,
    cwd: outputDir,
    gzip: true,
    preservePaths: false,
    strict: true
  });
  const manifestRaw = await readFile2(join2(outputDir, "manifest.json"), "utf-8");
  const manifest = JSON.parse(manifestRaw);
  let integrityValid = true;
  for (const fileEntry of manifest.files) {
    try {
      const content = await readFile2(join2(outputDir, fileEntry.path));
      const hash = createHash2("sha256").update(content).digest("hex");
      if (hash !== fileEntry.sha256) {
        integrityValid = false;
      }
    } catch {
      integrityValid = false;
    }
  }
  const files = await collectAllFiles(outputDir, outputDir);
  return { manifest, files, outputDir, integrityValid };
}

// src/core/sanitizer.ts
var SENSITIVE_PATTERNS = [
  { name: "openai", pattern: /sk-(?:proj-)?[a-zA-Z0-9]{20,}/ },
  { name: "anthropic", pattern: /sk-ant-[a-zA-Z0-9-]{20,}/ },
  { name: "google", pattern: /AIza[a-zA-Z0-9_-]{35}/ },
  { name: "xai", pattern: /xai-[a-zA-Z0-9]{20,}/ },
  { name: "telegram", pattern: /\d{8,10}:[a-zA-Z0-9_-]{35}/ },
  {
    name: "discord",
    pattern: /[MN][a-zA-Z0-9]{23,}\.[a-zA-Z0-9_-]{6}\.[a-zA-Z0-9_-]{27,}/
  },
  { name: "slack", pattern: /xoxb-[0-9]+-[a-zA-Z0-9]+/ },
  { name: "private_key", pattern: /-----BEGIN (?:RSA |EC )?PRIVATE KEY-----/ },
  {
    name: "high_entropy",
    test: (v2) => v2.length > 16 && shannonEntropy(v2) > 4.5
  }
];
function shannonEntropy(str) {
  const freq = /* @__PURE__ */ new Map();
  for (const ch of str) {
    freq.set(ch, (freq.get(ch) ?? 0) + 1);
  }
  let entropy = 0;
  for (const count of freq.values()) {
    const p2 = count / str.length;
    entropy -= p2 * Math.log2(p2);
  }
  return entropy;
}
function detectSensitiveValues(input) {
  const matches = [];
  for (const rule of SENSITIVE_PATTERNS) {
    if (rule.pattern) {
      const regex = new RegExp(rule.pattern, "g");
      let match;
      while ((match = regex.exec(input)) !== null) {
        matches.push({
          name: rule.name,
          original: match[0],
          startIndex: match.index,
          endIndex: match.index + match[0].length
        });
      }
    } else if (rule.test?.(input)) {
      matches.push({
        name: rule.name,
        original: input,
        startIndex: 0,
        endIndex: input.length
      });
    }
  }
  return matches;
}
var SENSITIVE_JSON_PATHS = [
  "gateway.auth.token",
  "gateway.auth.password",
  "channels.*.token",
  "channels.*.secret",
  "channels.*.apiKey",
  "agents.*.auth.*"
];
function matchesJsonPath(actualPath, pattern) {
  const actualParts = actualPath.split(".");
  const patternParts = pattern.split(".");
  if (actualParts.length !== patternParts.length) {
    return false;
  }
  return patternParts.every((p2, i) => p2 === "*" || p2 === actualParts[i]);
}
function isSecretRef(value) {
  return typeof value === "string" && value.startsWith("$ref:env:");
}
function sanitizeConfig(config) {
  const removedCredentials = [];
  function walk(obj, currentPath) {
    const result = {};
    for (const [key, value] of Object.entries(obj)) {
      const path = [...currentPath, key];
      const pathStr = path.join(".");
      if (typeof value === "object" && value !== null && !Array.isArray(value)) {
        result[key] = walk(value, path);
      } else if (typeof value === "string") {
        if (isSecretRef(value)) {
          result[key] = value;
        } else if (SENSITIVE_JSON_PATHS.some((p2) => matchesJsonPath(pathStr, p2))) {
          const provider = path.length >= 2 ? path[path.length - 2] : "unknown";
          const type = key;
          result[key] = `$CLAW_PLACEHOLDER:${provider}:${type}`;
          removedCredentials.push({ path: pathStr, provider, type });
        } else {
          const detected = detectSensitiveValues(value);
          if (detected.length > 0) {
            const provider = detected[0].name;
            result[key] = `$CLAW_PLACEHOLDER:${provider}:${key}`;
            removedCredentials.push({ path: pathStr, provider, type: key });
          } else {
            result[key] = value;
          }
        }
      } else {
        result[key] = value;
      }
    }
    return result;
  }
  const sanitized = walk(config, []);
  return { sanitized, removedCredentials };
}

// src/core/scanner.ts
import { readFile as readFile3, readdir as readdir2 } from "node:fs/promises";
import { join as join3, relative as relative2 } from "node:path";

// src/core/clawignore.ts
var MANDATORY_FILE_EXCLUSIONS = [
  ".git/**",
  ".openclaw/**",
  "auth-profiles.json",
  "auth.json",
  "credentials/**",
  "sessions/**",
  "memory/**",
  "*.key",
  "*.pem",
  "*.p12",
  "*.pfx",
  "*.png",
  "*.jpg",
  "*.jpeg",
  "*.gif",
  "*.py",
  "ppt_env/**"
];
function parseClawignore(content) {
  const filePatterns = [];
  const jsonPaths = [];
  for (const raw of content.split("\n")) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) {
      continue;
    }
    if (line.startsWith("$.")) {
      jsonPaths.push(line);
    } else {
      filePatterns.push(line);
    }
  }
  return { filePatterns, jsonPaths };
}
function matchesGlob(filePath, pattern) {
  if (pattern.endsWith("/")) {
    return filePath.startsWith(pattern) || filePath.startsWith(pattern.slice(0, -1));
  }
  if (pattern.includes("**")) {
    const prefix = pattern.split("**")[0];
    return filePath.startsWith(prefix);
  }
  if (pattern.startsWith("*.")) {
    return filePath.endsWith(pattern.slice(1));
  }
  return filePath === pattern || filePath.endsWith("/" + pattern);
}
function shouldExclude(filePath, userRules) {
  for (const pattern of MANDATORY_FILE_EXCLUSIONS) {
    if (matchesGlob(filePath, pattern)) {
      return true;
    }
  }
  for (const pattern of userRules.filePatterns) {
    if (matchesGlob(filePath, pattern)) {
      return true;
    }
  }
  return false;
}

// src/core/scanner.ts
async function collectFiles(dir, baseDir, rules, files) {
  const entries = await readdir2(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = join3(dir, entry.name);
    const relPath = relative2(baseDir, fullPath);
    if (shouldExclude(relPath, rules)) {
      continue;
    }
    if (entry.isDirectory()) {
      await collectFiles(fullPath, baseDir, rules, files);
    } else if (entry.isFile()) {
      const content = await readFile3(fullPath);
      files.push({
        relativePath: relPath,
        absolutePath: fullPath,
        content,
        size: content.length
      });
    }
  }
}
async function collectAllFiles2(dir, baseDir) {
  const files = [];
  let entries;
  try {
    entries = await readdir2(dir, { withFileTypes: true });
  } catch {
    return files;
  }
  for (const entry of entries) {
    const fullPath = join3(dir, entry.name);
    const relPath = relative2(baseDir, fullPath);
    if (entry.isDirectory()) {
      files.push(...await collectAllFiles2(fullPath, baseDir));
    } else if (entry.isFile()) {
      const content = await readFile3(fullPath);
      files.push({ relativePath: relPath, absolutePath: fullPath, content, size: content.length });
    }
  }
  return files;
}
async function scanSkills(stateDir) {
  const skillsDir = join3(stateDir, "skills");
  let entries;
  try {
    entries = await readdir2(skillsDir, { withFileTypes: true });
  } catch {
    return [];
  }
  const skills = [];
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const skillDir = join3(skillsDir, entry.name);
    const files = await collectAllFiles2(skillDir, skillDir);
    if (files.length === 0) continue;
    let source = "user";
    let version;
    try {
      const metaRaw = await readFile3(join3(skillDir, "_meta.json"), "utf-8");
      const meta = JSON.parse(metaRaw);
      source = "clawhub";
      version = meta.version;
    } catch {
    }
    skills.push({ name: entry.name, version, source, files });
  }
  return skills;
}
async function scanInstance(stateDir, agentId = "main") {
  const configPath = join3(stateDir, "openclaw.json");
  let config = null;
  try {
    const raw = await readFile3(configPath, "utf-8");
    config = JSON.parse(raw);
  } catch {
    config = null;
  }
  let clawignoreContent = "";
  try {
    clawignoreContent = await readFile3(join3(stateDir, ".clawignore"), "utf-8");
  } catch {
  }
  const rules = parseClawignore(clawignoreContent);
  const candidateDirs = [
    join3(stateDir, "workspace"),
    join3(stateDir, "agents", agentId, "agent", "workspace")
  ];
  const workspaceFiles = [];
  for (const workspaceDir of candidateDirs) {
    try {
      await collectFiles(workspaceDir, workspaceDir, rules, workspaceFiles);
      if (workspaceFiles.length > 0) {
        break;
      }
    } catch {
    }
  }
  const skills = await scanSkills(stateDir);
  return {
    config,
    configPath: config ? configPath : null,
    workspaceFiles,
    skills,
    stateDir,
    agentId
  };
}

// src/types/ref.ts
var REF_PATTERN = /^([a-z0-9][a-z0-9_-]*)\/([a-z0-9][a-z0-9._-]*)(?::([a-zA-Z0-9][a-zA-Z0-9._-]*))?$/;
function parseClawRef(input) {
  const match = input.match(REF_PATTERN);
  if (!match) {
    throw new Error(`Invalid claw reference "${input}". Expected format: namespace/name[:tag]`);
  }
  return {
    namespace: match[1],
    name: match[2],
    tag: match[3] ?? "latest"
  };
}
function formatClawRef(ref) {
  return `${ref.namespace}/${ref.name}:${ref.tag}`;
}

// src/cli/standalone.ts
var BACKUP_DIR_NAME = ".zhuaxia-backups";
function usage() {
  console.log(`Usage:
  clawctl save <ref> [--source <path>] [-o <path>] [--description <text>] [--include-memory]
  clawctl load <file> [--target <path>] [--agent-name <name>] [--dry-run] [--no-backup]
  clawctl backup [--source <path>] [--label <text>]
  clawctl rollback [<id>] [--target <path>]
  clawctl backups [--source <path>]

Commands:
  save      Export an OpenClaw instance to a .claw file
  load      Import from a .claw file (auto-backs up before install)
  backup    Create a backup of current state
  rollback  Restore from a backup (latest or by id)
  backups   List available backups

Examples:
  clawctl save cjy/my-bot:v1 -o ~/my-bot.claw
  clawctl load ~/my-bot.claw --dry-run
  clawctl load ~/my-bot.claw
  clawctl backup --label "before experiment"
  clawctl backups
  clawctl rollback
  clawctl rollback 20260308-143022`);
  process.exit(1);
}
function parseArgs(argv) {
  const args = argv.slice(2);
  if (args.length < 1) usage();
  const command = args[0];
  const noPositionalCommands = ["backups", "backup"];
  let positional = "";
  let flagStart = 1;
  if (!noPositionalCommands.includes(command) && args.length > 1 && !args[1].startsWith("-")) {
    positional = args[1];
    flagStart = 2;
  }
  const flags = {};
  for (let i = flagStart; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--include-memory" || arg === "--dry-run" || arg === "--no-backup") {
      flags[arg.slice(2)] = true;
    } else if (arg.startsWith("--") || arg === "-o") {
      const key = arg.startsWith("--") ? arg.slice(2) : "output";
      const value = args[++i];
      if (!value) {
        console.error(`Missing value for ${arg}`);
        process.exit(1);
      }
      flags[key] = value;
    }
  }
  return { command, positional, flags };
}
function backupRoot(stateDir) {
  return resolve(stateDir, BACKUP_DIR_NAME);
}
function makeBackupId() {
  const d = /* @__PURE__ */ new Date();
  const pad = (n, w2 = 2) => String(n).padStart(w2, "0");
  return `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}-${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
}
async function exists(p2) {
  try {
    await stat(p2);
    return true;
  } catch {
    return false;
  }
}
async function collectRelativeFiles(dir) {
  const result = [];
  async function walk(d) {
    let entries;
    try {
      entries = await readdir3(d, { withFileTypes: true });
    } catch {
      return;
    }
    for (const e of entries) {
      const full = resolve(d, e.name);
      if (e.isDirectory()) {
        await walk(full);
      } else {
        result.push(relative3(dir, full));
      }
    }
  }
  await walk(dir);
  return result;
}
async function createBackup(stateDir, label) {
  const id = makeBackupId();
  const dest = resolve(backupRoot(stateDir), id);
  await mkdir3(resolve(dest, "workspace"), { recursive: true });
  let fileCount = 0;
  const workspaceDir = resolve(stateDir, "workspace");
  if (await exists(workspaceDir)) {
    const files = await collectRelativeFiles(workspaceDir);
    for (const rel of files) {
      const src = resolve(workspaceDir, rel);
      const dst = resolve(dest, "workspace", rel);
      await mkdir3(resolve(dst, ".."), { recursive: true });
      await cp(src, dst);
      fileCount++;
    }
  }
  let hasConfig = false;
  const configPath = resolve(stateDir, "openclaw.json");
  if (await exists(configPath)) {
    await cp(configPath, resolve(dest, "openclaw.json"));
    hasConfig = true;
    fileCount++;
  }
  const meta = {
    id,
    created: (/* @__PURE__ */ new Date()).toISOString(),
    label,
    files: fileCount,
    hasConfig
  };
  await writeFile2(resolve(dest, "backup.meta.json"), JSON.stringify(meta, null, 2));
  return meta;
}
async function listBackups(stateDir) {
  const root = backupRoot(stateDir);
  if (!await exists(root)) return [];
  const entries = await readdir3(root, { withFileTypes: true });
  const metas = [];
  for (const e of entries) {
    if (!e.isDirectory()) continue;
    const metaPath = resolve(root, e.name, "backup.meta.json");
    try {
      const raw = await readFile4(metaPath, "utf-8");
      metas.push(JSON.parse(raw));
    } catch {
    }
  }
  return metas.sort((a, b2) => b2.id.localeCompare(a.id));
}
async function restoreBackup(stateDir, backupId) {
  const src = resolve(backupRoot(stateDir), backupId);
  if (!await exists(src)) {
    throw new Error(`Backup "${backupId}" not found`);
  }
  const metaRaw = await readFile4(resolve(src, "backup.meta.json"), "utf-8");
  const meta = JSON.parse(metaRaw);
  const workspaceBackup = resolve(src, "workspace");
  const workspaceDir = resolve(stateDir, "workspace");
  if (await exists(workspaceBackup)) {
    const backedUpFiles = await collectRelativeFiles(workspaceBackup);
    for (const rel of backedUpFiles) {
      const dst = resolve(workspaceDir, rel);
      await mkdir3(resolve(dst, ".."), { recursive: true });
      await cp(resolve(workspaceBackup, rel), dst);
    }
  }
  const configBackup = resolve(src, "openclaw.json");
  if (await exists(configBackup)) {
    await cp(configBackup, resolve(stateDir, "openclaw.json"));
  }
  console.log(`Restored backup "${backupId}" (${meta.label || "no label"})`);
  console.log(`  Files: ${meta.files}`);
  console.log(`  Config: ${meta.hasConfig ? "restored" : "not in backup"}`);
}
async function runSave(ref, flags) {
  const parsed = parseClawRef(ref);
  const source = flags.source ?? resolve(homedir(), ".openclaw");
  console.log(`Scanning ${source}...`);
  const scan = await scanInstance(source);
  console.log("Running security scan...");
  const sanitized = scan.config ? sanitizeConfig(scan.config) : { sanitized: {}, removedCredentials: [] };
  if (sanitized.removedCredentials.length > 0) {
    console.log(`Removed ${sanitized.removedCredentials.length} sensitive values:`);
    for (const cred of sanitized.removedCredentials) {
      console.log(`  - ${cred.path} (${cred.provider}:${cred.type})`);
    }
  }
  const workspaceFiles = flags["include-memory"] ? scan.workspaceFiles : scan.workspaceFiles.filter((f2) => f2.relativePath !== "MEMORY.md");
  const config = scan.config;
  const skillEntries = config?.skills?.entries;
  const pluginNames = skillEntries ? Object.keys(skillEntries) : [];
  const channelEntries = config?.channels;
  const channels = channelEntries ? Object.keys(channelEntries) : [];
  const skillInputs = scan.skills.map((s3) => ({
    name: s3.name,
    version: s3.version,
    source: s3.source,
    files: s3.files.map((f2) => ({
      relativePath: f2.relativePath,
      content: f2.content,
      size: f2.size
    }))
  }));
  if (skillInputs.length > 0) {
    console.log(`
Bundling ${skillInputs.length} skill(s):`);
    for (const s3 of skillInputs) {
      const ver = s3.version ? `@${s3.version}` : "";
      console.log(`  - ${s3.name}${ver} (${s3.source}, ${s3.files.length} files)`);
    }
  }
  const stagingDir = resolve(source, ".claw-staging");
  const result = await pack({
    ref: parsed,
    description: flags.description ?? "",
    sanitizedConfig: sanitized.sanitized,
    workspaceFiles: workspaceFiles.map((f2) => ({
      relativePath: f2.relativePath,
      content: f2.content,
      size: f2.size
    })),
    removedCredentials: [...sanitized.removedCredentials],
    plugins: pluginNames,
    skills: skillInputs,
    channels,
    outputDir: stagingDir
  });
  const defaultOutput = `${parsed.name}-${parsed.tag}.claw`;
  const outputPath = resolve(process.cwd(), flags.output ?? defaultOutput);
  await copyFile(result.archivePath, outputPath);
  await rm(stagingDir, { recursive: true, force: true });
  console.log(`
Saved ${formatClawRef(parsed)}`);
  console.log(`  File: ${outputPath}`);
  console.log(`  Size: ${result.totalSize} bytes`);
  console.log(`  Files: ${result.manifest.files.length}`);
  if (result.manifest.bundledSkills && result.manifest.bundledSkills.length > 0) {
    console.log(`  Skills bundled: ${result.manifest.bundledSkills.length}`);
  }
  console.log(`  Checksum: ${result.manifest.integrity.checksum}`);
}
async function runLoad(file, flags) {
  const archivePath = resolve(process.cwd(), file);
  const target = flags.target ?? resolve(homedir(), ".openclaw");
  console.log(`Loading ${basename(archivePath)}...`);
  const tmpDir = resolve(target, ".claw-tmp", `load-${Date.now()}`);
  const result = await unpack(archivePath, tmpDir);
  const bundledSkills = result.manifest.bundledSkills ?? [];
  console.log(`
  Name: ${result.manifest.name}:${result.manifest.tag}`);
  console.log(`  Description: ${result.manifest.description || "(none)"}`);
  console.log(`  Files: ${result.manifest.files.length}`);
  console.log(`  Plugins: ${result.manifest.plugins.join(", ") || "(none)"}`);
  console.log(`  Channels: ${result.manifest.channels.join(", ") || "(none)"}`);
  if (bundledSkills.length > 0) {
    console.log(`  Bundled skills: ${bundledSkills.map((s3) => s3.name + (s3.version ? `@${s3.version}` : "")).join(", ")}`);
  }
  console.log(`  Integrity: ${result.integrityValid ? "verified" : "FAILED"}`);
  if (!result.integrityValid) {
    console.error("\nIntegrity check FAILED. File may be corrupted or tampered.");
    await rm(tmpDir, { recursive: true, force: true });
    process.exit(1);
  }
  if (result.manifest.requiredCredentials.length > 0) {
    console.log("\n  Required credentials:");
    for (const cred of result.manifest.requiredCredentials) {
      console.log(`    - ${cred.provider} (${cred.type})`);
    }
  }
  if (flags["dry-run"]) {
    console.log("\n  Workspace files:");
    for (const f2 of result.files) {
      if (f2.relativePath.startsWith("workspace/")) {
        console.log(`    ${f2.relativePath.slice("workspace/".length)}`);
      }
    }
    if (bundledSkills.length > 0) {
      console.log("\n  Bundled skills:");
      for (const s3 of bundledSkills) {
        const ver = s3.version ? `@${s3.version}` : "";
        console.log(`    ${s3.name}${ver} (${s3.source}, ${s3.fileCount} files)`);
      }
    }
    await rm(tmpDir, { recursive: true, force: true });
    return;
  }
  if (!flags["no-backup"]) {
    console.log("\n  Creating backup before install...");
    const label = `before-load:${basename(archivePath)}`;
    const meta = await createBackup(target, label);
    console.log(`  Backup created: ${meta.id} (${meta.files} files)`);
    console.log(`  Rollback with: clawctl rollback ${meta.id}`);
  }
  const nameParts = result.manifest.name.split("/");
  const defaultName = nameParts[nameParts.length - 1];
  const agentName = flags["agent-name"] ?? defaultName;
  const workspaceDir = resolve(target, "workspace");
  await mkdir3(workspaceDir, { recursive: true });
  let installed = 0;
  for (const f2 of result.files) {
    if (f2.relativePath.startsWith("workspace/")) {
      const relPath = f2.relativePath.slice("workspace/".length);
      const content = await readFile4(f2.absolutePath);
      const dest = resolve(workspaceDir, relPath);
      await mkdir3(resolve(dest, ".."), { recursive: true });
      await writeFile2(dest, content);
      installed++;
    }
  }
  let skillsInstalled = 0;
  const skillsSkipped = [];
  if (bundledSkills.length > 0) {
    const targetSkillsDir = resolve(target, "skills");
    await mkdir3(targetSkillsDir, { recursive: true });
    for (const skillMeta of bundledSkills) {
      const targetSkillDir = resolve(targetSkillsDir, skillMeta.name);
      const alreadyExists = await exists(targetSkillDir);
      if (alreadyExists) {
        let existingVersion;
        try {
          const metaRaw = await readFile4(resolve(targetSkillDir, "_meta.json"), "utf-8");
          existingVersion = JSON.parse(metaRaw).version;
        } catch {
        }
        const isNewer = skillMeta.version && existingVersion && skillMeta.version > existingVersion;
        if (!isNewer && existingVersion) {
          skillsSkipped.push(`${skillMeta.name}@${existingVersion} (already installed)`);
          continue;
        }
      }
      const skillFiles = result.files.filter(
        (f2) => f2.relativePath.startsWith(`skills/${skillMeta.name}/`)
      );
      for (const f2 of skillFiles) {
        const relPath = f2.relativePath.slice(`skills/${skillMeta.name}/`.length);
        const dest = resolve(targetSkillDir, relPath);
        await mkdir3(resolve(dest, ".."), { recursive: true });
        const content = await readFile4(f2.absolutePath);
        await writeFile2(dest, content);
      }
      skillsInstalled++;
    }
  }
  const configFile = result.files.find(
    (f2) => f2.relativePath === "config/openclaw.sanitized.json"
  );
  if (configFile) {
    const content = await readFile4(configFile.absolutePath, "utf-8");
    const importedConfigPath = resolve(target, "openclaw.imported.json");
    await writeFile2(importedConfigPath, content);
    console.log(`
  Imported config saved to: openclaw.imported.json`);
    console.log("  (Review and merge into openclaw.json manually to preserve your credentials)");
  }
  await rm(tmpDir, { recursive: true, force: true });
  console.log(`
Loaded "${agentName}" - ${installed} workspace files installed.`);
  if (skillsInstalled > 0) {
    console.log(`  Skills installed: ${skillsInstalled}`);
  }
  if (skillsSkipped.length > 0) {
    console.log(`  Skills skipped: ${skillsSkipped.join(", ")}`);
  }
  if (result.manifest.plugins.length > 0) {
    const bundledNames = new Set(bundledSkills.map((s3) => s3.name));
    const unbundled = result.manifest.plugins.filter((p2) => !bundledNames.has(p2));
    if (unbundled.length > 0) {
      console.log(`
  Additional skills referenced in config (not bundled, may be built-in):`);
      for (const skill of unbundled) {
        console.log(`    - ${skill}`);
      }
    }
  }
  if (result.manifest.requiredCredentials.length > 0) {
    console.log("  Configure credentials with: openclaw config set ...");
  }
}
async function runBackup(flags) {
  const source = flags.source ?? resolve(homedir(), ".openclaw");
  const label = flags.label ?? "";
  console.log(`Backing up ${source}...`);
  const meta = await createBackup(source, label);
  console.log(`
Backup created: ${meta.id}`);
  console.log(`  Label: ${meta.label || "(none)"}`);
  console.log(`  Files: ${meta.files}`);
  console.log(`  Config: ${meta.hasConfig ? "included" : "not found"}`);
  console.log(`  Rollback with: clawctl rollback ${meta.id}`);
}
async function runBackups(flags) {
  const source = flags.source ?? resolve(homedir(), ".openclaw");
  const metas = await listBackups(source);
  if (metas.length === 0) {
    console.log("No backups found.");
    return;
  }
  console.log(`Found ${metas.length} backup(s):
`);
  for (const m2 of metas) {
    const label = m2.label ? ` \u2014 ${m2.label}` : "";
    const config = m2.hasConfig ? " +config" : "";
    console.log(`  ${m2.id}  ${m2.files} files${config}${label}`);
    console.log(`    ${m2.created}`);
  }
  console.log(`
Rollback with: clawctl rollback <id>`);
}
async function runRollback(id, flags) {
  const target = flags.target ?? resolve(homedir(), ".openclaw");
  let backupId = id;
  if (!backupId) {
    const metas = await listBackups(target);
    if (metas.length === 0) {
      console.error("No backups found. Nothing to rollback to.");
      process.exit(1);
    }
    backupId = metas[0].id;
    console.log(`Using latest backup: ${backupId}`);
  }
  console.log("Backing up current state before rollback...");
  const safeMeta = await createBackup(target, `before-rollback:${backupId}`);
  console.log(`  Safety backup: ${safeMeta.id}`);
  await restoreBackup(target, backupId);
}
async function main() {
  const { command, positional, flags } = parseArgs(process.argv);
  switch (command) {
    case "save":
      if (!positional) usage();
      await runSave(positional, flags);
      break;
    case "load":
      if (!positional) usage();
      await runLoad(positional, flags);
      break;
    case "backup":
      await runBackup(flags);
      break;
    case "backups":
      await runBackups(flags);
      break;
    case "rollback":
      await runRollback(positional, flags);
      break;
    default:
      console.error(`Unknown command: ${command}`);
      usage();
  }
}
main().catch((err) => {
  console.error(err instanceof Error ? err.message : String(err));
  process.exit(1);
});
