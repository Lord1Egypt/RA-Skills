# v16 引擎接入清单 + 双重注册检查

**v16 实战教训**：6/2 给搜狗加 site:bing 代理时，复制 `weixin` 行忘加 HTTP 解析器，sogou 变成只注册 URL 没注册 parser。deep mode 触发 KeyError，stderr 一直刷。

## 4 个映射表必须**全**对齐

新加一个引擎 alias 时，**4 个字典都要写一行**（不写就跑 KeyError）：

| 字典 | 作用 | 缺它会怎样 |
|:-----|:-----|:-----------|
| `HTTP_BASE_URLS` | 引擎 → 搜索 URL 模板 | 不写：跑 deep mode 不会触发此引擎 |
| `HTTP_PARSERS` | 引擎 → 解析函数 | 不写：**KeyError 反复刷 stderr**（v16 修复的就是这个） |
| `PW_BASE_URLS` | Playwright 引擎 URL | 不写：此引擎不会进 PW 段 |
| `PW_PARSERS` | Playwright 引擎解析 | 不写：PW 段 KeyError |

引擎走 HTTP 还是 PW 取决于你想跑哪种协议；v15+ 大量 site:bing 代理**只走 HTTP**，但有些引擎（如 weixin）**两边都注册**（HTTP 段 weixin_bing + PW 段 weixin_pw）。

## 新增引擎的 6 步流程

1. **探测 site:bing 是否有效**（用 `references/v15-site-bing-probe-results.md` 的脚本）
2. 在 `HTTP_BASE_URLS` 加一行
3. 在 `HTTP_PARSERS` 加一行（**v16 关键！忘写必 KeyError**）
4. **smoke test 前先 diff 4 个 dict 长度**（见下）
5. smoke test：`python3 search.py "测试 query" --engine <新引擎> --top 3` 看有没有 KeyError
6. 写 `references/<新引擎>-probe.md` 记录该域的稳定性数据

## 验证 4 个 dict 的内联检查

新加完引擎提交前一行命令必跑：

```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
import search
http_engines = set(search.HTTP_BASE_URLS) - set(search.PW_BASE_URLS)
pw_engines = set(search.PW_BASE_URLS) - set(search.HTTP_BASE_URLS)
errors = []
for e in http_engines:
    if e not in search.HTTP_PARSERS:
        errors.append(f'❌ {e} 在 HTTP_BASE_URLS 但 HTTP_PARSERS 无')
for e in pw_engines:
    if e not in search.PW_PARSERS:
        errors.append(f'❌ {e} 在 PW_BASE_URLS 但 PW_PARSERS 无')
for e in search.HTTP_PARSERS:
    if e not in search.HTTP_BASE_URLS:
        errors.append(f'⚠️ {e} 在 HTTP_PARSERS 但 HTTP_BASE_URLS 无')
for e in search.PW_PARSERS:
    if e not in search.PW_BASE_URLS:
        errors.append(f'⚠️ {e} 在 PW_PARSERS 但 PW_BASE_URLS 无')
print('OK' if not errors else 'ERRORS:\n' + '\n'.join(errors))
"
```

预期（v16 修复后）：`OK`

## 历史 bug 档案

| 日期 | 引擎 | Bug | 修复 |
|:-----|:-----|:----|:-----|
| 2026-06-02 | sogou | `HTTP_BASE_URLS` 注册了但 `HTTP_PARSERS` 没注册 | 删 `HTTP_BASE_URLS` 那行（sogou 走 PW 即可）|