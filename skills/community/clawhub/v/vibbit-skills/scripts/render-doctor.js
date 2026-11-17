#!/usr/bin/env node
'use strict'

// Read-only discovery. Never load project code, run package managers, or fetch dependencies.
const fs = require('node:fs')
const os = require('node:os')
const path = require('node:path')

const ENGINES = {
  remotion: {
    skills: ['remotion-best-practices', 'remotion-create', 'remotion-markup', 'remotion-studio', 'remotion-render'],
    packages: ['remotion', '@remotion/cli'],
    cli: 'remotion',
  },
  hyperframes: {
    skills: ['hyperframes', 'hyperframes-core', 'hyperframes-animation', 'hyperframes-cli', 'motion-graphics', 'general-video'],
    packages: ['hyperframes'],
    cli: 'hyperframes',
  },
}

function expandPath(value, home) {
  if (value === '~') return home
  if (value.startsWith('~/') || value.startsWith('~\\')) return path.resolve(home, value.slice(2))
  return path.resolve(value)
}

function isDirectory(file) {
  try { return fs.statSync(file).isDirectory() } catch { return false }
}

function readJson(file) {
  let data
  try {
    if (!fs.statSync(file).isFile()) return { status: 'not_file' }
    data = fs.readFileSync(file, 'utf8')
  } catch (error) {
    return { status: error.code === 'ENOENT' ? 'missing' : 'unreadable' }
  }
  try {
    const parsed = JSON.parse(data)
    return parsed && typeof parsed === 'object' && !Array.isArray(parsed)
      ? { status: 'readable', data: parsed }
      : { status: 'invalid_object' }
  } catch { return { status: 'invalid_json' } }
}

function ancestorDirectories(directory) {
  const directories = []
  while (directory) {
    directories.push(directory)
    const parent = path.dirname(directory)
    if (parent === directory) break
    directory = parent
  }
  return directories
}

function executableIn(name, directories, platform, env) {
  const extensions = platform === 'win32'
    ? ['', ...(env.PATHEXT || '.EXE;.CMD;.BAT').split(';').filter(Boolean)]
    : ['']
  for (const directory of directories) {
    if (!directory) continue
    for (const extension of extensions) {
      const candidate = path.join(directory, name + extension)
      try {
        if (!fs.statSync(candidate).isFile()) continue
        fs.accessSync(candidate, platform === 'win32' ? fs.constants.F_OK : fs.constants.X_OK)
        return { status: 'located', path: path.resolve(candidate) }
      } catch { /* Try the next bounded candidate; do not execute it. */ }
    }
  }
  return { status: 'not_found_in_checked_paths' }
}

function skillAt(root, name) {
  const file = path.join(root, name, 'SKILL.md')
  try {
    if (!fs.statSync(file).isFile()) return null
    fs.accessSync(file, fs.constants.R_OK)
    return { name, path: path.resolve(file), status: 'file_readable', host_discovery_verified: false, provenance_verified: false }
  } catch (error) {
    return error.code === 'ENOENT' ? null : { name, path: path.resolve(file), status: 'unreadable' }
  }
}

