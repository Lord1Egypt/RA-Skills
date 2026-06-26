import { useState } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight, MapPin, X, ChevronLeft, ChevronRight } from "lucide-react";

const categories = ["All", "Residential", "Commercial", "Garden Design", "Hardscaping"];

const projects = [
  {
    id: 1,
    img: "https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?w=900&q=80",
    title: "Modern Backyard Oasis",
    location: "Lake Oswego, OR",
    category: "Residential",
    desc: "A complete backyard transformation featuring a custom infinity-edge pool, surrounding patio, outdoor kitchen, and lush plantings for a resort-style feel.",
    year: "2024",
  },
  {
    id: 2,
    img: "https://images.unsplash.com/photo-1558905585-2d3c6b28c3c1?w=900&q=80",
    title: "Zen Garden Retreat",
    location: "Portland, OR",
    category: "Garden Design",
    desc: "A serene Japanese-inspired garden with raked gravel, bamboo, water features, and carefully curated stone elements that create a meditative outdoor sanctuary.",
    year: "2024",
  },
  {
    id: 3,
    img: "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=900&q=80",
    title: "Mountain Estate Gardens",
    location: "Beaverton, OR",
    category: "Residential",
    desc: "Sweeping estate grounds with terraced gardens, native plantings, and panoramic mountain views framed by mature trees and natural stone features.",
    year: "2023",
  },
  {
    id: 4,
    img: "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=900&q=80",
    title: "Rolling Meadow Retreat",
    location: "Hillsboro, OR",
    category: "Residential",
    desc: "A sprawling residential property transformed with wildflower meadows, formal garden rooms, and a winding path system that invites exploration.",
    year: "2023",
  },
  {
    id: 5,
    img: "https://images.unsplash.com/photo-1549813069-f95e44d7f498?w=900&q=80",
    title: "Coastal Corporate Campus",
    location: "Gresham, OR",
    category: "Commercial",
    desc: "Full grounds management for a 5-acre corporate campus including sustainable plantings, employee garden areas, and award-winning seasonal displays.",
    year: "2024",
  },
  {
    id: 6,
    img: "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=900&q=80",
    title: "English Country Garden",
    location: "Tigard, OR",
    category: "Garden Design",
    desc: "A romantic English-inspired garden with rose arbors, cottage perennials, clipped hedges, and a charming potting shed surrounded by blooms.",
    year: "2023",
  },
  {
    id: 7,
    img: "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=900&q=80",
    title: "Natural Stone Patio",
    location: "Portland, OR",
    category: "Hardscaping",
    desc: "Custom bluestone patio with built-in fire pit, curved seating walls, and integrated landscape lighting for stunning year-round outdoor entertaining.",
    year: "2024",
  },
  {
    id: 8,
    img: "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=900&q=80",
    title: "Heritage Tree Garden",
    location: "West Linn, OR",
    category: "Garden Design",
    desc: "A mature garden restoration preserving 100-year-old oak trees while adding modern plantings and stone terracing for a timeless, layered aesthetic.",
    year: "2023",
  },
];

