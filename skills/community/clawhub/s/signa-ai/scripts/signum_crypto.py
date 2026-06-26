"""
signum_crypto.py — Pure-Python local transaction signing for the Signum blockchain.

Ported faithfully from signumjs:
  packages/crypto/src/base/curve25519.ts
  packages/crypto/src/base/ec-kcdsa.ts

No external dependencies — stdlib only (hashlib).
"""

import hashlib


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _trunc16(v):
    """JavaScript (v / 0x10000) | 0  — truncate toward zero, then take lower 32 bits."""
    return int(v / 0x10000)


def _to_int32(v):
    """Truncate Python int to 32-bit signed integer (mirrors JS | 0 and << behavior)."""
    v = v & 0xFFFFFFFF
    if v >= 0x80000000:
        v -= 0x100000000
    return v


def _sar32(v, n):
    """Arithmetic right shift of a 32-bit signed integer by n bits (mirrors JS >>)."""
    # Ensure v is int32 first
    v = _to_int32(v)
    if v < 0:
        # Python arithmetic right shift preserves sign on arbitrary-precision ints
        return v >> n
    return v >> n


def _sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


# ---------------------------------------------------------------------------
# Curve25519
# ---------------------------------------------------------------------------

class Curve25519:
    KEY_SIZE     = 32
    UNPACKED_SIZE = 16   # JS Uint16Array of 16 elements

    # group order (a prime near 2^252+2^124)
    ORDER = [
        237, 211, 245,  92,
         26,  99,  18,  88,
        214, 156, 247, 162,
        222, 249, 222,  20,
          0,   0,   0,   0,
          0,   0,   0,   0,
          0,   0,   0,   0,
          0,   0,   0,  16,
    ]

    # smallest multiple of the order that's >= 2^255
    ORDER_TIMES_8 = [
        104, 159, 174, 231,
        210,  24, 147, 192,
        178, 230, 188,  23,
        245, 206, 247, 166,
          0,   0,   0,   0,
          0,   0,   0,   0,
          0,   0,   0,   0,
          0,   0,   0, 128,
    ]

    # constants 2Gy and 1/(2Gy) — 16-element unpacked arrays
    BASE_2Y = [
        22587,   610, 29883, 44076,
        15515,  9479, 25859, 56197,
        23910,  4462, 17831, 16322,
        62102, 36542, 52412, 16035,
    ]

    BASE_R2Y = [
         5744, 16384, 61977, 54121,
         8776, 18501, 26522, 34893,
        23833,  5823, 55924, 58749,
        24147, 14085, 13606,  6080,
    ]

    C1      = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    C9      = [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    C486671 = [0x6D0F, 0x0007, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    C39420360 = [0x81C8, 0x0259, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    P25 = 33554431   # (1 << 25) - 1
    P26 = 67108863   # (1 << 26) - 1

    # ------------------------------------------------------------------
    # Key agreement
    # ------------------------------------------------------------------

    @staticmethod
    def clamp(k):
        k[31] &= 0x7F
        k[31] |= 0x40
        k[0]  &= 0xF8

    # ------------------------------------------------------------------
    # radix 2^8 math
    # ------------------------------------------------------------------

    @staticmethod
    def cpy32(d, s):
        for i in range(32):
            d[i] = s[i]

    @staticmethod
    def mula_small(p, q, m, x, n, z):
        """p[m..n+m-1] = q[m..n+m-1] + z * x;  returns carry."""
        v = 0
        for i in range(n):
            v += (q[i + m] & 0xFF) + z * (x[i] & 0xFF)
            p[i + m] = v & 0xFF
            v >>= 8
        return v

    @staticmethod
    def mula32(p, x, y, t, z):
        """p += x * y * z  where z is small; x size 32, y size t, p size 32+t."""
        n = 31
        w = 0
        i = 0
        for i in range(t):
            zy = z * (y[i] & 0xFF)
            w += Curve25519.mula_small(p, p, i, x, n, zy) + (p[i + n] & 0xFF) + zy * (x[n] & 0xFF)
            p[i + n] = w & 0xFF
            w >>= 8
        # In JS, the for-loop exits with i = t (post-increment), not t-1
        # So the final assignment uses p[t + n], not p[(t-1) + n]
        i = t
        p[i + n] = (w + (p[i + n] & 0xFF)) & 0xFF
        return w >> 8

    @staticmethod
    def divmod(q, r, n, d, t):
        """Divide r (size n) by d (size t); quotient in q, remainder in r."""
        rn = 0
        dt = (d[t - 1] & 0xFF) << 8
        if t > 1:
            dt |= (d[t - 2] & 0xFF)
        while n >= t:
            n -= 1
            z = (rn << 16) | ((r[n] & 0xFF) << 8)
            if n > 0:
                z |= (r[n - 1] & 0xFF)
            i = n - t + 1
            z = int(z / dt)   # truncate toward zero
            rn += Curve25519.mula_small(r, r, i, d, t, -z)
            q[i] = (z + rn) & 0xFF
            Curve25519.mula_small(r, r, i, d, t, -rn)
            rn = r[n] & 0xFF
            r[n] = 0
        r[t - 1] = rn & 0xFF

    @staticmethod
    def numsize(x, n):
        while n != 0 and x[n - 1] == 0:
            n -= 1
        return n

    @staticmethod
    def egcd32(x, y, a, b):
        """Extended GCD; returns x or y holding inv(a) mod b as 32-byte signed."""
        for i in range(32):
            x[i] = y[i] = 0
        x[0] = 1
        an = Curve25519.numsize(a, 32)
        if an == 0:
            return y
        bn = 32
        temp = [0] * 32
        while True:
            qn = bn - an + 1
            Curve25519.divmod(temp, b, bn, a, an)
            bn = Curve25519.numsize(b, bn)
            if bn == 0:
                return x
            Curve25519.mula32(y, x, temp, qn, -1)

            qn = an - bn + 1
            Curve25519.divmod(temp, a, an, b, bn)
            an = Curve25519.numsize(a, an)
            if an == 0:
                return y
            Curve25519.mula32(x, y, temp, qn, -1)

    # ------------------------------------------------------------------
    # radix 2^25.5 GF(2^255-19) math — pack / unpack
    # ------------------------------------------------------------------

    @staticmethod
    def createUnpackedArray():
        """16-element list of ints (mirrors Uint16Array)."""
        return [0] * 16

    @staticmethod
    def unpack(x, m):
        """Convert 32-byte little-endian list to internal 16-element form."""
        for i in range(0, Curve25519.KEY_SIZE, 2):
            x[i // 2] = (m[i] & 0xFF) | ((m[i + 1] & 0xFF) << 8)

    @staticmethod
    def is_overflow(x):
        return (
            (x[0] > Curve25519.P26 - 19)
            and (x[1] & x[3] & x[5] & x[7] & x[9]) == Curve25519.P25
            and (x[2] & x[4] & x[6] & x[8]) == Curve25519.P26
        ) or (x[9] > Curve25519.P25)

    @staticmethod
    def pack(x, m):
        """Convert internal 16-element form to 32-byte little-endian list."""
        # Ensure m has 32 slots
        while len(m) < 32:
            m.append(0)
        for i in range(Curve25519.UNPACKED_SIZE):
            if 2 * i >= len(m):
                m.append(x[i] & 0x00FF)
            else:
                m[2 * i] = x[i] & 0x00FF
            if 2 * i + 1 >= len(m):
                m.append((x[i] & 0xFF00) >> 8)
            else:
                m[2 * i + 1] = (x[i] & 0xFF00) >> 8

    @staticmethod
    def cpy(d, s):
        for i in range(Curve25519.UNPACKED_SIZE):
            d[i] = s[i]

    @staticmethod
    def set(d, s):
        d[0] = s
        for i in range(1, Curve25519.UNPACKED_SIZE):
            d[i] = 0

    # ------------------------------------------------------------------
    # Field arithmetic
    # ------------------------------------------------------------------

    @staticmethod
    def c255lsqr8h(a7, a6, a5, a4, a3, a2, a1, a0):
        r = [0] * 16
        v = a0 * a0
        r[0] = v & 0xFFFF

        v = _trunc16(v) + 2 * a0 * a1
        r[1] = v & 0xFFFF

        v = _trunc16(v) + 2 * a0 * a2 + a1 * a1
        r[2] = v & 0xFFFF

        v = _trunc16(v) + 2 * a0 * a3 + 2 * a1 * a2
        r[3] = v & 0xFFFF

        v = _trunc16(v) + 2 * a0 * a4 + 2 * a1 * a3 + a2 * a2
        r[4] = v & 0xFFFF

        v = _trunc16(v) + 2 * a0 * a5 + 2 * a1 * a4 + 2 * a2 * a3
        r[5] = v & 0xFFFF

        v = _trunc16(v) + 2 * a0 * a6 + 2 * a1 * a5 + 2 * a2 * a4 + a3 * a3
        r[6] = v & 0xFFFF

        v = _trunc16(v) + 2 * a0 * a7 + 2 * a1 * a6 + 2 * a2 * a5 + 2 * a3 * a4
        r[7] = v & 0xFFFF

        v = _trunc16(v) + 2 * a1 * a7 + 2 * a2 * a6 + 2 * a3 * a5 + a4 * a4
        r[8] = v & 0xFFFF

        v = _trunc16(v) + 2 * a2 * a7 + 2 * a3 * a6 + 2 * a4 * a5
        r[9] = v & 0xFFFF

        v = _trunc16(v) + 2 * a3 * a7 + 2 * a4 * a6 + a5 * a5
        r[10] = v & 0xFFFF

        v = _trunc16(v) + 2 * a4 * a7 + 2 * a5 * a6
        r[11] = v & 0xFFFF

        v = _trunc16(v) + 2 * a5 * a7 + a6 * a6
        r[12] = v & 0xFFFF

        v = _trunc16(v) + 2 * a6 * a7
        r[13] = v & 0xFFFF

        v = _trunc16(v) + a7 * a7
        r[14] = v & 0xFFFF

        r[15] = _trunc16(v)
        return r

    @staticmethod
    def sqr(r, a):
        x = Curve25519.c255lsqr8h(a[15], a[14], a[13], a[12], a[11], a[10], a[9], a[8])
        z = Curve25519.c255lsqr8h(a[7],  a[6],  a[5],  a[4],  a[3],  a[2],  a[1], a[0])
        y = Curve25519.c255lsqr8h(
            a[15] + a[7], a[14] + a[6], a[13] + a[5], a[12] + a[4],
            a[11] + a[3], a[10] + a[2], a[9]  + a[1], a[8]  + a[0],
        )

        v = 0x800000 + z[0] + (y[8] - x[8] - z[8] + x[0] - 0x80) * 38
        r[0] = v & 0xFFFF

        for i in range(1, 8):
            v = 0x7fff80 + _trunc16(v) + z[i] + (y[8 + i] - x[8 + i] - z[8 + i] + x[i]) * 38
            r[i] = v & 0xFFFF

        v = 0x7fff80 + _trunc16(v) + z[8] + y[0] - x[0] - z[0] + x[8] * 38
        r[8] = v & 0xFFFF

        for i in range(9, 15):
            v = 0x7fff80 + _trunc16(v) + z[i] + y[i - 8] - x[i - 8] - z[i - 8] + x[i] * 38
            r[i] = v & 0xFFFF

        r15 = 0x7fff80 + _trunc16(v) + z[15] + y[7] - x[7] - z[7] + x[15] * 38
        Curve25519.c255lreduce(r, r15)

    @staticmethod
    def c255lmul8h(a7, a6, a5, a4, a3, a2, a1, a0,
                   b7, b6, b5, b4, b3, b2, b1, b0):
        r = [0] * 16
        v = a0 * b0
        r[0] = v & 0xFFFF

        v = _trunc16(v) + a0 * b1 + a1 * b0
        r[1] = v & 0xFFFF

        v = _trunc16(v) + a0 * b2 + a1 * b1 + a2 * b0
        r[2] = v & 0xFFFF

        v = _trunc16(v) + a0 * b3 + a1 * b2 + a2 * b1 + a3 * b0
        r[3] = v & 0xFFFF

        v = _trunc16(v) + a0 * b4 + a1 * b3 + a2 * b2 + a3 * b1 + a4 * b0
        r[4] = v & 0xFFFF

        v = _trunc16(v) + a0 * b5 + a1 * b4 + a2 * b3 + a3 * b2 + a4 * b1 + a5 * b0
        r[5] = v & 0xFFFF

        v = _trunc16(v) + a0 * b6 + a1 * b5 + a2 * b4 + a3 * b3 + a4 * b2 + a5 * b1 + a6 * b0
        r[6] = v & 0xFFFF

        v = (_trunc16(v) + a0 * b7 + a1 * b6 + a2 * b5 + a3 * b4
             + a4 * b3 + a5 * b2 + a6 * b1 + a7 * b0)
        r[7] = v & 0xFFFF

        v = _trunc16(v) + a1 * b7 + a2 * b6 + a3 * b5 + a4 * b4 + a5 * b3 + a6 * b2 + a7 * b1
        r[8] = v & 0xFFFF

        v = _trunc16(v) + a2 * b7 + a3 * b6 + a4 * b5 + a5 * b4 + a6 * b3 + a7 * b2
        r[9] = v & 0xFFFF

        v = _trunc16(v) + a3 * b7 + a4 * b6 + a5 * b5 + a6 * b4 + a7 * b3
        r[10] = v & 0xFFFF

        v = _trunc16(v) + a4 * b7 + a5 * b6 + a6 * b5 + a7 * b4
        r[11] = v & 0xFFFF

        v = _trunc16(v) + a5 * b7 + a6 * b6 + a7 * b5
        r[12] = v & 0xFFFF

        v = _trunc16(v) + a6 * b7 + a7 * b6
        r[13] = v & 0xFFFF

        v = _trunc16(v) + a7 * b7
        r[14] = v & 0xFFFF

        r[15] = _trunc16(v)
        return r

    @staticmethod
    def mul(r, a, b):
        x = Curve25519.c255lmul8h(
            a[15], a[14], a[13], a[12], a[11], a[10], a[9], a[8],
            b[15], b[14], b[13], b[12], b[11], b[10], b[9], b[8],
        )
        z = Curve25519.c255lmul8h(
            a[7], a[6], a[5], a[4], a[3], a[2], a[1], a[0],
            b[7], b[6], b[5], b[4], b[3], b[2], b[1], b[0],
        )
        y = Curve25519.c255lmul8h(
            a[15] + a[7], a[14] + a[6], a[13] + a[5], a[12] + a[4],
            a[11] + a[3], a[10] + a[2], a[9]  + a[1], a[8]  + a[0],
            b[15] + b[7], b[14] + b[6], b[13] + b[5], b[12] + b[4],
            b[11] + b[3], b[10] + b[2], b[9]  + b[1], b[8]  + b[0],
        )

        v = 0x800000 + z[0] + (y[8] - x[8] - z[8] + x[0] - 0x80) * 38
        r[0] = v & 0xFFFF

        for i in range(1, 8):
            v = 0x7fff80 + _trunc16(v) + z[i] + (y[8 + i] - x[8 + i] - z[8 + i] + x[i]) * 38
            r[i] = v & 0xFFFF

        v = 0x7fff80 + _trunc16(v) + z[8] + y[0] - x[0] - z[0] + x[8] * 38
        r[8] = v & 0xFFFF

        for i in range(9, 15):
            v = 0x7fff80 + _trunc16(v) + z[i] + y[i - 8] - x[i - 8] - z[i - 8] + x[i] * 38
            r[i] = v & 0xFFFF

        r15 = 0x7fff80 + _trunc16(v) + z[15] + y[7] - x[7] - z[7] + x[15] * 38
        Curve25519.c255lreduce(r, r15)

    @staticmethod
    def c255lreduce(a, a15):
        v = a15
        a[15] = v & 0x7FFF
        v = _trunc16(v >> 15) * 19     # (v / 0x8000) | 0  then * 19
        # re-express: _trunc16(v >> 15) is wrong — need trunc(v / 0x8000)
        # Redo: the JS is  ((v / 0x8000) | 0) * 19
        # We already did a[15] = v & 0x7FFF, now carry = trunc(v / 0x8000)
        carry = int(a15 / 0x8000)   # truncate-toward-zero division
        a[15] = a15 & 0x7FFF
        v = carry * 19
        for i in range(15):
            v += a[i]
            a[i] = v & 0xFFFF
            v = _trunc16(v)
        a[15] += v

    @staticmethod
    def add(r, a, b):
        v = (int(a[15] / 0x8000) + int(b[15] / 0x8000)) * 19 + a[0] + b[0]
        r[0] = v & 0xFFFF
        for i in range(1, 15):
            v = _trunc16(v) + a[i] + b[i]
            r[i] = v & 0xFFFF
        r[15] = _trunc16(v) + (a[15] & 0x7FFF) + (b[15] & 0x7FFF)

    @staticmethod
    def sub(r, a, b):
        v = 0x80000 + (int(a[15] / 0x8000) - int(b[15] / 0x8000) - 1) * 19 + a[0] - b[0]
        r[0] = v & 0xFFFF
        for i in range(1, 15):
            v = _trunc16(v) + 0x7fff8 + a[i] - b[i]
            r[i] = v & 0xFFFF
        r[15] = _trunc16(v) + 0x7ff8 + (a[15] & 0x7FFF) - (b[15] & 0x7FFF)

    @staticmethod
    def mul_small(r, a, m):
        v = a[0] * m
        r[0] = v & 0xFFFF
        for i in range(1, 15):
            v = _trunc16(v) + a[i] * m
            r[i] = v & 0xFFFF
        r15 = _trunc16(v) + a[15] * m
        Curve25519.c255lreduce(r, r15)

    @staticmethod
    def recip(y, x, sqrtassist):
        """y = x^(p-2)  or  x^((p-5)/8) when sqrtassist."""
        t0 = Curve25519.createUnpackedArray()
        t1 = Curve25519.createUnpackedArray()
        t2 = Curve25519.createUnpackedArray()
        t3 = Curve25519.createUnpackedArray()
        t4 = Curve25519.createUnpackedArray()

        Curve25519.sqr(t1, x)           #  2
        Curve25519.sqr(t2, t1)          #  4
        Curve25519.sqr(t0, t2)          #  8
        Curve25519.mul(t2, t0, x)       #  9
        Curve25519.mul(t0, t2, t1)      # 11
        Curve25519.sqr(t1, t0)          # 22
        Curve25519.mul(t3, t1, t2)      # 31 = 2^5 - 2^0
        Curve25519.sqr(t1, t3)          # 2^6  - 2^1
        Curve25519.sqr(t2, t1)          # 2^7  - 2^2
        Curve25519.sqr(t1, t2)          # 2^8  - 2^3
        Curve25519.sqr(t2, t1)          # 2^9  - 2^4
        Curve25519.sqr(t1, t2)          # 2^10 - 2^5
        Curve25519.mul(t2, t1, t3)      # 2^10 - 2^0
        Curve25519.sqr(t1, t2)          # 2^11 - 2^1
        Curve25519.sqr(t3, t1)          # 2^12 - 2^2
        for _ in range(1, 5):
            Curve25519.sqr(t1, t3)
            Curve25519.sqr(t3, t1)
        # t3 = 2^20 - 2^10
        Curve25519.mul(t1, t3, t2)      # 2^20 - 2^0
        Curve25519.sqr(t3, t1)          # 2^21 - 2^1
        Curve25519.sqr(t4, t3)          # 2^22 - 2^2
        for _ in range(1, 10):
            Curve25519.sqr(t3, t4)
            Curve25519.sqr(t4, t3)
        # t4 = 2^40 - 2^20
        Curve25519.mul(t3, t4, t1)      # 2^40 - 2^0
        for _ in range(5):
            Curve25519.sqr(t1, t3)
            Curve25519.sqr(t3, t1)
        # t3 = 2^50 - 2^10
        Curve25519.mul(t1, t3, t2)      # 2^50 - 2^0
        Curve25519.sqr(t2, t1)          # 2^51 - 2^1
        Curve25519.sqr(t3, t2)          # 2^52 - 2^2
        for _ in range(1, 25):
            Curve25519.sqr(t2, t3)
            Curve25519.sqr(t3, t2)
        # t3 = 2^100 - 2^50
        Curve25519.mul(t2, t3, t1)      # 2^100 - 2^0
        Curve25519.sqr(t3, t2)          # 2^101 - 2^1
        Curve25519.sqr(t4, t3)          # 2^102 - 2^2
        for _ in range(1, 50):
            Curve25519.sqr(t3, t4)
            Curve25519.sqr(t4, t3)
        # t4 = 2^200 - 2^100
        Curve25519.mul(t3, t4, t2)      # 2^200 - 2^0
        for _ in range(25):
            Curve25519.sqr(t4, t3)
            Curve25519.sqr(t3, t4)
        # t3 = 2^250 - 2^50
        Curve25519.mul(t2, t3, t1)      # 2^250 - 2^0
        Curve25519.sqr(t1, t2)          # 2^251 - 2^1
        Curve25519.sqr(t2, t1)          # 2^252 - 2^2
        if sqrtassist != 0:
            Curve25519.mul(y, x, t2)    # 2^252 - 3
        else:
            Curve25519.sqr(t1, t2)      # 2^253 - 2^3
            Curve25519.sqr(t2, t1)      # 2^254 - 2^4
            Curve25519.sqr(t1, t2)      # 2^255 - 2^5
            Curve25519.mul(y, t1, t0)   # 2^255 - 21

    @staticmethod
    def is_negative(x):
        isOverflowOrNegative = Curve25519.is_overflow(x) or x[9] < 0
        lsb = x[0] & 1
        return ((1 if isOverflowOrNegative else 0) ^ lsb) & 0xFFFFFFFF

    @staticmethod
    def sqrt(x, u):
        v  = Curve25519.createUnpackedArray()
        t1 = Curve25519.createUnpackedArray()
        t2 = Curve25519.createUnpackedArray()
        Curve25519.add(t1, u, u)            # t1 = 2u
        Curve25519.recip(v, t1, 1)          # v  = (2u)^((p-5)/8)
        Curve25519.sqr(x, v)                # x  = v^2
        Curve25519.mul(t2, t1, x)           # t2 = 2uv^2
        Curve25519.sub(t2, t2, Curve25519.C1)  # t2 = 2uv^2-1
        Curve25519.mul(t1, v, t2)           # t1 = v(2uv^2-1)
        Curve25519.mul(x, u, t1)            # x  = uv(2uv^2-1)

    # ------------------------------------------------------------------
    # Montgomery ladder
    # ------------------------------------------------------------------

    @staticmethod
    def mont_prep(t1, t2, ax, az):
        Curve25519.add(t1, ax, az)
        Curve25519.sub(t2, ax, az)

    @staticmethod
    def mont_add(t1, t2, t3, t4, ax, az, dx):
        Curve25519.mul(ax, t2, t3)
        Curve25519.mul(az, t1, t4)
        Curve25519.add(t1, ax, az)
        Curve25519.sub(t2, ax, az)
        Curve25519.sqr(ax, t1)
        Curve25519.sqr(t1, t2)
        Curve25519.mul(az, t1, dx)

    @staticmethod
    def mont_dbl(t1, t2, t3, t4, bx, bz):
        Curve25519.sqr(t1, t3)
        Curve25519.sqr(t2, t4)
        Curve25519.mul(bx, t1, t2)
        Curve25519.sub(t2, t1, t2)
        Curve25519.mul_small(bz, t2, 121665)
        Curve25519.add(t1, t1, bz)
        Curve25519.mul(bz, t1, t2)

    @staticmethod
    def x_to_y2(t, y2, x):
        Curve25519.sqr(t, x)
        Curve25519.mul_small(y2, x, 486662)
        Curve25519.add(t, t, y2)
        Curve25519.add(t, t, Curve25519.C1)
        Curve25519.mul(y2, t, x)

    @staticmethod
    def core(Px, s, k, Gx):
        """P = kG  and  s = sign(P)/k  (s may be None)."""
        dx = Curve25519.createUnpackedArray()
        t1 = Curve25519.createUnpackedArray()
        t2 = Curve25519.createUnpackedArray()
        t3 = Curve25519.createUnpackedArray()
        t4 = Curve25519.createUnpackedArray()
        x  = [Curve25519.createUnpackedArray(), Curve25519.createUnpackedArray()]
        z  = [Curve25519.createUnpackedArray(), Curve25519.createUnpackedArray()]

        if Gx is not None:
            Curve25519.unpack(dx, Gx)
        else:
            Curve25519.set(dx, 9)

        Curve25519.set(x[0], 1)
        Curve25519.set(z[0], 0)
        Curve25519.cpy(x[1], dx)
        Curve25519.set(z[1], 1)

        for i in range(31, -1, -1):
            for j in range(7, -1, -1):
                bit1 = (k[i] & 0xFF) >> j & 1
                bit0 = (~(k[i] & 0xFF)) >> j & 1
                ax = x[bit0]; az = z[bit0]
                bx = x[bit1]; bz = z[bit1]

                Curve25519.mont_prep(t1, t2, ax, az)
                Curve25519.mont_prep(t3, t4, bx, bz)
                Curve25519.mont_add(t1, t2, t3, t4, ax, az, dx)
                Curve25519.mont_dbl(t1, t2, t3, t4, bx, bz)

        Curve25519.recip(t1, z[0], 0)
        Curve25519.mul(dx, x[0], t1)
        Curve25519.pack(dx, Px)

        if s is not None:
            Curve25519.x_to_y2(t2, t1, dx)          # t1 = Py^2
            Curve25519.recip(t3, z[1], 0)
            Curve25519.mul(t2, x[1], t3)             # t2 = Qx
            Curve25519.add(t2, t2, dx)               # t2 = Qx + Px
            Curve25519.add(t2, t2, Curve25519.C486671)   # t2 = Qx + Px + Gx + 486662
            Curve25519.sub(dx, dx, Curve25519.C9)         # dx = Px - Gx
            Curve25519.sqr(t3, dx)                    # t3 = (Px - Gx)^2
            Curve25519.mul(dx, t2, t3)                # dx = t2*(Px - Gx)^2
            Curve25519.sub(dx, dx, t1)                # dx -= Py^2
            Curve25519.sub(dx, dx, Curve25519.C39420360)  # dx -= Gy^2
            Curve25519.mul(t1, dx, Curve25519.BASE_R2Y)   # t1 = -Py

            if Curve25519.is_negative(t1) != 0:
                Curve25519.cpy32(s, k)
            else:
                Curve25519.mula_small(s, Curve25519.ORDER_TIMES_8, 0, k, 32, -1)

            temp1 = [0] * 32
            temp2 = [0] * 64
            temp3 = [0] * 64
            Curve25519.cpy32(temp1, Curve25519.ORDER)
            result = Curve25519.egcd32(temp2, temp3, s, temp1)
            Curve25519.cpy32(s, result)
            if (s[31] & 0x80) != 0:
                Curve25519.mula_small(s, s, 0, Curve25519.ORDER, 32, 1)


# ---------------------------------------------------------------------------
# ECKCDSA
# ---------------------------------------------------------------------------

class ECKCDSA:

    @staticmethod
    def sign(h, x, s):
        """v = (x - h) * s mod q.  Returns 32-byte list or None."""
        h1 = [0] * 32
        x1 = [0] * 32
        tmp1 = [0] * 64
        tmp2 = [0] * 64

        Curve25519.cpy32(h1, h)
        Curve25519.cpy32(x1, x)

        tmp3 = [0] * 32
        Curve25519.divmod(tmp3, h1, 32, Curve25519.ORDER, 32)
        Curve25519.divmod(tmp3, x1, 32, Curve25519.ORDER, 32)

        v = [0] * 32
        Curve25519.mula_small(v, x1, 0, h1, 32, -1)
        Curve25519.mula_small(v, v,  0, Curve25519.ORDER, 32, 1)

        Curve25519.mula32(tmp1, v, s, 32, 1)
        Curve25519.divmod(tmp2, tmp1, 64, Curve25519.ORDER, 32)

        w = 0
        for i in range(32):
            v[i] = tmp1[i]
            w |= v[i]

        return v if w != 0 else None

    @staticmethod
    def verify(v, h, P):
        """Y = v*P + h*G — returns Y as 32-byte list."""
        d = [0] * 32
        p  = [Curve25519.createUnpackedArray(), Curve25519.createUnpackedArray()]
        s  = [Curve25519.createUnpackedArray(), Curve25519.createUnpackedArray()]
        yx = [Curve25519.createUnpackedArray(), Curve25519.createUnpackedArray(), Curve25519.createUnpackedArray()]
        yz = [Curve25519.createUnpackedArray(), Curve25519.createUnpackedArray(), Curve25519.createUnpackedArray()]
        t1 = [Curve25519.createUnpackedArray(), Curve25519.createUnpackedArray(), Curve25519.createUnpackedArray()]
        t2 = [Curve25519.createUnpackedArray(), Curve25519.createUnpackedArray(), Curve25519.createUnpackedArray()]

        vi = 0; hi = 0; di = 0; nvh = 0

        Curve25519.set(p[0], 9)
        Curve25519.unpack(p[1], P)

        Curve25519.x_to_y2(t1[0], t2[0], p[1])           # t2[0] = Py^2
        Curve25519.sqrt(t1[0], t2[0])                     # t1[0] = Py or -Py
        j = Curve25519.is_negative(t1[0])
        Curve25519.add(t2[0], t2[0], Curve25519.C39420360)   # t2[0] = Py^2 + Gy^2
        Curve25519.mul(t2[1], Curve25519.BASE_2Y, t1[0])     # t2[1] = ±2 Py Gy
        Curve25519.sub(t1[j],     t2[0], t2[1])
        Curve25519.add(t1[1 - j], t2[0], t2[1])
        Curve25519.cpy(t2[0], p[1])
        Curve25519.sub(t2[0], t2[0], Curve25519.C9)
        Curve25519.sqr(t2[1], t2[0])
        Curve25519.recip(t2[0], t2[1], 0)
        Curve25519.mul(s[0], t1[0], t2[0])
        Curve25519.sub(s[0], s[0], p[1])
        Curve25519.sub(s[0], s[0], Curve25519.C486671)
        Curve25519.mul(s[1], t1[1], t2[0])
        Curve25519.sub(s[1], s[1], p[1])
        Curve25519.sub(s[1], s[1], Curve25519.C486671)
        Curve25519.mul_small(s[0], s[0], 1)
        Curve25519.mul_small(s[1], s[1], 1)

        # Build chain
        for i in range(32):
            vi = (vi >> 8) ^ (v[i] & 0xFF) ^ ((v[i] & 0xFF) << 1)
            hi = (hi >> 8) ^ (h[i] & 0xFF) ^ ((h[i] & 0xFF) << 1)
            nvh = ~(vi ^ hi)
            di = (nvh & (di & 0x80) >> 7) ^ vi
            di ^= nvh & (di & 0x01) << 1
            di ^= nvh & (di & 0x02) << 1
            di ^= nvh & (di & 0x04) << 1
            di ^= nvh & (di & 0x08) << 1
            di ^= nvh & (di & 0x10) << 1
            di ^= nvh & (di & 0x20) << 1
            di ^= nvh & (di & 0x40) << 1
            d[i] = di & 0xFF

        di = ((nvh & (di & 0x80) << 1) ^ vi) >> 8

        Curve25519.set(yx[0], 1)
        Curve25519.cpy(yx[1], p[di])
        Curve25519.cpy(yx[2], s[0])
        Curve25519.set(yz[0], 0)
        Curve25519.set(yz[1], 1)
        Curve25519.set(yz[2], 1)

        vi = 0; hi = 0

        for i in range(31, -1, -1):
            # JS uses int32 arithmetic: << 8 truncates to 32 bits
            vi = _to_int32((vi << 8) | (v[i] & 0xFF))
            hi = _to_int32((hi << 8) | (h[i] & 0xFF))
            di = _to_int32((di << 8) | (d[i] & 0xFF))

            for j in range(7, -1, -1):
                Curve25519.mont_prep(t1[0], t2[0], yx[0], yz[0])
                Curve25519.mont_prep(t1[1], t2[1], yx[1], yz[1])
                Curve25519.mont_prep(t1[2], t2[2], yx[2], yz[2])

                k = ((_sar32(vi ^ _sar32(vi, 1), j) & 1)
                     + (_sar32(hi ^ _sar32(hi, 1), j) & 1))
                Curve25519.mont_dbl(yx[2], yz[2], t1[k], t2[k], yx[0], yz[0])

                k = (_sar32(di, j) & 2) ^ ((_sar32(di, j) & 1) << 1)
                Curve25519.mont_add(t1[1], t2[1], t1[k], t2[k], yx[1], yz[1],
                                    p[_sar32(di, j) & 1])

                Curve25519.mont_add(t1[2], t2[2], t1[0], t2[0], yx[2], yz[2],
                                    s[(_sar32(vi ^ hi, j) & 2) >> 1])

        k = (vi & 1) + (hi & 1)
        Curve25519.recip(t1[0], yz[k], 0)
        Curve25519.mul(t1[1], yx[k], t1[0])

        Y = []
        Curve25519.pack(t1[1], Y)
        return Y

    @staticmethod
    def keygen(k):
        """k is a list of 32 ints (bytes).  Returns {p, s, k}."""
        P = [0] * 32
        s = [0] * 32
        Curve25519.clamp(k)
        Curve25519.core(P, s, k, None)
        return {"p": P, "s": s, "k": k}


# ---------------------------------------------------------------------------
# High-level API
# ---------------------------------------------------------------------------

def generate_sign_keys(passphrase: str) -> dict:
    """
    Derive Signum sign keys from a passphrase.

    Returns dict with keys:
      publicKey         — hex string (32 bytes)
      signPrivateKey    — hex string (32 bytes)
      agreementPrivateKey — hex string (32 bytes)
    """
    hashed = list(_sha256(passphrase.encode("utf-8")))
    keys = ECKCDSA.keygen(hashed)
    return {
        "publicKey":          bytes(keys["p"]).hex(),
        "signPrivateKey":     bytes(keys["s"]).hex(),
        "agreementPrivateKey": bytes(keys["k"]).hex(),
    }


def generate_signature(message_hex: str, private_key_hex: str) -> str:
    """
    Sign a message (as hex) with the sign private key (as hex).

    Returns 64-byte signature as hex string.
    """
    m_bytes = bytes.fromhex(message_hex)
    m = list(_sha256(m_bytes))             # sha256 of raw message bytes

    s = list(bytes.fromhex(private_key_hex))

    x_bytes = _sha256(bytes(m) + bytes(s))
    x = list(x_bytes)

    # keygen clamps x in-place in JS; pass x directly so our copy is clamped too
    y_keys = ECKCDSA.keygen(x)            # clamps x in-place
    y = list(bytes(y_keys["p"]))

    h = list(_sha256(bytes(m) + bytes(y)))

    # x is now clamped (same as JS reference)
    v = ECKCDSA.sign(list(h), list(x), list(s))
    if v is None:
        raise ValueError("Signature generation failed — v is zero")

    return bytes(v).hex() + bytes(h).hex()


def verify_signature(signature_hex: str, message_hex: str, public_key_hex: str) -> bool:
    """
    Verify a Signum EC-KCDSA signature.

    signature_hex   — 128 hex chars (v||h, each 32 bytes)
    message_hex     — original message as hex
    public_key_hex  — public key as hex (32 bytes)

    Returns True if valid.
    """
    if len(signature_hex) != 128:
        return False

    v = list(bytes.fromhex(signature_hex[:64]))
    h = list(bytes.fromhex(signature_hex[64:]))
    P = list(bytes.fromhex(public_key_hex))

    m_bytes = bytes.fromhex(message_hex)
    m = list(_sha256(m_bytes))

    Y = ECKCDSA.verify(v, h, P)

    h2 = list(_sha256(bytes(m) + bytes(Y)))
    return h2 == h


def generate_signed_transaction_bytes(unsigned_hex: str, signature: str) -> str:
    """
    Embed a 64-byte signature into unsigned transaction bytes.

    The signature occupies bytes 64..128 (chars 128..256) of the transaction,
    i.e. chars 192..320 in the hex representation (96..160 byte range).

    Formula:  unsignedHex[:192] + signature + unsignedHex[320:]
    """
    return unsigned_hex[:192] + signature + unsigned_hex[320:]


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    PASSPHRASE   = "hope green dust squeeze bright catch crush tuna lend squeeze"
    MESSAGE_HEX  = "00" * 64   # 64 zero bytes — stand-in for an unsigned tx

    print("=== Signum Crypto Self-Test ===")
    print(f"Passphrase : {PASSPHRASE!r}")

    try:
        # Key generation
        keys = generate_sign_keys(PASSPHRASE)
        print(f"Public key : {keys['publicKey']}")
        print(f"Sign priv  : {keys['signPrivateKey']}")
        print(f"Agree priv : {keys['agreementPrivateKey']}")

        # Signing
        sig = generate_signature(MESSAGE_HEX, keys["signPrivateKey"])
        print(f"Signature  : {sig}")

        # Verification
        ok = verify_signature(sig, MESSAGE_HEX, keys["publicKey"])
        print(f"Verify     : {'PASS' if ok else 'FAIL'}")

        # Rejection test — flip one bit in signature
        bad_sig = (format(int(sig[:2], 16) ^ 1, "02x") + sig[2:])
        ok2 = verify_signature(bad_sig, MESSAGE_HEX, keys["publicKey"])
        print(f"Reject bad : {'PASS' if not ok2 else 'FAIL'}")

        if ok and not ok2:
            print("\nSELF-TEST: PASS")
            sys.exit(0)
        else:
            print("\nSELF-TEST: FAIL")
            sys.exit(1)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\nSELF-TEST: FAIL ({e})")
        sys.exit(1)
