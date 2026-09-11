(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  function bind() {
    const hero = document.querySelector('header.hero-cine');
    if (!hero || hero.dataset.enhanced) return;
    hero.dataset.enhanced = 'true';
    const video = hero.querySelector('.hero-video');
    const play = hero.querySelector('[data-hero-toggle]');
    let userPaused = reduced.matches, visible = true;
    const sync = () => {
      play.textContent = video.paused ? 'Play video' : 'Pause video';
      play.setAttribute('aria-label', video.paused ? 'Play hero video' : 'Pause hero video');
    };
    play.addEventListener('click', () => {
      if (video.paused) { userPaused = false; video.play().catch(sync); }
      else { userPaused = true; video.pause(); }
      sync();
    });
    video.addEventListener('play', sync);
    video.addEventListener('pause', sync);
    video.addEventListener('error', () => {
      video.style.visibility = 'hidden'; play.textContent = 'Image view'; play.disabled = true;
    });
    const observer = new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      if (!visible) video.pause();
      else if (!userPaused && !document.hidden) video.play().catch(sync);
    }, { threshold: .05 });
    observer.observe(hero);
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) video.pause();
      else if (visible && !userPaused) video.play().catch(sync);
    });
    reduced.addEventListener('change', () => {
      userPaused = reduced.matches;
      if (userPaused) video.pause();
      else if (visible && !document.hidden) video.play().catch(sync);
    });
    video.muted = true;
    if (userPaused) video.pause();
    sync();
  }
  const observer = new MutationObserver(bind);
  observer.observe(document.body, { childList: true, subtree: true });
  bind();
})();
