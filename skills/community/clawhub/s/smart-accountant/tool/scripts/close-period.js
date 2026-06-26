const db = require('../lib/db');

function closePeriod() {
    console.log("Starting period close...");
    
    // Simple mock logic for setting config flag
    const stmt = db.prepare("INSERT OR REPLACE INTO config (key, value) VALUES ('period_status', 'CLOSED')");
    stmt.run();
    
    console.log("Period locked. Status set to CLOSED.");
}

if (require.main === module) {
    closePeriod();
}