function inspectEnvironment(options = {}) {
  const engine = options.engine || 'all'
  if (engine !== 'all' && !Object.hasOwn(ENGINES, engine)) throw new Error('engine must be remotion, hyperframes, or all')
  const env = options.env || process.env
  const home = options.home || os.homedir()
  const platform = options.platform || process.platform
  const project = options.project ? expandPath(options.project, home) : null
  const projectExists = project !== null && isDirectory(project)
  const projectRoots = projectExists ? ancestorDirectories(project) : []
  const packageResult = projectExists ? readJson(path.join(project, 'package.json')) : null
  const packageData = packageResult?.data || {}
  const declared = { ...packageData.dependencies, ...packageData.devDependencies, ...packageData.optionalDependencies }
  const defaults = [
    ...(projectExists ? [path.join(project, '.agents', 'skills'), path.join(project, '.claude', 'skills')] : []),
    ...(env.CODEX_HOME ? [path.join(env.CODEX_HOME, 'skills')] : []),
    path.join(home, '.codex', 'skills'),
    path.join(home, '.agents', 'skills'),
    path.join(home, '.claude', 'skills'),
  ]
  const roots = [...new Set((options.skillRoots?.length ? options.skillRoots : defaults).map(p => expandPath(p, home)))]
  const pathDirectories = (env.PATH || '').split(platform === 'win32' ? ';' : ':').filter(Boolean)
  const engines = {}
  for (const name of engine === 'all' ? Object.keys(ENGINES) : [engine]) {
    const spec = ENGINES[name]
    const skills = roots.flatMap(root => spec.skills.map(skill => skillAt(root, skill)).filter(Boolean))
    const packages = spec.packages.map(packageName => {
      let result = { name: packageName, declared: typeof declared[packageName] === 'string' ? declared[packageName] : null,
        status: projectExists ? 'not_found_in_project_ancestors' : 'project_not_checked' }
      for (const directory of projectRoots) {
        const file = path.join(directory, 'node_modules', packageName, 'package.json')
        const found = readJson(file)
        if (found.status === 'missing') continue
        result = { ...result, status: found.status, path: file,
          installed_version: typeof found.data?.version === 'string' ? found.data.version : null }
        break
      }
      return result
    })
    const projectCli = executableIn(spec.cli, projectRoots.map(p => path.join(p, 'node_modules', '.bin')), platform, env)
    const cli = projectCli.status === 'located'
      ? { ...projectCli, origin: 'project_or_ancestor' }
      : { ...executableIn(spec.cli, pathDirectories, platform, env), origin: 'PATH' }
    engines[name] = {
      skills_status: skills.some(s => s.status === 'file_readable') ? 'candidate_files_found' : 'not_found_in_checked_roots',
      skills, packages, cli,
      versions_compatible: 'not_verified',
      render_verified: false,
    }
  }
  return {
    mode: 'read_only_discovery',
    runtime: { node: process.version, platform, arch: process.arch },
    checked_skill_roots: roots,
    project: project === null ? { status: 'not_supplied' } : {
      path: project, status: projectExists ? 'directory_found' : 'not_found_or_unreadable',
      package_json_status: packageResult?.status || 'not_checked',
    },
    tools: Object.fromEntries(['npm', 'pnpm', 'bun', 'ffmpeg', 'ffprobe'].map(name => [name, executableIn(name, pathDirectories, platform, env)])),
    engines,
    limitations: ['Candidate files do not prove official provenance or host skill discovery.',
      'No dependency compatibility, browser, font, media, template, or render verification was performed.',
      'No installer, package manager, engine, project code, or network request was executed.'],
  }
}

function parseArguments(args) {
  const options = { skillRoots: [] }
  for (let i = 0; i < args.length; i++) {
    const name = args[i]
    if (name === '--help' || name === '-h') { options.help = true; continue }
    if (!['--engine', '--project', '--skill-root'].includes(name)) throw new Error('Unknown argument: ' + name)
    const value = args[++i]
    if (!value || value.startsWith('--')) throw new Error('Missing value for ' + name)
    if (name === '--skill-root') options.skillRoots.push(value)
    else {
      const key = name.slice(2)
      if (options[key]) throw new Error('Repeated argument: ' + name)
      options[key] = value
    }
  }
  return options
}

if (require.main === module) {
  try {
    const options = parseArguments(process.argv.slice(2))
    if (options.help) {
      process.stdout.write('Usage: node render-doctor.js [--engine remotion|hyperframes|all] [--project PATH] [--skill-root PATH ...]\nRead-only discovery; does not install or verify rendering.\n')
    } else process.stdout.write(JSON.stringify(inspectEnvironment(options), null, 2) + '\n')
  } catch (error) {
    process.stderr.write(JSON.stringify({ error: error.message }) + '\n')
    process.exitCode = 2
  }
}

module.exports = { inspectEnvironment, parseArguments }
