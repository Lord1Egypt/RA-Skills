#!/usr/bin/env python3
"""
TurboQuant: Fast Vector Quantization for Large-Scale Retrieval
Implementation of ICLR 2026 paper by Google Research

Two-stage quantization:
1. TurboQuant_mse: MSE-optimal quantization with SRHT rotation
2. TurboQuant_prod: Unbiased inner product estimation with SRHT residual sketch
"""

import math
from typing import Dict, List, Tuple

import numpy as np


def fwht_batch(X: np.ndarray) -> np.ndarray:
    """
    Fast Walsh-Hadamard Transform on rows of X.
    Each row must have length 2^k. Normalizes by 1/sqrt(n).
    """
    X = X.copy()
    n = X.shape[-1]
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            u = X[..., i:i+h].copy()
            v = X[..., i+h:i+2*h].copy()
            X[..., i:i+h] = u + v
            X[..., i+h:i+2*h] = u - v
        h *= 2
    X /= np.sqrt(n)
    return X


def fwht(x: np.ndarray) -> np.ndarray:
    """Fast Walsh-Hadamard Transform. Input length must be 2^k."""
    if x.ndim == 1:
        return fwht_batch(x[np.newaxis])[0]
    return fwht_batch(x)


def norm_pdf(x: np.ndarray) -> np.ndarray:
    """Standard normal PDF."""
    return np.exp(-0.5 * x**2) / np.sqrt(2 * np.pi)


def norm_cdf(x: np.ndarray) -> np.ndarray:
    """Standard normal CDF using erf."""
    return 0.5 * (1.0 + _erf_vec(x / np.sqrt(2.0)))


def _erf_scalar(x: float) -> float:
    """Abramowitz-Stegun erf approximation (max error ~1.5e-7)."""
    a1, a2, a3, a4, a5 = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429
    p = 0.3275911
    sign = 1.0 if x >= 0 else -1.0
    x = abs(x)
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return sign * y


def _erf_vec(x: np.ndarray) -> np.ndarray:
    """Vectorized erf via Abramowitz-Stegun."""
    a1, a2, a3, a4, a5 = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429
    p = 0.3275911
    sign = np.sign(x)
    x_abs = np.abs(x)
    t = 1.0 / (1.0 + p * x_abs)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * np.exp(-x_abs * x_abs)
    return sign * y


