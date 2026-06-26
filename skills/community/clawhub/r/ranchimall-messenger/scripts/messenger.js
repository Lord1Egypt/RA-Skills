(function () {
    const rmMessenger = window.rmMessenger = {};

    const user = {
        get id() {
            return floDapps.user.id
        },
        get public() {
            return floDapps.user.public
        }
    }

    const expiredKeys = {};

    const UI = {
        group: (d, e) => console.log(d, e),
        pipeline: (d, e) => console.log(d, e),
        direct: (d, e) => console.log(d, e),
        chats: (c) => console.log(c),
        mails: (m) => console.log(m),
        marked: (r) => console.log(r),
        onChatMigrated: (oldID, newID) => console.log(`Migrated ${oldID} to ${newID}`)
    };
    rmMessenger.renderUI = {};
    Object.defineProperties(rmMessenger.renderUI, {
        chats: {
            set: ui_fn => UI.chats = ui_fn
        },
        directChat: {
            set: ui_fn => UI.direct = ui_fn
        },
        groupChat: {
            set: ui_fn => UI.group = ui_fn
        },
        pipeline: {
            set: ui_fn => UI.pipeline = ui_fn
        },
        mails: {
            set: ui_fn => UI.mails = ui_fn
        },
        marked: {
            set: ui_fn => UI.marked = ui_fn
        },
        onChatMigrated: {
            set: ui_fn => UI.onChatMigrated = ui_fn
        }
    });

    const _loaded = {};
    Object.defineProperties(rmMessenger, {
        chats: {
            get: () => _loaded.chats
        },
        groups: {
            get: () => _loaded.groups
        },
        pipeline: {
            get: () => _loaded.pipeline
        },
        blocked: {
            get: () => _loaded.blocked
        },
        marked: {
            get: () => _loaded.marked
        }
    });

    var directConnID = [], groupConnID = {},
        pipeConnID = {};
    rmMessenger.conn = {};
    Object.defineProperties(rmMessenger.conn, {
        direct: {
            get: () => directConnID
        },
        group: {
            get: () => Object.assign({}, groupConnID),
            // value: g_id => groupConnID[g_id]
        }
    });

    // Validate any blockchain address (all 19 supported chains)
    function isValidBlockchainAddress(address) {
        if (!address || typeof address !== 'string') return false;

        // FLO/BTC/DOGE/LTC legacy (Base58, 33-34 chars)
        if ((address.length === 33 || address.length === 34) && /^[1-9A-HJ-NP-Za-km-z]+$/.test(address)) {
            return floCrypto.validateAddr(address) || true;
        }
        // Ethereum/EVM addresses (0x prefix, 40 hex chars) - ETH, AVAX, BSC, MATIC, ARB, OP
        if (/^0x[a-fA-F0-9]{40}$/.test(address)) return true;
        // SUI addresses (0x prefix, 64 hex chars)
        if (/^0x[a-fA-F0-9]{64}$/.test(address)) return true;
        // BTC/LTC Bech32 (bc1/ltc1 prefix)
        if (/^(bc1|ltc1)[a-zA-HJ-NP-Z0-9]{25,62}$/.test(address)) return true;
        // Solana (Base58, 43-44 chars)
        if ((address.length === 43 || address.length === 44) && /^[1-9A-HJ-NP-Za-km-z]+$/.test(address)) return true;
        // XRP (r-prefix, 25-35 chars)
        if (address.startsWith('r') && address.length >= 25 && address.length <= 35 && /^r[a-zA-Z0-9]+$/.test(address)) return true;
        // TRON (T-prefix, 34 chars)
        if (address.startsWith('T') && address.length === 34 && /^T[a-zA-Z0-9]+$/.test(address)) return true;
        // Cardano (addr1 prefix, Bech32)
        if (address.startsWith('addr1') && address.length > 50) return true;
        // Polkadot (SS58, starts with 1, 47-48 chars)
        if (address.startsWith('1') && (address.length === 47 || address.length === 48) && /^[a-zA-Z0-9]+$/.test(address)) return true;
        // TON (Base64 URL-safe, 48 chars)
        if (address.length === 48 && /^[A-Za-z0-9_-]+$/.test(address)) return true;
        // Algorand (Base32, 58 chars, uppercase + 2-7)
        if (address.length === 58 && /^[A-Z2-7]+$/.test(address)) return true;
        // Stellar (G-prefix, Base32, 56 chars)
        if (address.startsWith('G') && address.length === 56 && /^G[A-Z2-7]+$/.test(address)) return true;
        // Bitcoin Cash CashAddr (q-prefix)
        if (address.startsWith('q') && address.length >= 34 && address.length <= 45 && /^q[a-z0-9]+$/.test(address)) return true;
        // HBAR (0.0.xxxxx format)
        if (/^0\.0\.\d+$/.test(address)) return true;

        return false;
    }

    function sendRaw(message, recipient, type, encrypt = null, comment = undefined) {
        return new Promise((resolve, reject) => {
            if (!isValidBlockchainAddress(recipient))
                return reject("Invalid Recipient");

            if ([true, null].includes(encrypt)) {
                // Try to get pubKey safely (may fail for non-FLO addresses)
                let r_pubKey = null;
                try {
                    r_pubKey = floDapps.user.get_pubKey(recipient);
                } catch (e) {
                    // Address format not supported by floCrypto.decodeAddr
                    r_pubKey = floGlobals.pubKeys ? floGlobals.pubKeys[recipient] : null;
                }
                if (r_pubKey)
                    message = floCrypto.encryptData(message, r_pubKey);
                else if (encrypt === true)
                    return reject("recipient's pubKey not found")
            }
            let options = {
                receiverID: recipient,
            }
            if (comment) {
                options.comment = comment;
            }

            // If we're logged in with an alt chain, embed it in the comment for migration mapping
            try {
                let activeChain = localStorage.getItem(`${floGlobals.application}#activeChain`);
                if (activeChain && activeChain !== 'FLO') {
                    let proxyID = null;
                    switch (activeChain) {
                        case 'ETH':
                        case 'AVAX':
                        case 'BSC':
                        case 'MATIC':
                        case 'ARB':
                        case 'OP':
                        case 'HBAR':
                            proxyID = floEthereum.ethAddressFromCompressedPublicKey(user.public); break;
                        case 'BTC': proxyID = floGlobals.myBtcID; break;
                        case 'BCH': proxyID = floGlobals.myBchID; break;
                        case 'XRP': proxyID = floGlobals.myXrpID; break;
                        case 'SUI': proxyID = floGlobals.mySuiID; break;
                        case 'TON': proxyID = floGlobals.myTonID; break;
                        case 'TRON': proxyID = floGlobals.myTronID; break;
                        case 'DOGE': proxyID = floGlobals.myDogeID; break;
                        case 'LTC': proxyID = floGlobals.myLtcID; break;
                        case 'DOT': proxyID = floGlobals.myDotID; break;
                        case 'ALGO': proxyID = floGlobals.myAlgoID; break;
                        case 'XLM': proxyID = floGlobals.myXlmID; break;
                        case 'SOL': proxyID = floGlobals.mySolID; break;
                        case 'ADA': proxyID = floGlobals.myAdaID; break;
                    }
                    if (proxyID && proxyID !== user.id) {
                        options.comment = (options.comment ? options.comment + "|" : "") + "FROM_ALT:" + proxyID;
                    }
                }
            } catch (e) {
                console.warn("Could not append FROM_ALT tag", e);
            }

            floCloudAPI.sendApplicationData(message, type, options)
                .then(result => resolve(result))
                .catch(error => reject(error))
        })
    }
    rmMessenger.sendRaw = sendRaw;

    function encrypt(value, key = _loaded.appendix.AESKey) {
        return Crypto.AES.encrypt(value, key)
    }
    rmMessenger.encrypt = encrypt;

    function decrypt(value, key = _loaded.appendix.AESKey) {
        return Crypto.AES.decrypt(value, key)
    }

    function addMark(key, mark) {
        return new Promise((resolve, reject) => {
            compactIDB.readData("marked", key).then(result => {
                if (!result)
                    result = [mark];
                else if (!result.includes(mark))
                    result.push(mark);
                else
                    return resolve("Mark already exist");
                compactIDB.writeData("marked", result, key)
                    .then(result => resolve(result))
                    .catch(error => reject(error))
            }).catch(error => reject(error))
        })
    }

    function removeMark(key, mark) {
        return new Promise((resolve, reject) => {
            compactIDB.readData("marked", key).then(result => {
                if (!result || !result.includes(mark))
                    return resolve("Mark doesnot exist")
                else {
                    result.splice(result.indexOf(mark), 1); //remove the mark from the list of marks
                    compactIDB.writeData("marked", result, key)
                        .then(result => resolve("Mark removed"))
                        .catch(error => reject(error))
                }
            }).catch(error => reject(error))
        })
    }

    const initUserDB = function () {
        return new Promise((resolve, reject) => {
            var obj = {
                messages: {},
                mails: {},
                marked: {},
                chats: {},
                groups: {},
                gkeys: {},
                blocked: {},
                pipeline: {},
                request_sent: {},
                request_received: {},
                response_sent: {},
                response_received: {},
                flodata: {},
                appendix: {},
                userSettings: {},
                multisigLabels: {}
            }
            let user_db = `${floGlobals.application}_${floCrypto.toFloID(user.id)}`;
            compactIDB.initDB(user_db, obj).then(result => {
                console.info(result)
                compactIDB.setDefaultDB(user_db);
                resolve("Messenger UserDB Initated Successfully")
            }).catch(error => reject(error));
        })
    }

    rmMessenger.blockUser = function (floID) {
        return new Promise((resolve, reject) => {
            if (_loaded.blocked.has(floID))
                return resolve("User is already blocked");
            compactIDB.addData("blocked", true, floID).then(result => {
                _loaded.blocked.add(floID);
                resolve("Blocked User: " + floID);
            }).catch(error => reject(error))
        })
    }

    rmMessenger.unblockUser = function (floID) {
        return new Promise((resolve, reject) => {
            if (!_loaded.blocked.has(floID))
                return resolve("User is not blocked");
            compactIDB.removeData("blocked", floID).then(result => {
                _loaded.blocked.delete(floID);
                resolve("Unblocked User: " + floID);
            }).catch(error => reject(error))
        })
    }

    rmMessenger.sendMessage = function (message, receiver) {
        return new Promise((resolve, reject) => {
            sendRaw(message, receiver, "MESSAGE").then(result => {
                let vc = result.vectorClock;
                let data = {
                    floID: receiver,
                    time: result.time,
                    category: 'sent',
                    message: encrypt(message)
                }
                _loaded.chats[receiver] = parseInt(vc)
                compactIDB.writeData("chats", parseInt(vc), receiver)
                compactIDB.addData("messages", Object.assign({}, data), `${receiver}|${vc}`)
                data.message = message;
                resolve({
                    [vc]: data
                });
            }).catch(error => reject(error))
        })
    }

    rmMessenger.sendMail = function (subject, content, recipients, prev = null) {
        return new Promise((resolve, reject) => {
            if (!Array.isArray(recipients))
                recipients = [recipients]
            let mail = {
                subject: subject,
                content: content,
                ref: Date.now() + floCrypto.randString(8, true),
                prev: prev
            }
            let promises = recipients.map(r => sendRaw(JSON.stringify(mail), r, "MAIL"))
            Promise.allSettled(promises).then(results => {
                mail.time = Date.now();
                mail.from = user.id
                mail.to = []
                results.forEach(r => {
                    if (r.status === "fulfilled")
                        mail.to.push(r.value.receiverID)
                });
                if (mail.to.length === 0)
                    return reject(results)
                mail.content = encrypt(content)
                compactIDB.addData("mails", Object.assign({}, mail), mail.ref)
                mail.content = content
                resolve({
                    [mail.ref]: mail
                });
            })
        })
    }

    function listRequests(obs, options = null) {
        return new Promise((resolve, reject) => {
            compactIDB.readAllData(obs).then(result => {
                if (!options || typeof options !== 'object')
                    return resolve(result);
                let filtered = {};
                for (let k in result) {
                    let val = result[k];
                    if (options.type && options.type == val.type) continue;
                    else if (options.floID && options.floID == val.floID) continue;
                    else if (typeof options.completed !== 'undefined' && options.completed == !(val.completed))
                        continue;
                    filtered[k] = val;
                }
                resolve(filtered);
            }).catch(error => reject(error))
        })
    }

    rmMessenger.list_request_sent = (options = null) => listRequests('request_sent', options);
    rmMessenger.list_request_received = (options = null) => listRequests('request_received', options);
    rmMessenger.list_response_sent = (options = null) => listRequests('response_sent', options);
    rmMessenger.list_response_received = (options = null) => listRequests('response_received', options);

    function sendRequest(receiver, type, message, encrypt = null) {
        return new Promise((resolve, reject) => {
            sendRaw(message, receiver, "REQUEST", encrypt, type).then(result => {
                let vc = result.vectorClock;
                let data = {
                    floID: receiver,
                    time: result.time,
                    message: message,
                    type: type
                }
                compactIDB.addData("request_sent", data, vc);
                resolve({
                    [vc]: data
                });
            }).catch(error => reject(error))
        })
    }

    rmMessenger.request_pubKey = (receiver, message = '') => sendRequest(receiver, "PUBLIC_KEY", message, false);

    function sendResponse(req_id, message, encrypt = null) {
        return new Promise((resolve, reject) => {
            compactIDB.readData("request_received", req_id).then(request => {
                let _message = JSON.stringify({
                    value: message,
                    reqID: req_id
                });
                sendRaw(_message, request.floID, "RESPONSE", encrypt, request.type).then(result => {
                    let vc = result.vectorClock;
                    let data = {
                        floID: request.floID,
                        time: result.time,
                        message: message,
                        type: request.type,
                        reqID: req_id
                    }
                    compactIDB.addData("response_sent", data, vc);
                    request.completed = vc;
                    compactIDB.writeData("request_received", request, req_id);
                    resolve({
                        [vc]: data
                    });
                }).catch(error => reject(error))
            }).catch(error => reject(error))
        })
    }

    rmMessenger.respond_pubKey = (req_id, message = '') => sendResponse(req_id, message, false);

    const processData = {};
    processData.direct = function () {
        return async (unparsed, newInbox) => {
            //store the pubKey if not stored already
            floDapps.storePubKey(unparsed.senderID, unparsed.pubKey);
            if (_loaded.blocked.has(unparsed.senderID) && unparsed.type !== "REVOKE_KEY")
                throw "blocked-user";
            if (unparsed.message instanceof Object && "secret" in unparsed.message)
                unparsed.message = floDapps.user.decrypt(unparsed.message);
            let vc = unparsed.vectorClock;
            switch (unparsed.type) {
                case "MESSAGE": { //process as message
                    let vc = unparsed.vectorClock;

                    // Chat Migration Logic
                    if (unparsed.comment && unparsed.comment.includes("FROM_ALT:")) {
                        let altID = unparsed.comment.split("FROM_ALT:")[1].split("|")[0]; // Extract the alt ID
                        if (altID && altID !== unparsed.senderID) {
                            // Check if an existing chat with this alt ID exists
                            if (_loaded.chats[altID] !== undefined) {
                                console.log(`Migrating chat history from ${altID} to ${unparsed.senderID}`);

                                // Run migration asynchronously but wait for it to complete
                                try {
                                    // Migrate Messages
                                    let _options = { lowerKey: `${altID}|`, upperKey: `${altID}||` };
                                    let result = await compactIDB.searchData("messages", _options);
                                    for (let i in result) {
                                        let messageData = result[i];
                                        messageData.floID = unparsed.senderID;
                                        let oldVc = i.split("|")[1];
                                        await compactIDB.addData("messages", messageData, `${unparsed.senderID}|${oldVc}`).catch(e => console.warn(e));
                                        await compactIDB.removeData("messages", i);
                                    }

                                    // Migrate Contacts
                                    if (floGlobals.contacts[altID]) {
                                        let contactName = floGlobals.contacts[altID];
                                        floDapps.storeContact(unparsed.senderID, contactName);
                                        await compactIDB.removeData("contacts", altID, floDapps.user.db_name);
                                        delete floGlobals.contacts[altID];
                                    }

                                    // Delete old chat reference
                                    delete _loaded.chats[altID];
                                    await compactIDB.removeData("chats", altID);

                                    // Trigger UI update if available
                                    if (UI.onChatMigrated) UI.onChatMigrated(altID, unparsed.senderID);
                                    if (UI.chats) await UI.chats(getChatOrder());
                                } catch (error) {
                                    console.error("Migration failed:", error);
                                }
                            }
                        }
                    }

                    let dm = {
                        time: unparsed.time,
                        floID: unparsed.senderID,
                        category: "received",
                        message: encrypt(unparsed.message)
                    }
                    console.debug(dm, `${dm.floID}|${vc}`);
                    try {
                        await compactIDB.addData("messages", Object.assign({}, dm), `${dm.floID}|${vc}`);
                    } catch (e) {
                        console.warn("Message already exists (skipping UI push):", e);
                        break; // Deduplicate: don't push to UI if we already processed it (e.g. self-messaging)
                    }
                    _loaded.chats[dm.floID] = parseInt(vc)
                    compactIDB.writeData("chats", parseInt(vc), dm.floID)
                    dm.message = unparsed.message;
                    newInbox.messages[vc] = dm;
                    addMark(dm.floID, "unread");
                    break;
                }
                case "REQUEST": {
                    let req = {
                        floID: unparsed.senderID,
                        time: unparsed.time,
                        message: unparsed.message,
                        type: unparsed.comment
                    }
                    compactIDB.addData("request_received", req, vc);
                    newInbox.requests[vc] = req;
                    break;
                }
                case "RESPONSE": {
                    let data = JSON.parse(unparsed.message);
                    let res = {
                        floID: unparsed.senderID,
                        time: unparsed.time,
                        message: data.value,
                        type: unparsed.comment,
                        reqID: data.reqID
                    }
                    compactIDB.addData("response_received", res, vc);
                    compactIDB.readData("request_sent", data.reqID).then(req => {
                        req.completed = vc;
                        compactIDB.writeData("request_sent", req, data.reqID)
                    });
                    newInbox.responses[vc] = res;
                    break;
                }
                case "MAIL": { //process as mail
                    let data = JSON.parse(unparsed.message);
                    let mail = {
                        time: unparsed.time,
                        from: unparsed.senderID,
                        to: [unparsed.receiverID],
                        subject: data.subject,
                        content: encrypt(data.content),
                        ref: data.ref,
                        prev: data.prev
                    }
                    compactIDB.addData("mails", Object.assign({}, mail), mail.ref);
                    mail.content = data.content;
                    newInbox.mails[mail.ref] = mail;
                    addMark(mail.ref, "unread");
                    break;
                }
                case "CREATE_GROUP": { //process create group
                    let groupInfo = JSON.parse(unparsed.message);
                    let h = ["groupID", "created", "admin"].map(x => groupInfo[x]).join('|')
                    if (groupInfo.admin === unparsed.senderID &&
                        floCrypto.verifySign(h, groupInfo.hash, groupInfo.pubKey) &&
                        floCrypto.getFloID(groupInfo.pubKey) === groupInfo.groupID) {
                        let eKey = groupInfo.eKey
                        groupInfo.eKey = encrypt(eKey)
                        compactIDB.writeData("groups", Object.assign({}, groupInfo), groupInfo.groupID)
                        groupInfo.eKey = eKey
                        _loaded.groups[groupInfo.groupID] = groupInfo
                        requestGroupInbox(groupInfo.groupID)
                        newInbox.newgroups.push(groupInfo.groupID)
                    }
                    break;
                }
                case "REVOKE_KEY": { //revoke group key
                    let r = JSON.parse(unparsed.message);
                    let groupInfo = _loaded.groups[r.groupID]
                    if (unparsed.senderID === groupInfo.admin) {
                        if (typeof expiredKeys[r.groupID] !== "object")
                            expiredKeys[r.groupID] = {}
                        expiredKeys[r.groupID][vc] = groupInfo.eKey
                        let eKey = r.newKey
                        groupInfo.eKey = encrypt(eKey);
                        compactIDB.writeData("groups", Object.assign({}, groupInfo), groupInfo.groupID)
                        groupInfo.eKey = eKey
                        newInbox.keyrevoke.push(groupInfo.groupID)
                    }
                    break;
                }
                case "CREATE_PIPELINE": { //add pipeline
                    let pipelineInfo = JSON.parse(unparsed.message);
                    let eKey = pipelineInfo.eKey;
                    pipelineInfo.eKey = encrypt(eKey)
                    compactIDB.addData("pipeline", Object.assign({}, pipelineInfo), pipelineInfo.id);
                    pipelineInfo.eKey = eKey;
                    _loaded.pipeline[pipelineInfo.id] = pipelineInfo
                    requestPipelineInbox(pipelineInfo.id, pipelineInfo.model);
                    newInbox.pipeline[pipelineInfo.id] = pipelineInfo.model;
                }
            }
        }
    }

    const requestDirectInbox = rmMessenger.reconnectInbox = function () {
        if (directConnID.length) { //close existing request connection (if any)
            directConnID.forEach(id => floCloudAPI.closeRequest(id));
            directConnID = [];
        }
        const parseData = processData.direct();
        let callbackFn = async function (dataSet, error) {
            if (error)
                return console.error(error)
            let newInbox = {
                messages: {},
                requests: {},
                responses: {},
                mails: {},
                newgroups: [],
                keyrevoke: [],
                pipeline: {}
            }
            // Await processing in order according to vector clocks
            let sortedVCs = Object.keys(dataSet).sort((a, b) => parseInt(a) - parseInt(b));
            for (let vc of sortedVCs) {
                try {
                    await parseData(dataSet[vc], newInbox);
                } catch (error) {
                    //if (error !== "blocked-user")
                    console.log(error);
                } finally {
                    if (_loaded.appendix.lastReceived < vc)
                        _loaded.appendix.lastReceived = vc;
                }
            }
            compactIDB.writeData("appendix", _loaded.appendix.lastReceived, "lastReceived");
            console.debug(newInbox);
            UI.direct(newInbox)
        }
        return new Promise(async (resolve, reject) => {
            // All blockchain address IDs to listen on
            let activeChain = localStorage.getItem(`${floGlobals.application}#activeChain`);
            const blockchainAddressIDs = [floGlobals.myFloID || user.id]; // Always listen to FLO address (primary)

            if (!activeChain) {
                try {
                    let privKey = floDapps.user.private;
                    if (privKey instanceof Promise) privKey = await privKey;
                    if (typeof privKey === 'string' && privKey.length > 0) {
                        if (privKey.startsWith('suiprivkey1')) activeChain = 'SUI';
                        else if (privKey.startsWith('s')) activeChain = 'XRP';
                        else if (privKey.startsWith('Q') || privKey.startsWith('6')) activeChain = 'DOGE';
                        else if (privKey.startsWith('T') && privKey.length === 51) activeChain = 'LTC';
                        else if (privKey.startsWith('K') || privKey.startsWith('L') || privKey.startsWith('5')) activeChain = 'BTC';
                        else if (privKey.startsWith('S') && privateKey.length === 56) activeChain = 'XLM';
                        else if (privKey.startsWith('R') || privKey.startsWith('c') || privKey.startsWith('p')) activeChain = 'FLO';
                    }
                } catch (e) {
                    console.warn("Could not deduce fallback activeChain", e);
                }
            }

            if (activeChain) {
                const addIfValid = (id) => { if (id && !blockchainAddressIDs.includes(id)) blockchainAddressIDs.push(id) };

                switch (activeChain) {
                    case 'ETH':
                    case 'AVAX':
                    case 'BSC':
                    case 'MATIC':
                    case 'ARB':
                    case 'OP':
                    case 'HBAR':
                        addIfValid(floEthereum.ethAddressFromCompressedPublicKey(user.public));
                        break;
                    case 'BTC': addIfValid(floGlobals.myBtcID); break;
                    case 'BCH': addIfValid(floGlobals.myBchID); break;
                    case 'XRP': addIfValid(floGlobals.myXrpID); break;
                    case 'SUI': addIfValid(floGlobals.mySuiID); break;
                    case 'TON': addIfValid(floGlobals.myTonID); break;
                    case 'TRON': addIfValid(floGlobals.myTronID); break;
                    case 'DOGE': addIfValid(floGlobals.myDogeID); break;
                    case 'LTC': addIfValid(floGlobals.myLtcID); break;
                    case 'DOT': addIfValid(floGlobals.myDotID); break;
                    case 'ALGO': addIfValid(floGlobals.myAlgoID); break;
                    case 'XLM': addIfValid(floGlobals.myXlmID); break;
                    case 'SOL': addIfValid(floGlobals.mySolID); break;
                    case 'ADA': addIfValid(floGlobals.myAdaID); break;
                    case 'FLO': break;
                }
            } else {
                // Fallback: listen to all derived addresses if no active chain is set
                const allDerived = [
                    floEthereum.ethAddressFromCompressedPublicKey(user.public),
                    floGlobals.myBtcID, floGlobals.myAvaxID, floGlobals.myBscID,
                    floGlobals.myMaticID, floGlobals.myArbID, floGlobals.myOpID,
                    floGlobals.myHbarID, floGlobals.myXrpID,
                    floGlobals.mySuiID, floGlobals.myTonID, floGlobals.myTronID,
                    floGlobals.myDogeID, floGlobals.myLtcID, floGlobals.myBchID,
                    floGlobals.myDotID, floGlobals.myAlgoID, floGlobals.myXlmID,
                    floGlobals.mySolID, floGlobals.myAdaID
                ];
                allDerived.forEach(id => {
                    if (id && !blockchainAddressIDs.includes(id)) {
                        blockchainAddressIDs.push(id);
                    }
                });
            }

            const promises = blockchainAddressIDs.map(receiverID =>
                floCloudAPI.requestApplicationData(null, {
                    receiverID: receiverID,
                    lowerVectorClock: _loaded.appendix.lastReceived + 1,
                    callback: callbackFn
                })
            );
            Promise.all(promises).then(connectionIds => {
                directConnID = [...directConnID, ...connectionIds];
                resolve("Direct Inbox connected");
            }).catch(error => reject(error))
        })
    }

    rmMessenger.getMail = function (mailRef) {
        return new Promise((resolve, reject) => {
            compactIDB.readData("mails", mailRef).then(mail => {
                mail.content = decrypt(mail.content)
                resolve(mail)
            }).catch(error => reject(error))
        });
    }

    const getChatOrder = rmMessenger.getChatOrder = function (separate = false) {
        let result;
        if (separate) {
            result = {};
            result.direct = Object.keys(_loaded.chats).map(a => [_loaded.chats[a], a])
                .sort((a, b) => b[0] - a[0]).map(a => a[1]);
            result.group = Object.keys(_loaded.groups).map(a => [parseInt(_loaded.appendix[`lastReceived_${a}`]), a])
                .sort((a, b) => b[0] - a[0]).map(a => a[1]);
            result.pipeline = Object.keys(_loaded.pipeline).map(a => [parseInt(_loaded.appendix[`lastReceived_${a}`]), a])
                .sort((a, b) => b[0] - a[0]).map(a => a[1]);
        } else {
            result = Object.keys(_loaded.chats).map(a => [_loaded.chats[a], a])
                .concat(Object.keys(_loaded.groups).map(a => [parseInt(_loaded.appendix[`lastReceived_${a}`]), a]))
                .concat(Object.keys(_loaded.pipeline).map(a => [parseInt(_loaded.appendix[`lastReceived_${a}`]), a]))
                .sort((a, b) => b[0] - a[0]).map(a => a[1])
        }
        return result;
    }

    rmMessenger.storeContact = function (floID, name) {
        // For FLO/BTC addresses, use the standard validation
        if (floCrypto.validateAddr(floID)) {
            return floDapps.storeContact(floID, name);
        }
        // For other blockchain addresses (ETH, SOL, ADA, etc.), store directly
        return new Promise((resolve, reject) => {
            compactIDB.writeData("contacts", name, floID, floDapps.user.db_name).then(result => {
                floGlobals.contacts[floID] = name;
                resolve("Contact stored");
            }).catch(error => reject(error));
        });
    }

    const loadDataFromIDB = function (defaultList = true) {
        return new Promise((resolve, reject) => {
            if (defaultList)
                dataList = ["mails", "marked", "groups", "pipeline", "chats", "blocked", "appendix"]
            else
                dataList = ["messages", "mails", "marked", "chats", "groups", "gkeys", "pipeline", "blocked", "appendix"]
            let promises = []
            for (var i = 0; i < dataList.length; i++)
                promises[i] = compactIDB.readAllData(dataList[i])
            Promise.all(promises).then(results => {
                let data = {}
                for (var i = 0; i < dataList.length; i++)
                    data[dataList[i]] = results[i]
                data.appendix.lastReceived = data.appendix.lastReceived || '0';
                if (data.appendix.AESKey) {
                    try {
                        let AESKey = floDapps.user.decrypt(data.appendix.AESKey);
                        data.appendix.AESKey = AESKey;
                        if (dataList.includes("messages"))
                            for (let m in data.messages)
                                if (data.messages[m].message)
                                    data.messages[m].message = decrypt(data.messages[m].message, AESKey);
                        if (dataList.includes("mails"))
                            for (let m in data.mails)
                                data.mails[m].content = decrypt(data.mails[m].content, AESKey);
                        if (dataList.includes("groups"))
                            for (let g in data.groups)
                                data.groups[g].eKey = decrypt(data.groups[g].eKey, AESKey);
                        if (dataList.includes("gkeys"))
                            for (let k in data.gkeys)
                                data.gkeys[k] = decrypt(data.gkeys[k], AESKey);
                        if (dataList.includes("pipeline"))
                            for (let p in data.pipeline)
                                data.pipeline[p].eKey = decrypt(data.pipeline[p].eKey, AESKey);
                        resolve(data)
                    } catch (error) {
                        console.error(error)
                        reject("Corrupted AES Key");
                    }
                } else {
                    if (Object.keys(data.mails).length)
                        return reject("AES Key not Found")
                    let AESKey = floCrypto.randString(32, false);
                    let encryptedKey = floCrypto.encryptData(AESKey, user.public);
                    compactIDB.addData("appendix", encryptedKey, "AESKey").then(result => {
                        data.appendix.AESKey = AESKey;
                        resolve(data);
                    }).catch(error => reject("Unable to Generate AES Key"))
                }
            }).catch(error => reject(error))
        })
    }

    rmMessenger.addMark = function (key, mark) {
        if (_loaded.marked.hasOwnProperty(key) && !_loaded.marked[key].includes(mark))
            _loaded.marked[key].push(mark)
        return addMark(key, mark)
    }

    rmMessenger.removeMark = function (key, mark) {
        if (_loaded.marked.hasOwnProperty(key))
            _loaded.marked[key] = _loaded.marked[key].filter(v => v !== mark)
        return removeMark(key, mark)
    }

    rmMessenger.addChat = function (chatID) {
        return new Promise((resolve, reject) => {
            compactIDB.addData("chats", 0, chatID)
                .then(result => resolve("Added chat"))
                .catch(error => reject(error))
        })
    }

    rmMessenger.rmChat = function (chatID) {
        return new Promise((resolve, reject) => {
            compactIDB.removeData("chats", chatID)
                .then(result => resolve("Chat removed"))
                .catch(error => reject(error))
        })
    }

    rmMessenger.clearChat = function (chatID) {
        return new Promise((resolve, reject) => {
            let options = {
                lowerKey: `${chatID}|`,
                upperKey: `${chatID}||`
            }
            compactIDB.searchData("messages", options).then(result => {
                let promises = []
                for (let i in result)
                    promises.push(compactIDB.removeData("messages", i))
                Promise.all(promises)
                    .then(result => resolve("Chat cleared"))
                    .catch(error => reject(error))
            }).catch(error => reject(error))
        })
    }

    const getChat = rmMessenger.getChat = function (chatID) {
        return new Promise((resolve, reject) => {
            let options = {
                lowerKey: `${chatID}|`,
                upperKey: `${chatID}||`
            }
            compactIDB.searchData("messages", options).then(result => {
                for (let i in result)
                    if (result[i].message)
                        result[i].message = decrypt(result[i].message)
                resolve(result)
            }).catch(error => reject(error))
        })
    }

    rmMessenger.backupData = function () {
        return new Promise((resolve, reject) => {
            loadDataFromIDB(false).then(data => {
                delete data.appendix.AESKey;
                data.contacts = floGlobals.contacts;
                data.pubKeys = floGlobals.pubKeys;
                data = btoa(unescape(encodeURIComponent(JSON.stringify(data))))
                let blobData = {
                    floID: user.id,
                    pubKey: user.public,
                    data: floDapps.user.encipher(data),
                }
                blobData.sign = floDapps.user.sign(blobData.data);
                resolve(new Blob([JSON.stringify(blobData)], {
                    type: 'application/json'
                }));
            }).catch(error => reject(error))
        })
    }

    const parseBackup = rmMessenger.parseBackup = function (blob) {
        return new Promise((resolve, reject) => {
            if (blob instanceof Blob || blob instanceof File) {
                let reader = new FileReader();
                reader.onload = evt => {
                    var blobData = JSON.parse(evt.target.result);
                    if (!floCrypto.verifySign(blobData.data, blobData.sign, blobData.pubKey))
                        reject("Corrupted Backup file: Signature verification failed");
                    else if (user.id !== blobData.floID || user.public !== blobData.pubKey)
                        reject("Invalid Backup file: Incorrect floID");
                    else {
                        try {
                            let data = floDapps.user.decipher(blobData.data);
                            try {
                                data = JSON.parse(decodeURIComponent(escape(atob(data))));
                                resolve(data)
                            } catch (e) {
                                reject("Corrupted Backup file: Parse failed");
                            }
                        } catch (e) {
                            reject("Corrupted Backup file: Decryption failed");
                        }
                    }
                }
                reader.readAsText(blob);
            } else
                reject("Backup is not a valid File (or) Blob")
        })
    }

    rmMessenger.restoreData = function (arg) {
        return new Promise((resolve, reject) => {
            if (arg instanceof Blob || arg instanceof File)
                var parseData = parseBackup
            else
                var parseData = data => new Promise((res, rej) => res(data))
            parseData(arg).then(data => {
                for (let m in data.messages)
                    if (data.messages[m].message)
                        data.messages[m].message = encrypt(data.messages[m].message)
                for (let m in data.mails)
                    data.mails[m].content = encrypt(data.mails[m].content)
                for (let k in data.gkeys)
                    data.gkeys[k] = encrypt(data.gkeys[k])
                for (let g in data.groups)
                    data.groups[g].eKey = encrypt(data.groups[g].eKey)
                for (let p in data.pipeline)
                    data.pipeline[p].eKey = encrypt(data.pipeline[p].eKey)
                for (let c in data.chats)
                    if (data.chats[c] <= _loaded.chats[c])
                        delete data.chats[c]
                for (let l in data.appendix)
                    if (l.startsWith('lastReceived') && data.appendix[l] <= _loaded.appendix[l])
                        delete data.appendix[l]
                for (let c in data.contacts)
                    if (c in floGlobals.contacts)
                        delete data.contacts[c]
                for (let p in data.pubKeys)
                    if (p in floGlobals.pubKeys)
                        delete data.pubKeys[p]
                let promises = [];
                for (let obs in data) {
                    let writeFn;
                    switch (obs) {
                        case "contacts":
                            writeFn = (k, v) => floDapps.storeContact(k, v);
                            break;
                        case "pubKeys":
                            writeFn = (k, v) => floDapps.storePubKey(k, v);
                            break;
                        default:
                            writeFn = (k, v) => compactIDB.writeData(obs, v, k);
                            break;
                    }
                    for (let k in data[obs])
                        promises.push(writeFn(k, data[obs][k]));
                }

                Promise.all(promises)
                    .then(results => resolve("Restore Successful"))
                    .catch(error => reject("Restore Failed: Unable to write to IDB"))
            }).catch(error => reject(error))
        })
    }

    rmMessenger.clearUserData = function () {
        return new Promise((resolve, reject) => {
            let user_floID = floCrypto.toFloID(user.id);
            let promises = [
                compactIDB.deleteDB(`${floGlobals.application}_${user_floID}`),
                compactIDB.removeData('lastTx', `${floGlobals.application}|${user_floID}`, floDapps.root),
                floDapps.clearCredentials()
            ]
            Promise.all(promises)
                .then(result => resolve("User Data cleared"))
                .catch(error => reject(error))
        })
    }

    //group feature

    rmMessenger.createGroup = function (groupname, description = '') {
        return new Promise((resolve, reject) => {
            if (!groupname) return reject("Invalid Group Name")
            let id = floCrypto.generateNewID();
            let groupInfo = {
                groupID: id.floID,
                pubKey: id.pubKey,
                admin: user.id,
                name: groupname,
                description: description,
                created: Date.now(),
                members: [user.id]
            }
            let h = ["groupID", "created", "admin"].map(x => groupInfo[x]).join('|')
            groupInfo.hash = floCrypto.signData(h, id.privKey)
            let eKey = floCrypto.randString(16, false)
            groupInfo.eKey = encrypt(eKey)
            let p1 = compactIDB.addData("groups", groupInfo, id.floID)
            let p2 = compactIDB.addData("gkeys", encrypt(id.privKey), id.floID)
            Promise.all([p1, p2]).then(r => {
                groupInfo.eKey = eKey
                _loaded.groups[id.floID] = groupInfo;
                requestGroupInbox(id.floID)
                resolve(groupInfo)
            }).catch(e => reject(e))
        })
    }

    rmMessenger.changeGroupName = function (groupID, name) {
        return new Promise((resolve, reject) => {
            let groupInfo = _loaded.groups[groupID]
            if (user.id !== groupInfo.admin)
                return reject("Access denied: Admin only!")
            let message = encrypt(name, groupInfo.eKey)
            sendRaw(message, groupID, "UP_NAME", false)
                .then(result => resolve('Name updated'))
                .catch(error => reject(error))
        })
    }

    rmMessenger.changeGroupDescription = function (groupID, description) {
        return new Promise((resolve, reject) => {
            let groupInfo = _loaded.groups[groupID]
            if (user.id !== groupInfo.admin)
                return reject("Access denied: Admin only!")
            let message = encrypt(description, groupInfo.eKey)
            sendRaw(message, groupID, "UP_DESCRIPTION", false)
                .then(result => resolve('Description updated'))
                .catch(error => reject(error))
        })
    }

    rmMessenger.addGroupMembers = function (groupID, newMem, note = undefined) {
        return new Promise((resolve, reject) => {
            if (!Array.isArray(newMem) && typeof newMem === "string")
                newMem = [newMem]
            //check for validity
            let imem1 = [],
                imem2 = []
            newMem.forEach(m =>
                !floCrypto.validateAddr(m) ? imem1.push(m) :
                    m in floGlobals.pubKeys ? null : imem2.push(m)
            );
            if (imem1.length)
                return reject(`Invalid Members(floIDs): ${imem1}`)
            else if (imem2.length)
                return reject(`Invalid Members (pubKey not available): ${imem2}`)
            //send new newMem list to existing members
            let groupInfo = _loaded.groups[groupID]
            if (user.id !== groupInfo.admin)
                return reject("Access denied: Admin only!")
            let k = groupInfo.eKey;
            //send groupInfo to new newMem
            groupInfo = JSON.stringify(groupInfo)
            let promises = newMem.map(m => sendRaw(groupInfo, m, "CREATE_GROUP", true));
            Promise.allSettled(promises).then(results => {
                let success = [],
                    failed = [];
                for (let i in results)
                    if (results[i].status === "fulfilled")
                        success.push(newMem[i])
                    else if (results[i].status === "rejected")
                        failed.push(newMem[i])
                let message = encrypt(success.join("|"), k)
                sendRaw(message, groupID, "ADD_MEMBERS", false, note)
                    .then(r => resolve(`Members added: ${success}`))
                    .catch(e => reject(e))
            })
        })
    }

    rmMessenger.rmGroupMembers = function (groupID, rmMem, note = undefined) {
        return new Promise((resolve, reject) => {
            if (!Array.isArray(rmMem) && typeof rmMem === "string")
                rmMem = [rmMem]
            let groupInfo = _loaded.groups[groupID]
            let imem = rmMem.filter(m => !groupInfo.members.includes(m))
            if (imem.length)
                return reject(`Invalid members: ${imem}`)
            if (user.id !== groupInfo.admin)
                return reject("Access denied: Admin only!")
            let message = encrypt(rmMem.join("|"), groupInfo.eKey)
            let p1 = sendRaw(message, groupID, "RM_MEMBERS", false, note)
            groupInfo.members = groupInfo.members.filter(m => !rmMem.includes(m))
            let p2 = revokeKey(groupID)
            Promise.all([p1, p2])
                .then(r => resolve(`Members removed: ${rmMem}`))
                .catch(e => reject(e))
        })
    }

    const revokeKey = rmMessenger.revokeKey = function (groupID) {
        return new Promise((resolve, reject) => {
            let groupInfo = _loaded.groups[groupID]
            if (user.id !== groupInfo.admin)
                return reject("Access denied: Admin only!")
            let newKey = floCrypto.randString(16, false);
            Promise.all(groupInfo.members.map(m => sendRaw(JSON.stringify({
                newKey,
                groupID
            }), m, "REVOKE_KEY", true))).then(result => {
                resolve("Group key revoked")
            }).catch(error => reject(error))
        })
    }

    rmMessenger.sendGroupMessage = function (message, groupID) {
        return new Promise((resolve, reject) => {
            let k = _loaded.groups[groupID].eKey
            message = encrypt(message, k)
            sendRaw(message, groupID, "GROUP_MSG", false)
                .then(result => resolve(`${groupID}: ${message}`))
                .catch(error => reject(error))
        })
    }

    const disableGroup = rmMessenger.disableGroup = function (groupID) {
        return new Promise((resolve, reject) => {
            if (!_loaded.groups[groupID])
                return reject("Group not found");
            let groupInfo = Object.assign({}, _loaded.groups[groupID]);
            if (groupInfo.disabled)
                return resolve("Group already diabled");
            groupInfo.disabled = true;
            groupInfo.eKey = encrypt(groupInfo.eKey)
            compactIDB.writeData("groups", groupInfo, groupID).then(result => {
                floCloudAPI.closeRequest(groupConnID[groupID]);
                delete groupConnID[groupID];
                resolve("Group diabled");
            }).catch(error => reject(error))
        })
    }

    processData.group = function (groupID) {
        return (unparsed, newInbox) => {
            if (!_loaded.groups[groupID].members.includes(unparsed.senderID))
                return;
            //store the pubKey if not stored already
            floDapps.storePubKey(unparsed.senderID, unparsed.pubKey)
            let data = {
                time: unparsed.time,
                sender: unparsed.senderID,
                groupID: unparsed.receiverID
            }
            let vc = unparsed.vectorClock,
                k = _loaded.groups[groupID].eKey;
            if (expiredKeys[groupID]) {
                var ex = Object.keys(expiredKeys[groupID]).sort()
                while (ex.length && vc > ex[0]) ex.shift()
                if (ex.length)
                    k = expiredKeys[groupID][ex.shift()]
            }
            unparsed.message = decrypt(unparsed.message, k);
            var infoChange = false;
            if (unparsed.type === "GROUP_MSG")
                data.message = encrypt(unparsed.message);
            else if (data.sender === _loaded.groups[groupID].admin) {
                let groupInfo = _loaded.groups[groupID]
                data.admin = true;
                switch (unparsed.type) {
                    case "ADD_MEMBERS": {
                        data.newMembers = unparsed.message.split("|")
                        data.note = unparsed.comment
                        groupInfo.members = Array.from(new Set(groupInfo.members.concat(data.newMembers)))
                        break;
                    }
                    case "UP_DESCRIPTION": {
                        data.description = unparsed.message;
                        groupInfo.description = data.description;
                        break;
                    }
                    case "RM_MEMBERS": {
                        data.rmMembers = unparsed.message.split("|")
                        data.note = unparsed.comment
                        groupInfo.members = groupInfo.members.filter(m => !data.rmMembers.includes(m))
                        if (data.rmMembers.includes(user.id)) {
                            disableGroup(groupID);
                            return;
                        }
                        break;
                    }
                    case "UP_NAME": {
                        data.name = unparsed.message
                        groupInfo.name = data.name;
                        break;
                    }
                }
                infoChange = true;
            }
            compactIDB.addData("messages", Object.assign({}, data), `${groupID}|${vc}`)
            if (data.message)
                data.message = decrypt(data.message);
            newInbox.messages[vc] = data;
            if (!floCrypto.isSameAddr(data.sender, user.id))
                addMark(data.groupID, "unread");
            return infoChange;
        }
    }

    function requestGroupInbox(groupID, _async = true) {
        if (groupConnID[groupID]) { //close existing request connection (if any)
            floCloudAPI.closeRequest(groupConnID[groupID]);
            delete groupConnID[groupID];
        }

        const parseData = processData.group(groupID);
        let callbackFn = function (dataSet, error) {
            if (error)
                return console.error(error)
            console.info(dataSet)
            let newInbox = {
                messages: {}
            }
            let infoChange = false;
            for (let vc in dataSet) {
                if (groupID !== dataSet[vc].receiverID)
                    continue;
                try {
                    infoChange = parseData(dataSet[vc], newInbox) || infoChange;
                    if (!_loaded.appendix[`lastReceived_${groupID}`] ||
                        _loaded.appendix[`lastReceived_${groupID}`] < vc)
                        _loaded.appendix[`lastReceived_${groupID}`] = vc;
                } catch (error) {
                    console.log(error)
                }
            }
            compactIDB.writeData("appendix", _loaded.appendix[`lastReceived_${groupID}`], `lastReceived_${groupID}`);
            if (infoChange) {
                let newInfo = Object.assign({}, _loaded.groups[groupID]);
                newInfo.eKey = encrypt(newInfo.eKey)
                compactIDB.writeData("groups", newInfo, groupID)
            }
            console.debug(newInbox);
            UI.group(newInbox);
        }
        let fn = floCloudAPI.requestApplicationData(null, {
            receiverID: groupID,
            lowerVectorClock: _loaded.appendix[`lastReceived_${groupID}`] + 1,
            callback: callbackFn
        });
        if (_async) {
            fn.then(conn_id => groupConnID[groupID] = conn_id)
                .catch(error => console.error(`request-group(${groupID}):`, error))
        } else {
            return new Promise((resolve, reject) => {
                fn.then(conn_id => {
                    groupConnID[groupID] = conn_id;
                    resolve(`Connected to group ${groupID}`);
                }).catch(error => reject(error))
            });
        }
    }

    //rmMessenger startups
    rmMessenger.init = function () {
        return new Promise((resolve, reject) => {
            initUserDB().then(result => {
                console.debug(result);
                loadDataFromIDB().then(data => {
                    console.debug(data);
                    //load data to memory
                    _loaded.appendix = data.appendix;
                    _loaded.groups = data.groups;
                    _loaded.pipeline = data.pipeline;
                    _loaded.chats = data.chats;
                    _loaded.marked = data.marked;
                    _loaded.blocked = new Set(Object.keys(data.blocked));
                    //call UI render functions
                    UI.chats(getChatOrder());
                    UI.mails(data.mails);
                    UI.marked(data.marked);
                    resolve('Loaded local data')
                    //request data from cloud
                    let promises = [];
                    promises.push(requestDirectInbox());
                    for (let g in data.groups)
                        if (data.groups[g].disabled !== true)
                            promises.push(requestGroupInbox(g, false));
                    for (let p in data.pipeline)
                        if (data.pipeline[p].disabled !== true)
                            promises.push(requestPipelineInbox(p, data.pipeline[p].model, false));
                    loadDataFromBlockchain().then(result => {
                        Promise.all(promises)
                            .then(result => resolve("Messenger initiated"))
                            .catch(error => reject(error))
                    }).catch(error => reject(error))
                }).catch(error => reject(error));
            })
        })
    }

    const loadDataFromBlockchain = rmMessenger.loadDataFromBlockchain = function () {
        return new Promise((resolve, reject) => {
            let user_floID = floCrypto.toFloID(user.id);
            if (!user_floID)
                return reject("Not an valid address");
            let last_key = `${floGlobals.application}|${user_floID}`;
            compactIDB.readData("lastTx", last_key, floDapps.root).then(lastTx => {
                var query_options = { pattern: floGlobals.application, tx: true };
                if (typeof lastTx == 'number')  //lastTx is tx count (*backward support)
                    query_options.ignoreOld = lastTx;
                else if (typeof lastTx == 'string') //lastTx is txid of last tx
                    query_options.after = lastTx;
                floBlockchainAPI.readData(user_floID, query_options).then(result => {
                    for (var i = result.items.length - 1; i >= 0; i--) {
                        let tx = result.items[i],
                            content = JSON.parse(tx.data)[floGlobals.application];
                        if (!(content instanceof Object))
                            continue;
                        let key = (content.type ? content.type + "|" : "") + tx.txid.substr(0, 16);
                        compactIDB.writeData("flodata", {
                            time: tx.time,
                            txid: tx.txid,
                            data: content
                        }, key);
                    }
                    compactIDB.writeData("lastTx", result.lastItem, last_key, floDapps.root);
                    resolve(true);
                }).catch(error => reject(error))
            }).catch(error => reject(error))
        })
    }

    //BTC multisig application
    const MultiSig = rmMessenger.multisig = {}
    const TYPE_BTC_MULTISIG = "btc_multisig", //used for both pipeline and multisig address creation
        TYPE_FLO_MULTISIG = "flo_multisig"; //only used for pipeline

    MultiSig.createAddress = function (pubKeys, minRequired) {
        return new Promise(async (resolve, reject) => {
            let co_owners = pubKeys.map(p => floCrypto.getFloID(p));
            if (co_owners.includes(null))
                return reject("Invalid public key: " + pubKeys[co_owners.indexOf(null)]);
            let privateKey = await floDapps.user.private;
            let multisig = btcOperator.multiSigAddress(pubKeys, minRequired) //TODO: change to correct function
            if (typeof multisig !== 'object')
                return reject("Unable to create multisig address");
            let content = {
                type: TYPE_BTC_MULTISIG,
                address: multisig.address, //TODO: maybe encrypt the address
                redeemScript: multisig.redeemScript
            };
            console.debug(content.address, content.redeemScript);
            debugger;
            floBlockchainAPI.writeDataMultiple([privateKey], JSON.stringify({
                [floGlobals.application]: content
            }), co_owners).then(txid => {
                console.info(txid);
                let key = TYPE_BTC_MULTISIG + "|" + txid.substr(0, 16);
                compactIDB.writeData("flodata", {
                    time: null, //time will be overwritten when confirmed on blockchain
                    txid: txid,
                    data: content
                }, key);
                resolve(multisig.address);
            }).catch(error => reject(error))
        })
    }

    MultiSig.listAddress = function () {
        return new Promise((resolve, reject) => {
            let options = {
                lowerKey: `${TYPE_BTC_MULTISIG}|`,
                upperKey: `${TYPE_BTC_MULTISIG}||`
            }
            compactIDB.searchData("flodata", options).then(result => {
                let multsigs = {};
                for (let i in result) {
                    let addr = result[i].data.address,
                        addr_type = btcOperator.validateAddress(addr);
                    let decode = (addr_type == "multisig" ?
                        coinjs.script().decodeRedeemScript : coinjs.script().decodeRedeemScriptBech32)
                        (result[i].data.redeemScript);
                    if (addr_type != "multisig" && addr_type != "multisigBech32")
                        console.warn("Invalid multi-sig address:", addr);
                    else if (!decode || decode.address !== addr)
                        console.warn("Invalid redeem-script:", addr);
                    else if (decode.type !== "multisig__")
                        console.warn("Redeem-script is not of a multisig:", addr);
                    else if (!decode.pubkeys.includes(user.public.toLowerCase()) && !decode.pubkeys.includes(user.public.toUpperCase()))
                        console.warn("User is not a part of this multisig:", addr);
                    else if (decode.pubkeys.length < decode.signaturesRequired)
                        console.warn("Invalid multisig (required is greater than users):", addr);
                    else
                        multsigs[addr] = {
                            redeemScript: decode.redeemscript,
                            pubKeys: decode.pubkeys,
                            minRequired: decode.signaturesRequired,
                            time: result[i].time,
                            txid: result[i].txid
                        }
                }
                resolve(multsigs);
            }).catch(error => reject(error))
        })
    }

    //create multisig tx for BTC
    MultiSig.createTx_BTC = function (address, redeemScript, receivers, amounts, fee = null, options = {}) {
        return new Promise(async (resolve, reject) => {
            let addr_type = btcOperator.validateAddress(address);
            if (addr_type != "multisig" && addr_type != "multisigBech32")
                return reject("Sender address is not a multisig");
            let decode = (addr_type == "multisig" ?
                coinjs.script().decodeRedeemScript : coinjs.script().decodeRedeemScriptBech32)(redeemScript);
            if (!decode || decode.address !== address || decode.type !== "multisig__")
                return reject("Invalid redeem-script");
            else if (!decode.pubkeys.includes(user.public.toLowerCase()) && !decode.pubkeys.includes(user.public.toUpperCase()))
                return reject("User is not a part of this multisig");
            else if (decode.pubkeys.length < decode.signaturesRequired)
                return reject("Invalid multisig (required is greater than users)");
            let co_owners = decode.pubkeys.map(p => floCrypto.getFloID(p));
            let privateKey = await floDapps.user.private;
            btcOperator.createMultiSigTx(address, redeemScript, receivers, amounts, fee, options).then(({ tx_hex }) => {
                tx_hex = btcOperator.signTx(tx_hex, privateKey);
                createPipeline(TYPE_BTC_MULTISIG, co_owners, 32, decode.pubkeys).then(pipeline => {
                    let message = encrypt(tx_hex, pipeline.eKey);
                    sendRaw(message, pipeline.id, "TRANSACTION", false)
                        .then(result => resolve(pipeline.id))
                        .catch(error => reject(error))
                }).catch(error => reject(error))
            }).catch(error => reject(error))
        })
    }

    //sign multisig tx for BTC
    MultiSig.signTx_BTC = function (pipeID) {
        return new Promise((resolve, reject) => {
            if (_loaded.pipeline[pipeID].model !== TYPE_BTC_MULTISIG)
                return reject('Incorrect pipeline model. Only works for BTC-multisig');
            if (_loaded.pipeline[pipeID].disabled)
                return reject("Pipeline is already closed");
            getChat(pipeID).then(async result => {
                let pipeline = _loaded.pipeline[pipeID],
                    tx_hex_latest = Object.keys(result).sort().map(i => result[i].tx_hex).filter(x => x).pop();
                let privateKey = await floDapps.user.private;
                let tx_hex_signed = btcOperator.signTx(tx_hex_latest, privateKey);
                let message = encrypt(tx_hex_signed, pipeline.eKey);
                sendRaw(message, pipeline.id, "TRANSACTION", false).then(result => {
                    if (!btcOperator.checkSigned(tx_hex_signed))
                        return resolve({
                            tx_hex: tx_hex_signed
                        });
                    debugger;
                    btcOperator.broadcastTx(tx_hex_signed).then(txid => {
                        console.debug(txid);
                        sendRaw(encrypt(txid, pipeline.eKey), pipeline.id, "BROADCAST", false)
                            .then(result => resolve({
                                tx_hex: tx_hex_signed,
                                txid: txid
                            })).catch(error => reject(error))
                    }).catch(error => reject(error))
                }).catch(error => reject(error))
            }).catch(error => console.error(error))
        })
    }

    //create multisig tx for FLO
    MultiSig.createTx_FLO = function (address, redeemScript, receivers, amounts, floData = '', options = {}) {
        return new Promise(async (resolve, reject) => {
            if (!floCrypto.validateFloID(address)) { //not a flo multisig, but maybe btc multisig address
                let addr_type = btcOperator.validateAddress(address);
                if (addr_type != "multisig" && addr_type != "multisigBech32")
                    return reject("Sender address is not a multisig");
                address = floCrypto.toMultisigFloID(address);
            }
            let decode = floCrypto.decodeRedeemScript(redeemScript);
            if (!decode || decode.address !== address)
                return reject("Invalid redeem-script");
            else if (!decode.pubkeys.includes(user.public.toLowerCase()) && !decode.pubkeys.includes(user.public.toUpperCase()))
                return reject("User is not a part of this multisig");
            else if (decode.pubkeys.length < decode.required)
                return reject("Invalid multisig (required is greater than users)");
            let co_owners = decode.pubkeys.map(p => floCrypto.getFloID(p));
            let privateKey = await floDapps.user.private;
            floBlockchainAPI.createMultisigTx(redeemScript, receivers, amounts, floData).then(tx_hex => {
                tx_hex = floBlockchainAPI.signTx(tx_hex, privateKey);
                createPipeline(TYPE_FLO_MULTISIG, co_owners, 32, decode.pubkeys).then(pipeline => {
                    let message = encrypt(tx_hex, pipeline.eKey);
                    sendRaw(message, pipeline.id, "TRANSACTION", false)
                        .then(result => resolve(pipeline.id))
                        .catch(error => reject(error))
                }).catch(error => reject(error))
            }).catch(error => reject(error))
        })
    }

    //sign multisig tx for FLO
    MultiSig.signTx_FLO = function (pipeID) {
        return new Promise((resolve, reject) => {
            if (_loaded.pipeline[pipeID].model !== TYPE_FLO_MULTISIG)
                return reject('Incorrect pipeline model. Only works for FLO-multisig');
            if (_loaded.pipeline[pipeID].disabled)
                return reject("Pipeline is already closed");
            getChat(pipeID).then(async result => {
                let pipeline = _loaded.pipeline[pipeID],
                    tx_hex_latest = Object.keys(result).sort().map(i => result[i].tx_hex).filter(x => x).pop();
                let privateKey = await floDapps.user.private;
                let tx_hex_signed = floBlockchainAPI.signTx(tx_hex_latest, privateKey);
                let message = encrypt(tx_hex_signed, pipeline.eKey);
                sendRaw(message, pipeline.id, "TRANSACTION", false).then(result => {
                    if (!floBlockchainAPI.checkSigned(tx_hex_signed))
                        return resolve({ tx_hex: tx_hex_signed });
                    debugger;
                    floBlockchainAPI.broadcastTx(tx_hex_signed).then(txid => {
                        console.debug(txid);
                        sendRaw(encrypt(txid, pipeline.eKey), pipeline.id, "BROADCAST", false)
                            .then(result => resolve({
                                tx_hex: tx_hex_signed,
                                txid: txid
                            })).catch(error => reject(error))
                    }).catch(error => reject(error))
                }).catch(error => reject(error))
            }).catch(error => console.error(error))
        })
    }

    //Pipelines
    const createPipeline = rmMessenger.createPipeline = function (model, members, ekeySize = 16, pubkeys = null) {
        return new Promise((resolve, reject) => {
            //optional pubkey parameter
            if (pubkeys !== null) {
                if (!Array.isArray(pubkeys))
                    return reject('pubkeys must be an array (if passed)');
                else if (pubkeys.length !== members.length)
                    return reject('pubkey length doesnot match members length');
            }

            //validate members
            let imem1 = [],
                imem2 = []
            members.forEach((m, i) => {
                if (!floCrypto.validateAddr(m))
                    imem1.push(m);
                else if (!(m in floGlobals.pubKeys) && !floCrypto.isSameAddr(user.id, m)) {
                    if (pubkeys !== null && floCrypto.verifyPubKey(pubkeys[i], m))
                        floGlobals.pubKeys[m] = pubkeys[i];
                    else
                        imem2.push(m);
                }
            });
            if (imem1.length)
                return reject(`Invalid Members(floIDs): ${imem1}`);
            else if (imem2.length)
                return reject(`Invalid Members (pubKey not available): ${imem2}`);
            //create pipeline info
            const id = floCrypto.tmpID;
            let pipeline = {
                id,
                model,
                members
            }
            if (ekeySize)
                pipeline.eKey = floCrypto.randString(ekeySize);
            //send pipeline info to members
            let pipelineInfo = JSON.stringify(pipeline);
            let promises = members.filter(m => !floCrypto.isSameAddr(m, user.id)).map(m => sendRaw(pipelineInfo, m, "CREATE_PIPELINE", true));
            Promise.allSettled(promises).then(results => {
                console.debug(results.filter(r => r.status === "rejected").map(r => r.reason));
                _loaded.pipeline[pipeline.id] = Object.assign({}, pipeline);
                if (pipeline.eKey)
                    pipeline.eKey = encrypt(pipeline.eKey);
                compactIDB.addData("pipeline", pipeline, pipeline.id).then(result => {
                    requestPipelineInbox(pipeline.id, pipeline.model);
                    resolve(_loaded.pipeline[pipeline.id])
                }).catch(error => reject(error))
            })
        })
    }

    function requestPipelineInbox(pipeID, model, _async = true) {
        if (pipeConnID[pipeID]) { //close existing request connection (if any)
            floCloudAPI.closeRequest(pipeConnID[pipeID]);
            delete pipeConnID[pipeID];
        }

        let parseData = processData.pipeline[model](pipeID);
        let callbackFn = function (dataSet, error) {
            if (error)
                return console.error(error);
            console.info(dataSet)
            let newInbox = {
                messages: {}
            }
            for (let vc in dataSet) {
                if (pipeID !== dataSet[vc].receiverID)
                    continue;
                try {
                    parseData(dataSet[vc], newInbox);
                    if (!floCrypto.isSameAddr(dataSet[vc].senderID, user.id))
                        addMark(pipeID, "unread")
                    if (!_loaded.appendix[`lastReceived_${pipeID}`] ||
                        _loaded.appendix[`lastReceived_${pipeID}`] < vc)
                        _loaded.appendix[`lastReceived_${pipeID}`] = vc;
                } catch (error) {
                    console.log(error)
                }
            }
            compactIDB.writeData("appendix", _loaded.appendix[`lastReceived_${pipeID}`], `lastReceived_${pipeID}`);
            console.debug(newInbox);
            UI.pipeline(model, newInbox);
        }

        let fn = floCloudAPI.requestApplicationData(null, {
            receiverID: pipeID,
            lowerVectorClock: _loaded.appendix[`lastReceived_${pipeID}`] + 1,
            callback: callbackFn
        });
        if (_async) {
            fn.then(conn_id => pipeConnID[pipeID] = conn_id)
                .catch(error => console.error(`request-pipeline(${pipeID}):`, error))
        } else {
            return new Promise((resolve, reject) => {
                fn.then(conn_id => {
                    pipeConnID[pipeID] = conn_id;
                    resolve(`Connected to pipeline ${pipeID}`);
                }).catch(error => reject(error))
            });
        }
    }

    const disablePipeline = rmMessenger.disablePipeline = function (pipeID) {
        console.debug(JSON.stringify(pipeConnID), pipeConnID[pipeID])
        return new Promise((resolve, reject) => {
            if (!_loaded.pipeline[pipeID])
                return reject("Pipeline not found");
            if (_loaded.pipeline[pipeID].disabled)
                return resolve("Pipeline already diabled");
            _loaded.pipeline[pipeID].disabled = true;
            let pipelineInfo = Object.assign({}, _loaded.pipeline[pipeID]);
            pipelineInfo.eKey = encrypt(pipelineInfo.eKey)
            compactIDB.writeData("pipeline", pipelineInfo, pipeID).then(result => {
                floCloudAPI.closeRequest(pipeConnID[pipeID]);
                delete pipeConnID[pipeID];
                resolve("Pipeline diabled");
            }).catch(error => reject(error))
        })
    }

    rmMessenger.sendPipelineMessage = function (message, pipeID) {
        return new Promise((resolve, reject) => {
            let k = _loaded.pipeline[pipeID].eKey;
            if (k) message = encrypt(message, k);
            sendRaw(message, pipeID, "MESSAGE", false)
                .then(result => resolve(`${pipeID}: ${message}`))
                .catch(error => reject(error))
        })
    }

    rmMessenger.editFee = function (tx_id, new_fee, private_keys, change_only = true) {
        return new Promise(async (resolve, reject) => {
            //1. FIND REDEEMSCRIPT
            //2. CHANGE OUTPUT VALUES
            //3. Call modified version of MultiSig.createTx_BTC_1 where the input taken is txhex rather than senders etc 
            //4. MultiSig.createTx_BTC_1 will in turn call btcOperator.createMultiSigTx_1(tx_hex). Check that Redeemscript information is present
            var address;

            if (!Array.isArray(private_keys))
                private_keys = [private_keys];
            try {
                let tx, tx_parsed;
                tx = await btcOperator.tx_fetch_for_editing(tx_id)
                tx_parsed = await btcOperator.parseTransaction(tx)
                if (tx_parsed.fee >= new_fee)
                    return reject("Fees can only be increased");

                //editable addresses in output values (for fee increase)
                var edit_output_address = new Set();
                if (change_only === true) //allow only change values (ie, sender address) to be edited to inc fee
                    tx_parsed.inputs.forEach(inp => edit_output_address.add(inp.address));
                else if (change_only === false) //allow all output values to be edited
                    tx_parsed.outputs.forEach(out => edit_output_address.add(out.address));
                else if (typeof change_only == 'string') // allow only given receiver id output to be edited
                    edit_output_address.add(change_only);
                else if (Array.isArray(change_only)) //allow only given set of receiver id outputs to be edited
                    change_only.forEach(id => edit_output_address.add(id));

                //edit output values to increase fee
                let inc_fee = btcOperator.util.BTC_to_Sat(new_fee - tx_parsed.fee);
                if (inc_fee < MIN_FEE_UPDATE)
                    return reject(`Insufficient additional fee. Minimum increment: ${MIN_FEE_UPDATE}`);
                for (let i = tx.outs.length - 1; i >= 0 && inc_fee > 0; i--) //reduce in reverse order
                    if (edit_output_address.has(tx_parsed.outputs[i].address)) {
                        let current_value = tx.outs[i].value;
                        if (current_value instanceof BigInteger) //convert BigInteger class to inv value
                            current_value = current_value.intValue();
                        //edit the value as required
                        if (current_value > inc_fee) {
                            tx.outs[i].value = current_value - inc_fee;
                            inc_fee = 0;
                        } else {
                            inc_fee -= current_value;
                            tx.outs[i].value = 0;
                        }
                    }
                if (inc_fee > 0) {
                    let max_possible_fee = btcOperator.util.BTC_to_Sat(new_fee) - inc_fee; //in satoshi
                    return reject(`Insufficient output values to increase fee. Maximum fee possible: ${btcOperator.util.Sat_to_BTC(max_possible_fee)}`);
                }
                tx.outs = tx.outs.filter(o => o.value >= DUST_AMT); //remove all output with value less than DUST amount

                //remove existing signatures and reset the scripts
                let wif_keys = [];
                let witness_position = 0;
                for (let i in tx.ins) {
                    var addr = tx_parsed.inputs[i].address,
                        value = btcOperator.util.BTC_to_Sat(tx_parsed.inputs[i].value);
                    let addr_decode = coinjs.addressDecode(addr);
                    //find the correct key for addr
                    var privKey = private_keys.find(pk => verifyKey(addr, pk));
                    if (!privKey)
                        return reject(`Private key missing for ${addr}`);
                    //find redeemScript (if any)
                    const rs = _redeemScript(addr, privKey);
                    rs === false ? wif_keys.unshift(privKey) : wif_keys.push(privKey); //sorting private-keys (wif)
                    //reset the script for re-signing
                    var script;
                    if (!rs || !rs.length) {
                        //legacy script (derive from address)
                        let s = coinjs.script();
                        s.writeOp(118); //OP_DUP
                        s.writeOp(169); //OP_HASH160
                        s.writeBytes(addr_decode.bytes);
                        s.writeOp(136); //OP_EQUALVERIFY
                        s.writeOp(172); //OP_CHECKSIG
                        script = Crypto.util.bytesToHex(s.buffer);
                    } else if (((rs.match(/^00/) && rs.length == 44)) || (rs.length == 40 && rs.match(/^[a-f0-9]+$/gi))) {
                        //redeemScript for segwit/bech32 
                        if (addr_decode == "bech32") { witness_position = witness_position + 1; } //bech32 has witness
                        let s = coinjs.script();
                        s.writeBytes(Crypto.util.hexToBytes(rs));
                        s.writeOp(0);
                        s.writeBytes(coinjs.numToBytes(value.toFixed(0), 8));
                        script = Crypto.util.bytesToHex(s.buffer);
                    } else if (addr_decode.type === 'multisigBech32') {
                        //redeemScript multisig (bech32)
                        address = addr;
                        var rs_array = [];
                        rs_array = btcOperator.extractLastHexStrings(tx.witness);
                        let redeemScript = rs_array[witness_position];
                        witness_position = witness_position + 1; //this permits mixing witness and non witness based inputs

                        let s = coinjs.script();
                        s.writeBytes(Crypto.util.hexToBytes(redeemScript));
                        s.writeOp(0);
                        s.writeBytes(coinjs.numToBytes(value.toFixed(0), 8));
                        script = Crypto.util.bytesToHex(s.buffer);
                    } else //redeemScript for multisig (segwit)
                        script = rs;
                    tx.ins[i].script = coinjs.script(script);
                }
                tx.witness = false; //remove all witness signatures
                console.debug("Unsigned:", tx.serialize());
                //re-sign the transaction
                new Set(wif_keys).forEach(key => tx.sign(key, 1 /*sighashtype*/)); //Sign the tx using private key WIF
                let tx_hex = tx.serialize();

                //Call MultiSig.createTx_BTC_editFee(tx.serialize());
                let addr_type = btcOperator.validateAddress(address);
                if (addr_type != "multisig" && addr_type != "multisigBech32")
                    return reject("Sender address is not a multisig");
                let decode = (addr_type == "multisig" ?
                    coinjs.script().decodeRedeemScript : coinjs.script().decodeRedeemScriptBech32)(redeemScript);
                if (!decode || decode.address !== address || decode.type !== "multisig__")
                    return reject("Invalid redeem-script");
                else if (!decode.pubkeys.includes(user.public.toLowerCase()) && !decode.pubkeys.includes(user.public.toUpperCase()))
                    return reject("User is not a part of this multisig");
                else if (decode.pubkeys.length < decode.signaturesRequired)
                    return reject("Invalid multisig (required is greater than users)");
                let co_owners = decode.pubkeys.map(p => floCrypto.getFloID(p));
                //let privateKey = await floDapps.user.private;

                //  let tx_hex = btcOperator.signTx_1(tx, privateKey);

                createPipeline(TYPE_BTC_MULTISIG, co_owners, 32, decode.pubkeys).then(pipeline => {
                    let message = encrypt(tx_hex, pipeline.eKey);
                    sendRaw(message, pipeline.id, "TRANSACTION", false)
                        .then(result => resolve(pipeline.id))
                        .catch(error => reject(error)) //SENDRAW
                }).catch(error => reject(error)) //CREATE PIPELINE
                // resolve(tx.serialize()); //CHECK THIS -- NOT NEEDED
            } catch (error) {
                reject(error);
            }
        })
    }


    processData.pipeline = {};

    //pipeline model for btc multisig
    processData.pipeline[TYPE_BTC_MULTISIG] = function (pipeID) {
        return (unparsed, newInbox) => {
            if (!_loaded.pipeline[pipeID].members.includes(floCrypto.toFloID(unparsed.senderID)))
                return;
            let data = {
                time: unparsed.time,
                sender: unparsed.senderID,
                pipeID: unparsed.receiverID
            }
            let vc = unparsed.vectorClock,
                k = _loaded.pipeline[pipeID].eKey;
            unparsed.message = decrypt(unparsed.message, k)
            //store the pubKey if not stored already
            floDapps.storePubKey(unparsed.senderID, unparsed.pubKey);
            data.type = unparsed.type;
            switch (unparsed.type) {
                case "TRANSACTION": {
                    data.tx_hex = unparsed.message;
                    break;
                }
                case "BROADCAST": {
                    data.txid = unparsed.message;
                    //the following check is done on parallel (in background) instead of sync
                    btcOperator.getTx.hex(data.txid).then(tx_hex_final => {
                        getChat(pipeID).then(result => {
                            let tx_hex_inital = Object.keys(result).sort().map(i => result[i].tx_hex).filter(x => x).shift();
                            if (btcOperator.checkIfSameTx(tx_hex_inital, tx_hex_final))
                                disablePipeline(pipeID);
                        }).catch(error => console.error(error))
                    }).catch(error => console.error(error))
                    break;
                }
                case "MESSAGE": {
                    data.message = encrypt(unparsed.message);
                    break;
                }
            }
            compactIDB.addData("messages", Object.assign({}, data), `${pipeID}|${vc}`);
            if (data.message)
                data.message = decrypt(data.message);
            newInbox.messages[vc] = data;
        }
    }

    //pipeline model for flo multisig
    processData.pipeline[TYPE_FLO_MULTISIG] = function (pipeID) {
        return (unparsed, newInbox) => {
            if (!_loaded.pipeline[pipeID].members.includes(floCrypto.toFloID(unparsed.senderID)))
                return;
            let data = {
                time: unparsed.time,
                sender: unparsed.senderID,
                pipeID: unparsed.receiverID
            }
            let vc = unparsed.vectorClock,
                k = _loaded.pipeline[pipeID].eKey;
            unparsed.message = decrypt(unparsed.message, k)
            //store the pubKey if not stored already
            floDapps.storePubKey(unparsed.senderID, unparsed.pubKey);
            data.type = unparsed.type;
            switch (unparsed.type) {
                case "TRANSACTION": {
                    data.tx_hex = unparsed.message;
                    break;
                }
                case "BROADCAST": {
                    data.txid = unparsed.message;
                    //the following check is done on parallel (in background) instead of sync
                    getChat(pipeID).then(result => {
                        var tx_hex_list = Object.keys(result).sort().map(i => result[i].tx_hex).filter(x => x);
                        let tx_hex_inital = tx_hex_list[0],
                            tx_hex_final = tx_hex_list.pop();
                        if (floBlockchainAPI.checkIfSameTx(tx_hex_inital, tx_hex_final) &&
                            floBlockchainAPI.transactionID(tx_hex_final) == data.txid) //compare the txHex and txid
                            disablePipeline(pipeID);
                    }).catch(error => console.error(error))
                    break;
                }
                case "MESSAGE": {
                    data.message = encrypt(unparsed.message);
                    break;
                }
            }
            compactIDB.addData("messages", Object.assign({}, data), `${pipeID}|${vc}`);
            if (data.message)
                data.message = decrypt(data.message);
            newInbox.messages[vc] = data;
        }
    }

})();
