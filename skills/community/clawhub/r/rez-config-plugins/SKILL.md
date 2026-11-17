---
name: rez-config-plugins
description: "Rez configuration layering and the plugin system — config precedence and merge rules, string expansion, DelayLoad, key settings (packages_path, implicit_packages, caching, package_filter), and the seven plugin types with their discovery mechanisms and entry points. Use when the user asks how to configure rez, why a setting is not taking effect, or how to write or install a plugin. Covers Rez 3.4.0."
---

# Rez configuration and plugins

> **One-sentence summary**: configuration is layered (each source *overrides*, not replaces, the
> previous), and everything extensible — shells, build systems, repositories, release hooks — is a
> plugin discovered either by `rezplugins` directory layout or by Python entry points.

Skill scope: configuration and plugins. For resolve behavior see `rez-resolve`; for the CLI see
`rez-cli`.

## Configuration precedence

Lowest to highest. Later sources win.

1. `rezconfig.py` shipped in the rez installation (defaults + documentation for every setting)
2. File pointed at by `REZ_CONFIG_FILE` — can be a path-like list to read several files
3. `$HOME/.rezconfig` or `$HOME/.rezconfig.py`
4. `REZ_<SETTING>_JSON` environment variable — value must be JSON-encoded
5. `REZ_<SETTING>` environment variable — e.g. `REZ_PACKAGES_PATH` overrides `packages_path`.
   **Takes precedence over the `_JSON` form when both are present.**
6. *(build/release only)* the package's own `config` section via `scope("config")`

Related: `REZ_DISABLE_HOME_CONFIG` skips the home config.

Verify what actually took effect:

```bash
rez-config                 # dump all settings
rez-config packages_path   # one setting
```

## Merge rules

Sources **merge**; they do not replace wholesale.

- Dicts are merged **recursively**.
- Non-dicts override the previous value.

To append/prepend to a list setting instead of replacing it, use `ModifyList`:

```python
release_hooks = ModifyList(append=["custom_release_notify"])
```

`prepend=[...]` is also supported.

## File formats

Both YAML (`.rezconfig`) and Python (`.rezconfig.py`) are supported. Choose Python when settings
must vary by platform. You only need to list settings that differ from the defaults.

## String expansion

Applied to all configuration settings:

- Environment variables: `${HOME}`
- `system` object properties: `{system.platform}`, `{system.arch}`, `{system.os}`

## DelayLoad

Keep a large setting out of the main config and load it only when referenced (YAML or JSON):

```python
default_relocatable_per_package = DelayLoad('/svr/configs/rez_relocs.yaml')
```

## Settings that matter most

| Setting | Default | Purpose |
|---|---|---|
| `packages_path` | see install | package search path |
| `local_packages_path` | `~/packages` | where `rez-build --install` lands |
| `release_packages_path` | `~/.rez/packages/int` | where `rez-release` deploys |
| `cache_packages_path` | `None` | package cache location |
| `implicit_packages` | `~platform=={system.platform}`, `~arch=={system.arch}`, `~os=={system.os}` | weak system constraints |
| `variant_select_mode` | `version_priority` | variant preference strategy |
| `plugin_path` | `[]` | where to find `rezplugins` |
| `package_filter` | `None` | hide packages from resolves |
| `package_definition_python_path` | `None` | extra import path for `package.py` |
| `resolve_caching` | `True` | cache resolves |
| `cache_package_files` / `cache_listdir` | `True` | filesystem caches |
| `default_cachable` | `False` | whether packages may be cached |
| `memcached_uri` | `[]` | back the caches with memcached |
| `error_on_missing_variant_requires` | `True` | fail on incomplete variant requirements |
| `pathed_env_vars` | any var ending in `PATH` | which vars get path-normalized |
| `rez_1_environment_variables` | `False` | legacy variable naming |
| `warn_old_commands` / `error_old_commands` | `True` / `False` | old-style `commands` detection |

The full, authoritative list with documentation lives in `src/rez/rezconfig.py` in the rez source.

## Plugins

Plugin types and their base classes:

| Type | Base class | Top-level settings |
|---|---|---|
| `build_process` | `rez.build_process.BuildProcess` *or* `BuildProcessHelper` | No |
| `build_system` | `rez.build_system.BuildSystem` | No |
| `command` | `rez.command.Command` | Yes |
| `package_repository` | `rez.package_repository.PackageRepository` + 3 `package_resources` classes | No |
| `release_hook` | `rez.release_hook.ReleaseHook` | Yes |
| `release_vcs` | `rez.release_vcs.ReleaseVCS` | Yes |
| `shell` | `rez.shells.Shell` | No |

Built-ins live in `src/rezplugins`. New plugins are encouraged **out-of-tree**.

List what is installed and its load status:

```bash
rez -i
```

Example output — note `release vcs / svn / FAILED: No module named 'pysvn'`, i.e. `rez -i` is the
quickest way to see a plugin that failed to import.

### Configuring plugins

```python
plugins = {
    "package_repository": {
        "filesystem": {}
    }
}
```

### Discovery mechanism 1 — `rezplugins` directory layout

Point `plugin_path` (or `REZ_PLUGIN_PATH`) at the directory **above** your `rezplugins` dir:

```
rezplugins/
├── __init__.py
└── <plugin_type>/
    ├── __init__.py
    └── <plugin name>.py
```

> The `rezplugins` directory name is not optional, and your sparse copy must be on
> `REZ_PLUGIN_PATH` only — **not** on `PYTHONPATH`. That ordering guarantees rez's own copy of
> `rezplugins` is found first.

### Discovery mechanism 2 — entry points (rez 3.3.0+)

One entry point per plugin type:

- `rez.plugins.build_process`
- `rez.plugins.build_system`
- `rez.plugins.command`
- `rez.plugins.package_repository`
- `rez.plugins.release_hook`
- `rez.plugins.release_vcs`
- `rez.plugins.shell`

This is the more flexible option: no special file layout, and one package can ship several plugins
of different types.

### Default settings for a plugin

Ship a `rezconfig.py` or `rezconfig.yml` beside the plugin module; rez loads it automatically.

```python
top_level_setting = "value"

plugin_name = {
    "setting_1": "value1"
}
```

`plugin_name` settings arrive as `self.settings`; `top_level_setting` as
`self.type_settings.top_level_setting`. Only the types marked "Yes" in the table above support
top-level settings.

### Overriding built-ins

Install a plugin with the same **name and type** as a built-in and rez prefers yours. This is the
supported way to modify built-in behavior without patching rez source.

## Troubleshooting

| Symptom | Check |
|---|---|
| Setting not taking effect | walk the precedence list; `REZ_<SETTING>` beats the `_JSON` form and beats files |
| Home config interfering | `REZ_DISABLE_HOME_CONFIG`, or inspect with `rez-config` |
| List setting got replaced not extended | use `ModifyList(append=[...])` |
| Plugin not found | `rez -i`; confirm `REZ_PLUGIN_PATH` points **above** `rezplugins` |
| Plugin import error | `rez -i` shows `FAILED: <error>` in the status column |
| Packages silently missing from resolves | `package_filter`, `rez-pkg-ignore`, `packages_path` order |
| Resolves look stale | `resolve_caching`; retest with `rez-env --no-cache` |

## Agent workflow

1. Confirm the effective value with `rez-config <setting>` before changing anything.
2. Prefer environment variables for one-off overrides, `REZ_CONFIG_FILE` for site-wide policy.
3. Use `ModifyList` whenever you mean "add to" rather than "replace".
4. Check `rez -i` before debugging a plugin by hand.
5. Put new plugins in entry-point packages unless you specifically need the directory layout.
