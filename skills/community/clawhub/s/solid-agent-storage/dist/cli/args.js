const argv = process.argv.slice(2);
export function getArg(name) {
    const idx = argv.indexOf(`--${name}`);
    return idx >= 0 ? argv[idx + 1] : undefined;
}
export function requireArg(name, usage) {
    const value = getArg(name);
    if (!value) {
        console.error(usage);
        process.exit(1);
    }
    return value;
}
export function getServerUrl() {
    return process.env.SOLID_SERVER_URL ?? getArg('serverUrl') ?? 'https://crawlout.io';
}
export function getPassphrase() {
    const passphrase = process.env.INTERITION_PASSPHRASE;
    if (!passphrase) {
        console.error(JSON.stringify({
            error: 'No passphrase provided. Set INTERITION_PASSPHRASE environment variable.',
        }));
        process.exit(1);
    }
    return passphrase;
}
//# sourceMappingURL=args.js.map