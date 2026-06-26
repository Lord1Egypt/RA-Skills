(function (EXPORTS) { //floCloudAPI v2.4.5
    /* FLO Cloud operations to send/request application data*/
    'use strict';
    const floCloudAPI = EXPORTS;

    const DEFAULT = {
        blockchainPrefix: 0x23, //Prefix version for FLO blockchain
        SNStorageID: floGlobals.SNStorageID || "FNaN9McoBAEFUjkRmNQRYLmBF8SpS7Tgfk",
        adminID: floGlobals.adminID,
        application: floGlobals.application,
        SNStorageName: "SuperNodeStorage",
        callback: (d, e) => console.debug(d, e)
    };

    var user_id, user_public, user_private, aes_key;

    function user(id, priv) {
        if (!priv || !id)
            return user.clear();
        let pub = floCrypto.getPubKeyHex(priv);
        if (!pub || !floCrypto.verifyPubKey(pub, id))
            return user.clear();
        let n = floCrypto.randInt(12, 20);
        aes_key = floCrypto.randString(n);
        user_private = Crypto.AES.encrypt(priv, aes_key);
        user_public = pub;
        user_id = id;
        return user_id;
    }

    Object.defineProperties(user, {
        id: {
            get: () => {
                if (!user_id)
                    throw "User not set";
                return user_id;
            }
        },
        public: {
            get: () => {
                if (!user_public)
                    throw "User not set";
                return user_public;
            }
        },
        sign: {
            value: msg => {
                if (!user_private)
                    throw "User not set";
                return floCrypto.signData(msg, Crypto.AES.decrypt(user_private, aes_key));
            }
        },
        clear: {
            value: () => user_id = user_public = user_private = aes_key = undefined
        }
    })

    Object.defineProperties(floCloudAPI, {
        SNStorageID: {
            get: () => DEFAULT.SNStorageID
        },
        SNStorageName: {
            get: () => DEFAULT.SNStorageName
        },
        adminID: {
            get: () => DEFAULT.adminID
        },
        application: {
            get: () => DEFAULT.application
        },
        user: {
            get: () => user
        }
    });

    var appObjects, generalData, lastVC;
    Object.defineProperties(floGlobals, {
        appObjects: {
            get: () => appObjects,
            set: obj => appObjects = obj
        },
        generalData: {
            get: () => generalData,
            set: data => generalData = data
        },
        generalDataset: {
            value: (type, options = {}) => generalData[filterKey(type, options)]
        },
        lastVC: {
            get: () => lastVC,
            set: vc => lastVC = vc
        }
    });

    var supernodes = {}; //each supnernode must be stored as floID : {uri:<uri>,pubKey:<publicKey>}
    Object.defineProperty(floCloudAPI, 'nodes', {
        get: () => JSON.parse(JSON.stringify(supernodes))
    });

    var kBucket;
    const K_Bucket = floCloudAPI.K_Bucket = function (masterID, nodeList) {

        const decodeID = floID => {
            let k = bitjs.Base58.decode(floID);
            k.shift();
            k.splice(-4, 4);
            let decodedId = Crypto.util.bytesToHex(k);
            let nodeIdBigInt = new BigInteger(decodedId, 16);
            let nodeIdBytes = nodeIdBigInt.toByteArrayUnsigned();
            let nodeIdNewInt8Array = new Uint8Array(nodeIdBytes);
            return nodeIdNewInt8Array;
        };

        const _KB = new BuildKBucket({
            localNodeId: decodeID(masterID)
        });
        nodeList.forEach(id => _KB.add({
            id: decodeID(id),
            floID: id
        }));

        const _CO = nodeList.map(id => [_KB.distance(_KB.localNodeId, decodeID(id)), id])
            .sort((a, b) => a[0] - b[0])
            .map(a => a[1]);

        const self = this;
        Object.defineProperty(self, 'tree', {
            get: () => _KB
        });
        Object.defineProperty(self, 'list', {
            get: () => Array.from(_CO)
        });

        self.isNode = floID => _CO.includes(floID);
        self.innerNodes = function (id1, id2) {
            if (!_CO.includes(id1) || !_CO.includes(id2))
                throw Error('Given nodes are not supernode');
            let iNodes = []
            for (let i = _CO.indexOf(id1) + 1; _CO[i] != id2; i++) {
                if (i < _CO.length)
                    iNodes.push(_CO[i])
                else i = -1
            }
            return iNodes
        }
        self.outterNodes = function (id1, id2) {
            if (!_CO.includes(id1) || !_CO.includes(id2))
                throw Error('Given nodes are not supernode');
            let oNodes = []
            for (let i = _CO.indexOf(id2) + 1; _CO[i] != id1; i++) {
                if (i < _CO.length)
                    oNodes.push(_CO[i])
                else i = -1
            }
            return oNodes
        }
        self.prevNode = function (id, N = 1) {
            let n = N || _CO.length;
            if (!_CO.includes(id))
                throw Error('Given node is not supernode');
            let pNodes = []
            for (let i = 0, j = _CO.indexOf(id) - 1; i < n; j--) {
                if (j == _CO.indexOf(id))
                    break;
                else if (j > -1)
                    pNodes[i++] = _CO[j]
                else j = _CO.length
            }
            return (N == 1 ? pNodes[0] : pNodes)
        }
        self.nextNode = function (id, N = 1) {
            let n = N || _CO.length;
            if (!_CO.includes(id))
                throw Error('Given node is not supernode');
            if (!n) n = _CO.length;
            let nNodes = []
            for (let i = 0, j = _CO.indexOf(id) + 1; i < n; j++) {
                if (j == _CO.indexOf(id))
                    break;
                else if (j < _CO.length)
                    nNodes[i++] = _CO[j]
                else j = -1
            }
            return (N == 1 ? nNodes[0] : nNodes)
        }
        self.closestNode = function (id, N = 1) {
            let decodedId = decodeID(id);
            let n = N || _CO.length;
            let cNodes = _KB.closest(decodedId, n)
                .map(k => k.floID)
            return (N == 1 ? cNodes[0] : cNodes)
        }
    }

    floCloudAPI.init = function startCloudProcess(nodes) {
        return new Promise((resolve, reject) => {
            try {
                supernodes = nodes;
                kBucket = new K_Bucket(DEFAULT.SNStorageID, Object.keys(supernodes));
                resolve('Cloud init successful');
            } catch (error) {
                reject(error);
            }
        })
    }

    Object.defineProperty(floCloudAPI, 'kBucket', {
        get: () => kBucket
    });

    const _inactive = new Set();

    function ws_connect(snID) {
        return new Promise((resolve, reject) => {
            if (!(snID in supernodes))
                return reject(`${snID} is not a supernode`)
            if (_inactive.has(snID))
                return reject(`${snID} is not active`)
            var wsConn = new WebSocket("wss://" + supernodes[snID].uri + "/");
            wsConn.onopen = evt => resolve(wsConn);
            wsConn.onerror = evt => {
                _inactive.add(snID)
                reject(`${snID} is unavailable`)
            }
        })
    }

    function ws_activeConnect(snID, reverse = false) {
        return new Promise((resolve, reject) => {
            if (_inactive.size === kBucket.list.length)
                return reject('Cloud offline');
            if (!(snID in supernodes))
                snID = kBucket.closestNode(proxyID(snID));
            ws_connect(snID)
                .then(node => resolve(node))
                .catch(error => {
                    if (reverse)
                        var nxtNode = kBucket.prevNode(snID);
                    else
                        var nxtNode = kBucket.nextNode(snID);
                    ws_activeConnect(nxtNode, reverse)
                        .then(node => resolve(node))
                        .catch(error => reject(error))
                })
        })
    }

    function fetch_API(snID, data) {
        return new Promise((resolve, reject) => {
            if (_inactive.has(snID))
                return reject(`${snID} is not active`);
            let fetcher, sn_url = "https://" + supernodes[snID].uri;
            if (typeof data === "string")
                fetcher = fetch(sn_url + "?" + data);
            else if (typeof data === "object" && data.method === "POST")
                fetcher = fetch(sn_url, data);
            fetcher.then(response => {
                if (response.ok || response.status === 400 || response.status === 500)
                    resolve(response);
                else
                    reject(response);
            }).catch(error => reject(error))
        })
    }

    function fetch_ActiveAPI(snID, data, reverse = false) {
        return new Promise((resolve, reject) => {
            if (_inactive.size === kBucket.list.length)
                return reject('Cloud offline');
            if (!(snID in supernodes))
                snID = kBucket.closestNode(proxyID(snID));
            fetch_API(snID, data)
                .then(result => resolve(result))
                .catch(error => {
                    _inactive.add(snID)
                    if (reverse)
                        var nxtNode = kBucket.prevNode(snID);
                    else
                        var nxtNode = kBucket.nextNode(snID);
                    fetch_ActiveAPI(nxtNode, data, reverse)
                        .then(result => resolve(result))
                        .catch(error => reject(error));
                })
        })
    }

    function singleRequest(floID, data_obj, method = "POST") {
        return new Promise((resolve, reject) => {
            let data;
            if (method === "POST")
                data = {
                    method: "POST",
                    body: JSON.stringify(data_obj)
                };
            else
                data = new URLSearchParams(JSON.parse(JSON.stringify(data_obj))).toString();
            fetch_ActiveAPI(floID, data).then(response => {
                if (response.ok)
                    response.json()
                        .then(result => resolve(result))
                        .catch(error => reject(error))
                else response.text()
                    .then(result => reject(response.status + ": " + result)) //Error Message from Node
                    .catch(error => reject(error))
            }).catch(error => reject(error))
        })
    }

    const _liveRequest = {};

    function liveRequest(floID, request, callback) {
        const filterData = typeof request.status !== 'undefined' ?
            data => {
                if (request.status)
                    return data;
                else {
                    let filtered = {};
                    for (let i in data)
                        if (request.trackList.includes(i))
                            filtered[i] = data[i];
                    return filtered;
                }
            } :
            data => {
                data = objectifier(data);
                let filtered = {},
                    proxy = proxyID(request.receiverID),
                    r = request;
                for (let v in data) {
                    let d = data[v];
                    if ((!r.atVectorClock || r.atVectorClock == v) &&
                        (r.atVectorClock || !r.lowerVectorClock || r.lowerVectorClock <= v) &&
                        (r.atVectorClock || !r.upperVectorClock || r.upperVectorClock >= v) &&
                        (!r.afterTime || r.afterTime < d.log_time) &&
                        r.application == d.application &&
                        (proxy == d.receiverID || proxy == d.proxyID) &&
                        (!r.comment || r.comment == d.comment) &&
                        (!r.type || r.type == d.type) &&
                        (!r.senderID || r.senderID.includes(d.senderID)))
                        filtered[v] = data[v];
                }
                return filtered;
            };

        return new Promise((resolve, reject) => {
            ws_activeConnect(floID).then(node => {
                let randID = floCrypto.randString(5);
                node.send(JSON.stringify(request));
                node.onmessage = (evt) => {
                    let d = null,
                        e = null;
                    try {
                        d = filterData(JSON.parse(evt.data));
                    } catch (error) {
                        e = evt.data
                    } finally {
                        callback(d, e)
                    }
                }
                _liveRequest[randID] = node;
                _liveRequest[randID].request = request;
                resolve(randID);
            }).catch(error => reject(error));
        });
    }

    Object.defineProperty(floCloudAPI, 'liveRequest', {
        get: () => _liveRequest
    });

    Object.defineProperty(floCloudAPI, 'inactive', {
        get: () => _inactive
    });

    const util = floCloudAPI.util = {};

    const encodeMessage = util.encodeMessage = function (message) {
        return btoa(unescape(encodeURIComponent(JSON.stringify(message))))
    }

    const decodeMessage = util.decodeMessage = function (message) {
        return JSON.parse(decodeURIComponent(escape(atob(message))))
    }

    const filterKey = util.filterKey = function (type, options = {}) {
        return type + (options.comment ? ':' + options.comment : '') +
            '|' + (options.group || options.receiverID || DEFAULT.adminID) +
            '|' + (options.application || DEFAULT.application);
    }

    const proxyID = util.proxyID = function (address) {
        if (!address)
            return;
        var bytes;

        // XRP Address (Base58, starts with 'r', 25-35 chars) - must be checked before FLO/BTC legacy
        if (address.length >= 25 && address.length <= 35 && address.startsWith('r')) {
            try {
                // XRP address - hash the raw address for unique proxy ID
                let addrBytes = [];
                for (let i = 0; i < address.length; i++) {
                    addrBytes.push(address.charCodeAt(i));
                }
                bytes = ripemd160(Crypto.SHA256(addrBytes, { asBytes: true }));
            } catch (e) {
                bytes = undefined;
            }
        }
        // FLO/BTC legacy encoding (33-34 chars)
        else if (address.length == 33 || address.length == 34) {
            let decode = bitjs.Base58.decode(address);
            bytes = decode.slice(0, decode.length - 4);
            let checksum = decode.slice(decode.length - 4),
                hash = Crypto.SHA256(Crypto.SHA256(bytes, {
                    asBytes: true
                }), {
                    asBytes: true
                });
            hash[0] != checksum[0] || hash[1] != checksum[1] || hash[2] != checksum[2] || hash[3] != checksum[3] ?
                bytes = undefined : bytes.shift();
        }
        // BTC/LTC Bech32 encoding (bc1 or ltc1 prefix)
        else if (/^(bc1|ltc1)[a-zA-HJ-NP-Z0-9]{25,62}$/.test(address)) {
            if (typeof coinjs !== 'function')
                throw "library missing (lib_btc.js)";
            let decode = coinjs.bech32_decode(address);
            if (decode) {
                bytes = decode.data;
                bytes.shift();
                bytes = coinjs.bech32_convert(bytes, 5, 8, false);
                if (address.length == 62) //for long bech, aggregate once more to get 160 bit 
                    bytes = coinjs.bech32_convert(bytes, 5, 8, false);
            }
        }
        // Public key hex (66 chars starting with 02, 03, or 04)
        else if (address.length == 66 && /^0[234][a-fA-F0-9]{64}$/.test(address)) {
            bytes = ripemd160(Crypto.SHA256(Crypto.util.hexToBytes(address), {
                asBytes: true
            }));
        }
        // Ethereum/EVM Address (40 or 42 chars with 0x prefix)
        else if ((address.length == 42 && address.startsWith("0x")) || (address.length == 40 && /^[a-fA-F0-9]{40}$/.test(address))) {
            if (address.startsWith("0x")) { address = address.substring(2); }
            bytes = Crypto.util.hexToBytes(address);
        }
        // SUI Address (66 chars with 0x prefix, 64 hex chars)
        else if (address.length == 66 && address.startsWith("0x") && /^0x[a-fA-F0-9]{64}$/.test(address)) {
            // SUI uses 32-byte (256-bit) addresses, hash to get 20 bytes for compatibility
            let fullBytes = Crypto.util.hexToBytes(address.substring(2));
            bytes = ripemd160(Crypto.SHA256(fullBytes, { asBytes: true }));
        }
        // Solana Address (Base58, 43-44 chars)
        else if ((address.length == 43 || address.length == 44) && /^[1-9A-HJ-NP-Za-km-z]+$/.test(address)) {
            try {
                // Solana address - hash the raw address for unique proxy ID
                let addrBytes = [];
                for (let i = 0; i < address.length; i++) {
                    addrBytes.push(address.charCodeAt(i));
                }
                bytes = ripemd160(Crypto.SHA256(addrBytes, { asBytes: true }));
            } catch (e) {
                bytes = undefined;
            }
        }
        // XRP Address (Base58, starts with 'r', 25-35 chars)
        else if (address.length >= 25 && address.length <= 35 && address.startsWith('r')) {
            try {
                // XRP address - hash the raw address for unique proxy ID
                let addrBytes = [];
                for (let i = 0; i < address.length; i++) {
                    addrBytes.push(address.charCodeAt(i));
                }
                bytes = ripemd160(Crypto.SHA256(addrBytes, { asBytes: true }));
            } catch (e) {
                bytes = undefined;
            }
        }
        // TRON Address (Base58, starts with 'T', 34 chars)
        else if (address.length == 34 && address.startsWith('T')) {
            try {
                // TRON address - hash the raw address for unique proxy ID
                let addrBytes = [];
                for (let i = 0; i < address.length; i++) {
                    addrBytes.push(address.charCodeAt(i));
                }
                bytes = ripemd160(Crypto.SHA256(addrBytes, { asBytes: true }));
            } catch (e) {
                bytes = undefined;
            }
        }
        // Cardano Address (Bech32, starts with 'addr1', typically 98-103 chars)
        else if (address.startsWith('addr1') && address.length > 50) {
            try {
                // Cardano bech32 address - hash the raw address for unique proxy ID
                let addrBytes = [];
                for (let i = 0; i < address.length; i++) {
                    addrBytes.push(address.charCodeAt(i));
                }
                bytes = ripemd160(Crypto.SHA256(addrBytes, { asBytes: true }));
            } catch (e) {
                bytes = undefined;
            }
        }
        // Polkadot Address (SS58, starts with '1', 47-48 chars)
        else if ((address.length == 47 || address.length == 48) && /^1[a-zA-Z0-9]+$/.test(address)) {
            try {
                // Polkadot address - hash the raw address for unique proxy ID
                let addrBytes = [];
                for (let i = 0; i < address.length; i++) {
                    addrBytes.push(address.charCodeAt(i));
                }
                bytes = ripemd160(Crypto.SHA256(addrBytes, { asBytes: true }));
            } catch (e) {
                bytes = undefined;
            }
        }
        // TON Address (Base64, 48 chars)
        else if (address.length == 48 && /^[A-Za-z0-9_-]+$/.test(address)) {
            try {
                // TON address - hash the raw address for unique proxy ID
                let addrBytes = [];
                for (let i = 0; i < address.length; i++) {
                    addrBytes.push(address.charCodeAt(i));
                }
                bytes = ripemd160(Crypto.SHA256(addrBytes, { asBytes: true }));
            } catch (e) {
                bytes = undefined;
            }
        }
        // Algorand Address (Base32, 58 chars)
        else if (address.length == 58 && /^[A-Z2-7]+$/.test(address)) {
            try {
                // Algorand address - hash the raw address for unique proxy ID
                let addrBytes = [];
                for (let i = 0; i < address.length; i++) {
                    addrBytes.push(address.charCodeAt(i));
                }
                bytes = ripemd160(Crypto.SHA256(addrBytes, { asBytes: true }));
            } catch (e) {
                bytes = undefined;
            }
        }
        // Stellar Address (Base32, starts with 'G', 56 chars)
        else if (address.length == 56 && address.startsWith('G')) {
            try {
                // Stellar address - hash the raw address for unique proxy ID
                let addrBytes = [];
                for (let i = 0; i < address.length; i++) {
                    addrBytes.push(address.charCodeAt(i));
                }
                bytes = ripemd160(Crypto.SHA256(addrBytes, { asBytes: true }));
            } catch (e) {
                bytes = undefined;
            }
        }
        // Bitcoin Cash CashAddr format (without prefix, 42 chars of data)
        else if (address.length >= 34 && address.length <= 45 && /^q[a-z0-9]+$/.test(address)) {
            try {
                // BCH address - hash the raw address for unique proxy ID
                let addrBytes = [];
                for (let i = 0; i < address.length; i++) {
                    addrBytes.push(address.charCodeAt(i));
                }
                bytes = ripemd160(Crypto.SHA256(addrBytes, { asBytes: true }));
            } catch (e) {
                bytes = undefined;
            }
        }
        // HBAR Address (account ID format: 0.0.xxxxx)
        else if (/^0\.0\.\d+$/.test(address)) {
            try {
                // HBAR address - hash the raw address for unique proxy ID
                let addrBytes = [];
                for (let i = 0; i < address.length; i++) {
                    addrBytes.push(address.charCodeAt(i));
                }
                bytes = ripemd160(Crypto.SHA256(addrBytes, { asBytes: true }));
            } catch (e) {
                bytes = undefined;
            }
        }

        if (!bytes)
            throw "Invalid address: " + address;
        else {
            bytes.unshift(DEFAULT.blockchainPrefix);
            let hash = Crypto.SHA256(Crypto.SHA256(bytes, {
                asBytes: true
            }), {
                asBytes: true
            });
            return bitjs.Base58.encode(bytes.concat(hash.slice(0, 4)));
        }
    }

    const lastCommit = {};
    Object.defineProperty(lastCommit, 'get', {
        value: objName => JSON.parse(lastCommit[objName])
    });
    Object.defineProperty(lastCommit, 'set', {
        value: objName => lastCommit[objName] = JSON.stringify(appObjects[objName])
    });

    function updateObject(objectName, dataSet) {
        try {
            console.log(dataSet)
            let vcList = Object.keys(dataSet).sort();
            for (let vc of vcList) {
                if (vc < lastVC[objectName] || dataSet[vc].type !== objectName)
                    continue;
                switch (dataSet[vc].comment) {
                    case "RESET":
                        if (dataSet[vc].message.reset)
                            appObjects[objectName] = dataSet[vc].message.reset;
                        break;
                    case "UPDATE":
                        if (dataSet[vc].message.diff)
                            appObjects[objectName] = diff.merge(appObjects[objectName], dataSet[vc].message.diff);
                }
                lastVC[objectName] = vc;
            }
            lastCommit.set(objectName);
            compactIDB.writeData("appObjects", appObjects[objectName], objectName);
            compactIDB.writeData("lastVC", lastVC[objectName], objectName);
        } catch (error) {
            console.error(error)
        }
    }

    function storeGeneral(fk, dataSet) {
        try {
            console.log(dataSet)
            if (typeof generalData[fk] !== "object")
                generalData[fk] = {}
            for (let vc in dataSet) {
                generalData[fk][vc] = dataSet[vc];
                if (dataSet[vc].log_time > lastVC[fk])
                    lastVC[fk] = dataSet[vc].log_time;
            }
            compactIDB.writeData("lastVC", lastVC[fk], fk)
            compactIDB.writeData("generalData", generalData[fk], fk)
        } catch (error) {
            console.error(error)
        }
    }

    function objectifier(data) {
        if (!Array.isArray(data))
            data = [data];
        return Object.fromEntries(data.map(d => {
            d.message = decodeMessage(d.message);
            return [d.vectorClock, d];
        }));
    }

    //set status as online for user_id
    floCloudAPI.setStatus = function (options = {}) {
        return new Promise((resolve, reject) => {
            let callback = options.callback instanceof Function ? options.callback : DEFAULT.callback;
            var request = {
                floID: user.id,
                application: options.application || DEFAULT.application,
                time: Date.now(),
                status: true,
                pubKey: user.public
            }
            let hashcontent = ["time", "application", "floID"].map(d => request[d]).join("|");
            request.sign = user.sign(hashcontent);
            liveRequest(options.refID || DEFAULT.adminID, request, callback)
                .then(result => resolve(result))
                .catch(error => reject(error))
        })
    }

    //request status of floID(s) in trackList
    floCloudAPI.requestStatus = function (trackList, options = {}) {
        return new Promise((resolve, reject) => {
            if (!Array.isArray(trackList))
                trackList = [trackList];
            let callback = options.callback instanceof Function ? options.callback : DEFAULT.callback;
            let request = {
                status: false,
                application: options.application || DEFAULT.application,
                trackList: trackList
            }
            liveRequest(options.refID || DEFAULT.adminID, request, callback)
                .then(result => resolve(result))
                .catch(error => reject(error))
        })
    }

    //send any message to supernode cloud storage
    const sendApplicationData = floCloudAPI.sendApplicationData = function (message, type, options = {}) {
        return new Promise((resolve, reject) => {
            let originalReceiverID = options.receiverID || DEFAULT.adminID;
            let serverReceiverID = originalReceiverID;
            try {
                if (!floCrypto.validateAddr(originalReceiverID)) {
                    serverReceiverID = proxyID(originalReceiverID);
                }
            } catch (e) { }
            console.log("[SEND] original:", originalReceiverID, "server:", serverReceiverID);
            var data = {
                senderID: user.id,
                receiverID: serverReceiverID,
                pubKey: user.public,
                message: encodeMessage(message),
                time: Date.now(),
                application: options.application || DEFAULT.application,
                type: type,
                comment: options.comment || ""
            }
            let hashcontent = ["receiverID", "time", "application", "type", "message", "comment"]
                .map(d => data[d]).join("|")
            data.sign = user.sign(hashcontent);
            singleRequest(originalReceiverID, data)
                .then(result => resolve(result))
                .catch(error => reject(error))
        })
    }

    //request any data from supernode cloud
    const requestApplicationData = floCloudAPI.requestApplicationData = function (type, options = {}) {
        return new Promise((resolve, reject) => {
            let originalReceiverID = options.receiverID || DEFAULT.adminID;
            let serverReceiverID = originalReceiverID;
            try {
                if (!floCrypto.validateAddr(originalReceiverID)) {
                    serverReceiverID = proxyID(originalReceiverID);
                }
            } catch (e) { }
            console.log("[RECV] original:", originalReceiverID, "server:", serverReceiverID);
            var request = {
                receiverID: serverReceiverID,
                senderID: options.senderID || undefined,
                application: options.application || DEFAULT.application,
                type: type,
                comment: options.comment || undefined,
                lowerVectorClock: options.lowerVectorClock || undefined,
                upperVectorClock: options.upperVectorClock || undefined,
                atVectorClock: options.atVectorClock || undefined,
                afterTime: options.afterTime || undefined,
                mostRecent: options.mostRecent || undefined,
            }

            if (options.callback instanceof Function) {
                liveRequest(originalReceiverID, request, options.callback)
                    .then(result => resolve(result))
                    .catch(error => reject(error))
            } else {
                if (options.method === "POST")
                    request = {
                        time: Date.now(),
                        request
                    };
                singleRequest(originalReceiverID, request, options.method || "GET")
                    .then(data => resolve(data)).catch(error => reject(error))
            }
        })
    }

    /*(NEEDS UPDATE)
    //delete data from supernode cloud (received only)
    floCloudAPI.deleteApplicationData = function(vectorClocks, options = {}) {
        return new Promise((resolve, reject) => {
            var delreq = {
                requestorID: user.id,
                pubKey: user.public,
                time: Date.now(),
                delete: (Array.isArray(vectorClocks) ? vectorClocks : [vectorClocks]),
                application: options.application || DEFAULT.application
            }
            let hashcontent = ["time", "application", "delete"]
                .map(d => delreq[d]).join("|")
            delreq.sign = user.sign(hashcontent)
            singleRequest(delreq.requestorID, delreq).then(result => {
                let success = [],
                    failed = [];
                result.forEach(r => r.status === 'fulfilled' ?
                    success.push(r.value) : failed.push(r.reason));
                resolve({
                    success,
                    failed
                })
            }).catch(error => reject(error))
        })
    }
    */
    //edit comment of data in supernode cloud (sender only)
    floCloudAPI.editApplicationData = function (vectorClock, comment_edit, options = {}) {
        return new Promise((resolve, reject) => {
            //request the data from cloud for resigning
            let req_options = Object.assign({}, options);
            req_options.atVectorClock = vectorClock;
            requestApplicationData(undefined, req_options).then(result => {
                if (!result.length)
                    return reject("Data not found");
                let data = result[0];
                if (data.senderID !== user.id)
                    return reject("Only sender can edit comment");
                data.comment = comment_edit;
                let hashcontent = ["receiverID", "time", "application", "type", "message", "comment"]
                    .map(d => data[d]).join("|");
                let re_sign = user.sign(hashcontent);
                var request = {
                    receiverID: options.receiverID || DEFAULT.adminID,
                    requestorID: user.id,
                    pubKey: user.public,
                    time: Date.now(),
                    vectorClock: vectorClock,
                    edit: comment_edit,
                    re_sign: re_sign
                }
                let request_hash = ["time", "vectorClock", "edit", "re_sign"].map(d => request[d]).join("|");
                request.sign = user.sign(request_hash);
                singleRequest(request.receiverID, request)
                    .then(result => resolve(result))
                    .catch(error => reject(error))
            }).catch(error => reject(error))
        })
    }

    //tag data in supernode cloud (subAdmin access only)
    floCloudAPI.tagApplicationData = function (vectorClock, tag, options = {}) {
        return new Promise((resolve, reject) => {
            if (!floGlobals.subAdmins.includes(user.id))
                return reject("Only subAdmins can tag data")
            var request = {
                receiverID: options.receiverID || DEFAULT.adminID,
                requestorID: user.id,
                pubKey: user.public,
                time: Date.now(),
                vectorClock: vectorClock,
                tag: tag,
            }
            let hashcontent = ["time", "vectorClock", 'tag'].map(d => request[d]).join("|");
            request.sign = user.sign(hashcontent);
            singleRequest(request.receiverID, request)
                .then(result => resolve(result))
                .catch(error => reject(error))
        })
    }

    //note data in supernode cloud (receiver only or subAdmin allowed if receiver is adminID)
    floCloudAPI.noteApplicationData = function (vectorClock, note, options = {}) {
        return new Promise((resolve, reject) => {
            var request = {
                receiverID: options.receiverID || DEFAULT.adminID,
                requestorID: user.id,
                pubKey: user.public,
                time: Date.now(),
                vectorClock: vectorClock,
                note: note,
            }
            let hashcontent = ["time", "vectorClock", 'note'].map(d => request[d]).join("|");
            request.sign = user.sign(hashcontent);
            singleRequest(request.receiverID, request)
                .then(result => resolve(result))
                .catch(error => reject(error))
        })
    }

    //send general data
    floCloudAPI.sendGeneralData = function (message, type, options = {}) {
        return new Promise((resolve, reject) => {
            if (options.encrypt) {
                let encryptionKey = options.encrypt === true ?
                    floGlobals.settings.encryptionKey : options.encrypt
                message = floCrypto.encryptData(JSON.stringify(message), encryptionKey)
            }
            sendApplicationData(message, type, options)
                .then(result => resolve(result))
                .catch(error => reject(error))
        })
    }

    //request general data
    floCloudAPI.requestGeneralData = function (type, options = {}) {
        return new Promise((resolve, reject) => {
            var fk = filterKey(type, options)
            lastVC[fk] = parseInt(lastVC[fk]) || 0;
            options.afterTime = options.afterTime || lastVC[fk];
            if (options.callback instanceof Function) {
                let new_options = Object.create(options)
                new_options.callback = (d, e) => {
                    storeGeneral(fk, d);
                    options.callback(d, e)
                }
                requestApplicationData(type, new_options)
                    .then(result => resolve(result))
                    .catch(error => reject(error))
            } else {
                requestApplicationData(type, options).then(dataSet => {
                    storeGeneral(fk, objectifier(dataSet))
                    resolve(dataSet)
                }).catch(error => reject(error))
            }
        })
    }

    //request an object data from supernode cloud
    floCloudAPI.requestObjectData = function (objectName, options = {}) {
        return new Promise((resolve, reject) => {
            options.lowerVectorClock = options.lowerVectorClock || lastVC[objectName] + 1;
            options.senderID = [false, null].includes(options.senderID) ? null :
                options.senderID || floGlobals.subAdmins;
            options.mostRecent = true;
            options.comment = 'RESET';
            let callback = null;
            if (options.callback instanceof Function) {
                let old_callback = options.callback;
                callback = (d, e) => {
                    updateObject(objectName, d);
                    old_callback(d, e);
                }
                delete options.callback;
            }
            requestApplicationData(objectName, options).then(dataSet => {
                updateObject(objectName, objectifier(dataSet));
                delete options.comment;
                options.lowerVectorClock = lastVC[objectName] + 1;
                delete options.mostRecent;
                if (callback) {
                    let new_options = Object.create(options);
                    new_options.callback = callback;
                    requestApplicationData(objectName, new_options)
                        .then(result => resolve(result))
                        .catch(error => reject(error))
                } else {
                    requestApplicationData(objectName, options).then(dataSet => {
                        updateObject(objectName, objectifier(dataSet))
                        resolve(appObjects[objectName])
                    }).catch(error => reject(error))
                }
            }).catch(error => reject(error))
        })
    }

    floCloudAPI.closeRequest = function (requestID) {
        return new Promise((resolve, reject) => {
            let conn = _liveRequest[requestID]
            if (!conn)
                return reject('Request not found')
            conn.onclose = evt => {
                delete _liveRequest[requestID];
                resolve('Request connection closed')
            }
            conn.close()
        })
    }

    //reset or initialize an object and send it to cloud
    floCloudAPI.resetObjectData = function (objectName, options = {}) {
        return new Promise((resolve, reject) => {
            let message = {
                reset: appObjects[objectName]
            }
            options.comment = 'RESET';
            sendApplicationData(message, objectName, options).then(result => {
                lastCommit.set(objectName);
                resolve(result)
            }).catch(error => reject(error))
        })
    }

    //update the diff and send it to cloud
    floCloudAPI.updateObjectData = function (objectName, options = {}) {
        return new Promise((resolve, reject) => {
            let message = {
                diff: diff.find(lastCommit.get(objectName), appObjects[
                    objectName])
            }
            options.comment = 'UPDATE';
            sendApplicationData(message, objectName, options).then(result => {
                lastCommit.set(objectName);
                resolve(result)
            }).catch(error => reject(error))
        })
    }

    //upload file
    floCloudAPI.uploadFile = function (fileBlob, type, options = {}) {
        return new Promise((resolve, reject) => {
            if (!(fileBlob instanceof File) && !(fileBlob instanceof Blob))
                return reject("file must be instance of File/Blob");
            fileBlob.arrayBuffer().then(arraybuf => {
                let file_data = { type: fileBlob.type, name: fileBlob.name };
                file_data.content = Crypto.util.bytesToBase64(new Uint8Array(arraybuf));
                if (options.encrypt) {
                    let encryptionKey = options.encrypt === true ?
                        floGlobals.settings.encryptionKey : options.encrypt
                    file_data = floCrypto.encryptData(JSON.stringify(file_data), encryptionKey)
                }
                sendApplicationData(file_data, type, options)
                    .then(({ vectorClock, receiverID, type, application }) => resolve({ vectorClock, receiverID, type, application }))
                    .catch(error => reject(error))
            }).catch(error => reject(error))
        })
    }

    //download file
    floCloudAPI.downloadFile = function (vectorClock, options = {}) {
        return new Promise((resolve, reject) => {
            options.atVectorClock = vectorClock;
            requestApplicationData(options.type, options).then(result => {
                if (!result.length)
                    return reject("File not found");
                result = result[0];
                try {
                    let file_data = decodeMessage(result.message);
                    //file is encrypted: decryption required
                    if (file_data instanceof Object && "secret" in file_data) {
                        if (!options.decrypt)
                            return reject("Data is encrypted");
                        let decryptionKey = (options.decrypt === true) ? Crypto.AES.decrypt(user_private, aes_key) : options.decrypt;
                        if (!Array.isArray(decryptionKey))
                            decryptionKey = [decryptionKey];
                        let flag = false;
                        for (let key of decryptionKey) {
                            try {
                                let tmp = floCrypto.decryptData(file_data, key);
                                file_data = JSON.parse(tmp);
                                flag = true;
                                break;
                            } catch (error) { }
                        }
                        if (!flag)
                            return reject("Unable to decrypt file: Invalid private key");
                    }
                    //reconstruct the file
                    let arraybuf = new Uint8Array(Crypto.util.base64ToBytes(file_data.content))
                    result.file = new File([arraybuf], file_data.name, { type: file_data.type });
                    resolve(result)
                } catch (error) {
                    console.error(error);
                    reject("Data is not a file");
                }
            }).catch(error => reject(error))
        })
    }

    /*
    Functions:
    findDiff(original, updatedObj) returns an object with the added, deleted and updated differences  
    mergeDiff(original, allDiff) returns a new object from original object merged with all differences (allDiff is returned object of findDiff)
    */
    var diff = (function () {
        const isDate = d => d instanceof Date;
        const isEmpty = o => Object.keys(o).length === 0;
        const isObject = o => o != null && typeof o === 'object';
        const properObject = o => isObject(o) && !o.hasOwnProperty ? {
            ...o
        } : o;
        const getLargerArray = (l, r) => l.length > r.length ? l : r;

        const preserve = (diff, left, right) => {
            if (!isObject(diff)) return diff;
            return Object.keys(diff).reduce((acc, key) => {
                const leftArray = left[key];
                const rightArray = right[key];
                if (Array.isArray(leftArray) && Array.isArray(rightArray)) {
                    const array = [...getLargerArray(leftArray, rightArray)];
                    return {
                        ...acc,
                        [key]: array.reduce((acc2, item, index) => {
                            if (diff[key].hasOwnProperty(index)) {
                                acc2[index] = preserve(diff[key][index], leftArray[index], rightArray[index]); // diff recurse and check for nested arrays
                                return acc2;
                            }
                            delete acc2[index]; // no diff aka empty
                            return acc2;
                        }, array)
                    };
                }
                return {
                    ...acc,
                    [key]: diff[key]
                };
            }, {});
        };

        const updatedDiff = (lhs, rhs) => {
            if (lhs === rhs) return {};
            if (!isObject(lhs) || !isObject(rhs)) return rhs;
            const l = properObject(lhs);
            const r = properObject(rhs);
            if (isDate(l) || isDate(r)) {
                if (l.valueOf() == r.valueOf()) return {};
                return r;
            }
            return Object.keys(r).reduce((acc, key) => {
                if (l.hasOwnProperty(key)) {
                    const difference = updatedDiff(l[key], r[key]);
                    if (isObject(difference) && isEmpty(difference) && !isDate(difference)) return acc;
                    return {
                        ...acc,
                        [key]: difference
                    };
                }
                return acc;
            }, {});
        };


        const diff = (lhs, rhs) => {
            if (lhs === rhs) return {}; // equal return no diff
            if (!isObject(lhs) || !isObject(rhs)) return rhs; // return updated rhs
            const l = properObject(lhs);
            const r = properObject(rhs);
            const deletedValues = Object.keys(l).reduce((acc, key) => {
                return r.hasOwnProperty(key) ? acc : {
                    ...acc,
                    [key]: null
                };
            }, {});
            if (isDate(l) || isDate(r)) {
                if (l.valueOf() == r.valueOf()) return {};
                return r;
            }
            return Object.keys(r).reduce((acc, key) => {
                if (!l.hasOwnProperty(key)) return {
                    ...acc,
                    [key]: r[key]
                }; // return added r key
                const difference = diff(l[key], r[key]);
                if (isObject(difference) && isEmpty(difference) && !isDate(difference)) return acc; // return no diff
                return {
                    ...acc,
                    [key]: difference
                }; // return updated key
            }, deletedValues);
        };

        const addedDiff = (lhs, rhs) => {
            if (lhs === rhs || !isObject(lhs) || !isObject(rhs)) return {};
            const l = properObject(lhs);
            const r = properObject(rhs);
            return Object.keys(r).reduce((acc, key) => {
                if (l.hasOwnProperty(key)) {
                    const difference = addedDiff(l[key], r[key]);
                    if (isObject(difference) && isEmpty(difference)) return acc;
                    return {
                        ...acc,
                        [key]: difference
                    };
                }
                return {
                    ...acc,
                    [key]: r[key]
                };
            }, {});
        };

        const arrayDiff = (lhs, rhs) => {
            if (lhs === rhs) return {}; // equal return no diff
            if (!isObject(lhs) || !isObject(rhs)) return rhs; // return updated rhs
            const l = properObject(lhs);
            const r = properObject(rhs);
            const deletedValues = Object.keys(l).reduce((acc, key) => {
                return r.hasOwnProperty(key) ? acc : {
                    ...acc,
                    [key]: null
                };
            }, {});
            if (isDate(l) || isDate(r)) {
                if (l.valueOf() == r.valueOf()) return {};
                return r;
            }
            if (Array.isArray(r) && Array.isArray(l)) {
                const deletedValues = l.reduce((acc, item, index) => {
                    return r.hasOwnProperty(index) ? acc.concat(item) : acc.concat(null);
                }, []);
                return r.reduce((acc, rightItem, index) => {
                    if (!deletedValues.hasOwnProperty(index)) {
                        return acc.concat(rightItem);
                    }
                    const leftItem = l[index];
                    const difference = diff(rightItem, leftItem);
                    if (isObject(difference) && isEmpty(difference) && !isDate(difference)) {
                        delete acc[index];
                        return acc; // return no diff
                    }
                    return acc.slice(0, index).concat(rightItem).concat(acc.slice(index + 1)); // return updated key
                }, deletedValues);
            }

            return Object.keys(r).reduce((acc, key) => {
                if (!l.hasOwnProperty(key)) return {
                    ...acc,
                    [key]: r[key]
                }; // return added r key
                const difference = diff(l[key], r[key]);
                if (isObject(difference) && isEmpty(difference) && !isDate(difference)) return acc; // return no diff
                return {
                    ...acc,
                    [key]: difference
                }; // return updated key
            }, deletedValues);
        };

        const deletedDiff = (lhs, rhs) => {
            if (lhs === rhs || !isObject(lhs) || !isObject(rhs)) return {};
            const l = properObject(lhs);
            const r = properObject(rhs);
            return Object.keys(l).reduce((acc, key) => {
                if (r.hasOwnProperty(key)) {
                    const difference = deletedDiff(l[key], r[key]);
                    if (isObject(difference) && isEmpty(difference)) return acc;
                    return {
                        ...acc,
                        [key]: difference
                    };
                }
                return {
                    ...acc,
                    [key]: null
                };
            }, {});
        };

        const mergeRecursive = (obj1, obj2, deleteMode = false) => {
            for (var p in obj2) {
                try {
                    if (obj2[p].constructor == Object)
                        obj1[p] = mergeRecursive(obj1[p], obj2[p], deleteMode);
                    // Property in destination object set; update its value.
                    else if (Array.isArray(obj2[p])) {
                        // obj1[p] = [];
                        if (obj2[p].length < 1)
                            obj1[p] = obj2[p];
                        else
                            obj1[p] = mergeRecursive(obj1[p], obj2[p], deleteMode);
                    } else
                        obj1[p] = deleteMode && obj2[p] === null ? undefined : obj2[p];
                } catch (e) {
                    // Property in destination object not set; create it and set its value.
                    obj1[p] = deleteMode && obj2[p] === null ? undefined : obj2[p];
                }
            }
            return obj1;
        }

        const cleanse = (obj) => {
            Object.keys(obj).forEach(key => {
                var value = obj[key];
                if (typeof value === "object" && value !== null)
                    obj[key] = cleanse(value);
                else if (typeof value === 'undefined')
                    delete obj[key]; // undefined, remove it
            });
            if (Array.isArray(obj))
                obj = obj.filter(v => typeof v !== 'undefined');
            return obj;
        }


        const findDiff = (lhs, rhs) => ({
            added: addedDiff(lhs, rhs),
            deleted: deletedDiff(lhs, rhs),
            updated: updatedDiff(lhs, rhs),
        });

        /*obj is original object or array, diff is the output of findDiff */
        const mergeDiff = (obj, diff) => {
            if (Object.keys(diff.updated).length !== 0)
                obj = mergeRecursive(obj, diff.updated)
            if (Object.keys(diff.deleted).length !== 0) {
                obj = mergeRecursive(obj, diff.deleted, true)
                obj = cleanse(obj)
            }
            if (Object.keys(diff.added).length !== 0)
                obj = mergeRecursive(obj, diff.added)
            return obj
        }

        return {
            find: findDiff,
            merge: mergeDiff
        }
    })();


})('object' === typeof module ? module.exports : window.floCloudAPI = {});
