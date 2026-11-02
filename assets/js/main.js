(function () {
  // Mobile menu
  var btn = document.querySelector('.menu');
  var nav = document.getElementById('primary-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
      btn.textContent = open ? 'Close' : 'Menu';
    });
  }

  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Reveal on scroll + animate bars when visible
  var targets = document.querySelectorAll('.reveal, .chart');
  function activate(el) {
    el.classList.add('in');
    el.querySelectorAll('.bar-fill').forEach(function (b) { b.style.width = b.dataset.w; });
  }
  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { activate(e.target); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(activate);
  }

  // Hero security console
  var rows = document.querySelectorAll('.console .log');
  if (rows.length) {
    if (reduced) { rows.forEach(function (r) { r.classList.add('show'); }); }
    else { rows.forEach(function (r, i) { setTimeout(function () { r.classList.add('show'); }, 350 + i * 520); }); }
  }

  // Project filters
  var filters = document.querySelectorAll('.filter');
  var cases = document.querySelectorAll('.case');
  function applyFilter(cat) {
    filters.forEach(function (f) { f.setAttribute('aria-pressed', String(f.dataset.cat === cat)); });
    cases.forEach(function (c) {
      var show = cat === 'all' || (c.dataset.cat || '').split(' ').indexOf(cat) !== -1;
      c.hidden = !show;
      if (show) activate(c.querySelector('.chart') || c);
    });
  }
  filters.forEach(function (f) { f.addEventListener('click', function () { applyFilter(f.dataset.cat); }); });
})();
