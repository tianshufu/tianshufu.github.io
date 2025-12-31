(function($) {

  "use strict";

  // Wait for DOM to be fully loaded
  window.addEventListener('load', () => {

    // One Page Navigation & WOW.js
    // ========================================================================
    const OnePNav = $('.onepage-nev');
    const top_offset = OnePNav.height();
    OnePNav.onePageNav({
      currentClass: 'active',
      scrollOffset: top_offset,
    });

    // Page Loader - Fade out preloader
    // ========================================================================
    const preloader = document.getElementById('preloader');
    if (preloader) {
      preloader.style.display = 'none';
    }

    // Sticky Navigation - Vanilla JS
    // ========================================================================
    const navbar = document.querySelector('.scrolling-navbar');

    window.addEventListener('scroll', () => {
      if (window.scrollY > 200) {
        navbar?.classList.add('top-nav-collapse');
      } else {
        navbar?.classList.remove('top-nav-collapse');
      }
    });

    // Mobile Menu (Slicknav)
    // ========================================================================
    $('.mobile-menu').slicknav({
      prependTo: '.navbar-header',
      parentTag: 'liner',
      allowParentLinks: true,
      duplicate: true,
      label: '',
      closedSymbol: '<i class="icon-arrow-right"></i>',
      openedSymbol: '<i class="icon-arrow-down"></i>',
    });

    // WOW Scroll Spy (Scroll Animations)
    // ========================================================================
    const wow = new WOW({
      mobile: false // Disabled for mobile devices
    });
    wow.init();

    // Nivo Lightbox (if lightbox elements exist)
    // ========================================================================
    const lightboxElements = document.querySelectorAll('.lightbox');
    if (lightboxElements.length > 0) {
      $('.lightbox').nivoLightbox({
        effect: 'fadeScale',
        keyboardNav: true,
      });
    }

    // Counter Animation (if counter elements exist)
    // ========================================================================
    const counterElements = document.querySelectorAll('.counterUp');
    if (counterElements.length > 0) {
      $('.counterUp').counterUp({
        delay: 10,
        time: 1000
      });
    }

    // Back to Top Button - Vanilla JS
    // ========================================================================
    const backToTopBtn = document.querySelector('.back-to-top');
    const SCROLL_OFFSET = 200;
    const SCROLL_DURATION = 500;

    window.addEventListener('scroll', () => {
      if (window.scrollY > SCROLL_OFFSET) {
        backToTopBtn?.classList.add('show');
        backToTopBtn.style.display = 'inline-block';
        backToTopBtn.style.opacity = '1';
      } else {
        backToTopBtn.style.opacity = '0';
        setTimeout(() => {
          if (window.scrollY <= SCROLL_OFFSET) {
            backToTopBtn.style.display = 'none';
          }
        }, 400);
      }
    });

    backToTopBtn?.addEventListener('click', (event) => {
      event.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });

    // WeChat Modal - Vanilla JS (already in HTML, this is just for reference)
    // ========================================================================
    const contactMeBtn = document.getElementById('contactMeBtn');
    const wechatBtn = document.getElementById('wechatBtn');
    const wechatModal = document.getElementById('wechatModal');
    const closeWechatModal = document.getElementById('closeWechatModal');

    if (contactMeBtn && wechatModal) {
      contactMeBtn.addEventListener('click', () => {
        wechatModal.style.display = 'flex';
      });
    }

    if (wechatBtn && wechatModal) {
      wechatBtn.addEventListener('click', (e) => {
        e.preventDefault();
        wechatModal.style.display = 'flex';
      });
    }

    if (closeWechatModal && wechatModal) {
      closeWechatModal.addEventListener('click', () => {
        wechatModal.style.display = 'none';
      });
    }

    if (wechatModal) {
      wechatModal.addEventListener('click', (e) => {
        if (e.target === wechatModal) {
          wechatModal.style.display = 'none';
        }
      });
    }

  });

}(jQuery));
