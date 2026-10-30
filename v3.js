// Portfolio v3: small behaviours only.
(function () {
    'use strict';
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    // Featured rows: play the short loop while the row is hovered or focused.
    if (!reduce) {
        document.querySelectorAll('.feature').forEach(function (row) {
            var v = row.querySelector('video');
            if (!v) return;
            function on() { v.currentTime = 0; v.playbackRate = 0.5; v.classList.add('on'); var p = v.play(); if (p && p.catch) p.catch(function () {}); }
            function off() { v.pause(); v.classList.remove('on'); }
            row.addEventListener('mouseenter', on); row.addEventListener('mouseleave', off);
            row.addEventListener('focusin', on); row.addEventListener('focusout', off);
        });
    }
    // Autoplaying videos respect reduced motion.
    document.querySelectorAll('video[autoplay]').forEach(function (v) { if (reduce) { v.removeAttribute('autoplay'); v.pause(); } });
    // Maya hero: click to pause or play.
    var cabin = document.querySelector('.cabin-hero');
    if (cabin) {
        var cv = cabin.querySelector('video');
        cabin.setAttribute('title', 'Click to pause or play');
        cabin.addEventListener('click', function () { if (cv.paused) cv.play(); else cv.pause(); });
    }
    // Theme toggle: remembers the choice; otherwise follows the system setting.
    var root = document.documentElement, btn = document.querySelector('.theme-toggle');
    function sync() {
        var dark = root.getAttribute('data-theme') === 'dark';
        if (btn) { btn.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme'); btn.setAttribute('aria-pressed', dark ? 'true' : 'false'); }
    }
    if (btn) btn.addEventListener('click', function () {
        var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        try { localStorage.setItem('theme', next); } catch (e) {}
        sync();
    });
    sync();
})();
