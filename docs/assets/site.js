// Mobile menu
(function () {
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
    btn.textContent = open ? 'Close' : 'Menu';
  });
})();

// Enquiry form: compose the enquiry and hand it to WhatsApp or the email app
(function () {
  var form = document.getElementById('enquiry');
  if (!form) return;
  var services = { holiday: 'Holiday package or tour', visa: 'Visa application assistance', tours: 'Holiday package or tour',
                   consulting: 'Consulting & administrative services', business: 'Business enquiry', flights: 'Flights & travel bookings' };
  var pre = new URLSearchParams(location.search).get('service');
  if (pre && services[pre]) form.querySelector('#f-service').value = services[pre];

  var via = 'whatsapp';
  form.querySelectorAll('button[type=submit]').forEach(function (b) {
    b.addEventListener('click', function () { via = b.dataset.via; });
  });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var status = form.querySelector('.form-status');
    var missing = Array.prototype.filter.call(form.querySelectorAll('[required]'), function (el) { return !el.value.trim(); });
    if (missing.length) {
      status.textContent = 'Please fill in your name, email, phone and the service you need.';
      missing[0].focus();
      return;
    }
    var email = form.querySelector('#f-email');
    if (!/^\S+@\S+\.\S+$/.test(email.value.trim())) { status.textContent = 'Please check your email address.'; email.focus(); return; }
    var lines = ['New enquiry — ByGoodness Travels website', ''];
    Array.prototype.forEach.call(form.elements, function (el) {
      if (el.name && el.value.trim()) lines.push(el.name + ': ' + el.value.trim());
    });
    var text = lines.join('\n');
    if (via === 'email') {
      location.href = 'mailto:info@bygoodnesstravels.com?subject=' + encodeURIComponent('Website enquiry: ' + form.querySelector('#f-service').value) + '&body=' + encodeURIComponent(text);
      status.textContent = 'Your email app should open with the enquiry ready to send.';
    } else {
      window.open('https://wa.me/97430995071?text=' + encodeURIComponent(text), '_blank', 'noopener');
      status.textContent = 'WhatsApp should open with your enquiry ready. Press send to deliver it.';
    }
  });
})();
