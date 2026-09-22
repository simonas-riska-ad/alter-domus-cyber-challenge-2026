(() => {
  const expectedReferenceHash = "a92ce522b8bfbe8a729c274638279a1f7f4765f7a52242387872a88112239078";
  const payload = [44,45,73,80,93,95,104,88,39,16,59,39,23,61,59,53,13,55,33,78,65,74,88,67,84];

  async function sha256(value) {
    const data = new TextEncoder().encode(value);
    const digest = await crypto.subtle.digest("SHA-256", data);
    return [...new Uint8Array(digest)]
      .map(byte => byte.toString(16).padStart(2, "0"))
      .join("");
  }

  function deriveFlag(reference) {
    const phrase = payload
      .map((value, index) =>
        String.fromCharCode(value ^ reference.charCodeAt(index % reference.length))
      )
      .join("");

    return "ADCTF{" + phrase + "}";
  }

  async function verify() {
    const input = document.getElementById("approval-code");
    const feedback = document.getElementById("feedback");
    const reference = input.value.trim();

    if (!reference) {
      feedback.textContent = "Enter an approval reference first.";
      return;
    }

    const hash = await sha256(reference);

    if (hash !== expectedReferenceHash) {
      feedback.textContent = "That reference does not match the reviewer record.";
      return;
    }

    feedback.textContent = "";
    document.getElementById("flag-output").textContent = deriveFlag(reference);
    document.getElementById("success-panel").classList.remove("hidden");
    document.getElementById("verify-code").disabled = true;
    input.disabled = true;
  }

  document.getElementById("verify-code").addEventListener("click", verify);
  document.getElementById("approval-code").addEventListener("keydown", event => {
    if (event.key === "Enter") {
      verify();
    }
  });
})();
