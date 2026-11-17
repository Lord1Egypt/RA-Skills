// Cargo.toml:
// [lib]
// name = "fastcore"
// crate-type = ["cdylib"]
// [dependencies]
// pyo3 = { version = "0.26", features = ["extension-module"] }

use pyo3::prelude::*;

#[pyfunction]
fn add(a: i64, b: i64) -> i64 {
    a + b
}

#[pymodule]
fn fastcore(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    Ok(())
}
