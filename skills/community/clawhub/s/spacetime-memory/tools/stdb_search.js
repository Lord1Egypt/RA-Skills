"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// @ts-nocheck
const sdk_1 = require("../sdk");
const argsStr = process.argv[2] || "{}";
const args = JSON.parse(argsStr);
const queryStr = args.query?.toLowerCase() || "";
const URL = process.env.SPACETIMEDB_URL || "http://127.0.0.1:3001";
const DB_NAME = process.env.SPACETIMEDB_NAME || "stdb-memory-1vgys";
async function main() {
    let db;
    await new Promise((resolve, reject) => {
        db = sdk_1.DbConnection.builder()
            .withUri(URL)
            .withDatabaseName(DB_NAME)
            .onConnect((connection) => {
            connection.subscriptionBuilder()
                .onApplied(() => {
                resolve();
            })
                .subscribe(['SELECT * FROM memory']);
        })
            .onConnectError((ctx, err) => reject(err))
            .build();
    });
    const allMemories = Array.from(db.db.memory.iter());
    const results = allMemories.filter((m) => m.content.toLowerCase().includes(queryStr) ||
        m.tags.some((t) => t.toLowerCase().includes(queryStr)));
    console.log(JSON.stringify({
        status: "success",
        count: results.length,
        results: results.map((r) => ({
            id: r.id,
            content: r.content,
            tags: r.tags,
            timestamp: r.timestamp.toString()
        }))
    }, null, 2));
    db.disconnect();
    process.exit(0);
}
main().catch(err => {
    console.error(err);
    process.exit(1);
});
//# sourceMappingURL=stdb_search.js.map