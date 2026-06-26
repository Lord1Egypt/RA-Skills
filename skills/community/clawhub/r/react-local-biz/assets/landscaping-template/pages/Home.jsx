import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ChevronDown, Star, ArrowRight, Check, Scissors, Flower2, Trees,
  Droplets, HardHat, Leaf, Quote, Award, Users, ThumbsUp, Trophy
} from "lucide-react";

const fadeUp = { hidden: { opacity: 0, y: 30 }, visible: { opacity: 1, y: 0 } };
const stagger = { visible: { transition: { staggerChildren: 0.12 } } };

const stats = [
  { value: "500+", label: "Projects Completed", icon: Trophy },
  { value: "15+", label: "Years Experience", icon: Award },
  { value: "98%", label: "Client Satisfaction", icon: ThumbsUp },
  { value: "50+", label: "Awards Won", icon: Star },
];

const services = [
  {
    icon: Scissors,
    title: "Lawn Care & Maintenance",
    desc: "Expert mowing, edging, fertilizing, and seasonal treatments to keep your lawn lush and healthy year-round.",
    img: "https://images.unsplash.com/photo-1592417817098-8fd3d9eb14a5?w=600&q=80",
  },
  {
    icon: Flower2,
    title: "Garden Design & Installation",
    desc: "Custom garden designs that blend beauty with function, from colorful perennial beds to serene Zen gardens.",
    img: "https://images.unsplash.com/photo-1585320806297-9794b3e4aaae?w=600&q=80",
  },
  {
    icon: HardHat,
    title: "Hardscaping & Patios",
    desc: "Transform your outdoor living space with stunning patios, walkways, retaining walls, and outdoor kitchens.",
    img: "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=600&q=80",
  },
];

const portfolioImages = [
  { img: "https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?w=800&q=80", title: "Modern Backyard Oasis", cat: "Residential" },
  { img: "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80", title: "Mountain Estate Gardens", cat: "Residential" },
  { img: "https://images.unsplash.com/photo-1558905585-2d3c6b28c3c1?w=800&q=80", title: "Zen Garden Retreat", cat: "Garden Design" },
  { img: "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&q=80", title: "Rolling Meadow Estate", cat: "Residential" },
  { img: "https://images.unsplash.com/photo-1549813069-f95e44d7f498?w=800&q=80", title: "Coastal Luxury Garden", cat: "Commercial" },
  { img: "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&q=80", title: "English Country Garden", cat: "Garden Design" },
];

const testimonials = [
  {
    name: "Sarah Mitchell",
    location: "Portland, OR",
    rating: 5,
    text: "GreenScape Pro completely transformed our backyard. What was once a bare patch of dirt is now a stunning outdoor living space. The team was professional, creative, and delivered beyond our expectations.",
  },
  {
    name: "James & Linda Harlow",
    location: "Lake Oswego, OR",
    rating: 5,
    text: "We hired GreenScape Pro for a full front yard redesign. The results are jaw-dropping. Our neighbors constantly ask who did the work. Absolutely worth every penny!",
  },
  {
    name: "David Chen",
    location: "Beaverton, OR",
    rating: 5,
    text: "Exceptional quality and professionalism. They handled everything from design to installation seamlessly. Our commercial property has never looked better, and clients always comment on it.",
  },
];

const whyUs = [
  "100% eco-friendly practices and sustainable materials",
  "Licensed, insured & certified landscape professionals",
  "Free consultation and detailed project estimates",
  "Satisfaction guarantee on all work performed",
];

