import socket, time, struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)
sock.connect(('192.168.1.13', 5891))
sock.send(bytearray([0x01, 0x00, 0x00, 0x00, 0x00]))
time.sleep(0.3)
data = sock.recv(8192)
sock.close()

body = data[data.index(b'\n')+1:]
print(f'Body length: {len(body)} bytes')

# Parse all variables
pos = 0
count = 0
while pos < len(body) - 4 and count < 20:
    # Skip nulls
    while pos < len(body) and body[pos] == 0:
        pos += 1
    if pos >= len(body) - 4:
        break
    
    # Read name
    name_start = pos
    while pos < len(body) and body[pos] != 0:
        pos += 1
    name = body[name_start:pos].decode('ascii', errors='replace')
    pos += 1  # skip null after name
    
    if len(name) < 2 or not name[0].isalpha():
        continue
    
    # Read type
    if pos >= len(body):
        break
    type_code = body[pos]
    pos += 1
    
    # Skip null padding
    while pos < len(body) and body[pos] == 0:
        pos += 1
    
    # Read data based on type
    value = None
    data_len = 0
    if type_code == 0x01:  # bool
        value = body[pos] != 0 if pos < len(body) else False
        data_len = 1
    elif type_code == 0x04:  # int32
        if pos + 4 <= len(body):
            value = int.from_bytes(body[pos:pos+4], 'little')
            data_len = 4
    elif type_code == 0x18:  # 6 floats
        if pos + 24 <= len(body):
            value = struct.unpack('<6f', body[pos:pos+24])
            data_len = 24
    elif type_code == 0x08:  # string
        str_start = pos
        while pos < len(body) and body[pos] != 0:
            pos += 1
        value = body[str_start:pos].decode('ascii', errors='replace')
        data_len = pos - str_start
    else:
        # Unknown type - skip
        pass
    
    if value is not None:
        print(f'{name:25s} type=0x{type_code:02x} ({type_code:3d}) data_len={data_len} = {value}')
        count += 1
    
    pos += data_len
