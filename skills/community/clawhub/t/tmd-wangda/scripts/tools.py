import json, sys, os, asyncio
from dotenv import find_dotenv, load_dotenv
from session_tools import (
    get_session,
    reset_session,
    add_progress,
    set_session,
    get_next_course,
    remove_session_file,
)
from subject_tools import get_url_type, parse, skip_to_uncompleted_chapter
from chrome_tools import navi, NeedLoginError, _get_current_url_silent, kill_chrome
from login_tools import fill_phone, fill_sms_code, get_employee_name
import platform, time
import subprocess

load_dotenv(find_dotenv(), override=True)


def getSession(key=None):
    """
    获取现有session的完整信息，或某个字段的信息

    Args:
        key: 可选，session的某个字段名

    Returns:
        完整session或某个字段的信息
    """
    value = get_session(key)
    print(json.dumps(value, ensure_ascii=False, indent=2))
    return value


def resetSession():
    """
    重置session

    Returns:
        重置后的session完整内容
    """
    print(json.dumps(reset_session(), ensure_ascii=False, indent=2))


def addSubject(subjectUrl):
    """
    向session的progress中添加新的待学习课程信息

    Args:
        subjectUrl: 课程URL

    Returns:
        在progress添加的subject的信息
    """

    # 使用subject_tools.get_url_type 判断url类型，如果不是subject类型抛出异常
    url_type = get_url_type(subjectUrl)
    if url_type == "other" or url_type == "course":
        raise ValueError(f"无效的URL: {subjectUrl}，不是有效的课程地址")

    # 使用chrome_tools.navi, 先导航到subject页面，如果需要登录，抛出需要登录的异常
    try:
        navi(subjectUrl)
    except NeedLoginError as e:
        raise NeedLoginError(f"需要登录才能访问该课程: {e}")

    # 使用subject_tools.parse(url,False)解析课程信息
    subject_info = parse(subjectUrl, should_navi=False)
    if not subject_info:
        raise RuntimeError(f"解析课程信息失败: {subjectUrl}")

    # 使用session_tools.add_progress添加课程信息
    subject_json = json.dumps(subject_info, ensure_ascii=False)
    add_progress(subject_json)

    # 返回加入progress的subject信息
    print(json.dumps(subject_info, ensure_ascii=False, indent=2))
    return subject_info


def _setup_cron_task(script_path, python_cmd, interval_min):
    """macOS/Linux: 设置 cron 定时任务（已存在且间隔相同则跳过）"""

    cron_tag = "#WANGDA_MONITOR"
    # 加引号防止路径中有空格；先激活 venv 再执行
    venv_dir = os.environ.get("_WANGDA_PYTHON_VENV_DIR", "")
    if venv_dir:
        activate = f'source "{venv_dir}/bin/activate" && '
    else:
        activate = ""
    cron_cmd = f'cd "{script_path}" && {activate}"{python_cmd}" tools.py monitor-hook'
    cron_line = f"*/{interval_min} * * * * {cron_cmd} {cron_tag}"

    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        existing = result.stdout if result.returncode == 0 else ""
    except Exception:
        existing = ""

    # 检查是否已有完全相同的任务
    existing_lines = [line for line in existing.strip().split("\n") if line.strip()]
    for line in existing_lines:
        if cron_tag in line:
            if line.strip() == cron_line.strip():
                print(
                    f"Cron 定时任务已存在且间隔相同（每{interval_min}分钟），无需重复添加"
                )
                return
            else:
                print(f"Cron 定时任务已存在但间隔不同，更新为每{interval_min}分钟")
                break

    # 移除旧的 WANGDA_MONITOR 任务，添加新任务
    new_lines = [line for line in existing_lines if cron_tag not in line]
    new_lines.append(cron_line)
    subprocess.run(
        ["crontab", "-"],
        input="\n".join(new_lines) + "\n",
        capture_output=True,
        text=True,
    )
    print(f"Cron 定时任务已设置: 每{interval_min}分钟执行一次监控")


