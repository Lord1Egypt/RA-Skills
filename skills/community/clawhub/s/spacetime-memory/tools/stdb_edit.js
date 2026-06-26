"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// @ts-nocheck
const sdk_1 = require("../sdk");
const argsStr = process.argv[2] || "{}";
const args = JSON.parse(argsStr);

const URL = process.env.SPACETIMEDB_URL || "http://127.0.0.1:3001";
const DB_NAME = process.env.SPACETIMEDB_NAME || "stdb-memory-1vgys";

async function main() {
    let db;
    await new Promise((resolve, reject) => {
        const builder = sdk_1.DbConnection.builder()
            .withUri(URL)
            .withDatabaseName(DB_NAME)
            .onConnect((connection, identity, token) => {
                resolve();
            })
            .onConnectError((ctx, err) => {
                reject(err);
            });
        db = builder.build();
    });

    const memoryId = args.id;
    const content = args.content;
    const tags = args.tags;

    if (!memoryId || !content || !tags) {
        throw new Error("Missing id, content, or tags");
    }

    db.reducers.updateMemory({ id: memoryId, content, tags });

    // Wait for the server to process the reducer
    await new Promise(resolve => setTimeout(resolve, 500));

    console.log(JSON.stringify({
        status: "success",
        id: memoryId,
        message: "Memory updated successfully"
    }));

    db.disconnect();
    process.exit(0);
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
