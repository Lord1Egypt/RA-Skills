# learn（网络学堂）接口核验文档

> 已实测验证（2026-08-06）。作为子 SKILL 接口核验的参考模板。
> 开发新系统时，用同样的方法核验各接口的真实返回。

## 登录链路（已验证）

| 步骤 | 方式 | 状态 |
|------|------|:---:|
| CAS 登录 | `login.py --system learn --ensure`（浏览器即用即退 + 两阶段 2FA） | ✅ |
| 信任确认 | 真实点击"确定"（触发 saveFinger JS），非 form.submit/独立 POST | ✅ |
| 免 2FA 复用 | 信任浏览器建立后 `--ensure` 0.2s 返回 | ✅ |
| 信任上限 | saveFinger 返回"信任浏览器数量已达到上限"时，提示去 `id.tsinghua.edu.cn/f/account/trustDeviceIndex` 删旧设备 | ✅ |

## API 接口（learn_api.py，已核验）

| 方法 | 端点 | 返回 | 验证 |
|------|------|------|:---:|
| get_courses | `/b/kc/zhjw_v_code_xnxq/getCurrentAndNextSemester` + 课程列表 | 课程 wlkcid/kcm/jsm | ✅ 真实课程 |
| get_homeworks | `/b/wlxt/kczy/zy/...` | 作业 bt/zt/scsjStr/zyid | ✅ 11 个真实作业 |
| get_files | `/b/wlxt/kj/wlkc_kjxxb/student/kjxxbByWlkcidAndSizeForStudent` | 课件 bt/wjid | ✅ 9 个 PDF（修复 &amp; 解码）|
| get_announcements | 公告列表 | sfyd/bt/fbsjStr | ✅ 空数组正常 |
| todos 汇总 | get_course_detail 聚合 | 未读/未交统计 | ✅ |
| download_file | `/b/wlxt/kj/wlkc_kjxxb/student/downloadFile` | 文件 | 未实测下载 |

## 关键参数

- `wlkcid`：课程 ID（如 `2025-2026-3152188393`）
- `zyid`：作业 ID；`xszyid`：学生作业 ID
- `wjid`：课件 ID
- `csrf`：来自 learn 域 XSRF-TOKEN cookie（新版），非 URL 参数

## 已知坑

1. **课件名 HTML 实体**：文件名含 `&amp;`，需 `html.unescape`（learn_api.py 已修复）
2. **CSRF 来源**：learn 新版 CSRF 在 XSRF-TOKEN cookie，不是 URL `_csrf`
3. **session 时效**：learn session 会过期，`--ensure` 时 `session.session_valid()` 只查字段存在（不真验证）——失效时需重新登录
