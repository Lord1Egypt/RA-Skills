import test from "node:test";
import assert from "node:assert/strict";

import {
  maskSecret,
  parseDotEnv,
  validateSkillEnv
} from "../scripts/check-env.mjs";

test("parseDotEnv parses quoted and unquoted values", () => {
  const parsed = parseDotEnv(`
# Movie skill config
QUARK_COOKIE="a=b; c=d"
BAIDU_COOKIE="BDUSS=abc; STOKEN=def"
OPENLIST_TOKEN='openlist-token'
QUARK_DEFAULT_SAVE_URL=https://pan.quark.cn/list#/list/all/fid-%E5%A4%87%E4%BB%BD
BAIDU_DEFAULT_SAVE_PATH=/我的资源/影视
OPENLIST_DEFAULT_COPY_DST_PATH=/影视资源备份/影视
`);

  assert.equal(parsed.QUARK_COOKIE, "a=b; c=d");
  assert.equal(parsed.BAIDU_COOKIE, "BDUSS=abc; STOKEN=def");
  assert.equal(parsed.OPENLIST_TOKEN, "openlist-token");
  assert.equal(parsed.QUARK_DEFAULT_SAVE_URL, "https://pan.quark.cn/list#/list/all/fid-%E5%A4%87%E4%BB%BD");
  assert.equal(parsed.BAIDU_DEFAULT_SAVE_PATH, "/我的资源/影视");
  assert.equal(parsed.OPENLIST_DEFAULT_COPY_DST_PATH, "/影视资源备份/影视");
});

test("validateSkillEnv reports missing required first-use configuration", () => {
  const result = validateSkillEnv({
    QUARK_COOKIE: "",
    OPENLIST_TOKEN: "",
    QUARK_DEFAULT_SAVE_URL: "",
    OPENLIST_DEFAULT_COPY_DST_PATH: ""
  });

  assert.equal(result.ok, false);
  assert.deepEqual(
    result.missing.map((item) => item.key),
    ["OPENLIST_TOKEN", "OPENLIST_BASE_URL", "OPENLIST_DEFAULT_COPY_DST_PATH"]
  );
  assert.equal(result.providerOk, false);
  assert.equal(result.nextAction, "configure_core_and_provider");
});

test("validateSkillEnv accepts complete configuration and masks secrets", () => {
  const result = validateSkillEnv({
    QUARK_COOKIE: "b-user-id=abc; __uid=uid-value",
    OPENLIST_TOKEN: "openlist-test-token",
    OPENLIST_BASE_URL: "http://127.0.0.1:5244/",
    QUARK_DEFAULT_SAVE_URL: "/备份资源",
    OPENLIST_DEFAULT_COPY_DST_PATH: "/影视资源备份/影视"
  });

  assert.equal(result.ok, true);
  assert.equal(result.providerOk, true);
  assert.equal(result.nextAction, "ready");
  assert.equal(result.values.OPENLIST_BASE_URL.displayValue, "http://127.0.0.1:5244/");
  assert.equal(result.values.QUARK_COOKIE.secret, true);
  assert.match(result.values.QUARK_COOKIE.displayValue, /^b-user-i/);
  assert.doesNotMatch(result.values.QUARK_COOKIE.displayValue, /uid-value/);
});

test("validateSkillEnv accepts Baidu-only cloud-drive configuration", () => {
  const result = validateSkillEnv({
    BAIDU_COOKIE: "BDUSS=abc; STOKEN=secret-token",
    OPENLIST_TOKEN: "token",
    OPENLIST_BASE_URL: "http://127.0.0.1:5244/",
    BAIDU_DEFAULT_SAVE_PATH: "/NAS资源下载",
    OPENLIST_DEFAULT_COPY_DST_PATH: "/影视资源备份/影视"
  });

  assert.equal(result.ok, true);
  assert.equal(result.providerOk, true);
  assert.equal(result.providerResults.find((item) => item.provider === "baidu").ok, true);
  assert.equal(result.values.BAIDU_COOKIE.secret, true);
});

test("validateSkillEnv ignores incomplete optional provider when another provider is complete", () => {
  const result = validateSkillEnv({
    QUARK_COOKIE: "cookie",
    QUARK_DEFAULT_SAVE_URL: "not-a-quark-target",
    BAIDU_COOKIE: "BDUSS=abc; STOKEN=secret-token",
    OPENLIST_TOKEN: "token",
    OPENLIST_BASE_URL: "http://127.0.0.1:5244/",
    BAIDU_DEFAULT_SAVE_PATH: "/NAS资源下载",
    OPENLIST_DEFAULT_COPY_DST_PATH: "/影视资源备份/影视"
  });

  assert.equal(result.ok, true);
  assert.equal(result.providerOk, true);
  assert.deepEqual(result.invalid, []);
  assert.equal(result.providerResults.find((item) => item.provider === "quark").ok, false);
});

test("validateSkillEnv reports provider invalid values when no provider is complete", () => {
  const result = validateSkillEnv({
    QUARK_COOKIE: "cookie",
    QUARK_DEFAULT_SAVE_URL: "not-a-quark-target",
    OPENLIST_TOKEN: "token",
    OPENLIST_BASE_URL: "http://127.0.0.1:5244/",
    OPENLIST_DEFAULT_COPY_DST_PATH: "/影视资源备份/影视"
  });

  assert.equal(result.ok, false);
  assert.equal(result.nextAction, "configure_provider");
  assert.deepEqual(result.invalid.map((item) => item.key), ["QUARK_DEFAULT_SAVE_URL"]);
});

test("validateSkillEnv accepts Baidu folder URL as default save target", () => {
  const result = validateSkillEnv({
    BAIDU_COOKIE: "BDUSS=abc; STOKEN=def",
    OPENLIST_TOKEN: "token",
    OPENLIST_BASE_URL: "http://127.0.0.1:5244/",
    BAIDU_DEFAULT_SAVE_PATH:
      "https://pan.baidu.com/disk/main#/index?category=all&path=%2FNAS%E8%B5%84%E6%BA%90%E4%B8%8B%E8%BD%BD",
    OPENLIST_DEFAULT_COPY_DST_PATH: "/影视资源备份/影视"
  });

  assert.equal(result.ok, true);
  assert.equal(
    result.values.BAIDU_DEFAULT_SAVE_PATH.displayValue,
    "https://pan.baidu.com/disk/main#/index?category=all&path=%2FNAS%E8%B5%84%E6%BA%90%E4%B8%8B%E8%BD%BD"
  );
});

test("validateSkillEnv validates URL and OpenList path shapes", () => {
  const result = validateSkillEnv({
    QUARK_COOKIE: "cookie",
    BAIDU_COOKIE: "BDUSS=abc; STOKEN=def",
    OPENLIST_TOKEN: "token",
    OPENLIST_BASE_URL: "not-a-url",
    QUARK_DEFAULT_SAVE_URL: "https://example.com/not-quark",
    BAIDU_DEFAULT_SAVE_PATH: "我的资源/影视",
    OPENLIST_DEFAULT_COPY_DST_PATH: "影视资源备份/影视"
  });

  assert.equal(result.ok, false);
  assert.deepEqual(
    result.invalid.map((item) => item.key).sort(),
    ["BAIDU_DEFAULT_SAVE_PATH", "OPENLIST_BASE_URL", "OPENLIST_DEFAULT_COPY_DST_PATH", "QUARK_DEFAULT_SAVE_URL"].sort()
  );
});

test("maskSecret only reveals a small prefix and suffix", () => {
  assert.equal(maskSecret("1234567890abcdef"), "12345678...cdef");
  assert.equal(maskSecret("short"), "***");
});
