//! UNIHIKER K10 (DFRobot UNIHIKER, ESP32-S3, 8 MB PSRAM, 16 MB flash):
//!   - 2.8" 240×320 TFT, TFT_eSPI `ILI9341_DRIVER` over SPI: SCLK 12, MOSI 21, CS 14, DC 13
//!   - buttons, backlight and amp enable behind an I2C GPIO expander (PCA9555 at 0x20) —
//!     `digital_read()` in the K10 library addresses the expander, never a pad
//!   - light sensor (LTR303ALS) and accelerometer (SC7A20H): not modelled
use std::sync::{Arc, Mutex};

use esp_periph::i2c::{I2cDevice, Reg8Device};
use esp_soc::board::BoardModel;
use esp_soc::devices::DcsPanel;

const PIN_TFT_SCLK: u8 = 12;
const PIN_TFT_MOSI: u8 = 21;
const PIN_TFT_CS: u8 = 14;
const PIN_TFT_DC: u8 = 13;
/// Pads a script's `press btnA` / `press btnB` acts on. The K10 has no pad to press, so the
/// board watches these two lines and moves the expander's input bits instead.
const PIN_BTN_A: u8 = 5;
const PIN_BTN_B: u8 = 11;
const EXPANDER_ADDR: u8 = 0x20;

/// Shared expander input state: the two 8-bit ports, all ones = nothing pressed.
#[derive(Clone)]
pub struct Expander(Arc<Mutex<[u8; 2]>>);

impl Expander {
    fn new() -> Self { Expander(Arc::new(Mutex::new([0xff, 0xff]))) }
    fn press(&self, down: bool) {
        let mut p = self.0.lock().expect("expander mutex");
        *p = if down { [0x00, 0x00] } else { [0xff, 0xff] };
    }
}

struct K10Expander { state: Expander, regs: [u8; 8], ptr: u8, first: bool }

impl I2cDevice for K10Expander {
    fn start(&mut self, read: bool) -> bool { if !read { self.first = true; } true }
    fn write(&mut self, b: u8) -> bool {
        if self.first { self.ptr = b; self.first = false; } else { self.regs[self.ptr as usize & 7] = b; self.ptr = self.ptr.wrapping_add(1); }
        true
    }
    fn read(&mut self) -> u8 {
        let ports = *self.state.0.lock().expect("expander mutex");
        let v = match self.ptr & 7 { 0 => ports[0], 1 => ports[1], i => self.regs[i as usize] };
        self.ptr = self.ptr.wrapping_add(1);
        v
    }
}

/// What the glass shows: the controller's RAM undone from MADCTL, so the app's own
/// coordinates come back (portrait 240×320, or 320×240 when MV is set).
pub fn frame(p: &DcsPanel) -> Vec<u16> {
    let mv = p.madctl & 0x20 != 0;
    let (w, h) = if mv { (p.rows, p.cols) } else { (p.cols, p.rows) };
    let mut out = vec![0u16; w * h];
    for pr in 0..p.rows {
        for pc in 0..p.cols {
            let mut c = pc;
            let mut r = pr;
            if p.madctl & 0x40 != 0 { c = p.cols - 1 - c; }
            if p.madctl & 0x80 != 0 { r = p.rows - 1 - r; }
            let (x, y) = if mv { (r, c) } else { (c, r) };
            let mut px = p.gram[pr * p.cols + pc];
            if p.inverted { px = !px; }
            out[y * w + x] = px;
        }
    }
    out
}

pub struct UnihikerK10 {
    pub tft: DcsPanel,
    pub expander: Expander,
    gpio_events: u64,
}

impl Default for UnihikerK10 { fn default() -> Self { Self::new() } }

impl UnihikerK10 {
    pub fn new() -> Self { UnihikerK10 { tft: DcsPanel::new(240, 320), expander: Expander::new(), gpio_events: 0 } }
}

impl BoardModel for UnihikerK10 {
    fn name(&self) -> &'static str { "unihiker-k10" }

    fn gpio_changes(&mut self, changes: &[(u8, bool)]) {
        for &(pin, level) in changes {
            self.gpio_events += 1;
            if pin == PIN_TFT_DC { self.tft.dc = level; }
            if pin == PIN_BTN_A || pin == PIN_BTN_B { self.expander.press(!level); }
        }
    }

    fn gpio_events(&self) -> u64 { self.gpio_events }

    /// Hardware SPI to the panel: the SoC delivers the bytes, DC comes from the pins.
    fn spi_tx(&mut self, _host: u8, data: &[u8]) {
        for &b in data { self.tft.byte(b); }
    }

    fn i2c_devices(&mut self) -> Vec<(u8, u8, Box<dyn I2cDevice>)> {
        let mut dev = K10Expander { state: self.expander.clone(), regs: [0; 8], ptr: 0, first: true };
        dev.regs[6] = 0xff;                     // every pin an input, as after the driver's init
        dev.regs[7] = 0xff;
        vec![(0, EXPANDER_ADDR, Box::new(dev) as Box<dyn I2cDevice>)]
    }

    fn display(&self) -> Option<(u32, u32, Vec<u16>, u64)> {
        let mv = self.tft.madctl & 0x20 != 0;
        let (w, h) = if mv { (320, 240) } else { (240, 320) };
        Some((w, h, frame(&self.tft), self.tft.pixels_written))
    }
    fn display_version(&self) -> u64 { self.tft.pixels_written }
    fn display_quiet_push(&self) -> bool { true }
    fn display_frames(&self) -> u64 { self.tft.frames }
    fn gram(&self) -> Option<(Vec<u16>, usize, usize)> { Some((self.tft.gram.clone(), self.tft.cols, self.tft.rows)) }

    fn named_pin(&self, name: &str) -> Option<u8> {
        match name { "btnA" | "a" => Some(PIN_BTN_A), "btnB" | "b" => Some(PIN_BTN_B), _ => None }
    }

    /// The expander's inputs idle high: without this an undriven pad reads low and the firmware
    /// sees both buttons held down from the first instruction.
    fn input_levels(&self) -> Vec<(u8, bool)> {
        vec![(PIN_BTN_A, true), (PIN_BTN_B, true)]
    }

    /// `press btnA 200` in a script drives pad 5: move the expander's input bits with it.
    fn gpio_input(&mut self, pin: u8, level: bool) {
        if pin == PIN_BTN_A || pin == PIN_BTN_B { self.expander.press(!level); }
    }

    fn report(&self) -> String {
        let t = &self.tft;
        format!("[emu] k10 tft: {} RAMWR, {} pixels, madctl={:#x} colmod={:#x} inverted={} on={} bbox={:?} top colours {:x?}; gpio events {}",
                t.frames, t.pixels_written, t.madctl, t.colmod, t.inverted, t.on, t.bbox(), t.histogram(5), self.gpio_events)
    }
}
