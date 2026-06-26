import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Leaf, Menu, X, Phone } from "lucide-react";

const links = [
  { to: "/", label: "Home" },
  { to: "/services", label: "Services" },
  { to: "/portfolio", label: "Portfolio" },
  { to: "/about", label: "About" },
  { to: "/contact", label: "Contact" },
];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => setOpen(false), [location]);

  const isHome = location.pathname === "/";
  const transparent = isHome && !scrolled && !open;

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        transparent
          ? "bg-transparent py-5"
          : "bg-white/95 backdrop-blur-md shadow-lg py-3 border-b border-stone-100"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className={`p-2 rounded-xl transition-colors ${transparent ? "bg-white/20" : "bg-primary-50"}`}>
              <Leaf className={`w-6 h-6 transition-colors ${transparent ? "text-white" : "text-primary-600"}`} />
            </div>
            <div>
              <span className={`font-display font-bold text-lg leading-none block transition-colors ${transparent ? "text-white" : "text-stone-900"}`}>
                GreenScape
              </span>
              <span className={`text-xs font-semibold tracking-widest uppercase transition-colors ${transparent ? "text-white/70" : "text-primary-600"}`}>
                Pro
              </span>
            </div>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-1">
            {links.map(({ to, label }) => {
              const active = location.pathname === to;
              return (
                <Link
                  key={to}
                  to={to}
                  className={`px-4 py-2 rounded-lg font-medium text-sm transition-all duration-200 ${
                    active
                      ? transparent
                        ? "bg-white/20 text-white"
                        : "bg-primary-50 text-primary-700"
                      : transparent
                      ? "text-white/90 hover:text-white hover:bg-white/10"
                      : "text-stone-600 hover:text-stone-900 hover:bg-stone-50"
                  }`}
                >
                  {label}
                </Link>
              );
            })}
          </div>

          {/* CTA */}
          <div className="hidden md:flex items-center gap-3">
            <a
              href="tel:+15555550123"
              className={`flex items-center gap-2 text-sm font-medium transition-colors ${transparent ? "text-white/80 hover:text-white" : "text-stone-500 hover:text-stone-700"}`}
            >
              <Phone className="w-4 h-4" />
              (555) 555-0123
            </a>
            <Link to="/contact" className="btn-primary text-sm px-5 py-2.5">
              Get Free Quote
            </Link>
          </div>

          {/* Mobile Toggle */}
          <button
            onClick={() => setOpen(!open)}
            className={`md:hidden p-2 rounded-lg transition-colors ${transparent ? "text-white hover:bg-white/10" : "text-stone-700 hover:bg-stone-100"}`}
            aria-label="Toggle menu"
          >
            {open ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {open && (
          <div className="md:hidden mt-4 pb-4 border-t border-white/20">
            <div className="pt-4 space-y-1">
              {links.map(({ to, label }) => (
                <Link
                  key={to}
                  to={to}
                  className={`block px-4 py-3 rounded-xl font-medium transition-colors ${
                    location.pathname === to
                      ? transparent
                        ? "bg-white/20 text-white"
                        : "bg-primary-50 text-primary-700"
                      : transparent
                      ? "text-white/90 hover:bg-white/10"
                      : "text-stone-700 hover:bg-stone-50"
                  }`}
                >
                  {label}
                </Link>
              ))}
              <div className="pt-3">
                <Link to="/contact" className="btn-primary w-full justify-center text-sm">
                  Get Free Quote
                </Link>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
