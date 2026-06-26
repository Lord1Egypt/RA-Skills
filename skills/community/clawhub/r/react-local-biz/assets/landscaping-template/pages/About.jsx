import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowRight, Leaf, Award, Users, Heart, Recycle, Star, Sprout } from "lucide-react";

const team = [
  {
    name: "Marcus Rivera",
    role: "Founder & Lead Designer",
    bio: "With 20+ years in landscape architecture, Marcus founded GreenScape Pro with a vision to make world-class landscape design accessible to every homeowner.",
    initials: "MR",
    color: "bg-primary-700",
  },
  {
    name: "Elena Westbrook",
    role: "Head of Garden Design",
    bio: "A certified horticulturist and award-winning designer, Elena brings a botanical expertise and artistic eye that sets our gardens apart.",
    initials: "EW",
    color: "bg-bark-600",
  },
  {
    name: "Tyler Nguyen",
    role: "Hardscaping Director",
    bio: "Tyler leads our hardscaping division with 15 years of experience crafting patios, walls, and outdoor living spaces that stand the test of time.",
    initials: "TN",
    color: "bg-primary-800",
  },
  {
    name: "Priya Patel",
    role: "Client Experience Manager",
    bio: "Priya ensures every client relationship exceeds expectations, from the first consultation through project completion and beyond.",
    initials: "PP",
    color: "bg-earth-600",
  },
];

const values = [
  {
    icon: Recycle,
    title: "Sustainability First",
    desc: "We prioritize eco-friendly practices, native plantings, and sustainable materials in every project. Our goal is to create landscapes that give back to the environment.",
    color: "bg-primary-50 text-primary-700",
  },
  {
    icon: Award,
    title: "Quality Craftsmanship",
    desc: "We never cut corners. Every plant, stone, and installation meets our rigorous quality standards. The result is a landscape that looks great and lasts for decades.",
    color: "bg-earth-50 text-earth-600",
  },
  {
    icon: Heart,
    title: "Customer First",
    desc: "Your vision is our blueprint. We listen deeply, communicate clearly, and are never satisfied until you are. Your satisfaction is our most important deliverable.",
    color: "bg-bark-50 text-bark-600",
  },
];

const milestones = [
  { year: "2009", event: "Founded in Portland with a team of 3" },
  { year: "2012", event: "Expanded to commercial landscaping" },
  { year: "2015", event: "Won Pacific NW Landscape Design Award" },
  { year: "2018", event: "Opened second location in Beaverton" },
  { year: "2021", event: "Launched GreenScape Sustainability Initiative" },
  { year: "2024", event: "Completed 500th project & 50+ industry awards" },
];

const awards = [
  { icon: "🏆", title: "Best Landscape Design", org: "Portland Business Journal, 2024" },
  { icon: "🌿", title: "Green Business Certification", org: "Oregon Environmental Council" },
  { icon: "⭐", title: "5-Star Houzz Pro", org: "Houzz Platform, 2023–2024" },
  { icon: "🎖️", title: "BBB Accredited Business", org: "A+ Rating Since 2012" },
  { icon: "🌱", title: "Sustainable Landscaping Award", org: "NW Landscape Assoc., 2023" },
  { icon: "🏅", title: "Top Rated Contractor", org: "Angi & HomeAdvisor, 2024" },
];

