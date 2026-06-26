(function (EXPORTS) { //btcOperator v1.2.10
    /* BTC Crypto and API Operator */
    const btcOperator = EXPORTS;
    const SATOSHI_IN_BTC = 1e8;

    const util = btcOperator.util = {};

    util.Sat_to_BTC = value => parseFloat((value / SATOSHI_IN_BTC).toFixed(8));
    util.BTC_to_Sat = value => parseInt(value * SATOSHI_IN_BTC);

    const checkIfTor = btcOperator.checkIfTor = () => {
        return fetch('https://check.torproject.org/api/ip')
            .then(res => res.json())
            .then(res => {
                return res.IsTor
            }).catch(e => {
                console.error(e)
                return false
            })
    }
    let isTor = false;
    checkIfTor().then(result => isTor = result);

    async function post(url, data, { asText = false } = {}) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                mode: 'no-cors',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            if (response.ok) {
                return asText ? await response.text() : await response.json()
            } else {
                throw response
            }
        } catch (e) {
            throw e
        }
    }

    // NOTE: some APIs may not support all functions properly hence they are omitted
    const APIs = btcOperator.APIs = [
        {
            url: 'https://api.blockcypher.com/v1/btc/main/',
            name: 'Blockcypher',
            balance({ addr }) {
                return fetch_api(`addrs/${addr}/balance`, { url: this.url })
                    .then(result => util.Sat_to_BTC(result.balance))
            },
            async block({ id }) {
                try {
                    let block = await fetch_api(`blocks/${id}`, { url: this.url })
                    return formatBlock(block)
                } catch (e) {
                    console.log(e)
                }
            },
            async broadcast({ rawTxHex, url }) {
                try {
                    const result = await post(`${url || this.url}pushtx`, { tx: rawTxHex })
                    return result.hash
                } catch (e) {
                    throw e
                }
            }
        },
        {
            url: 'https://blockstream.info/api/',
            name: 'Blockstream',
            hasOnion: true,
            onionUrl: `http://explorerzydxu5ecjrkwceayqybizmpjjznk5izmitf2modhcusuqlid.onion/api/`,
            balance({ addr, url }) {
                return fetch_api(`address/${addr}/utxo`, { url: url || this.url })
                    .then(result => {
                        const balance = result.reduce((t, u) => t + u.value, 0)
                        return util.Sat_to_BTC(balance)
                    })
            },
            latestBlock() {
                return fetch_api(`blocks/tip/height`, { url: this.url })
            },
            tx({ txid, url }) {
                return fetch_api(`tx/${txid}`, { url: url || this.url })
                    .then(result => formatTx(result))
            },
            txHex({ txid, url }) {
                return fetch_api(`tx/${txid}/hex`, { url: url || this.url, asText: true })
            },
            txs({ addr, url, ...args }) {
                let queryParams = Object.entries(args).map(([key, value]) => `${key}=${value}`).join('&')
                if (queryParams)
                    queryParams = '?' + queryParams
                return fetch_api(`address/${addr}/txs${queryParams}`, { url: url || this.url })
            },
            async block({ id, url }) {
                // if id is hex string then it is block hash
                try {
                    let blockHash = id
                    if (!/^[0-9a-f]{64}$/i.test(id))
                        blockHash = await fetch_api(`block-height/${id}`, { url: url || this.url, asText: true })
                    const block = await fetch_api(`block/${blockHash}`, { url: url || this.url })
                    return formatBlock(block)
                } catch (e) {
                    throw e
                }
            },
            async broadcast({ rawTxHex, url }) {
                return post(`${url || this.url}tx`, { tx: rawTxHex }, { asText: true })
            }
        },
        {
            url: 'https://mempool.space/api/',
            name: 'Mempool',
            balance({ addr }) {
                return fetch_api(`address/${addr}`, { url: this.url })
                    .then(result => util.Sat_to_BTC(result.chain_stats.funded_txo_sum - result.chain_stats.spent_txo_sum))
            },
            latestBlock() {
                return fetch_api(`blocks/tip/height`, { url: this.url })
            },
            tx({ txid }) {
                return fetch_api(`tx/${txid}`, { url: this.url })
                    .then(result => formatTx(result))

            },
            txHex({ txid }) {
                return fetch_api(`tx/${txid}/hex`, { url: this.url, asText: true })
            },
            txs({ addr, ...args }) {
                let queryParams = Object.entries(args).map(([key, value]) => `${key}=${value}`).join('&')
                if (queryParams)
                    queryParams = '?' + queryParams
                return fetch_api(`address/${addr}/txs${queryParams}`, { url: this.url })
            },
            async block({ id }) {
                // if id is hex string then it is block hash
                try {
                    let blockHash = id
                    if (!/^[0-9a-f]{64}$/i.test(id))
                        blockHash = await fetch_api(`block-height/${id}`, { url: this.url, asText: true })
                    const block = await fetch_api(`block/${blockHash}`, { url: this.url })
                    return formatBlock(block)
                } catch (e) {
                    throw e
                }
            },
            async broadcast({ rawTxHex, url }) {
                return post(`${url || this.url}tx`, { tx: rawTxHex }, { asText: true })
            }
        },
        {
            url: 'https://blockchain.info/',
            name: 'Blockchain',
            balance({ addr }) {
                return fetch_api(`q/addressbalance/${addr}`, { url: this.url })
                    .then(result => util.Sat_to_BTC(result))
            },
            unspent({ addr, allowUnconfirmedUtxos = false }) {
                return fetch_api(`unspent?active=${addr}`, { url: this.url })
                    .then(result => formatUtxos(result.unspent_outputs, allowUnconfirmedUtxos))
            },
            tx({ txid }) {
                return fetch_api(`rawtx/${txid}`, { url: this.url })
                    .then(result => formatTx(result))
            },
            txHex({ txid }) {
                return fetch_api(`rawtx/${txid}?format=hex`, { url: this.url, asText: true })
            },
            txs({ addr, ...args }) {
                let queryParams = Object.entries(args).map(([key, value]) => `${key}=${value}`).join('&')
                if (queryParams)
                    queryParams = '?' + queryParams
                return fetch_api(`rawaddr/${addr}${queryParams}`, { url: this.url })
                    .then(result => result.txs)
            },
            latestBlock() {
                return fetch_api(`q/getblockcount`, { url: this.url })
            },
            async block({ id }) {
                try {
                    let block
                    // if id is hex string then it is block hash
                    if (/^[0-9a-f]{64}$/i.test(id))
                        block = await fetch_api(`rawblock/${id}`, { url: this.url })
                    else {
                        const result = await fetch_api(`block-height/${id}?format=json`, { url: this.url })
                        block = result.blocks[0]
                    }
                    return formatBlock(block)
                } catch (e) {
                    throw e
                }
            },
            async blockTxs({ id }) {
                try {
                    let block
                    // if id is hex string then it is block hash
                    if (/^[0-9a-f]{64}$/i.test(id))
                        block = await fetch_api(`rawblock/${id}`, { url: this.url })
                    else {
                        const result = await fetch_api(`block-height/${id}?format=json`, { url: this.url })
                        block = result.blocks[0]
                    }
                    return block.tx
                } catch (e) {

                }
            }
        },
        {
            url: 'https://coinb.in/api/?uid=1&key=12345678901234567890123456789012&setmodule=bitcoin&request=sendrawtransaction',
            name: 'Coinb.in',
            broadcast({ rawTxHex }) {
                return new Promise((resolve, reject) => {
                    fetch(this.url, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        body: "rawtx=" + rawTxHex
                    }).then(response => {
                        console.log(response)
                        response.text().then(resultText => {
                            let r = resultText.match(/<result>.*<\/result>/);
                            if (!r)
                                reject(resultText);
                            else {
                                r = r.pop().replace('<result>', '').replace('</result>', '');
                                if (r == '1') {
                                    let txid = resultText.match(/<txid>.*<\/txid>/).pop().replace('<txid>', '').replace('</txid>', '');
                                    resolve(txid);
                                } else if (r == '0') {
                                    let error
                                    if (resultText.includes('<message>')) {
                                        error = resultText.match(/<message>.*<\/message>/).pop().replace('<message>', '').replace('</message>', '');
                                    } else {
                                        error = resultText.match(/<response>.*<\/response>/).pop().replace('<response>', '').replace('</response>', '');
                                    }
                                    reject(decodeURIComponent(error.replace(/\+/g, " ")));
                                } else reject(resultText);
                            }
                        }).catch(error => reject(error))
                    }).catch(error => reject(error))
                });
            }
        }
    ]

    btcOperator.util.format = {} // functions to homogenize API results
    const formatBlock = btcOperator.util.format.block = async (block) => {
        try {
            const { height, hash, id, time, timestamp, mrkl_root, merkle_root, prev_block, next_block, size } = block;
            const details = {
                height,
                hash: hash || id,
                time: (time || timestamp) * 1000,
                merkle_root: merkle_root || mrkl_root,
                size,
            }
            if (prev_block)
                details.prev_block = prev_block
            if (next_block)
                details.next_block = next_block[0]
            return details
        } catch (e) {
            throw e
        }
    }
    const formatUtxos = btcOperator.util.format.utxos = async (utxos, allowUnconfirmedUtxos = false) => {
        try {
            if (!allowUnconfirmedUtxos && !utxos || !Array.isArray(utxos))
                throw {
                    message: "No utxos found",
                    code: 1000 //error code for when issue is not from API but situational (like no utxos found) 
                }
            return utxos.map(utxo => {
                const { tx_hash, tx_hash_big_endian, txid, tx_output_n, vout, value, script, confirmations, status: { confirmed } = {} } = utxo;
                return {
                    confirmations: confirmations || confirmed,
                    tx_hash_big_endian: tx_hash_big_endian || tx_hash || txid,
                    tx_output_n: tx_output_n || vout,
                    value,
                    script
                }
            })
        } catch (e) {
            throw e
        }
    }

    const formatTx = btcOperator.util.format.tx = async (tx) => {
        try {
            let { txid, hash, time, block_height, fee, fees, received,
                confirmed, size, double_spend, block_hash, confirmations,
                status: { block_height: statusBlockHeight, block_hash: statusBlockHash, block_time } = {}
            } = tx;
            if ((block_height || statusBlockHeight) && confirmations === undefined || confirmations === null) {
                const latestBlock = await multiApi('latestBlock');
                confirmations = latestBlock - (block_height || statusBlockHeight);
            }
            const inputs = tx.vin || tx.inputs;
            const outputs = tx.vout || tx.outputs || tx.out;
            return {
                hash: hash || txid,
                size: size,
                fee: fee || fees,
                double_spend,
                time: (time * 1000) || new Date(confirmed || received).getTime() || block_time * 1000 || Date.now(),
                block_height: block_height || statusBlockHeight,
                block_hash: block_hash || statusBlockHash,
                confirmations,
                inputs: inputs.map(input => {
                    return {
                        index: input.n || input.output_index || input.vout,
                        prev_out: {
                            addr: input.prev_out?.addr || input.addresses?.[0] || input.prev_out?.address || input.addr || input.prevout.scriptpubkey_address,
                            value: input.prev_out?.value || input.output_value || input.prevout.value,
                        },
                    }
                }),
                out: outputs.map(output => {
                    return {
                        addr: output.scriptpubkey_address || output.addresses?.[0] || output.scriptpubkey_address || output.addr,
                        value: output.value || output.scriptpubkey_value,
                    }
                })
            }
        } catch (e) {
            throw e
        }
    }

    const multiApi = btcOperator.multiApi = async (fnName, { index = 0, ...args } = {}) => {
        try {
            let triedOnion = false;
            while (index < APIs.length) {
                if (!APIs[index][fnName] || (APIs[index].coolDownTime && APIs[index].coolDownTime > new Date().getTime())) {
                    index += 1;
                    continue;
                }
                return await APIs[index][fnName](args);
            }
            if (isTor && !triedOnion) {
                triedOnion = true;
                index = 0;
                while (index < APIs.length) {
                    if (!APIs[index].hasOnion || (APIs[index].coolDownTime && APIs[index].coolDownTime > new Date().getTime())) {
                        index += 1;
                        continue;
                    }
                    return await multiApi(fnName, { index: index + 1, ...args, url: APIs[index].onionUrl });
                }
            }
            throw "No API available"
        } catch (error) {
            console.error(error)
            if (index < APIs.length) {
                APIs[index].coolDownTime = new Date().getTime() + 1000 * 60 * 10; // 10 minutes
                return multiApi(fnName, { index: index + 1, ...args });
            }
            throw error;
        }
    };

    function parseTx(tx, addressOfTx) {
        const { txid, hash, time, block_height, inputs, outputs, out, vin, vout, fee, fees, received, confirmed, status: { block_height: statusBlockHeight, block_time } = {} } = tx;
        let parsedTx = {
            txid: hash || txid,
            time: (time * 1000) || new Date(confirmed || received).getTime() || block_time * 1000 || Date.now(),
            block: block_height || statusBlockHeight,
        }
        //sender list
        parsedTx.tx_senders = {};
        (inputs || vin).forEach(i => {
            const address = i.prev_out?.addr || i.addresses?.[0] || i.prev_out?.address || i.addr || i.prevout.scriptpubkey_address;
            const value = i.prev_out?.value || i.output_value || i.value || i.prevout.value;
            if (address in parsedTx.tx_senders)
                parsedTx.tx_senders[address] += value;
            else parsedTx.tx_senders[address] = value;
        });
        parsedTx.tx_input_value = 0;
        for (let senderAddr in parsedTx.tx_senders) {
            let val = parsedTx.tx_senders[senderAddr];
            parsedTx.tx_senders[senderAddr] = util.Sat_to_BTC(val);
            parsedTx.tx_input_value += val;
        }
        parsedTx.tx_input_value = util.Sat_to_BTC(parsedTx.tx_input_value);
        //receiver list
        parsedTx.tx_receivers = {};
        (outputs || out || vout).forEach(o => {
            const address = o.scriptpubkey_address || o.addresses?.[0] || o.scriptpubkey_address || o.addr;
            const value = o.value || o.scriptpubkey_value;
            if (address in parsedTx.tx_receivers)
                parsedTx.tx_receivers[address] += value;
            else parsedTx.tx_receivers[address] = value;
        });
        parsedTx.tx_output_value = 0;
        for (let receiverAddr in parsedTx.tx_receivers) {
            let val = parsedTx.tx_receivers[receiverAddr];
            parsedTx.tx_receivers[receiverAddr] = util.Sat_to_BTC(val);
            parsedTx.tx_output_value += val;
        }
        parsedTx.tx_output_value = util.Sat_to_BTC(parsedTx.tx_output_value);
        // tx fee
        parsedTx.tx_fee = util.Sat_to_BTC(fee || fees || (parsedTx.tx_input_value - parsedTx.tx_output_value));
        //detect tx type (in, out, self)
        if (Object.keys(parsedTx.tx_receivers).length === 1 && Object.keys(parsedTx.tx_senders).length === 1 && Object.keys(parsedTx.tx_senders)[0] === Object.keys(parsedTx.tx_receivers)[0]) {
            parsedTx.type = 'self';
            parsedTx.amount = parsedTx.tx_receivers[addressOfTx];
            parsedTx.address = addressOfTx;
        } else if (addressOfTx in parsedTx.tx_senders && Object.keys(parsedTx.tx_receivers).some(addr => addr !== addressOfTx)) {
            parsedTx.type = 'out';
            parsedTx.receiver = Object.keys(parsedTx.tx_receivers).filter(addr => addr != addressOfTx);
            parsedTx.amount = parsedTx.receiver.reduce((t, addr) => t + parsedTx.tx_receivers[addr], 0) + parsedTx.tx_fee;
        } else {
            parsedTx.type = 'in';
            parsedTx.sender = Object.keys(parsedTx.tx_senders).filter(addr => addr != addressOfTx);
            parsedTx.amount = parsedTx.tx_receivers[addressOfTx];
        }
        return parsedTx;
    }


    const DUST_AMT = 546,
        MIN_FEE_UPDATE = 219;

    const fetch_api = btcOperator.fetch = function (api, { asText = false, url = 'https://blockchain.info/' } = {}) {
        return new Promise((resolve, reject) => {
            console.debug(url + api);
            fetch(url + api).then(response => {
                if (response.ok) {
                    (asText ? response.text() : response.json())
                        .then(result => resolve(result))
                        .catch(error => reject(error))
                } else {
                    response.json()
                        .then(result => reject(result))
                        .catch(error => reject(error))
                }
            }).catch(error => reject(error))
        })
    };

    function get_fee_rate() {
        return new Promise((resolve, reject) => {
            fetch('https://api.blockchain.info/mempool/fees').then(response => {
                if (response.ok)
                    response.json()
                        .then(result => resolve(util.Sat_to_BTC(result.regular)))
                        .catch(error => reject(error));
                else
                    reject(response);
            }).catch(error => reject(error))
        })
    }

    const broadcastTx = btcOperator.broadcastTx = rawTxHex => new Promise((resolve, reject) => {
        console.log('txHex:', rawTxHex)
        return multiApi('broadcast', { rawTxHex })
            .then(result => resolve(result))
            .catch(error => reject(error));
    });

    Object.defineProperties(btcOperator, {
        newKeys: {
            get: () => {
                let r = coinjs.newKeys();
                r.segwitAddress = coinjs.segwitAddress(r.pubkey).address;
                r.bech32Address = coinjs.bech32Address(r.pubkey).address;
                return r;
            }
        },
        pubkey: {
            value: key => key.length >= 66 ? key : (key.length == 64 ? coinjs.newPubkey(key) : coinjs.wif2pubkey(key).pubkey)
        },
        address: {
            value: (key, prefix = undefined) => coinjs.pubkey2address(btcOperator.pubkey(key), prefix)
        },
        segwitAddress: {
            value: key => coinjs.segwitAddress(btcOperator.pubkey(key)).address
        },
        bech32Address: {
            value: key => coinjs.bech32Address(btcOperator.pubkey(key)).address
        },
        bech32mAddress: {
            value: key => segwit_addr.encode("bc", 1, key)
        }
    });

    coinjs.compressed = true;

    const verifyKey = btcOperator.verifyKey = function (addr, key) {
        if (!addr || !key)
            return undefined;
        switch (coinjs.addressDecode(addr).type) {
            case "standard":
                return btcOperator.address(key) === addr;
            case "multisig":
                return btcOperator.segwitAddress(key) === addr;
            case "bech32":
                return btcOperator.bech32Address(key) === addr;
            case "bech32m":
                return btcOperator.bech32mAddress(key) === addr; // Key is a byte array of 32 bytes    
            default:
                return null;
        }
    }

    const validateAddress = btcOperator.validateAddress = function (addr) {
        if (!addr)
            return undefined;
        let type = coinjs.addressDecode(addr).type;
        if (["standard", "multisig", "bech32", "multisigBech32", "bech32m"].includes(type))
            return type;
        else
            return false;
    }

    btcOperator.multiSigAddress = function (pubKeys, minRequired, bech32 = true) {
        if (!Array.isArray(pubKeys))
            throw "pubKeys must be an array of public keys";
        else if (pubKeys.length < minRequired)
            throw "minimum required should be less than the number of pubKeys";
        if (bech32)
            return coinjs.pubkeys2MultisigAddressBech32(pubKeys, minRequired);
        else
            return coinjs.pubkeys2MultisigAddress(pubKeys, minRequired);
    }

    btcOperator.decodeRedeemScript = function (redeemScript, bech32 = true) {
        let script = coinjs.script();
        let decoded = (bech32) ?
            script.decodeRedeemScriptBech32(redeemScript) :
            script.decodeRedeemScript(redeemScript);
        if (!decoded)
            return null;
        return {
            address: decoded.address,
            pubKeys: decoded.pubkeys,
            redeemScript: decoded.redeemscript,
            required: decoded.signaturesRequired
        }

    }

    //convert from one blockchain to another blockchain (target version)
    btcOperator.convert = {};

    btcOperator.convert.wif = function (source_wif, target_version = coinjs.priv) {
        let keyHex = util.decodeLegacy(source_wif).hex;
        if (!keyHex || keyHex.length < 66 || !/01$/.test(keyHex))
            return null;
        else
            return util.encodeLegacy(keyHex, target_version);
    }

    btcOperator.convert.legacy2legacy = function (source_addr, target_version = coinjs.pub) {
        let rawHex = util.decodeLegacy(source_addr).hex;
        if (!rawHex)
            return null;
        else
            return util.encodeLegacy(rawHex, target_version);
    }

    btcOperator.convert.legacy2bech = function (source_addr, target_version = coinjs.bech32.version, target_hrp = coinjs.bech32.hrp) {
        let rawHex = util.decodeLegacy(source_addr).hex;
        if (!rawHex)
            return null;
        else
            return util.encodeBech32(rawHex, target_version, target_hrp);
    }

    btcOperator.convert.bech2bech = function (source_addr, target_version = coinjs.bech32.version, target_hrp = coinjs.bech32.hrp) {
        let rawHex = util.decodeBech32(source_addr).hex;
        if (!rawHex)
            return null;
        else
            return util.encodeBech32(rawHex, target_version, target_hrp);
    }

    btcOperator.convert.bech2legacy = function (source_addr, target_version = coinjs.pub) {
        let rawHex = util.decodeBech32(source_addr).hex;
        if (!rawHex)
            return null;
        else
            return util.encodeLegacy(rawHex, target_version);
    }

    btcOperator.convert.multisig2multisig = function (source_addr, target_version = coinjs.multisig) {
        let rawHex = util.decodeLegacy(source_addr).hex;
        if (!rawHex)
            return null;
        else
            return util.encodeLegacy(rawHex, target_version);
    }

    btcOperator.convert.bech2multisig = function (source_addr, target_version = coinjs.multisig) {
        let rawHex = util.decodeBech32(source_addr).hex;
        if (!rawHex)
            return null;
        else {
            rawHex = Crypto.util.bytesToHex(ripemd160(Crypto.util.hexToBytes(rawHex), { asBytes: true }));
            return util.encodeLegacy(rawHex, target_version);
        }
    }

    util.decodeLegacy = function (source) {
        var decode = coinjs.base58decode(source);
        var raw = decode.slice(0, decode.length - 4),
            checksum = decode.slice(decode.length - 4);
        var hash = Crypto.SHA256(Crypto.SHA256(raw, {
            asBytes: true
        }), {
            asBytes: true
        });
        if (hash[0] != checksum[0] || hash[1] != checksum[1] || hash[2] != checksum[2] || hash[3] != checksum[3])
            return false;
        let version = raw.shift();
        return {
            version: version,
            hex: Crypto.util.bytesToHex(raw)
        }
    }

    util.encodeLegacy = function (hex, version) {
        var bytes = Crypto.util.hexToBytes(hex);
        bytes.unshift(version);
        var hash = Crypto.SHA256(Crypto.SHA256(bytes, {
            asBytes: true
        }), {
            asBytes: true
        });
        var checksum = hash.slice(0, 4);
        return coinjs.base58encode(bytes.concat(checksum));
    }

    util.decodeBech32 = function (source) {
        let decode = coinjs.bech32_decode(source);
        if (!decode)
            return false;
        var raw = decode.data;
        let version = raw.shift();
        raw = coinjs.bech32_convert(raw, 5, 8, false);
        return {
            hrp: decode.hrp,
            version: version,
            hex: Crypto.util.bytesToHex(raw)
        }
    }

    util.encodeBech32 = function (hex, version, hrp) {
        var bytes = Crypto.util.hexToBytes(hex);
        bytes = coinjs.bech32_convert(bytes, 8, 5, true);
        bytes.unshift(version)
        return coinjs.bech32_encode(hrp, bytes);
    }

    //BTC blockchain APIs
    btcOperator.getBalance = addr => new Promise((resolve, reject) => {
        if (!validateAddress(addr))
            return reject("Invalid address");
        multiApi('balance', { addr })
            .then(result => resolve(result))
            .catch(error => reject(error))
    });

    const BASE_TX_SIZE = 12,
        BASE_INPUT_SIZE = 41,
        LEGACY_INPUT_SIZE = 107,
        BECH32_INPUT_SIZE = 27,
        BECH32_MULTISIG_INPUT_SIZE = 35,
        SEGWIT_INPUT_SIZE = 59,
        MULTISIG_INPUT_SIZE_ES = 351,
        BASE_OUTPUT_SIZE = 9,
        LEGACY_OUTPUT_SIZE = 25,
        BECH32_OUTPUT_SIZE = 23,
        BECH32_MULTISIG_OUTPUT_SIZE = 34,
        SEGWIT_OUTPUT_SIZE = 23;
    BECH32M_OUTPUT_SIZE = 35; // Check this later

    function _redeemScript(addr, key) {
        let decode = coinjs.addressDecode(addr);
        switch (decode.type) {
            case "standard":
                return false;
            case "multisig":
                return key ? coinjs.segwitAddress(btcOperator.pubkey(key)).redeemscript : null;
            case "bech32":
                return decode.redeemscript;
            case "'multisigBech32":
                return decode.redeemscript; //Multisig-edit-fee-change1
            case "bech32m":
                return decode.outstring; //Maybe the redeemscript will come when input processing happens for bech32m   
            default:
                return null;
        }
    }
    btcOperator._redeemScript = _redeemScript;

    function _sizePerInput(addr, rs) {
        switch (coinjs.addressDecode(addr).type) {
            case "standard":
                return BASE_INPUT_SIZE + LEGACY_INPUT_SIZE;
            case "bech32":
                return BASE_INPUT_SIZE + BECH32_INPUT_SIZE;
            case "multisigBech32":
                return BASE_INPUT_SIZE + BECH32_MULTISIG_INPUT_SIZE;
            case "multisig":
                switch (coinjs.script().decodeRedeemScript(rs).type) {
                    case "segwit__":
                        return BASE_INPUT_SIZE + SEGWIT_INPUT_SIZE;
                    case "multisig__":
                        return BASE_INPUT_SIZE + MULTISIG_INPUT_SIZE_ES;
                    default:
                        return null;
                };
            default:
                return null;
        }
    }

    function _sizePerOutput(addr) {
        switch (coinjs.addressDecode(addr).type) {
            case "standard":
                return BASE_OUTPUT_SIZE + LEGACY_OUTPUT_SIZE;
            case "bech32":
                return BASE_OUTPUT_SIZE + BECH32_OUTPUT_SIZE;
            case "multisigBech32":
                return BASE_OUTPUT_SIZE + BECH32_MULTISIG_OUTPUT_SIZE;
            case "multisig":
                return BASE_OUTPUT_SIZE + SEGWIT_OUTPUT_SIZE;
            case "bech32m":
                return BASE_OUTPUT_SIZE + BECH32M_OUTPUT_SIZE;
            default:
                return null;
        }
    }

    function validateTxParameters(parameters) {
        let invalids = [];
        //sender-ids
        if (parameters.senders) {
            if (!Array.isArray(parameters.senders))
                parameters.senders = [parameters.senders];
            parameters.senders.forEach(id => !validateAddress(id) ? invalids.push(id) : null);
            if (invalids.length)
                throw "Invalid senders:" + invalids;
        }
        if (parameters.privkeys) {
            if (!Array.isArray(parameters.privkeys))
                parameters.privkeys = [parameters.privkeys];
            if (parameters.senders.length != parameters.privkeys.length)
                throw "Array length for senders and privkeys should be equal";
            parameters.senders.forEach((id, i) => {
                let key = parameters.privkeys[i];
                if (!verifyKey(id, key)) //verify private-key
                    invalids.push(id);
                if (key.length === 64) //convert Hex to WIF if needed
                    parameters.privkeys[i] = coinjs.privkey2wif(key);
            });
            if (invalids.length)
                throw "Invalid private key for address:" + invalids;
        }
        //receiver-ids (and change-id)
        if (!Array.isArray(parameters.receivers))
            parameters.receivers = [parameters.receivers];
        parameters.receivers.forEach(id => !validateAddress(id) ? invalids.push(id) : null);
        if (invalids.length)
            throw "Invalid receivers:" + invalids;
        if (parameters.change_address && !validateAddress(parameters.change_address))
            throw "Invalid change_address:" + parameters.change_address;
        //fee and amounts
        if ((typeof parameters.fee !== "number" || parameters.fee <= 0) && parameters.fee !== null) //fee = null (auto calc)
            throw "Invalid fee:" + parameters.fee;
        if (!Array.isArray(parameters.amounts))
            parameters.amounts = [parameters.amounts];
        if (parameters.receivers.length != parameters.amounts.length)
            throw "Array length for receivers and amounts should be equal";
        parameters.amounts.forEach(a => typeof a !== "number" || a <= 0 ? invalids.push(a) : null);
        if (invalids.length)
            throw "Invalid amounts:" + invalids;
        //return
        return parameters;
    }
    btcOperator.validateTxParameters = validateTxParameters;

    const createTransaction = btcOperator.createTransaction = ({
        senders, redeemScripts, receivers, amounts, fee, change_address,
        fee_from_receiver, allowUnconfirmedUtxos = false, sendingTx = false,
        hasInsufficientBalance = false
    }) => {
        return new Promise((resolve, reject) => {
            let total_amount = parseFloat(amounts.reduce((t, a) => t + a, 0).toFixed(8));
            const tx = coinjs.transaction();
            let output_size = addOutputs(tx, receivers, amounts, change_address);
            addInputs(tx, senders, redeemScripts, total_amount, fee, output_size, fee_from_receiver, allowUnconfirmedUtxos).then(result => {
                if (result.change_amount > 0 && result.change_amount > result.fee) //add change amount if any (ignore dust change)
                    tx.outs[tx.outs.length - 1].value = util.BTC_to_Sat(result.change_amount); //values are in satoshi
                if (fee_from_receiver) { //deduce fee from receivers if fee_from_receiver
                    let fee_remaining = util.BTC_to_Sat(result.fee);
                    for (let i = 0; i < tx.outs.length - 1 && fee_remaining > 0; i++) {
                        if (fee_remaining < tx.outs[i].value) {
                            tx.outs[i].value -= fee_remaining;
                            fee_remaining = 0;
                        } else {
                            fee_remaining -= tx.outs[i].value;
                            tx.outs[i].value = 0;
                        }
                    }
                    if (fee_remaining > 0)
                        return reject("Send amount is less than fee");

                }
                //remove all output with value less than DUST amount
                let filtered_outputs = [], dust_value = 0;
                tx.outs.forEach(o => o.value >= DUST_AMT ? filtered_outputs.push(o) : dust_value += o.value);
                tx.outs = filtered_outputs;
                //update result values
                result.fee += util.Sat_to_BTC(dust_value);
                result.output_size = output_size;
                result.output_amount = total_amount - (fee_from_receiver ? result.fee : 0);
                result.total_size = BASE_TX_SIZE + output_size + result.input_size;
                result.transaction = tx;
                if (sendingTx && result.hasOwnProperty('hasInsufficientBalance') && result.hasInsufficientBalance)
                    reject({
                        message: "Insufficient balance",
                        ...result
                    });
                else
                    resolve(result);
            }).catch(error => reject(error))
        })
    }

    function addInputs(tx, senders, redeemScripts, total_amount, fee, output_size, fee_from_receiver, allowUnconfirmedUtxos = false) {
        return new Promise((resolve, reject) => {
            if (fee !== null) {
                addUTXOs(tx, senders, redeemScripts, fee_from_receiver ? total_amount : total_amount + fee, false, { allowUnconfirmedUtxos }).then(result => {
                    result.fee = fee;
                    resolve(result);
                }).catch(error => reject(error))
            } else {
                get_fee_rate().then(fee_rate => {
                    let net_fee = BASE_TX_SIZE * fee_rate;
                    net_fee += (output_size * fee_rate);
                    (fee_from_receiver ?
                        addUTXOs(tx, senders, redeemScripts, total_amount, false, { allowUnconfirmedUtxos }) :
                        addUTXOs(tx, senders, redeemScripts, total_amount + net_fee, fee_rate, { allowUnconfirmedUtxos })
                    ).then(result => {
                        result.fee = parseFloat((net_fee + (result.input_size * fee_rate)).toFixed(8));
                        result.fee_rate = fee_rate;
                        resolve(result);
                    }).catch(error => reject(error))
                }).catch(error => reject(error))
            }
        })
    }
    btcOperator.addInputs = addInputs;

    function addUTXOs(tx, senders, redeemScripts, required_amount, fee_rate, rec_args = { allowUnconfirmedUtxos: false }) {
        return new Promise((resolve, reject) => {
            required_amount = parseFloat(required_amount.toFixed(8));
            if (typeof rec_args.n === "undefined") {
                rec_args.n = 0;
                rec_args.input_size = 0;
                rec_args.input_amount = 0;
            }
            if (required_amount <= 0)
                return resolve({
                    input_size: rec_args.input_size,
                    input_amount: rec_args.input_amount,
                    change_amount: required_amount * -1 //required_amount will be -ve of change_amount
                });
            else if (rec_args.n >= senders.length) {
                return resolve({
                    hasInsufficientBalance: true,
                    input_size: rec_args.input_size,
                    input_amount: rec_args.input_amount,
                    change_amount: required_amount * -1
                });
            }
            let addr = senders[rec_args.n],
                rs = redeemScripts[rec_args.n];
            let addr_type = coinjs.addressDecode(addr).type;
            let size_per_input = _sizePerInput(addr, rs);
            multiApi('unspent', { addr, allowUnconfirmedUtxos: rec_args.allowUnconfirmedUtxos }).then(utxos => {
                //console.debug("add-utxo", addr, rs, required_amount, utxos);
                for (let i = 0; i < utxos.length && required_amount > 0; i++) {
                    if (utxos.length === 1 && rec_args.allowUnconfirmedUtxos) {
                        console.log('allowing unconfirmed utxos')
                    } else if (!utxos[i].confirmations) //ignore unconfirmed utxo
                        continue;
                    var script;
                    if (!rs || !rs.length) //legacy script
                        script = utxos[i].script;
                    else if (((rs.match(/^00/) && rs.length == 44)) || (rs.length == 40 && rs.match(/^[a-f0-9]+$/gi)) || addr_type === 'multisigBech32') {
                        //redeemScript for segwit/bech32 and multisig (bech32)
                        let s = coinjs.script();
                        s.writeBytes(Crypto.util.hexToBytes(rs));
                        s.writeOp(0);
                        s.writeBytes(coinjs.numToBytes(utxos[i].value.toFixed(0), 8));
                        script = Crypto.util.bytesToHex(s.buffer);
                    } else //redeemScript for multisig (segwit)
                        script = rs;
                    tx.addinput(utxos[i].tx_hash_big_endian, utxos[i].tx_output_n, script, 0xfffffffd /*sequence*/); //0xfffffffd for Replace-by-fee
                    //update track values
                    rec_args.input_size += size_per_input;
                    rec_args.input_amount += util.Sat_to_BTC(utxos[i].value);
                    required_amount -= util.Sat_to_BTC(utxos[i].value);
                    if (fee_rate) //automatic fee calculation (dynamic)
                        required_amount += size_per_input * fee_rate;
                }
                rec_args.n += 1;
                addUTXOs(tx, senders, redeemScripts, required_amount, fee_rate, rec_args)
                    .then(result => resolve(result))
                    .catch(error => reject(error))
            }).catch(error => reject(error))
        })
    }
    btcOperator.addUTXOs = addUTXOs;

    function addOutputs(tx, receivers, amounts, change_address) {
        let size = 0;
        for (let i in receivers) {
            tx.addoutput(receivers[i], amounts[i]);
            size += _sizePerOutput(receivers[i]);
        }
        tx.addoutput(change_address, 0);
        size += _sizePerOutput(change_address);
        return size;
    }
    btcOperator.addOutputs = addOutputs;

    function tx_fetch_for_editing(tx) {
        return new Promise((resolve, reject) => {
            if (typeof tx == 'string' && /^[0-9a-f]{64}$/i.test(tx)) { //tx is txid
                getTx.hex(tx)
                    .then(txhex => resolve(deserializeTx(txhex)))
                    .catch(error => reject(error))
            } else resolve(deserializeTx(tx));
        })
    }
    btcOperator.tx_fetch_for_editing = tx_fetch_for_editing;

    const extractLastHexStrings = btcOperator.extractLastHexStrings = function (arr) {
        const result = [];
        for (let i = 0; i < arr.length; i++) {
            const innerArray = arr[i];
            if (innerArray.length > 0) {
                const lastHexString = innerArray[innerArray.length - 1];
                result.push(lastHexString);
            }
        }
        return result;
    }

    btcOperator.editFee = function (tx_hex, new_fee, private_keys, change_only = true) {
        return new Promise((resolve, reject) => {
            if (!Array.isArray(private_keys))
                private_keys = [private_keys];
            tx_fetch_for_editing(tx_hex).then(tx => {
                parseTransaction(tx).then(tx_parsed => {
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
                    else if (Array.isArray(change_only))    //allow only given set of receiver id outputs to be edited
                        change_only.forEach(id => edit_output_address.add(id));

                    //edit output values to increase fee
                    let inc_fee = util.BTC_to_Sat(new_fee - tx_parsed.fee);
                    if (inc_fee < MIN_FEE_UPDATE)
                        return reject(`Insufficient additional fee. Minimum increment: ${MIN_FEE_UPDATE}`);
                    for (let i = tx.outs.length - 1; i >= 0 && inc_fee > 0; i--)   //reduce in reverse order
                        if (edit_output_address.has(tx_parsed.outputs[i].address)) {
                            let current_value = tx.outs[i].value;
                            if (current_value instanceof BigInteger)    //convert BigInteger class to inv value
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
                        let max_possible_fee = util.BTC_to_Sat(new_fee) - inc_fee; //in satoshi
                        return reject(`Insufficient output values to increase fee. Maximum fee possible: ${util.Sat_to_BTC(max_possible_fee)}`);
                    }
                    tx.outs = tx.outs.filter(o => o.value >= DUST_AMT); //remove all output with value less than DUST amount

                    //remove existing signatures and reset the scripts
                    let wif_keys = [];
                    for (let i in tx.ins) {
                        var addr = tx_parsed.inputs[i].address,
                            value = util.BTC_to_Sat(tx_parsed.inputs[i].value);
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
                        } else if (((rs.match(/^00/) && rs.length == 44)) || (rs.length == 40 && rs.match(/^[a-f0-9]+$/gi)) || addr_decode.type === 'multisigBech32') {
                            //redeemScript for segwit/bech32 and multisig (bech32)
                            let s = coinjs.script();
                            s.writeBytes(Crypto.util.hexToBytes(rs));
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
                    resolve(tx.serialize());
                }).catch(error => reject(error))
            }).catch(error => reject(error))
        })
    }

    btcOperator.editFee_corewallet = function (tx_hex, new_fee, private_keys, change_only = true) {
        return new Promise((resolve, reject) => {
            if (!Array.isArray(private_keys))
                private_keys = [private_keys];
            tx_fetch_for_editing(tx_hex).then(tx => {
                parseTransaction(tx).then(tx_parsed => {
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
                    let inc_fee = util.BTC_to_Sat(new_fee - tx_parsed.fee);
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
                        let max_possible_fee = util.BTC_to_Sat(new_fee) - inc_fee; //in satoshi
                        return reject(`Insufficient output values to increase fee. Maximum fee possible: ${util.Sat_to_BTC(max_possible_fee)}`);
                    }
                    tx.outs = tx.outs.filter(o => o.value >= DUST_AMT); //remove all output with value less than DUST amount

                    //remove existing signatures and reset the scripts
                    let wif_keys = [];
                    let witness_position = 0;
                    for (let i in tx.ins) {
                        var addr = tx_parsed.inputs[i].address,
                            value = util.BTC_to_Sat(tx_parsed.inputs[i].value);
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
                            let s = coinjs.script();
                            s.writeBytes(Crypto.util.hexToBytes(rs));
                            s.writeOp(0);
                            s.writeBytes(coinjs.numToBytes(value.toFixed(0), 8));
                            script = Crypto.util.bytesToHex(s.buffer);
                            if (addr_decode == "bech32") { witness_position = witness_position + 1; } //bech32 has witness
                        } else if (addr_decode.type === 'multisigBech32') {
                            var rs_array = [];
                            rs_array = btcOperator.extractLastHexStrings(tx.witness);
                            let redeemScript = rs_array[witness_position];
                            witness_position = witness_position + 1;

                            //redeemScript multisig (bech32)
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
                    if (btcOperator.checkSigned(tx)) {
                        resolve(tx.serialize());
                    } else {
                        reject("All private keys not present");
                    }
                }).catch(error => reject(error))
            }).catch(error => reject(error))
        })
    }


    btcOperator.sendTx = function (senders, privkeys, receivers, amounts, fee = null, options = {}) {
        options.sendingTx = true;
        return new Promise((resolve, reject) => {
            createSignedTx(senders, privkeys, receivers, amounts, fee, options).then(result => {
                broadcastTx(result.transaction.serialize())
                    .then(txid => resolve(txid))
                    .catch(error => reject(error));
            }).catch(error => reject(error))
        })
    }

    const createSignedTx = btcOperator.createSignedTx = function (senders, privkeys, receivers, amounts, fee = null, options = {}) {
        return new Promise((resolve, reject) => {
            try {
                ({
                    senders,
                    privkeys,
                    receivers,
                    amounts
                } = validateTxParameters({
                    senders,
                    privkeys,
                    receivers,
                    amounts,
                    fee,
                    ...options
                }));
            } catch (e) {
                return reject(e)
            }
            let redeemScripts = [],
                wif_keys = [];
            for (let i in senders) {
                let rs = _redeemScript(senders[i], privkeys[i]); //get redeem-script (segwit/bech32)
                redeemScripts.push(rs);
                rs === false ? wif_keys.unshift(privkeys[i]) : wif_keys.push(privkeys[i]); //sorting private-keys (wif)
            }
            if (redeemScripts.includes(null)) //TODO: segwit
                return reject("Unable to get redeem-script");
            //create transaction
            createTransaction({
                senders, redeemScripts, receivers, amounts, fee,
                change_address: options.change_address || senders[0],
                ...options
            }).then(result => {
                let tx = result.transaction;
                console.debug("Unsigned:", tx.serialize());
                new Set(wif_keys).forEach(key => tx.sign(key, 1 /*sighashtype*/)); //Sign the tx using private key WIF
                console.debug("Signed:", tx.serialize());
                resolve(result);
            }).catch(error => reject(error));
        })
    }

    btcOperator.createTx = function (senders, receivers, amounts, fee = null, options = {
        allowUnconfirmedUtxos: false
    }) {
        return new Promise((resolve, reject) => {
            try {
                ({
                    senders,
                    receivers,
                    amounts
                } = validateTxParameters({
                    senders,
                    receivers,
                    amounts,
                    fee,
                    change_address: options.change_address
                }));
            } catch (e) {
                return reject(e)
            }
            let redeemScripts = senders.map(id => _redeemScript(id));
            if (redeemScripts.includes(null)) //TODO: segwit
                return reject("Unable to get redeem-script");
            //create transaction
            createTransaction({
                senders, redeemScripts, receivers, amounts, fee,
                change_address: options.change_address || senders[0],
                ...options
            }).then(result => {
                result.tx_hex = result.transaction.serialize();
                delete result.transaction;
                resolve(result);
            }).catch(error => reject(error))
        })
    }

    btcOperator.createMultiSigTx = function (sender, redeemScript, receivers, amounts, fee = null, options = {}) {
        return new Promise((resolve, reject) => {
            //validate tx parameters
            let addr_type = validateAddress(sender);
            if (!(["multisig", "multisigBech32"].includes(addr_type)))
                return reject("Invalid sender (multisig):" + sender);
            else {
                let script = coinjs.script();
                let decode = (addr_type == "multisig") ?
                    script.decodeRedeemScript(redeemScript) :
                    script.decodeRedeemScriptBech32(redeemScript);
                if (!decode || decode.address !== sender)
                    return reject("Invalid redeem-script");
            }
            try {
                ({
                    receivers,
                    amounts
                } = validateTxParameters({
                    receivers,
                    amounts,
                    fee,
                    change_address: options.change_address
                }));
            } catch (e) {
                return reject(e)
            }
            //create transaction
            createTransaction({
                senders: [sender], redeemScripts: [redeemScript],
                receivers, amounts, fee,
                change_address: options.change_address || sender,
                ...options
            }).then(result => {
                result.tx_hex = result.transaction.serialize();
                delete result.transaction;
                resolve(result);
            }).catch(error => reject(error))

        })
    }

    const deserializeTx = btcOperator.deserializeTx = function (tx) {
        if (typeof tx === 'string' || Array.isArray(tx)) {
            try {
                tx = coinjs.transaction().deserialize(tx);
            } catch {
                throw "Invalid transaction hex";
            }
        } else if (typeof tx !== 'object' || typeof tx.sign !== 'function')
            throw "Invalid transaction object";
        return tx;
    }

    btcOperator.signTx = function (tx, privkeys, sighashtype = 1) {
        tx = deserializeTx(tx);
        if (!Array.isArray(privkeys))
            privkeys = [privkeys];
        for (let i in privkeys)
            if (privkeys[i].length === 64)
                privkeys[i] = coinjs.privkey2wif(privkeys[i]);
        new Set(privkeys).forEach(key => tx.sign(key, sighashtype)); //Sign the tx using private key WIF
        return tx.serialize();
    }

    const checkSigned = btcOperator.checkSigned = function (tx, bool = true) {
        tx = deserializeTx(tx);
        let n = [];
        for (let i in tx.ins) {
            var s = tx.extractScriptKey(i);
            if (s['type'] !== 'multisig' && s['type'] !== 'multisig_bech32')
                n.push(s.signed == 'true' || (tx.witness[i] && tx.witness[i].length == 2))
            else {
                var rs = coinjs.script().decodeRedeemScript(s.script);  //will work for bech32 too, as only address is diff
                let x = {
                    s: s['signatures'],
                    r: rs['signaturesRequired'],
                    t: rs['pubkeys'].length
                };
                if (x.r > x.t)
                    throw "signaturesRequired is more than publicKeys";
                else if (x.s < x.r)
                    n.push(x);
                else
                    n.push(true);
            }
        }
        return bool ? !(n.filter(x => x !== true).length) : n;
    }

    btcOperator.checkIfSameTx = function (tx1, tx2) {
        tx1 = deserializeTx(tx1);
        tx2 = deserializeTx(tx2);
        //compare input and output length
        if (tx1.ins.length !== tx2.ins.length || tx1.outs.length !== tx2.outs.length)
            return false;
        //compare inputs
        for (let i = 0; i < tx1.ins.length; i++)
            if (tx1.ins[i].outpoint.hash !== tx2.ins[i].outpoint.hash || tx1.ins[i].outpoint.index !== tx2.ins[i].outpoint.index)
                return false;
        //compare outputs
        for (let i = 0; i < tx1.outs.length; i++)
            if (tx1.outs[i].value !== tx2.outs[i].value || Crypto.util.bytesToHex(tx1.outs[i].script.buffer) !== Crypto.util.bytesToHex(tx2.outs[i].script.buffer))
                return false;
        return true;
    }

    const getTxOutput = (txid, i) => new Promise((resolve, reject) => {
        multiApi('tx', { txid })
            .then(result => resolve(result.out[i]))
            .catch(error => reject(error))
    });

    const parseTransaction = btcOperator.parseTransaction = function (tx) {
        return new Promise((resolve, reject) => {
            tx = deserializeTx(tx);
            let result = {};
            let promises = [];
            //Parse Inputs
            for (let i = 0; i < tx.ins.length; i++)
                promises.push(getTxOutput(tx.ins[i].outpoint.hash, tx.ins[i].outpoint.index));
            Promise.all(promises).then(inputs => {
                result.inputs = inputs.map(inp => Object({
                    address: inp.addr,
                    value: util.Sat_to_BTC(inp.value)
                }));
                let signed = checkSigned(tx, false);
                result.inputs.forEach((inp, i) => inp.signed = signed[i]);
                //Parse Outputs
                result.outputs = tx.outs.map(out => {
                    var address;
                    switch (out.script.chunks[0]) {
                        case 0: //bech32, multisig-bech32
                            address = util.encodeBech32(Crypto.util.bytesToHex(out.script.chunks[1]), coinjs.bech32.version, coinjs.bech32.hrp);
                            break;
                        case 169: //segwit, multisig-segwit
                            address = util.encodeLegacy(Crypto.util.bytesToHex(out.script.chunks[1]), coinjs.multisig);
                            break;
                        case 118: //legacy
                            address = util.encodeLegacy(Crypto.util.bytesToHex(out.script.chunks[2]), coinjs.pub);
                    }
                    return {
                        address,
                        value: util.Sat_to_BTC(out.value)
                    }
                });
                //Parse Totals
                result.total_input = parseFloat(result.inputs.reduce((a, inp) => a += inp.value, 0).toFixed(8));
                result.total_output = parseFloat(result.outputs.reduce((a, out) => a += out.value, 0).toFixed(8));
                result.fee = parseFloat((result.total_input - result.total_output).toFixed(8));
                resolve(result);
            }).catch(error => reject(error))
        })
    }

    btcOperator.transactionID = function (tx) {
        tx = deserializeTx(tx);
        let clone = coinjs.clone(tx);
        clone.witness = null;
        let raw_bytes = Crypto.util.hexToBytes(clone.serialize());
        let txid = Crypto.SHA256(Crypto.SHA256(raw_bytes, { asBytes: true }), { asBytes: true }).reverse();
        return Crypto.util.bytesToHex(txid);
    }

    const getTx = btcOperator.getTx = txid => new Promise(async (resolve, reject) => {
        try {
            const result = await multiApi('tx', { txid });
            resolve({
                confirmations: result.confirmations,
                block: result.block_height,
                txid: result.hash,
                time: result.time,
                size: result.size,
                fee: util.Sat_to_BTC(result.fee),
                inputs: result.inputs.map(i => Object({ address: i.prev_out.addr, value: util.Sat_to_BTC(i.prev_out.value) })),
                total_input_value: util.Sat_to_BTC(result.inputs.reduce((a, i) => a + i.prev_out.value, 0)),
                outputs: result.out.map(o => Object({ address: o.addr, value: util.Sat_to_BTC(o.value) })),
                total_output_value: util.Sat_to_BTC(result.out.reduce((a, o) => a += o.value, 0)),
            })
        } catch (error) {
            reject(error)
        }
    }).catch(error => reject(error))

    getTx.hex = btcOperator.getTx.hex = txid => multiApi('txHex', { txid });

    btcOperator.getAddressData = address => new Promise((resolve, reject) => {
        Promise.all([
            multiApi('balance', { addr: address }),
            multiApi('txs', { addr: address })
        ]).then(([balance, txs]) => {
            const parsedTxs = txs.map(tx => parseTx(tx, address));
            resolve({
                address,
                balance,
                txs: parsedTxs
            });
        }).catch(error => reject(error))
    });

    btcOperator.getBlock = block => new Promise((resolve, reject) => {
        fetch_api(`rawblock/${block}`).then(result => resolve({
            height: result.height,
            hash: result.hash,
            merkle_root: result.mrkl_root,
            prev_block: result.prev_block,
            next_block: result.next_block[0],
            size: result.size,
            time: result.time * 1000, //s to ms
            txs: result.tx.map(t => Object({
                fee: t.fee,
                size: t.size,
                inputs: t.inputs.map(i => Object({ address: i.prev_out.addr, value: util.Sat_to_BTC(i.prev_out.value) })),
                total_input_value: util.Sat_to_BTC(t.inputs.reduce((a, i) => a + i.prev_out.value, 0)),
                outputs: t.out.map(o => Object({ address: o.addr, value: util.Sat_to_BTC(o.value) })),
                total_output_value: util.Sat_to_BTC(t.out.reduce((a, o) => a += o.value, 0)),
            }))

        })).catch(error => reject(error))
    });

})('object' === typeof module ? module.exports : window.btcOperator = {});
