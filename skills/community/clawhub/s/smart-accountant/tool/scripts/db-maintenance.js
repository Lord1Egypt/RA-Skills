const db = require('../lib/db');

function main() {
    console.log("Running Database Maintenance...");
    
    db.exec("VACUUM");
    console.log("VACUUM completed.");
    
    db.exec("ANALYZE");
    console.log("ANALYZE completed.");
    
    const wal = db.prepare("PRAGMA wal_checkpoint(FULL)").get();
    console.log("WAL Checkpoint:", wal);
}

if (require.main === module) {
    main();
}