export default function About() {
  return (
    <div>
      {/* Hero */}
      <section className="relative py-40 overflow-hidden">
        <img
          src="https://images.unsplash.com/photo-1541614101331-1a5a3a194e92?w=1920&q=80"
          alt="The GreenScape Pro team"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/65 to-black/50" />
        <div className="relative z-10 max-w-5xl mx-auto px-4 text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <div className="flex items-center justify-center gap-2 mb-5 text-primary-300">
              <span className="h-px w-12 bg-primary-400" />
              <span className="text-sm font-semibold uppercase tracking-widest">About Us</span>
              <span className="h-px w-12 bg-primary-400" />
            </div>
            <h1 className="font-display text-5xl md:text-7xl font-bold text-white mb-5">
              Our Story
            </h1>
            <p className="text-white/75 text-xl max-w-2xl mx-auto">
              15 years of passion, craft, and a deep love for the outdoors — all channeled into transforming your landscape.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Story */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <span className="section-label">Who We Are</span>
              <h2 className="section-title mb-6">Growing Beautiful Landscapes Since 2009</h2>
              <p className="text-stone-600 leading-relaxed mb-5 text-lg">
                GreenScape Pro was born from a simple belief: everyone deserves an outdoor space they love. What started as a two-person crew with a pickup truck and a passion for plants has grown into Portland's most trusted landscaping company with 50+ team members and hundreds of happy clients.
              </p>
              <p className="text-stone-500 leading-relaxed mb-8">
                Our founder, Marcus Rivera, grew up working in his family's garden and developed a deep respect for the natural world. That reverence for nature is baked into everything we do — from our sustainable sourcing practices to the way we design spaces that attract pollinators and support local ecosystems. We don't just make yards look beautiful. We create living, breathing outdoor environments that endure.
              </p>

              <div className="grid grid-cols-2 gap-5">
                {[["50+", "Team Members"], ["500+", "Happy Clients"], ["15+", "Years of Experience"], ["98%", "5-Star Reviews"]].map(([val, lbl]) => (
                  <div key={lbl} className="bg-stone-50 rounded-2xl p-5 border border-stone-100">
                    <div className="font-display font-bold text-primary-600 text-3xl">{val}</div>
                    <div className="text-stone-500 text-sm mt-0.5">{lbl}</div>
                  </div>
                ))}
              </div>
            </motion.div>

            {/* Image with floating elements */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="rounded-3xl overflow-hidden shadow-2xl aspect-[3/4]">
                <img
                  src="https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?w=900&q=80"
                  alt="Beautiful garden we designed"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="absolute -bottom-6 -left-6 bg-primary-600 text-white rounded-2xl shadow-xl p-5 max-w-[180px]">
                <Sprout className="w-7 h-7 mb-2 text-primary-200" />
                <div className="font-display font-bold text-2xl">10,000+</div>
                <div className="text-primary-200 text-xs font-medium mt-0.5">Plants installed in 2024</div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="py-24 bg-stone-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="section-label">What We Stand For</span>
            <h2 className="section-title mb-4">Our Core Values</h2>
            <p className="text-stone-500 text-lg max-w-2xl mx-auto">
              These aren't just words on a wall — they guide every decision we make and every project we take on.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {values.map(({ icon: Icon, title, desc, color }, i) => (
              <motion.div
                key={title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.12 }}
                className="bg-white rounded-3xl p-8 shadow-md hover:shadow-xl transition-shadow"
              >
                <div className={`w-14 h-14 ${color} rounded-2xl flex items-center justify-center mb-5`}>
                  <Icon className="w-7 h-7" />
                </div>
                <h3 className="font-display text-xl font-bold text-stone-900 mb-3">{title}</h3>
                <p className="text-stone-500 leading-relaxed">{desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="py-24 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="section-label">Our Journey</span>
            <h2 className="section-title">Milestones</h2>
          </div>
          <div className="relative">
            <div className="absolute left-8 md:left-1/2 top-0 bottom-0 w-0.5 bg-primary-100" />
            {milestones.map(({ year, event }, i) => (
              <motion.div
                key={year}
                initial={{ opacity: 0, x: i % 2 === 0 ? -20 : 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className={`relative flex items-center mb-8 ${i % 2 === 0 ? "md:flex-row" : "md:flex-row-reverse"} pl-16 md:pl-0`}
              >
                {/* Dot */}
                <div className="absolute left-6 md:left-1/2 md:-translate-x-1/2 w-5 h-5 bg-primary-600 rounded-full border-4 border-white shadow-md z-10" />
                <div className={`md:w-1/2 ${i % 2 === 0 ? "md:pr-12 md:text-right" : "md:pl-12"}`}>
                  <div className="bg-stone-50 rounded-2xl p-5 border border-stone-100 hover:border-primary-200 hover:shadow-md transition-all">
                    <span className="text-primary-600 font-bold text-sm">{year}</span>
                    <p className="text-stone-700 font-medium mt-1">{event}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="py-24 bg-stone-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="section-label">The People Behind the Magic</span>
            <h2 className="section-title mb-4">Meet Our Team</h2>
            <p className="text-stone-500 text-lg max-w-2xl mx-auto">
              Passionate professionals who pour their expertise and heart into every project.
            </p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-7">
            {team.map(({ name, role, bio, initials, color }, i) => (
              <motion.div
                key={name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="bg-white rounded-2xl p-6 shadow-md hover:shadow-xl transition-shadow text-center"
              >
                <div className={`w-20 h-20 ${color} rounded-2xl flex items-center justify-center mx-auto mb-5 text-white font-display font-bold text-2xl shadow-lg`}>
                  {initials}
                </div>
                <h3 className="font-display font-bold text-stone-900 text-lg mb-0.5">{name}</h3>
                <p className="text-primary-600 font-semibold text-sm mb-3">{role}</p>
                <p className="text-stone-500 text-sm leading-relaxed">{bio}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Awards */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="section-label">Recognition</span>
            <h2 className="section-title mb-4">Awards & Certifications</h2>
          </div>
          <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-5">
            {awards.map(({ icon, title, org }, i) => (
              <motion.div
                key={title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.08 }}
                className="flex items-center gap-4 bg-stone-50 rounded-2xl p-5 border border-stone-100 hover:border-primary-200 hover:shadow-md transition-all"
              >
                <span className="text-3xl">{icon}</span>
                <div>
                  <div className="font-semibold text-stone-900 text-sm">{title}</div>
                  <div className="text-stone-500 text-xs mt-0.5">{org}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-primary-800">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="section-title-white mb-4">Work With Our Team</h2>
          <p className="text-primary-200 text-lg mb-8">
            Ready to experience the GreenScape Pro difference? Let's talk about your outdoor vision.
          </p>
          <Link to="/contact" className="bg-white text-primary-700 hover:bg-stone-50 font-bold px-8 py-4 rounded-full transition-all duration-300 hover:shadow-xl flex items-center gap-2 mx-auto w-fit">
            Get in Touch <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
}
