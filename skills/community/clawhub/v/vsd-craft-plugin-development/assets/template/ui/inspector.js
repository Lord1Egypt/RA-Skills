'use strict';

(function () {
  const status = document.getElementById('status');
  const step = document.getElementById('step');
  const save = document.getElementById('save');
  let socket;
  let actionInfo;
  let inspectorUuid;

  function send(payload) {
    if (socket?.readyState !== WebSocket.OPEN) return;
    socket.send(JSON.stringify({event: 'sendToPlugin', action: actionInfo.action,
      context: inspectorUuid, payload: {...payload, actionContext: actionInfo.context}}));
  }
  function connect(port, uuid, registerEvent, info, rawActionInfo) {
    if (socket) socket.close();
    socket = undefined;
    step.disabled = save.disabled = true;
    try {
      actionInfo = JSON.parse(rawActionInfo);
      if (!actionInfo || typeof actionInfo.action !== 'string' || typeof actionInfo.context !== 'string') {
        throw new Error('Missing action instance');
      }
      inspectorUuid = uuid;
      step.value = String(actionInfo.payload?.settings?.step || 1);
      const connection = new WebSocket(`ws://127.0.0.1:${port}`);
      socket = connection;
      connection.onopen = () => {
        if (socket !== connection) return;
        connection.send(JSON.stringify({event: registerEvent, uuid}));
        step.disabled = save.disabled = false;
        status.textContent = 'Connected';
        send({op: 'get'});
      };
      connection.onmessage = (event) => {
        if (socket !== connection) return;
        try {
          const message = JSON.parse(event.data);
          if (message.event === 'sendToPropertyInspector') {
            step.value = String(message.payload.step);
            status.textContent = `Current value: ${message.payload.value}`;
          } else if (message.event === 'didReceiveSettings') {
            step.value = String(message.payload.settings.step || 1);
          }
        } catch { status.textContent = 'Could not read the settings response.'; }
      };
      connection.onclose = () => {
        if (socket !== connection) return;
        step.disabled = save.disabled = true;
        status.textContent = 'Connection closed. Reopen the settings panel.';
      };
      connection.onerror = () => {
        if (socket === connection) status.textContent = 'Could not connect to VSD Craft.';
      };
    } catch { status.textContent = 'Could not read the inspector launch information.'; }
  }
  save.addEventListener('click', () => {
    const value = Number(step.value);
    if (!Number.isInteger(value) || value < 1 || value > 100) {
      status.textContent = 'Enter an integer from 1 to 100.';
      return;
    }
    send({op: 'setStep', step: value});
  });
  window.connectElgatoStreamDeckSocket = connect;
  window.connectSocket = connect;
})();
