"""CPU Lewiner marching cubes adapter for the pinned TripoSR helper.

TripoSR's helper expects torchmcubes ZYX vertex ordering, then reverses it.
scikit-image returns array-axis XYZ ordering. Reverse here so the two
reversals preserve the physical coordinate system without a native build.
"""
def marching_cubes(volume, level):
    import numpy as np
    import torch
    from skimage.measure import marching_cubes as cpu_marching_cubes
    values = volume.detach().to('cpu', dtype=torch.float32).numpy()
    if not np.isfinite(values).all():
        raise ValueError('Density field contains non-finite values')
    if not float(values.min()) < level < float(values.max()):
        raise ValueError('No density isosurface at this threshold; reconstruction failed')
    vertices, faces, _, _ = cpu_marching_cubes(values, level=level, allow_degenerate=False)
    return torch.from_numpy(vertices[:, ::-1].copy()), torch.from_numpy(faces.astype(np.int64).copy())
