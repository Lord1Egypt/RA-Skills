#!/usr/bin/env python3
"""SkillQA Pro — autonomous QA and certification for agent skills (OpenClaw/ClawHub).

Usage:
    python3 skillqa.py test <path> [--lang ru|en] [--skip a,b] [--load N]
                              [--parallel [N]] [--timeout S] [--demo|--pro]
                              [--config]
    python3 skillqa.py selftest [--lang ru|en] [--timeout S] [--load N]
    python3 skillqa.py license --install <file> | --status | --machine-id
    python3 skillqa.py config
    python3 skillqa.py version

Exit codes: 0 = no failures, 1 = failures found, 2 = usage error,
            3 = license missing/invalid for --pro.
"""

import argparse
import hashlib
import hmac
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.2.8"
TOOL = "skillqa"

# ---------------------------------------------------------------------------
# Licensing (ViBo-style: license file + machine-id binding)
# ---------------------------------------------------------------------------
LICENSE_SECRET = "skillqa-pro::local-edition::2026"
LICENSE_DIR = Path.home() / ".config" / "skillqa"
LICENSE_FILE = LICENSE_DIR / "skillqa_license.dat"
LICENSE_ALT_NAMES = ["skillqa_license.dat"]

BANNER = r"""
  ███████╗██╗  ██╗██╗██╗     ██╗      ██████╗  █████╗     ██████╗ ██████╗  ██████╗
  ██╔════╝██║ ██╔╝██║██║     ██║      ██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔═══██╗
  ███████╗█████╔╝ ██║██║     ██║      ██████╔╝███████║    ██████╔╝██████╔╝██║   ██║
  ╚════██║██╔═██╗ ██║██║     ██║      ██╔═══╝ ██╔══██║    ██╔══██╗██╔══██╗██║   ██║
  ███████║██║  ██╗██║███████╗███████╗ ██║     ██║  ██║    ██████╔╝██████╔╝╚██████╔╝
  ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝ ╚═╝     ╚═╝  ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝
"""


# ---------------------------------------------------------------------------
# machine-id / license
# ---------------------------------------------------------------------------
def machine_id():
    """sha256 of the first available machine id source, first 16 hex chars."""
    for p in ("/etc/machine-id", "/var/lib/dbus/machine-id"):
        try:
            val = Path(p).read_text(encoding="utf-8").strip()
            if val:
                return hashlib.sha256(val.encode()).hexdigest()[:16]
        except OSError:
            pass
    val = socket.gethostname()
    return hashlib.sha256(val.encode()).hexdigest()[:16]


def _license_canonical(lic):
    return f"{lic['machine_id']}|{lic['edition']}|{lic['expires']}"


def _license_sign(lic):
    return hmac.new(LICENSE_SECRET.encode(),
                    _license_canonical(lic).encode(),
                    hashlib.sha256).hexdigest()


def _license_paths():
    paths = [LICENSE_FILE]
    for alt in LICENSE_ALT_NAMES:
        for base in (Path.cwd(), Path(__file__).resolve().parent):
            paths.append(base / alt)
    return paths


def license_status():
    """Returns (status, edition, expires, path). status: valid | no_license |
    bad_signature | wrong_machine | expired."""
    for path in _license_paths():
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return ("bad_signature", "pro", None, path)
        try:
            lic = {"machine_id": str(data["machine_id"]),
                   "edition": str(data["edition"]),
                   "expires": str(data["expires"])}
            sig = str(data["sig"])
        except KeyError:
            return ("bad_signature", "pro", None, path)
        if not hmac.compare_digest(_license_sign(lic), sig):
            return ("bad_signature", lic["edition"], lic["expires"], path)
        if lic["machine_id"] != machine_id():
            return ("wrong_machine", lic["edition"], lic["expires"], path)
        if lic["expires"] < datetime.now().strftime("%Y-%m-%d"):
            return ("expired", lic["edition"], lic["expires"], path)
        return ("valid", lic["edition"], lic["expires"], path)
    return ("no_license", None, None, None)


