(function () {
  'use strict';

  /* ------------------------------------------------------------------
     CONFIGURAÇÃO COMERCIAL
     Número de parcelas: os materiais da empresa citam "12x" e "18x".
     Enquanto a MSA não confirmar, deixe como null (exibe apenas
     "Parcelamento facilitado"). Para publicar, troque por 12 ou 18.
     ------------------------------------------------------------------ */
  var INSTALLMENTS = null;

  var header = document.querySelector('.site-header');
  var nav = document.getElementById('menu');
  var toggle = document.querySelector('.menu-toggle');
  var desktop = window.matchMedia('(min-width: 980px)');

  /* Parcelamento configurável */
  if (INSTALLMENTS) {
    var label = document.querySelector('[data-installments-label]');
    if (label) label.innerHTML = 'Parcelamento <br>em até ' + INSTALLMENTS + 'x';
    var tag = document.querySelector('[data-installments-tag]');
    if (tag) { tag.textContent = 'Em até ' + INSTALLMENTS + 'x'; tag.hidden = false; }
  }

  /* Ano do rodapé */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* Menu móvel */
  function setMenu(open) {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    document.body.classList.toggle('menu-open', open);
  }

  toggle.addEventListener('click', function () {
    setMenu(toggle.getAttribute('aria-expanded') !== 'true');
  });
  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      setMenu(false);
      toggle.focus();
    }
  });
  desktop.addEventListener('change', function (e) { if (e.matches) setMenu(false); });

  /* Cabeçalho ao rolar */
  function onScroll() { header.classList.toggle('is-scrolled', window.scrollY > 8); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* Revelar ao rolar */
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-visible'); });
  }
})();
