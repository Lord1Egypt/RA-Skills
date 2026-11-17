#!/usr/bin/env python3
# wb_api_checkin.py —— WorkBuddy「Buddy 加油站」API 直连签到（零 GUI 依赖）
# ============================================================================
# 方案背景(2026-08-18 老板要求补齐):
#   SkillHub 上的 workbuddy-checkin / workbuddy-daily-checkin 都是 API 直连方案,
#   比坐标点击更稳(无窗口位置/DPI/更新横幅遮挡问题)。本脚本实现同款:
#   读 WorkBuddy 桌面端本地登录态(auth .info 文件, 明文 JSON 含 JWT accessToken)
#   -> 调官方接口 POST https://copilot.tencent.com/billing/meter/* 完成签到。
#
# 接口(从 app.asar 逆向确认, 与社区披露一致):
#   POST /billing/meter/checkin-status   查询签到状态(只读)
#   POST /billing/meter/daily-checkin    每日签到(幂等: 已签返回 code 10001)
#   POST /billing/meter/get-user-resource 套餐信息(只读)
# 认证: Authorization: Bearer <accessToken>  (HttpService 拦截器同款)
#
# 用法:
#   python wb_api_checkin.py        # 查询状态+未签则领取, 输出结论, 退出码 0/2
#   python wb_api_checkin.py -status   # 仅查询, 不领取
#
# 退出码: 0=成功/已签过   2=失败(token缺失/接口异常/领取失败)
#
# 【隐私说明】仅读取本机登录态并调用官方接口, 凭据不落盘不外发。
# ============================================================================

import glob, json, os, sys, urllib.request, urllib.error

# WorkBuddy 桌面端登录态文件(2026-08-18 逆向定位: sharedDataPath/auth/<id>.info)
AUTH_FILE = os.path.join(os.path.expanduser("~"), "AppData", "Local",
                         "CodeBuddyExtension", "Data", "Public", "auth",
                         "workbuddy-desktop.info")
# 兜底: 腾讯云登录态(同一账号体系)
AUTH_FILE_FALLBACK = os.path.join(os.path.expanduser("~"), "AppData", "Local",
                                  "CodeBuddyExtension", "Data", "Public", "auth",
                                  "Tencent-Cloud.coding-copilot.info")
# 后端 host(逆向自 app.asar: getFullUrl = window.location.origin + path,
# 前端 origin = https://copilot.tencent.com, 已验证可通)
BASE = "https://copilot.tencent.com"
# v2 新端点(2026-09-29 实测, 与 totorosir-workbuddy-score 同源):
#   域名取登录态 auth.domain(缺省 www.codebuddy.cn), 数据比旧端点真实
#   (旧端点在活动期外会返回 连续0/激活False 的假数据, 已签状态也可能不准)
BASE_V2 = "https://www.codebuddy.cn"
STATUS_PATH_V2 = "/v2/billing/meter/checkin-activity-status"
CHECKIN_PATH_V2 = "/v2/billing/meter/daily-checkin"
TIMEOUT = 20
# 服务端按 UA 区分请求来源, 非浏览器 UA 直接裸 400(2026-08-18 实测坑), 必须带浏览器 UA
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# ----------------------------------------------------------------------------
# 5.6.2+ 加密登录态兼容(2026-09-29 新增):
#   新版 WorkBuddy 把 auth.accessToken 改为 AES-256-GCM 信封 {"$wbEncrypted":1,...},
#   静态钥 atRestSecretKey 运行时驻留 WorkBuddy.exe 进程内存(磁盘无明文),
#   需多级密钥发现(环境变量->密钥文件->DPAPI/进程内存扫描->CDP)才能解密。
#   本脚本不重复造轮子, 复用市场 skill totorosir-workbuddy-score 的解密引擎
#   (buddy_station.load_credentials, MIT-0): import 失败/未安装时明确报错 exit 2,
#   由调用方回退 GUI 兜底方案, 行为与旧版"无登录态"一致。
# ----------------------------------------------------------------------------
_bs_mod = None  # 缓存已加载的 buddy_station 模块


