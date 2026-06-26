import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowRight, Check, Scissors, Flower2, Trees, Droplets, HardHat, Snowflake, ClipboardList, Pencil, Hammer, Heart } from "lucide-react";

const services = [
  {
    icon: Scissors,
    title: "Lawn Care & Maintenance",
    desc: "A healthy, vibrant lawn is the foundation of a beautiful landscape. Our comprehensive lawn care programs cover everything your turf needs to thrive through every season.",
    img: "https://images.unsplash.com/photo-1592417817098-8fd3d9eb14a5?w=700&q=80",
    features: ["Weekly/bi-weekly mowing", "Professional edging & trimming", "Fertilization programs", "Weed control & prevention", "Aeration & overseeding", "Pest & disease management"],
    color: "primary",
  },
  {
    icon: Flower2,
    title: "Garden Design & Installation",
    desc: "Our award-winning designers work with you to create stunning garden spaces that reflect your personality and complement your home's architecture.",
    img: "https://images.unsplash.com/photo-1585320806297-9794b3e4aaae?w=700&q=80",
    features: ["Custom design consultations", "Seasonal planting plans", "Native plant expertise", "Perennial & annual beds", "Container garden design", "Rain garden installation"],
    color: "primary",
  },
  {
    icon: Trees,
    title: "Tree & Shrub Care",
    desc: "Protect and enhance the trees and shrubs that give your landscape structure, shade, and character with our certified arborist services.",
    img: "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=700&q=80",
    features: ["Professional tree pruning", "Shrub shaping & trimming", "Tree health assessments", "Deep root fertilization", "Stump grinding", "Emergency tree services"],
    color: "primary",
  },
  {
    icon: Droplets,
    title: "Irrigation Systems",
    desc: "Smart irrigation delivers the right amount of water to the right places, saving you money and keeping your landscape looking its best — even in dry summers.",
    img: "https://images.unsplash.com/photo-1563514227147-6d2af01ffb8e?w=700&q=80",
    features: ["Custom system design", "Smart controller installation", "Drip irrigation systems", "Seasonal startup & shutdown", "Leak detection & repair", "Water efficiency audits"],
    color: "primary",
  },
  {
    icon: HardHat,
    title: "Hardscaping & Patios",
    desc: "Extend your living space outdoors with expertly crafted hardscaping elements that add beauty, functionality, and value to your property.",
    img: "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=700&q=80",
    features: ["Custom patio design & installation", "Natural stone & pavers", "Retaining walls", "Walkways & pathways", "Outdoor kitchens & fire pits", "Pergolas & shade structures"],
    color: "primary",
  },
  {
    icon: Snowflake,
    title: "Seasonal Cleanup",
    desc: "Keep your property looking impeccable year-round with our thorough seasonal cleanup services tailored to each change of season.",
    img: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=700&q=80",
    features: ["Spring garden preparation", "Fall leaf removal & cleanup", "Winter plant protection", "Debris removal & hauling", "Bed edging & mulching", "Holiday lighting installation"],
    color: "primary",
  },
];

const process = [
  { icon: ClipboardList, step: "01", title: "Free Consultation", desc: "We meet with you to understand your vision, assess your space, and discuss your budget and timeline." },
  { icon: Pencil, step: "02", title: "Custom Design", desc: "Our designers create a detailed plan tailored to your property, lifestyle, and aesthetic preferences." },
  { icon: Hammer, step: "03", title: "Expert Installation", desc: "Our skilled crews bring the design to life with meticulous attention to detail and quality craftsmanship." },
  { icon: Heart, step: "04", title: "Ongoing Care", desc: "We maintain and nurture your landscape so it continues to thrive and evolve beautifully over time." },
];

