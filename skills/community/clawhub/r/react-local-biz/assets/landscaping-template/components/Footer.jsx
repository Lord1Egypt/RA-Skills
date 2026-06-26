import { Link } from "react-router-dom";
import { Leaf, MapPin, Phone, Mail, Facebook, Instagram, Twitter, Youtube } from "lucide-react";

const services = ["Lawn Care & Maintenance", "Garden Design", "Tree & Shrub Care", "Irrigation Systems", "Hardscaping & Patios", "Seasonal Cleanup"];
const quickLinks = [
  { to: "/", label: "Home" },
  { to: "/services", label: "Services" },
  { to: "/portfolio", label: "Portfolio" },
  { to: "/about", label: "About Us" },
  { to: "/contact", label: "Contact" },
];

export default function Footer() {
  return (
    <footer className="bg-stone-900 text-stone-300">
      {/* Main Footer */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
          {/* Brand */}
          <div className="lg:col-span-1">
            <Link to="/" className="flex items-center gap-2.5 mb-5 group">
              <div className="p-2 bg-primary-600/20 rounded-xl">
                <Leaf className="w-6 h-6 text-primary-400" />
              </div>
              <div>
                <span className="font-display font-bold text-lg text-white leading-none block">GreenScape</span>
                <span className="text-xs font-semibold tracking-widest uppercase text-primary-400">Pro</span>
              </div>
            </Link>
            <p className="text-stone-400 text-sm leading-relaxed mb-6">
              Transforming outdoor spaces into breathtaking landscapes since 2009. Award-winning design, expert craftsmanship, and a commitment to sustainability.
            </p>
            <div className="flex gap-3">
              {[Facebook, Instagram, Twitter, Youtube].map((Icon, i) => (
                <a
                  key={i}
                  href="#"
                  className="w-9 h-9 bg-stone-800 hover:bg-primary-600 rounded-lg flex items-center justify-center transition-colors duration-200"
                  aria-label="Social media"
                >
                  <Icon className="w-4 h-4" />
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-display font-bold text-white text-lg mb-5">Quick Links</h4>
            <ul className="space-y-2.5">
              {quickLinks.map(({ to, label }) => (
                <li key={to}>
                  <Link
                    to={to}
                    className="text-stone-400 hover:text-primary-400 text-sm transition-colors flex items-center gap-1.5 group"
                  >
                    <span className="w-1 h-1 bg-primary-600 rounded-full opacity-0 group-hover:opacity-100 transition-opacity" />
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Services */}
          <div>
            <h4 className="font-display font-bold text-white text-lg mb-5">Our Services</h4>
            <ul className="space-y-2.5">
              {services.map((s) => (
                <li key={s}>
                  <Link
                    to="/services"
                    className="text-stone-400 hover:text-primary-400 text-sm transition-colors flex items-center gap-1.5 group"
                  >
                    <span className="w-1 h-1 bg-primary-600 rounded-full opacity-0 group-hover:opacity-100 transition-opacity" />
                    {s}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="font-display font-bold text-white text-lg mb-5">Contact Us</h4>
            <ul className="space-y-4">
              <li className="flex items-start gap-3">
                <MapPin className="w-5 h-5 text-primary-400 mt-0.5 shrink-0" />
                <span className="text-stone-400 text-sm">1234 Garden Valley Drive<br />Portland, OR 97201</span>
              </li>
              <li className="flex items-center gap-3">
                <Phone className="w-5 h-5 text-primary-400 shrink-0" />
                <a href="tel:+15555550123" className="text-stone-400 hover:text-primary-400 text-sm transition-colors">(555) 555-0123</a>
              </li>
              <li className="flex items-center gap-3">
                <Mail className="w-5 h-5 text-primary-400 shrink-0" />
                <a href="mailto:hello@greenscapepro.com" className="text-stone-400 hover:text-primary-400 text-sm transition-colors">hello@greenscapepro.com</a>
              </li>
            </ul>
            <div className="mt-6 p-4 bg-stone-800 rounded-xl">
              <p className="text-xs text-stone-400 font-semibold uppercase tracking-wider mb-2">Business Hours</p>
              <p className="text-stone-300 text-sm">Mon – Fri: 7am – 6pm</p>
              <p className="text-stone-300 text-sm">Sat: 8am – 4pm</p>
              <p className="text-stone-500 text-sm">Sun: Closed</p>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-stone-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-stone-500 text-sm">
            © 2025 GreenScape Pro. All rights reserved.
          </p>
          <div className="flex gap-5">
            <a href="#" className="text-stone-500 hover:text-primary-400 text-sm transition-colors">Privacy Policy</a>
            <a href="#" className="text-stone-500 hover:text-primary-400 text-sm transition-colors">Terms of Service</a>
            <a href="#" className="text-stone-500 hover:text-primary-400 text-sm transition-colors">Sitemap</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