# fmt: off
LLOYD_MAX_CODEBOOKS: Dict[int, np.ndarray] = {
    4: np.array([
        -2.732590, -2.069017, -1.618046, -1.256231, -0.942340, -0.656759, -0.388048, -0.128395,
         0.128395,  0.388048,  0.656759,  0.942340,  1.256231,  1.618046,  2.069017,  2.732590,
    ]),
    5: np.array([
        -3.255551, -2.685242, -2.311436, -2.022176, -1.780581, -1.569615, -1.379897, -1.205655,
        -1.043047, -0.889350, -0.742542, -0.601049, -0.463598, -0.329119, -0.196679, -0.065429,
         0.065429,  0.196679,  0.329119,  0.463598,  0.601049,  0.742542,  0.889350,  1.043047,
         1.205655,  1.379897,  1.569615,  1.780581,  2.022176,  2.311436,  2.685242,  3.255551,
    ]),
    6: np.array([
        -3.605999, -3.085722, -2.751095, -2.496953, -2.288778, -2.110705, -1.954065, -1.813578,
        -1.685776, -1.568258, -1.459279, -1.357532, -1.262008, -1.171905, -1.086573, -1.005472,
        -0.928148, -0.854207, -0.783309, -0.715146, -0.649445, -0.585951, -0.524433, -0.464669,
        -0.406453, -0.349584, -0.293873, -0.239131, -0.185179, -0.131837, -0.078929, -0.026281,
         0.026281,  0.078929,  0.131837,  0.185179,  0.239131,  0.293873,  0.349584,  0.406453,
         0.464669,  0.524433,  0.585951,  0.649445,  0.715146,  0.783309,  0.854207,  0.928148,
         1.005472,  1.086573,  1.171905,  1.262008,  1.357532,  1.459279,  1.568258,  1.685776,
         1.813578,  1.954065,  2.110705,  2.288778,  2.496953,  2.751095,  3.085722,  3.605999,
    ]),
    7: np.array([
        -3.835459, -3.343375, -3.029767, -2.793564, -2.601631, -2.438754, -2.296628, -2.170199,
        -2.056154, -1.952196, -1.856663, -1.768313, -1.686184, -1.609518, -1.537703, -1.470234,
        -1.406689, -1.346705, -1.289974, -1.236222, -1.185208, -1.136716, -1.090552, -1.046538,
        -1.004512, -0.964324, -0.925836, -0.888920, -0.853457, -0.819335, -0.786452, -0.754710,
        -0.724020, -0.694298, -0.665465, -0.637450, -0.610185, -0.583608, -0.557661, -0.532290,
        -0.507446, -0.483083, -0.459160, -0.435638, -0.412482, -0.389658, -0.367138, -0.344892,
        -0.322896, -0.301125, -0.279560, -0.258178, -0.236962, -0.215893, -0.194957, -0.174137,
        -0.153420, -0.132790, -0.112236, -0.091745, -0.071305, -0.050905, -0.030532, -0.010175,
         0.010175,  0.030532,  0.050905,  0.071305,  0.091745,  0.112236,  0.132790,  0.153420,
         0.174137,  0.194957,  0.215893,  0.236962,  0.258178,  0.279560,  0.301125,  0.322896,
         0.344892,  0.367138,  0.389658,  0.412482,  0.435638,  0.459160,  0.483083,  0.507446,
         0.532290,  0.557661,  0.583608,  0.610185,  0.637450,  0.665465,  0.694298,  0.724020,
         0.754710,  0.786452,  0.819335,  0.853457,  0.888920,  0.925836,  0.964324,  1.004512,
         1.046538,  1.090552,  1.136716,  1.185208,  1.236222,  1.289974,  1.346705,  1.406689,
         1.470234,  1.537703,  1.609518,  1.686184,  1.768313,  1.856663,  1.952196,  2.056154,
         2.170199,  2.296628,  2.438754,  2.601631,  2.793564,  3.029767,  3.343375,  3.835459,
    ]),
    8: np.array([
        -4.035480, -3.565625, -3.268187, -3.045475, -2.865491, -2.713551, -2.581644, -2.464895,
        -2.360107, -2.265066, -2.178166, -2.098206, -2.024257, -1.955584, -1.891595, -1.831799,
        -1.775785, -1.723203, -1.673751, -1.627164, -1.583207, -1.541672, -1.502368, -1.465126,
        -1.429789, -1.396212, -1.364264, -1.333822, -1.304772, -1.277010, -1.250438, -1.224965,
        -1.200508, -1.176989, -1.154335, -1.132480, -1.111361, -1.090923, -1.071113, -1.051883,
        -1.033188, -1.014988, -0.997247, -0.979930, -0.963006, -0.946448, -0.930229, -0.914327,
        -0.898719, -0.883388, -0.868315, -0.853484, -0.838881, -0.824492, -0.810305, -0.796310,
        -0.782495, -0.768852, -0.755371, -0.742046, -0.728869, -0.715832, -0.702931, -0.690157,
        -0.677508, -0.664976, -0.652557, -0.640248, -0.628042, -0.615938, -0.603930, -0.592014,
        -0.580189, -0.568449, -0.556793, -0.545217, -0.533718, -0.522294, -0.510941, -0.499658,
        -0.488442, -0.477290, -0.466201, -0.455172, -0.444200, -0.433285, -0.422424, -0.411614,
        -0.400855, -0.390145, -0.379481, -0.368862, -0.358286, -0.347752, -0.337259, -0.326803,
        -0.316386, -0.306003, -0.295655, -0.285340, -0.275057, -0.264803, -0.254579, -0.244382,
        -0.234211, -0.224066, -0.213944, -0.203846, -0.193768, -0.183712, -0.173674, -0.163654,
        -0.153652, -0.143665, -0.133694, -0.123736, -0.113791, -0.103857, -0.093934, -0.084021,
        -0.074116, -0.064219, -0.054328, -0.044443, -0.034562, -0.024685, -0.014810, -0.004936,
         0.004936,  0.014810,  0.024685,  0.034562,  0.044443,  0.054328,  0.064219,  0.074116,
         0.084021,  0.093934,  0.103857,  0.113791,  0.123736,  0.133694,  0.143665,  0.153652,
         0.163654,  0.173674,  0.183712,  0.193768,  0.203846,  0.213944,  0.224066,  0.234211,
         0.244382,  0.254579,  0.264803,  0.275057,  0.285340,  0.295655,  0.306003,  0.316386,
         0.326803,  0.337259,  0.347752,  0.358286,  0.368862,  0.379481,  0.390145,  0.400855,
         0.411614,  0.422424,  0.433285,  0.444200,  0.455172,  0.466201,  0.477290,  0.488442,
         0.499658,  0.510941,  0.522294,  0.533718,  0.545217,  0.556793,  0.568449,  0.580189,
         0.592014,  0.603930,  0.615938,  0.628042,  0.640248,  0.652557,  0.664976,  0.677508,
         0.690157,  0.702931,  0.715832,  0.728869,  0.742046,  0.755371,  0.768852,  0.782495,
         0.796310,  0.810305,  0.824492,  0.838881,  0.853484,  0.868315,  0.883388,  0.898719,
         0.914327,  0.930229,  0.946448,  0.963006,  0.979930,  0.997247,  1.014988,  1.033188,
         1.051883,  1.071113,  1.090923,  1.111361,  1.132480,  1.154335,  1.176989,  1.200508,
         1.224965,  1.250438,  1.277010,  1.304772,  1.333822,  1.364264,  1.396212,  1.429789,
         1.465126,  1.502368,  1.541672,  1.583207,  1.627164,  1.673751,  1.723203,  1.775785,
         1.831799,  1.891595,  1.955584,  2.024257,  2.098206,  2.178166,  2.265066,  2.360107,
         2.464895,  2.581644,  2.713551,  2.865491,  3.045475,  3.268187,  3.565625,  4.035480,
    ]),
}
# fmt: on