def install_license_file(src_path, parser):
    """Validate and install a license file (bound to this machine)."""
    try:
        data = json.loads(Path(src_path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        parser.error(f"cannot read license file {src_path}: {e}")
    for k in ("machine_id", "edition", "expires", "sig"):
        if k not in data:
            parser.error(f"license file missing field: {k}")
    lic = {k: str(data[k]) for k in ("machine_id", "edition", "expires")}
    if not hmac.compare_digest(_license_sign(lic), str(data["sig"])):
        print("[license] ERROR: bad signature", file=sys.stderr)
        return 3
    if lic["machine_id"] != machine_id():
        print(f"[license] ERROR: license is bound to another machine "
              f"({lic['machine_id']} != {machine_id()})", file=sys.stderr)
        return 3
    LICENSE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src_path, LICENSE_FILE)
    print(f"⚠️ License stored at {LICENSE_FILE} (machine-bound to this host: "
          f"reads /etc/machine-id, hashed). Remove the file to uninstall.")
    print(f"[license] installed to {LICENSE_FILE}")
    print(f"[license] edition={lic['edition']} expires={lic['expires']}")
    return 0


def install_test_license():
    """Generate a local test license for the current machine (selftest)."""
    lic = {"machine_id": machine_id(), "edition": "pro",
           "expires": "2099-12-31"}
    lic["sig"] = _license_sign(lic)
    LICENSE_DIR.mkdir(parents=True, exist_ok=True)
    LICENSE_FILE.write_text(json.dumps(lic, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# i18n
# ---------------------------------------------------------------------------
I18N = {
    "ru": {
        "module.summary": "Итог: {total} проверок, {fail} fail, {warn} warn",
        "check.no_skilmd": "нет SKILL.md — проверка пропущена",
        "check.skilmd_exists.missing": "SKILL.md не найден",
        "check.skilmd_exists.empty": "SKILL.md пуст или слишком мал ({size} байт, нужно > 200)",
        "check.skilmd_exists.ok": "SKILL.md найден, {size} байт",
        "check.skilmd_exists.unreadable": "SKILL.md не читается: {err}",
        "check.frontmatter_valid.missing": "блок frontmatter (---) не найден",
        "check.frontmatter_valid.fail": "невалидный YAML-заголовок: {err}",
        "check.frontmatter_valid.ok": "валидный YAML-заголовок",
        "check.frontmatter_fields.fail": "отсутствуют обязательные поля: {fields}",
        "check.frontmatter_fields.ok": "обязательные поля (name, description, version, tools) на месте",
        "check.frontmatter_fields.warn": "нет поля tools/allowed-tools",
        "check.frontmatter_fields.warn_version": "нет version (рекомендуется для маркетплейсов, не обязательно)",
        "check.frontmatter_fields.nofm": "frontmatter отсутствует — поля не проверены",
        "check.referenced_paths_exist.fail": "отсутствуют файлы, упомянутые в SKILL.md: {paths}",
        "check.referenced_paths_exist.internal": "ссылки на файлы проекта вне скилла (внутренний скилл)",
        "check.referenced_paths_exist.warn": "в примерах упомянуты, но отсутствуют: {paths}",
        "check.referenced_paths_exist.ok": "все упомянутые пути существуют ({n})",
        "check.no_empty_broken_files.fail": "пустые/битые файлы: {files}",
        "check.no_empty_broken_files.warn": "крупные бинарники в корне: {files}",
        "check.no_empty_broken_files.ok": "нет пустых или битых файлов",
        "check.no_magic_paths.fail": "абсолютные магические пути в SKILL.md: {paths}",
        "check.no_magic_paths.warn": "в SKILL.md есть пути с ~/ (непортируемо)",
        "check.no_magic_paths.ok": "нет абсолютных магических путей",
        "check.reasonable_sizes.warn": "файлы больше 5 МБ: {files}",
        "check.reasonable_sizes.ok": "все файлы в пределах лимитов",
        "check.version_consistent.notsemver": "версия {v} не соответствует semver (X.Y.Z)",
        "check.version_consistent.mentions": "версии в тексте SKILL.md различаются: {mentions}",
        "check.version_consistent.ok": "версия {v} согласована",
        "check.version_consistent.internal": "история версий во внутренней документации",
        "check.version_consistent.noversion": "версия не указана",
        "check.scripts_discovered.none": "исполняемых скриптов (*.py/*.sh/*.js) не найдено",
        "check.scripts_discovered.summary": "исполняемых скриптов не найдено",
        "check.run.timeout": "завис: убит по таймауту {s} c (SIGTERM/SIGKILL)",
        "check.run.warn": "exit 0, но stderr непуст, или usage",
        "check.run.env": "не хватает зависимости/интерпретатора (окружение), не дефект скилла",
        "check.run.ok": "exit 0, stderr пуст ({ms} мс)",
        "check.run.fail": "exit {code} или необработанное исключение",
        "check.help.timeout": "--help завис: убит по таймауту {s} c",
        "check.help.ok": "--help отрабатывает, exit 0",
        "check.help.warn": "exit {code}, но usage/help выводится",
        "check.help.crash": "--help упал с traceback",
        "check.help.fail": "--help не сработал (exit {code})",
        "check.noargs.timeout": "без аргументов завис: убит по таймауту {s} c",
        "check.noargs.crash": "без аргументов упал с traceback",
        "check.noargs.ok": "без аргументов — понятная ошибка (exit {code})",
        "check.noargs.warn_code": "без аргументов exit {code} без пояснения",
        "check.noargs.warn": "без аргументов — молчаливый успех (exit 0)",
        "check.sandbox_isolated.fail": "скрипт писал в оригинальную папку скилла: {files}",
        "check.sandbox_isolated.warn": "часть запусков зависла (подозрение на hang)",
        "check.sandbox_isolated.ok": "все запуски изолированы, в оригинал ничего не записано",
        "check.logging_present.yes": "логирование обнаружено (logging/.log)",
        "check.logging_present.no": "логирование не обнаружено",
        "check.log_rotation.warn": "append-логирование без ротации: {files}",
        "check.log_rotation.ok": "append-логирования без ротации нет",
        "check.error_quality.ok": "ошибки содержат traceback с файл:строкой",
        "check.error_quality.fail": "traceback без файла:строки",
        "check.error_quality.warn": "ошибки без файла:строки",
        "check.error_quality.none": "ошибок в выводе не обнаружено",
        "check.secret_leak.fail": "возможный хардкод-секрет в коде/логах: {items}",
        "check.secret_leak.ok": "хардкод-секретов в коде/логах нет",
        "check.env_secrets.fail": "прод-секреты в .env-файлах: {items}",
        "check.env_secrets.dev": "все значения в .env — dev-заглушки (test/changeme/пример)",
        "check.env_secrets.unknown": "пограничные значения в .env (проверить вручную): {items}",
        "check.env_secrets.ok": ".env-файлов нет или они пустые",
        "check.log_growth.warn": "файловый лог без ротации/лимита размера: {files}",
        "check.log_growth.ok": "неконтролируемого роста логов нет",
        "check.library_reachable.warn": "библиотека скиллов не найдена (~/.openclaw отсутствует)",
        "check.library_reachable.none": "библиотека скиллов отсутствует — дублей нет",
        "check.library_reachable.ok": "библиотека скиллов: {dirs}",
        "check.name_collision.fail": "дублирует существующий скилл: {skills}",
        "check.name_collision.warn": "совпадает имя папки с: {skills}",
        "check.name_collision.ok": "коллизий по имени нет",
        "check.description_overlap.fail": "описание почти совпадает (ratio {ratio}) с {skill}",
        "check.description_overlap.warn": "описание пересекается (ratio {ratio}) с {skill}",
        "check.description_overlap.ok": "пересечений описаний нет",
        "check.description_overlap.nodesc": "описание пустое — пересечение не оценено",
        "check.description_not_empty.fail": "описание пустое/короче 20 симв./шаблон",
        "check.description_not_empty.ok": "описание содержательное ({n} симв.)",
        "check.has_examples.ok": "секция примеров/Usage или пример в коде найден",
        "check.has_examples.warn": "примеров использования не найдено",
        "check.novelty.duplicate": "дублирует существующий скилл",
        "check.novelty.value": "добавляет ценность библиотеке",
        "check.main_script_found.none": "главный скрипт не найден",
        "check.main_script_found.ok": "главный скрипт: {name}",
        "check.runs_completed.fail": "{hangs} из {n} прогонов зависли",
        "check.runs_completed.ok": "все {n} прогонов завершились",
        "check.timing_stats.ok": "min {min}s avg {avg}s max {max}s медиана {median}s",
        "check.no_degradation.fail": "деградация: среднее последних 5 ({last}s) > 1.5× первых 5 ({first}s)",
        "check.no_degradation.warn": "макс. время > 3× медианы (выбросы)",
        "check.no_degradation.ok": "деградации не обнаружено",
        "check.no_memory_leak.unavailable": "метрика RSS недоступна",
        "check.no_memory_leak.fail": "рост RSS: среднее последних 5 ({last} kB) > 120% первых 5 ({first} kB)",
        "check.no_memory_leak.ok": "утечки памяти не обнаружено",
        "check.hang_detected.fail": "{hangs} прогон(ов) убиты по таймауту",
        "check.hang_detected.ok": "зависаний нет",
        "check.all_finished.fail": "не все из {n} процессов завершились (взаимоблокировка/зависание)",
        "check.all_finished.ok": "все {n} процессов завершились",
        "check.exit_codes_ok.ok": "все {n} процессов exit 0",
        "check.exit_codes_ok.warn": "{ok} из {n} процессов exit 0",
        "check.exit_codes_ok.fail": "все {n} процессов завершились с ошибкой",
        "check.unique_tmp_files.ok": "экземпляры создают изолированные temp-файлы/выводы различаются",
        "check.unique_tmp_files.warn": "нет уникальных temp-файлов (возможна общая запись)",
        "check.no_conflicts.fail": "конфликты записи: {items}",
        "check.no_conflicts.ok": "конфликтов записи не обнаружено",
        "check.python_required.ok": "требуется Python >= {v} (фичи: {feats})",
        "check.python_required.base": "версионозависимых фич нет — Python >= 3.8",
        "check.deps_installable.fail": "битый синтаксис зависимостей: {problems}",
        "check.deps_installable.warn": "нерезолвятся импорты: {mods}",
        "check.deps_installable.ok": "зависимости парсятся, сторонних импортов нет",
        "check.runs_on_installed_pythons.none": "интерпретаторы python3.10/3.11/3.12 не найдены",
        "check.runs_on_installed_pythons.nomain": "главный скрипт не найден — прогон на версиях пропущен",
        "check.runs_on_installed_pythons.fail": "крашится на: {versions}",
        "check.runs_on_installed_pythons.warn": "протестировано только на Python {version}",
        "check.runs_on_installed_pythons.unsupported": "не поддерживается на (вне заявленных требований): {versions}",
        "check.runs_on_installed_pythons.ok": "проходит на: {versions}",
        "check.version_features_noted.ok": "версионозависимые фичи: {features}",
        "check.compat.features": "обнаружены фичи: {feats}",
        "cli.license.required": "для --pro нужна валидная лицензия ({status}). Установите: python3 skillqa.py license --install <файл>",
        "cli.license.test_installed": "selftest: установлена локальная тестовая лицензия (machine-id {mid})",
        "cli.report.demo": "отчёт-тизер (demo): {path}",
        "cli.report.md": "сертификат: {path}",
        "cli.report.json": "json: {path}",
        "cli.grade": "Оценка: {grade} ({score}/100) — fail_count={fails}",
        "cli.skipped": "пропущено: {skipped}",
        "cli.budget": "превышен общий бюджет 300 c — модуль {name} помечен fail",
    },
    "en": {
        "module.summary": "Summary: {total} checks, {fail} fails, {warn} warns",
        "check.no_skilmd": "no SKILL.md — check skipped",
        "check.skilmd_exists.missing": "SKILL.md not found",
        "check.skilmd_exists.empty": "SKILL.md empty or too small ({size} bytes, need > 200)",
        "check.skilmd_exists.ok": "SKILL.md found, {size} bytes",
        "check.skilmd_exists.unreadable": "SKILL.md unreadable: {err}",
        "check.frontmatter_valid.missing": "frontmatter block (---) not found",
        "check.frontmatter_valid.fail": "invalid YAML frontmatter: {err}",
        "check.frontmatter_valid.ok": "valid YAML frontmatter",
        "check.frontmatter_fields.fail": "missing required fields: {fields}",
        "check.frontmatter_fields.ok": "required fields (name, description, version, tools) present",
        "check.frontmatter_fields.warn": "no tools/allowed-tools field",
        "check.frontmatter_fields.warn_version": "no version (recommended for marketplaces, not required)",
        "check.frontmatter_fields.nofm": "no frontmatter — fields not checked",
        "check.referenced_paths_exist.fail": "paths referenced in SKILL.md missing: {paths}",
        "check.referenced_paths_exist.internal": "project-file references outside the skill (internal skill)",
        "check.referenced_paths_exist.warn": "mentioned in examples but missing: {paths}",
        "check.referenced_paths_exist.ok": "all referenced paths exist ({n})",
        "check.no_empty_broken_files.fail": "empty/broken files: {files}",
        "check.no_empty_broken_files.warn": "large binaries in root: {files}",
        "check.no_empty_broken_files.ok": "no empty or broken files",
        "check.no_magic_paths.fail": "absolute magic paths in SKILL.md: {paths}",
        "check.no_magic_paths.warn": "SKILL.md contains ~/ paths (not portable)",
        "check.no_magic_paths.ok": "no absolute magic paths",
        "check.reasonable_sizes.warn": "files over 5 MB: {files}",
        "check.reasonable_sizes.ok": "all files within limits",
        "check.version_consistent.notsemver": "version {v} is not semver (X.Y.Z)",
        "check.version_consistent.mentions": "versions in SKILL.md text differ: {mentions}",
        "check.version_consistent.ok": "version {v} is consistent",
        "check.version_consistent.internal": "version history in internal docs",
        "check.version_consistent.noversion": "no version declared",
        "check.scripts_discovered.none": "no executable scripts (*.py/*.sh/*.js) found",
        "check.scripts_discovered.summary": "no executable scripts found",
        "check.run.timeout": "hung: killed by {s}s timeout (SIGTERM/SIGKILL)",
        "check.run.warn": "exit 0 but stderr non-empty, or usage shown",
        "check.run.env": "environment gap (missing dependency/interpreter) — not a skill defect",
        "check.run.ok": "exit 0, empty stderr ({ms} ms)",
        "check.run.fail": "exit {code} or unhandled exception",
        "check.help.timeout": "--help hung: killed by {s}s timeout",
        "check.help.ok": "--help works, exit 0",
        "check.help.warn": "exit {code} but usage/help shown",
        "check.help.crash": "--help crashed with traceback",
        "check.help.fail": "--help failed (exit {code})",
        "check.noargs.timeout": "no-args run hung: killed by {s}s timeout",
        "check.noargs.crash": "no-args run crashed with traceback",
        "check.noargs.ok": "no args: clear error (exit {code})",
        "check.noargs.warn_code": "no args: exit {code} without explanation",
        "check.noargs.warn": "no args: silent success (exit 0)",
        "check.sandbox_isolated.fail": "script wrote into the original skill folder: {files}",
        "check.sandbox_isolated.warn": "some runs timed out (hang suspected)",
        "check.sandbox_isolated.ok": "all runs isolated, nothing written to the original",
        "check.logging_present.yes": "logging detected (logging module / .log files)",
        "check.logging_present.no": "no logging detected",
        "check.log_rotation.warn": "append logging without rotation: {files}",
        "check.log_rotation.ok": "no append-without-rotation logging",
        "check.error_quality.ok": "errors carry file:line tracebacks",
        "check.error_quality.fail": "traceback without file:line",
        "check.error_quality.warn": "errors without file:line",
        "check.error_quality.none": "no errors in output",
        "check.secret_leak.fail": "possible hardcoded secret in code/logs: {items}",
        "check.secret_leak.ok": "no hardcoded secrets in code or logs",
        "check.env_secrets.fail": "production secrets in .env files: {items}",
        "check.env_secrets.dev": "all .env values are dev placeholders (test/changeme/example)",
        "check.env_secrets.unknown": "borderline values in .env (check manually): {items}",
        "check.env_secrets.ok": "no .env files or they are empty",
        "check.log_growth.warn": "file log without rotation/size limit: {files}",
        "check.log_growth.ok": "no unbounded log growth",
        "check.library_reachable.warn": "no skill library found (~/.openclaw missing)",
        "check.library_reachable.none": "no skill library — no duplicates",
        "check.library_reachable.ok": "skill library: {dirs}",
        "check.name_collision.fail": "duplicates existing skill: {skills}",
        "check.name_collision.warn": "folder name matches: {skills}",
        "check.name_collision.ok": "no name collisions",
        "check.description_overlap.fail": "description almost identical (ratio {ratio}) to {skill}",
        "check.description_overlap.warn": "description overlaps (ratio {ratio}) with {skill}",
        "check.description_overlap.ok": "no description overlap",
        "check.description_overlap.nodesc": "empty description — overlap not assessed",
        "check.description_not_empty.fail": "description empty / shorter than 20 chars / template",
        "check.description_not_empty.ok": "description is meaningful ({n} chars)",
        "check.has_examples.ok": "examples section / Usage / code example found",
        "check.has_examples.warn": "no usage examples found",
        "check.novelty.duplicate": "duplicates an existing skill",
        "check.novelty.value": "adds value to the library",
        "check.main_script_found.none": "no main script found",
        "check.main_script_found.ok": "main script: {name}",
        "check.runs_completed.fail": "{hangs} of {n} runs hung",
        "check.runs_completed.ok": "all {n} runs completed",
        "check.timing_stats.ok": "min {min}s avg {avg}s max {max}s median {median}s",
        "check.no_degradation.fail": "degradation: avg(last 5) {last}s > 1.5x avg(first 5) {first}s",
        "check.no_degradation.warn": "max time > 3x median (spikes)",
        "check.no_degradation.ok": "no degradation trend",
        "check.no_memory_leak.unavailable": "RSS metric unavailable",
        "check.no_memory_leak.fail": "RSS growth: avg(last 5) {last} kB > 120% of avg(first 5) {first} kB",
        "check.no_memory_leak.ok": "no memory leak",
        "check.hang_detected.fail": "{hangs} run(s) killed by timeout",
        "check.hang_detected.ok": "no hangs",
        "check.all_finished.fail": "not all of {n} processes finished (deadlock/hang)",
        "check.all_finished.ok": "all {n} processes finished",
        "check.exit_codes_ok.ok": "all {n} processes exited 0",
        "check.exit_codes_ok.warn": "{ok} of {n} processes exited 0",
        "check.exit_codes_ok.fail": "all {n} processes failed",
        "check.unique_tmp_files.ok": "instances create isolated temp files / outputs differ",
        "check.unique_tmp_files.warn": "no unique temp files (possible shared state)",
        "check.no_conflicts.fail": "write conflicts: {items}",
        "check.no_conflicts.ok": "no write conflicts",
        "check.python_required.ok": "requires Python >= {v} (features: {feats})",
        "check.python_required.base": "no version-specific features — Python >= 3.8",
        "check.deps_installable.fail": "broken dependency syntax: {problems}",
        "check.deps_installable.warn": "unresolvable imports: {mods}",
        "check.deps_installable.ok": "dependencies parse cleanly, no third-party imports",
        "check.runs_on_installed_pythons.none": "no python3.10/3.11/3.12 interpreters found",
        "check.runs_on_installed_pythons.nomain": "no main script — version runs skipped",
        "check.runs_on_installed_pythons.fail": "crashes on: {versions}",
        "check.runs_on_installed_pythons.warn": "tested only on Python {version}",
        "check.runs_on_installed_pythons.unsupported": "unsupported (outside declared requirements): {versions}",
        "check.runs_on_installed_pythons.ok": "passes on: {versions}",
        "check.version_features_noted.ok": "version-dependent features: {features}",
        "check.compat.features": "detected features: {feats}",
        "cli.license.required": "--pro requires a valid license ({status}). Install one with: python3 skillqa.py license --install <file>",
        "cli.license.test_installed": "selftest: installed local test license (machine-id {mid})",
        "cli.report.demo": "demo teaser report: {path}",
        "cli.report.md": "certificate: {path}",
        "cli.report.json": "json: {path}",
        "cli.grade": "Grade: {grade} ({score}/100) — fail_count={fails}",
        "cli.skipped": "skipped: {skipped}",
        "cli.budget": "overall 300s budget exceeded — module {name} marked fail",
    },
}


def make_t(lang):
    def t(key, **kw):
        table = I18N.get(lang, I18N["en"])
        tmpl = table.get(key) or I18N["en"].get(key) or key
        try:
            return tmpl.format(**kw)
        except Exception:
            return tmpl
    return t


def make_logger():
    green, yellow, red, reset = "\033[32m", "\033[33m", "\033[31m", "\033[0m"
    icons = {"pass": f"{green}[✓]{reset}", "warn": f"{yellow}[!]{reset}",
             "fail": f"{red}[✗]{reset}", "info": "[·]"}

    def log(msg, level="info"):
        print(f"{icons.get(level, icons['info'])} {msg}")
    return log


# ---------------------------------------------------------------------------
# skill helpers
# ---------------------------------------------------------------------------
SCRIPT_EXTS = (".py", ".sh", ".js")
MAIN_MARKER_RE = re.compile(r"\b(main|run)\b", re.I)


def _parse_frontmatter_simple(text):
    """name/description/version/tools from the frontmatter block (no deps)."""
    data = {}
    if not text.startswith("---"):
        return data
    lines = text.splitlines()
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            break
        line = lines[i]
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, val = line.partition(":")
            data[key.strip()] = val.strip().strip("\"'")
    return data


def derive_skill_name(path):
    md = Path(path) / "SKILL.md"
    if md.exists():
        try:
            fm = _parse_frontmatter_simple(md.read_text(encoding="utf-8",
                                                        errors="replace"))
        except OSError:
            fm = {}
        name = fm.get("name")
        if name:
            s = re.sub(r"[^a-z0-9_-]", "_", str(name).lower())
            s = re.sub(r"_+", "_", s).strip("_")
            if s:
                return s
    return Path(path).name.lower()


def looks_like_script(tok):
    if not tok or len(tok) > 200:
        return False
    if tok.startswith(("/", "~", "$", "-", "(")):
        return False
    if "://" in tok or " " in tok:
        return False
    return Path(tok).suffix.lower() in SCRIPT_EXTS


def find_main_script(skill_dir):
    """Pick the main script: (1) SKILL.md path with main/run marker,
    (2) first *.py in the root, (3) first executable file."""
    skill_dir = Path(skill_dir)
    md = skill_dir / "SKILL.md"
    candidates = []  # (priority, path) — 0 = marker line, 1 = other
    if md.exists():
        try:
            lines = md.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            lines = []
        for i, line in enumerate(lines):
            marked = bool(MAIN_MARKER_RE.search(line))
            tokens = []
            for m in re.finditer(r"`([^`]+)`", line):
                tokens.extend(m.group(1).split())
            if not tokens and line.strip().startswith("```"):
                # code fence opener: collect content until the closing fence
                for j in range(i + 1, min(i + 6, len(lines))):
                    if lines[j].strip().startswith("```"):
                        break
                    tokens.extend(lines[j].split())
            for tok in tokens:
                if looks_like_script(tok):
                    cand = skill_dir / tok
                    if cand.exists() and cand.is_file():
                        candidates.append((0 if marked else 1, cand))
        if candidates:
            candidates.sort(key=lambda x: x[0])
            return candidates[0][1]
    for p in sorted(skill_dir.glob("*.py")):
        if p.is_file():
            return p
    for p in sorted(skill_dir.iterdir()):
        if (p.is_file() and os.access(p, os.X_OK)
                and Path(p).suffix.lower() in ("", ".sh", ".py")):
            return p
    return None


def compute_grade(results):
    """Grade from module results. pass=2, warn=1, fail=0."""
    CRITICAL_CHECKS = {"secret_leak", "no_magic_paths",
                       "skilmd_exists", "frontmatter_valid", "sandbox_isolated",
                       "run_", "help_", "noargs_"}
    if not results:
        return "D", 0.0, 0
    total = sum(2 if r["status"] == "pass"
                else 1 if r["status"] == "warn" else 0 for r in results)
    score = total / (2.0 * len(results))
    fails = sum(1 for r in results if r["status"] == "fail")
    if fails == 0 and score >= 0.85:
        grade = "A"
    elif fails <= 1 and score >= 0.65:
        grade = "B"
    elif score >= 0.45:
        grade = "C"
    else:
        grade = "D"
    # crashes / secret leaks cap the grade at B
    if grade == "A" and any(r["module"] in ("sandbox", "log")
                            and r["status"] == "fail" for r in results):
        grade = "B"
    # trust threshold: with no critical defects and a decent score,
    # stylistic findings alone must never sink the grade below B
    critical = any(
        r["status"] == "fail" and (
            r["module"] in ("sandbox", "log")
            or any(c["status"] == "fail" and c["name"] in CRITICAL_CHECKS
                   for c in r["checks"]))
        for r in results)
    # (fix 26.08: only lift C/D to B — must not override an earned A)
    if grade in ("C", "D") and not critical and score >= 0.5:
        grade = "B"
    return grade, round(score, 4), fails


# ---------------------------------------------------------------------------
# reports
# ---------------------------------------------------------------------------
def _check_icons(checks):
    n_pass = sum(1 for c in checks if c["status"] == "pass")
    n_warn = sum(1 for c in checks if c["status"] == "warn")
    n_fail = sum(1 for c in checks if c["status"] == "fail")
    return n_pass, n_warn, n_fail


def _skill_sha256(skill_path):
    """Stable sha256 of the skill content (relative paths + file bytes).
    Binds the certificate to the exact tested version of the skill."""
    import hashlib
    h = hashlib.sha256()
    root = Path(skill_path)
    for p in sorted(root.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            rel = str(p.relative_to(root))
            h.update(rel.encode("utf-8", "surrogatepass"))
            try:
                data = p.read_bytes()
            except OSError:
                data = b""
            h.update(data)
    return h.hexdigest()


def _recommendations(results):
    """Concrete, actionable steps to reach the next grade."""
    recs = []
    for r in results:
        mod = r["module"]
        for c in r["checks"]:
            if c["status"] == "fail":
                if mod == "log" and c["name"] in ("env_secrets", "secret_leak"):
                    recs.append(f"- **{mod}/{c['name']}** — fix FAIL: secrets detected "
                                f"(values masked — see the local full report)")
                    continue
                recs.append(f"- **{mod}/{c['name']}** — fix FAIL: {c['detail'][:140]}")
            elif c["status"] == "warn":
                recs.append(f"- {mod}/{c['name']} — reduce warning: {c['detail'][:120]}")
    return recs[:14]


def _verdict_summary(report):
    """'critical defects vs stylistic notes' one-liner for the report."""
    crit = 0
    styl = 0
    for m in report["modules"]:
        for c in m["checks"]:
            if c["status"] == "fail":
                if (m["module"] in ("sandbox", "log")
                        or c["name"] in ("secret_leak", "no_magic_paths",
                                         "skilmd_exists", "frontmatter_valid")):
                    crit += 1
                else:
                    styl += 1
            elif c["status"] == "warn":
                styl += 1
    return (f"critical defects: {crit} · stylistic notes: {styl}"
            + (" — clean, sellable skill" if crit == 0 else " — fix criticals first"))


def _check_type(module, check):
    """🔴 critical / 🟡 stylistic / ⚪ info — trust typology for findings."""
    if check["status"] == "pass":
        return "⚪"
    if (module in ("sandbox", "log")
            or check["name"] in ("secret_leak", "no_magic_paths",
                                 "skilmd_exists", "frontmatter_valid",
                                 "sandbox_isolated")
            or check["name"].startswith(("run_", "help_", "noargs_"))):
        return "🔴"
    return "🟡"


def render_certificate(report):
    grade = report["grade"]
    score = int(round(report["score_pct"] * 100))
    lic = report.get("license") or {}
    certified = grade in ("A", "B")
    lines = [
        BANNER,
        "",
        "**QA REPORT / ОТЧЁТ QA**" if not certified else
        "**СЕРТИФИЦИРОВАНО SKILLQA PRO**  ·  **CERTIFIED BY SKILLQA PRO**",
        "",
        f"- **Skill:** {report['skill_name']}",
        f"- **Date:** {report['date']}",
        f"- **Tool:** ViBo SkillQA v{report['version']} ({report['edition']} edition)",
        f"- **Language:** {report['lang']}",
        f"- **Skill SHA-256:** `{report.get('skill_sha256', '-')[:24]}…` "
        f"(bound to this exact skill content)",
        "",
        f"## Вердикт / Verdict: **Оценка / Grade: {grade} ({score}/100)**",
        "",
        "| Module | Status | Time | Checks |",
        "|---|---|---|---|",
    ]
    for m in report["modules"]:
        np_, nw, nf = _check_icons(m["checks"])
        icon = {"pass": "✓", "warn": "!", "fail": "✗"}[m["status"]]
        lines.append(
            f"| {m['module']} | {icon} {m['status']} | {m['duration_ms']} ms "
            f"| {len(m['checks'])} (✓{np_} !{nw} ✗{nf}) |")
    lines += ["", "## Детали / Details", ""]
    for i, m in enumerate(report["modules"], 1):
        icon = {"pass": "✓", "warn": "!", "fail": "✗"}[m["status"]]
        lines.append(f"### {i}. {m['module']} — {m.get('title', m['module'])} "
                     f"({icon} {m['status']}, {m['duration_ms']} ms)")
        for c in m["checks"]:
            cicon = {"pass": "✓", "warn": "!", "fail": "✗"}[c["status"]]
            detail = c["detail"]
            if m["module"] == "log" and c["name"] in ("env_secrets", "secret_leak"):
                detail = ("secrets detected — values masked, details only in the "
                          "local full report")
            lines.append(f"- [{cicon}] {_check_type(m['module'], c)} "
                         f"**{c['name']}** — {detail}")
        if m.get("details"):
            lines += ["", f"> {m['details']}"]
        lines.append("")
    lines += [
        "## Сводка / Summary",
        "",
        f"- **Skipped modules:** {', '.join(report['skipped']) if report['skipped'] else 'none'}",
        f"- **Fail count:** {report['fail_count']}",
        f"- **Summary:** {_verdict_summary(report)}",
        f"- **Total time:** {report['duration_ms']} ms",
        "",
    ]
    recs = report.get("recommendations") or []
    if recs:
        lines += [
            "## Следующий уровень / Next grade roadmap",
            "",
            "Проверки, которые удерживают оценку, и что исправить, чтобы подняться "
            "на следующий уровень (A > B > C > D). После исправлений перезапустите "
            "тест — сертификат привязан к новой версии скилла:",
            "",
        ]
        lines += recs
        lines += ["", "Рекомендации генерируются автоматически из результатов "
                      "каждой проверки.", ""]
    lines += [
        "---",
        "",
        f"**{'Сертифицировано / Certified' if certified else 'Отчёт QA / QA report'} "
        f"ViBo SkillQA v{report['version']}**  ·  "
        f"license: {lic.get('status', '-')} (expires {lic.get('expires', '-')})",
        "",
    ]
    if certified:
        lines += [
            "*This certificate is generated by ViBo SkillQA and can be shown to "
            "buyers of the skill.*",
            "",
        ]
    else:
        lines += [
            "*This is a QA report, not a certificate — the skill did not pass "
            "certification (grade below B).*",
            "",
        ]
    return "\n".join(lines)


def render_demo_report(report):
    lines = [
        BANNER,
        "",
        "**SkillQA Pro — DEMO EDITION**",
        "",
        f"- **Skill:** {report['skill_name']}",
        f"- **Path:** `{report['skill_path']}`",
        f"- **Date:** {report['date']}",
        f"- **Tool:** SkillQA Pro v{report['version']}",
        "",
        "## Static scan (demo)",
        "",
        "| Check | Status | Detail |",
        "|---|---|---|",
    ]
    for m in report["modules"]:
        if m["module"] != "static":
            continue
        for c in m["checks"]:
            icon = {"pass": "✓", "warn": "!", "fail": "✗"}[c["status"]]
            lines.append(f"| {c['name']} | {icon} {c['status']} | {c['detail']} |")
        if m.get("details"):
            lines += ["", f"> {m['details']}"]
    lines += [
        "",
        "## What SkillQA Pro gives you (Pro edition)",
        "",
        "1. **Static scan** — structure, frontmatter, magic paths, version consistency",
        "2. **Sandbox run** — every script executed safely with fake tokens and a hard timeout-kill",
        "3. **Log audit** — logging quality, rotation, **secret-leak detection**",
        "4. **Novelty** — overlap with the local skill library",
        "5. **Load test** — N runs, min/avg/max/median, degradation and memory-leak detection",
        "6. **Parallel test** — races, deadlocks, write conflicts",
        "7. **Compat check** — required Python version, deps, runs on 3.10/3.11/3.12",
        "",
        "Pro also adds: the **quality certificate (grade A/B/C/D)** and "
        "**JSON reports for CI**.",
        "",
        "## Licensing",
        "",
        f"- Demo: static scan + this teaser (free)",
        f"- Pro: full certification, license key bound to your machine-id",
        f"- Pricing: see https://wwwvibo.com",
        "",
        "Get a license: `python3 skillqa.py license --status` · "
        "`python3 skillqa.py license --machine-id`",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# test command
# ---------------------------------------------------------------------------
def parse_skip(value):
    return {m.strip() for m in value.split(",") if m.strip()}


def read_qaignore(path):
    """Returns (skip_set, notes). Broken lines end up in notes as warnings."""
    skip, notes = set(), []
    p = Path(path) / ".qaignore"
    if not p.exists():
        return skip, notes
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if re.match(r"^[a-z_]+$", line):
            skip.add(line)
        else:
            notes.append(line)
    return skip, notes


def cmd_test(args, parser):
    path = Path(args.path).expanduser().resolve()
    if not path.is_dir():
        parser.error(f"path is not a directory: {path}")

    if args.config:
        print("Pricing: see https://wwwvibo.com")
        return 0

    # edition resolution
    status, edition, expires, _ = license_status()
    if args.pro:
        if status != "valid":
            print(f"[license] ERROR: " +
                  I18N[args.lang]["cli.license.required"].format(status=status),
                  file=sys.stderr)
            return 3
        edition = "pro"
    elif args.demo:
        edition = "demo"
    else:
        edition = "pro" if status == "valid" else "demo"

    t = make_t(args.lang)
    log = make_logger()
    lang = args.lang

    from modules import MODULES
    from modules.sandbox import Sandbox

    sandbox = Sandbox(lang=lang, timeout=args.timeout)
    overall_start = time.monotonic()
    try:
        sandbox.copy_skill(path)
        skill_name = derive_skill_name(path)
        skip = parse_skip(args.skip)
        qaignore_notes = []
        qa_skip, qa_notes = read_qaignore(path)
        skip |= qa_skip
        qaignore_notes = qa_notes
        # internal skills: load/parallel tests are meaningless (scripts need
        # the project environment) — auto-skip them
        try:
            _md_head = (Path(path) / "SKILL.md").read_text(encoding="utf-8", errors="replace").split("---", 2)
            if len(_md_head) >= 2 and re.search(r"(?m)^internal:\s*true", _md_head[1]):
                skip |= {"load", "parallel"}
        except Exception:
            pass

        run_outputs = []
        ctx = {
            "skill_path": path,
            "skill_name": skill_name,
            "lang": lang,
            "timeout": args.timeout,
            "load_n": args.load,
            "skip": skip,
            "parallel": args.parallel is not None,
            "parallel_n": max(5, min(10, args.parallel or 5)),
            "edition": edition,
            "sandbox": sandbox,
            "tmp_root": sandbox.tmp_root,
            "run_outputs": run_outputs,
            "log": log,
            "t": t,
        }
        # modules use attribute access for convenience
        ctx = _Ctx(**ctx)
        ctx.main_script = find_main_script(sandbox.skill_dir)

        results = []
        skipped_run = []
        for name, cls in MODULES.items():
            if name in ctx.skip:
                skipped_run.append(name)
                continue
            if name == "parallel" and not ctx.parallel:
                skipped_run.append(name)
                continue
            if edition == "demo" and name != "static":
                skipped_run.append(name)
                continue
            if time.monotonic() - overall_start > 300:
                results.append({
                    "module": name, "status": "fail",
                    "checks": [{"name": "budget_exceeded", "status": "fail",
                                "detail": "overall 300s budget exceeded"}],
                    "details": "overall time budget exceeded",
                })
                continue
            module = cls()
            start = time.monotonic()
            try:
                res = module.run(ctx)
                if not isinstance(res, dict):
                    raise TypeError(
                        f"module {name} returned {type(res).__name__}, expected dict")
                res = dict(res)
            except Exception as e:
                res = {"module": name, "status": "fail",
                       "checks": [{"name": "module_crash", "status": "fail",
                                   "detail": f"{type(e).__name__}: {e}"}],
                       "details": f"{type(e).__name__}: {e}"}
            res["duration_ms"] = int((time.monotonic() - start) * 1000)
            res["title"] = module.title.get(lang, module.title["en"])
            results.append(res)
            log(f"{module.title.get(lang, module.title['en'])} — "
                f"{res['status']} ({res['duration_ms']} ms)", level=res["status"])

        grade, score_pct, fail_count = compute_grade(results)

        ts = datetime.now().strftime("%Y-%m-%d_%H%M%S%f")
        iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        report_dir = Path("qa_reports") / skill_name
        report_dir.mkdir(parents=True, exist_ok=True)
        report = {
            "tool": TOOL, "version": VERSION, "edition": edition,
            "skill_name": skill_name, "skill_path": str(path),
            "grade": grade, "score_pct": score_pct, "fail_count": fail_count,
            "date": iso, "lang": lang, "skipped": sorted(skipped_run),
            "duration_ms": int((time.monotonic() - overall_start) * 1000),
            "skill_sha256": _skill_sha256(path),
            "recommendations": _recommendations(results),
            "modules": results,
            "qaignore_notes": qaignore_notes,
            "license": {"status": status, "expires": expires},
        }

        if edition == "demo":
            md_path = report_dir / f"{ts}_demo.md"
            md_path.write_text(render_demo_report(report), encoding="utf-8")
            log(t("cli.report.demo", path=md_path))
        else:
            md_path = report_dir / f"{ts}.md"
            json_path = report_dir / f"{ts}.json"
            md_path.write_text(render_certificate(report), encoding="utf-8")
            json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False),
                                 encoding="utf-8")
            log(t("cli.report.md", path=md_path))
            log(t("cli.report.json", path=json_path))
            print(f"⚠️ Report saved to {md_path} — contains local paths; "
                  f"review before sharing.")

        log(t("cli.grade", grade=grade, score=int(round(score_pct * 100)),
              fails=fail_count), level="pass" if fail_count == 0 else "fail")
        if skipped_run:
            log(t("cli.skipped", skipped=", ".join(skipped_run)), level="info")
        if qaignore_notes:
            log(f"qaignore: invalid lines ignored: {', '.join(qaignore_notes)}",
                level="warn")
        return 0 if fail_count == 0 else 1
    finally:
        sandbox.cleanup()


class _Ctx:
    """Lightweight attribute-access context object."""

    def __init__(self, **kw):
        self.__dict__.update(kw)


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------
BUG_CHECK_MAP = {
    "crash": [("sandbox", "run_run.py")],
    "hang": [("sandbox", "run_hang.py")],
    "missing-file": [("static", "referenced_paths_exist")],
    "secret-leak": [("log", "secret_leak")],
    "env-secret": [("log", "env_secrets")],
    "magic-path": [("static", "no_magic_paths")],
}


def _bug_found(report, bug):
    """True if the report contains a fail for the expected bug."""
    for mod, check in BUG_CHECK_MAP.get(bug["id"], []):
        for m in report["modules"]:
            if m["module"] != mod:
                continue
            for c in m["checks"]:
                if c["name"] == check and c["status"] == "fail":
                    return True
                # missing-file may surface as warn (backtick/doc example path)
                if (bug["id"] == "missing-file"
                        and c["name"] == check and c["status"] == "warn"):
                    return True
    # bug-specific fallbacks (fixture names may drift)
    if bug["id"] == "hang":
        if any(m["module"] == "sandbox"
               and c["status"] == "fail"
               and ("timed out" in c["detail"].lower()
                    or "hung" in c["detail"].lower())
               for m in report["modules"] for c in m["checks"]):
            return True
    # generic fallback: any fail check whose name/detail matches a hint part
    hint = bug.get("hint", "")
    for part in [p.strip().lower() for p in hint.split("|") if p.strip()]:
        for m in report["modules"]:
            for c in m["checks"]:
                if (c["status"] == "fail"
                        and part in (c["name"] + " " + c["detail"]).lower()):
                    return True
    return False


_NORM_TIMING_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:ms|мс|s|сек|kB|KB|MB|bytes|КБ|МБ|байт)\b|rss=\d+\b")


def _normalize_report(obj):
    """Strip run-specific values so reports can be compared across runs.

    Removes duration_ms/date keys and scrubs timing + RSS figures that
    legitimately vary between runs (e.g. '51 ms', '0.052s', 'rss=26432 kB')
    out of every string, including check details and module details.
    """
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in ("duration_ms", "date"):
                continue
            out[k] = _normalize_report(v)
        return out
    if isinstance(obj, list):
        return [_normalize_report(x) for x in obj]
    if isinstance(obj, str):
        return _NORM_TIMING_RE.sub("N", obj)
    return obj


def cmd_selftest(args):
    base = Path(__file__).resolve().parent
    bad = base / "fixtures" / "bad_skill"
    good = base / "fixtures" / "good_skill"
    expected_file = bad / "EXPECTED_BUGS.json"
    ok = True

    print(f"SkillQA Pro selftest (v{VERSION}) — python {platform.python_version()}")

    # pro mode needed for JSON reports -> ensure a local license
    status, _, _, _ = license_status()
    if status != "valid":
        install_test_license()
        print(f"⚠️ selftest wrote a local TEST pro license to "
              f"{LICENSE_FILE} (machine-bound: hashed /etc/machine-id). "
              f"This is a selftest artifact; remove it with "
              f"'rm {LICENSE_FILE}' if you do not want it.")
        print(I18N[args.lang]["cli.license.test_installed"].format(mid=machine_id()))

    def run_test(*extra):
        cmd = [sys.executable, str(base / "skillqa.py"), "test"]
        cmd += [str(x) for x in extra]
        try:
            return subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=180 + args.timeout * 6, cwd=str(base))
        except subprocess.TimeoutExpired:
            return None

    def newest_json(skill_name, before=None):
        d = base / "qa_reports" / skill_name
        if not d.exists():
            return None
        jsons = sorted(d.glob("*.json"), key=lambda p: p.stat().st_mtime)
        if before is not None:
            # only reports created after the snapshot — mtime ties between
            # runs (same second) could otherwise return a stale file
            jsons = [p for p in jsons if p not in before]
        return jsons[-1] if jsons else None

    # ---- phase 1: integrity (own static + sandbox, must not crash) ----
    print("[selftest] phase 1: integrity (own code through static + sandbox)")
    r = run_test(".", "--lang", args.lang, "--skip", "parallel,novelty,load",
                 "--timeout", str(args.timeout))
    if r is None:
        print("[FAIL] phase 1: self-test timed out")
        ok = False
    elif r.returncode not in (0, 1):
        print(f"[FAIL] phase 1: self-test crashed (exit {r.returncode})")
        ok = False
    elif "Traceback" in (r.stdout + r.stderr):
        print("[FAIL] phase 1: traceback in self-test output")
        ok = False
    else:
        print(f"[ OK ] phase 1: integrity (exit {r.returncode})")

    # ---- phase 2: bad_skill must expose all expected bugs ----
    print("[selftest] phase 2: bad_skill — all expected bugs must be found")
    missing = []
    if not bad.is_dir() or not expected_file.exists():
        missing.append("(fixtures/bad_skill missing)")
    else:
        before = set((base / "qa_reports" / "bad-skill").glob("*.json"))
        r = run_test(str(bad), "--lang", args.lang, "--timeout", str(args.timeout),
                     "--load", str(args.load), "--parallel", "5")
        if r is None:
            missing.append("(bad_skill run timed out)")
        else:
            jp = newest_json("bad-skill", before)
            if jp is None:
                missing.append("(no JSON report — pro license not active)")
            else:
                report = json.loads(jp.read_text(encoding="utf-8"))
                expected = json.loads(expected_file.read_text(encoding="utf-8"))
                for bug in expected.get("bugs", []):
                    if not _bug_found(report, bug):
                        missing.append(bug["id"])
    if missing:
        print(f"[FAIL] phase 2: bugs not detected: {', '.join(missing)}")
        ok = False
    else:
        print("[ OK ] phase 2: all 5 expected bugs found")

    # ---- phase 3: good_skill must have no fails ----
    print("[selftest] phase 3: good_skill — no failures allowed")
    fails = []
    if not good.is_dir():
        fails.append("(fixtures/good_skill missing)")
    else:
        before = set((base / "qa_reports" / "good-skill").glob("*.json"))
        r = run_test(str(good), "--lang", args.lang, "--timeout", str(args.timeout),
                     "--load", str(args.load))
        if r is None:
            fails.append("(good_skill run timed out)")
        else:
            jp = newest_json("good-skill", before)
            if jp is None:
                fails.append("(no JSON report)")
            else:
                report = json.loads(jp.read_text(encoding="utf-8"))
                for m in report["modules"]:
                    for c in m["checks"]:
                        if c["status"] == "fail":
                            fails.append(f"{m['module']}/{c['name']}")
    if fails:
        print(f"[FAIL] phase 3: good_skill failures: {', '.join(fails[:10])}")
        ok = False
    else:
        print("[ OK ] phase 3: good_skill clean")

    # ---- phase 4: stability — 3 consecutive runs identical ----
    print("[selftest] phase 4: stability — 3 consecutive runs identical")
    normed = []
    for i in range(3):
        before = set((base / "qa_reports" / "good-skill").glob("*.json"))
        run_test(str(good), "--lang", args.lang, "--timeout", str(args.timeout),
                 "--load", str(args.load))
        jp = newest_json("good-skill", before)
        if jp is None:
            normed.append(None)
        else:
            report = json.loads(jp.read_text(encoding="utf-8"))
            normed.append(_normalize_report(report))
    if any(n is None for n in normed):
        print("[FAIL] phase 4: report missing in one of the runs")
        ok = False
    elif normed[0] == normed[1] == normed[2]:
        print("[ OK ] phase 4: stable across 3 runs")
    else:
        print("[FAIL] phase 4: normalized reports differ between runs")
        ok = False

    # ---- phase 5: a skill installed INSIDE the library must not collide
    #      with itself (regression: self in library -> name_collision fail) ----
    print("[selftest] phase 5: skill inside library — no self-collision")
    import shutil as _sh
    import tempfile as _tf
    _lib = Path(_tf.mkdtemp(prefix="skillqa_selflib_"))
    _inst = _lib / "good_skill_installed"
    _sh.copytree(good, _inst, ignore=_sh.ignore_patterns("__pycache__", "*.pyc"))
    try:
        _env = dict(os.environ, OPENCLAW_SKILLS_DIR=str(_lib))
        _before = set((base / "qa_reports" / "good-skill").glob("*.json"))
        r = subprocess.run(
            [sys.executable, str(base / "skillqa.py"), "test", str(_inst),
             "--lang", args.lang, "--timeout", str(args.timeout),
             "--skip", "load,parallel"],
            capture_output=True, text=True, timeout=150, env=_env)
        jp = newest_json("good-skill", _before)
        self_fail = False
        if r.returncode == 0 and jp is not None:
            report = json.loads(jp.read_text(encoding="utf-8"))
            for m in report["modules"]:
                if m["module"] == "novelty":
                    for c in m["checks"]:
                        if c["name"] == "name_collision" and c["status"] == "fail":
                            self_fail = True
        if not (r.returncode == 0 and jp is not None) or self_fail:
            print("[FAIL] phase 5: installed skill collides with itself")
            ok = False
        else:
            print("[ OK ] phase 5: no self-collision")
    finally:
        _sh.rmtree(_lib, ignore_errors=True)

    print()
    print(f"selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser():
    parser = argparse.ArgumentParser(
        prog="skillqa",
        description="SkillQA Pro — autonomous QA and certification for agent skills")
    parser.add_argument("--version", action="store_true",
                        help="show version and exit")
    sub = parser.add_subparsers(dest="command")

    p_test = sub.add_parser("test", help="run quality checks on a skill")
    p_test.add_argument("path", help="path to the skill directory")
    p_test.add_argument("--lang", choices=["ru", "en"], default="ru",
                        help="report language (default: ru)")
    p_test.add_argument("--skip", default="",
                        help="comma-separated modules to skip")
    p_test.add_argument("--load", type=int, default=20,
                        help="number of load-test runs (default: 20)")
    p_test.add_argument("--parallel", nargs="?", const=5, type=int, default=None,
                        help="enable parallel test with N instances (5-10)")
    p_test.add_argument("--timeout", type=int, default=15,
                        help="per-run timeout in seconds (default: 15)")
    grp = p_test.add_mutually_exclusive_group()
    grp.add_argument("--demo", action="store_true",
                     help="force demo edition (static scan + teaser only)")
    grp.add_argument("--pro", action="store_true",
                     help="force pro edition (requires a valid license)")
    p_test.add_argument("--config", action="store_true",
                        help="print payment/config placeholders and exit")

    p_self = sub.add_parser("selftest", help="test SkillQA Pro on itself and fixtures")
    p_self.add_argument("--lang", choices=["ru", "en"], default="ru")
    p_self.add_argument("--timeout", type=int, default=15)
    p_self.add_argument("--load", type=int, default=20)

    p_lic = sub.add_parser("license", help="license management")
    p_lic.add_argument("--install", metavar="FILE",
                       help="install a license file (bound to this machine)")
    p_lic.add_argument("--status", action="store_true", help="show license status")
    p_lic.add_argument("--machine-id", action="store_true",
                       help="print this machine's ID")

    p_cfg = sub.add_parser("config", help="show payment/config placeholders")
    sub.add_parser("version", help="show version")

    return parser


def cmd_license(args, parser):
    if args.install:
        return install_license_file(args.install, parser)
    if args.status:
        status, edition, expires, path = license_status()
        print(f"status: {status}")
        print(f"edition: {edition or 'demo'}")
        print(f"expires: {expires or '-'}")
        print(f"machine-id: {machine_id()}")
        if path:
            print(f"file: {path}")
        return 0 if status == "valid" else 3
    if args.machine_id:
        print(machine_id())
        return 0
    parser.error("license: use --install FILE, --status or --machine-id")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version or args.command == "version":
        print(f"skillqa {VERSION}")
        return 0
    if args.command == "test":
        return cmd_test(args, parser)
    if args.command == "selftest":
        return cmd_selftest(args)
    if args.command == "license":
        return cmd_license(args, parser)
    if args.command == "config":
        print("Pricing: see https://wwwvibo.com")
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
