// ===========================
// CONTACT PANEL TOGGLE (existing)
const contactLink = document.getElementById('contactLink');
const contactPanel = document.getElementById('contactPanel');
const closeContactBtn = document.getElementById('closeContact');

contactLink.addEventListener('click', function(event) {
  event.preventDefault();
  contactPanel.classList.add('open');
});

closeContactBtn.addEventListener('click', function() {
  contactPanel.classList.remove('open');
});

window.addEventListener('click', function(e) {
  if (
    contactPanel.classList.contains('open') &&
    !contactPanel.contains(e.target) &&
    e.target !== contactLink
  ) {
    contactPanel.classList.remove('open');
  }
});

// ===========================
// LOGIN/SIGNUP PANEL TOGGLE (existing)
const authPanel = document.getElementById('authPanel');
const closeAuthBtn = document.getElementById('closeAuth');
const tabLogin = document.getElementById('tabLogin');
const tabSignup = document.getElementById('tabSignup');
const panelLogin = document.getElementById('panelLogin');
const panelSignup = document.getElementById('panelSignup');

tabLogin.addEventListener('click', () => {
  tabLogin.classList.add('active');
  tabSignup.classList.remove('active');
  tabLogin.setAttribute('aria-selected', 'true');
  tabSignup.setAttribute('aria-selected', 'false');
  tabLogin.tabIndex = 0;
  tabSignup.tabIndex = -1;

  panelLogin.hidden = false;
  panelSignup.hidden = true;
});

tabSignup.addEventListener('click', () => {
  tabSignup.classList.add('active');
  tabLogin.classList.remove('active');
  tabSignup.setAttribute('aria-selected', 'true');
  tabLogin.setAttribute('aria-selected', 'false');
  tabSignup.tabIndex = 0;
  tabLogin.tabIndex = -1;

  panelSignup.hidden = false;
  panelLogin.hidden = true;
});

closeAuthBtn.addEventListener('click', () => {
  authPanel.classList.remove('open');
  authPanel.setAttribute('aria-hidden', 'true');
});

document.getElementById('exploreBtn').addEventListener('click', function() {
  this.classList.add('loading');
});
// ==============
// New Explore logic moved inline in index.html <script> for immediate action on click,
// so no need to add more here unless you want further dynamic behavior for search.
