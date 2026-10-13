const LOADING_DURATION = 2000; // 1500~2500
const WIPE_DURATION = 1000; // 800~1200

const body = document.body;
const wipe = document.getElementById("wipe");
const intro = document.getElementById("intro");
const main = document.getElementById("main");
const progressText = document.getElementById("progressText");
const progressFill = document.getElementById("progressFill");

let wipeStarted = false;

wipe.style.setProperty("--wipe-duration", `${WIPE_DURATION}ms`);

function setProgress(percent) {
  const value = Math.max(0, Math.min(100, percent));
  progressText.textContent = `${value}%`;
  progressFill.style.transform = `scaleY(${value / 100})`;
}

function runLoading() {
  const start = performance.now();

  function tick(now) {
    const elapsed = now - start;
    const ratio = Math.min(elapsed / LOADING_DURATION, 1);
    const percent = Math.floor(ratio * 100);
    setProgress(percent);

    if (ratio < 1) {
      requestAnimationFrame(tick);
      return;
    }

    setProgress(100);
    startWipe();
  }

  requestAnimationFrame(tick);
}

function startWipe() {
  if (wipeStarted) return;
  wipeStarted = true;
  body.classList.add("is-wiping");
}

wipe.addEventListener("transitionend", (event) => {
  if (!wipeStarted) return;

  if (event.propertyName === "transform") {
    body.classList.add("is-main");
    intro.setAttribute("aria-hidden", "true");
    main.setAttribute("aria-hidden", "false");
    requestAnimationFrame(() => body.classList.add("is-revealing"));
    return;
  }

  if (event.propertyName === "opacity" && body.classList.contains("is-revealing")) {
    wipe.classList.add("hidden");
  }
});

setProgress(0);
runLoading();
