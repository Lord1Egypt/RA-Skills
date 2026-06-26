function toggleDay(header) {
  const body = header.nextElementSibling;
  const arrow = header.querySelector('.arrow');
  
  body.classList.toggle('show');
  arrow.classList.toggle('open');
}

function toggleGuide(title) {
  const body = title.nextElementSibling;
  body.classList.toggle('show');
}

const STORAGE_KEY = 'trip-prepare-checklist';

function loadChecklist() {
  const saved = localStorage.getItem(STORAGE_KEY);
  return saved ? JSON.parse(saved) : {};
}

function saveChecklist(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

function updateProgress() {
  const checkboxes = document.querySelectorAll('.check-item input[type="checkbox"]');
  const checked = document.querySelectorAll('.check-item input[type="checkbox"]:checked');
  const total = checkboxes.length;
  const checkedCount = checked.length;
  
  const progressCount = document.querySelector('.progress-count');
  const progressFill = document.querySelector('.progress-fill');
  
  if (progressCount) {
    progressCount.textContent = `${checkedCount}/${total}`;
  }
  
  if (progressFill) {
    const percentage = total > 0 ? (checkedCount / total) * 100 : 0;
    progressFill.style.width = `${percentage}%`;
  }
}

function renderTabbar(activePage) {
  const pages = [
    { name: 'index', label: '行程', href: 'index.html' },
    { name: 'prepare', label: '准备', href: 'prepare.html' },
    { name: 'notes', label: '注意', href: 'notes.html' },
    { name: 'budget', label: '预算', href: 'budget.html' }
  ];
  
  const icons = {
    index: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M8 2v4M16 2v4M3 10h18M5 4h14a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V6a2 2 0 012-2z"/><path d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01"/></svg>',
    prepare: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="M9 12l2 2 4-4"/></svg>',
    notes: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>',
    budget: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>'
  };
  
  const nav = document.createElement('nav');
  nav.className = 'tabbar';
  
  pages.forEach(page => {
    const a = document.createElement('a');
    a.href = page.href;
    a.className = 'tabbar-item' + (activePage === page.name ? ' active' : '');
    
    a.innerHTML = `
      <div class="tabbar-icon">${icons[page.name]}</div>
      <span class="tabbar-label">${page.label}</span>
    `;
    
    nav.appendChild(a);
  });
  
  document.body.appendChild(nav);
}

document.addEventListener('DOMContentLoaded', function() {
  const cards = document.querySelectorAll('.glass-card, .prepare-card, .progress-card, .note-category, .budget-section, .budget-total-card, .budget-tip-card');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });
  
  cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
  });

  const checkboxes = document.querySelectorAll('.check-item input[type="checkbox"]');
  if (checkboxes.length > 0) {
    const savedData = loadChecklist();
    
    checkboxes.forEach(checkbox => {
      const id = checkbox.dataset.id;
      if (savedData[id]) {
        checkbox.checked = true;
      }
      
      checkbox.addEventListener('change', function() {
        const data = loadChecklist();
        data[this.dataset.id] = this.checked;
        saveChecklist(data);
        updateProgress();
      });
    });
    
    updateProgress();
  }
});
