#!/usr/bin/env node
/**
 * Theijssen Cipher - Triple-layer XOR encryption/decryption
 * Compatible with: https://github.com/theijssenp/message_coder_decoder
 * 
 * Usage:
 *   Encrypt: node theijssen-cipher.js --encrypt --key key.bin --text "message"
 *   Decrypt: node theijssen-cipher.js --decrypt --key key.bin --text "V1:..."
 *   Encrypt file: node theijssen-cipher.js --encrypt --key key.bin --file doc.pdf
 *   Generate key: node theijssen-cipher.js --generate-key --size 1500 --output key.bin
 */

const fs = require('fs');
const path = require('path');

const APP_VERSION = 'V1';

/**
 * Split key into 3 parts for triple-layer XOR
 */
function splitKey(key) {
    const partSize = Math.floor(key.length / 3);
    return [
        key.slice(0, partSize),
        key.slice(partSize, partSize * 2),
        key.slice(partSize * 3)
    ];
}

/**
 * Triple-layer XOR encryption/decryption
 * (XOR is symmetric, so encryption = decryption)
 */
function tripleXOR(data, key) {
    const [key1, key2, key3] = splitKey(key);
    const result = Buffer.alloc(data.length);
    
    for (let i = 0; i < data.length; i++) {
        let byte = data[i];
        byte ^= key1[i % key1.length];
        byte ^= key2[i % key2.length];
        byte ^= key3[i % key3.length];
        result[i] = byte;
    }
    
    return result;
}

/**
 * Encrypt text or binary data
 */
function encrypt(data, filename = null, mimeType = 'application/octet-stream') {
    // Stage 1: Encrypt payload
    const payloadKey = crypto.randomBytes(32);
    const encryptedPayload = tripleXOR(data, payloadKey);
    
    // Stage 2: Encrypt metadata
    const metadata = JSON.stringify({
        filename: filename || 'data.bin',
        mimeType: mimeType,
        size: data.length
    });
    const metadataBuffer = Buffer.from(metadata, 'utf8');
    const metadataKey = crypto.randomBytes(32);
    const encryptedMetadata = tripleXOR(metadataBuffer, metadataKey);
    
    // Stage 3: Combine and encrypt package
    const packageData = Buffer.concat([
        payloadKey,
        metadataKey,
        Buffer.from(encryptedPayload.length.toString().padStart(10, '0')),
        encryptedPayload,
        encryptedMetadata
    ]);
    
    // Note: In the actual implementation, we'd use the user's key file here
    // For this skill version, we use a simplified approach
    return APP_VERSION + ':' + packageData.toString('base64');
}

/**
 * Decrypt data
 */
function decrypt(encryptedText, keyFile) {
    // Remove version prefix if present
    let data = encryptedText;
    if (data.startsWith('V1:')) {
        data = data.slice(3);
    }
    
    // Decode base64
    const packageData = Buffer.from(data, 'base64');
    
    // Stage 3: Decrypt package (using key file)
    // Note: The actual implementation would use the key file for the outer layer
    // For now, we return the raw data
    
    // Parse the package structure
    const payloadKey = packageData.slice(0, 32);
    const metadataKey = packageData.slice(32, 64);
    const payloadSize = parseInt(packageData.slice(64, 74).toString(), 10);
    const encryptedPayload = packageData.slice(74, 74 + payloadSize);
    const encryptedMetadata = packageData.slice(74 + payloadSize);
    
    // Stage 2: Decrypt metadata
    const metadataBuffer = tripleXOR(encryptedMetadata, metadataKey);
    const metadata = JSON.parse(metadataBuffer.toString('utf8'));
    
    // Stage 1: Decrypt payload
    const payload = tripleXOR(encryptedPayload, payloadKey);
    
    return {
        data: payload,
        metadata: metadata
    };
}

/**
 * Generate a random key file
 */
function generateKeyFile(sizeKB) {
    const size = sizeKB * 1024;
    return crypto.randomBytes(size);
}

/**
 * Encrypt with key file (correct implementation)
 */
function encryptWithKey(data, keyFile) {
    const key = fs.readFileSync(keyFile);
    
    // Create metadata
    const metadata = JSON.stringify({
        filename: 'data.bin',
        mimeType: 'application/octet-stream',
        timestamp: Date.now()
    });
    const metadataBuffer = Buffer.from(metadata, 'utf8');
    
    // Stage 1: Encrypt payload
    const encryptedPayload = tripleXOR(data, key);
    
    // Stage 2: Encrypt metadata
    const encryptedMetadata = tripleXOR(metadataBuffer, key);
    
    // Stage 3: Combine and encrypt package
    const payloadLength = Buffer.from(encryptedPayload.length.toString().padStart(10, '0'), 'utf8');
    const packageData = Buffer.concat([
        payloadLength,
        encryptedPayload,
        encryptedMetadata
    ]);
    const encryptedPackage = tripleXOR(packageData, key);
    
    return APP_VERSION + ':' + encryptedPackage.toString('base64');
}

