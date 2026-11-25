import AppKit

let input = URL(fileURLWithPath: CommandLine.arguments[1])
let output = URL(fileURLWithPath: CommandLine.arguments[2])
guard let base = NSImage(contentsOf: input) else { fatalError("cannot read visual") }
let size = NSSize(width: 1600, height: 900)
let canvas = NSImage(size: size)
canvas.lockFocus()
base.draw(in: NSRect(origin: .zero, size: size), from: .zero, operation: .sourceOver, fraction: 1)
let heading = NSMutableParagraphStyle(); heading.lineBreakMode = .byWordWrapping
let title: [NSAttributedString.Key: Any] = [.font: NSFont.systemFont(ofSize: 60, weight: .bold), .foregroundColor: NSColor(calibratedRed: 0.06, green: 0.30, blue: 0.26, alpha: 1), .paragraphStyle: heading]
let subtitle: [NSAttributedString.Key: Any] = [.font: NSFont.systemFont(ofSize: 26, weight: .regular), .foregroundColor: NSColor(calibratedRed: 0.17, green: 0.23, blue: 0.21, alpha: 1), .paragraphStyle: heading]
("公众号素材库目录" as NSString).draw(in: NSRect(x: 100, y: 510, width: 690, height: 100), withAttributes: title)
("只读整理可见素材\n交付带来源的目录草稿" as NSString).draw(in: NSRect(x: 104, y: 400, width: 620, height: 100), withAttributes: subtitle)
canvas.unlockFocus()
guard let data = canvas.tiffRepresentation, let rep = NSBitmapImageRep(data: data), let png = rep.representation(using: .png, properties: [:]) else { fatalError("cannot encode png") }
try png.write(to: output)
