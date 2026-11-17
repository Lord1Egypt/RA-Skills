"use strict";

const assert = require("assert");
const { createSecureAxios } = require("../scripts/axios_secure");

const http = createSecureAxios({ proxy: { host: "127.0.0.1", port: 8080 } });

assert.equal(
  http.defaults.proxy,
  false,
  "问卷网统一请求器必须禁用环境代理和调用方代理覆盖"
);
assert.ok(http.defaults.httpsAgent, "必须使用受控 HTTPS Agent");

console.log("secure axios proxy regression test passed");
