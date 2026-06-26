#!/usr/bin/env node
import { call } from "./lib/api.js";

const [,, cmd, ...args] = process.argv;

const kv = Object.fromEntries(args.map(a => a.split("=")));

const FORBIDDEN_PATHS = [
  "/api/notebook/createNotebook",
  "/api/notebook/removeNotebook",
  "/api/notebook/renameNotebook",
  "/api/notebook/closeNotebook",
  "/api/notebook/saveNotebookConf"
];

function isWritePath(path) {
  return !(
    path.startsWith("/api/system") ||
    path.startsWith("/api/search") ||
    path.startsWith("/api/ref") ||
    path.startsWith("/api/outline") ||
    path.startsWith("/api/history") ||
    path.startsWith("/api/render") ||
    path.startsWith("/api/filetree/getDoc") ||
    path.startsWith("/api/filetree/listDocs") ||
    path.startsWith("/api/block/getBlockInfo") ||
    path.startsWith("/api/block/getChildBlocks") ||
    path.startsWith("/api/notebook/listNotebooks") ||
    path.startsWith("/api/notebook/lsNotebooks") ||
    path.startsWith("/api/notebook/getOpenedNotebooks") ||
    path.startsWith("/api/query/sql")
  );
}

async function main() {
  switch (cmd) {
    case "search":
    case "searchByNotebook": {
      if (!kv.query) throw new Error("search requires query=<keyword>");
      const limit = Number(kv.limit || 20);
      const notebook = kv.notebook;
      let sql = `SELECT id, type, content, created, updated FROM blocks WHERE content LIKE '%${kv.query.replace(/'/g, "''")}%'`;
      if (notebook) {
        sql += ` AND box = '${notebook}'`;
      }
      sql += ` ORDER BY updated DESC LIMIT ${limit}`;
      return call("/api/query/sql", { stmt: sql });
    }

    case "getDoc":
      return call("/api/filetree/getDoc", { id: kv.id });

    case "getBlock":
      return call("/api/block/getBlockInfo", { id: kv.id });

    case "getChildren":
      return call("/api/block/getChildBlocks", { id: kv.id });

    case "backlinks":
      return call("/api/ref/getBacklink2", { id: kv.id });

    case "outline":
      return call("/api/outline/getDocOutline", { id: kv.id });

    case "sql":
      if (!/^\s*SELECT\b/i.test(kv.stmt)) {
        throw new Error("sql command only allows SELECT statements");
      }
      return call("/api/query/sql", { stmt: kv.stmt });

    case "exportMd":
      return call("/api/export/exportMd", { id: kv.id });

    case "insertBlock":
      if (kv.write !== "true") {
        throw new Error("insertBlock requires write=true");
      }
      return call("/api/block/insertBlock", {
        parentID: kv.parentID,
        data: kv.data,
        position: kv.position || "after"
      });

    case "deleteBlock":
      if (kv.write !== "true") {
        throw new Error("deleteBlock requires write=true");
      }
      return call("/api/block/deleteBlock", { id: kv.id });

    case "updateBlock":
      if (kv.write !== "true") {
        throw new Error("updateBlock requires write=true");
      }
      return call("/api/block/updateBlock", { id: kv.id, data: kv.data });

    case "call": {
      const path = kv.path;
      if (!path) throw new Error("call requires path=/api/...");

      if (FORBIDDEN_PATHS.includes(path)) {
        throw new Error(`Forbidden API path: ${path}`);
      }

      const body = { ...kv };
      delete body.path;

      if (isWritePath(path) && body.write !== "true") {
        throw new Error(`Write operation blocked for ${path} (set write=true)`);
      }

      delete body.write;
      return call(path, body);
    }

    default:
      throw new Error(`Unknown command: ${cmd}`);
  }
}

main()
  .then(res => {
    console.log(JSON.stringify(res, null, 2));
  })
  .catch(err => {
    console.error(err.message);
    process.exit(1);
  });
