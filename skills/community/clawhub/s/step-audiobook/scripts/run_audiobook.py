#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from common import (
    DEFAULT_LIBRARY_PATH,
    get_story_base_name,
    load_yaml,
    load_yaml_if_exists,
    resolve_path,
    resolve_story_workspace_dir,
    trim_string,
)
from story_artifacts import (
    build_story_artifact_manifest,
    format_manifest_pretty,
    save_story_artifact_manifest,
    select_manifest_items,
)


SCRIPT_DIR = Path(__file__).resolve().parent
SYNC_SCRIPT = SCRIPT_DIR / 'sync_voice_library.py'
RECOMMEND_SCRIPT = SCRIPT_DIR / 'recommend_casting.py'
CLONE_SCRIPT = SCRIPT_DIR / 'clone_selected_voices.py'
GENERATE_STRUCTURED_SCRIPT = SCRIPT_DIR / 'generate_structured_script.py'
BUILD_TTS_REQUESTS_SCRIPT = SCRIPT_DIR / 'build_tts_requests.py'
SYNTHESIZE_TTS_REQUESTS_SCRIPT = SCRIPT_DIR / 'synthesize_tts_requests.py'
FINALIZE_AUDIOBOOK_SCRIPT = SCRIPT_DIR / 'finalize_audiobook.py'
STRUCTURED_STORY_EXTENSIONS = {'.yaml', '.yml', '.json'}


def resolve_default_casting_plan_path(input_path: Path) -> Path:
    return resolve_story_workspace_dir(input_path) / f"{get_story_base_name(input_path)}.casting-plan.yaml"


def get_casting_base_name(output_path: Path) -> str:
    base = output_path.stem
    return base[: -len('.casting-plan')] if base.endswith('.casting-plan') else base


def get_casting_review_path(output_path: Path) -> Path:
    return output_path.parent / f"{get_casting_base_name(output_path)}.casting-review.yaml"


def get_clone_review_path(output_path: Path) -> Path:
    return output_path.parent / f"{get_casting_base_name(output_path)}.clone-review.yaml"


def parse_json_output(stdout: str, command: list[str]) -> dict[str, Any]:
    payload = stdout.strip()
    if not payload:
        raise RuntimeError(f"命令没有输出 JSON: {' '.join(command)}")
    try:
        return json.loads(payload)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"命令输出不是合法 JSON: {' '.join(command)}\n{payload[:500]}") from error


