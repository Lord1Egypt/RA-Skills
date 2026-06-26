# Release Checklist — Agent Memory V12

## Pre-Release

- [ ] All tests pass: `pytest agent_memory/tests/ -q`
- [ ] Benchmarks within thresholds: `python -m agent_memory.benchmarks.benchmark_suite --check-regression`
- [ ] Version updated in `VERSION` file
- [ ] Version updated in `agent_memory/__init__.py` docstring
- [ ] CHANGELOG.md updated with release date and changes
- [ ] README.md reflects current features
- [ ] API documentation matches code
- [ ] No V10/V11 version references remain
- [ ] DEPLOYMENT.md is accurate
- [ ] pyproject.toml metadata is correct
- [ ] Docker build succeeds: `docker build -t agent-memory:test .`
- [ ] Package builds: `python -m build`
- [ ] Package installs: `pip install dist/agent_memory-12.0.0-py3-none-any.whl`
- [ ] Import works: `python -c "from agent_memory import AgentMemory; print('OK')"`
- [ ] Quickstart demo runs: `python examples/quickstart.py`
- [ ] Security scan: `bandit -r agent_memory/ -c .bandit`
- [ ] No hardcoded secrets in code
- [ ] JWT default secret rejected in production mode

## Release

- [ ] Git tag created: `git tag v12.0.0`
- [ ] GitHub Release created with CHANGELOG excerpt
- [ ] PyPI upload: `twine upload dist/*`
- [ ] Docker Hub push: `docker push agent-memory:12.0.0`

## Post-Release

- [ ] GitHub Release page updated with assets
- [ ] Documentation site updated
- [ ] Announcement posted (blog, social, communities)
- [ ] Monitor PyPI download stats
- [ ] Monitor GitHub issues for regression reports
