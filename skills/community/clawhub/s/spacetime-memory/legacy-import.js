const fs = require('fs');
const path = require('path');
const sdk_1 = require('./sdk');

const args = process.argv.slice(2);
const confirm = args.includes('--confirm');
const workspace = args.find(a => !a.startsWith('--'));

if (!confirm || !workspace) {
    console.error("CRITICAL ERROR: This is a destructive operation that will overwrite files. You must explicitly pass the '--confirm' flag and the target workspace path to proceed.");
    process.exit(1);
}

const filesToImport = [
    'MEMORY.md', 'IDENTITY.md', 'USER.md', 'SOUL.md', 'HEARTBEAT.md', 'AGENTS.md', 'TOOLS.md'
];

const URL = process.env.SPACETIMEDB_URL || 'http://127.0.0.1:3001';
const DB_NAME = process.env.SPACETIMEDB_NAME || 'stdb-memory-1vgys';

async function main() {
    console.log(`Starting legacy import for workspace: ${workspace}`);

    let db;
    await new Promise((resolve, reject) => {
        const builder = sdk_1.DbConnection.builder()
            .withUri(URL)
            .withDatabaseName(DB_NAME)
            .onConnect(() => resolve())
            .onConnectError((ctx, err) => reject(err));
        db = builder.build();
    });

    for (const file of filesToImport) {
        const fullPath = path.join(workspace, file);
        if (fs.existsSync(fullPath)) {
            const content = fs.readFileSync(fullPath, 'utf8');
            if (content.includes("migrated to SpacetimeDB")) {
                console.log(`Skipping ${file} - already migrated`);
                continue;
            }
            console.log(`Importing ${file}...`);
            
            // Create a backup before overwriting
            const backupPath = `${fullPath}.bak`;
            fs.copyFileSync(fullPath, backupPath);
            console.log(`Created backup at ${backupPath}`);

            const id = Date.now().toString() + Math.floor(Math.random() * 1000).toString();
            const timestamp = BigInt(Date.now()) * 1000n;
            const tags = ['legacy', 'import', file.replace('.md', '').toLowerCase()];
            
            try {
                // Store natively 
                db.reducers.storeMemory({ id, content: content.trim(), timestamp, tags });
                
                // Wait for processing
                await new Promise(r => setTimeout(r, 200));
                
                console.log(`Imported ${file}`);
                
                // Overwrite the file
                fs.writeFileSync(fullPath, `# ${file}\nContent migrated to SpacetimeDB. Use stdb_search.\n`);
            } catch (err) {
                console.error(`Failed to import ${file}: ${err.message}`);
            }
        }
    }
    console.log("Legacy import completed.");
    db.disconnect();
    process.exit(0);
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
