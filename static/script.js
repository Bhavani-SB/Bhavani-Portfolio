// IntersectionObserver for reveal animations
const io = new IntersectionObserver((entries) => {
  entries.forEach(en => {
    if (en.isIntersecting) {
      en.target.classList.add("visible");
      io.unobserve(en.target);
    }
  });
});
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Skill card gentle rotate
document.querySelectorAll('.skill-card').forEach(card => {
  card.animate(
    [
      { transform: 'translateY(0) rotate(0deg)' },
      { transform: 'translateY(-4px) rotate(1deg)' },
      { transform: 'translateY(0) rotate(0deg)' }
    ],
    { duration: 4200, iterations: Infinity, easing: 'ease-in-out' }
  );
});

// Hero photo hover parallax
const heroPhoto = document.querySelector('.hero-photo img');
document.querySelector('.hero').addEventListener('mousemove', (e) => {
  const rect = document.querySelector('.hero').getBoundingClientRect();
  const cx = rect.left + rect.width/2;
  const cy = rect.top + rect.height/2;
  const dx = (e.clientX - cx)/rect.width*20;
  const dy = (e.clientY - cy)/rect.height*20;
  heroPhoto.style.transform = `translate(${dx}px, ${dy}px) scale(1.02)`;
});
document.querySelector('.hero').addEventListener('mouseleave', () => heroPhoto.style.transform = 'translate(0,0) scale(1)');

// IntersectionObserver for scroll animations
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      // You can assign different animations depending on section
      if (entry.target.classList.contains('skill-card')) {
        entry.target.style.animation = 'bounce-in 0.7s ease forwards';
      } else if (entry.target.classList.contains('timeline-item')) {
        entry.target.style.animation = 'slide-in-bottom 0.6s ease forwards';
      } else if (entry.target.classList.contains('project-card')) {
        entry.target.style.animation = 'scale-in 0.5s ease forwards';
      } else if (entry.target.classList.contains('blog-card')) {
        entry.target.style.animation = 'fade-in 0.5s ease forwards';
      } else {
        entry.target.style.animation = 'scale-in 0.6s ease forwards';
      }
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.2 });

// Observe all reveal elements
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// Scroll reveal
const panels = document.querySelectorAll('.panel');
function revealPanels() {
  panels.forEach(panel=>{
    const top = panel.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;
    if(top < windowHeight*0.85){
      panel.classList.add('visible');
    }
  });
}
window.addEventListener('scroll', revealPanels);
revealPanels();

// Full-screen scroll snap effect
document.documentElement.style.scrollBehavior = 'smooth';

