import Foundation
import CoreLocation

let outputPath = CommandLine.arguments.count > 1
    ? CommandLine.arguments[1]
    : nil

func writeResult(_ text: String) {
    if let path = outputPath {
        try? text.write(toFile: path, atomically: true, encoding: .utf8)
    } else {
        print(text)
    }
}

class LocationDelegate: NSObject, CLLocationManagerDelegate {
    let manager = CLLocationManager()

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyHundredMeters
    }

    func start() {
        manager.startUpdatingLocation()
    }

    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let loc = locations.last else { return }
        writeResult("\(loc.coordinate.latitude),\(loc.coordinate.longitude)")
        exit(0)
    }

    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        writeResult("error:\(error.localizedDescription)")
        exit(1)
    }

    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        switch manager.authorizationStatus {
        case .denied, .restricted:
            writeResult("denied")
            exit(2)
        case .authorizedAlways, .authorized:
            manager.startUpdatingLocation()
        case .notDetermined:
            break
        @unknown default:
            break
        }
    }
}

let delegate = LocationDelegate()
delegate.start()

DispatchQueue.main.asyncAfter(deadline: .now() + 10) {
    writeResult("timeout")
    exit(3)
}

RunLoop.main.run()
