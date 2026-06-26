const http = require('http');

/**
 * Sony Bravia TV API client using IRCC-IP and REST API protocols.
 *
 * IRCC-IP: POST /sony/ircc with SOAP envelope (remote control buttons)
 * REST API: POST /sony/{service} with JSON-RPC (volume, input, power, etc.)
 */
class SonyTVClient {
  constructor(host, psk) {
    this.host = host;
    this.psk = psk;
  }

  _request(path, body) {
    return new Promise((resolve, reject) => {
      const data = JSON.stringify(body);
      const options = {
        hostname: this.host,
        port: 80,
        path,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(data),
          'X-Auth-PSK': this.psk,
        },
      };

      const req = http.request(options, (res) => {
        let chunks = '';
        res.on('data', (chunk) => (chunks += chunk));
        res.on('end', () => {
          try {
            resolve(JSON.parse(chunks));
          } catch {
            resolve({ raw: chunks, status: res.statusCode });
          }
        });
      });

      req.on('error', reject);
      req.setTimeout(5000, () => {
        req.destroy();
        reject(new Error('Request timeout'));
      });
      req.write(data);
      req.end();
    });
  }

  /** Send an IRCC remote control command */
  sendIRCC(irccCode) {
    const soapBody = `<?xml version="1.0"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1">
      <IRCCCode>${irccCode}</IRCCCode>
    </u:X_SendIRCC>
  </s:Body>
</s:Envelope>`;

    return new Promise((resolve, reject) => {
      const options = {
        hostname: this.host,
        port: 80,
        path: '/sony/ircc',
        method: 'POST',
        headers: {
          'Content-Type': 'text/xml; charset=utf-8',
          'SOAPACTION': '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"',
          'X-Auth-PSK': this.psk,
          'Content-Length': Buffer.byteLength(soapBody),
        },
      };

      const req = http.request(options, (res) => {
        let chunks = '';
        res.on('data', (chunk) => (chunks += chunk));
        res.on('end', () => resolve({ status: res.statusCode }));
      });

      req.on('error', reject);
      req.setTimeout(5000, () => {
        req.destroy();
        reject(new Error('IRCC timeout'));
      });
      req.write(soapBody);
      req.end();
    });
  }

  /** Power on */
  powerOn() {
    return this.sendIRCC('AAAAAQAAAAEAAAAuAw==');
  }

  /** Power off */
  powerOff() {
    return this.sendIRCC('AAAAAQAAAAEAAAAvAw==');
  }

  /** Toggle power */
  togglePower() {
    return this.sendIRCC('AAAAAQAAAAEAAAAVAw==');
  }

  // --- Navigation ---
  up() { return this.sendIRCC('AAAAAQAAAAEAAAB0Aw=='); }
  down() { return this.sendIRCC('AAAAAQAAAAEAAAB1Aw=='); }
  left() { return this.sendIRCC('AAAAAQAAAAEAAAA0Aw=='); }
  right() { return this.sendIRCC('AAAAAQAAAAEAAAAzAw=='); }
  confirm() { return this.sendIRCC('AAAAAQAAAAEAAABlAw=='); }
  home() { return this.sendIRCC('AAAAAQAAAAEAAABgAw=='); }
  exit() { return this.sendIRCC('AAAAAQAAAAEAAABjAw=='); }
  options() { return this.sendIRCC('AAAAAgAAAJcAAAA2Aw=='); }
  back() { return this.sendIRCC('AAAAAgAAAJcAAAAjAw=='); }

  // --- Volume ---
  volumeUp() { return this.sendIRCC('AAAAAQAAAAEAAAASAw=='); }
  volumeDown() { return this.sendIRCC('AAAAAQAAAAEAAAATAw=='); }
  mute() { return this.sendIRCC('AAAAAQAAAAEAAAAUAw=='); }

  // --- Channel ---
  channelUp() { return this.sendIRCC('AAAAAQAAAAEAAAAQAw=='); }
  channelDown() { return this.sendIRCC('AAAAAQAAAAEAAAARAw=='); }

  // --- Playback ---
  play() { return this.sendIRCC('AAAAAgAAAJcAAAAaAw=='); }
  pause() { return this.sendIRCC('AAAAAgAAAJcAAAAZAw=='); }
  stop() { return this.sendIRCC('AAAAAgAAAJcAAAAYAw=='); }
  rewind() { return this.sendIRCC('AAAAAgAAAJcAAAAbAw=='); }
  forward() { return this.sendIRCC('AAAAAgAAAJcAAAAcAw=='); }

  // --- HDMI Inputs ---
  hdmi1() { return this.sendIRCC('AAAAAgAAABoAAABaAw=='); }
  hdmi2() { return this.sendIRCC('AAAAAgAAABoAAABbAw=='); }
  hdmi3() { return this.sendIRCC('AAAAAgAAABoAAABcAw=='); }
  hdmi4() { return this.sendIRCC('AAAAAgAAABoAAABdAw=='); }

  // --- Open URL in TV browser ---
  openURL(url) {
    const uri = 'localapp://webappruntime?url=' + url;
    return this._request('/sony/appControl', {
      method: 'setActiveApp',
      params: [{ uri, data: '' }],
      id: 1,
      version: '1.0',
    });
  }

  // --- Kill/Terminate all running apps ---
  terminateApps() {
    return this._request('/sony/appControl', {
      method: 'terminateApps',
      params: [],
      id: 1,
      version: '1.0',
    });
  }

  // --- Get current volume ---
  async getVolume() {
    const result = await this._request('/sony/audio', {
      method: 'getVolumeInformation',
      params: [
        {
          target: 'speaker',
        },
      ],
      id: 1,
      version: '1.0',
    });
    return result;
  }

  /** Get current power status */
  async getPowerStatus() {
    const result = await this._request('/sony/system', {
      method: 'getPowerStatus',
      params: [],
      id: 1,
      version: '1.0',
    });
    return result;
  }

  /** Get current input */
  async getCurrentInput() {
    const result = await this._request('/sony/avContent', {
      method: 'getPlayingContentInfo',
      params: [],
      id: 1,
      version: '1.0',
    });
    return result;
  }

  /** Set volume (REST API, if supported) */
  async setVolume(target, volume) {
    return this._request('/sony/audio', {
      method: 'setAudioVolume',
      params: [
        {
          target,
          volume: String(volume),
        },
      ],
      id: 1,
      version: '1.0',
    });
  }
}

module.exports = SonyTVClient;