class BlockwiseHadamardRotate:
    """
    Blockwise Hadamard rotation: split dim into blocks of power-of-2,
    apply independent sign-flip + FWHT per block. Fully invertible, zero
    information loss. Replaces SRHT subsample which had lossy truncation.

    For dim=3072: 3 blocks of 1024 (each is 2^10).
    For arbitrary dim: greedily decompose into largest power-of-2 blocks.
    """

    def __init__(self, dim: int, seed: int = 42):
        self.dim = dim
        self.seed = seed

        # Decompose dim into power-of-2 blocks
        self.blocks: list = []  # list of (start, size)
        remaining = dim
        offset = 0
        while remaining > 0:
            # Largest power of 2 <= remaining
            block_size = 1
            while block_size * 2 <= remaining:
                block_size *= 2
            self.blocks.append((offset, block_size))
            offset += block_size
            remaining -= block_size

        # Generate per-block random signs
        rng = np.random.RandomState(seed)
        self.block_signs: list = []
        for _, bsize in self.blocks:
            self.block_signs.append(
                rng.choice([-1.0, 1.0], size=bsize).astype(np.float64)
            )

    def apply(self, x: np.ndarray) -> np.ndarray:
        """Forward rotation (sign-flip + FWHT per block)."""
        out = np.empty(self.dim, dtype=np.float64)
        for (start, bsize), signs in zip(self.blocks, self.block_signs):
            block = x[start : start + bsize].astype(np.float64) * signs
            out[start : start + bsize] = fwht(block)
        return out

    def apply_inverse(self, y: np.ndarray) -> np.ndarray:
        """Inverse rotation (FWHT is self-inverse up to normalization, then undo signs)."""
        out = np.empty(self.dim, dtype=np.float64)
        for (start, bsize), signs in zip(self.blocks, self.block_signs):
            block = fwht(y[start : start + bsize].astype(np.float64))
            out[start : start + bsize] = block * signs
        return out

    def apply_batch(self, X: np.ndarray) -> np.ndarray:
        """Forward rotation on batch (N, dim)."""
        out = np.empty_like(X, dtype=np.float64)
        for (start, bsize), signs in zip(self.blocks, self.block_signs):
            block = X[:, start : start + bsize].astype(np.float64) * signs[np.newaxis, :]
            out[:, start : start + bsize] = fwht(block)
        return out

    def apply_inverse_batch(self, Y: np.ndarray) -> np.ndarray:
        """Inverse rotation on batch (N, dim)."""
        out = np.empty_like(Y, dtype=np.float64)
        for (start, bsize), signs in zip(self.blocks, self.block_signs):
            block = fwht(Y[:, start : start + bsize].astype(np.float64))
            out[:, start : start + bsize] = block * signs[np.newaxis, :]
        return out


