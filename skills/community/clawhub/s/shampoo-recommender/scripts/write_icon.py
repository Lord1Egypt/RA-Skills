import base64, zlib, struct, os

signature = b'\x89PNG\r\n\x1a\n'

def crc32(data):
    return zlib.crc32(data) & 0xffffffff

def chunk(ctype, data):
    c = ctype.encode() + data
    return struct.pack('>I', len(data)) + c + struct.pack('>I', crc32(c))

ihdr = chunk('IHDR', struct.pack('>IIBBBBB', 512, 512, 8, 6, 0, 0, 0))

raw = []
for y in range(512):
    raw.append(0)
    for x in range(512):
        in_rounded = 20 <= x <= 492 and 20 <= y <= 492
        corners = (
            (x < 80 and y < 80 and ((80-x)**2 + (80-y)**2) > 6400) or
            (x > 432 and y < 80 and ((x-432)**2 + (80-y)**2) > 6400) or
            (x < 80 and y > 432 and ((80-x)**2 + (y-432)**2) > 6400) or
            (x > 432 and y > 432 and ((x-432)**2 + (y-432)**2) > 6400)
        )
        bg = in_rounded and not corners
        bottle_body = 170 <= x <= 342 and 180 <= y <= 400
        bottle_cap = 205 <= x <= 307 and 100 <= y <= 180
        bottle_neck = 220 <= x <= 292 and 85 <= y <= 110
        cx, cy = 256, 275
        dist = ((x-cx)**2 + ((y-cy)*1.5)**2) ** 0.5
        drop = 227 <= x <= 285 and 230 <= y <= 290 and dist <= 30
        bubbles = (
            ((x-120)**2 + (y-120)**2) <= 1600 or
            ((x-375)**2 + (y-135)**2) <= 1225 or
            ((x-400)**2 + (y-320)**2) <= 900 or
            ((x-105)**2 + (y-335)**2) <= 1225
        )
        if bubbles:
            raw.extend([200, 230, 255, 200])
        elif drop:
            raw.extend([180, 140, 255, 255])
        elif bottle_neck:
            raw.extend([200, 170, 240, 255])
        elif bottle_cap or bottle_body:
            raw.extend([255, 255, 255, 255])
        elif bg:
            raw.extend([138, 97, 214, 255])
        else:
            raw.extend([0, 0, 0, 0])

compressed = zlib.compress(bytes(raw), level=9)
png = signature + ihdr + chunk('IDAT', compressed) + chunk('IEND', b'')
out = r'C:\Users\chenyuxin\.qclaw\workspace\skills\shampoo-recommender\scripts\icon.png'
with open(out, 'wb') as f:
    f.write(png)
print('written', len(png), 'bytes to', out)
