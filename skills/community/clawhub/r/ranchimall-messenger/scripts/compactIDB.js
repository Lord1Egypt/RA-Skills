(function (EXPORTS) { //compactIDB v2.1.2
    /* Compact IndexedDB operations */
    'use strict';
    const compactIDB = EXPORTS;

    var defaultDB;

    const indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB;
    const IDBTransaction = window.IDBTransaction || window.webkitIDBTransaction || window.msIDBTransaction;
    const IDBKeyRange = window.IDBKeyRange || window.webkitIDBKeyRange || window.msIDBKeyRange;

    if (!indexedDB) {
        console.error("Your browser doesn't support a stable version of IndexedDB.");
        return;
    }

    compactIDB.setDefaultDB = dbName => defaultDB = dbName;

    Object.defineProperty(compactIDB, 'default', {
        get: () => defaultDB,
        set: dbName => defaultDB = dbName
    });

    function getDBversion(dbName = defaultDB) {
        return new Promise((resolve, reject) => {
            openDB(dbName).then(db => {
                resolve(db.version)
                db.close()
            }).catch(error => reject(error))
        })
    }

    function upgradeDB(dbName, createList = null, deleteList = null) {
        return new Promise((resolve, reject) => {
            getDBversion(dbName).then(version => {
                var idb = indexedDB.open(dbName, version + 1);
                idb.onerror = (event) => reject("Error in opening IndexedDB");
                idb.onupgradeneeded = (event) => {
                    let db = event.target.result;
                    if (createList instanceof Object) {
                        if (Array.isArray(createList)) {
                            let tmp = {}
                            createList.forEach(o => tmp[o] = {})
                            createList = tmp
                        }
                        for (let o in createList) {
                            let obs = db.createObjectStore(o, createList[o].options || {});
                            if (createList[o].indexes instanceof Object)
                                for (let i in createList[o].indexes)
                                    obs.createIndex(i, i, createList[o].indexes || {});
                        }
                    }
                    if (Array.isArray(deleteList))
                        deleteList.forEach(o => db.deleteObjectStore(o));
                    resolve('Database upgraded')
                }
                idb.onsuccess = (event) => event.target.result.close();
            }).catch(error => reject(error))
        })
    }

    compactIDB.initDB = function (dbName, objectStores = {}) {
        return new Promise((resolve, reject) => {
            if (!(objectStores instanceof Object))
                return reject('ObjectStores must be an object or array')
            defaultDB = defaultDB || dbName;
            var idb = indexedDB.open(dbName);
            idb.onerror = (event) => reject("Error in opening IndexedDB");
            idb.onsuccess = (event) => {
                var db = event.target.result;
                let cList = Object.values(db.objectStoreNames);
                var obs = {},
                    a_obs = {},
                    d_obs = [];
                if (!Array.isArray(objectStores))
                    var obs = objectStores
                else
                    objectStores.forEach(o => obs[o] = {})
                let nList = Object.keys(obs)
                for (let o of nList)
                    if (!cList.includes(o))
                        a_obs[o] = obs[o]
                for (let o of cList)
                    if (!nList.includes(o))
                        d_obs.push(o)
                if (!Object.keys(a_obs).length && !d_obs.length)
                    resolve("Initiated IndexedDB");
                else
                    upgradeDB(dbName, a_obs, d_obs)
                        .then(result => resolve(result))
                        .catch(error => reject(error))
                db.close();
            }
        });
    }

    const openDB = compactIDB.openDB = function (dbName = defaultDB) {
        return new Promise((resolve, reject) => {
            var idb = indexedDB.open(dbName);
            idb.onerror = (event) => reject("Error in opening IndexedDB");
            idb.onupgradeneeded = (event) => {
                event.target.result.close();
                deleteDB(dbName).then(_ => null).catch(_ => null).finally(_ => reject("Datebase not found"))
            }
            idb.onsuccess = (event) => resolve(event.target.result);
        });
    }

    const deleteDB = compactIDB.deleteDB = function (dbName = defaultDB) {
        return new Promise((resolve, reject) => {
            var deleteReq = indexedDB.deleteDatabase(dbName);;
            deleteReq.onerror = (event) => reject("Error deleting database!");
            deleteReq.onsuccess = (event) => resolve("Database deleted successfully");
        });
    }

    compactIDB.writeData = function (obsName, data, key = false, dbName = defaultDB) {
        return new Promise((resolve, reject) => {
            openDB(dbName).then(db => {
                var obs = db.transaction(obsName, "readwrite").objectStore(obsName);
                let writeReq = (key ? obs.put(data, key) : obs.put(data));
                writeReq.onsuccess = (evt) => resolve(`Write data Successful`);
                writeReq.onerror = (evt) => reject(
                    `Write data unsuccessful [${evt.target.error.name}] ${evt.target.error.message}`
                );
                db.close();
            }).catch(error => reject(error));
        });
    }

    compactIDB.addData = function (obsName, data, key = false, dbName = defaultDB) {
        return new Promise((resolve, reject) => {
            openDB(dbName).then(db => {
                var obs = db.transaction(obsName, "readwrite").objectStore(obsName);
                let addReq = (key ? obs.add(data, key) : obs.add(data));
                addReq.onsuccess = (evt) => resolve(`Add data successful`);
                addReq.onerror = (evt) => reject(
                    `Add data unsuccessful [${evt.target.error.name}] ${evt.target.error.message}`
                );
                db.close();
            }).catch(error => reject(error));
        });
    }

    compactIDB.removeData = function (obsName, key, dbName = defaultDB) {
        return new Promise((resolve, reject) => {
            openDB(dbName).then(db => {
                var obs = db.transaction(obsName, "readwrite").objectStore(obsName);
                let delReq = obs.delete(key);
                delReq.onsuccess = (evt) => resolve(`Removed Data ${key}`);
                delReq.onerror = (evt) => reject(
                    `Remove data unsuccessful [${evt.target.error.name}] ${evt.target.error.message}`
                );
                db.close();
            }).catch(error => reject(error));
        });
    }

    compactIDB.clearData = function (obsName, dbName = defaultDB) {
        return new Promise((resolve, reject) => {
            openDB(dbName).then(db => {
                var obs = db.transaction(obsName, "readwrite").objectStore(obsName);
                let clearReq = obs.clear();
                clearReq.onsuccess = (evt) => resolve(`Clear data Successful`);
                clearReq.onerror = (evt) => reject(`Clear data Unsuccessful`);
                db.close();
            }).catch(error => reject(error));
        });
    }

    compactIDB.readData = function (obsName, key, dbName = defaultDB) {
        return new Promise((resolve, reject) => {
            openDB(dbName).then(db => {
                var obs = db.transaction(obsName, "readonly").objectStore(obsName);
                let getReq = obs.get(key);
                getReq.onsuccess = (evt) => resolve(evt.target.result);
                getReq.onerror = (evt) => reject(
                    `Read data unsuccessful [${evt.target.error.name}] ${evt.target.error.message}`
                );
                db.close();
            }).catch(error => reject(error));
        });
    }

    compactIDB.readAllData = function (obsName, dbName = defaultDB) {
        return new Promise((resolve, reject) => {
            openDB(dbName).then(db => {
                var obs = db.transaction(obsName, "readonly").objectStore(obsName);
                var tmpResult = {}
                let curReq = obs.openCursor();
                curReq.onsuccess = (evt) => {
                    var cursor = evt.target.result;
                    if (cursor) {
                        tmpResult[cursor.primaryKey] = cursor.value;
                        cursor.continue();
                    } else
                        resolve(tmpResult);
                }
                curReq.onerror = (evt) => reject(
                    `Read-All data unsuccessful [${evt.target.error.name}] ${evt.target.error.message}`
                );
                db.close();
            }).catch(error => reject(error));
        });
    }

    /* compactIDB.searchData = function (obsName, options = {}, dbName = defaultDB) {
        
        return new Promise((resolve, reject) => {
            openDB(dbName).then(db => {
                var obs = db.transaction(obsName, "readonly").objectStore(obsName);
                var filteredResult = {}
                let keyRange;
                if(options.lowerKey!==null && options.upperKey!==null)
                    keyRange = IDBKeyRange.bound(options.lowerKey, options.upperKey);
                else if(options.lowerKey!==null)
                    keyRange = IDBKeyRange.lowerBound(options.lowerKey);
                else if (options.upperKey!==null)
                    keyRange = IDBKeyRange.upperBound(options.upperBound);
                else if (options.atKey)
                let curReq = obs.openCursor(keyRange, )
            }).catch(error => reject(error))
        })
    }*/

    compactIDB.searchData = function (obsName, options = {}, dbName = defaultDB) {
        options.lowerKey = options.atKey || options.lowerKey || 0
        options.upperKey = options.atKey || options.upperKey || false
        options.patternEval = options.patternEval || ((k, v) => true);
        options.limit = options.limit || false;
        options.reverse = options.reverse || false;
        options.lastOnly = options.lastOnly || false
        return new Promise((resolve, reject) => {
            openDB(dbName).then(db => {
                var obs = db.transaction(obsName, "readonly").objectStore(obsName);
                var filteredResult = {}
                let curReq = obs.openCursor(
                    options.upperKey ? IDBKeyRange.bound(options.lowerKey, options.upperKey) : IDBKeyRange.lowerBound(options.lowerKey),
                    options.lastOnly || options.reverse ? "prev" : "next");
                curReq.onsuccess = (evt) => {
                    var cursor = evt.target.result;
                    if (!cursor || (options.limit && options.limit <= Object.keys(filteredResult).length))
                        return resolve(filteredResult); //reached end of key list or limit reached
                    else if (options.patternEval(cursor.primaryKey, cursor.value)) {
                        filteredResult[cursor.primaryKey] = cursor.value;
                        options.lastOnly ? resolve(filteredResult) : cursor.continue();
                    } else
                        cursor.continue();
                }
                curReq.onerror = (evt) => reject(`Search unsuccessful [${evt.target.error.name}] ${evt.target.error.message}`);
                db.close();
            }).catch(error => reject(error));
        });
    }


})(window.compactIDB = {});