def run_json_command(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or f'命令失败: {result.returncode}'
        raise RuntimeError(f"{' '.join(command)}\n{message}")
    return parse_json_output(result.stdout, command)


def run_json_command_safe(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        try:
            return {
                'ok': True,
                'command': command,
                'result': parse_json_output(result.stdout, command),
            }
        except Exception as error:
            return {
                'ok': False,
                'command': command,
                'error': str(error),
                'stdout': result.stdout.strip(),
                'stderr': result.stderr.strip(),
            }
    return {
        'ok': False,
        'command': command,
        'error': result.stderr.strip() or result.stdout.strip() or f'命令失败: {result.returncode}',
        'stdout': result.stdout.strip(),
        'stderr': result.stderr.strip(),
    }


def dedupe_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    ordered: list[Path] = []
    for path in paths:
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        ordered.append(path.resolve())
    return ordered


def collect_requested_voice_inputs(
    args: argparse.Namespace,
    library: dict[str, Any],
    library_dir: Path,
) -> list[Path]:
    requested: list[Path] = []

    for raw_path in args.voice_input or []:
        candidate = Path(raw_path).resolve()
        if not candidate.exists() or not candidate.is_file():
            raise RuntimeError(f"待分析音频不存在: {candidate}")
        requested.append(candidate)

    if args.process_inbox:
        inbox_dir = resolve_path(
            library_dir,
            (library.get('paths') or {}).get('inbox_dir', 'voices/inbox'),
        )
        if inbox_dir.exists():
            requested.extend(sorted(item.resolve() for item in inbox_dir.iterdir() if item.is_file()))

    return dedupe_paths(requested)


def collect_pending_voice_reviews(library: dict[str, Any], library_dir: Path) -> dict[str, Any]:
    paths = library.get('paths') or {}
    review_path = resolve_path(library_dir, paths.get('review_file', 'voice-reviews.yaml'))
    effective_library_path = resolve_path(
        library_dir,
        paths.get('effective_library_file', '.audiobook/effective-voice-library.yaml'),
    )

    review_store = load_yaml_if_exists(review_path, {'clones': {}}) or {'clones': {}}
    effective_library = load_yaml_if_exists(effective_library_path, {'clones': {}}) or {'clones': {}}

    asset_ids = sorted(
        {
            *list((library.get('clones') or {}).keys()),
            *list((review_store.get('clones') or {}).keys()),
            *list((effective_library.get('clones') or {}).keys()),
        }
    )

    items: list[dict[str, Any]] = []
    for asset_id in asset_ids:
        meta = ((library.get('clones') or {}).get(asset_id)) or {}
        review_entry = ((review_store.get('clones') or {}).get(asset_id)) or {}
        effective_entry = ((effective_library.get('clones') or {}).get(asset_id)) or {}
        review_status = (
            ((review_entry.get('review') or {}).get('status'))
            or ((meta.get('review_ref') or {}).get('last_status'))
            or 'pending_manual_confirmation'
        )
        if review_status == 'manual_override_present':
            continue
        items.append(
            {
                'asset_id': asset_id,
                'display_name': review_entry.get('display_name')
                or meta.get('display_name')
                or effective_entry.get('display_name')
                or asset_id,
                'review_status': review_status,
            }
        )

    return {
        'review_path': str(review_path),
        'effective_library_path': str(effective_library_path),
        'pending_count': len(items),
        'items': items,
    }


def collect_selected_clone_assets(library: dict[str, Any]) -> dict[str, Any]:
    items = []
    for asset_id, clone_meta in sorted((library.get('clones') or {}).items()):
        if not isinstance(clone_meta, dict):
            continue
        if clone_meta.get('enabled') is False:
            continue
        if clone_meta.get('selected_for_clone') is True:
            items.append(
                {
                    'asset_id': asset_id,
                    'display_name': clone_meta.get('display_name') or asset_id,
                    'status': clone_meta.get('status') or 'unknown',
                }
            )
    return {'selected_count': len(items), 'items': items}


def collect_casting_status(output_path: Path) -> dict[str, Any]:
    casting_review_path = get_casting_review_path(output_path)
    clone_review_path = get_clone_review_path(output_path)
    casting_plan = load_yaml_if_exists(output_path, {}) or {}
    casting_review = load_yaml_if_exists(casting_review_path, {'roles': {}}) or {'roles': {}}
    clone_review = load_yaml_if_exists(clone_review_path, {'items': {}}) or {'items': {}}

    role_items = casting_review.get('roles') or {}
    pending_manual_roles: list[dict[str, Any]] = []
    manual_override_roles: list[dict[str, Any]] = []
    for role_id, entry in role_items.items():
        review_status = ((entry.get('review') or {}).get('status')) or 'pending_manual_review'
        item = {'role_id': role_id, 'role_name': entry.get('role_name') or role_id, 'review_status': review_status}
        if review_status == 'manual_override_present':
            manual_override_roles.append(item)
        else:
            pending_manual_roles.append(item)

    clone_items = clone_review.get('items') or {}
    pending_clone_items: list[dict[str, Any]] = []
    confirm_clone_items: list[dict[str, Any]] = []
    skipped_clone_items: list[dict[str, Any]] = []
    for asset_id, entry in clone_items.items():
        review_status = ((entry.get('review') or {}).get('status')) or 'pending_clone_confirmation'
        item = {
            'asset_id': asset_id,
            'display_name': entry.get('display_name') or asset_id,
            'review_status': review_status,
        }
        if review_status == 'confirm_clone_requested':
            confirm_clone_items.append(item)
        elif review_status == 'skipped_by_user':
            skipped_clone_items.append(item)
        else:
            pending_clone_items.append(item)

    return {
        'casting_plan_path': str(output_path),
        'casting_review_path': str(casting_review_path),
        'clone_review_path': str(clone_review_path),
        'role_count': len(casting_plan.get('roles') or []),
        'pending_manual_role_count': len(pending_manual_roles),
        'manual_override_role_count': len(manual_override_roles),
        'pending_manual_roles': pending_manual_roles,
        'pending_clone_confirmation_count': len(pending_clone_items),
        'confirm_clone_requested_count': len(confirm_clone_items),
        'skipped_clone_count': len(skipped_clone_items),
        'pending_clone_items': pending_clone_items,
        'confirm_clone_items': confirm_clone_items,
    }


def is_structured_story_input(path: Path | None) -> bool:
    return bool(path and path.suffix.lower() in STRUCTURED_STORY_EXTENSIONS)


def materialize_structured_story_input(path: Path) -> Path:
    workspace_dir = resolve_story_workspace_dir(path)
    target_path = workspace_dir / path.name
    if path.resolve() == target_path.resolve():
        return path.resolve()

    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, target_path)
    return target_path.resolve()


def build_downstream_blockers(
    *,
    story_input_path: Path | None,
    casting_output_path: Path | None,
    casting_status: dict[str, Any] | None,
    downstream_mode: str,
) -> list[str]:
    blockers: list[str] = []
    if downstream_mode == 'off':
        blockers.append('downstream_mode=off')
        return blockers

    if not story_input_path or not casting_output_path:
        blockers.append('缺少 structured story input 或 casting-plan 输出路径')
        return blockers

    if not is_structured_story_input(story_input_path):
        blockers.append('当前新的下游链路只支持结构化 yaml/json，暂不支持直接从 txt 继续到 tts-requests')
        return blockers

    if downstream_mode == 'force':
        return blockers

    if casting_status and casting_status.get('pending_manual_role_count', 0) > 0:
        blockers.append(
            f"仍有 {casting_status['pending_manual_role_count']} 个角色待人工确认，auto 模式先不继续下游链路"
        )
    if casting_status and casting_status.get('pending_clone_confirmation_count', 0) > 0:
        blockers.append(
            f"仍有 {casting_status['pending_clone_confirmation_count']} 个待确认 clone，auto 模式先不继续下游链路"
        )
    return blockers


def run_downstream_pipeline(
    *,
    args: argparse.Namespace,
    story_input_path: Path | None,
    casting_output_path: Path | None,
    casting_status: dict[str, Any] | None,
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        'mode': args.downstream_mode,
        'eligible_story_input': str(story_input_path) if story_input_path else '',
        'casting_output_path': str(casting_output_path) if casting_output_path else '',
        'structured_input': is_structured_story_input(story_input_path),
        'status': 'skipped',
        'blockers': [],
        'build_tts_requests': None,
        'synthesize': None,
        'finalize': None,
        'request_artifact_path': '',
        'final_output_path': '',
    }

    blockers = build_downstream_blockers(
        story_input_path=story_input_path,
        casting_output_path=casting_output_path,
        casting_status=casting_status,
        downstream_mode=args.downstream_mode,
    )
    if blockers:
        summary['blockers'] = blockers
        summary['status'] = 'disabled' if args.downstream_mode == 'off' else 'blocked'
        return summary

    assert story_input_path is not None
    assert casting_output_path is not None

    build_command = [
        'python3',
        str(BUILD_TTS_REQUESTS_SCRIPT),
        '--input',
        str(story_input_path),
        '--casting',
        str(casting_output_path),
    ]
    if args.tts_model:
        build_command.extend(['--model', args.tts_model])
    if args.sample_rate is not None:
        build_command.extend(['--sample-rate', str(args.sample_rate)])
    if args.response_format:
        build_command.extend(['--response-format', args.response_format])
    if args.volume is not None:
        build_command.extend(['--volume', str(args.volume)])
    for tone_entry in args.tone_map:
        build_command.extend(['--tone-map', tone_entry])
    if args.pronunciation_map_file:
        build_command.extend(['--pronunciation-map-file', str(Path(args.pronunciation_map_file).resolve())])

    build_result = run_json_command_safe(build_command)
    summary['build_tts_requests'] = build_result
    if not build_result.get('ok'):
        summary['status'] = 'blocked'
        summary['blockers'] = [build_result.get('error') or 'build_tts_requests 失败']
        return summary

    request_artifact_path = trim_string((build_result.get('result') or {}).get('output_path'))
    summary['request_artifact_path'] = request_artifact_path

    synth_command = [
        'python3',
        str(SYNTHESIZE_TTS_REQUESTS_SCRIPT),
        '--input',
        request_artifact_path,
        '--request-mode',
        args.synthesis_request_mode,
        '--api-key-env',
        args.api_key_env or 'STEP_API_KEY',
        '--base-url',
        args.base_url or 'https://api.stepfun.com/v1',
    ]
    if args.force_synthesis:
        synth_command.append('--force')

    synth_result = run_json_command_safe(synth_command)
    summary['synthesize'] = synth_result
    if not synth_result.get('ok'):
        summary['status'] = 'failed'
        summary['blockers'] = [synth_result.get('error') or 'synthesize_tts_requests 失败']
        return summary

    synth_payload = synth_result.get('result') or {}
    if int(synth_payload.get('failed_count') or 0) > 0:
        summary['status'] = 'partial'
        summary['blockers'] = [
            f"仍有 {synth_payload.get('failed_count')} 个段落合成失败，请检查 requests artifact 后再重放。"
        ]
        return summary

    finalize_command = [
        'python3',
        str(FINALIZE_AUDIOBOOK_SCRIPT),
        '--input',
        request_artifact_path,
    ]
    if args.final_output:
        finalize_command.extend(['--output', args.final_output])
    if args.normalize_final:
        finalize_command.append('--normalize')
    if args.force_finalize:
        finalize_command.append('--force')

    finalize_result = run_json_command_safe(finalize_command)
    summary['finalize'] = finalize_result
    if not finalize_result.get('ok'):
        summary['status'] = 'partial'
        summary['blockers'] = [finalize_result.get('error') or 'finalize_audiobook 失败']
        return summary

    finalize_payload = finalize_result.get('result') or {}
    summary['final_output_path'] = trim_string(finalize_payload.get('output_path'))
    summary['status'] = 'completed'
    return summary


def build_next_actions(
    *,
    voice_review_status: dict[str, Any],
    casting_status: dict[str, Any] | None,
    clone_preview: dict[str, Any],
    downstream_status: dict[str, Any] | None = None,
    artifact_manifest_path: str = '',
) -> list[str]:
    actions: list[str] = []

    if voice_review_status['pending_count'] > 0:
        actions.append(
            f"检查 {voice_review_status['review_path']} 里的 clones.<asset_id>.manual，确认克隆音色真实描述。"
        )

    if casting_status and casting_status['pending_manual_role_count'] > 0:
        actions.append(
            f"检查 {casting_status['casting_review_path']} 里的 roles.<role_id>.manual，确认最终角色选角。"
        )

    if casting_status and casting_status['pending_clone_confirmation_count'] > 0:
        actions.append(
            f"检查 {casting_status['clone_review_path']} 里的 items.<asset_id>.manual.decision，决定 confirm_clone 或 skip。"
        )

    if clone_preview.get('target_count', 0) > 0:
        actions.append(
            '如确认无误，可执行 python3 scripts/clone_selected_voices.py 进入真正付费克隆。'
        )

    if downstream_status:
        if downstream_status.get('status') == 'completed' and downstream_status.get('final_output_path'):
            actions.append(
                f"最终音频已导出到 {downstream_status['final_output_path']}；如需局部重放，可直接编辑 tts-requests 后重跑 synthesize/finalize。"
            )
        elif downstream_status.get('status') in {'blocked', 'partial', 'failed'}:
            for blocker in downstream_status.get('blockers') or []:
                actions.append(str(blocker))

    if artifact_manifest_path:
        actions.append(
            f"想看本轮中间产物，可执行 python3 scripts/list_story_artifacts.py --manifest {artifact_manifest_path} --level review --pretty。"
        )

    if not actions:
        actions.append('当前前置准备已完成；下一步可以继续进入有声书合成链路。')

    return actions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Run the audiobook workflow: voice sync, casting, clone preview, and when possible the downstream synthesis chain.'
    )
    parser.add_argument('--story-input', dest='story_input', help='Story/script path for casting generation')
    parser.add_argument('--casting-output', dest='casting_output', help='Optional casting-plan output path')
    parser.add_argument('--voice-input', dest='voice_input', action='append', default=[], help='Reference audio to ingest before casting; may be repeated')
    parser.add_argument('--process-inbox', action='store_true', help='Process every file currently in voices/inbox before casting')
    parser.add_argument('--refresh-casting-only', action='store_true', help='Only rebuild effective casting from existing review files')
    parser.add_argument('--library', default=str(DEFAULT_LIBRARY_PATH), help='Path to voice-library.yaml')
    parser.add_argument('--script-output', dest='script_output', help='Optional output path for generated structured script when story-input is raw txt')
    parser.add_argument('--script-model', dest='script_model', help='Optional model override for txt -> structured script generation')
    parser.add_argument('--script-chunk-chars', dest='script_chunk_chars', type=int, help='Optional per-chunk text size for txt -> structured script generation')
    parser.add_argument('--model')
    parser.add_argument('--role-model', dest='role_model')
    parser.add_argument('--selection-model', dest='selection_model')
    parser.add_argument('--base-url', dest='base_url')
    parser.add_argument('--api-key-env', dest='api_key_env')
    parser.add_argument('--temperature', type=float)
    parser.add_argument('--max-tokens', dest='max_tokens')
    parser.add_argument('--top-candidates', dest='top_candidates')
    parser.add_argument('--downstream-mode', choices=['auto', 'off', 'force'], default='auto')
    parser.add_argument('--tts-model', dest='tts_model', help='Optional TTS model override for build_tts_requests')
    parser.add_argument('--sample-rate', dest='sample_rate', type=int, help='Optional sample rate override for build_tts_requests')
    parser.add_argument('--response-format', dest='response_format', help='Optional audio format override for build_tts_requests')
    parser.add_argument('--volume', type=float, help='Optional TTS volume passthrough for build_tts_requests')
    parser.add_argument(
        '--tone-map',
        dest='tone_map',
        action='append',
        default=[],
        help='Repeatable pronunciation_map.tone entry for build_tts_requests',
    )
    parser.add_argument(
        '--pronunciation-map-file',
        dest='pronunciation_map_file',
        help='Optional JSON/YAML pronunciation_map file for build_tts_requests',
    )
    parser.add_argument('--synthesis-request-mode', dest='synthesis_request_mode', choices=['auto', 'split_instruction', 'inline_prefixed'], default='auto')
    parser.add_argument('--force-synthesis', action='store_true', help='Force re-synthesis of existing successful segment artifacts')
    parser.add_argument('--final-output', dest='final_output', help='Optional final audio output override')
    parser.add_argument('--normalize-final', action='store_true', help='Apply ffmpeg loudnorm when exporting final audio')
    parser.add_argument('--force-finalize', action='store_true', help='Overwrite the final output path if it already exists')
    parser.add_argument(
        '--show-artifacts',
        choices=['essential', 'review', 'debug'],
        help='Also print a human-readable artifact view to stderr after the JSON summary',
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    library_path = Path(args.library).resolve()
    if not library_path.exists():
        raise RuntimeError(f'音色库文件不存在: {library_path}')

    if args.refresh_casting_only and not args.story_input:
        raise RuntimeError('--refresh-casting-only 需要同时提供 --story-input')

    library = load_yaml(library_path)
    library_dir = library_path.parent
    requested_voice_inputs = collect_requested_voice_inputs(args, library, library_dir)
    if args.refresh_casting_only and requested_voice_inputs:
        raise RuntimeError(
            '--refresh-casting-only 不应和新的 voice input / inbox 处理一起使用；如果想让新音色参与选角，请去掉这个 flag。'
        )

    official_sync: dict[str, Any] | None = None
    voice_sync_results: list[dict[str, Any]] = []

    if requested_voice_inputs:
        for voice_input in requested_voice_inputs:
            voice_sync_results.append(
                run_json_command(
                    [
                        'python3',
                        str(SYNC_SCRIPT),
                        '--library',
                        str(library_path),
                        '--input',
                        str(voice_input),
                    ]
                )
            )
    else:
        official_sync = run_json_command(
            [
                'python3',
                str(SYNC_SCRIPT),
                '--library',
                str(library_path),
                '--refresh-official-only',
            ]
        )

    casting_result: dict[str, Any] | None = None
    casting_status: dict[str, Any] | None = None
    story_input_path: Path | None = None
    effective_story_input_path: Path | None = None
    casting_output_path: Path | None = None
    structured_script_result: dict[str, Any] | None = None
    if args.story_input:
        story_input_path = Path(args.story_input).resolve()
        if not story_input_path.exists():
            raise RuntimeError(f'故事输入不存在: {story_input_path}')
        effective_story_input_path = story_input_path

        if not is_structured_story_input(story_input_path):
            generate_command = [
                'python3',
                str(GENERATE_STRUCTURED_SCRIPT),
                '--input',
                str(story_input_path),
                '--library',
                str(library_path),
            ]
            if args.script_output:
                generate_command.extend(['--output', str(Path(args.script_output).resolve())])
            if args.script_model:
                generate_command.extend(['--model', args.script_model])
            if args.base_url:
                generate_command.extend(['--base-url', args.base_url])
            if args.api_key_env:
                generate_command.extend(['--api-key-env', args.api_key_env])
            if args.temperature is not None:
                generate_command.extend(['--temperature', str(args.temperature)])
            if args.max_tokens is not None:
                generate_command.extend(['--max-tokens', str(args.max_tokens)])
            if args.script_chunk_chars is not None:
                generate_command.extend(['--chunk-chars', str(args.script_chunk_chars)])

            structured_script_result = run_json_command(generate_command)
            effective_story_input_path = Path(structured_script_result['output_path']).resolve()
        else:
            effective_story_input_path = materialize_structured_story_input(story_input_path)

        casting_output_path = (
            Path(args.casting_output).resolve()
            if args.casting_output
            else resolve_default_casting_plan_path(effective_story_input_path)
        )

        command = [
            'python3',
            str(RECOMMEND_SCRIPT),
            '--input',
            str(effective_story_input_path),
            '--library',
            str(library_path),
            '--output',
            str(casting_output_path),
        ]
        if args.refresh_casting_only:
            command.append('--refresh-only')
        for flag, value in [
            ('--model', args.model),
            ('--role-model', args.role_model),
            ('--selection-model', args.selection_model),
            ('--base-url', args.base_url),
            ('--api-key-env', args.api_key_env),
            ('--temperature', args.temperature),
            ('--max-tokens', args.max_tokens),
            ('--top-candidates', args.top_candidates),
        ]:
            if value is None:
                continue
            command.extend([flag, str(value)])

        casting_result = run_json_command(command)
        casting_status = collect_casting_status(casting_output_path)

    clone_preview = run_json_command(
        ['python3', str(CLONE_SCRIPT), '--library', str(library_path), '--dry-run']
    )

    downstream_status = run_downstream_pipeline(
        args=args,
        story_input_path=effective_story_input_path,
        casting_output_path=casting_output_path,
        casting_status=casting_status,
    )

    library_after = load_yaml(library_path)
    voice_review_status = collect_pending_voice_reviews(library_after, library_dir)
    selected_clone_assets = collect_selected_clone_assets(library_after)
    artifact_manifest = build_story_artifact_manifest(
        story_input_path=story_input_path,
        effective_story_input_path=effective_story_input_path,
        structured_script_artifact_path=((structured_script_result or {}).get('artifact_path') if structured_script_result else ''),
        casting_output_path=casting_output_path,
        casting_review_path=((casting_status or {}).get('casting_review_path') if casting_status else ''),
        clone_review_path=((casting_status or {}).get('clone_review_path') if casting_status else ''),
        role_profiles_path=((casting_result or {}).get('role_profiles_path') if casting_result else ''),
        casting_selection_path=((casting_result or {}).get('casting_response_path') if casting_result else ''),
        tts_requests_path=((downstream_status or {}).get('request_artifact_path') if downstream_status else ''),
        library_path=library_path,
    )
    artifact_manifest_path = save_story_artifact_manifest(artifact_manifest)

    summary = {
        'mode': 'run-audiobook',
        'library_path': str(library_path),
        'story_input_path': str(story_input_path) if story_input_path else '',
        'effective_story_input_path': str(effective_story_input_path) if effective_story_input_path else '',
        'casting_output_path': str(casting_output_path) if casting_output_path else '',
        'processed_voice_input_count': len(requested_voice_inputs),
        'processed_voice_inputs': [str(path) for path in requested_voice_inputs],
        'official_sync': official_sync,
        'voice_sync_results': voice_sync_results,
        'structured_script': structured_script_result,
        'casting': casting_result,
        'casting_status': casting_status,
        'voice_review_status': voice_review_status,
        'selected_clone_assets': selected_clone_assets,
        'clone_preview': clone_preview,
        'downstream': downstream_status,
        'artifact_manifest': {
            'manifest_path': str(artifact_manifest_path),
            'artifact_base_dir': artifact_manifest.get('artifact_base_dir'),
            'counts': artifact_manifest.get('counts') or {},
            'essential_items': select_manifest_items(artifact_manifest, 'essential'),
        },
        'next_actions': build_next_actions(
            voice_review_status=voice_review_status,
            casting_status=casting_status,
            clone_preview=clone_preview,
            downstream_status=downstream_status,
            artifact_manifest_path=str(artifact_manifest_path),
        ),
    }
    if args.show_artifacts:
        summary['artifact_manifest']['preview_level'] = args.show_artifacts
        summary['artifact_manifest']['preview_items'] = select_manifest_items(
            artifact_manifest,
            args.show_artifacts,
        )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.show_artifacts:
        print(format_manifest_pretty(artifact_manifest, args.show_artifacts), file=sys.stderr, end='')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:  # pragma: no cover - CLI error path
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from error
