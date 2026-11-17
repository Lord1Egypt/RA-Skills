/* Fixed application helper. User values remain JSON and NSTask argv data.
 * No shell, model, provider SDK, or Reminders write is performed here.
 */
ObjC.import('Foundation');

function atomicResult(path, result) {
    var content = $(JSON.stringify(result));
    if (!content.writeToFileAtomicallyEncodingError($(path), true, $.NSUTF8StringEncoding, null)) {
        throw new Error('Cannot write private helper result');
    }
    if (!$.NSFileManager.defaultManager.setAttributesOfItemAtPathError(
            $({NSFilePosixPermissions: 384}), $(path), null)) {
        throw new Error('Cannot protect helper result');
    }
}

function run() {
    var config = null;
    try {
        var args = ObjC.deepUnwrap($.NSProcessInfo.processInfo.arguments);
        var index = args.indexOf('--config');
        if (index < 0 || index + 1 >= args.length) throw new Error('Missing fixed config argument');
        var content = $.NSString.stringWithContentsOfFileEncodingError($(args[index + 1]), $.NSUTF8StringEncoding, null);
        if (!content) throw new Error('Cannot read fixed helper configuration');
        config = JSON.parse(ObjC.unwrap(content));
        if (config.version !== 1 || config.owner !== 'team-tasks.macos-sync.v1' ||
            typeof config.python !== 'string' || config.python.charAt(0) !== '/' ||
            !Array.isArray(config.argv) || !config.argv.every(function (x) { return typeof x === 'string'; }) ||
            !config.argv.length || config.argv[0].charAt(0) !== '/' ||
            ['scheduled', 'diagnose'].indexOf(config.mode) < 0 ||
            typeof config.logFile !== 'string' || config.logFile.charAt(0) !== '/' ||
            typeof config.helperResultFile !== 'string' || config.helperResultFile.charAt(0) !== '/') {
            throw new Error('Invalid fixed helper configuration');
        }
        var manager = $.NSFileManager.defaultManager;
        if (manager.fileExistsAtPath($(config.logFile))) {
            var attributes = manager.attributesOfItemAtPathError($(config.logFile), null);
            if (attributes && Number(ObjC.unwrap(attributes.objectForKey($.NSFileSize))) > 5242880) {
                var previous = config.logFile + '.previous';
                if (manager.fileExistsAtPath($(previous))) {
                    manager.removeItemAtPathError($(previous), null);
                }
                if (!manager.moveItemAtPathToPathError($(config.logFile), $(previous), null)) {
                    throw new Error('Cannot rotate sync log');
                }
            }
        }
        if (!manager.fileExistsAtPath($(config.logFile))) {
            if (!manager.createFileAtPathContentsAttributes($(config.logFile), $.NSData.data,
                    $({NSFilePosixPermissions: 384}))) throw new Error('Cannot create private sync log');
        }
        var log = $.NSFileHandle.fileHandleForWritingAtPath($(config.logFile));
        if (!log) throw new Error('Cannot open sync log');
        log.seekToEndOfFile;
        var task = $.NSTask.alloc.init;
        task.launchPath = $(config.python);
        task.arguments = $(config.argv);
        task.standardOutput = log;
        task.standardError = log;
        task.launch;
        task.waitUntilExit;
        var status = Number(task.terminationStatus);
        log.closeFile;
        atomicResult(config.helperResultFile, {ok: status === 0, code: 'helper_exit',
            exitCode: status, mode: config.mode, probeToken: config.probeToken || null,
            at: new Date().toISOString(), message: status === 0 ? '' : 'Sync subprocess exited with status ' + status});
    } catch (error) {
        if (config && typeof config.helperResultFile === 'string') {
            atomicResult(config.helperResultFile, {ok: false, code: 'helper_error',
                mode: config.mode, probeToken: config.probeToken || null,
                at: new Date().toISOString(), message: String(error)});
        } else {
            throw error;
        }
    }
}
