(() => {
  const cookieName = "briefing_access";

  function readCookie(name) {
    const prefix = name + "=";
    const match = document.cookie
      .split(";")
      .map(value => value.trim())
      .find(value => value.startsWith(prefix));

    return match ? decodeURIComponent(match.slice(prefix.length)) : null;
  }

  function ensureSession() {
    let role = readCookie(cookieName);

    if (!role) {
      document.cookie = cookieName + "=viewer; SameSite=Lax";
      role = "viewer";
    }

    return role;
  }

  function decodeVerificationPhrase(role) {
    const payload = [61, 55, 55, 39, 34, 50, 72, 62, 51, 43, 34, 44, 55, 57, 72, 69, 65];

    return payload
      .map((value, index) =>
        String.fromCharCode(value ^ role.charCodeAt(index % role.length))
      )
      .join("");
  }

  function toFlag(phrase) {
    return "ADCTF{" + phrase.toLowerCase().replaceAll("-", "_") + "}";
  }

  function render() {
    const role = ensureSession();
    const currentRole = document.getElementById("current-role");
    const sideRole = document.getElementById("side-role");
    const status = document.getElementById("briefing-status");

    currentRole.textContent = role;
    sideRole.textContent = role;

    if (role === "reviewer") {
      const phrase = decodeVerificationPhrase(role);

      document.getElementById("locked-state").classList.add("hidden");
      document.getElementById("unlocked-state").classList.remove("hidden");
      document.getElementById("flag-output").textContent = toFlag(phrase);
      status.textContent = "Unlocked";
    } else {
      status.textContent = "Locked";
    }
  }

  document.getElementById("refresh-access").addEventListener("click", () => {
    window.location.reload();
  });

  render();
})();