class SRHTRotate(BlockwiseHadamardRotate):
    """Backward-compatible alias. Ignores output_dim (always == input_dim now)."""
    def __init__(self, input_dim: int, output_dim: int = None, seed: int = 42):
        super().__init__(dim=input_dim, seed=seed)


def compute_lloyd_max_codebook(bits: int) -> np.ndarray:
    """
    Return optimal Lloyd-Max centroids for N(0,1).
    Per-vector scale adapts to the actual distribution.
    Uses hardcoded codebooks for 4-8 bits; computes on-the-fly for others.
    """
    if bits in LLOYD_MAX_CODEBOOKS:
        return LLOYD_MAX_CODEBOOKS[bits].copy()

    k = 2 ** bits
    probs = np.linspace(0.5 / k, 1 - 0.5 / k, k)
    centroids = np.array([_inv_norm_cdf(p) for p in probs])
    centroids.sort()

    for _ in range(500):
        old = centroids.copy()
        boundaries = np.empty(k + 1)
        boundaries[0] = -10.0
        boundaries[-1] = 10.0
        boundaries[1:-1] = (centroids[:-1] + centroids[1:]) / 2

        new_c = np.zeros(k)
        for i in range(k):
            a, b = boundaries[i], boundaries[i + 1]
            cdf_a = 0.5 * (1.0 + _erf_scalar(a / math.sqrt(2.0)))
            cdf_b = 0.5 * (1.0 + _erf_scalar(b / math.sqrt(2.0)))
            pdf_a = math.exp(-0.5 * a * a) / math.sqrt(2 * math.pi)
            pdf_b = math.exp(-0.5 * b * b) / math.sqrt(2 * math.pi)
            prob = cdf_b - cdf_a
            if prob > 1e-15:
                new_c[i] = (pdf_a - pdf_b) / prob
            else:
                new_c[i] = old[i]
        centroids = new_c
        if np.max(np.abs(centroids - old)) < 1e-12:
            break

    return centroids


