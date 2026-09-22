(() => {
  const storageKey = "reporting_preferences";
  const payload = [20, 35, 42, 33, 52, 51, 17, 47, 26, 19, 61, 13, 34, 36, 9, 19, 39, 10, 44, 8, 41, 12, 34, 33, 48, 49];

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