def _setup_schtasks(script_path, python_cmd, interval_min):
    """Windows: 设置 schtasks 定时任务（已存在且间隔相同则跳过）"""
    import subprocess

    task_name = "WangdaMonitor"
    # 加引号防止路径中有空格；先激活 venv 再执行
    venv_dir = os.environ.get("_WANGDA_PYTHON_VENV_DIR", "")
    if venv_dir:
        activate = f'"{venv_dir}\\Scripts\\activate.bat" && '
    else:
        activate = ""
    cmd = f'cd /d "{script_path}" && {activate}"{python_cmd}" tools.py monitor-hook'

    # 查询是否已有同名任务
    query = subprocess.run(
        ["schtasks", "/query", "/tn", task_name, "/v", "/fo", "LIST"],
        capture_output=True,
        text=True,
    )
    if query.returncode == 0:
        # 任务已存在，检查间隔是否相同
        # schtasks 输出中形如 "Repeat: Every: 0 Hour(s), 5 Minute(s)"
        output = query.stdout
        if f"{interval_min} Minute" in output or f"0:{interval_min:02d}:00" in output:
            print(
                f"Windows 定时任务已存在且间隔相同（每{interval_min}分钟），无需重复添加"
            )
            return
        else:
            print(f"Windows 定时任务已存在但间隔不同，更新为每{interval_min}分钟")

    # 删除旧任务（忽略不存在的情况）
    subprocess.run(
        ["schtasks", "/delete", "/tn", task_name, "/f"], capture_output=True, text=True
    )
    # 创建新任务
    result = subprocess.run(
        [
            "schtasks",
            "/create",
            "/tn",
            task_name,
            "/tr",
            cmd,
            "/sc",
            "MINUTE",
            "/mo",
            str(interval_min),
            "/f",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"Windows 定时任务已设置: 每{interval_min}分钟执行一次监控")
    else:
        print(f"设置定时任务失败: {result.stderr}")


def _remove_cron_task():
    """macOS/Linux: 仅移除 WANGDA_MONITOR 相关的 cron 定时任务"""
    import subprocess

    cron_tag = "#WANGDA_MONITOR"
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            existing_lines = [
                line for line in result.stdout.strip().split("\n") if line.strip()
            ]
            has_monitor = any(cron_tag in line for line in existing_lines)
            if not has_monitor:
                print("没有找到 WANGDA_MONITOR 定时任务")
                return
            # 仅保留非 WANGDA_MONITOR 的任务
            keep_lines = [line for line in existing_lines if cron_tag not in line]
            new_cron = "\n".join(keep_lines) + "\n" if keep_lines else ""
            subprocess.run(
                ["crontab", "-"], input=new_cron, capture_output=True, text=True
            )
            print("Cron 定时任务已移除（仅移除 WANGDA_MONITOR）")
        else:
            print("没有找到定时任务")
    except Exception as e:
        print(f"移除定时任务失败: {e}")


def _remove_schtasks():
    """Windows: 仅移除 WangdaMonitor 定时任务"""
    import subprocess

    task_name = "WangdaMonitor"
    result = subprocess.run(
        ["schtasks", "/delete", "/tn", task_name, "/f"], capture_output=True, text=True
    )
    if result.returncode == 0:
        print("Windows 定时任务已移除（仅移除 WangdaMonitor）")
    else:
        print("没有找到 WangdaMonitor 定时任务")


def startAutoStudy():
    # 基于操作用户的操作系统(例如mac和linux就是cron)，根据环境变量_WANGDA_CHECK_INTERVAL（单位秒），设置定时任务
    # 执行python/python3 ${script_path}/tools.py monitor指令,注意这个script_path

    from datetime import datetime

    # 1. 获取下一个待学习的课件
    next_course = get_next_course()
    if not next_course:
        print("没有需要学习的课件")
        return None

    # 2. 导航到课件页面
    course_url = next_course.get("url")
    if not course_url:
        print("课件URL不存在")
        return None

    print(f"开始学习课件: {next_course.get('name', 'Unknown')}")
    try:
        navi(course_url)
    except NeedLoginError:
        print("需要先登录")
        raise

    time.sleep(3)

    # 3. 解析课件并跳转到未完成章节
    course_info = parse(course_url, should_navi=False)
    if course_info and not course_info.get("completed", False):
        add_progress(json.dumps(course_info, ensure_ascii=False))
        skip_to_uncompleted_chapter(course_info)

    # 4. 设置定时任务
    interval = int(os.environ.get("_WANGDA_CHECK_INTERVAL", "300"))
    script_path = os.path.dirname(os.path.abspath(__file__))
    python_cmd = sys.executable or "python3"
    interval_min = max(1, interval // 60)

    if platform.system() == "Windows":
        _setup_schtasks(script_path, python_cmd, interval_min)
    else:
        _setup_cron_task(script_path, python_cmd, interval_min)

    # 5. 更新 session 状态
    set_session("auto_study", "true")
    set_session("auto_study_start_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    print(json.dumps(next_course, ensure_ascii=False, indent=2))
    return next_course


def stopStudy():
    """
    停止学习（删除操作系统的定时任务）
    """
    import platform

    if platform.system() == "Windows":
        _remove_schtasks()
    else:
        _remove_cron_task()

    set_session("auto_study", "false")


async def monitorHook():
    """
    用于被定时调用的学习监控钩子
    （检查1.登录状态是否失效 2.更新学习进度 3.如果当前课件已学完，自动进入下一个）
    """
    from datetime import datetime

    def update_monitor_status(status, message=""):
        """更新监控状态和时间"""
        set_session("monitor_status", status)
        set_session("last_monitor_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if message:
            print(message)

    try:
        # 1. 获取当前 URL 并判断类型
        current_url = _get_current_url_silent()
        url_type = get_url_type(current_url) if current_url else "other"

        # 2. 如果不是课件页，获取下一个待学习的课件并导航
        if url_type != "course":
            print(f"当前不在课件页，URL类型: {url_type}")
            next_course = get_next_course()

            if not next_course:
                # 所有课程都已完成
                print("所有课程已完成学习")
                session = get_session()
                if session:
                    session["completed"] = True
                    # 标记所有 subject 和 course 为已完成
                    progress = session.get("progress", {})
                    for subject in progress.get("subjects", []):
                        subject["completed"] = True
                        for course in subject.get("courses", []):
                            course["completed"] = True
                    # 保存更新后的 session
                    set_session("progress", json.dumps(progress, ensure_ascii=False))
                    set_session("completed", "true")
                stopStudy()
                return

            # 导航到下一个课件
            course_url = next_course.get("url")
            if course_url:
                print(f"准备学习课件: {next_course.get('name', 'Unknown')}")
                try:
                    navi(course_url)
                except NeedLoginError:
                    update_monitor_status("error_need_login", "需要重新登录")
                    return

        # 3. 现在应该在课件页了，解析并更新学习状态
        current_url = _get_current_url_silent()
        if get_url_type(current_url) == "course":
            # 解析当前课件信息
            course_info = parse(current_url, should_navi=False)
            if course_info:
                # 更新 session 中的课程进度
                course_json = json.dumps(course_info, ensure_ascii=False)
                add_progress(course_json)

                # 如果当前课件已完成，获取下一个
                if course_info.get("completed", False):
                    print(f"课件已完成: {course_info.get('name')}")
                    next_course = get_next_course()
                    if next_course and next_course.get("url"):
                        try:
                            navi(next_course.get("url"))
                        except NeedLoginError:
                            update_monitor_status("error_need_login", "需要重新登录")
                            return
                        # 进入新课件后，解析并跳转到未完成章节
                        new_course_info = parse(
                            next_course.get("url"), should_navi=False
                        )
                        if new_course_info and not new_course_info.get(
                            "completed", False
                        ):
                            skip_to_uncompleted_chapter(new_course_info)
                    elif not next_course:
                        # 所有课程完成
                        print("所有课程已完成学习")
                        stopStudy()
                        return
                else:
                    # 课件未完成，跳转到第一个未完成的章节
                    skip_to_uncompleted_chapter(course_info)

        # 4. 更新监控状态为正常
        update_monitor_status("normal", "监控检查完成，状态正常")

    except Exception as e:
        print(f"监控钩子执行出错: {e}")
        update_monitor_status("error", f"执行异常: {str(e)}")
        raise


def enterLoginPage():
    """
    进入登录页面
    """
    navi("https://wangda.chinamobile.com/oauth/#login/nodata")
    return True


async def fillPhone(phoneNumber):
    """
    填充手机号至登录页面，并发送验证码

    Args:
        phoneNumber: 手机号

    Returns:
        发送验证码成功或失败
    """
    await fill_phone(phoneNumber)
    print("手机填写成功,验证码已经发送")
    return True


async def fillSmsCode(codeNumber):
    """
    填充验证码至登录页面，并尝试登录

    Args:
        codeNumber: 验证码

    Returns:
        登录成功或失败
    """
    await fill_sms_code(codeNumber)
    print("验证码填写成功,登录成功")
    return True


def updateEmployeeName():
    """
    分析网大的用户信息页，自动更新session中的employeeName

    Returns:
        抓取到的员工姓名
    """
    employee_name = asyncio.run(get_employee_name())
    set_session("employeeName", employee_name)
    return employee_name


async def clear():
    stopStudy()
    kill_chrome()
    remove_session_file()
    print("已经终止所有课程学习(删除session文件，关闭chrome浏览器，清除定时任务)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="网大课程工具集")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # get-session command
    get_session_cmd = subparsers.add_parser("get-session", help="获取当前session")
    get_session_cmd.add_argument(
        "key", nargs="?", type=str, help="session字段名（可选）"
    )

    # reset-session command
    subparsers.add_parser("reset-session", help="重置session")

    # add-subject command
    add_subject_cmd = subparsers.add_parser("add-subject", help="添加待学习课程")
    add_subject_cmd.add_argument("subject_url", type=str, help="课程URL")

    # start-auto-study command
    subparsers.add_parser("start-auto-study", help="开始自动学习")

    # stop-study command
    subparsers.add_parser("stop-study", help="停止学习")

    # monitor-hook command
    subparsers.add_parser("monitor-hook", help="学习监控钩子")

    subparsers.add_parser(
        "clear", help="中断现有的学习,包括删除session问价/删除监控任务/关闭浏览器"
    )

    # enter-login-page command
    subparsers.add_parser("enter-login-page", help="进入登录页面")

    # fill-phone command
    fill_phone_cmd = subparsers.add_parser("fill-phone", help="填充手机号并发送验证码")
    fill_phone_cmd.add_argument("phone_number", type=str, help="手机号")

    # fill-sms-code command
    fill_sms_cmd = subparsers.add_parser("fill-sms-code", help="填充验证码并登录")
    fill_sms_cmd.add_argument("code_number", type=str, help="验证码")

    # update-employee-name command
    subparsers.add_parser("update-employee-name", help="更新员工姓名")

    args = parser.parse_args()

    if args.command == "get-session":
        getSession(args.key)
    elif args.command == "reset-session":
        resetSession()
    elif args.command == "add-subject":
        addSubject(args.subject_url)
    elif args.command == "start-auto-study":
        startAutoStudy()
    elif args.command == "stop-study":
        stopStudy()
    elif args.command == "monitor-hook":
        asyncio.run(monitorHook())
    elif args.command == "clear":
        asyncio.run(clear())
    elif args.command == "enter-login-page":
        enterLoginPage()
    elif args.command == "fill-phone":
        asyncio.run(fillPhone(args.phone_number))
    elif args.command == "fill-sms-code":
        asyncio.run(fillSmsCode(args.code_number))
    elif args.command == "update-employee-name":
        employee_name = updateEmployeeName()
        print(employee_name)
    else:
        parser.print_help()