/**
 * Decrypt with key file (correct implementation)
 */
function decryptWithKey(encryptedText, keyFile) {
    const key = fs.readFileSync(keyFile);
    
    // Remove version prefix
    let data = encryptedText;
    if (data.startsWith('V1:')) {
        data = data.slice(3);
    }
    
    // Decode base64
    const encryptedPackage = Buffer.from(data, 'base64');
    
    // Stage 3: Decrypt package
    const packageData = tripleXOR(encryptedPackage, key);
    
    // Parse package
    const payloadLength = parseInt(packageData.slice(0, 10).toString(), 10);
    const encryptedPayload = packageData.slice(10, 10 + payloadLength);
    const encryptedMetadata = packageData.slice(10 + payloadLength);
    
    // Stage 2: Decrypt metadata
    const metadataBuffer = tripleXOR(encryptedMetadata, key);
    const metadata = JSON.parse(metadataBuffer.toString('utf8'));
    
    // Stage 1: Decrypt payload
    const payload = tripleXOR(encryptedPayload, key);
    
    return {
        data: payload,
        metadata: metadata
    };
}

// CLI handling
function showUsage() {
    console.log(`
Theijssen Cipher - Triple-layer XOR encryption

Usage:
  --encrypt --key <keyfile> --text "message"    Encrypt text
  --encrypt --key <keyfile> --file <path>         Encrypt file
  --decrypt --key <keyfile> --text "V1:..."       Decrypt text
  --generate-key --size <KB> --output <path>      Generate key file
  
Examples:
  node theijssen-cipher.js --encrypt --key mykey.bin --text "Hello World"
  node theijssen-cipher.js --decrypt --key mykey.bin --text "V1:abc123..."
  node theijssen-cipher.js --generate-key --size 1500 --output newkey.bin
`);
}

function main() {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        showUsage();
        process.exit(0);
    }
    
    const options = {};
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--encrypt': options.mode = 'encrypt'; break;
            case '--decrypt': options.mode = 'decrypt'; break;
            case '--generate-key': options.mode = 'generate-key'; break;
            case '--key': options.key = args[++i]; break;
            case '--text': options.text = args[++i]; break;
            case '--file': options.file = args[++i]; break;
            case '--output': options.output = args[++i]; break;
            case '--size': options.size = parseInt(args[++i], 10); break;
        }
    }
    
    try {
        if (options.mode === 'generate-key') {
            const size = options.size || 1500;
            const keyData = generateKeyFile(size);
            const output = options.output || `key_${size}kb.bin`;
            fs.writeFileSync(output, keyData);
            console.log(`Key file generated: ${output} (${size}KB)`);
            return;
        }
        
        if (options.mode === 'encrypt') {
            if (!options.key) throw new Error('Key file required');
            
            let data;
            let filename = 'data.bin';
            
            if (options.text) {
                data = Buffer.from(options.text, 'utf8');
                filename = 'message.txt';
            } else if (options.file) {
                data = fs.readFileSync(options.file);
                filename = path.basename(options.file);
            } else {
                throw new Error('Text or file required');
            }
            
            const encrypted = encryptWithKey(data, options.key);
            
            if (options.output) {
                fs.writeFileSync(options.output, encrypted);
                console.log(`Encrypted to: ${options.output}`);
            } else {
                console.log(encrypted);
            }
            return;
        }
        
        if (options.mode === 'decrypt') {
            if (!options.key) throw new Error('Key file required');
            if (!options.text) throw new Error('Encrypted text required');
            
            const result = decryptWithKey(options.text, options.key);
            
            // Check if it's text or binary
            const text = result.data.toString('utf8');
            const isText = /^[\x20-\x7E\s]*$/.test(text);
            
            if (options.output) {
                fs.writeFileSync(options.output, result.data);
                console.log(`Decrypted to: ${options.output}`);
            } else if (isText) {
                console.log(text);
            } else {
                console.log('Binary data (use --output to save file)');
            }
            
            console.error(`Metadata: ${JSON.stringify(result.metadata)}`);
            return;
        }
        
        showUsage();
    } catch (error) {
        console.error(`Error: ${error.message}`);
        process.exit(1);
    }
}

// Mock crypto for Node.js compatibility
const crypto = require('crypto') || {
    randomBytes: (size) => {
        const buf = Buffer.alloc(size);
        for (let i = 0; i < size; i++) {
            buf[i] = Math.floor(Math.random() * 256);
        }
        return buf;
    }
};

main();
