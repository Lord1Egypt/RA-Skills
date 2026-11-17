# MIT License

Copyright (c) 2026 三剪客

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 附加说明

本技能包（`sanjianke-a7w-bridge`）是**本地协议适配层**，本身不提供任何 AI 能力。

- 桥只把请求转发到 `api.a7w.cn`，不缓存、不落盘、不外传数据到其他地址。
- API Key 从本机 `~/.a7w/config.json` 或环境变量读取，**代码内不内嵌任何密钥**。
- 桥默认仅监听 `127.0.0.1`，不对外暴露、不含鉴权。若要供局域网或公网使用，
  使用者需自行加鉴权、HTTPS 与访问控制，并自行承担由此产生的风险。
- 算力集市的能力、计费与可用性以平台为准；本包不对上游故障负责。
- 接入第三方开源项目时，请自行核对其许可证（部分为 AGPL / 非商用许可）。
