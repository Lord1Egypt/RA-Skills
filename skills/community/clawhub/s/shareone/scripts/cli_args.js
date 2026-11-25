// Command metadata owns argument parsing and the side-effect-free help surface.
const path = require('node:path');
const {emitError} = require('./shareone_client');
const contract = require('./api_contract.json');

const COMMON = {
    '--api-key': {value: 'key', description: 'Use an existing account key; Sudowork manages it through its proxy.'},
    '--base-url': {value: 'url', description: 'Explicit API deployment; otherwise use SHAREONE_BASE_URL or the default service.'},
    '--idempotency-key': {value: 'key', description: 'Reuse this intent key and identical input when replaying a supported creation.'},
    '--filename': {value: 'name', description: 'Artifact filename, retaining its actual format.'},
    '--password': {value: 'text', description: 'Share password; an empty string clears it on update.'},
    '--watermark': {value: 'text', description: 'Watermark text; an empty string clears it on update.'},
    '--slug': {value: 'slug', aliases: ['--custom-slug'], description: 'Explicit share slug; omitted updates retain it.'},
    '--share-id': {value: 'ref', description: 'Update this original text share, preserving its URL and comments.'},
    '--allow-comments': {value: 'boolean', choices: ['true', 'false'], description: 'Enable only when requested. New Agent text publications default to false; omitted updates retain the setting.'},
    '--allow-data': {value: 'boolean', choices: ['true', 'false'], description: 'Enable shared page storage only when requested; omitted updates retain the setting.'},
    '--viewer-scope': {value: 'scope', choices: contract.viewer_scopes, description: 'Private GitLab defaults to owner_and_collaborators; link export needs an operator grant and explicit owner selection.'},
    '--force-new': {description: 'Create another share when explicitly requested instead of updating a recorded share.'},
};

function commandLine({summary, result, positional, optional = false, options}) {
    const definitions = Object.fromEntries(Object.entries(options).map(([flag, spec]) => [flag, spec === true ? COMMON[flag] : spec]));
    const name = path.basename(process.argv[1]);
    const flags = Object.entries(definitions).map(([flag, spec]) => `[${flag}${spec.value ? ' <' + (spec.choices || [spec.value]).join('|') + '>' : ''}]`);
    const usage = ['Use when: ' + summary, 'Returns: ' + result,
        `Usage: node ${name} ${optional ? '[' + positional + ']' : '<' + positional + '>'} ${flags.join(' ')}`,
        ...Object.entries(definitions).map(([flag, spec]) => `  ${flag}${spec.aliases ? ' (' + spec.aliases.join(', ') + ')' : ''}  ${spec.description}`),
        '  --help, -h  Show this help without credentials, content reads, or network requests.'].join('\n');
    const args = process.argv.slice(2);
    if (args.length === 1 && ['--help', '-h'].includes(args[0])) { console.log(usage); process.exit(0); }
    const values = {}, positionals = [];
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        const flag = Object.keys(definitions).find(flag => flag === arg || definitions[flag].aliases?.includes(arg));
        if (flag) {
            const spec = definitions[flag];
            let value = true;
            if (spec.value) {
                value = args[++i];
                if (value === undefined || value.startsWith('--')) emitError('MISSING_VALUE', arg, {hint: usage});
                if (spec.normalize) value = spec.normalize(value);
                if (spec.choices && !spec.choices.includes(value)) emitError('BAD_ARGS', `Invalid ${arg}.`, {hint: usage});
                if (spec.value === 'boolean') value = value === 'true';
            }
            values[flag.slice(2)] = value;
        } else if (arg.startsWith('-')) emitError('UNKNOWN_ARGUMENT', arg, {hint: usage});
        else positionals.push(arg);
    }
    if (positionals.includes('') || positionals.length > 1 || (!optional && positionals.length !== 1)) emitError('BAD_ARGS', 'Incorrect positional arguments.', {hint: usage});
    if (values['base-url'] !== undefined) process.env.SHAREONE_BASE_URL = values['base-url'];
    return {values, positional: positionals[0] || null};
}

module.exports = {commandLine};
