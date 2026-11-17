#!/usr/bin/env python3
"""Scaffold a Playwright E2E test from a list of steps.

步骤语法（每步用 `;` 分隔，**动词后必须给出参数**）：

    打开|导航到|访问 <路径>        路径须以 / # ? http:// https:// 开头
    输入|填写|键入 <字段> <值>     两段，缺值不猜
    点击|按下 <按钮名>
    断言跳转|跳转断言 <路径>       只接受 URL 形态
    断言 <路径>                    URL 形态 → toHaveURL
    断言 文本 <文案>               → getByText(...).toBeVisible()

无法解析的步骤**不会被猜测**，一律降级为 `// TODO:` 注释并附提示，
避免生成"能跑但断言错"的假测试（如把动词自身当成 URL）。

Usage:
    python3 scripts/e2e_scaffold.py --name 登录流程 \
        --steps "打开 /login;输入 账号 hope;输入 密码 secret;点击 提交;断言跳转 /dashboard"
    python3 scripts/e2e_scaffold.py --name 登录流程 --steps "..." --output tests/login.spec.ts
"""
import argparse
import re
import sys

# 导航/断言只接受 URL 形态的目标，否则拒绝猜测
URLISH_RE = re.compile(r"^(?:/|\#|\?|https?://)")

NAV_RE = re.compile(r"^(?:打开|导航到|访问)\s*(.*)$")
FILL_RE = re.compile(r"^(?:输入|填写|键入)\s*(.*)$")
CLICK_RE = re.compile(r"^(?:点击|按下)\s*(.*)$")
# 顺序重要：长别名在前，且不允许回退到短别名吞掉后半个词
ASSERT_URL_RE = re.compile(r"^(?:断言跳转|跳转断言|断言URL|断言\s*URL)\s*(.*)$")
ASSERT_ANY_RE = re.compile(r"^断言\s*(.*)$")
ASSERT_TEXT_RE = re.compile(r"^(?:文本|文案|内容|text)\s+(.+)$", re.IGNORECASE)


def esc(value):
    """Escape a value for embedding in a single-quoted TS string literal."""
    return str(value).replace("\\", "\\\\").replace("'", "\\'")


def todo(step, hint=None):
    return f"  // TODO: {step}" + (f"（{hint}）" if hint else "")


def render_step(step):
    s = step.strip()
    if not s:
        return None

    m = NAV_RE.match(s)
    if m:
        target = m.group(1).strip()
        if not target:
            return todo(s, "缺少路径，写成「打开 /login」")
        if not URLISH_RE.match(target):
            return todo(s, f"'{target}' 不是路径，写成「打开 /login」或完整 URL")
        return f"  await page.goto('{esc(target)}');"

    m = FILL_RE.match(s)
    if m:
        rest = m.group(1).strip()
        parts = rest.split(None, 1)
        if len(parts) < 2:
            return todo(s, "缺少值，写成「输入 账号 hope」")
        field, value = parts[0], parts[1].strip()
        if field.startswith("/") or field.startswith("#") or field.startswith("["):
            return f"  await page.locator('{esc(field)}').fill('{esc(value)}');"
        return f"  await page.getByLabel('{esc(field)}').fill('{esc(value)}');"

    m = ASSERT_URL_RE.match(s)
    if m:
        target = m.group(1).strip()
        if not target:
            return todo(s, "缺少路径，写成「断言跳转 /dashboard」")
        if not URLISH_RE.match(target):
            return todo(s, f"'{target}' 不是路径；断言文案请写「断言 文本 {target}」")
        return f"  await expect(page).toHaveURL('{esc(target)}');"

    m = ASSERT_ANY_RE.match(s)
    if m:
        rest = m.group(1).strip()
        if not rest:
            return todo(s, "缺少断言目标，写成「断言跳转 /dashboard」或「断言 文本 已登录」")
        mt = ASSERT_TEXT_RE.match(rest)
        if mt:
            return (f"  await expect(page.getByText('{esc(mt.group(1).strip())}'))"
                    f".toBeVisible();")
        if URLISH_RE.match(rest):
            return f"  await expect(page).toHaveURL('{esc(rest)}');"
        return f"  await expect(page.getByText('{esc(rest)}')).toBeVisible();"

    m = CLICK_RE.match(s)
    if m:
        target = m.group(1).strip()
        if not target:
            return todo(s, "缺少按钮名，写成「点击 提交」")
        return f"  await page.getByRole('button', {{ name: '{esc(target)}' }}).click();"

    return todo(s, "未识别的步骤动词，见脚本 docstring 的步骤语法")


def main():
    ap = argparse.ArgumentParser(description="Scaffold a Playwright E2E test.")
    ap.add_argument("--name", required=True, help="test / flow name")
    ap.add_argument("--steps", required=True, help="semicolon-separated steps")
    ap.add_argument("--output", help="write to file instead of stdout")
    args = ap.parse_args()

    steps = [render_step(s) for s in args.steps.split(";")]
    steps = [s for s in steps if s]
    runnable = [s for s in steps if not s.lstrip().startswith("//")]

    if not steps:
        steps = ["  // TODO: 未解析出任何步骤，检查 --steps 是否用 ';' 分隔"]
    if not runnable:
        print("WARNING: 没有任何步骤被解析成断言/操作，生成的测试体只有 TODO；"
              "空测试会「假绿」，请补全步骤后再纳入 CI。", file=sys.stderr)
    elif len(runnable) < len(steps):
        print(f"WARNING: {len(steps) - len(runnable)}/{len(steps)} 个步骤降级为 TODO，"
              "请按 docstring 的步骤语法补参数。", file=sys.stderr)

    body = "\n".join(steps)

    code = f"""import {{ test, expect }} from '@playwright/test';

test('{esc(args.name)}', async ({{ page }}) => {{
{body}
}});
"""
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(code)
        print(f"written: {args.output}", file=sys.stderr)
    else:
        print(code)


if __name__ == "__main__":
    main()
