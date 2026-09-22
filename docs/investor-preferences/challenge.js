(() => {
  const storageKey = "reporting_preferences";
  const payload = [30, 10, 16, 21, 30, 54, 16, 0, 10, 22, 51, 2, 21, 48, 27, 7, 44, 7, 22, 22, 6, 45, 10, 12, 26, 17, 22, 61, 9, 28, 10, 22];

  function defaultPreferences() {
    return {
      theme: "dark",
      compact: false,
      restrictedReports: false
    };
  }

  function encodePreferences(value) {
    return btoa(JSON.stringify(value));
  }

  function decodePreferences(value) {
    try {
      return JSON.parse(atob(value));
    } catch {
      return defaultPreferences();
    }
  }

  function ensurePreferences() {
    let raw = localStorage.getItem(storageKey);

    if (!raw) {
      raw = encodePreferences(defaultPreferences());
      localStorage.setItem(storageKey, raw);
    }

    return decodePreferences(raw);
  }

  function deriveFlag(seed) {
    const phrase = payload
      .map((value, index) =>
        String.fromCharCode(value ^ seed.charCodeAt(index % seed.length))
      )
      .join("");

    return "ADCTF{" + phrase + "}";
  }

  function render() {
    const preferences = ensurePreferences();
    const enabled = preferences.restrictedReports === true;

    document.getElementById("view-label").textContent = enabled ? "Reviewer" : "Standard";
    document.getElementById("restricted-status").textContent = enabled ? "Enabled" : "Disabled";

    if (enabled) {
      document.getElementById("standard-panel").classList.add("hidden");
      document.getElementById("restricted-panel").classList.remove("hidden");
      document.getElementById("flag-output").textContent = deriveFlag("restrictedReports");
    }
  }

  document.getElementById("reload-preferences").addEventListener("click", () => {
    window.location.reload();
  });

  render();
})();