export default function Services() {
  return (
    <div>
      {/* Hero */}
      <section className="relative py-40 overflow-hidden">
        <img
          src="https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=1920&q=80"
          alt="Landscaping services"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/65 to-black/50" />
        <div className="relative z-10 max-w-5xl mx-auto px-4 text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <div className="flex items-center justify-center gap-2 mb-5 text-primary-300">
              <span className="h-px w-12 bg-primary-400" />
              <span className="text-sm font-semibold uppercase tracking-widest">Our Services</span>
              <span className="h-px w-12 bg-primary-400" />
            </div>
            <h1 className="font-display text-5xl md:text-7xl font-bold text-white mb-5">
              What We Do Best
            </h1>
            <p className="text-white/75 text-xl max-w-2xl mx-auto">
              From lawn maintenance to full landscape transformations, we offer comprehensive services for every outdoor need.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Services Grid */}
      <section className="py-24 bg-stone-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="section-label">Complete Landscaping Solutions</span>
            <h2 className="section-title">Everything Your Landscape Needs</h2>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {services.map(({ icon: Icon, title, desc, img, features }, i) => (
              <motion.div
                key={title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.08 }}
                className="card group"
              >
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={img}
                    alt={title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
                  <div className="absolute bottom-4 left-4 w-12 h-12 bg-primary-600 rounded-xl flex items-center justify-center shadow-lg">
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                </div>
                <div className="p-6">
                  <h3 className="font-display text-xl font-bold text-stone-900 mb-2">{title}</h3>
                  <p className="text-stone-500 text-sm leading-relaxed mb-5">{desc}</p>
                  <ul className="space-y-2 mb-6">
                    {features.map((f) => (
                      <li key={f} className="flex items-center gap-2 text-sm text-stone-600">
                        <Check className="w-3.5 h-3.5 text-primary-600 shrink-0" />
                        {f}
                      </li>
                    ))}
                  </ul>
                  <Link
                    to="/contact"
                    className="text-primary-600 hover:text-primary-700 font-semibold text-sm flex items-center gap-1.5 group/link"
                  >
                    Get a Quote
                    <ArrowRight className="w-4 h-4 group-hover/link:translate-x-1 transition-transform" />
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Process */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="section-label">Our Approach</span>
            <h2 className="section-title mb-4">How It Works</h2>
            <p className="text-stone-500 text-lg max-w-2xl mx-auto">
              Our streamlined 4-step process makes turning your dream landscape into reality simple and stress-free.
            </p>
          </div>

          <div className="relative">
            {/* Connecting line */}
            <div className="hidden lg:block absolute top-16 left-[12.5%] right-[12.5%] h-0.5 bg-gradient-to-r from-primary-200 via-primary-400 to-primary-200" />

            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
              {process.map(({ icon: Icon, step, title, desc }, i) => (
                <motion.div
                  key={step}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.12 }}
                  className="relative text-center"
                >
                  <div className="relative w-16 h-16 bg-primary-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg shadow-primary-200">
                    <Icon className="w-7 h-7 text-white" />
                    <div className="absolute -top-2 -right-2 w-6 h-6 bg-stone-900 rounded-full flex items-center justify-center text-white text-xs font-bold">
                      {i + 1}
                    </div>
                  </div>
                  <div className="text-primary-300 font-bold text-5xl font-display absolute top-2 left-1/2 -translate-x-1/2 opacity-20 select-none">{step}</div>
                  <h3 className="font-display text-xl font-bold text-stone-900 mb-2">{title}</h3>
                  <p className="text-stone-500 text-sm leading-relaxed">{desc}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-primary-800">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="section-title-white mb-4">Not Sure Which Service You Need?</h2>
          <p className="text-primary-200 text-lg mb-8">
            Our experts will assess your property and recommend the perfect solution for your goals and budget.
          </p>
          <Link to="/contact" className="bg-white text-primary-700 hover:bg-stone-50 font-bold px-8 py-4 rounded-full transition-all duration-300 hover:shadow-xl flex items-center gap-2 mx-auto w-fit">
            Schedule Free Consultation <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
}
