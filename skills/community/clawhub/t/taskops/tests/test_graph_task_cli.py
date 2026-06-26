import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI = REPO_ROOT / "scripts" / "graph_task.py"
PACKAGER = Path("/home/jimmy/.npm-global/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py")


class GraphTaskCliTests(unittest.TestCase):
    maxDiff = None

    def run_cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=check,
        )

    def run_git(self, *args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
        env = {
            **os.environ,
            "GIT_AUTHOR_NAME": "Graph Task Tests",
            "GIT_AUTHOR_EMAIL": "graph-task-tests@example.com",
            "GIT_COMMITTER_NAME": "Graph Task Tests",
            "GIT_COMMITTER_EMAIL": "graph-task-tests@example.com",
        }
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=check,
            env=env,
        )

    def test_end_to_end_cli_flow(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "demo-run"

            self.run_cli(
                "init",
                str(run_dir),
                "--id",
                "demo-project",
                "--title",
                "Demo project",
                "--description",
                "A minimal graph-task smoke test",
                "--goal",
                "Reach a valid inspectable graph",
            )
            self.run_cli(
                "add-step",
                str(run_dir),
                "--id",
                "step-1",
                "--step-type",
                "implementation",
                "--description",
                "Implement simple state handling",
            )
            self.run_cli(
                "add-phase",
                str(run_dir),
                "--step-id",
                "step-1",
                "--id",
                "phase-diverge-1",
                "--phase-type",
                "diverge",
                "--description",
                "Explore state management options",
            )
            self.run_cli(
                "add-node",
                str(run_dir),
                "--phase-id",
                "phase-diverge-1",
                "--id",
                "node-1",
                "--title",
                "Compare candidate libraries",
                "--description",
                "Check Zustand and Redux for current scope",
            )
            self.run_cli(
                "add-edge",
                str(run_dir),
                "--phase-id",
                "phase-diverge-1",
                "--id",
                "edge-1",
                "--from-node",
                "phase-diverge-1-root",
                "--to-node",
                "node-1",
                "--edge-type",
                "flow",
            )
            self.run_cli(
                "add-phase",
                str(run_dir),
                "--step-id",
                "step-1",
                "--id",
                "phase-verify-1",
                "--phase-type",
                "verify",
                "--description",
                "Verify the current choice",
            )
            self.run_cli(
                "add-phase-edge",
                str(run_dir),
                "--step-id",
                "step-1",
                "--id",
                "phase-edge-1",
                "--from-phase",
                "phase-diverge-1",
                "--to-phase",
                "phase-verify-1",
            )
            self.run_cli(
                "write-result",
                str(run_dir),
                "--node-id",
                "node-1",
                "--expected",
                "Choose a candidate state library",
                "--actual",
                "Selected Zustand after comparing complexity and setup cost",
                "--status",
                "done",
                "--notes",
                "Simple enough for the current scope",
            )

            validate = self.run_cli("validate", str(run_dir))
            self.assertIn("VALID", validate.stdout)

            summary = self.run_cli("summary", str(run_dir))
            self.assertIn("Selected Zustand", summary.stdout)
            self.assertTrue((run_dir / "summary.md").exists())

            graph = json.loads((run_dir / "graph.json").read_text(encoding="utf-8"))
            node = graph["project"]["steps"][0]["phases"][0]["nodes"][1]
            self.assertEqual(node["status"], "done")
            self.assertEqual(node["results"][0]["status"], "done")
            self.assertEqual(node["results"][0]["nodeId"], "node-1")

    def test_repeated_diverge_verify_phases_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "repeat-run"

            self.run_cli(
                "init",
                str(run_dir),
                "--id",
                "repeat-project",
                "--title",
                "Repeat project",
                "--description",
                "Ensure repeated phase types remain valid",
                "--goal",
                "Keep history while looping through phases",
            )
            self.run_cli(
                "add-step",
                str(run_dir),
                "--id",
                "step-1",
                "--step-type",
                "analysis",
                "--description",
                "Loop through diverge and verify more than once",
            )

            for phase_id, phase_type, description in [
                ("phase-diverge-1", "diverge", "Explore initial options"),
                ("phase-verify-1", "verify", "Check the first option"),
                ("phase-diverge-2", "diverge", "Re-open exploration after verification"),
                ("phase-verify-2", "verify", "Check the revised option"),
                ("phase-commit-1", "commit", "Lock the chosen path"),
            ]:
                self.run_cli(
                    "add-phase",
                    str(run_dir),
                    "--step-id",
                    "step-1",
                    "--id",
                    phase_id,
                    "--phase-type",
                    phase_type,
                    "--description",
                    description,
                )

            for edge_id, from_phase, to_phase in [
                ("phase-edge-1", "phase-diverge-1", "phase-verify-1"),
                ("phase-edge-2", "phase-verify-1", "phase-diverge-2"),
                ("phase-edge-3", "phase-diverge-2", "phase-verify-2"),
                ("phase-edge-4", "phase-verify-2", "phase-commit-1"),
            ]:
                self.run_cli(
                    "add-phase-edge",
                    str(run_dir),
                    "--step-id",
                    "step-1",
                    "--id",
                    edge_id,
                    "--from-phase",
                    from_phase,
                    "--to-phase",
                    to_phase,
                )

            validate = self.run_cli("validate", str(run_dir))
            self.assertIn("VALID", validate.stdout)

    def test_multiple_commit_phases_fail_before_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "invalid-commit-run"

            self.run_cli(
                "init",
                str(run_dir),
                "--id",
                "invalid-commit-project",
                "--title",
                "Invalid commit project",
                "--description",
                "Ensure only one commit phase is allowed",
                "--goal",
                "Catch duplicate commit phases",
            )
            self.run_cli(
                "add-step",
                str(run_dir),
                "--id",
                "step-1",
                "--step-type",
                "implementation",
                "--description",
                "Test duplicate commit phase validation",
            )
            self.run_cli(
                "add-phase",
                str(run_dir),
                "--step-id",
                "step-1",
                "--id",
                "phase-commit-1",
                "--phase-type",
                "commit",
                "--description",
                "First commit phase",
            )

            second_commit = self.run_cli(
                "add-phase",
                str(run_dir),
                "--step-id",
                "step-1",
                "--id",
                "phase-commit-2",
                "--phase-type",
                "commit",
                "--description",
                "Second commit phase should fail validation",
                check=False,
            )
            self.assertNotEqual(second_commit.returncode, 0)
            self.assertIn("already has a commit phase", second_commit.stdout + second_commit.stderr)

            validate = self.run_cli("validate", str(run_dir))
            self.assertIn("VALID", validate.stdout)

    def test_self_dogfood_example_validates(self):
        run_dir = REPO_ROOT / "examples" / "self-dogfood-project"

        validate = self.run_cli("validate", str(run_dir))
        self.assertIn("VALID", validate.stdout)

        summary = self.run_cli("show", str(run_dir))
        self.assertIn("Dogfood TaskOps on its own repo", summary.stdout)
        self.assertIn("step-self-dogfood", summary.stdout)
        self.assertIn("step-followups", summary.stdout)

    def test_obsidian_export_writes_linked_vault(self):
        run_dir = REPO_ROOT / "examples" / "self-dogfood-project"

        with tempfile.TemporaryDirectory() as tmp:
            export_dir = Path(tmp) / "vault"
            export = self.run_cli("export-obsidian", str(run_dir), str(export_dir))
            self.assertIn("Exported Obsidian vault", export.stdout)

            index_text = (export_dir / "index.md").read_text(encoding="utf-8")
            project_text = (export_dir / "projects" / "dogfood-phase1-project.md").read_text(encoding="utf-8")
            step_text = (export_dir / "steps" / "step-self-dogfood.md").read_text(encoding="utf-8")
            phase_text = (export_dir / "phases" / "step-self-dogfood__phase-diverge-execution-2.md").read_text(encoding="utf-8")
            node_text = (export_dir / "nodes" / "step-followups__phase-converge-findings-1__node-summarize-findings.md").read_text(encoding="utf-8")

            self.assertIn("[[projects/dogfood-phase1-project|Dogfood TaskOps on its own repo]]", index_text)
            self.assertIn("[[steps/step-self-dogfood|step-self-dogfood]]", project_text)
            self.assertIn("[[phases/step-self-dogfood__phase-diverge-execution-2|phase-diverge-execution-2]]", step_text)
            self.assertIn("[[nodes/step-self-dogfood__phase-diverge-execution-2__node-build-self-dogfood-example|node-build-self-dogfood-example]]", phase_text)
            self.assertIn("Strengths: repeated phases, step edges, and result records compose cleanly", node_text)

    def test_init_can_target_git_repo_checkout_with_project_subdir(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            remote_repo = tmp_path / "remote.git"
            seed_repo = tmp_path / "seed"
            checkout_dir = tmp_path / "checkout"

            self.run_git("init", "--bare", str(remote_repo), cwd=tmp_path)
            seed_repo.mkdir()
            self.run_git("init", "-b", "main", cwd=seed_repo)
            (seed_repo / "README.md").write_text("# vault\n", encoding="utf-8")
            self.run_git("add", ".", cwd=seed_repo)
            self.run_git("commit", "-m", "seed", cwd=seed_repo)
            self.run_git("remote", "add", "origin", str(remote_repo), cwd=seed_repo)
            self.run_git("push", "-u", "origin", "main", cwd=seed_repo)

            result = self.run_cli(
                "init",
                str(checkout_dir),
                "--repo-url",
                str(remote_repo),
                "--repo-branch",
                "main",
                "--id",
                "Demo Project",
                "--title",
                "Demo project",
                "--description",
                "Repo-backed init",
                "--goal",
                "Write under a project-specific subdirectory",
            )

            project_dir = checkout_dir / "demo-project"
            graph_path = project_dir / "graph.json"
            self.assertTrue(graph_path.exists(), msg=result.stdout + result.stderr)
            self.assertIn("Repo-backed project directory", result.stdout)

            graph = json.loads(graph_path.read_text(encoding="utf-8"))
            self.assertEqual(graph["project"]["id"], "Demo Project")
            self.assertEqual(graph["project"]["repo"]["url"], str(remote_repo))
            self.assertEqual(graph["project"]["repo"]["branch"], "main")
            self.assertEqual(graph["project"]["repo"]["projectDir"], "demo-project")

    def test_git_sync_commands_work_for_repo_backed_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            remote_repo = tmp_path / "remote.git"
            seed_repo = tmp_path / "seed"
            second_clone = tmp_path / "second"
            checkout_dir = tmp_path / "checkout"

            self.run_git("init", "--bare", str(remote_repo), cwd=tmp_path)
            seed_repo.mkdir()
            self.run_git("init", "-b", "main", cwd=seed_repo)
            (seed_repo / "README.md").write_text("# vault\n", encoding="utf-8")
            self.run_git("add", ".", cwd=seed_repo)
            self.run_git("commit", "-m", "seed", cwd=seed_repo)
            self.run_git("remote", "add", "origin", str(remote_repo), cwd=seed_repo)
            self.run_git("push", "-u", "origin", "main", cwd=seed_repo)

            self.run_cli(
                "init",
                str(checkout_dir),
                "--repo-url",
                str(remote_repo),
                "--repo-branch",
                "main",
                "--id",
                "Sync Demo",
                "--title",
                "Sync demo",
                "--description",
                "Repo-backed sync test",
                "--goal",
                "Exercise git sync commands",
            )

            run_dir = checkout_dir / "sync-demo"
            status = self.run_cli("git-status", str(run_dir))
            self.assertIn("sync: in-sync", status.stdout)

            self.run_cli(
                "add-step",
                str(run_dir),
                "--id",
                "step-1",
                "--step-type",
                "implementation",
                "--description",
                "Create a local change",
            )
            status_after_change = self.run_cli("git-status", str(run_dir))
            self.assertIn("dirty: yes", status_after_change.stdout)

            push = self.run_cli("git-push", str(run_dir), "--message", "Add first step")
            self.assertIn("Committed and pushed changes", push.stdout)

            self.run_git("clone", "--branch", "main", str(remote_repo), str(second_clone), cwd=tmp_path)
            (second_clone / "shared.md").write_text("hello\n", encoding="utf-8")
            self.run_git("add", ".", cwd=second_clone)
            self.run_git("commit", "-m", "Add shared note", cwd=second_clone)
            self.run_git("push", "origin", "HEAD:main", cwd=second_clone)

            status_behind = self.run_cli("git-status", str(run_dir))
            self.assertIn("sync: behind", status_behind.stdout)

            pull = self.run_cli("git-pull", str(run_dir))
            self.assertIn("Pulled latest changes", pull.stdout)
            self.assertTrue((checkout_dir / "shared.md").exists())

            sync = self.run_cli("git-sync", str(run_dir))
            self.assertIn("Pulled and pushed changes", sync.stdout)

    def test_md_first_minimal_example_validates_and_summarizes(self):
        example_root = REPO_ROOT / "examples" / "md-first-minimal"

        validate = self.run_cli("validate", str(example_root))
        self.assertIn("VALID", validate.stdout)
        self.assertIn("md-first project", validate.stdout)

        summary = self.run_cli("summary", str(example_root))
        self.assertIn("Project Alpha", summary.stdout)
        self.assertIn("results: 1", summary.stdout)
        self.assertTrue((example_root / "project-alpha" / "summary.md").exists())

    def test_md_first_validator_rejects_bad_result_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = REPO_ROOT / "examples" / "md-first-minimal"
            dst = tmp_path / "md-first-copy"
            shutil.copytree(src, dst)

            result_file = dst / "project-alpha" / "steps" / "step-1" / "phases" / "phase-diverge-1" / "results" / "result-0001.md"
            broken = result_file.read_text(encoding="utf-8").replace("node-compare-layout", "node-missing")
            result_file.write_text(broken, encoding="utf-8")

            validate = self.run_cli("validate", str(dst), check=False)
            self.assertNotEqual(validate.returncode, 0)
            self.assertIn("INVALID", validate.stdout)
            self.assertIn("nodeId 'node-missing' not found", validate.stdout)

    def test_skill_packages_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_copy = Path(tmp) / "graph-task"
            shutil.copytree(
                REPO_ROOT,
                skill_copy,
                ignore=shutil.ignore_patterns(".git", "__pycache__", ".dist", "*.pyc"),
            )
            output_dir = Path(tmp) / "dist"
            result = subprocess.run(
                [sys.executable, str(PACKAGER), str(skill_copy), str(output_dir)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, msg=result.stdout + "\n" + result.stderr)
            package_path = output_dir / "graph-task.skill"
            self.assertTrue(package_path.exists())

            with zipfile.ZipFile(package_path) as zf:
                names = set(zf.namelist())
            self.assertIn("graph-task/SKILL.md", names)
            self.assertIn("graph-task/scripts/graph_task.py", names)
            self.assertIn("graph-task/references/schema.graph-task.json", names)


if __name__ == "__main__":
    unittest.main()
