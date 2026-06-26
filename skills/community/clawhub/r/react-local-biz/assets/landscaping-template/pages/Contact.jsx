import { useState } from "react";
import { motion } from "framer-motion";
import { MapPin, Phone, Mail, Clock, ArrowRight, CheckCircle, Star } from "lucide-react";

const services = [
  "Lawn Care & Maintenance",
  "Garden Design & Installation",
  "Tree & Shrub Care",
  "Irrigation Systems",
  "Hardscaping & Patios",
  "Seasonal Cleanup",
  "Other / Not Sure Yet",
];

const hours = [
  ["Monday – Friday", "7:00 AM – 6:00 PM"],
  ["Saturday", "8:00 AM – 4:00 PM"],
  ["Sunday", "Closed"],
];

export default function Contact() {
  const [form, setForm] = useState({ name: "", email: "", phone: "", service: "", message: "" });
  const [submitted, setSubmitted] = useState(false);
  const [errors, setErrors] = useState({});

  const validate = () => {
    const e = {};
    if (!form.name.trim()) e.name = "Name is required";
    if (!form.email.trim() || !/\S+@\S+\.\S+/.test(form.email)) e.email = "Valid email is required";
    if (!form.message.trim()) e.message = "Please tell us about your project";
    return e;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }
    setSubmitted(true);
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    if (errors[e.target.name]) setErrors({ ...errors, [e.target.name]: null });
  };

  return (
    <div>
      {/* Hero */}
      <section className="relative py-40 overflow-hidden">
        <img
          src="https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=1920&q=80"
          alt="Contact hero"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/65 to-black/50" />
        <div className="relative z-10 max-w-5xl mx-auto px-4 text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <div className="flex items-center justify-center gap-2 mb-5 text-primary-300">
              <span className="h-px w-12 bg-primary-400" />
              <span className="text-sm font-semibold uppercase tracking-widest">Contact Us</span>
              <span className="h-px w-12 bg-primary-400" />
            </div>
            <h1 className="font-display text-5xl md:text-7xl font-bold text-white mb-5">
              Let's Talk Landscaping
            </h1>
            <p className="text-white/75 text-xl max-w-2xl mx-auto">
              Ready to transform your outdoor space? Get your free consultation and estimate — no obligation.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-24 bg-stone-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-5 gap-12">
            {/* Form */}
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="lg:col-span-3"
            >
              <div className="bg-white rounded-3xl shadow-xl p-8 md:p-10">
                <h2 className="font-display text-2xl font-bold text-stone-900 mb-2">Get a Free Quote</h2>
                <p className="text-stone-500 mb-8">Fill out the form and we'll be in touch within 24 hours.</p>

                {submitted ? (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="text-center py-12"
                  >
                    <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-5">
                      <CheckCircle className="w-10 h-10 text-primary-600" />
                    </div>
                    <h3 className="font-display text-2xl font-bold text-stone-900 mb-2">Message Sent!</h3>
                    <p className="text-stone-500 max-w-sm mx-auto">
                      Thanks, {form.name.split(" ")[0]}! We'll review your request and reach out within 1 business day.
                    </p>
                    <button
                      onClick={() => { setSubmitted(false); setForm({ name: "", email: "", phone: "", service: "", message: "" }); }}
                      className="btn-outline-green mt-6"
                    >
                      Send Another Message
                    </button>
                  </motion.div>
                ) : (
                  <form onSubmit={handleSubmit} className="space-y-5" noValidate>
                    <div className="grid sm:grid-cols-2 gap-5">
                      <div>
                        <label className="block text-sm font-semibold text-stone-700 mb-1.5">
                          Full Name <span className="text-red-500">*</span>
                        </label>
                        <input
                          name="name"
                          value={form.name}
                          onChange={handleChange}
                          placeholder="John Smith"
                          className={`input-field ${errors.name ? "border-red-400 ring-1 ring-red-400" : ""}`}
                        />
                        {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name}</p>}
                      </div>
                      <div>
                        <label className="block text-sm font-semibold text-stone-700 mb-1.5">
                          Email Address <span className="text-red-500">*</span>
                        </label>
                        <input
                          name="email"
                          type="email"
                          value={form.email}
                          onChange={handleChange}
                          placeholder="john@email.com"
                          className={`input-field ${errors.email ? "border-red-400 ring-1 ring-red-400" : ""}`}
                        />
                        {errors.email && <p className="text-red-500 text-xs mt-1">{errors.email}</p>}
                      </div>
                    </div>

                    <div className="grid sm:grid-cols-2 gap-5">
                      <div>
                        <label className="block text-sm font-semibold text-stone-700 mb-1.5">Phone Number</label>
                        <input
                          name="phone"
                          type="tel"
                          value={form.phone}
                          onChange={handleChange}
                          placeholder="(555) 555-0123"
                          className="input-field"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-semibold text-stone-700 mb-1.5">Service Interested In</label>
                        <select name="service" value={form.service} onChange={handleChange} className="input-field">
                          <option value="">Select a service...</option>
                          {services.map((s) => (
                            <option key={s} value={s}>{s}</option>
                          ))}
                        </select>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-stone-700 mb-1.5">
                        Tell Us About Your Project <span className="text-red-500">*</span>
                      </label>
                      <textarea
                        name="message"
                        value={form.message}
                        onChange={handleChange}
                        rows={5}
                        placeholder="Describe your outdoor space, what you're hoping to achieve, and any specific ideas you have in mind..."
                        className={`input-field resize-none ${errors.message ? "border-red-400 ring-1 ring-red-400" : ""}`}
                      />
                      {errors.message && <p className="text-red-500 text-xs mt-1">{errors.message}</p>}
                    </div>

                    <div className="bg-primary-50 rounded-xl p-4 text-sm text-stone-600 flex items-start gap-3">
                      <CheckCircle className="w-5 h-5 text-primary-600 shrink-0 mt-0.5" />
                      <span>Your information is secure and will never be shared with third parties.</span>
                    </div>

                    <button type="submit" className="btn-primary w-full justify-center text-base py-4">
                      Send Message & Request Quote <ArrowRight className="w-5 h-5" />
                    </button>
                  </form>
                )}
              </div>
            </motion.div>

            {/* Info Panel */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="lg:col-span-2 space-y-6"
            >
              {/* Contact Details */}
              <div className="bg-white rounded-3xl shadow-md p-7">
                <h3 className="font-display text-xl font-bold text-stone-900 mb-5">Get in Touch</h3>
                <div className="space-y-5">
                  <div className="flex items-start gap-4">
                    <div className="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center shrink-0">
                      <MapPin className="w-5 h-5 text-primary-600" />
                    </div>
                    <div>
                      <div className="font-semibold text-stone-900 text-sm mb-0.5">Our Location</div>
                      <div className="text-stone-500 text-sm">1234 Garden Valley Drive<br />Portland, OR 97201</div>
                    </div>
                  </div>
                  <div className="flex items-start gap-4">
                    <div className="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center shrink-0">
                      <Phone className="w-5 h-5 text-primary-600" />
                    </div>
                    <div>
                      <div className="font-semibold text-stone-900 text-sm mb-0.5">Phone</div>
                      <a href="tel:+15555550123" className="text-primary-600 hover:text-primary-700 text-sm font-medium transition-colors">
                        (555) 555-0123
                      </a>
                    </div>
                  </div>
                  <div className="flex items-start gap-4">
                    <div className="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center shrink-0">
                      <Mail className="w-5 h-5 text-primary-600" />
                    </div>
                    <div>
                      <div className="font-semibold text-stone-900 text-sm mb-0.5">Email</div>
                      <a href="mailto:hello@greenscapepro.com" className="text-primary-600 hover:text-primary-700 text-sm font-medium transition-colors">
                        hello@greenscapepro.com
                      </a>
                    </div>
                  </div>
                </div>
              </div>

              {/* Hours */}
              <div className="bg-white rounded-3xl shadow-md p-7">
                <div className="flex items-center gap-2 mb-5">
                  <Clock className="w-5 h-5 text-primary-600" />
                  <h3 className="font-display text-xl font-bold text-stone-900">Business Hours</h3>
                </div>
                <table className="w-full text-sm">
                  <tbody>
                    {hours.map(([day, time]) => (
                      <tr key={day} className="border-b border-stone-100 last:border-0">
                        <td className="py-2.5 text-stone-600 font-medium">{day}</td>
                        <td className={`py-2.5 text-right font-semibold ${time === "Closed" ? "text-stone-400" : "text-stone-800"}`}>
                          {time}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                <p className="text-xs text-stone-400 mt-3">Emergency services available 24/7 for existing clients.</p>
              </div>

              {/* Map Placeholder */}
              <div className="bg-white rounded-3xl shadow-md p-7">
                <h3 className="font-display text-xl font-bold text-stone-900 mb-4">Visit Our Showroom</h3>
                <div className="relative bg-gradient-to-br from-primary-50 to-stone-100 rounded-2xl h-44 overflow-hidden flex items-center justify-center border border-stone-200">
                  <div className="absolute inset-0 opacity-30 bg-[radial-gradient(circle_at_30%_50%,#16a34a_0%,transparent_60%)]" />
                  <div className="text-center">
                    <MapPin className="w-10 h-10 text-primary-600 mx-auto mb-2" />
                    <p className="font-semibold text-stone-800 text-sm">1234 Garden Valley Drive</p>
                    <p className="text-stone-500 text-xs">Portland, OR 97201</p>
                    <a
                      href="https://maps.google.com"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1.5 text-primary-600 font-semibold text-xs mt-3 hover:text-primary-700 transition-colors"
                    >
                      Open in Google Maps <ArrowRight className="w-3.5 h-3.5" />
                    </a>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-14 bg-white border-t border-stone-100">
        <div className="max-w-5xl mx-auto px-4">
          <div className="flex flex-wrap justify-center items-center gap-8 md:gap-14">
            <div className="flex items-center gap-3">
              <div className="flex gap-0.5">
                {Array(5).fill(0).map((_, i) => (
                  <Star key={i} className="w-5 h-5 text-yellow-400 fill-yellow-400" />
                ))}
              </div>
              <div>
                <div className="font-bold text-stone-900 text-sm">4.9/5.0</div>
                <div className="text-stone-500 text-xs">Google Reviews (120+)</div>
              </div>
            </div>
            <div className="h-10 w-px bg-stone-200 hidden md:block" />
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">BBB</div>
              <div>
                <div className="font-bold text-stone-900 text-sm">A+ Rating</div>
                <div className="text-stone-500 text-xs">BBB Accredited Business</div>
              </div>
            </div>
            <div className="h-10 w-px bg-stone-200 hidden md:block" />
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center text-white font-bold text-xs">LIC</div>
              <div>
                <div className="font-bold text-stone-900 text-sm">Licensed & Insured</div>
                <div className="text-stone-500 text-xs">Oregon Lic. #LCB12345</div>
              </div>
            </div>
            <div className="h-10 w-px bg-stone-200 hidden md:block" />
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-orange-500 rounded-lg flex items-center justify-center text-white font-bold text-xs">5★</div>
              <div>
                <div className="font-bold text-stone-900 text-sm">Top Rated Pro</div>
                <div className="text-stone-500 text-xs">Houzz & Angi Certified</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
