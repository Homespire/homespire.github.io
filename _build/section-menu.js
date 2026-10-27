
        // Section menu: built from each slide's data-nav-chapter / data-nav-title.
        // Hover the right edge or the tab (desktop), tap the tab (phones), or press M.
        (function () {
            const all = [...document.querySelectorAll('.slide')];
            if (!all.some(s => s.dataset.navTitle)) return;

            const zone = document.createElement('div');
            zone.className = 'navzone';
            const tab = document.createElement('button');
            tab.type = 'button';
            tab.className = 'navtab';
            tab.setAttribute('aria-label', 'Open the section menu');
            tab.innerHTML = '☰<span>Sections</span>';
            const drawer = document.createElement('nav');
            drawer.className = 'navdrawer';
            drawer.setAttribute('aria-label', 'Sections');
            drawer.innerHTML = '<div class="navdrawer-head"><div><strong>Jump to</strong><small>Press M to open or close</small></div>' +
                '<button type="button" class="navdrawer-close" aria-label="Close">✕</button></div><div class="navdrawer-list"></div>';
            const list = drawer.querySelector('.navdrawer-list');

            let chapter = null;
            all.forEach((slide, i) => {
                if (!slide.dataset.navTitle) return;
                if (slide.dataset.navChapter !== chapter) {
                    chapter = slide.dataset.navChapter;
                    const h = document.createElement('div');
                    h.className = 'navchapter';
                    h.textContent = chapter;
                    list.appendChild(h);
                }
                const item = document.createElement('button');
                item.type = 'button';
                item.className = 'navitem';
                item.dataset.index = i;
                item.innerHTML = '<small>' + (i + 1) + '</small><span></span>';
                item.querySelector('span').textContent = slide.dataset.navTitle;
                list.appendChild(item);
            });

            document.body.appendChild(zone);
            document.body.appendChild(tab);
            document.body.appendChild(drawer);

            const onScreen = () => {
                const mid = window.innerHeight / 2;
                return Math.max(0, all.findIndex(s => { const r = s.getBoundingClientRect(); return r.top <= mid && r.bottom > mid; }));
            };
            let closeTimer;
            function open() {
                clearTimeout(closeTimer);
                const cur = onScreen();
                list.querySelectorAll('.navitem').forEach(b => b.classList.toggle('current', +b.dataset.index === cur));
                drawer.classList.add('open');
                const c = list.querySelector('.navitem.current');
                if (c) c.scrollIntoView({ block: 'nearest' });
            }
            function close() { drawer.classList.remove('open'); }
            const isOpen = () => drawer.classList.contains('open');

            // Desktop: hovering the right edge opens it; leaving the menu closes it
            const fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
            if (fine) {
                zone.addEventListener('mouseenter', open);
                tab.addEventListener('mouseenter', open);
                drawer.addEventListener('mouseenter', () => clearTimeout(closeTimer));
                drawer.addEventListener('mouseleave', () => { closeTimer = setTimeout(close, 350); });
            }
            tab.addEventListener('click', () => (isOpen() ? close() : open()));
            drawer.querySelector('.navdrawer-close').addEventListener('click', close);
            list.addEventListener('click', e => {
                const item = e.target.closest('.navitem');
                if (!item) return;
                close();
                all[+item.dataset.index].scrollIntoView({ behavior: 'smooth' });
            });
            document.addEventListener('click', e => {
                if (isOpen() && !drawer.contains(e.target) && !tab.contains(e.target)) close();
            });
            window.addEventListener('keydown', e => {
                if (e.target.matches && e.target.matches('input, select, textarea')) return;
                if (e.key === 'm' || e.key === 'M') {
                    isOpen() ? close() : open();
                    e.preventDefault();
                    e.stopPropagation();
                } else if (e.key === 'Escape' && isOpen()) {
                    close();
                    e.stopPropagation();
                }
            }, true);
        })();