export default function Portfolio() {
  const [active, setActive] = useState("All");
  const [lightbox, setLightbox] = useState(null);

  const filtered = active === "All" ? projects : projects.filter((p) => p.category === active);

  const lightboxIdx = lightbox !== null ? filtered.findIndex((p) => p.id === lightbox) : -1;

  const prev = () => {
    const i = (lightboxIdx - 1 + filtered.length) % filtered.length;
    setLightbox(filtered[i].id);
  };
  const next = () => {
    const i = (lightboxIdx + 1) % filtered.length;
    setLightbox(filtered[i].id);
  };

  const activeLightbox = lightbox !== null ? filtered.find((p) => p.id === lightbox) : null;

  return (
    <div>
      {/* Hero */}
      <section className="relative py-40 overflow-hidden">
        <img
          src="https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?w=1920&q=80"
          alt="Portfolio hero"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/65 to-black/50" />
        <div className="relative z-10 max-w-5xl mx-auto px-4 text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <div className="flex items-center justify-center gap-2 mb-5 text-primary-300">
              <span className="h-px w-12 bg-primary-400" />
              <span className="text-sm font-semibold uppercase tracking-widest">Our Portfolio</span>
              <span className="h-px w-12 bg-primary-400" />
            </div>
            <h1 className="font-display text-5xl md:text-7xl font-bold text-white mb-5">
              Our Best Work
            </h1>
            <p className="text-white/75 text-xl max-w-2xl mx-auto">
              Browse our portfolio of stunning outdoor transformations across Portland and the Pacific Northwest.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Filter + Grid */}
      <section className="py-24 bg-stone-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Filter Tabs */}
          <div className="flex flex-wrap gap-3 justify-center mb-14">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setActive(cat)}
                className={`px-5 py-2.5 rounded-full font-semibold text-sm transition-all duration-200 ${
                  active === cat
                    ? "bg-primary-600 text-white shadow-lg shadow-primary-200"
                    : "bg-white text-stone-600 hover:bg-primary-50 hover:text-primary-600 border border-stone-200"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Grid */}
          <motion.div layout className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
            <AnimatePresence>
              {filtered.map((project, i) => (
                <motion.div
                  key={project.id}
                  layout
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ delay: i * 0.05 }}
                  onClick={() => setLightbox(project.id)}
                  className="group relative overflow-hidden rounded-2xl cursor-pointer shadow-md hover:shadow-xl transition-shadow aspect-square"
                >
                  <img
                    src={project.img}
                    alt={project.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-5">
                    <span className="text-primary-300 text-xs font-semibold uppercase tracking-wider mb-1">
                      {project.category}
                    </span>
                    <span className="text-white font-display font-bold text-lg leading-tight">
                      {project.title}
                    </span>
                    <span className="text-white/70 text-xs flex items-center gap-1 mt-1">
                      <MapPin className="w-3 h-3" /> {project.location}
                    </span>
                  </div>
                  {/* Category badge */}
                  <div className="absolute top-3 left-3 bg-black/50 backdrop-blur-sm text-white text-xs font-semibold px-2.5 py-1 rounded-full">
                    {project.category}
                  </div>
                  <div className="absolute top-3 right-3 bg-primary-600 text-white text-xs font-semibold px-2.5 py-1 rounded-full">
                    {project.year}
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </motion.div>
        </div>
      </section>

      {/* Featured Project */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <span className="section-label">Spotlight</span>
            <h2 className="section-title">Featured Project</h2>
          </div>
          <div className="grid lg:grid-cols-2 gap-0 rounded-3xl overflow-hidden shadow-2xl">
            <div className="relative h-80 lg:h-auto">
              <img
                src="https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?w=1000&q=80"
                alt="Modern Backyard Oasis"
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-r from-transparent to-black/20" />
            </div>
            <div className="bg-stone-900 p-10 lg:p-14 flex flex-col justify-center">
              <span className="text-primary-400 text-sm font-semibold uppercase tracking-widest mb-3">Residential · 2024</span>
              <h3 className="font-display text-3xl md:text-4xl font-bold text-white mb-4">Modern Backyard Oasis</h3>
              <p className="text-stone-400 leading-relaxed mb-6">
                Nestled in Lake Oswego, this complete backyard transformation turned a barren slope into a breathtaking outdoor living space. Featuring a custom infinity-edge pool, natural stone patio, outdoor kitchen, and a curated planting scheme that provides year-round interest and privacy.
              </p>
              <div className="grid grid-cols-3 gap-4 mb-8">
                {[["3 months", "Timeline"], ["$185K", "Investment"], ["2024", "Completed"]].map(([val, lbl]) => (
                  <div key={lbl} className="text-center p-3 bg-stone-800 rounded-xl">
                    <div className="font-display font-bold text-primary-400 text-xl">{val}</div>
                    <div className="text-stone-400 text-xs mt-0.5">{lbl}</div>
                  </div>
                ))}
              </div>
              <Link to="/contact" className="btn-primary w-fit">
                Start Your Project <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Lightbox */}
      <AnimatePresence>
        {activeLightbox && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/95 flex items-center justify-center p-4"
            onClick={() => setLightbox(null)}
          >
            <button
              onClick={() => setLightbox(null)}
              className="absolute top-5 right-5 w-10 h-10 bg-white/10 hover:bg-white/20 rounded-full flex items-center justify-center text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
            <button
              onClick={(e) => { e.stopPropagation(); prev(); }}
              className="absolute left-5 top-1/2 -translate-y-1/2 w-12 h-12 bg-white/10 hover:bg-white/20 rounded-full flex items-center justify-center text-white transition-colors"
            >
              <ChevronLeft className="w-6 h-6" />
            </button>
            <button
              onClick={(e) => { e.stopPropagation(); next(); }}
              className="absolute right-5 top-1/2 -translate-y-1/2 w-12 h-12 bg-white/10 hover:bg-white/20 rounded-full flex items-center justify-center text-white transition-colors"
            >
              <ChevronRight className="w-6 h-6" />
            </button>

            <motion.div
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
              onClick={(e) => e.stopPropagation()}
              className="max-w-5xl w-full bg-stone-900 rounded-3xl overflow-hidden"
            >
              <div className="relative h-72 md:h-96">
                <img src={activeLightbox.img} alt={activeLightbox.title} className="w-full h-full object-cover" />
                <div className="absolute top-4 left-4 bg-primary-600 text-white text-xs font-bold px-3 py-1 rounded-full">
                  {activeLightbox.category}
                </div>
              </div>
              <div className="p-8">
                <h3 className="font-display text-2xl font-bold text-white mb-1">{activeLightbox.title}</h3>
                <p className="text-primary-400 text-sm flex items-center gap-1 mb-4">
                  <MapPin className="w-3.5 h-3.5" /> {activeLightbox.location} · {activeLightbox.year}
                </p>
                <p className="text-stone-400 leading-relaxed">{activeLightbox.desc}</p>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* CTA */}
      <section className="py-20 bg-primary-800">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="section-title-white mb-4">Love What You See?</h2>
          <p className="text-primary-200 text-lg mb-8">
            Let's create something equally stunning for your property. Get a free consultation and project estimate today.
          </p>
          <Link to="/contact" className="bg-white text-primary-700 hover:bg-stone-50 font-bold px-8 py-4 rounded-full transition-all duration-300 hover:shadow-xl flex items-center gap-2 mx-auto w-fit">
            Start Your Project <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
}
