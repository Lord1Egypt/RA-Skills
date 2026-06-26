// @ts-nocheck
import { DbConnection, tables } from '../sdk';

const argsStr = process.argv[2] || "{}";
const args = JSON.parse(argsStr);
const queryStr = args.query?.toLowerCase() || "";

const URL = 'http://127.0.0.1:3001';
const DB_NAME = 'stdb-memory-1vgys';

async function main() {
  let db: any;
  await new Promise<void>((resolve, reject) => {
    db = DbConnection.builder()
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

  const results = allMemories.filter((m: any) => 
    m.content.toLowerCase().includes(queryStr) || 
    m.tags.some((t: string) => t.toLowerCase().includes(queryStr))
  );

  console.log(JSON.stringify({
    status: "success",
    count: results.length,
    results: results.map((r: any) => ({
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