export default function Home() {
  return (
    <div>
      {/* ─── HERO ─────────────────────────────── */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <img
          src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1920&q=80"
          alt="Beautiful landscaped garden"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/50 to-black/70" />

        <div className="relative z-10 text-center px-4 max-w-5xl mx-auto">
          <motion.div
            initial="hidden"
            animate="visible"
            variants={stagger}
          >
            <motion.span
              variants={fadeUp}
              className="inline-block bg-primary-600/90 backdrop-blur-sm text-white text-sm font-semibold px-5 py-2 rounded-full mb-6 tracking-wider uppercase"
            >
              🌿 Portland's Premier Landscaping Company
            </motion.span>
            <motion.h1
              variants={fadeUp}
              className="font-display text-5xl md:text-7xl lg:text-8xl font-bold text-white mb-6 leading-[1.05]"
            >
              Transform Your{" "}
              <span className="text-primary-400">Outdoor Space</span>{" "}
              Into a Paradise
            </motion.h1>
            <motion.p
              variants={fadeUp}
              className="text-white/80 text-xl md:text-2xl mb-10 max-w-2xl mx-auto font-light leading-relaxed"
            >
              Professional landscaping services for residential & commercial properties.
              Design. Install. Maintain. Inspire.
            </motion.p>
            <motion.div variants={fadeUp} className="flex flex-wrap gap-4 justify-center">
              <Link to="/contact" className="btn-primary text-base px-8 py-4">
                Get Free Quote <ArrowRight className="w-5 h-5" />
              </Link>
              <Link to="/portfolio" className="btn-outline text-base px-8 py-4">
                View Our Work
              </Link>
            </motion.div>
          </motion.div>
        </div>

        {/* Scroll Indicator */}
        <div className="absolute bottom-10 left-1/2 -translate-x-1/2 text-white/60 flex flex-col items-center gap-2 animate-bounce">
          <span className="text-xs uppercase tracking-widest">Scroll</span>
          <ChevronDown className="w-5 h-5" />
        </div>
      </section>

      {/* ─── STATS BAR ─────────────────────────── */}
      <section className="bg-primary-800 py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map(({ value, label, icon: Icon }) => (
              <motion.div
                key={label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                className="text-center"
              >
                <Icon className="w-7 h-7 text-primary-300 mx-auto mb-2" />
                <div className="font-display text-4xl font-bold text-primary-300 mb-1">{value}</div>
                <div className="text-white/70 text-sm font-medium">{label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── SERVICES PREVIEW ─────────────────── */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <motion.span
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              className="section-label"
            >
              What We Do
            </motion.span>
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="section-title mb-4"
            >
              Expert Services for Every Space
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="text-stone-500 text-lg max-w-2xl mx-auto"
            >
              From concept to completion, we handle every aspect of your outdoor transformation.
            </motion.p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {services.map(({ icon: Icon, title, desc, img }, i) => (
              <motion.div
                key={title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="card group cursor-pointer"
              >
                <div className="relative h-56 overflow-hidden">
                  <img
                    src={img}
                    alt={title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent" />
                  <div className="absolute top-4 left-4 w-11 h-11 bg-primary-600 rounded-xl flex items-center justify-center shadow-lg">
                    <Icon className="w-5 h-5 text-white" />
                  </div>
                </div>
                <div className="p-6">
                  <h3 className="font-display text-xl font-bold text-stone-900 mb-2">{title}</h3>
                  <p className="text-stone-500 text-sm leading-relaxed mb-4">{desc}</p>
                  <Link
                    to="/services"
                    className="text-primary-600 hover:text-primary-700 font-semibold text-sm flex items-center gap-1.5 group/link"
                  >
                    Learn More
                    <ArrowRight className="w-4 h-4 group-hover/link:translate-x-1 transition-transform" />
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>

          <div className="text-center mt-12">
            <Link to="/services" className="btn-outline-green">
              View All Services <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* ─── WHY CHOOSE US ────────────────────── */}
      <section className="py-24 bg-stone-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            {/* Image */}
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="rounded-3xl overflow-hidden shadow-2xl aspect-[4/3]">
                <img
                  src="https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?w=1200&q=80"
                  alt="Our team at work"
                  className="w-full h-full object-cover"
                />
              </div>
              {/* Floating Badge */}
              <div className="absolute -bottom-6 -right-6 bg-white rounded-2xl shadow-xl p-5 border border-stone-100">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
                    <Award className="w-6 h-6 text-primary-600" />
                  </div>
                  <div>
                    <div className="font-display font-bold text-stone-900 text-lg leading-none">15 Years</div>
                    <div className="text-primary-600 text-xs font-semibold mt-0.5">of Excellence</div>
                  </div>
                </div>
              </div>
              {/* Second floating badge */}
              <div className="absolute -top-5 -left-5 bg-primary-600 rounded-2xl shadow-xl p-4">
                <div className="text-center">
                  <div className="font-display font-bold text-white text-2xl leading-none">500+</div>
                  <div className="text-primary-200 text-xs mt-0.5">Happy Clients</div>
                </div>
              </div>
            </motion.div>

            {/* Content */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <span className="section-label">Why Choose Us</span>
              <h2 className="section-title mb-5">
                Crafting Beautiful Outdoor Spaces Since 2009
              </h2>
              <p className="text-stone-500 text-lg leading-relaxed mb-8">
                For over 15 years, GreenScape Pro has been Portland's most trusted landscaping company. Our team of certified designers and horticulturists brings passion, expertise, and creativity to every project — no matter the size.
              </p>

              <ul className="space-y-4 mb-10">
                {whyUs.map((item) => (
                  <li key={item} className="flex items-start gap-3">
                    <div className="w-6 h-6 bg-primary-100 rounded-full flex items-center justify-center shrink-0 mt-0.5">
                      <Check className="w-3.5 h-3.5 text-primary-600" />
                    </div>
                    <span className="text-stone-700 font-medium">{item}</span>
                  </li>
                ))}
              </ul>

              <div className="flex flex-wrap gap-4">
                <Link to="/services" className="btn-primary">
                  Our Services <ArrowRight className="w-5 h-5" />
                </Link>
                <Link to="/contact" className="btn-secondary">
                  Contact Us
                </Link>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ─── PORTFOLIO PREVIEW ────────────────── */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="section-label">Our Work</span>
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="section-title mb-4"
            >
              Recent Projects
            </motion.h2>
            <p className="text-stone-500 text-lg max-w-2xl mx-auto">
              Every project tells a story. Browse our portfolio and envision what we can do for your space.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {portfolioImages.map(({ img, title, cat }, i) => (
              <motion.div
                key={title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.07 }}
                className={`relative overflow-hidden rounded-2xl group cursor-pointer ${i === 0 ? "sm:row-span-2" : ""}`}
              >
                <div className={`${i === 0 ? "h-80 sm:h-full min-h-64" : "h-56"} overflow-hidden`}>
                  <img
                    src={img}
                    alt={title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                  />
                </div>
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-5">
                  <span className="text-primary-300 text-xs font-semibold uppercase tracking-wider mb-1">{cat}</span>
                  <span className="text-white font-display font-bold text-lg leading-tight">{title}</span>
                  <span className="text-white/70 text-sm mt-1 flex items-center gap-1">
                    View Details <ArrowRight className="w-3.5 h-3.5" />
                  </span>
                </div>
                {/* Category badge */}
                <div className="absolute top-4 left-4 bg-black/50 backdrop-blur-sm text-white text-xs font-semibold px-3 py-1 rounded-full">
                  {cat}
                </div>
              </motion.div>
            ))}
          </div>

          <div className="text-center mt-12">
            <Link to="/portfolio" className="btn-outline-green">
              View All Projects <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* ─── TESTIMONIALS ─────────────────────── */}
      <section className="py-24 bg-primary-900 relative overflow-hidden">
        <div className="absolute inset-0 opacity-5">
          <div className="absolute top-0 left-0 w-96 h-96 bg-primary-400 rounded-full -translate-x-1/2 -translate-y-1/2" />
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-primary-400 rounded-full translate-x-1/2 translate-y-1/2" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="text-primary-400 font-semibold text-sm uppercase tracking-[0.2em] block mb-3">Testimonials</span>
            <h2 className="section-title-white mb-4">What Our Clients Say</h2>
            <p className="text-primary-200/70 text-lg max-w-2xl mx-auto">
              Don't just take our word for it — hear from the homeowners and businesses we've helped.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-7">
            {testimonials.map(({ name, location, rating, text }, i) => (
              <motion.div
                key={name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="bg-white/10 backdrop-blur-sm border border-white/10 rounded-2xl p-7 hover:bg-white/15 transition-colors"
              >
                <Quote className="w-8 h-8 text-primary-400 mb-4 opacity-60" />
                <div className="flex gap-1 mb-4">
                  {Array(rating).fill(0).map((_, j) => (
                    <Star key={j} className="w-4 h-4 text-earth-400 fill-earth-400" />
                  ))}
                </div>
                <p className="text-white/85 text-sm leading-relaxed mb-6 italic">"{text}"</p>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                    {name[0]}
                  </div>
                  <div>
                    <div className="text-white font-semibold text-sm">{name}</div>
                    <div className="text-primary-300 text-xs">{location}</div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── CTA BANNER ───────────────────────── */}
      <section className="py-20 bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <Leaf className="absolute top-5 left-10 w-32 h-32 text-white rotate-12" />
          <Leaf className="absolute bottom-5 right-10 w-24 h-24 text-white -rotate-12" />
        </div>
        <div className="relative max-w-4xl mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="font-display text-4xl md:text-5xl font-bold text-white mb-4">
              Ready to Transform Your Landscape?
            </h2>
            <p className="text-white/80 text-xl mb-10 max-w-xl mx-auto">
              Schedule your free consultation today. No obligation, just possibilities.
            </p>
            <div className="flex flex-wrap gap-4 justify-center">
              <Link to="/contact" className="bg-white text-primary-700 hover:bg-stone-50 font-bold px-8 py-4 rounded-full transition-all duration-300 hover:shadow-xl hover:-translate-y-0.5 flex items-center gap-2 text-base">
                Get Your Free Quote Today <ArrowRight className="w-5 h-5" />
              </Link>
              <a href="tel:+15555550123" className="btn-outline text-base px-8 py-4">
                Call (555) 555-0123
              </a>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
