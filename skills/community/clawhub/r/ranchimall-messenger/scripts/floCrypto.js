(function (EXPORTS) { //floCrypto v2.3.6a
    /* FLO Crypto Operators */
    'use strict';
    const floCrypto = EXPORTS;

    const p = BigInteger("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F", 16);
    const ecparams = EllipticCurve.getSECCurveByName("secp256k1");
    const ascii_alternatives = `‘ '\n’ '\n“ "\n” "\n– --\n— ---\n≥ >=\n≤ <=\n≠ !=\n× *\n÷ /\n← <-\n→ ->\n↔ <->\n⇒ =>\n⇐ <=\n⇔ <=>`;
    const exponent1 = () => p.add(BigInteger.ONE).divide(BigInteger("4"));
    coinjs.compressed = true; //defaulting coinjs compressed to true;

    function calculateY(x) {
        let exp = exponent1();
        // x is x value of public key in BigInteger format without 02 or 03 or 04 prefix
        return x.modPow(BigInteger("3"), p).add(BigInteger("7")).mod(p).modPow(exp, p)
    }

    function getUncompressedPublicKey(compressedPublicKey) {
        // Fetch x from compressedPublicKey
        let pubKeyBytes = Crypto.util.hexToBytes(compressedPublicKey);
        const prefix = pubKeyBytes.shift() // remove prefix
        let prefix_modulus = prefix % 2;
        pubKeyBytes.unshift(0) // add prefix 0
        let x = new BigInteger(pubKeyBytes)
        let xDecimalValue = x.toString()
        // Fetch y
        let y = calculateY(x);
        let yDecimalValue = y.toString();
        // verify y value
        let resultBigInt = y.mod(BigInteger("2"));
        let check = resultBigInt.toString() % 2;
        if (prefix_modulus !== check)
            yDecimalValue = y.negate().mod(p).toString();
        return {
            x: xDecimalValue,
            y: yDecimalValue
        };
    }

    function getSenderPublicKeyString() {
        let privateKey = ellipticCurveEncryption.senderRandom();
        var senderPublicKeyString = ellipticCurveEncryption.senderPublicString(privateKey);
        return {
            privateKey: privateKey,
            senderPublicKeyString: senderPublicKeyString
        }
    }

    function deriveSharedKeySender(receiverPublicKeyHex, senderPrivateKey) {
        let receiverPublicKeyString = getUncompressedPublicKey(receiverPublicKeyHex);
        var senderDerivedKey = ellipticCurveEncryption.senderSharedKeyDerivation(
            receiverPublicKeyString.x, receiverPublicKeyString.y, senderPrivateKey);
        return senderDerivedKey;
    }

    function deriveSharedKeyReceiver(senderPublicKeyString, receiverPrivateKey) {
        return ellipticCurveEncryption.receiverSharedKeyDerivation(
            senderPublicKeyString.XValuePublicString, senderPublicKeyString.YValuePublicString, receiverPrivateKey);
    }

    function getReceiverPublicKeyString(privateKey) {
        return ellipticCurveEncryption.receiverPublicString(privateKey);
    }

    function wifToDecimal(pk_wif, isPubKeyCompressed = false) {
        let pk = Bitcoin.Base58.decode(pk_wif)
        pk.shift()
        pk.splice(-4, 4)
        //If the private key corresponded to a compressed public key, also drop the last byte (it should be 0x01).
        if (isPubKeyCompressed == true) pk.pop()
        pk.unshift(0)
        let privateKeyDecimal = BigInteger(pk).toString()
        let privateKeyHex = Crypto.util.bytesToHex(pk)
        return {
            privateKeyDecimal: privateKeyDecimal,
            privateKeyHex: privateKeyHex
        }
    }

    //generate a random Interger within range
    floCrypto.randInt = function (min, max) {
        min = Math.ceil(min);
        max = Math.floor(max);
        return Math.floor(securedMathRandom() * (max - min + 1)) + min;
    }

    //generate a random String within length (options : alphaNumeric chars only)
    floCrypto.randString = function (length, alphaNumeric = true) {
        var result = '';
        var characters = alphaNumeric ? 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789' :
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_+-./*?@#&$<>=[]{}():';
        for (var i = 0; i < length; i++)
            result += characters.charAt(Math.floor(securedMathRandom() * characters.length));
        return result;
    }

    //Encrypt Data using public-key
    floCrypto.encryptData = function (data, receiverPublicKeyHex) {
        var senderECKeyData = getSenderPublicKeyString();
        var senderDerivedKey = deriveSharedKeySender(receiverPublicKeyHex, senderECKeyData.privateKey);
        let senderKey = senderDerivedKey.XValue + senderDerivedKey.YValue;
        let secret = Crypto.AES.encrypt(data, senderKey);
        return {
            secret: secret,
            senderPublicKeyString: senderECKeyData.senderPublicKeyString
        };
    }

    //Decrypt Data using private-key
    floCrypto.decryptData = function (data, privateKeyHex) {
        var receiverECKeyData = {};
        if (typeof privateKeyHex !== "string") throw new Error("No private key found.");
        let privateKey = wifToDecimal(privateKeyHex, true);
        if (typeof privateKey.privateKeyDecimal !== "string") throw new Error("Failed to detremine your private key.");
        receiverECKeyData.privateKey = privateKey.privateKeyDecimal;
        var receiverDerivedKey = deriveSharedKeyReceiver(data.senderPublicKeyString, receiverECKeyData.privateKey);
        let receiverKey = receiverDerivedKey.XValue + receiverDerivedKey.YValue;
        let decryptMsg = Crypto.AES.decrypt(data.secret, receiverKey);
        return decryptMsg;
    }

    //Sign data using private-key
    floCrypto.signData = function (data, privateKeyHex) {
        var key = new Bitcoin.ECKey(privateKeyHex);
        var messageHash = Crypto.SHA256(data);
        var messageSign = Bitcoin.ECDSA.sign(messageHash, key.priv);
        var sighex = Crypto.util.bytesToHex(messageSign);
        return sighex;
    }

    //Verify signatue of the data using public-key
    floCrypto.verifySign = function (data, signatureHex, publicKeyHex) {
        var msgHash = Crypto.SHA256(data);
        var sigBytes = Crypto.util.hexToBytes(signatureHex);
        var publicKeyPoint = ecparams.getCurve().decodePointHex(publicKeyHex);
        var verify = Bitcoin.ECDSA.verify(msgHash, sigBytes, publicKeyPoint);
        return verify;
    }

    //Generates a new flo ID and returns private-key, public-key and floID
    const generateNewID = floCrypto.generateNewID = function () {
        var key = new Bitcoin.ECKey(false);
        key.setCompressed(true);
        return {
            floID: key.getBitcoinAddress(),
            pubKey: key.getPubKeyHex(),
            privKey: key.getBitcoinWalletImportFormat()
        }
    }

    Object.defineProperties(floCrypto, {
        newID: {
            get: () => generateNewID()
        },
        hashID: {
            value: (str) => {
                let bytes = ripemd160(Crypto.SHA256(str, { asBytes: true }), { asBytes: true });
                bytes.unshift(bitjs.pub);
                var hash = Crypto.SHA256(Crypto.SHA256(bytes, {
                    asBytes: true
                }), {
                    asBytes: true
                });
                var checksum = hash.slice(0, 4);
                return bitjs.Base58.encode(bytes.concat(checksum));
            }
        },
        tmpID: {
            get: () => {
                let bytes = Crypto.util.randomBytes(20);
                bytes.unshift(bitjs.pub);
                var hash = Crypto.SHA256(Crypto.SHA256(bytes, {
                    asBytes: true
                }), {
                    asBytes: true
                });
                var checksum = hash.slice(0, 4);
                return bitjs.Base58.encode(bytes.concat(checksum));
            }
        }
    });

    //Returns public-key from private-key
    floCrypto.getPubKeyHex = function (privateKeyHex) {
        if (!privateKeyHex)
            return null;
        var key = new Bitcoin.ECKey(privateKeyHex);
        if (key.priv == null)
            return null;
        key.setCompressed(true);
        return key.getPubKeyHex();
    }

    //Returns flo-ID from public-key or private-key
    floCrypto.getFloID = function (keyHex) {
        if (!keyHex)
            return null;
        try {
            var key = new Bitcoin.ECKey(keyHex);
            if (key.priv == null)
                key.setPub(keyHex);
            return key.getBitcoinAddress();
        } catch {
            return null;
        }
    }

    floCrypto.getAddress = function (privateKeyHex, strict = false) {
        if (!privateKeyHex)
            return;
        var key = new Bitcoin.ECKey(privateKeyHex);
        if (key.priv == null)
            return null;
        key.setCompressed(true);
        let pubKey = key.getPubKeyHex(),
            version = bitjs.Base58.decode(privateKeyHex)[0];
        switch (version) {
            case coinjs.priv: //BTC
                return coinjs.bech32Address(pubKey).address;
            case bitjs.priv: //FLO
                return bitjs.pubkey2address(pubKey);
            default:
                return strict ? false : bitjs.pubkey2address(pubKey); //default to FLO address (if strict=false)
        }
    }

    //Verify the private-key for the given public-key or flo-ID
    floCrypto.verifyPrivKey = function (privateKeyHex, pubKey_floID, isfloID = true) {
        if (!privateKeyHex || !pubKey_floID)
            return false;
        try {
            var key = new Bitcoin.ECKey(privateKeyHex);
            if (key.priv == null)
                return false;
            key.setCompressed(true);
            if (isfloID && pubKey_floID == key.getBitcoinAddress())
                return true;
            else if (!isfloID && pubKey_floID.toUpperCase() == key.getPubKeyHex().toUpperCase())
                return true;
            else
                return false;
        } catch {
            return null;
        }
    }

    floCrypto.getMultisigAddress = function (publicKeyList, requiredSignatures) {
        if (!Array.isArray(publicKeyList) || !publicKeyList.length)
            return null;
        if (!Number.isInteger(requiredSignatures) || requiredSignatures < 1 || requiredSignatures > publicKeyList.length)
            return null;
        try {
            var multisig = bitjs.pubkeys2multisig(publicKeyList, requiredSignatures);
            return multisig;
        } catch {
            return null;
        }
    }

    floCrypto.decodeRedeemScript = function (redeemScript) {
        try {
            var decoded = bitjs.transaction().decodeRedeemScript(redeemScript);
            return decoded;
        } catch {
            return null;
        }
    }

    //Check if the given flo-id is valid or not
    floCrypto.validateFloID = function (floID, regularOnly = false) {
        if (!floID)
            return false;
        try {
            let addr = new Bitcoin.Address(floID);
            if (regularOnly && addr.version != Bitcoin.Address.standardVersion)
                return false;
            return true;
        } catch {
            return false;
        }
    }

    //Check if the given address (any blockchain) is valid or not
    floCrypto.validateAddr = function (address, std = true, bech = true) {
        let raw = decodeAddress(address);
        if (!raw)
            return false;
        if (typeof raw.version !== 'undefined') { //legacy or segwit
            if (std == false)
                return false;
            else if (std === true || (!Array.isArray(std) && std === raw.version) || (Array.isArray(std) && std.includes(raw.version)))
                return true;
            else
                return false;
        } else if (typeof raw.bech_version !== 'undefined') { //bech32
            if (bech === false)
                return false;
            else if (bech === true || (!Array.isArray(bech) && bech === raw.bech_version) || (Array.isArray(bech) && bech.includes(raw.bech_version)))
                return true;
            else
                return false;
        } else if (raw.type === 'ethereum' || raw.type === 'bch') {
            return true
        } else //unknown
            return false;
    }

    //Check the public-key (or redeem-script) for the address (any blockchain)
    floCrypto.verifyPubKey = function (pubKeyHex, address) {
        let raw = decodeAddress(address);
        if (!raw)
            return;
        let pub_hash = Crypto.util.bytesToHex(ripemd160(Crypto.SHA256(Crypto.util.hexToBytes(pubKeyHex), { asBytes: true })));
        if (typeof raw.bech_version !== 'undefined' && raw.bytes.length == 32) //bech32-multisig
            raw.hex = Crypto.util.bytesToHex(ripemd160(raw.bytes, { asBytes: true }));
        return pub_hash === raw.hex;
    }

    //Convert the given address (any blockchain) to equivalent floID
    floCrypto.toFloID = function (address, options = null) {
        if (!address)
            return;
        let raw = decodeAddress(address);
        if (!raw)
            return;
        else if (options) { //if (optional) version check is passed
            if (typeof raw.version !== 'undefined' && (!options.std || !options.std.includes(raw.version)))
                return;
            if (typeof raw.bech_version !== 'undefined' && (!options.bech || !options.bech.includes(raw.bech_version)))
                return;
        }
        raw.bytes.unshift(bitjs.pub);
        let hash = Crypto.SHA256(Crypto.SHA256(raw.bytes, {
            asBytes: true
        }), {
            asBytes: true
        });
        return bitjs.Base58.encode(raw.bytes.concat(hash.slice(0, 4)));
    }

    //Convert raw address bytes to floID
    floCrypto.rawToFloID = function (raw_bytes) {
        if (typeof raw_bytes === 'string')
            raw_bytes = Crypto.util.hexToBytes(raw_bytes);
        if (raw_bytes.length != 20)
            return null;
        raw_bytes.unshift(bitjs.pub);
        let hash = Crypto.SHA256(Crypto.SHA256(raw_bytes, {
            asBytes: true
        }), {
            asBytes: true
        });
        return bitjs.Base58.encode(raw_bytes.concat(hash.slice(0, 4)));
    }

    //Convert the given multisig address (any blockchain) to equivalent multisig floID
    floCrypto.toMultisigFloID = function (address, options = null) {
        if (!address)
            return;
        let raw = decodeAddress(address);
        if (!raw)
            return;
        else if (options) { //if (optional) version check is passed
            if (typeof raw.version !== 'undefined' && (!options.std || !options.std.includes(raw.version)))
                return;
            if (typeof raw.bech_version !== 'undefined' && (!options.bech || !options.bech.includes(raw.bech_version)))
                return;
        }
        if (typeof raw.bech_version !== 'undefined') {
            if (raw.bytes.length != 32) return; //multisig bech address have 32 bytes
            //multisig-bech:hash=SHA256 whereas multisig:hash=r160(SHA265), thus ripemd160 the bytes from multisig-bech
            raw.bytes = ripemd160(raw.bytes, {
                asBytes: true
            });
        }
        raw.bytes.unshift(bitjs.multisig);
        let hash = Crypto.SHA256(Crypto.SHA256(raw.bytes, {
            asBytes: true
        }), {
            asBytes: true
        });
        return bitjs.Base58.encode(raw.bytes.concat(hash.slice(0, 4)));
    }

    //Checks if the given addresses (any blockchain) are same (w.r.t keys)
    floCrypto.isSameAddr = function (addr1, addr2) {
        if (!addr1 || !addr2)
            return;
        let raw1 = decodeAddress(addr1),
            raw2 = decodeAddress(addr2);
        if (!raw1 || !raw2)
            return false;
        else {
            if (typeof raw1.bech_version !== 'undefined' && raw1.bytes.length == 32) //bech32-multisig
                raw1.hex = Crypto.util.bytesToHex(ripemd160(raw1.bytes, { asBytes: true }));
            if (typeof raw2.bech_version !== 'undefined' && raw2.bytes.length == 32) //bech32-multisig
                raw2.hex = Crypto.util.bytesToHex(ripemd160(raw2.bytes, { asBytes: true }));
            return raw1.hex === raw2.hex;
        }
    }

    const decodeAddress = floCrypto.decodeAddr = function (address) {
        if (!address)
            return;
        else if (address.length == 33 || address.length == 34) { //legacy encoding
            let decode = bitjs.Base58.decode(address);
            let bytes = decode.slice(0, decode.length - 4);
            let checksum = decode.slice(decode.length - 4),
                hash = Crypto.SHA256(Crypto.SHA256(bytes, {
                    asBytes: true
                }), {
                    asBytes: true
                });
            return (hash[0] != checksum[0] || hash[1] != checksum[1] || hash[2] != checksum[2] || hash[3] != checksum[3]) ? null : {
                version: bytes.shift(),
                hex: Crypto.util.bytesToHex(bytes),
                bytes
            }
        } else if (!address.startsWith("0x") && address.length == 42 || address.length == 62) { //bech encoding
            let decode = coinjs.bech32_decode(address);
            if (decode) {
                let bytes = decode.data;
                let bech_version = bytes.shift();
                bytes = coinjs.bech32_convert(bytes, 5, 8, false);
                return {
                    bech_version,
                    hrp: decode.hrp,
                    hex: Crypto.util.bytesToHex(bytes),
                    bytes
                }
            } else
                return null;
        } else if ((address.length == 42 && address.startsWith("0x")) || (address.length == 40 && !address.startsWith("0x"))) { //Ethereum Address
            if (address.startsWith("0x")) { address = address.substring(2); }
            let bytes = Crypto.util.hexToBytes(address);
            return {
                version: 1,
                hex: address,
                type: 'ethereum',
                bytes
            }
        } else if (address.length >= 34 && address.length <= 45 && /^q[a-z0-9]+$/.test(address)) { //BCH Address
            try {
                let addrBytes = [];
                for (let i = 0; i < address.length; i++) {
                    addrBytes.push(address.charCodeAt(i));
                }
                let payload = ripemd160(Crypto.SHA256(addrBytes, { asBytes: true }));
                return {
                    version: 1,
                    hex: Crypto.util.bytesToHex(payload),
                    type: 'bch',
                    bytes: payload
                }
            } catch (e) {
                return null;
            }
        }
    }

    //Split the str using shamir's Secret and Returns the shares 
    floCrypto.createShamirsSecretShares = function (str, total_shares, threshold_limit) {
        try {
            if (str.length > 0) {
                var strHex = shamirSecretShare.str2hex(str);
                var shares = shamirSecretShare.share(strHex, total_shares, threshold_limit);
                return shares;
            }
            return false;
        } catch {
            return false
        }
    }

    //Returns the retrived secret by combining the shamirs shares
    const retrieveShamirSecret = floCrypto.retrieveShamirSecret = function (sharesArray) {
        try {
            if (sharesArray.length > 0) {
                var comb = shamirSecretShare.combine(sharesArray.slice(0, sharesArray.length));
                comb = shamirSecretShare.hex2str(comb);
                return comb;
            }
            return false;
        } catch {
            return false;
        }
    }

    //Verifies the shares and str
    floCrypto.verifyShamirsSecret = function (sharesArray, str) {
        if (!str)
            return null;
        else if (retrieveShamirSecret(sharesArray) === str)
            return true;
        else
            return false;
    }

    const validateASCII = floCrypto.validateASCII = function (string, bool = true) {
        if (typeof string !== "string")
            return null;
        if (bool) {
            let x;
            for (let i = 0; i < string.length; i++) {
                x = string.charCodeAt(i);
                if (x < 32 || x > 127)
                    return false;
            }
            return true;
        } else {
            let x, invalids = {};
            for (let i = 0; i < string.length; i++) {
                x = string.charCodeAt(i);
                if (x < 32 || x > 127)
                    if (x in invalids)
                        invalids[string[i]].push(i)
                    else
                        invalids[string[i]] = [i];
            }
            if (Object.keys(invalids).length)
                return invalids;
            else
                return true;
        }
    }

    floCrypto.convertToASCII = function (string, mode = 'soft-remove') {
        let chars = validateASCII(string, false);
        if (chars === true)
            return string;
        else if (chars === null)
            return null;
        let convertor, result = string,
            refAlt = {};
        ascii_alternatives.split('\n').forEach(a => refAlt[a[0]] = a.slice(2));
        mode = mode.toLowerCase();
        if (mode === "hard-unicode")
            convertor = (c) => `\\u${('000' + c.charCodeAt().toString(16)).slice(-4)}`;
        else if (mode === "soft-unicode")
            convertor = (c) => refAlt[c] || `\\u${('000' + c.charCodeAt().toString(16)).slice(-4)}`;
        else if (mode === "hard-remove")
            convertor = c => "";
        else if (mode === "soft-remove")
            convertor = c => refAlt[c] || "";
        else
            return null;
        for (let c in chars)
            result = result.replaceAll(c, convertor(c));
        return result;
    }

    floCrypto.revertUnicode = function (string) {
        return string.replace(/\\u[\dA-F]{4}/gi,
            m => String.fromCharCode(parseInt(m.replace(/\\u/g, ''), 16)));
    }

})('object' === typeof module ? module.exports : window.floCrypto = {});
