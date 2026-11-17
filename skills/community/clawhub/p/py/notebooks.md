# Notebooks — Hidden State and the Path Back to Modules

The defining hazard of a notebook is that the visible order is not the execution order. Everything below follows from that.

## Reproducibility

- Restart-and-run-all is the only proof that a notebook works. A notebook that depends on your kernel's history is a transcript, not a program — run it clean before every commit, share, or conclusion.
- Deleting a cell does not delete the name it defined. The variable, the import, and the monkeypatch all survive; `%reset -f` clears the namespace, a kernel restart clears everything.
- Re-running a cell that mutates in place (`df.drop(...)`, `xs.append(...)`) compounds: run it twice and the data is different. Write cells that are safe to re-run — assign to a new name, or rebuild from the source each time (`collections.md`).
- Execution counts (`In [12]`) are the audit trail: non-monotonic numbers in a notebook you are asked to trust mean the results came from a state nobody can reconstruct.

## Environment

- `%pip install x` installs into the KERNEL's interpreter. `!pip install x` runs a shell where `pip` may belong to an entirely different Python — the notebook form of the bare-pip bug (`packaging.md`). Use the magic.
- The kernel is not your shell's activated venv: a kernelspec points at one specific interpreter. After creating the venv, register it once with `python -m ipykernel install --user --name myproj`, then select that kernel.
- `%load_ext autoreload` + `%autoreload 2` picks up edits to imported modules without a restart — but objects created before the edit keep the OLD class, so `isinstance` starts failing against what looks like the same class. When identity gets strange, restart; autoreload is a convenience, not a semantics.
- The kernel's working directory is normally the notebook's own directory, not the project root — relative paths behave differently here than in the module you copied them from. Anchor explicitly (`files.md`).

## Debugging and Measuring

- `%debug` immediately after an exception drops into post-mortem pdb at the failing frame; `%pdb on` arms it for every future error (`debugging.md`).
- `%timeit stmt` repeats and reports the best run; `%%time` times a whole cell once. Same discipline as anywhere else: state the input size with the number (`performance.md`).
- `%whos` lists live names with their types and sizes. A kernel using tens of GB is almost always three copies of the same dataframe — `del` the intermediates and call `gc.collect()`, or restart.
- `asyncio.run()` raises inside a notebook because a loop is already running; top-level `await` works in IPython (`concurrency.md`).

## Version Control and Leaks

- Outputs are stored inside the `.ipynb`: a printed API key, a token in a traceback, or a table of customer rows is committed permanently (`security.md`). Clear outputs before committing anything with real data.
- The JSON diff of a notebook is unreadable, and merge conflicts inside it are usually unresolvable. `nbstripout` (strip outputs on commit) or `jupytext` (a paired `.py` that is the reviewable artifact) fixes both.
- Large images and dataframes in outputs bloat the repository — the file grows by megabytes per run.

## Graduating To Modules

- The moment a notebook is copied to start a second analysis, its functions are a library. Move them into a package, `import` it, and leave the notebook as the narrative around the calls.
- Only module code can be tested and type-checked (`testing.md`, `type-checking.md`); code that only exists in cells is code with no safety net.
- Parameterized runs on a schedule: papermill executes a notebook with injected parameters and writes an output copy. Acceptable for reports; a service belongs in a module with an entry point (`cli.md`).
