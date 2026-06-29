from __future__ import annotations

import argparse
import json

import catalog
import gitea_api as g
import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def mark_deleted_documents(owner: str, repo: str, source_id: str, deleted_files: list[dict]) -> list[dict]:
    cat = catalog.read(owner, repo)
    marked = []
    for deleted in deleted_files:
        source_path = deleted.get("path", "")
        if not source_path:
            continue
        matched = None
        for doc in cat.get("documents", []):
            if doc.get("source_id") == source_id and doc.get("source_path") == source_path:
                matched = doc
                break
        if not matched:
            continue
        matched["source_deleted"] = True
        matched["source_deleted_at"] = now_str()
        matched["updated_at"] = now_str()
        result = g.get_file(owner, repo, matched["file"])
        if result and "源文件已从资料源删除" not in result[0]:
            notice = f"> 注意：该资料对应的源文件 `{source_path}` 已从资料源删除（{now_str()}）。\n\n"
            g.put_file(owner, repo, matched["file"], notice + result[0], "paper-kb: mark source deleted", sha=result[1])
        marked.append({"source_path": source_path, "page": matched.get("file", "")})
    if marked:
        catalog.write(owner, repo, cat)
        catalog.regen_index(owner, repo, repo, cat)
    return marked


def split_changed_files(changes: dict) -> tuple[list[dict], list[dict], list[dict]]:
    changed = list(changes.get("added", [])) + list(changes.get("modified", []))
    document_files = [item for item in changed if item.get("action") == "document"]
    code_files = [item for item in changed if item.get("action") in {"code_context", "dependency_context"}]
    skipped_files = [item for item in changed if item.get("action") == "skip"]
    return document_files, code_files, skipped_files


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_id", required=True)
    parser.add_argument("--batch_size", type=int, default=100)
    args = parser.parse_args()

    jobs = sc.jobs()
    job = jobs.get(args.job_id)
    if not job:
        out(json_fail("job_not_found", "找不到增量更新 job。"))
        return
    if job.get("type") != "incremental_compile":
        out(json_fail("bad_job_type", "该 job 不是 incremental_compile。"))
        return

    source_id = job.get("source_id", "")
    source = sc.sources().get(source_id)
    if not source:
        out(json_fail("source_not_found", "找不到该 job 对应的资料源。"))
        return

    owner = job.get("target_kb_owner") or source.get("target_kb_owner")
    repo = job.get("target_kb_repo") or source.get("target_kb_repo")
    changes = job.get("changes", {})
    deleted_files = list(changes.get("deleted", []))
    try:
        marked_deleted = mark_deleted_documents(owner, repo, source_id, deleted_files)
    except Exception as exc:
        out(json_fail("mark_deleted_failed", str(exc)))
        return

    document_files, code_files, skipped_files = split_changed_files(changes)
    needs_semantic = bool(document_files or code_files)
    now = now_str()
    job.update({
        "status": "running" if needs_semantic else "completed",
        "document_files": document_files,
        "code_files": code_files,
        "skipped_files": skipped_files,
        "deleted_files": deleted_files,
        "marked_deleted": marked_deleted,
        "total_documents": len(document_files),
        "processed_documents": 0,
        "failed_documents": 0,
        "skipped_documents": len(skipped_files),
        "processed_deleted": len(marked_deleted),
        "batch_size": args.batch_size,
        "next_cursor": 0,
        "auto_continue": True,
        "execution_mode": "background_worker" if needs_semantic else job.get("execution_mode", ""),
        "worker_required": bool(needs_semantic),
        "worker_spawn": job.get("worker_spawn", {}),
        "updated_at": now,
    })
    if not needs_semantic:
        job.setdefault("notified", False)
        if not job.get("notified"):
            job["notify_status"] = "pending" if (job.get("deliver_to") or {}).get("target") or (job.get("deliver_to") or {}).get("targets") else "no_target"

    def mutate_jobs(current: dict) -> dict:
        current[args.job_id] = job
        return current

    sc.update_json("jobs.json", mutate_jobs, default={})

    if not needs_semantic:
        fingerprints = job.get("current_fingerprints", {})
        current_commit = job.get("current_commit", "")

        def mutate_sources(current: dict) -> dict:
            if source_id in current:
                src = current[source_id]
                if fingerprints:
                    src["file_fingerprints"] = fingerprints
                if current_commit:
                    src["last_commit"] = current_commit
                src["last_status"] = "completed"
                src["last_scan_time"] = now
                src["last_success_time"] = now
                current[source_id] = src
            return current

        sc.update_json("sources.json", mutate_sources, default={})

    out({
        "success": True,
        "job_id": args.job_id,
        "needs_semantic": needs_semantic,
        "document_files": len(document_files),
        "code_files": len(code_files),
        "skipped_files": len(skipped_files),
        "marked_deleted": len(marked_deleted),
        "status": job["status"],
    })


if __name__ == "__main__":
    main()