def _load_decrypt_engine():
    """尝试 import totorosir-workbuddy-score 的 buddy_station 作解密引擎。"""
    global _bs_mod
    if _bs_mod is not None:
        return _bs_mod
    candidates = glob.glob(os.path.join(
        os.path.expanduser("~"), ".workbuddy", "skills",
        "totorosir-workbuddy-score*", "scripts"))
    if not candidates:
        print("[auth] 未找到解密引擎(totorosir-workbuddy-score skill 未安装), "
              "无法解密 5.6.2+ 加密登录态。")
        _bs_mod = False
        return _bs_mod
    sys.path.insert(0, candidates[0])
    try:
        import buddy_station  # noqa: PLC0415
        _bs_mod = buddy_station
    except Exception as e:
        print(f"[auth] 解密引擎 import 失败: {e}")
        _bs_mod = False
    return _bs_mod


def get_token():
    """读登录态文件拿 accessToken, 自动识别明文/5.6.2+ 加密信封。
    返回 (token, 来源路径) 或 (None, None)。"""
    for path in (AUTH_FILE, AUTH_FILE_FALLBACK):
        if not os.path.exists(path):
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                d = json.load(fh)
        except Exception:
            continue
        t = (d.get("auth") or {}).get("accessToken")
        if not t:
            continue
        if isinstance(t, str):          # 明文 JWT(旧客户端)
            return t, path
        if isinstance(t, dict) and t.get("$wbEncrypted"):  # 5.6.2+ 信封
            eng = _load_decrypt_engine()
            if not eng:
                return None, None
            try:
                token, _domain = eng.load_credentials(path)
                print("[auth] 加密登录态已解密(5.6.2+ 兼容引擎)。")
                return token, path
            except Exception as e:
                print(f"[auth] 加密登录态解密失败: {e}")
                return None, None
    return None, None


def call(path, token, body=None, base=None):
    """POST 官方接口。返回解析后的 JSON dict(含 HTTPError 时读 body 业务码)。"""
    req = urllib.request.Request(
        (base or BASE) + path,
        data=json.dumps(body or {}).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + token,
                 "User-Agent": UA,
                 "Accept-Language": "zh"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # 业务错误也走 HTTP 400, 但 body 是 JSON 业务码(如 10001=已签到)
        try:
            return json.loads(e.read().decode("utf-8"))
        except Exception:
            return {"code": e.code, "msg": "HTTP " + str(e.code)}
    except Exception as e:
        return {"code": -1, "msg": str(e)}


def main():
    status_only = "-status" in sys.argv
    token, src = get_token()
    if not token:
        print("ERROR: 未取得可用 accessToken(登录态缺失, 或 5.6.2+ 加密且解密引擎不可用)。")
        print(f"  查找路径: {AUTH_FILE}")
        print("  请确认 WorkBuddy 桌面端已登录; 仍失败请回退 GUI 兜底方案。")
        return 2
    print(f"[auth] 登录态: {src}")

    # 优先 v2 新端点(真实数据), 失败回退旧端点
    st = call(STATUS_PATH_V2, token, base=BASE_V2)
    use_v2 = st.get("code") == 0
    if not use_v2:
        print(f"[status] v2 端点不可用({st.get('msg', st.get('code'))}), 回退旧端点...")
        st = call("/billing/meter/checkin-status", token)
    if st.get("code") != 0:
        print(f"[status] 查询签到状态失败: {st}")
        return 2
    data = st.get("data") or {}
    today_checked = bool(data.get("today_checked_in"))
    streak = data.get("streak_days") or 0
    total = data.get("total_credits")
    total_s = f" | 总积分: {total}" if total is not None else ""
    print(f"[status] 今日已签: {today_checked} | 连续天数: {streak} | "
          f"今日积分: {data.get('today_credit') or 0}{total_s} | "
          f"端点: {'v2' if use_v2 else 'legacy'}")

    if today_checked:
        print("== 结论: 今日已签到, 无需领取 ==")
        return 0
    if status_only:
        print("== 结论: 今日未签到(-status 仅查询, 未领取) ==")
        return 0

    print("[checkin] 今日未签到, 调用 daily-checkin 领取...")
    r = (call(CHECKIN_PATH_V2, token, base=BASE_V2) if use_v2
         else call("/billing/meter/daily-checkin", token))
    code = r.get("code")
    if code == 0:
        d2 = r.get("data") or {}
        credit = d2.get("credit") or d2.get("today_credit") or 0
        streak2 = d2.get("streakDays") or d2.get("streak_days") or 0
        print(f"== 结论: 签到成功! 积分 {credit}, 连续 {streak2} 天 ==")
        return 0
    if code == 10001:
        print("== 结论: 今日已签到(接口幂等返回) ==")
        return 0
    print(f"== 结论: 签到失败: {r} ==")
    return 2


if __name__ == "__main__":
    sys.exit(main())