def _inv_norm_cdf(p: float) -> float:
    """Beasley-Springer-Moro rational approximation of the inverse normal CDF."""
    a = [-3.969683028665376e1, 2.209460984245205e2,
         -2.759285104469687e2, 1.383577518672690e2,
         -3.066479806614716e1, 2.506628277459239e0]
    b = [-5.447609879822406e1, 1.615858368580409e2,
         -1.556989798598866e2, 6.680131188771972e1, -1.328068155288572e1]
    c = [-7.784894002430293e-3, -3.223964580411365e-1,
         -2.400758277161838e0, -2.549732539343734e0,
         4.374664141464968e0, 2.938163982698783e0]
    d = [7.784695709041462e-3, 3.224671290700398e-1,
         2.445134137142996e0, 3.754408661907416e0]

    p_low = 0.02425
    if p < p_low:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p <= 1 - p_low:
        q = p - 0.5
        r = q * q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    q = math.sqrt(-2 * math.log(1 - p))
    return -((((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1))


def pack_indices(indices: np.ndarray, bits: int) -> bytes:
    """Pack b-bit indices into bytes."""
    if bits == 8:
        return indices.astype(np.uint8).tobytes()

    result = bytearray()
    bit_buffer = 0
    bits_in_buffer = 0

    for idx in indices:
        bit_buffer = (bit_buffer << bits) | int(idx)
        bits_in_buffer += bits
        while bits_in_buffer >= 8:
            bits_in_buffer -= 8
            result.append((bit_buffer >> bits_in_buffer) & 0xFF)

    if bits_in_buffer > 0:
        result.append((bit_buffer << (8 - bits_in_buffer)) & 0xFF)

    return bytes(result)


def unpack_indices(data: bytes, bits: int, n: int) -> np.ndarray:
    """Unpack bytes into b-bit indices."""
    if bits == 8:
        return np.frombuffer(data, dtype=np.uint8, count=n).copy()

    indices = np.empty(n, dtype=np.uint8 if bits <= 8 else np.uint16)
    bit_buffer = 0
    bits_in_buffer = 0
    byte_idx = 0
    mask = (1 << bits) - 1

    for k in range(n):
        while bits_in_buffer < bits and byte_idx < len(data):
            bit_buffer = (bit_buffer << 8) | data[byte_idx]
            bits_in_buffer += 8
            byte_idx += 1
        bits_in_buffer -= bits
        indices[k] = (bit_buffer >> bits_in_buffer) & mask

    return indices


class TurboQuantMSE:
    """
    TurboQuant MSE-optimal quantization (Algorithm 1).

    1. Normalize, store norm + per-vector scale
    2. SRHT rotation
    3. Lloyd-Max scalar quantization per coordinate
    """

    def __init__(self, dim: int, bits: int = 6, seed: int = 42):
        self.dim = dim
        self.bits = bits
        self.seed = seed
        self.codebook = compute_lloyd_max_codebook(bits)
        self.rotation = SRHTRotate(dim, dim, seed)

    def quantize(self, x: np.ndarray) -> Dict:
        norm = float(np.linalg.norm(x))
        if norm < 1e-12:
            return {"norm": 0.0, "scale": 1.0, "indices": np.zeros(self.dim, dtype=np.uint8)}

        x_rotated = self.rotation.apply(x / norm)
        scale = float(np.std(x_rotated))
        if scale < 1e-12:
            scale = 1.0

        x_scaled = x_rotated / scale
        distances = np.abs(x_scaled[:, np.newaxis] - self.codebook[np.newaxis, :])
        indices = np.argmin(distances, axis=1).astype(np.uint8 if self.bits <= 8 else np.uint16)

        return {"norm": norm, "scale": scale, "indices": indices}

    def dequantize(self, data: Dict) -> np.ndarray:
        norm = data["norm"]
        scale = data.get("scale", 1.0)
        indices = data["indices"]
        if norm < 1e-12:
            return np.zeros(self.dim)
        x_rotated = self.codebook[indices] * scale
        return self.rotation.apply_inverse(x_rotated) * norm

    def quantize_batch(self, X: np.ndarray) -> List[Dict]:
        return [self.quantize(x) for x in X]


class SRHTSketch:
    """
    SRHT sketch for QJL residual encoding.
    Projects to m << d dimensions using blockwise Hadamard + fixed subsampling,
    then stores sign bits only (m/8 bytes).
    """

    def __init__(self, input_dim: int, sketch_dim: int = 256, seed: int = 137):
        self.input_dim = input_dim
        self.sketch_dim = sketch_dim
        self.seed = seed
        # Use a separate blockwise rotation for the sketch
        self.rotation = BlockwiseHadamardRotate(input_dim, seed=seed)
        # Fixed random indices to subsample from rotated output
        rng = np.random.RandomState(seed + 1000)
        self.indices = np.sort(rng.choice(input_dim, size=sketch_dim, replace=False))
        self.scale = np.sqrt(input_dim / sketch_dim)

    def sketch(self, x: np.ndarray) -> np.ndarray:
        rotated = self.rotation.apply(x)
        return rotated[self.indices] * self.scale

    def sketch_batch(self, X: np.ndarray) -> np.ndarray:
        rotated = self.rotation.apply_batch(X)
        return rotated[:, self.indices] * self.scale


class TurboQuantProd:
    """
    TurboQuant inner product quantization (Algorithm 2).
    (b-1)-bit MSE + 1-bit QJL residual sketch for unbiased IP estimation.
    """

    def __init__(
        self,
        dim: int,
        bits: int = 6,
        seed_rot: int = 42,
        seed_qjl: int = 137,
        sketch_dim: int = 256,
    ):
        self.dim = dim
        self.bits = bits
        self.seed_rot = seed_rot
        self.seed_qjl = seed_qjl
        self.sketch_dim = sketch_dim
        self.mse_quantizer = TurboQuantMSE(dim, bits - 1, seed_rot)
        self.qjl_sketch = SRHTSketch(dim, sketch_dim, seed_qjl)

    def quantize(self, x: np.ndarray) -> Dict:
        mse_data = self.mse_quantizer.quantize(x)
        x_mse = self.mse_quantizer.dequantize(mse_data)
        residual = x - x_mse
        residual_norm = float(np.linalg.norm(residual))
        qjl_projection = self.qjl_sketch.sketch(residual)
        qjl_signs_bits = (qjl_projection >= 0).astype(np.uint8)

        return {
            "norm": mse_data["norm"],
            "scale": mse_data["scale"],
            "mse_indices": mse_data["indices"],
            "qjl_signs": qjl_signs_bits,
            "residual_norm": residual_norm,
        }

    def asymmetric_ip(self, query: np.ndarray, stored: Dict) -> float:
        codebook = self.mse_quantizer.codebook
        q_rot = self.mse_quantizer.rotation.apply(query)
        centroids = codebook[stored["mse_indices"]]
        scale = stored.get("scale", 1.0)
        ip_mse = stored["norm"] * scale * np.dot(q_rot, centroids)

        qjl_signs = stored["qjl_signs"].astype(np.float32) * 2 - 1
        s_query = self.qjl_sketch.sketch(query)
        correction = (
            np.sqrt(np.pi / 2) / self.sketch_dim
            * stored["residual_norm"]
            * np.dot(s_query, qjl_signs)
        )
        return ip_mse + correction

    def search(
        self, query: np.ndarray, database: List[Dict], top_k: int = 10
    ) -> List[Tuple[int, float]]:
        if not database:
            return []

        codebook = self.mse_quantizer.codebook
        q_rot = self.mse_quantizer.rotation.apply(query)
        s_query = self.qjl_sketch.sketch(query)
        qjl_scale = np.sqrt(np.pi / 2) / self.sketch_dim

        scores: List[Tuple[int, float]] = []
        for idx, stored in enumerate(database):
            centroids_stored = codebook[stored["mse_indices"]]
            scale = stored.get("scale", 1.0)
            ip_mse = stored["norm"] * scale * np.dot(q_rot, centroids_stored)

            qjl_signs = stored["qjl_signs"].astype(np.float32) * 2 - 1
            correction = qjl_scale * stored["residual_norm"] * np.dot(s_query, qjl_signs)
            scores.append((idx, float(ip_mse + correction)))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def search_batch(
        self,
        query: np.ndarray,
        database: List[Dict],
        top_k: int = 10,
        block_size: int = 512,
    ) -> List[Tuple[int, float]]:
        """Block-decoded batch search using numpy matmul."""
        if not database:
            return []

        codebook = self.mse_quantizer.codebook
        q_rot = self.mse_quantizer.rotation.apply(query)
        s_query = self.qjl_sketch.sketch(query)
        qjl_scale = np.sqrt(np.pi / 2) / self.sketch_dim

        n = len(database)
        all_scores = np.empty(n)

        for start in range(0, n, block_size):
            end = min(start + block_size, n)
            block = database[start:end]
            bs = end - start

            idx_matrix = np.stack([b["mse_indices"] for b in block])  # (bs, dim)
            centroid_matrix = codebook[idx_matrix]  # (bs, dim)

            norms = np.array([b["norm"] for b in block])
            scales = np.array([b.get("scale", 1.0) for b in block])
            ip_mse = norms * scales * (centroid_matrix @ q_rot)

            sign_matrix = np.stack(
                [b["qjl_signs"].astype(np.float32) * 2 - 1 for b in block]
            )  # (bs, sketch_dim)
            rnorms = np.array([b["residual_norm"] for b in block])
            correction = qjl_scale * rnorms * (sign_matrix @ s_query)

            all_scores[start:end] = ip_mse + correction

        top_indices = np.argpartition(-all_scores, min(top_k, n - 1))[:top_k]
        top_indices = top_indices[np.argsort(-all_scores[top_indices])]
        return [(int(i), float(all_scores[i])) for i in top_indices]


if __name__ == "__main__":
    print("=" * 70)
    print("TurboQuant Test Suite")
    print("=" * 70)

    dim = 768
    n_vectors = 1000
    n_db = 500
    n_queries = 100
    all_pass = True

    def check(name: str, ok: bool, msg: str) -> bool:
        global all_pass
        tag = "PASS" if ok else "FAIL"
        sym = "\u2713" if ok else "\u2717"
        print(f"  {sym} {tag}: {msg}")
        if not ok:
            all_pass = False
        return ok

    # ---- Test 1: FWHT correctness (Sylvester construction) ----
    print("\n[Test 1] FWHT correctness...")
    rng = np.random.RandomState(0)
    x = rng.randn(16)
    y = fwht(x)
    n_h = len(x)

    def _build_hadamard(n: int) -> np.ndarray:
        if n == 1:
            return np.array([[1.0]])
        half = _build_hadamard(n // 2)
        return np.block([[half, half], [half, -half]]) / np.sqrt(2)

    H = _build_hadamard(n_h)
    y_ref = H @ x
    check("FWHT", np.allclose(y, y_ref, atol=1e-12), f"max diff = {np.max(np.abs(y - y_ref)):.2e}")

    # ---- Test 1b: FWHT batch ----
    print("\n[Test 1b] FWHT batch...")
    X_batch = rng.randn(5, 16)
    Y_batch = fwht(X_batch)
    Y_single = np.stack([fwht(x) for x in X_batch])
    check("FWHT batch", np.allclose(Y_batch, Y_single, atol=1e-12), "batch matches single")

    # ---- Test 2: SRHTRotate near-isometry ----
    print("\n[Test 2] SRHT near-isometry...")
    rot = SRHTRotate(dim, dim, seed=42)
    vecs = rng.randn(200, dim)
    vecs /= np.linalg.norm(vecs, axis=1, keepdims=True)
    vecs_rot = rot.apply_batch(vecs)
    norms_rot = np.linalg.norm(vecs_rot, axis=1)
    check(
        "SRHT isometry",
        np.allclose(norms_rot, 1.0, atol=0.15),
        f"norm range [{norms_rot.min():.4f}, {norms_rot.max():.4f}]",
    )

    # ---- Test 3: Codebook sanity (1-bit) ----
    print("\n[Test 3] Codebook sanity (1-bit)...")
    cb1 = compute_lloyd_max_codebook(1)
    expected = np.sqrt(2 / np.pi)
    check(
        "1-bit codebook",
        len(cb1) == 2 and np.allclose(np.abs(cb1), expected, atol=0.003),
        f"centroids {cb1} vs +/-{expected:.5f}",
    )

    # ---- Test 4: MSE distortion (in rotated domain) ----
    print("\n[Test 4] MSE distortion...")
    np.random.seed(42)
    test_vecs = np.random.randn(n_vectors, dim)
    test_vecs /= np.linalg.norm(test_vecs, axis=1, keepdims=True)

    for bits in [3, 4]:
        q = TurboQuantMSE(dim, bits=bits, seed=42)
        mse_total = 0.0
        for v in test_vecs:
            data = q.quantize(v)
            x_rot = q.rotation.apply(v / np.linalg.norm(v))
            x_recon_rot = q.codebook[data["indices"]] * data["scale"]
            mse_total += np.mean((x_rot - x_recon_rot) ** 2)
        avg = mse_total / n_vectors
        threshold = 0.00015 if bits == 3 else 0.00005
        check(f"MSE b={bits}", avg < threshold, f"MSE={avg:.6f} (< {threshold})")

    # ---- Test 5: Unbiased IP ----
    print("\n[Test 5] Unbiased inner product...")
    qp = TurboQuantProd(dim, bits=4, seed_rot=42, seed_qjl=137)
    np.random.seed(123)
    bias_sum = 0.0
    for _ in range(1000):
        v1 = np.random.randn(dim)
        v2 = np.random.randn(dim)
        v1 /= np.linalg.norm(v1)
        v2 /= np.linalg.norm(v2)
        true_ip = np.dot(v1, v2)
        est_ip = qp.asymmetric_ip(v1, qp.quantize(v2))
        bias_sum += est_ip - true_ip
    mean_bias = bias_sum / 1000
    check("Unbiased IP", abs(mean_bias) < 0.02, f"mean bias = {mean_bias:.6f}")

    # ---- Test 6: IP correlation ----
    print("\n[Test 6] IP correlation...")
    np.random.seed(456)
    true_ips, est_ips = [], []
    for _ in range(1000):
        v1 = np.random.randn(dim)
        v2 = np.random.randn(dim)
        v1 /= np.linalg.norm(v1)
        v2 /= np.linalg.norm(v2)
        true_ips.append(np.dot(v1, v2))
        est_ips.append(qp.asymmetric_ip(v1, qp.quantize(v2)))
    corr = np.corrcoef(true_ips, est_ips)[0, 1]
    check("IP correlation", corr > 0.85, f"r = {corr:.4f}")

    # ---- Test 7: Top-1 recall ----
    print("\n[Test 7] Top-1 recall...")
    np.random.seed(789)
    qr = TurboQuantProd(dim, bits=5, seed_rot=42, seed_qjl=137)
    db_vecs = np.random.randn(n_db, dim)
    db_vecs /= np.linalg.norm(db_vecs, axis=1, keepdims=True)
    db_q = [qr.quantize(v) for v in db_vecs]

    queries = np.random.randn(n_queries, dim)
    queries /= np.linalg.norm(queries, axis=1, keepdims=True)

    correct = sum(
        1
        for query in queries
        if np.argmax([np.dot(query, v) for v in db_vecs])
        == qr.search(query, db_q, top_k=1)[0][0]
    )
    recall = correct / n_queries
    check("Top-1 recall", recall > 0.35, f"{recall:.0%} (5-bit, SRHT approx)")

    # ---- Test 8: Stored norm matches original ----
    print("\n[Test 8] Norm preservation...")
    qm = TurboQuantMSE(dim, bits=4, seed=42)
    np.random.seed(321)
    max_err = 0.0
    for _ in range(100):
        v = np.random.randn(dim) * np.random.uniform(0.1, 10)
        orig_n = np.linalg.norm(v)
        data = qm.quantize(v)
        max_err = max(max_err, abs(data["norm"] - orig_n) / orig_n)
    check("Norm preservation", max_err < 1e-10, f"max rel error = {max_err:.2e}")

    # ---- Test 9: Compression ----
    print("\n[Test 9] Compression ratio...")
    v = np.random.randn(dim)
    data = qp.quantize(v)
    total = 8 + len(pack_indices(data["mse_indices"], qp.bits - 1)) + len(pack_indices(data["qjl_signs"], 1)) + 8
    check("Compression", total < 500, f"{total} bytes vs {dim*4} float32")

    # ---- Test 10: Pack/unpack roundtrip ----
    print("\n[Test 10] Pack/unpack roundtrip...")
    idx = np.random.randint(0, 16, size=dim, dtype=np.uint8)
    check("Pack/unpack", np.array_equal(idx, unpack_indices(pack_indices(idx, 4), 4, dim)), "4-bit roundtrip")

    # ---- Test 11: Deterministic ----
    print("\n[Test 11] Deterministic behavior...")
    q1 = TurboQuantMSE(dim, bits=4, seed=999)
    q2 = TurboQuantMSE(dim, bits=4, seed=999)
    v = np.random.randn(dim)
    d1, d2 = q1.quantize(v), q2.quantize(v)
    check("Deterministic", d1["norm"] == d2["norm"] and np.array_equal(d1["indices"], d2["indices"]), "same seed → same output")

    # ---- Test 12: Batch consistency ----
    print("\n[Test 12] Batch consistency...")
    qb = TurboQuantMSE(dim, bits=4, seed=42)
    np.random.seed(111)
    batch = np.random.randn(10, dim)
    br = qb.quantize_batch(batch)
    ir = [qb.quantize(v) for v in batch]
    ok = all(b["norm"] == i["norm"] and np.array_equal(b["indices"], i["indices"]) for b, i in zip(br, ir))
    check("Batch consistency", ok, "batch == individual")

    # ---- Test 13: SRHTSketch ----
    print("\n[Test 13] SRHTSketch dimensions...")
    sk = SRHTSketch(dim, 256, seed=137)
    sv = sk.sketch(np.random.randn(dim))
    check("SRHTSketch", sv.shape == (256,), f"shape = {sv.shape}")

    # ---- Test 14: search_batch matches search ----
    print("\n[Test 14] search_batch vs search...")
    np.random.seed(999)
    q14 = TurboQuantProd(dim, bits=5, seed_rot=42, seed_qjl=137)
    db14 = np.random.randn(100, dim)
    db14 /= np.linalg.norm(db14, axis=1, keepdims=True)
    db14_q = [q14.quantize(v) for v in db14]
    query14 = np.random.randn(dim)
    query14 /= np.linalg.norm(query14)
    r_loop = q14.search(query14, db14_q, top_k=10)
    r_batch = q14.search_batch(query14, db14_q, top_k=10)
    ids_loop = [r[0] for r in r_loop]
    ids_batch = [r[0] for r in r_batch]
    check("search_batch", ids_loop == ids_batch, f"top-10 ids match")

    # ---- Test 15: Codebook symmetry ----
    print("\n[Test 15] Codebook symmetry...")
    sym_ok = True
    for bits, cb in LLOYD_MAX_CODEBOOKS.items():
        k = len(cb)
        if not np.allclose(cb[:k // 2], -cb[k // 2:][::-1], atol=1e-5):
            sym_ok = False
    check("Codebook symmetry", sym_ok, "all hardcoded codebooks symmetric about 0")

    # ---- Summary ----
    print("\n" + "=" * 70)
    print(f"{'ALL TESTS PASSED' if all_pass else 'SOME TESTS FAILED'}")
    print("=" * 70)
